#!/usr/bin/env python3
"""Unit tests for scripts/agent_fabric_check.py."""

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
            "BACKLOG", "READY", "CLAIMED", "ACTIVE", "BLOCKED", "WAITING_HUMAN",
            "READY_FOR_INTEGRATION", "INTEGRATING", "MERGED_VERIFYING",
            "MERGED_VERIFIED", "CANCELLED",
        ],
        "active_states": [
            "CLAIMED", "ACTIVE", "BLOCKED", "WAITING_HUMAN",
            "READY_FOR_INTEGRATION", "INTEGRATING", "MERGED_VERIFYING",
        ],
        "terminal_states": ["MERGED_VERIFIED", "CANCELLED"],
        "human_gate_kinds": [
            "NONE", "EVIDENCE_ATTESTATION", "IRREVERSIBLE_ACTION", "PHYSICAL_SAFETY",
            "EXTERNAL_COMMITMENT", "PRODUCT_DIRECTION",
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
            "parent_branch_pattern": "^work/(ie|ee|cs1|cs2)/[a-z0-9][a-z0-9-]*$",
            "parent_roles": ["IE", "EE", "CS1", "CS2"],
            "human_parent_limit_per_role": 1,
            "child_agent_limit": None,
            "parent_states": [
                "ACTIVE", "BLOCKED", "WAITING_HUMAN", "READY_FOR_INTEGRATION",
                "INTEGRATING", "MERGED_VERIFYING", "COMPLETE",
            ],
            "parent_pr_states": ["DRAFT", "READY", "MERGED"],
        }
    )
    value["integration"] = {
        "scope": "human-parent-to-master",
        "allow_parallel_parent_pull_requests": True,
        "max_parent_pull_requests": 4,
        "max_integration_ready_pull_requests": 1,
        "merge_method": "merge",
        "require_latest_master": True,
        "require_exact_head_ci": True,
        "require_post_merge_verification": True,
        "child_target_must_be_parent_branch": True,
        "shared_change_requires_cross_parent_check": True,
    }
    return value


def gate() -> dict:
    return {
        "kind": "NONE",
        "status": "NOT_REQUIRED",
        "question": None,
        "decision": None,
        "decided_by": None,
        "decided_at": None,
    }


