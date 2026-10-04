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


def make_owned(value: dict, *, owner: str, branch: str) -> dict:
    value.update(
        {
            "owner_agent": owner,
            "branch": branch,
            "lease": {
                "claimed_at": "2026-09-30T15:00:00Z",
                "heartbeat_at": "2026-09-30T15:30:00Z",
                "ttl_minutes": 360,
            },
        }
    )
    return value


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/coordination/parents").mkdir(parents=True)
        for relative in (
            ".agents/fabric.json",
            ".agents/TASK_TEMPLATE.json",
            ".agents/PARENT_WORKSTREAM_TEMPLATE.json",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text((REPO / relative).read_text(encoding="utf-8"), encoding="utf-8")

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
        make_owned(active, owner="agent-existing", branch="agent/frontend-ux/existing")
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
        make_owned(value, owner="agent-a", branch="agent/quality-release/task-a")
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
        make_owned(value, owner="agent-a", branch="agent/quality-release/task-a")
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

    def _integrating_child(
        self,
        task_id: str,
        *,
        execution_role: str,
        target_role_branch: str,
        path: str,
        pull_request: int,
    ) -> dict:
        child = make_task(task_id, state="INTEGRATING", path=path)
        child.update(
            {
                "schema_version": 2,
                "agent_kind": "CHILD",
                "parent_id": self.parent["id"],
                "parent_workstream": "ee",
                "execution_role": execution_role,
                "required_for_parent": True,
                "integration": {
                    "pull_request": pull_request,
                    "validated_head_sha": None,
                    "merge_sha": None,
                    "post_merge_verified_at": None,
                },
                "child_integration": {
                    "target_role_branch": target_role_branch,
                    "pull_request": pull_request,
                    "validated_head_sha": "a" * 40,
                    "integrated_commit_sha": None,
                    "verified_at": None,
                },
            }
        )
        make_owned(child, owner=f"agent-{execution_role}", branch=f"agent/{execution_role}/{task_id.lower()}")
        return child

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
        self.assertEqual(child["child_integration"]["target_role_branch"], "role/ehb-embedded-integration")
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
        make_owned(active, owner="agent-existing", branch="agent/cs1/existing")
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

    def test_parent_readiness_uses_role_fan_in_verification_not_master_terminal_state(self) -> None:
        first = self._integrating_child(
            "TASK-ONE",
            execution_role="ehb",
            target_role_branch="role/ehb-embedded-integration",
            path="scripts/one.py",
            pull_request=99,
        )
        second = self._integrating_child(
            "TASK-TWO",
            execution_role="ee",
            target_role_branch="role/ee-physical-systems",
            path="scripts/two.py",
            pull_request=100,
        )
        self.fx.add(first)
        self.fx.add(second)
        parent = self.fx.read_parent(self.parent["id"])
        parent["child_ids"] = ["TASK-ONE", "TASK-TWO"]
        self.fx.add_parent(parent)

        status = agent_task.parent_status(self.fx.root, self.parent["id"])
        self.assertFalse(status["ready_for_integration"])
        self.assertEqual(status["required_remaining"], ["TASK-ONE", "TASK-TWO"])

        verified_first = agent_task.verify_child_role_integration(
            self.fx.root,
            "TASK-ONE",
            owner="agent-ehb",
            integrated_commit_sha="b" * 40,
            at="2026-09-30T16:00:00Z",
        )
        self.assertEqual(verified_first["state"], "INTEGRATING")
        self.assertEqual(verified_first["child_integration"]["integrated_commit_sha"], "b" * 40)
        self.assertEqual(verified_first["child_integration"]["verified_at"], "2026-09-30T16:00:00Z")
        status = agent_task.parent_status(self.fx.root, self.parent["id"])
        self.assertFalse(status["ready_for_integration"])
        self.assertEqual(status["required_remaining"], ["TASK-TWO"])

        agent_task.verify_child_role_integration(
            self.fx.root,
            "TASK-TWO",
            owner="agent-ee",
            integrated_commit_sha="c" * 40,
            at="2026-09-30T16:01:00Z",
        )
        status = agent_task.parent_status(self.fx.root, self.parent["id"])
        self.assertTrue(status["ready_for_integration"])
        self.assertEqual(status["required_remaining"], [])
        self.assertEqual(self.fx.read("TASK-TWO")["state"], "INTEGRATING")

    def test_integrate_child_requires_configured_role_branch(self) -> None:
        child = make_task("TASK-INTEGRATE", state="READY_FOR_INTEGRATION", path="scripts/integrate.py")
        child.update(
            {
                "schema_version": 2,
                "agent_kind": "CHILD",
                "parent_id": self.parent["id"],
                "parent_workstream": "ee",
                "execution_role": "ehb",
                "required_for_parent": True,
            }
        )
        make_owned(child, owner="agent-child", branch="agent/ehb/integrate-child")
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
        self.assertEqual(result["child_integration"]["target_role_branch"], "role/ehb-embedded-integration")

    def test_parent_fanout_spawns_multiple_role_preserving_children(self) -> None:
        spawned = agent_task.fanout_parent_tasks(
            self.fx.root,
            self.parent["id"],
            [
                {
                    "task_id": "TASK-FANOUT-EE",
                    "title": "Measurement slice",
                    "execution_role": "ee",
                    "lane": "hw-measurement",
                    "touched_paths": ["KREATE/HARDWARE/measurement-slice"],
                },
                {
                    "task_id": "TASK-FANOUT-EHB",
                    "title": "Embedded slice",
                    "execution_role": "ehb",
                    "lane": "ehb-integration",
                    "touched_paths": ["KREATE/HARDWARE/embedded-slice"],
                },
            ],
        )
        self.assertEqual([item["id"] for item in spawned], ["TASK-FANOUT-EE", "TASK-FANOUT-EHB"])
        self.assertEqual(spawned[1]["execution_role"], "ehb")
        self.assertEqual(spawned[1]["child_integration"]["target_role_branch"], "role/ehb-embedded-integration")
        self.assertEqual(self.fx.read_parent(self.parent["id"])["child_ids"], ["TASK-FANOUT-EE", "TASK-FANOUT-EHB"])

    def test_parent_fanout_rejects_overlapping_sibling_paths_atomically(self) -> None:
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.fanout_parent_tasks(
                self.fx.root,
                self.parent["id"],
                [
                    {
                        "task_id": "TASK-SIBLING-A",
                        "title": "Sibling A",
                        "execution_role": "cs1",
                        "lane": "cs1",
                        "touched_paths": ["backend/app/decision"],
                    },
                    {
                        "task_id": "TASK-SIBLING-B",
                        "title": "Sibling B",
                        "execution_role": "cs1",
                        "lane": "cs1",
                        "touched_paths": ["backend/app/decision/new.py"],
                    },
                ],
            )
        self.assertEqual(self.fx.read_parent(self.parent["id"])["child_ids"], [])
        self.assertFalse((self.fx.root / ".agents/coordination/tasks/TASK-SIBLING-A.json").exists())
        self.assertFalse((self.fx.root / ".agents/coordination/tasks/TASK-SIBLING-B.json").exists())

    def test_integration_queue_allows_parallel_active_parents_but_one_ready_slot(self) -> None:
        parents = [
            make_parent("HUMAN-IE-OPS", workstream="ie"),
            make_parent("HUMAN-EE-OPS", workstream="ee"),
            make_parent("HUMAN-CS1-OPS", workstream="cs1"),
            make_parent("HUMAN-CS2-OPS", workstream="cs2"),
        ]
        for parent in parents:
            self.fx.add_parent(parent)
        queue = agent_task.parent_integration_queue(self.fx.root)
        self.assertIsNone(queue["active_slot"])
        self.assertEqual(len(queue["parents"]), 5)

        first = self.fx.read_parent("HUMAN-CS1-OPS")
        first["state"] = "READY_FOR_INTEGRATION"
        self.fx.add_parent(first)
        queue = agent_task.parent_integration_queue(self.fx.root)
        self.assertEqual(queue["active_slot"], "HUMAN-CS1-OPS")

        second = self.fx.read_parent("HUMAN-EE-OPS")
        second["state"] = "INTEGRATING"
        self.fx.add_parent(second)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.parent_integration_queue(self.fx.root)


if __name__ == "__main__":
    unittest.main()
