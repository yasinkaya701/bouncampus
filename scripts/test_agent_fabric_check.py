#!/usr/bin/env python3
"""Unit tests for agent_fabric_check.py using only the Python standard library."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import agent_fabric_check as fabric

NOW = datetime(2026, 9, 30, 16, 0, tzinfo=timezone.utc)


def base_config() -> dict:
    return {
        "schema_version": 1,
        "control_branch": "agent-coordination",
        "coordination_task_dir": ".agents/coordination/tasks",
        "branch_pattern": "^agent/[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*$",
        "integration": {
            "max_open_pull_requests": 1,
            "merge_method": "merge",
            "require_latest_master": True,
            "require_exact_head_ci": True,
            "require_post_merge_verification": True,
        },
        "lease": {
            "default_ttl_minutes": 360,
            "heartbeat_on_material_commit": True,
            "stale_reclaim_requires_no_open_task_pr": True,
        },
        "priorities": ["P0", "P1", "P2"],
        "states": [
            "BACKLOG",
            "READY",
            "CLAIMED",
            "ACTIVE",
            "BLOCKED",
            "WAITING_HUMAN",
            "READY_FOR_INTEGRATION",
            "INTEGRATING",
            "MERGED_VERIFYING",
            "MERGED_VERIFIED",
            "CANCELLED",
        ],
        "active_states": [
            "CLAIMED",
            "ACTIVE",
            "BLOCKED",
            "WAITING_HUMAN",
            "READY_FOR_INTEGRATION",
            "INTEGRATING",
            "MERGED_VERIFYING",
        ],
        "terminal_states": ["MERGED_VERIFIED", "CANCELLED"],
        "human_gate_kinds": [
            "NONE",
            "EVIDENCE_ATTESTATION",
            "IRREVERSIBLE_ACTION",
            "PHYSICAL_SAFETY",
            "EXTERNAL_COMMITMENT",
            "PRODUCT_DIRECTION",
        ],
        "human_gate_statuses": ["NOT_REQUIRED", "PENDING", "APPROVED", "REJECTED"],
        "autonomy_default": "AUTONOMOUS",
    }


def fabric_v2_config() -> dict:
    config = base_config()
    config.update(
        {
            "schema_version": 2,
            "coordination_parent_dir": ".agents/coordination/parents",
            "parent_branch_pattern": "^work/(ie|ee|cs1|cs2)/[a-z0-9][a-z0-9-]*$",
            "parent_workstreams": ["ie", "ee", "cs1", "cs2"],
            "child_agent_limit": None,
            "parent_states": [
                "ACTIVE",
                "BLOCKED",
                "WAITING_HUMAN",
                "READY_FOR_INTEGRATION",
                "INTEGRATING",
                "MERGED_VERIFYING",
                "COMPLETE",
            ],
            "parent_pr_states": ["DRAFT", "READY", "MERGED"],
            "role_branches": {
                "ie": "role/ie-customer-discovery",
                "ee": "role/ee-physical-systems",
                "ehb": "role/ehb-embedded-integration",
                "cs1": "role/cs1-decision-intelligence",
                "cs2": "role/cs2-product-strategy",
            },
            "hardware": {
                "ownership": {
                    "ee": ["calibration"],
                    "ehb": ["pcb", "firmware", "communications"],
                    "shared": ["ee-ehb-interface-contract"],
                },
                "evidence_labels": [
                    "ASSUMPTION",
                    "DATASHEET",
                    "CALCULATION",
                    "SIMULATION",
                    "BENCH_TEST",
                    "FIELD_TEST",
                    "PRODUCTION_EVIDENCE",
                ],
            },
        }
    )
    config["integration"].update(
        {
            "max_open_feature_pull_requests_per_role": 3,
            "max_integration_ready_pull_requests": 1,
            "require_latest_role_base": True,
            "allow_parallel_parent_work": True,
            "child_target_must_be_role_branch": True,
        }
    )
    return config


def template_task() -> dict:
    return {
        "schema_version": 1,
        "id": "TASK-TODO",
        "title": "TODO",
        "priority": "P1",
        "lane": "quality-release",
        "state": "BACKLOG",
        "owner_agent": None,
        "branch": None,
        "depends_on": [],
        "touched_paths": [],
        "acceptance_criteria": [],
        "validation_commands": [],
        "human_gate": {
            "kind": "NONE",
            "status": "NOT_REQUIRED",
            "question": None,
            "decision": None,
            "decided_by": None,
            "decided_at": None,
        },
        "lease": {"claimed_at": None, "heartbeat_at": None, "ttl_minutes": 360},
        "blocker": None,
        "integration": {
            "pull_request": None,
            "validated_head_sha": None,
            "merge_sha": None,
            "post_merge_verified_at": None,
        },
        "notes": [],
    }


def parent_template() -> dict:
    return {
        "schema_version": 2,
        "id": "HUMAN-CS1-TODO",
        "workstream": "cs1",
        "human_owner": "human:TODO",
        "objective": "TODO",
        "priority": "P1",
        "state": "ACTIVE",
        "parent_branch": "work/cs1/todo",
        "child_ids": [],
        "human_gate": {
            "kind": "NONE",
            "status": "NOT_REQUIRED",
            "question": None,
            "decision": None,
            "decided_by": None,
            "decided_at": None,
        },
        "integration": {
            "pr_state": "DRAFT",
            "pull_request": None,
            "validated_head_sha": None,
            "merge_sha": None,
            "post_merge_verified_at": None,
        },
        "notes": [],
    }


def task(task_id: str, *, state: str = "READY", path: str = "scripts/example.py") -> dict:
    value = template_task()
    value.update(
        {
            "id": task_id,
            "title": f"Task {task_id}",
            "state": state,
            "touched_paths": [path],
        }
    )
    if state in fabric.ACTIVE_OWNERSHIP_STATES or state == "MERGED_VERIFIED":
        value["owner_agent"] = "agent-test"
        value["branch"] = "agent/quality-release/test-task"
        value["lease"] = {
            "claimed_at": "2026-09-30T15:00:00Z",
            "heartbeat_at": "2026-09-30T15:30:00Z",
            "ttl_minutes": 360,
        }
    if state in fabric.VALIDATION_REQUIRED_STATES:
        value["acceptance_criteria"] = ["validator passes"]
        value["validation_commands"] = ["python scripts/agent_fabric_check.py"]
    if state == "INTEGRATING":
        value["integration"]["pull_request"] = 99
    if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
        value["integration"]["merge_sha"] = "a" * 40
    if state == "MERGED_VERIFIED":
        value["integration"].update(
            {
                "pull_request": 99,
                "validated_head_sha": "b" * 40,
                "post_merge_verified_at": "2026-09-30T15:55:00Z",
            }
        )
    return value


def make_child(
    task_id: str,
    *,
    state: str = "ACTIVE",
    role: str = "cs1",
    target_role_branch: str | None = None,
    path: str = "scripts/child.py",
) -> dict:
    value = task(task_id, state=state, path=path)
    config = fabric_v2_config()
    value.update(
        {
            "schema_version": 2,
            "agent_kind": "CHILD",
            "parent_id": "HUMAN-CS1-TEST",
            "parent_workstream": "cs1",
            "execution_role": role,
            "required_for_parent": True,
            "child_integration": {
                "target_role_branch": target_role_branch or config["role_branches"].get(role),
                "pull_request": 99 if state == "INTEGRATING" else None,
                "validated_head_sha": "c" * 40 if state == "INTEGRATING" else None,
                "integrated_commit_sha": None,
                "verified_at": None,
            },
        }
    )
    return value


class RepoFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/fabric.json").write_text(json.dumps(base_config()), encoding="utf-8")
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template_task()), encoding="utf-8")
        (self.root / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").write_text(
            json.dumps(parent_template()), encoding="utf-8"
        )

    def add(self, value: dict) -> None:
        path = self.root / ".agents/coordination/tasks" / f"{value['id']}.json"
        path.write_text(json.dumps(value), encoding="utf-8")

    def close(self) -> None:
        self.temp.cleanup()


class AgentFabricTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = RepoFixture()

    def tearDown(self) -> None:
        self.repo.close()

    def validate(self):
        return fabric.validate_repository(self.repo.root, now=NOW)

    def test_independent_active_tasks_are_valid(self) -> None:
        self.repo.add(task("TASK-AAA", state="ACTIVE", path="scripts/a.py"))
        second = task("TASK-BBB", state="ACTIVE", path="frontend/src/app")
        second["owner_agent"] = "agent-b"
        second["branch"] = "agent/frontend-ux/task-b"
        self.repo.add(second)
        errors, warnings, _ = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_overlapping_active_paths_fail(self) -> None:
        self.repo.add(task("TASK-AAA", state="ACTIVE", path="frontend/src"))
        second = task("TASK-BBB", state="ACTIVE", path="frontend/src/app/page.tsx")
        second["owner_agent"] = "agent-b"
        second["branch"] = "agent/frontend-ux/task-b"
        self.repo.add(second)
        errors, _, _ = self.validate()
        self.assertTrue(any("path ownership conflict" in error for error in errors))

    def test_dependency_cycle_fails(self) -> None:
        first = task("TASK-AAA")
        second = task("TASK-BBB")
        first["depends_on"] = ["TASK-BBB"]
        second["depends_on"] = ["TASK-AAA"]
        self.repo.add(first)
        self.repo.add(second)
        errors, _, _ = self.validate()
        self.assertTrue(any("dependency cycle" in error for error in errors))

    def test_waiting_human_requires_explicit_gate_question(self) -> None:
        value = task("TASK-AAA", state="WAITING_HUMAN")
        value["human_gate"] = {
            "kind": "PRODUCT_DIRECTION",
            "status": "PENDING",
            "question": None,
            "decision": None,
            "decided_by": None,
            "decided_at": None,
        }
        self.repo.add(value)
        errors, _, _ = self.validate()
        self.assertTrue(any("one concrete human_gate.question" in error for error in errors))

    def test_merged_verified_requires_integration_evidence(self) -> None:
        value = task("TASK-AAA", state="MERGED_VERIFIED")
        value["integration"]["validated_head_sha"] = None
        self.repo.add(value)
        errors, _, _ = self.validate()
        self.assertTrue(any("validated_head_sha" in error for error in errors))


class EHBRoleArchitectureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads((fabric.ROOT / fabric.CONFIG_PATH).read_text(encoding="utf-8"))

    def test_ehb_is_a_first_class_role_branch(self) -> None:
        self.assertEqual(self.config["role_branches"]["ehb"], "role/ehb-embedded-integration")
        self.assertEqual(set(self.config["role_branches"]), {"ie", "ee", "ehb", "cs1", "cs2"})

    def test_hardware_ownership_is_split_between_ee_and_ehb(self) -> None:
        ownership = self.config["hardware"]["ownership"]
        self.assertIn("ee", ownership)
        self.assertIn("ehb", ownership)
        self.assertIn("shared", ownership)
        self.assertNotIn("primary_role", self.config["hardware"])
        self.assertIn("calibration", ownership["ee"])
        self.assertIn("pcb", ownership["ehb"])
        self.assertIn("firmware", ownership["ehb"])
        self.assertIn("communications", ownership["ehb"])
        self.assertIn("ee-ehb-interface-contract", ownership["shared"])

    def test_interface_template_uses_canonical_evidence_labels(self) -> None:
        template = (fabric.ROOT / "KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md").read_text(
            encoding="utf-8"
        )
        evidence_line = next(line for line in template.splitlines() if line.startswith("- Evidence class:"))
        declared = evidence_line.split("`", 2)[1].split(" | ")
        self.assertEqual(declared, self.config["hardware"]["evidence_labels"])


class FabricV2RecutTests(unittest.TestCase):
    def test_schema_v2_config_is_accepted(self) -> None:
        errors: list[str] = []
        fabric.validate_config(fabric_v2_config(), errors)
        self.assertEqual(errors, [])

    def test_repository_config_declares_four_human_parents_and_five_execution_roles(self) -> None:
        config = json.loads((fabric.ROOT / fabric.CONFIG_PATH).read_text(encoding="utf-8"))
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["parent_workstreams"], ["ie", "ee", "cs1", "cs2"])
        self.assertIsNone(config["child_agent_limit"])
        self.assertEqual(set(config["role_branches"]), {"ie", "ee", "ehb", "cs1", "cs2"})
        self.assertEqual(config["role_branches"]["ehb"], "role/ehb-embedded-integration")
        self.assertNotIn("primary_role", config["hardware"])

    def test_unknown_parent_or_execution_role_is_rejected_for_child_task(self) -> None:
        repo = RepoFixture()
        try:
            config = fabric_v2_config()
            (repo.root / ".agents/fabric.json").write_text(json.dumps(config), encoding="utf-8")
            template = template_task()
            template["schema_version"] = 2
            (repo.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template), encoding="utf-8")
            child = make_child("TASK-CHILD")
            child["parent_workstream"] = "unknown"
            child["execution_role"] = "not-a-role"
            child["child_integration"]["target_role_branch"] = "role/not-a-role"
            repo.add(child)
            errors, _, _ = fabric.validate_repository(repo.root, now=NOW)
            self.assertTrue(any("parent_workstream" in error for error in errors))
            self.assertTrue(any("execution_role" in error for error in errors))
        finally:
            repo.close()

    def test_child_target_must_match_execution_role(self) -> None:
        repo = RepoFixture()
        try:
            config = fabric_v2_config()
            (repo.root / ".agents/fabric.json").write_text(json.dumps(config), encoding="utf-8")
            template = template_task()
            template["schema_version"] = 2
            (repo.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template), encoding="utf-8")
            child = make_child(
                "TASK-EHB-TARGET",
                role="ehb",
                target_role_branch="role/ee-physical-systems",
            )
            repo.add(child)
            errors, _, _ = fabric.validate_repository(repo.root, now=NOW)
            self.assertTrue(any("target_role_branch" in error for error in errors))
        finally:
            repo.close()

    def test_verified_role_fan_in_requires_complete_evidence(self) -> None:
        repo = RepoFixture()
        try:
            config = fabric_v2_config()
            (repo.root / ".agents/fabric.json").write_text(json.dumps(config), encoding="utf-8")
            template = template_task()
            template["schema_version"] = 2
            (repo.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template), encoding="utf-8")
            child = make_child("TASK-FANIN", state="INTEGRATING")
            child["child_integration"]["verified_at"] = "2026-09-30T15:55:00Z"
            child["child_integration"]["integrated_commit_sha"] = None
            repo.add(child)
            errors, _, _ = fabric.validate_repository(repo.root, now=NOW)
            self.assertTrue(any("integrated_commit_sha" in error for error in errors))
        finally:
            repo.close()

    def test_fifty_independent_children_have_no_agent_count_cap(self) -> None:
        repo = RepoFixture()
        try:
            config = fabric_v2_config()
            (repo.root / ".agents/fabric.json").write_text(json.dumps(config), encoding="utf-8")
            template = template_task()
            template["schema_version"] = 2
            (repo.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template), encoding="utf-8")
            for index in range(50):
                child = make_child(
                    f"TASK-C{index:02d}",
                    role="cs1",
                    path=f"scratch/child-{index}",
                )
                child["owner_agent"] = f"agent-child-{index}"
                child["branch"] = f"agent/cs1/child-{index}"
                repo.add(child)
            errors, warnings, tasks = fabric.validate_repository(repo.root, now=NOW)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(tasks), 50)
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()
