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


def parent_path(root: Path, parent_id: str) -> Path:
    config = load_config(root)
    parent_dir = config.get("coordination_parent_dir")
    if not isinstance(parent_dir, str) or not parent_dir:
        raise TaskOperationError("fabric schema does not configure parent workstreams")
    return root / parent_dir / f"{parent_id}.json"


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


def load_parent(root: Path, parent_id: str) -> dict[str, Any]:
    path = parent_path(root, parent_id)
    if not path.is_file():
        raise TaskOperationError(f"parent workstream not found: {parent_id}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TaskOperationError(f"invalid parent JSON for {parent_id}: {exc}") from exc
    if not isinstance(value, dict):
        raise TaskOperationError(f"parent {parent_id} must be a JSON object")
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


def _load_task_template(root: Path) -> dict[str, Any]:
    path = root / fabric.TEMPLATE_PATH
    if not path.is_file():
        raise TaskOperationError(f"missing task template: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TaskOperationError("task template must be a JSON object")
    return value


def _assert_spawn_paths_available(
    tasks: dict[str, dict[str, Any]],
    *,
    task_id: str,
    touched_paths: list[str],
) -> None:
    for existing_id, existing in tasks.items():
        if existing.get("state") not in fabric.ACTIVE_OWNERSHIP_STATES:
            continue
        for requested in touched_paths:
            for owned in existing.get("touched_paths", []):
                if not isinstance(requested, str) or not isinstance(owned, str):
                    continue
                try:
                    overlaps = fabric.paths_overlap(requested, owned)
                except ValueError as exc:
                    raise TaskOperationError(f"invalid touched path for {task_id}: {exc}") from exc
                if overlaps:
                    raise TaskOperationError(
                        f"path ownership conflict: {task_id} requests {requested!r} while "
                        f"{existing_id} owns {owned!r}"
                    )


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


def spawn_child_task(
    root: Path,
    *,
    parent_id: str,
    task_id: str,
    title: str,
    execution_role: str,
    lane: str,
    touched_paths: list[str],
    priority: str = "P1",
    depends_on: list[str] | None = None,
    required_for_parent: bool = True,
) -> dict[str, Any]:
    config = load_config(root)
    if config.get("schema_version") != 2:
        raise TaskOperationError("child spawning requires fabric schema v2")
    parent = load_parent(root, parent_id)
    parent_workstream = parent.get("workstream")
    if parent_workstream not in config.get("parent_workstreams", []):
        raise TaskOperationError(f"invalid parent workstream: {parent_workstream!r}")
    role_branches = config.get("role_branches", {})
    if execution_role not in role_branches:
        raise TaskOperationError(f"unknown execution role: {execution_role!r}")
    if not touched_paths:
        raise TaskOperationError("child task requires at least one touched path")
    destination = task_path(root, task_id)
    if destination.exists():
        raise TaskOperationError(f"task already exists: {task_id}")

    tasks = _validate_repo_or_raise(root)
    _assert_spawn_paths_available(tasks, task_id=task_id, touched_paths=touched_paths)

    candidate = deepcopy(_load_task_template(root))
    candidate.update(
        {
            "schema_version": 2,
            "id": task_id,
            "title": title,
            "priority": priority,
            "lane": lane,
            "state": "READY",
            "owner_agent": None,
            "branch": None,
            "depends_on": list(depends_on or []),
            "touched_paths": list(touched_paths),
            "acceptance_criteria": [],
            "validation_commands": [],
            "agent_kind": "CHILD",
            "parent_id": parent_id,
            "parent_workstream": parent_workstream,
            "execution_role": execution_role,
            "required_for_parent": bool(required_for_parent),
            "child_integration": {
                "target_role_branch": role_branches[execution_role],
                "pull_request": None,
                "validated_head_sha": None,
                "integrated_commit_sha": None,
                "verified_at": None,
            },
            "notes": [
                f"Spawned under {parent_id}; durable execution role is {execution_role}."
            ],
        }
    )

    parent_previous = deepcopy(parent)
    parent_candidate = deepcopy(parent)
    children = parent_candidate.setdefault("child_ids", [])
    if task_id in children:
        raise TaskOperationError(f"parent already references child task: {task_id}")
    children.append(task_id)

    _atomic_write(destination, candidate)
    try:
        errors, _, _ = fabric.validate_repository(root)
        if errors:
            raise TaskOperationError("spawn rejected by fabric invariants:\n- " + "\n- ".join(errors))
        _atomic_write(parent_path(root, parent_id), parent_candidate)
    except Exception:
        try:
            destination.unlink()
        except FileNotFoundError:
            pass
        _atomic_write(parent_path(root, parent_id), parent_previous)
        raise
    return candidate


def parent_status(root: Path, parent_id: str) -> dict[str, Any]:
    parent = load_parent(root, parent_id)
    tasks = _validate_repo_or_raise(root)
    child_ids = parent.get("child_ids", [])
    if not isinstance(child_ids, list):
        raise TaskOperationError(f"parent {parent_id} child_ids must be a list")

    states: dict[str, int] = {}
    required_remaining: list[str] = []
    missing: list[str] = []
    for child_id in child_ids:
        child = tasks.get(child_id)
        if child is None:
            missing.append(str(child_id))
            required_remaining.append(str(child_id))
            continue
        state = str(child.get("state"))
        states[state] = states.get(state, 0) + 1
        if child.get("required_for_parent", True) and state != "MERGED_VERIFIED":
            required_remaining.append(str(child_id))

    return {
        "parent_id": parent_id,
        "workstream": parent.get("workstream"),
        "child_count": len(child_ids),
        "states": dict(sorted(states.items())),
        "missing_children": sorted(missing),
        "required_remaining": sorted(required_remaining),
        "ready_for_integration": bool(child_ids) and not required_remaining,
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


def integrate_child_task(
    root: Path,
    task_id: str,
    *,
    owner: str,
    pull_request: int,
    validated_head_sha: str,
    target_role_branch: str,
    at: str | None = None,
) -> dict[str, Any]:
    previous = load_task(root, task_id)
    if previous.get("agent_kind") != "CHILD":
        raise TaskOperationError("integrate-child requires a CHILD task")
    execution_role = previous.get("execution_role")
    configured_target = load_config(root).get("role_branches", {}).get(execution_role)
    if not configured_target:
        raise TaskOperationError(f"child has unknown execution role: {execution_role!r}")
    if target_role_branch != configured_target:
        raise TaskOperationError(
            f"child target mismatch: execution role {execution_role!r} must target {configured_target!r}"
        )
    _require_owner(previous, owner)
    if previous.get("state") != "READY_FOR_INTEGRATION":
        raise TaskOperationError(
            f"integrate-child requires READY_FOR_INTEGRATION, found {previous.get('state')}"
        )
    if not isinstance(validated_head_sha, str) or not validated_head_sha.strip():
        raise TaskOperationError("integrate-child requires validated head SHA")

    integrated = transition_task(
        root,
        task_id,
        owner=owner,
        target="INTEGRATING",
        pull_request=pull_request,
        at=at,
        note=f"Child fan-in to {target_role_branch} via PR #{pull_request}.",
    )
    candidate = deepcopy(integrated)
    candidate["child_integration"] = {
        **candidate.get("child_integration", {}),
        "target_role_branch": target_role_branch,
        "pull_request": pull_request,
        "validated_head_sha": validated_head_sha,
    }
    _write_validated(root, task_id, integrated, candidate)
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

    parent = sub.add_parser("parent-status")
    parent.add_argument("parent_id")

    spawn = sub.add_parser("spawn-child")
    spawn.add_argument("parent_id")
    spawn.add_argument("task_id")
    spawn.add_argument("--title", required=True)
    spawn.add_argument("--execution-role", required=True)
    spawn.add_argument("--lane", required=True)
    spawn.add_argument("--path", action="append", dest="touched_paths", required=True)
    spawn.add_argument("--priority", default="P1")
    spawn.add_argument("--depends-on", action="append", default=[])
    spawn.add_argument("--optional", action="store_true")

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

    integrate = sub.add_parser("integrate-child")
    integrate.add_argument("task_id")
    integrate.add_argument("--owner", required=True)
    integrate.add_argument("--pr", type=int, required=True, dest="pull_request")
    integrate.add_argument("--validated-head-sha", required=True)
    integrate.add_argument("--target-role-branch", required=True)
    integrate.add_argument("--at")

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
        elif args.command == "parent-status":
            _print(parent_status(args.root, args.parent_id))
        elif args.command == "spawn-child":
            _print(
                spawn_child_task(
                    args.root,
                    parent_id=args.parent_id,
                    task_id=args.task_id,
                    title=args.title,
                    execution_role=args.execution_role,
                    lane=args.lane,
                    touched_paths=args.touched_paths,
                    priority=args.priority,
                    depends_on=args.depends_on,
                    required_for_parent=not args.optional,
                )
            )
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
        elif args.command == "integrate-child":
            _print(
                integrate_child_task(
                    args.root,
                    args.task_id,
                    owner=args.owner,
                    pull_request=args.pull_request,
                    validated_head_sha=args.validated_head_sha,
                    target_role_branch=args.target_role_branch,
                    at=args.at,
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
