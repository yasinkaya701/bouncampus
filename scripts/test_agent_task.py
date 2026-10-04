#!/usr/bin/env python3
"""Tests for agent_task.py using only the Python standard library."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import agent_task

REPO = Path(__file__).resolve().parents[1]


def make_task(task_id: str, *, state: str = "READY", path: str = "scripts/example.py") -> dict:
    template = json.loads((REPO / ".agents/TASK_TEMPLATE.json").read_text(encoding="utf-8"))
    template.update(
        {
            "id": task_id,
            "title": task_id,
            "priority": "P1",
            "lane": "quality-release",
            "state": state,
            "touched_paths": [path],
            "acceptance_criteria": ["passes"],
            "validation_commands": ["python -m compileall -q scripts"],
            "notes": [],
        }
    )
    return template


def make_parent(parent_id: str = "HUMAN-EE-HARDWARE", *, workstream: str = "ee") -> dict:
    template = json.loads((REPO / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").read_text(encoding="utf-8"))
    template.update(
        {
            "id": parent_id,
            "workstream": workstream,
            "human_owner": "human:owner",
            "objective": "Coordinate child work safely.",
            "parent_branch": f"work/{workstream}/hardware",
            "child_ids": [],
            "notes": [],
        }
    )
    return template


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/coordination/parents").mkdir(parents=True)
        (self.root / ".agents/fabric.json").write_text(
            (REPO / ".agents/fabric.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(
            (REPO / ".agents/TASK_TEMPLATE.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
        (self.root / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").write_text(
            (REPO / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def add(self, value: dict) -> None:
        (self.root / ".agents/coordination/tasks" / f"{value['id']}.json").write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def add_parent(self, value: dict) -> None:
        (self.root / ".agents/coordination/parents" / f"{value['id']}.json").write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def read(self, task_id: str) -> dict:
        return json.loads(
            (self.root / ".agents/coordination/tasks" / f"{task_id}.json").read_text(encoding="utf-8")
        )

    def read_parent(self, parent_id: str) -> dict:
        return json.loads(
            (self.root / ".agents/coordination/parents" / f"{parent_id}.json").read_text(encoding="utf-8")
        )

    def close(self) -> None:
        self.tmp.cleanup()


class AgentTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def test_claim_sets_owner_branch_and_lease(self) -> None:
        self.fx.add(make_task("TASK-AAA"))
        result = agent_task.claim_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            branch="agent/quality-release/task-a",
            at="2026-09-30T17:00:00Z",
        )
        self.assertEqual(result["state"], "CLAIMED")
        self.assertEqual(result["owner_agent"], "agent-a")
        self.assertEqual(result["branch"], "agent/quality-release/task-a")
        self.assertEqual(result["lease"]["claimed_at"], "2026-09-30T17:00:00Z")

    def test_claim_rejects_active_path_overlap_and_rolls_back(self) -> None:
        active = make_task("TASK-ACTIVE", state="ACTIVE", path="frontend/src")
        active["owner_agent"] = "agent-existing"
        active["branch"] = "agent/frontend-ux/existing"
        active["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add(active)
        self.fx.add(make_task("TASK-AAA", path="frontend/src/app/page.tsx"))
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.claim_task(
                self.fx.root,
                "TASK-AAA",
                owner="agent-a",
                branch="agent/frontend-ux/task-a",
                at="2026-09-30T17:00:00Z",
            )
        self.assertEqual(self.fx.read("TASK-AAA")["state"], "READY")

    def test_claim_rejects_pending_human_gate(self) -> None:
        value = make_task("TASK-AAA")
        value["human_gate"] = {
            "kind": "PRODUCT_DIRECTION",
            "status": "PENDING",
            "question": "Choose A or B?",
            "decision": None,
            "decided_by": None,
            "decided_at": None,
        }
        self.fx.add(value)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.claim_task(
                self.fx.root,
                "TASK-AAA",
                owner="agent-a",
                branch="agent/quality-release/task-a",
            )

    def test_normal_lifecycle_reaches_integrating(self) -> None:
        self.fx.add(make_task("TASK-AAA"))
        agent_task.claim_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            branch="agent/quality-release/task-a",
            at="2026-09-30T17:00:00Z",
        )
        agent_task.transition_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            target="ACTIVE",
            at="2026-09-30T17:01:00Z",
        )
        agent_task.transition_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            target="READY_FOR_INTEGRATION",
            at="2026-09-30T17:02:00Z",
        )
        result = agent_task.transition_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            target="INTEGRATING",
            pull_request=42,
            at="2026-09-30T17:03:00Z",
        )
        self.assertEqual(result["integration"]["pull_request"], 42)
        self.assertEqual(result["state"], "INTEGRATING")

    def test_blocked_requires_complete_evidence(self) -> None:
        value = make_task("TASK-AAA", state="ACTIVE")
        value["owner_agent"] = "agent-a"
        value["branch"] = "agent/quality-release/task-a"
        value["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add(value)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.transition_task(
                self.fx.root,
                "TASK-AAA",
                owner="agent-a",
                target="BLOCKED",
                blocker_reason="service unavailable",
            )

    def test_waiting_human_requires_approval_before_resume(self) -> None:
        value = make_task("TASK-AAA", state="ACTIVE")
        value["owner_agent"] = "agent-a"
        value["branch"] = "agent/quality-release/task-a"
        value["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add(value)
        agent_task.transition_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            target="WAITING_HUMAN",
            human_kind="PRODUCT_DIRECTION",
            human_question="Choose beachhead A or B?",
            at="2026-09-30T17:00:00Z",
        )
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.transition_task(
                self.fx.root,
                "TASK-AAA",
                owner="agent-a",
                target="ACTIVE",
                at="2026-09-30T17:01:00Z",
            )
        agent_task.decide_human_gate(
            self.fx.root,
            "TASK-AAA",
            status="APPROVED",
            decision="Choose A",
            decided_by="human-owner",
            at="2026-09-30T17:02:00Z",
        )
        resumed = agent_task.transition_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            target="ACTIVE",
            at="2026-09-30T17:03:00Z",
        )
        self.assertEqual(resumed["state"], "ACTIVE")
        self.assertEqual(resumed["human_gate"]["status"], "APPROVED")


class ParentChildOperationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.parent = make_parent()
        self.fx.add_parent(self.parent)

    def tearDown(self) -> None:
        self.fx.close()

    def test_spawn_child_records_parent_and_preserves_ehb_as_execution_role(self) -> None:
        child = agent_task.spawn_child_task(
            self.fx.root,
            parent_id=self.parent["id"],
            task_id="TASK-EHB-CHILD",
            title="Implement EHB integration slice",
            execution_role="ehb",
            lane="ehb-integration",
            touched_paths=["KREATE/HARDWARE/child-slice"],
        )
        self.assertEqual(child["schema_version"], 2)
        self.assertEqual(child["agent_kind"], "CHILD")
        self.assertEqual(child["parent_id"], self.parent["id"])
        self.assertEqual(child["parent_workstream"], "ee")
        self.assertEqual(child["execution_role"], "ehb")
        self.assertEqual(
            child["child_integration"]["target_role_branch"],
            "role/ehb-embedded-integration",
        )
        self.assertIn("TASK-EHB-CHILD", self.fx.read_parent(self.parent["id"])["child_ids"])

    def test_spawn_child_rejects_unknown_parent_or_execution_role(self) -> None:
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.spawn_child_task(
                self.fx.root,
                parent_id="HUMAN-CS1-MISSING",
                task_id="TASK-BAD-PARENT",
                title="Bad parent",
                execution_role="cs1",
                lane="cs1",
                touched_paths=["scripts/bad-parent"],
            )
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.spawn_child_task(
                self.fx.root,
                parent_id=self.parent["id"],
                task_id="TASK-BAD-ROLE",
                title="Bad role",
                execution_role="unknown",
                lane="cs1",
                touched_paths=["scripts/bad-role"],
            )

    def test_spawn_child_rejects_active_path_overlap_without_mutating_parent(self) -> None:
        active = make_task("TASK-ACTIVE", state="ACTIVE", path="backend/app/decision")
        active["owner_agent"] = "agent-existing"
        active["branch"] = "agent/cs1/existing"
        active["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add(active)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.spawn_child_task(
                self.fx.root,
                parent_id=self.parent["id"],
                task_id="TASK-CONFLICT",
                title="Conflicting child",
                execution_role="cs1",
                lane="cs1",
                touched_paths=["backend/app/decision/new.py"],
            )
        self.assertEqual(self.fx.read_parent(self.parent["id"])["child_ids"], [])
        self.assertFalse((self.fx.root / ".agents/coordination/tasks/TASK-CONFLICT.json").exists())

    def test_parent_status_requires_all_required_children_to_be_verified(self) -> None:
        first = make_task("TASK-ONE", state="MERGED_VERIFIED", path="scripts/one.py")
        first["schema_version"] = 2
        first["agent_kind"] = "CHILD"
        first["parent_id"] = self.parent["id"]
        first["parent_workstream"] = "ee"
        first["execution_role"] = "ehb"
        first["required_for_parent"] = True
        second = make_task("TASK-TWO", state="READY", path="scripts/two.py")
        second["schema_version"] = 2
        second["agent_kind"] = "CHILD"
        second["parent_id"] = self.parent["id"]
        second["parent_workstream"] = "ee"
        second["execution_role"] = "ee"
        second["required_for_parent"] = True
        self.fx.add(first)
        self.fx.add(second)
        parent = self.fx.read_parent(self.parent["id"])
        parent["child_ids"] = ["TASK-ONE", "TASK-TWO"]
        self.fx.add_parent(parent)

        status = agent_task.parent_status(self.fx.root, self.parent["id"])
        self.assertFalse(status["ready_for_integration"])
        self.assertEqual(status["required_remaining"], ["TASK-TWO"])

        second = self.fx.read("TASK-TWO")
        second.update(
            {
                "state": "MERGED_VERIFIED",
                "owner_agent": "agent-two",
                "branch": "agent/ee/task-two",
                "lease": {
                    "claimed_at": "2026-09-30T15:00:00Z",
                    "heartbeat_at": "2026-09-30T15:30:00Z",
                    "ttl_minutes": 360,
                },
                "integration": {
                    "pull_request": 100,
                    "validated_head_sha": "b" * 40,
                    "merge_sha": "c" * 40,
                    "post_merge_verified_at": "2026-09-30T15:55:00Z",
                },
            }
        )
        self.fx.add(second)
        status = agent_task.parent_status(self.fx.root, self.parent["id"])
        self.assertTrue(status["ready_for_integration"])
        self.assertEqual(status["required_remaining"], [])

    def test_integrate_child_requires_configured_role_branch(self) -> None:
        child = make_task("TASK-INTEGRATE", state="READY_FOR_INTEGRATION", path="scripts/integrate.py")
        child["schema_version"] = 2
        child["agent_kind"] = "CHILD"
        child["parent_id"] = self.parent["id"]
        child["parent_workstream"] = "ee"
        child["execution_role"] = "ehb"
        child["required_for_parent"] = True
        child["owner_agent"] = "agent-child"
        child["branch"] = "agent/ehb/integrate-child"
        child["lease"] = {
            "claimed_at": "2026-09-30T15:00:00Z",
            "heartbeat_at": "2026-09-30T15:30:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add(child)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.integrate_child_task(
                self.fx.root,
                "TASK-INTEGRATE",
                owner="agent-child",
                pull_request=123,
                validated_head_sha="a" * 40,
                target_role_branch="role/ee-physical-systems",
            )
        result = agent_task.integrate_child_task(
            self.fx.root,
            "TASK-INTEGRATE",
            owner="agent-child",
            pull_request=123,
            validated_head_sha="a" * 40,
            target_role_branch="role/ehb-embedded-integration",
        )
        self.assertEqual(result["state"], "INTEGRATING")
        self.assertEqual(result["integration"]["pull_request"], 123)
        self.assertEqual(result["child_integration"]["validated_head_sha"], "a" * 40)
        self.assertEqual(
            result["child_integration"]["target_role_branch"],
            "role/ehb-embedded-integration",
        )


if __name__ == "__main__":
    unittest.main()
