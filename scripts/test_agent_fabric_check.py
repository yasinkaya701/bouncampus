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


def v2_config() -> dict:
    value = base_config()
    value.update(
        {
            "schema_version": 2,
            "coordination_parent_dir": ".agents/coordination/parents",
            "parent_roles": ["IE", "EE", "CS1", "CS2"],
            "parent_branch_pattern": "^work/(ie|ee|cs1|cs2)/[a-z0-9][a-z0-9-]*$",
        }
    )
    value["integration"] = {
        "max_parent_pull_requests": 4,
        "max_integration_ready_pull_requests": 1,
        "merge_method": "merge",
        "require_latest_master": True,
        "require_exact_head_ci": True,
        "require_post_merge_verification": True,
    }
    return value


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


def v2_template_task() -> dict:
    value = template_task()
    value.update(
        {
            "schema_version": 2,
            "parent_id": None,
            "produces": [],
            "consumes": [],
            "child_integration": {
                "target_parent_branch": None,
                "validated_head_sha": None,
                "integrated_commit_sha": None,
                "verified_at": None,
            },
        }
    )
    return value


def parent_template(parent_id: str = "HUMAN-IE", role: str = "IE") -> dict:
    slug = role.lower()
    return {
        "schema_version": 2,
        "id": parent_id,
        "role": role,
        "human_owner": f"human:{slug}",
        "objective": f"Own the {role} KREATE workstream",
        "priority": "P1",
        "state": "ACTIVE",
        "parent_branch": f"work/{slug}/kreate",
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
            "pull_request": None,
            "pr_state": None,
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


def child_task(
    task_id: str,
    *,
    parent_id: str = "HUMAN-IE",
    state: str = "ACTIVE",
    path: str = "work/example.txt",
    owner: str = "agent:worker",
) -> dict:
    value = v2_template_task()
    value.update(
        {
            "id": task_id,
            "title": f"Child {task_id}",
            "lane": "quality-release",
            "state": state,
            "parent_id": parent_id,
            "owner_agent": owner,
            "branch": f"agent/quality-release/{task_id.lower()}",
            "touched_paths": [path],
            "acceptance_criteria": ["child output validated"],
            "validation_commands": ["python scripts/agent_fabric_check.py"],
            "lease": {
                "claimed_at": "2026-09-30T15:00:00Z",
                "heartbeat_at": "2026-09-30T15:30:00Z",
                "ttl_minutes": 360,
            },
        }
    )
    return value


class RepoFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/coordination/parents").mkdir(parents=True)
        (self.root / ".agents/fabric.json").write_text(json.dumps(base_config()), encoding="utf-8")
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(template_task()), encoding="utf-8")

    def use_v2(self) -> None:
        (self.root / ".agents/fabric.json").write_text(json.dumps(v2_config()), encoding="utf-8")
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(json.dumps(v2_template_task()), encoding="utf-8")
        (self.root / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").write_text(
            json.dumps(parent_template("HUMAN-TODO", "IE")), encoding="utf-8"
        )

    def add(self, value: dict) -> None:
        path = self.root / ".agents/coordination/tasks" / f"{value['id']}.json"
        path.write_text(json.dumps(value), encoding="utf-8")

    def add_parent(self, value: dict) -> None:
        path = self.root / ".agents/coordination/parents" / f"{value['id']}.json"
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

    def test_v2_four_unique_parent_workstreams_are_valid(self) -> None:
        self.repo.use_v2()
        for parent_id, role in (
            ("HUMAN-IE", "IE"),
            ("HUMAN-EE", "EE"),
            ("HUMAN-CS1", "CS1"),
            ("HUMAN-CS2", "CS2"),
        ):
            self.repo.add_parent(parent_template(parent_id, role))
        errors, warnings, _ = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_v2_duplicate_active_parent_role_is_rejected(self) -> None:
        self.repo.use_v2()
        self.repo.add_parent(parent_template("HUMAN-IE", "IE"))
        duplicate = parent_template("HUMAN-IE-ALT", "IE")
        duplicate["human_owner"] = "human:other-ie"
        duplicate["parent_branch"] = "work/ie/alternate"
        self.repo.add_parent(duplicate)
        errors, _, _ = self.validate()
        self.assertTrue(any("duplicate active parent role IE" in error for error in errors))

    def test_v2_child_missing_parent_is_rejected(self) -> None:
        self.repo.use_v2()
        self.repo.add(child_task("TASK-CHILD-001", parent_id="HUMAN-IE", path="tmp/child-001.txt"))
        errors, _, _ = self.validate()
        self.assertTrue(any("parent HUMAN-IE does not exist" in error for error in errors))

    def test_v2_fifty_parallel_children_are_valid_without_count_cap(self) -> None:
        self.repo.use_v2()
        self.repo.add_parent(parent_template("HUMAN-CS1", "CS1"))
        for index in range(50):
            self.repo.add(
                child_task(
                    f"TASK-C{index:03d}",
                    parent_id="HUMAN-CS1",
                    path=f"artifacts/cs1/{index:03d}.json",
                    owner=f"agent:cs1-{index:03d}",
                )
            )
        errors, warnings, tasks = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(tasks), 50)

    def test_v2_cross_parent_child_path_collision_is_rejected(self) -> None:
        self.repo.use_v2()
        self.repo.add_parent(parent_template("HUMAN-CS1", "CS1"))
        self.repo.add_parent(parent_template("HUMAN-CS2", "CS2"))
        self.repo.add(
            child_task(
                "TASK-CS1-A",
                parent_id="HUMAN-CS1",
                path="backend/app/decision",
                owner="agent:cs1-a",
            )
        )
        self.repo.add(
            child_task(
                "TASK-CS2-A",
                parent_id="HUMAN-CS2",
                path="backend/app/decision/router.py",
                owner="agent:cs2-a",
            )
        )
        errors, _, _ = self.validate()
        self.assertTrue(any("path ownership conflict" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
