#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import agent_bus


class AgentBusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        agents = self.root / ".agents"
        agents.mkdir(parents=True)
        (agents / "config.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "repository": "yasinkaya701/bouncampus",
                    "lease_ttl_minutes": 45,
                    "merge_lock_ttl_minutes": 30,
                    "lanes": [
                        "frontend-ux",
                        "campus-geo",
                        "api-product",
                        "quality-release",
                        "integration",
                    ],
                    "message_types": [
                        "INFO",
                        "REQUEST",
                        "DECISION",
                        "BLOCKER",
                        "HANDOFF",
                        "REVIEW",
                        "ACK",
                    ],
                    "remote_bus": {
                        "enabled": True,
                        "transport": "github_issue",
                        "issue_number": 8,
                        "marker": "BOUNCAMPUS_AGENT_BUS_V1",
                        "token_env": ["BOUNCAMPUS_TEST_TOKEN_THAT_DOES_NOT_EXIST"],
                    },
                }
            ),
            encoding="utf-8",
        )
        agent_bus.ensure_runtime_dirs(self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def args(self, **kwargs: object) -> Namespace:
        return Namespace(root=str(self.root), **kwargs)

    def claim(self, task: str, agent: str, path: str) -> None:
        agent_bus.cmd_claim(
            self.args(
                task_id=task,
                agent=agent,
                lane="quality-release",
                branch=f"agent/quality-release/{task}",
                scope=f"scope for {task}",
                paths=[path],
            )
        )

    def test_claim_rejects_path_overlap(self) -> None:
        self.claim("one", "agent-one", "scripts")
        with self.assertRaises(agent_bus.AgentBusError):
            self.claim("two", "agent-two", "scripts/other.py")

    def test_message_ack_and_retry_guard(self) -> None:
        message = agent_bus.create_message(
            self.root,
            "agent-one",
            "agent-two",
            "REQUEST",
            "Need interface",
            "Return the canonical contract.",
            "task-one",
            True,
        )
        self.assertFalse(agent_bus.message_acknowledged(self.root, message))

        agent_bus.cmd_ack(
            self.args(
                message_id=message["message_id"],
                agent="agent-two",
                offline=True,
            )
        )
        self.assertTrue(agent_bus.message_acknowledged(self.root, message))

        with self.assertRaises(agent_bus.AgentBusError):
            agent_bus.cmd_retry(
                self.args(
                    message_id=message["message_id"],
                    force=False,
                    offline=True,
                )
            )

    def test_handoff_requires_preintegration_state(self) -> None:
        self.claim("handoff-task", "agent-one", "frontend/src")
        agent_bus.cmd_handoff(
            self.args(
                task_id="handoff-task",
                from_agent="agent-one",
                to_agent="agent-two",
                reason="lane owner changed",
                next_action="continue implementation",
                offline=True,
            )
        )
        task = agent_bus.load_task(self.root, "handoff-task")
        self.assertEqual(task["owner_agent"], "agent-two")
        self.assertEqual(task["state"], "ACTIVE")

        agent_bus.cmd_ready(
            self.args(task_id="handoff-task", agent="agent-two", evidence=["tests green"])
        )
        with self.assertRaises(agent_bus.AgentBusError):
            agent_bus.cmd_handoff(
                self.args(
                    task_id="handoff-task",
                    from_agent="agent-two",
                    to_agent="agent-three",
                    reason="should fail",
                    next_action="none",
                    offline=True,
                )
            )

    def test_full_merge_lifecycle_releases_lock_and_lease(self) -> None:
        self.claim("merge-task", "agent-one", "docs")
        agent_bus.cmd_ready(
            self.args(task_id="merge-task", agent="agent-one", evidence=["compile"])
        )
        agent_bus.cmd_lock_acquire(
            self.args(task_id="merge-task", agent="agent-one", force_stale=False)
        )
        self.assertTrue(agent_bus.merge_lock_path(self.root).exists())

        agent_bus.cmd_merged(
            self.args(task_id="merge-task", agent="agent-one", merge_sha="abc123")
        )
        agent_bus.cmd_verify(
            self.args(task_id="merge-task", agent="agent-one", evidence=["master green"])
        )
        task = agent_bus.load_task(self.root, "merge-task")
        self.assertEqual(task["state"], "MERGED_VERIFIED")
        self.assertFalse(agent_bus.merge_lock_path(self.root).exists())
        self.assertFalse(agent_bus.lease_path(self.root, "merge-task").exists())

    def test_remote_envelope_round_trip(self) -> None:
        message = agent_bus.create_message(
            self.root,
            "agent-one",
            "agent-two",
            "DECISION",
            "Contract frozen",
            "Use schema v1.",
        )
        rendered = agent_bus.render_remote_envelope(self.root, message)
        parsed = agent_bus.parse_remote_envelope(self.root, rendered)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["message_id"], message["message_id"])
        self.assertEqual(parsed["type"], "DECISION")

    def test_validate_accepts_consistent_state(self) -> None:
        self.claim("valid-task", "agent-one", "backend/app")
        agent_bus.cmd_validate(self.args(offline=True))


if __name__ == "__main__":
    unittest.main()