def template_task(schema: int = 1) -> dict:
    value = {
        "schema_version": schema,
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
        "human_gate": gate(),
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
    if schema == 2:
        value.update(
            {
                "parent_id": None,
                "required_for_parent": True,
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


def parent_record(parent_id: str, role: str) -> dict:
    slug = role.lower()
    return {
        "schema_version": 2,
        "id": parent_id,
        "role": role,
        "human_owner": f"human:{slug}",
        "objective": f"Own {role}",
        "priority": "P1",
        "state": "ACTIVE",
        "parent_branch": f"work/{slug}/kreate",
        "child_ids": [],
        "human_gate": gate(),
        "integration": {
            "pull_request": None,
            "pr_state": None,
            "validated_head_sha": None,
            "merge_sha": None,
            "post_merge_verified_at": None,
            "ready_for_integration_at": None,
            "base_master_sha": None,
        },
        "integration_history": [],
        "notes": [],
    }


def legacy_task(task_id: str, *, state: str = "READY", path: str = "scripts/example.py") -> dict:
    value = template_task(1)
    value.update({"id": task_id, "title": task_id, "state": state, "touched_paths": [path]})
    if state in fabric.ACTIVE_OWNERSHIP_STATES or state == "MERGED_VERIFIED":
        value["owner_agent"] = "agent-old"
        value["branch"] = "agent/quality-release/legacy-task"
        value["lease"] = {
            "claimed_at": "2026-09-30T15:00:00Z",
            "heartbeat_at": "2026-09-30T15:30:00Z",
            "ttl_minutes": 360,
        }
    if state in fabric.VALIDATION_REQUIRED_STATES:
        value["acceptance_criteria"] = ["passes"]
        value["validation_commands"] = ["python scripts/agent_fabric_check.py"]
    if state == "INTEGRATING":
        value["integration"]["pull_request"] = 9
    if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
        value["integration"]["merge_sha"] = "a" * 40
    if state == "MERGED_VERIFIED":
        value["integration"].update(
            {
                "pull_request": 9,
                "validated_head_sha": "b" * 40,
                "post_merge_verified_at": "2026-09-30T15:55:00Z",
            }
        )
    return value


def child_task(
    task_id: str,
    *,
    parent_id: str = "HUMAN-CS1",
    state: str = "ACTIVE",
    path: str = "artifacts/child.json",
    owner: str = "agent:worker",
) -> dict:
    value = template_task(2)
    value.update(
        {
            "id": task_id,
            "title": task_id,
            "state": state,
            "parent_id": parent_id,
            "owner_agent": owner,
            "branch": f"agent/api-product/{task_id.lower()}",
            "touched_paths": [path],
            "acceptance_criteria": ["passes"],
            "validation_commands": ["python scripts/agent_fabric_check.py"],
            "lease": {
                "claimed_at": "2026-09-30T15:00:00Z",
                "heartbeat_at": "2026-09-30T15:30:00Z",
                "ttl_minutes": 360,
            },
        }
    )
    if state in {"INTEGRATING", "MERGED_VERIFYING", "MERGED_VERIFIED"}:
        value["child_integration"].update(
            {
                "target_parent_branch": "work/cs1/kreate",
                "validated_head_sha": "a" * 40,
            }
        )
    if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
        value["child_integration"]["integrated_commit_sha"] = "b" * 40
    if state == "MERGED_VERIFIED":
        value["child_integration"]["verified_at"] = "2026-09-30T15:45:00Z"
    return value


class Fixture:
    def __init__(self, *, schema: int = 2) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/coordination/parents").mkdir(parents=True)
        cfg = v2_config() if schema == 2 else base_config()
        (self.root / ".agents/fabric.json").write_text(json.dumps(cfg), encoding="utf-8")
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(
            json.dumps(template_task(schema)), encoding="utf-8"
        )
        if schema == 2:
            (self.root / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").write_text(
                json.dumps(parent_record("HUMAN-IE", "IE")), encoding="utf-8"
            )

    def task(self, value: dict) -> None:
        (self.root / ".agents/coordination/tasks" / f"{value['id']}.json").write_text(
            json.dumps(value), encoding="utf-8"
        )

    def parent(self, value: dict) -> None:
        (self.root / ".agents/coordination/parents" / f"{value['id']}.json").write_text(
            json.dumps(value), encoding="utf-8"
        )

    def close(self) -> None:
        self.tmp.cleanup()


class FabricValidatorTests(unittest.TestCase):
    def validate(self, fx: Fixture):
        return fabric.validate_repository(fx.root, now=NOW)

    def test_schema_v1_legacy_tasks_remain_valid(self) -> None:
        fx = Fixture(schema=1)
        try:
            fx.task(legacy_task("TASK-AAA", state="ACTIVE"))
            errors, warnings, _ = self.validate(fx)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
        finally:
            fx.close()

    def test_four_unique_parent_workstreams_are_valid(self) -> None:
        fx = Fixture()
        try:
            for parent_id, role in (
                ("HUMAN-IE", "IE"),
                ("HUMAN-EE", "EE"),
                ("HUMAN-CS1", "CS1"),
                ("HUMAN-CS2", "CS2"),
            ):
                fx.parent(parent_record(parent_id, role))
            errors, warnings, _ = self.validate(fx)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
        finally:
            fx.close()

    def test_duplicate_parent_role_is_rejected(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-IE", "IE"))
            duplicate = parent_record("HUMAN-IE-ALT", "IE")
            duplicate["human_owner"] = "human:other"
            duplicate["parent_branch"] = "work/ie/alternate"
            fx.parent(duplicate)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("duplicate active parent role IE" in error for error in errors))
        finally:
            fx.close()

    def test_child_missing_parent_is_rejected(self) -> None:
        fx = Fixture()
        try:
            fx.task(child_task("TASK-CHILD-001", parent_id="HUMAN-CS1"))
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("parent HUMAN-CS1 does not exist" in error for error in errors))
        finally:
            fx.close()

    def test_fifty_parallel_active_children_are_valid_without_count_cap(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-CS1", "CS1"))
            for index in range(50):
                fx.task(
                    child_task(
                        f"TASK-C{index:03d}",
                        path=f"artifacts/cs1/{index:03d}.json",
                        owner=f"agent:cs1-{index:03d}",
                    )
                )
            errors, warnings, tasks = self.validate(fx)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(tasks), 50)
        finally:
            fx.close()

    def test_cross_parent_path_collision_is_rejected(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-CS1", "CS1"))
            fx.parent(parent_record("HUMAN-CS2", "CS2"))
            fx.task(child_task("TASK-CS1-A", parent_id="HUMAN-CS1", path="backend/app/decision"))
            second = child_task(
                "TASK-CS2-A",
                parent_id="HUMAN-CS2",
                path="backend/app/decision/router.py",
                owner="agent:cs2-a",
            )
            second["child_integration"]["target_parent_branch"] = None
            fx.task(second)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("path ownership conflict" in error for error in errors))
        finally:
            fx.close()

    def test_dependency_cycle_is_rejected(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-CS1", "CS1"))
            first = child_task("TASK-AAA", state="READY", path="a.txt")
            second = child_task("TASK-BBB", state="READY", path="b.txt")
            first["owner_agent"] = None
            first["branch"] = None
            second["owner_agent"] = None
            second["branch"] = None
            first["lease"] = {"claimed_at": None, "heartbeat_at": None, "ttl_minutes": 360}
            second["lease"] = {"claimed_at": None, "heartbeat_at": None, "ttl_minutes": 360}
            first["depends_on"] = ["TASK-BBB"]
            second["depends_on"] = ["TASK-AAA"]
            fx.task(first)
            fx.task(second)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("dependency cycle" in error for error in errors))
        finally:
            fx.close()

    def test_waiting_human_requires_concrete_critical_gate(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-CS1", "CS1"))
            value = child_task("TASK-AAA", state="WAITING_HUMAN")
            value["human_gate"] = {
                "kind": "PRODUCT_DIRECTION",
                "status": "PENDING",
                "question": None,
                "decision": None,
                "decided_by": None,
                "decided_at": None,
            }
            fx.task(value)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("one concrete human_gate.question" in error for error in errors))
        finally:
            fx.close()

    def test_child_master_target_is_rejected(self) -> None:
        fx = Fixture()
        try:
            fx.parent(parent_record("HUMAN-CS1", "CS1"))
            value = child_task("TASK-AAA", state="INTEGRATING")
            value["child_integration"]["target_parent_branch"] = "master"
            fx.task(value)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("may not target master" in error for error in errors))
        finally:
            fx.close()

    def test_parent_history_rejects_same_child_in_two_batches(self) -> None:
        fx = Fixture()
        try:
            parent = parent_record("HUMAN-CS1", "CS1")
            child = child_task("TASK-CS1-A", state="MERGED_VERIFIED")
            fx.task(child)
            batch = {
                "pull_request": 7,
                "base_master_sha": "a" * 40,
                "validated_head_sha": "b" * 40,
                "merge_sha": "c" * 40,
                "post_merge_verified_at": "2026-09-30T15:50:00Z",
                "child_ids": ["TASK-CS1-A"],
            }
            parent["integration_history"] = [batch, {**batch, "pull_request": 8, "merge_sha": "d" * 40}]
            fx.parent(parent)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("appears in multiple verified parent batches" in error for error in errors))
        finally:
            fx.close()

    def test_parent_history_requires_verified_child(self) -> None:
        fx = Fixture()
        try:
            parent = parent_record("HUMAN-CS1", "CS1")
            fx.task(child_task("TASK-CS1-A", state="ACTIVE"))
            parent["integration_history"] = [
                {
                    "pull_request": 7,
                    "base_master_sha": "a" * 40,
                    "validated_head_sha": "b" * 40,
                    "merge_sha": "c" * 40,
                    "post_merge_verified_at": "2026-09-30T15:50:00Z",
                    "child_ids": ["TASK-CS1-A"],
                }
            ]
            fx.parent(parent)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("historical child TASK-CS1-A is not MERGED_VERIFIED" in error for error in errors))
        finally:
            fx.close()

    def test_legacy_merged_verified_requires_validated_head(self) -> None:
        fx = Fixture(schema=1)
        try:
            value = legacy_task("TASK-AAA", state="MERGED_VERIFIED")
            value["integration"]["validated_head_sha"] = None
            fx.task(value)
            errors, _, _ = self.validate(fx)
            self.assertTrue(any("validated_head_sha" in error for error in errors))
        finally:
            fx.close()


if __name__ == "__main__":
    unittest.main()
