#!/usr/bin/env python3
"""Standard-library tests for the BOUNCAMPUS parent/child task CLI."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import agent_task

REPO = Path(__file__).resolve().parents[1]


def legacy_task(task_id: str, *, state: str = "READY", path: str = "scripts/example.py") -> dict:
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


def parent_record(parent_id: str, role: str, *, priority: str = "P1") -> dict:
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
            "integration_history": [],
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
        "base_master_sha": None,
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

    def add_task(self, value: dict) -> None:
        (self.root / ".agents/coordination/tasks" / f"{value['id']}.json").write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def add_parent(self, value: dict) -> None:
        (self.root / ".agents/coordination/parents" / f"{value['id']}.json").write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )

    def close(self) -> None:
        self.tmp.cleanup()


class AgentTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()

    def tearDown(self) -> None:
        self.fx.close()

    def _add_parent(self, parent_id: str = "HUMAN-CS1", role: str = "CS1", priority: str = "P1") -> None:
        self.fx.add_parent(parent_record(parent_id, role, priority=priority))

    def _spawn(self, task_id: str, *, parent_id: str = "HUMAN-CS1", path: str | None = None, **kwargs):
        return agent_task.spawn_child(
            self.fx.root,
            parent_id=parent_id,
            task_id=task_id,
            title=task_id,
            lane=kwargs.pop("lane", "api-product"),
            priority=kwargs.pop("priority", "P1"),
            touched_paths=[path or f"artifacts/{task_id.lower()}.json"],
            **kwargs,
        )

    def _verify_child(self, task_id: str, *, parent_id: str = "HUMAN-CS1", owner: str = "agent:test") -> None:
        role = parent_id.removeprefix("HUMAN-").lower()
        agent_task.claim_task(
            self.fx.root,
            task_id,
            owner=owner,
            branch=f"agent/api-product/{task_id.lower()}",
            at="2026-09-30T17:00:00Z",
        )
        agent_task.transition_task(self.fx.root, task_id, owner=owner, target="ACTIVE", at="2026-09-30T17:01:00Z")
        agent_task.transition_task(
            self.fx.root, task_id, owner=owner, target="READY_FOR_INTEGRATION", at="2026-09-30T17:02:00Z"
        )
        agent_task.integrate_child(
            self.fx.root,
            task_id,
            owner=owner,
            target_parent_branch=f"work/{role}/kreate",
            validated_head_sha="a" * 40,
            at="2026-09-30T17:03:00Z",
        )
        agent_task.verify_child(
            self.fx.root,
            task_id,
            owner=owner,
            integrated_commit_sha="b" * 40,
            at="2026-09-30T17:04:00Z",
        )

    def test_legacy_claim_still_works_under_v2_fabric(self) -> None:
        self.fx.add_task(legacy_task("TASK-AAA"))
        result = agent_task.claim_task(
            self.fx.root,
            "TASK-AAA",
            owner="agent-a",
            branch="agent/quality-release/task-a",
            at="2026-09-30T17:00:00Z",
        )
        self.assertEqual(result["state"], "CLAIMED")

    def test_v2_child_requires_agent_identity(self) -> None:
        self._add_parent()
        self._spawn("TASK-CS1-A")
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.claim_task(
                self.fx.root,
                "TASK-CS1-A",
                owner="human:yasin",
                branch="agent/api-product/cs1-a",
            )

    def test_noncritical_waiting_human_is_rejected(self) -> None:
        value = legacy_task("TASK-AAA", state="ACTIVE")
        value["owner_agent"] = "agent-a"
        value["branch"] = "agent/quality-release/task-a"
        value["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add_task(value)
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.transition_task(
                self.fx.root,
                "TASK-AAA",
                owner="agent-a",
                target="WAITING_HUMAN",
                human_kind="ROUTINE_REVIEW",
                human_question="Review ordinary implementation?",
            )

    def test_all_five_critical_child_human_gates_are_allowed(self) -> None:
        for index, kind in enumerate(sorted(agent_task.fabric.CRITICAL_HUMAN_GATES)):
            task_id = f"TASK-GATE-{index}"
            value = legacy_task(task_id, state="ACTIVE", path=f"tmp/gate-{index}")
            value["owner_agent"] = "agent-a"
            value["branch"] = f"agent/quality-release/gate-{index}"
            value["lease"] = {
                "claimed_at": "2026-09-30T16:00:00Z",
                "heartbeat_at": "2026-09-30T16:55:00Z",
                "ttl_minutes": 360,
            }
            self.fx.add_task(value)
            result = agent_task.transition_task(
                self.fx.root,
                task_id,
                owner="agent-a",
                target="WAITING_HUMAN",
                human_kind=kind,
                human_question=f"Approve {kind}?",
            )
            self.assertEqual(result["human_gate"]["kind"], kind)

    def test_child_human_decision_atomically_returns_to_active(self) -> None:
        value = legacy_task("TASK-DECISION", state="ACTIVE", path="tmp/decision")
        value["owner_agent"] = "agent-a"
        value["branch"] = "agent/quality-release/decision"
        value["lease"] = {
            "claimed_at": "2026-09-30T16:00:00Z",
            "heartbeat_at": "2026-09-30T16:55:00Z",
            "ttl_minutes": 360,
        }
        self.fx.add_task(value)
        agent_task.transition_task(
            self.fx.root,
            "TASK-DECISION",
            owner="agent-a",
            target="WAITING_HUMAN",
            human_kind="EXTERNAL_COMMITMENT",
            human_question="Approve the external commitment?",
            at="2026-09-30T17:00:00Z",
        )
        result = agent_task.decide_human_gate(
            self.fx.root,
            "TASK-DECISION",
            status="REJECTED",
            decision="Do not send; continue internal work only",
            decided_by="human:owner",
            at="2026-09-30T17:01:00Z",
        )
        self.assertEqual(result["state"], "ACTIVE")
        self.assertEqual(result["human_gate"]["status"], "REJECTED")

    def test_parent_human_gate_rejects_noncritical_and_accepts_critical(self) -> None:
        self._add_parent()
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.request_parent_human_gate(
                self.fx.root, "HUMAN-CS1", kind="ROUTINE_REVIEW", question="Review?"
            )
        pending = agent_task.request_parent_human_gate(
            self.fx.root,
            "HUMAN-CS1",
            kind="PRODUCT_DIRECTION",
            question="Change the agreed core problem?",
            at="2026-09-30T17:00:00Z",
        )
        self.assertEqual(pending["state"], "WAITING_HUMAN")
        resumed = agent_task.decide_parent_human_gate(
            self.fx.root,
            "HUMAN-CS1",
            status="REJECTED",
            decision="Keep current direction",
            decided_by="human:cs1",
            at="2026-09-30T17:01:00Z",
        )
        self.assertEqual(resumed["state"], "ACTIVE")

    def test_child_never_integrates_directly_to_master(self) -> None:
        self._add_parent()
        self._spawn("TASK-CS1-A")
        agent_task.claim_task(
            self.fx.root,
            "TASK-CS1-A",
            owner="agent:a",
            branch="agent/api-product/cs1-a",
        )
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="ACTIVE")
        agent_task.transition_task(self.fx.root, "TASK-CS1-A", owner="agent:a", target="READY_FOR_INTEGRATION")
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.integrate_child(
                self.fx.root,
                "TASK-CS1-A",
                owner="agent:a",
                target_parent_branch="master",
                validated_head_sha="a" * 40,
            )

    def test_fifty_child_fanout_has_no_count_cap(self) -> None:
        self._add_parent()
        specs = [
            {
                "id": f"TASK-CS1-{index:03d}",
                "title": f"Child {index}",
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
        self.assertEqual(status["required_pending_children"], 50)

    def test_declared_artifact_consumer_waits_for_in_fabric_producer(self) -> None:
        self._add_parent()
        self._spawn("TASK-PRODUCER", path="artifacts/producer.json", produces=["ARTIFACT-A"])
        self._spawn("TASK-CONSUMER", path="artifacts/consumer.json", consumes=["ARTIFACT-A"])
        with self.assertRaises(agent_task.TaskOperationError):
            agent_task.claim_task(
                self.fx.root,
                "TASK-CONSUMER",
                owner="agent:consumer",
                branch="agent/api-product/consumer",
            )
        self._verify_child("TASK-PRODUCER", owner="agent:producer")
        result = agent_task.claim_task(
            self.fx.root,
            "TASK-CONSUMER",
            owner="agent:consumer",
            branch="agent/api-product/consumer",
        )
        self.assertEqual(result["state"], "CLAIMED")

    def test_external_consumed_artifact_without_declared_producer_does_not_block(self) -> None:
        self._add_parent()
        self._spawn("TASK-CONSUMER", consumes=["E-INT-012"])
        result = agent_task.claim_task(
            self.fx.root,
            "TASK-CONSUMER",
            owner="agent:consumer",
            branch="agent/api-product/consumer",
        )
        self.assertEqual(result["state"], "CLAIMED")

    def test_parent_batch_returns_active_and_records_history(self) -> None:
        self._add_parent()
        self._spawn("TASK-CS1-FIRST")
        self._verify_child("TASK-CS1-FIRST", owner="agent:first")
        ready = agent_task.mark_parent_ready(self.fx.root, "HUMAN-CS1", at="2026-09-30T17:05:00Z")
        self.assertEqual(ready["state"], "READY_FOR_INTEGRATION")
        acquired = agent_task.acquire_parent_integration(
            self.fx.root,
            "HUMAN-CS1",
            pull_request=77,
            current_master_sha="c" * 40,
            validated_head_sha="d" * 40,
            at="2026-09-30T17:06:00Z",
        )
        self.assertEqual(acquired["state"], "INTEGRATING")
        released = agent_task.release_parent_integration(
            self.fx.root,
            "HUMAN-CS1",
            merge_sha="e" * 40,
            validated_head_sha="d" * 40,
            at="2026-09-30T17:07:00Z",
        )
        self.assertEqual(released["state"], "ACTIVE")
        self.assertEqual(len(released["integration_history"]), 1)
        self.assertEqual(released["integration_history"][0]["child_ids"], ["TASK-CS1-FIRST"])
        self.assertEqual(agent_task.parent_status(self.fx.root, "HUMAN-CS1")["pending_children"], 0)
        self._spawn("TASK-CS1-SECOND", path="artifacts/second.json")
        self.assertEqual(agent_task.parent_status(self.fx.root, "HUMAN-CS1")["pending_children"], 1)

    def test_optional_child_does_not_block_parent_batch(self) -> None:
        self._add_parent("HUMAN-EE", "EE")
        self._spawn("TASK-EE-REQ", parent_id="HUMAN-EE", path="hardware/required.md", lane="hw-measurement")
        self._spawn(
            "TASK-EE-OPT",
            parent_id="HUMAN-EE",
            path="hardware/optional.md",
            lane="hw-measurement",
            required_for_parent=False,
        )
        self._verify_child("TASK-EE-REQ", parent_id="HUMAN-EE", owner="agent:req")
        self.assertTrue(agent_task.parent_status(self.fx.root, "HUMAN-EE")["ready_for_parent_integration"])

    def test_integration_queue_is_priority_then_oldest_then_id_when_unblocking_equal(self) -> None:
        for parent_id, role, priority, ready_at in (
            ("HUMAN-IE", "IE", "P1", "2026-09-30T17:00:00Z"),
            ("HUMAN-CS1", "CS1", "P0", "2026-09-30T17:05:00Z"),
            ("HUMAN-CS2", "CS2", "P0", "2026-09-30T17:01:00Z"),
        ):
            parent = parent_record(parent_id, role, priority=priority)
            parent["state"] = "READY_FOR_INTEGRATION"
            parent["integration"]["pr_state"] = "DRAFT"
            parent["integration"]["ready_for_integration_at"] = ready_at
            self.fx.add_parent(parent)
        queue = agent_task.integration_queue(self.fx.root)
        self.assertEqual([item["parent_id"] for item in queue], ["HUMAN-CS2", "HUMAN-CS1", "HUMAN-IE"])


if __name__ == "__main__":
    unittest.main()
