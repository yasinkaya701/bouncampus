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


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/fabric.json").write_text(
            (REPO / ".agents/fabric.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
        (self.root / ".agents/TASK_TEMPLATE.json").write_text(
            (REPO / ".agents/TASK_TEMPLATE.json").read_text(encoding="utf-8"), encoding="utf-8"
        )

    def add(self, value: dict) -> None:
        (self.root / ".agents/coordination/tasks" / f"{value['id']}.json").write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def read(self, task_id: str) -> dict:
        return json.loads(
            (self.root / ".agents/coordination/tasks" / f"{task_id}.json").read_text(encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
