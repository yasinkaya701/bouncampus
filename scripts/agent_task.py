#!/usr/bin/env python3
"""Operate BOUNCAMPUS agent-fabric task files safely on a coordination checkout.

This CLI intentionally edits only the local task store. Remote atomicity comes from
committing/pushing the resulting single-task change with the current git/GitHub
state; competing remote updates must be resolved by re-reading the task rather than
blindly overwriting it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import agent_fabric_check as fabric

ROOT = Path(__file__).resolve().parents[1]

TRANSITIONS: dict[str, set[str]] = {
    "BACKLOG": {"READY", "CANCELLED"},
    "READY": {"CLAIMED", "CANCELLED"},
    "CLAIMED": {"ACTIVE", "BLOCKED", "WAITING_HUMAN", "CANCELLED"},
    "ACTIVE": {"BLOCKED", "WAITING_HUMAN", "READY_FOR_INTEGRATION", "CANCELLED"},
    "BLOCKED": {"ACTIVE", "WAITING_HUMAN", "CANCELLED"},
    "WAITING_HUMAN": {"ACTIVE", "CANCELLED"},
    "READY_FOR_INTEGRATION": {"INTEGRATING", "BLOCKED", "CANCELLED"},
    "INTEGRATING": {"MERGED_VERIFYING", "BLOCKED"},
    "MERGED_VERIFYING": {"MERGED_VERIFIED", "BLOCKED"},
    "MERGED_VERIFIED": set(),
    "CANCELLED": set(),
}


class TaskOperationError(RuntimeError):
    pass


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config(root: Path) -> dict[str, Any]:
    path = root / fabric.CONFIG_PATH
    if not path.is_file():
        raise TaskOperationError(f"missing fabric config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def task_path(root: Path, task_id: str) -> Path:
    config = load_config(root)
    return root / config["coordination_task_dir"] / f"{task_id}.json"


def load_task(root: Path, task_id: str) -> dict[str, Any]:
    path = task_path(root, task_id)
    if not path.is_file():
        raise TaskOperationError(f"task not found: {task_id}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TaskOperationError(f"invalid task JSON for {task_id}: {exc}") from exc
    if not isinstance(value, dict):
        raise TaskOperationError(f"task {task_id} must be a JSON object")
    return value


def _atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def _validate_repo_or_raise(root: Path) -> dict[str, dict[str, Any]]:
    errors, _, tasks = fabric.validate_repository(root)
    if errors:
        raise TaskOperationError("fabric validation failed:\n- " + "\n- ".join(errors))
    return tasks


def _write_validated(root: Path, task_id: str, previous: dict[str, Any], candidate: dict[str, Any]) -> None:
    path = task_path(root, task_id)
    _atomic_write(path, candidate)
    errors, _, _ = fabric.validate_repository(root)
    if errors:
        _atomic_write(path, previous)
        raise TaskOperationError("operation rejected by fabric invariants:\n- " + "\n- ".join(errors))


def _require_owner(task: dict[str, Any], owner: str) -> None:
    actual = task.get("owner_agent")
    if actual != owner:
        raise TaskOperationError(f"owner mismatch: task owned by {actual!r}, caller is {owner!r}")


def _append_note(task: dict[str, Any], note: str | None) -> None:
    if note:
        task.setdefault("notes", []).append(note)


def list_ready(root: Path) -> list[str]:
    tasks = _validate_repo_or_raise(root)
    return fabric.ready_task_ids(tasks)


def summary(root: Path) -> dict[str, Any]:
    tasks = _validate_repo_or_raise(root)
    states: dict[str, int] = {}
    waiting_human: list[str] = []
    blocked: list[str] = []
    for task_id, task in sorted(tasks.items()):
        state = str(task.get("state"))
        states[state] = states.get(state, 0) + 1
        if state == "WAITING_HUMAN":
            waiting_human.append(task_id)
        if state == "BLOCKED":
            blocked.append(task_id)
    return {
        "states": dict(sorted(states.items())),
        "ready": fabric.ready_task_ids(tasks),
        "waiting_human": waiting_human,
        "blocked": blocked,
    }


def claim_task(root: Path, task_id: str, *, owner: str, branch: str, at: str | None = None) -> dict[str, Any]:
    tasks = _validate_repo_or_raise(root)
    if task_id not in tasks:
        raise TaskOperationError(f"task not found: {task_id}")
    previous = deepcopy(tasks[task_id])
    if previous.get("state") != "READY":
        raise TaskOperationError(f"claim requires READY, found {previous.get('state')}")

    gate = previous.get("human_gate", {})
    if gate.get("status") in {"PENDING", "REJECTED"}:
        raise TaskOperationError(f"task cannot be claimed while human gate is {gate.get('status')}")

    for dep in previous.get("depends_on", []):
        if tasks.get(dep, {}).get("state") != "MERGED_VERIFIED":
            raise TaskOperationError(f"dependency {dep} is not MERGED_VERIFIED")

    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = "CLAIMED"
    candidate["owner_agent"] = owner
    candidate["branch"] = branch
    candidate.setdefault("lease", {})["claimed_at"] = stamp
    candidate["lease"]["heartbeat_at"] = stamp
    if not isinstance(candidate["lease"].get("ttl_minutes"), int):
        candidate["lease"]["ttl_minutes"] = load_config(root)["lease"]["default_ttl_minutes"]
    _append_note(candidate, f"Claimed by {owner} at {stamp}.")
    _write_validated(root, task_id, previous, candidate)
    return candidate


def heartbeat_task(root: Path, task_id: str, *, owner: str, at: str | None = None, note: str | None = None) -> dict[str, Any]:
    previous = load_task(root, task_id)
    if previous.get("state") not in fabric.ACTIVE_OWNERSHIP_STATES:
        raise TaskOperationError(f"heartbeat requires an active-owned state, found {previous.get('state')}")
    _require_owner(previous, owner)
    candidate = deepcopy(previous)
    stamp = at or iso_now()
    candidate.setdefault("lease", {})["heartbeat_at"] = stamp
    _append_note(candidate, note or f"Heartbeat at {stamp}.")
    _write_validated(root, task_id, previous, candidate)
    return candidate


def transition_task(
    root: Path,
    task_id: str,
    *,
    owner: str,
    target: str,
    at: str | None = None,
    note: str | None = None,
    pull_request: int | None = None,
    validated_head_sha: str | None = None,
    merge_sha: str | None = None,
    blocker_reason: str | None = None,
    blocker_evidence: str | None = None,
    blocker_next_action: str | None = None,
    human_kind: str | None = None,
    human_question: str | None = None,
) -> dict[str, Any]:
    previous = load_task(root, task_id)
    current = str(previous.get("state"))
    if target not in TRANSITIONS.get(current, set()):
        raise TaskOperationError(f"invalid transition: {current} -> {target}")

    if current not in {"BACKLOG", "READY"}:
        _require_owner(previous, owner)
    elif current == "READY" and target != "CLAIMED":
        actual = previous.get("owner_agent")
        if actual not in {None, owner}:
            raise TaskOperationError(f"owner mismatch: task owned by {actual!r}")

    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = target

    if target == "CLAIMED":
        raise TaskOperationError("use claim command for READY -> CLAIMED")

    if target in fabric.ACTIVE_OWNERSHIP_STATES:
        candidate.setdefault("lease", {})["heartbeat_at"] = stamp

    if target == "ACTIVE":
        if current == "WAITING_HUMAN" and candidate.get("human_gate", {}).get("status") != "APPROVED":
            raise TaskOperationError("WAITING_HUMAN -> ACTIVE requires an APPROVED human gate")
        candidate["blocker"] = None

    if target == "BLOCKED":
        if not all([blocker_reason, blocker_evidence, blocker_next_action]):
            raise TaskOperationError("BLOCKED requires blocker reason, evidence, and next action")
        candidate["blocker"] = {
            "reason": blocker_reason,
            "evidence": blocker_evidence,
            "next_action": blocker_next_action,
        }

    if target == "WAITING_HUMAN":
        if not human_kind or human_kind == "NONE" or not human_question:
            raise TaskOperationError("WAITING_HUMAN requires non-NONE human kind and one concrete question")
        candidate["human_gate"] = {
            "kind": human_kind,
            "status": "PENDING",
            "question": human_question,
            "decision": None,
            "decided_by": None,
            "decided_at": None,
        }

    integration = candidate.setdefault("integration", {})
    if target == "INTEGRATING":
        if pull_request is None:
            raise TaskOperationError("INTEGRATING requires --pr")
        integration["pull_request"] = pull_request
    if target == "MERGED_VERIFYING":
        if not merge_sha:
            raise TaskOperationError("MERGED_VERIFYING requires --merge-sha")
        if validated_head_sha:
            integration["validated_head_sha"] = validated_head_sha
        integration["merge_sha"] = merge_sha
    if target == "MERGED_VERIFIED":
        if validated_head_sha:
            integration["validated_head_sha"] = validated_head_sha
        if merge_sha:
            integration["merge_sha"] = merge_sha
        integration["post_merge_verified_at"] = stamp

    _append_note(candidate, note or f"Transition {current} -> {target} at {stamp}.")
    _write_validated(root, task_id, previous, candidate)
    return candidate


def decide_human_gate(
    root: Path,
    task_id: str,
    *,
    status: str,
    decision: str,
    decided_by: str,
    at: str | None = None,
) -> dict[str, Any]:
    if status not in {"APPROVED", "REJECTED"}:
        raise TaskOperationError("human decision status must be APPROVED or REJECTED")
    previous = load_task(root, task_id)
    gate = previous.get("human_gate", {})
    if gate.get("kind") in {None, "NONE"} or gate.get("status") != "PENDING":
        raise TaskOperationError("task does not have a pending critical human gate")
    candidate = deepcopy(previous)
    stamp = at or iso_now()
    candidate["human_gate"].update(
        {
            "status": status,
            "decision": decision,
            "decided_by": decided_by,
            "decided_at": stamp,
        }
    )
    _append_note(candidate, f"Human gate {status.lower()} by {decided_by} at {stamp}: {decision}")
    _write_validated(root, task_id, previous, candidate)
    return candidate


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="checkout containing the coordination task store")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("summary")
    sub.add_parser("ready")

    show = sub.add_parser("show")
    show.add_argument("task_id")

    claim = sub.add_parser("claim")
    claim.add_argument("task_id")
    claim.add_argument("--owner", required=True)
    claim.add_argument("--branch", required=True)
    claim.add_argument("--at")

    heartbeat = sub.add_parser("heartbeat")
    heartbeat.add_argument("task_id")
    heartbeat.add_argument("--owner", required=True)
    heartbeat.add_argument("--at")
    heartbeat.add_argument("--note")

    transition = sub.add_parser("transition")
    transition.add_argument("task_id")
    transition.add_argument("--owner", required=True)
    transition.add_argument("--to", required=True, dest="target")
    transition.add_argument("--at")
    transition.add_argument("--note")
    transition.add_argument("--pr", type=int, dest="pull_request")
    transition.add_argument("--validated-head-sha")
    transition.add_argument("--merge-sha")
    transition.add_argument("--blocker-reason")
    transition.add_argument("--blocker-evidence")
    transition.add_argument("--blocker-next-action")
    transition.add_argument("--human-kind")
    transition.add_argument("--human-question")

    decision = sub.add_parser("human-decision")
    decision.add_argument("task_id")
    decision.add_argument("--status", choices=["APPROVED", "REJECTED"], required=True)
    decision.add_argument("--decision", required=True)
    decision.add_argument("--by", required=True, dest="decided_by")
    decision.add_argument("--at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "summary":
            _print(summary(args.root))
        elif args.command == "ready":
            _print(list_ready(args.root))
        elif args.command == "show":
            _print(load_task(args.root, args.task_id))
        elif args.command == "claim":
            _print(claim_task(args.root, args.task_id, owner=args.owner, branch=args.branch, at=args.at))
        elif args.command == "heartbeat":
            _print(heartbeat_task(args.root, args.task_id, owner=args.owner, at=args.at, note=args.note))
        elif args.command == "transition":
            _print(
                transition_task(
                    args.root,
                    args.task_id,
                    owner=args.owner,
                    target=args.target,
                    at=args.at,
                    note=args.note,
                    pull_request=args.pull_request,
                    validated_head_sha=args.validated_head_sha,
                    merge_sha=args.merge_sha,
                    blocker_reason=args.blocker_reason,
                    blocker_evidence=args.blocker_evidence,
                    blocker_next_action=args.blocker_next_action,
                    human_kind=args.human_kind,
                    human_question=args.human_question,
                )
            )
        elif args.command == "human-decision":
            _print(
                decide_human_gate(
                    args.root,
                    args.task_id,
                    status=args.status,
                    decision=args.decision,
                    decided_by=args.decided_by,
                    at=args.at,
                )
            )
        else:
            raise TaskOperationError(f"unknown command: {args.command}")
    except TaskOperationError as exc:
        print(f"AGENT TASK ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
