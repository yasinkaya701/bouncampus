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
    """Create a legacy schema-v1 task to protect backward compatibility."""
    template = json.loads((REPO / ".agents/TASK_TEMPLATE.json").read_text(encoding="utf-8"))
    for key in ("parent_id", "required_for_parent", "produces", "consumes", "child_integration"):
        template.pop(key, None)
    template.update(
        {
            "schema_version": 1,
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


def make_parent(parent_id: str, role: str, *, priority: str = "P1") -> dict:
    template = json.loads((REPO / ".agents/PARENT_WORKSTREAM_TEMPLATE.json").read_text(encoding="utf-8"))
    slug = role.lower()
    template.update(
        {
            "id": parent_id,
            "role": role,
            "human_owner": f"human:{slug}",
            "objective": f"Own {role}",
            "priority": priority,
            "state": "ACTIVE",
            "parent_branch": f"work/{slug}/kreate",
            "child_ids": [],
            "notes": [],
        }
    )
    template["integration"] = {
        "pull_request": None,
        "pr_state": None,
        "validated_head_sha": None,
        "merge_sha": None,
        "post_merge_verified_at": None,
        "ready_for_integration_at": None,
    }
    return template


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / ".agents/coordination/tasks").mkdir(parents=True)
        (self.root / ".agents/coordination/parents").mkdir(parents=True)
        for name in ("fabric.json", "TASK_TEMPLATE.json", "PARENT_WORKSTREAM_TEMPLATE.json"):
            (self.root / ".agents" / name).write_text(
                (REPO / ".agents" / name).read_text(encoding="utf-8"), encoding="utf-8"
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

    def test_legacy_claim_sets_owner_branch_and_lease(self) -> None:
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
        self.assertEqual(result["lease"]["claimed_at"], "2026-09-30T17:00:00Z")

    def test_legacy_claim_rejects_active_path_overlap_and_rolls_back(self) -> None:
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

    def test_legacy_normal_lifecycle_reaches_integrating(self) -> None:
        self.fx.add(make_task("TASK-AAA"))
        agent_task.claim_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            branch="agent/quality-release/task-a",
            at="2026-09-30T17:00:00Z",
        )
        agent_task.transition_task(self.fx.root, "TASK-AAA", owner="agent-a", target="ACTIVE")
        agent_task.transition_task(self.fx.root, "TASK-AAA", owner="agent-a", target="READY_FOR_INTEGRATION")
        result = agent_task.transition_task(
            self.fx.root, "TASK-AAA", owner="agent-a", target="INTEGRATING", pull_request=42
        )
        self.assertEqual(result["integration"]["pull_request"], 42)

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
                self.fx.root, "TASK-AAA", owner="agent-a", target="BLOCKED", blocker_reason="service unavailable"
            )

    def test_noncritical_waiting_human_is_rejected(self) -> None:
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
                target="WAITING_HUMAN",
                human_kind="ROUTINE_REVIEW",
                human_question="Review this routine implementation?",
            )

    def test_each_critical_human_gate_is_allowed(self) -> None:
        for index, kind in enumerate(
            [
                "EVIDENCE_ATTESTATION",
                "IRREVERSIBLE_ACTION",
                "PHYSICAL_SAFETY",
                "EXTERNAL_COMMITMENT",
                "PRODUCT_DIRECTION",
            ]
        ):
            task_id = f"TASK-GATE-{index}"
            value = make_task(task_id, state="ACTIVE", path=f"tmp/gate-{index}")
            value["owner_agent"] = "agent-a"
            value["branch"] = f"agent/quality-release/gate-{index}"
            value["lease"] = {
                "claimed_at": "2026-09-30T16:00:00Z",
                "heartbeat_at": "2026-09-30T16:55:00Z",
                "ttl_minutes": 360,
            }
            self.fx.add(value)
            result = agent_task.transition_task(
                self.fx.root,
                task_id,
                owner="agent-a",
                target="WAITING_HUMAN",
                human_kind=kind,
                human_question=f"Approve {kind}?",
            )
            self.assertEqual(result["human_gate"]["kind"], kind)

    def test_spawn_and_claim_child_under_parent(self) -> None:
        self.fx.add_parent(make_parent("HUMAN-CS1", "CS1"))
        child = agent_task.spawn_child(
            self.fx.root,
            parent_id="HUMAN-CS1",
            task_id="TASK-CS1-BASELINE",
            title="Baseline",
            lane="api-product",
            priority="P0",
            touched_paths=["backend/app/decision/baseline.py"],
        )
        self.assertEqual(child["parent_id"], "HUMAN-CS1")
        claimed = agent_task.claim_task(
            self.fx.root,
            "TASK-CS1-BASELINE",
            owner="agent:baseline",
            branch="agent/api-product/cs1-baseline",
            at="2026-09-30T17:00:00Z",
        )
        self.assertEqual(claimed["state"], "CLAIMED")

    def test_v2_child_cannot_use_legacy_master_integration(self) -> None:
        self.fx.add_parent(make_parent("HUMAN-CS1", "CS1"))
        agent_task.spawn_child(
            self.fx.root,
            parent_id="HUMAN-CS1",
            task_id="TASK-CS1-A",
            title="A",
            lane="api-product",
            priority="P1",
            touched_paths=["backend/app/a.py"],
        )
        agent_task.claim_task(
            self.fx.root,
            "TASK-CS1-A",
            owner="agent:a",
            branch="agent/api-product/cs1-a",
        )
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="ACTIVE")
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="READY_FOR_INTEGRATION")
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.transition_task(
                self.fx.root, "TASK-CS1-A", owner="agent:a", target="INTEGRATING", pull_request=99
            )
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.integrate_child(
                self.fx.root,
                "TASK-CS1-A",
                owner="agent:a",
                target_parent_branch="master",
                validated_head_sha="a" * 40,
            )

    def test_child_lifecycle_integrates_only_into_parent_branch(self) -> None:
        self.fx.add_parent(make_parent("HUMAN-CS1", "CS1"))
        agent_task.spawn_child(
            self.fx.root,
            parent_id="HUMAN-CS1",
            task_id="TASK-CS1-A",
            title="A",
            lane="api-product",
            priority="P1",
            touched_paths=["backend/app/a.py"],
        )
        agent_task.claim_task(
            self.fx.root,
            "TASK-CS1-A",
            owner="agent:a",
            branch="agent/api-product/cs1-a",
        )
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="ACTIVE")
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="READY_FOR_INTEGRATION")
        integrated = agent_task.integrate_child(
            self.fx.root,
            "TASK-CS1-A",
            owner="agent:a",
            target_parent_branch="work/cs1/kreate",
            validated_head_sha="a" * 40,
        )
        self.assertEqual(integrated["state"], "INTEGRATING")
        verified = agent_task.verify_child(
            self.fx.root,
            "TASK-CS1-A",
            owner="agent:a",
            integrated_commit_sha="b" * 40,
        )
        self.assertEqual(verified["state"], "MERGED_VERIFIED")
        self.assertEqual(verified["child_integration"]["target_parent_branch"], "work/cs1/kreate")

    def test_fanout_accepts_fifty_children_without_hard_cap(self) -> None:
        self.fx.add_parent(make_parent("HUMAN-CS1", "CS1"))
        specs = [
            {
                "id": f"TASK-CS1-{index:03d}",
                "title": f"CS1 child {index}",
                "lane": "api-product",
                "priority": "P1",
                "touched_paths": [f"artifacts/cs1/{index:03d}.json"],
            }
            for index in range(50)
        ]
        results = agent_task.fanout_children(self.fx.root, parent_id="HUMAN-CS1", specs=specs)
        self.assertEqual(len(results), 50)
        status = agent_task.parent_status(self.fx.root, "HUMAN-CS1")
        self.assertEqual(status["children"], 50)
        self.assertEqual(status["required_children"], 50)

    def test_parent_readiness_ignores_optional_child_but_requires_required_child(self) -> None:
        self.fx.add_parent(make_parent("HUMAN-EE", "EE"))
        required = agent_task.spawn_child(
            self.fx.root,
            parent_id="HUMAN-EE",
            task_id="TASK-EE-REQ",
            title="Required",
            lane="hw-measurement",
            priority="P0",
            touched_paths=["hardware/required.md"],
        )
        agent_task.spawn_child(
            self.fx.root,
            parent_id="HUMAN-EE",
            task_id="TASK-EE-OPT",
            title="Optional",
            lane="hw-measurement",
            priority="P2",
            touched_paths=["hardware/optional.md"],
            required_for_parent=False,
        )
        self.assertFalse(agent_task.parent_status(self.fx.root, "HUMAN-EE")["ready_for_parent_integration"])
        required.update(
            {
                "state": "MERGED_VERIFIED",
                "owner_agent": "agent:req",
                "branch": "agent/hw-measurement/ee-req",
                "lease": {
                    "claimed_at": "2026-09-30T16:00:00Z",
                    "heartbeat_at": "2026-09-30T16:55:00Z",
                    "ttl_minutes": 360,
                },
            }
        )
        required["child_integration"] = {
            "target_parent_branch": "work/ee/kreate",
            "validated_head_sha": "a" * 40,
            "integrated_commit_sha": "b" * 40,
            "verified_at": "2026-09-30T17:00:00Z",
        }
        self.fx.add(required)
        self.assertTrue(agent_task.parent_status(self.fx.root, "HUMAN-EE")["ready_for_parent_integration"])

    def test_integration_queue_is_priority_then_unblocking_then_oldest_then_id(self) -> None:
        first = make_parent("HUMAN-IE", "IE", priority="P1")
        second = make_parent("HUMAN-CS1", "CS1", priority="P0")
        third = make_parent("HUMAN-CS2", "CS2", priority="P0")
        for parent, ready_at in (
            (first, "2026-09-30T17:00:00Z"),
            (second, "2026-09-30T17:05:00Z"),
            (third, "2026-09-30T17:01:00Z"),
        ):
            parent["state"] = "READY_FOR_INTEGRATION"
            parent["integration"]["pr_state"] = "DRAFT"
            parent["integration"]["ready_for_integration_at"] = ready_at
            self.fx.add_parent(parent)
        queue = agent_task.integration_queue(self.fx.root)
        self.assertEqual([item["parent_id"] for item in queue], ["HUMAN-CS2", "HUMAN-CS1", "HUMAN-IE"])


if __name__ == "__main__":
    unittest.main()
