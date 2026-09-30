#!/usr/bin/env python3
"""Operate the BOUNCAMPUS human-parent / child-agent coordination fabric.

Fabric v2 keeps four persistent human-owned parent workstreams and allows an
unbounded-by-policy number of independently leased child agents beneath them.
Every mutation is written atomically and rolled back when fabric invariants fail.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

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
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TaskOperationError("fabric config must be a JSON object")
    return value


def task_path(root: Path, task_id: str) -> Path:
    return root / load_config(root)["coordination_task_dir"] / f"{task_id}.json"


def parent_path(root: Path, parent_id: str) -> Path:
    directory = load_config(root).get("coordination_parent_dir")
    if not directory:
        raise TaskOperationError("fabric schema does not define parent workstreams")
    return root / directory / f"{parent_id}.json"


def _load_object(path: Path, kind: str) -> dict[str, Any]:
    if not path.is_file():
        raise TaskOperationError(f"{kind} not found: {path.stem}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TaskOperationError(f"invalid {kind} JSON for {path.stem}: {exc}") from exc
    if not isinstance(value, dict):
        raise TaskOperationError(f"{kind} {path.stem} must be a JSON object")
    return value


def load_task(root: Path, task_id: str) -> dict[str, Any]:
    return _load_object(task_path(root, task_id), "task")


def load_parent(root: Path, parent_id: str) -> dict[str, Any]:
    return _load_object(parent_path(root, parent_id), "parent")


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


def _parents_or_raise(root: Path) -> dict[str, dict[str, Any]]:
    config = load_config(root)
    errors: list[str] = []
    parents = fabric.load_parents(root, config, errors)
    if errors:
        raise TaskOperationError("parent store invalid:\n- " + "\n- ".join(errors))
    return parents


def _write_validated(
    path: Path,
    previous: dict[str, Any] | None,
    candidate: dict[str, Any],
    root: Path,
) -> None:
    existed = path.exists()
    _atomic_write(path, candidate)
    errors, _, _ = fabric.validate_repository(root)
    if not errors:
        return
    if existed and previous is not None:
        _atomic_write(path, previous)
    else:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    raise TaskOperationError("operation rejected by fabric invariants:\n- " + "\n- ".join(errors))


def _write_task_validated(
    root: Path,
    task_id: str,
    previous: dict[str, Any] | None,
    candidate: dict[str, Any],
) -> None:
    _write_validated(task_path(root, task_id), previous, candidate, root)


def _write_parent_validated(
    root: Path,
    parent_id: str,
    previous: dict[str, Any],
    candidate: dict[str, Any],
) -> None:
    _write_validated(parent_path(root, parent_id), previous, candidate, root)


def _require_owner(task: dict[str, Any], owner: str) -> None:
    actual = task.get("owner_agent")
    if actual != owner:
        raise TaskOperationError(f"owner mismatch: task owned by {actual!r}, caller is {owner!r}")


def _append_note(record: dict[str, Any], note: str | None) -> None:
    if note:
        record.setdefault("notes", []).append(note)


def _priority_rank(priority: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2}.get(priority, 99)


def _declared_producers(tasks: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for task in tasks.values():
        for artifact in task.get("produces", []):
            if isinstance(artifact, str) and artifact:
                result.setdefault(artifact, []).append(task)
    return result


def unresolved_declared_consumes(
    task: dict[str, Any],
    tasks: dict[str, dict[str, Any]],
) -> list[str]:
    """Return in-fabric produced artifacts not yet available.

    Identifiers with no in-fabric producer are external evidence/artifacts and
    remain governed by KREATE evidence policy rather than being blocked here.
    """
    producers = _declared_producers(tasks)
    unresolved: list[str] = []
    for artifact in task.get("consumes", []):
        if not isinstance(artifact, str) or artifact not in producers:
            continue
        if not any(item.get("state") == "MERGED_VERIFIED" for item in producers[artifact]):
            unresolved.append(artifact)
    return sorted(set(unresolved))


def _conflicts_with_active(tasks: dict[str, dict[str, Any]], candidate: dict[str, Any]) -> bool:
    for other_id, other in tasks.items():
        if other_id == candidate.get("id") or other.get("state") not in fabric.ACTIVE_OWNERSHIP_STATES:
            continue
        for left in candidate.get("touched_paths", []):
            for right in other.get("touched_paths", []):
                if isinstance(left, str) and isinstance(right, str) and fabric.paths_overlap(left, right):
                    return True
    return False


def list_ready(root: Path, parent_id: str | None = None) -> list[str]:
    tasks = _validate_repo_or_raise(root)
    result: list[str] = []
    for task_id in fabric.ready_task_ids(tasks):
        task = tasks[task_id]
        if parent_id is not None and task.get("parent_id") != parent_id:
            continue
        if unresolved_declared_consumes(task, tasks):
            continue
        result.append(task_id)
    return result


def next_ready(root: Path, *, parent_id: str) -> list[str]:
    tasks = _validate_repo_or_raise(root)
    candidates: list[dict[str, Any]] = []
    for task_id in fabric.ready_task_ids(tasks):
        task = tasks[task_id]
        if task.get("schema_version") != 2 or task.get("parent_id") != parent_id:
            continue
        if unresolved_declared_consumes(task, tasks) or _conflicts_with_active(tasks, task):
            continue
        candidates.append(task)
    candidates.sort(key=lambda item: (_priority_rank(str(item.get("priority"))), str(item.get("id"))))
    return [str(item["id"]) for item in candidates]


def summary(root: Path) -> dict[str, Any]:
    tasks = _validate_repo_or_raise(root)
    states: dict[str, int] = {}
    waiting_human: list[str] = []
    blocked: list[str] = []
    by_parent: dict[str, int] = {}
    for task_id, task in sorted(tasks.items()):
        state = str(task.get("state"))
        states[state] = states.get(state, 0) + 1
        if state == "WAITING_HUMAN":
            waiting_human.append(task_id)
        if state == "BLOCKED":
            blocked.append(task_id)
        parent_id = task.get("parent_id")
        if isinstance(parent_id, str):
            by_parent[parent_id] = by_parent.get(parent_id, 0) + 1
    return {
        "states": dict(sorted(states.items())),
        "ready": list_ready(root),
        "waiting_human": waiting_human,
        "blocked": blocked,
        "children_by_parent": dict(sorted(by_parent.items())),
    }


def claim_task(
    root: Path,
    task_id: str,
    *,
    owner: str,
    branch: str,
    at: str | None = None,
) -> dict[str, Any]:
    tasks = _validate_repo_or_raise(root)
    if task_id not in tasks:
        raise TaskOperationError(f"task not found: {task_id}")
    previous = deepcopy(tasks[task_id])
    if previous.get("state") != "READY":
        raise TaskOperationError(f"claim requires READY, found {previous.get('state')}")
    if previous.get("schema_version") == 2 and not owner.startswith("agent:"):
        raise TaskOperationError("v2 child owner must use agent:<identity>")
    gate = previous.get("human_gate", {})
    if gate.get("status") in {"PENDING", "REJECTED"}:
        raise TaskOperationError(f"task cannot be claimed while human gate is {gate.get('status')}")
    for dep in previous.get("depends_on", []):
        if tasks.get(dep, {}).get("state") != "MERGED_VERIFIED":
            raise TaskOperationError(f"dependency {dep} is not MERGED_VERIFIED")
    unresolved = unresolved_declared_consumes(previous, tasks)
    if unresolved:
        raise TaskOperationError(f"declared consumed artifacts are not yet produced: {unresolved}")

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
    _write_task_validated(root, task_id, previous, candidate)
    return candidate


def heartbeat_task(
    root: Path,
    task_id: str,
    *,
    owner: str,
    at: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    previous = load_task(root, task_id)
    if previous.get("state") not in fabric.ACTIVE_OWNERSHIP_STATES:
        raise TaskOperationError(f"heartbeat requires an active-owned state, found {previous.get('state')}")
    _require_owner(previous, owner)
    candidate = deepcopy(previous)
    stamp = at or iso_now()
    candidate.setdefault("lease", {})["heartbeat_at"] = stamp
    _append_note(candidate, note or f"Heartbeat at {stamp}.")
    _write_task_validated(root, task_id, previous, candidate)
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
    if previous.get("schema_version") == 2 and target in {"INTEGRATING", "MERGED_VERIFYING", "MERGED_VERIFIED"}:
        raise TaskOperationError("v2 child integration must use integrate-child / verify-child")
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
        if human_kind not in fabric.CRITICAL_HUMAN_GATES or not human_question:
            raise TaskOperationError("WAITING_HUMAN requires a critical human gate and one concrete question")
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
    _write_task_validated(root, task_id, previous, candidate)
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
    """Record a critical human decision and immediately release the child.

    WAITING_HUMAN represents a *pending* gate only. Once the human has decided,
    the child returns to ACTIVE. A rejected decision means the agent must adapt
    its execution path without performing the rejected action; it does not need
    another permission round just to resume safe work.
    """
    if status not in {"APPROVED", "REJECTED"}:
        raise TaskOperationError("human decision status must be APPROVED or REJECTED")
    previous = load_task(root, task_id)
    gate = previous.get("human_gate", {})
    if previous.get("state") != "WAITING_HUMAN":
        raise TaskOperationError("human decision requires WAITING_HUMAN state")
    if gate.get("kind") not in fabric.CRITICAL_HUMAN_GATES or gate.get("status") != "PENDING":
        raise TaskOperationError("task does not have a pending critical human gate")
    candidate = deepcopy(previous)
    stamp = at or iso_now()
    candidate["human_gate"].update(
        {"status": status, "decision": decision, "decided_by": decided_by, "decided_at": stamp}
    )
    candidate["state"] = "ACTIVE"
    candidate.setdefault("lease", {})["heartbeat_at"] = stamp
    candidate["blocker"] = None
    _append_note(candidate, f"Human gate {status.lower()} by {decided_by} at {stamp}: {decision}")
    _write_task_validated(root, task_id, previous, candidate)
    return candidate


def _new_child_candidate(
    root: Path,
    *,
    parent_id: str,
    task_id: str,
    title: str,
    lane: str,
    priority: str,
    touched_paths: list[str],
    depends_on: list[str] | None = None,
    acceptance_criteria: list[str] | None = None,
    validation_commands: list[str] | None = None,
    produces: list[str] | None = None,
    consumes: list[str] | None = None,
    required_for_parent: bool = True,
) -> dict[str, Any]:
    template = json.loads((root / fabric.TEMPLATE_PATH).read_text(encoding="utf-8"))
    if template.get("schema_version") != 2:
        raise TaskOperationError("child creation requires schema-v2 task template")
    candidate = deepcopy(template)
    candidate.update(
        {
            "id": task_id,
            "title": title,
            "lane": lane,
            "priority": priority,
            "state": "READY",
            "parent_id": parent_id,
            "required_for_parent": bool(required_for_parent),
            "owner_agent": None,
            "branch": None,
            "depends_on": list(depends_on or []),
            "touched_paths": list(touched_paths),
            "acceptance_criteria": list(acceptance_criteria or []),
            "validation_commands": list(validation_commands or []),
            "produces": list(produces or []),
            "consumes": list(consumes or []),
            "notes": [f"Spawned under {parent_id} at {iso_now()}."],
        }
    )
    return candidate


def spawn_child(
    root: Path,
    *,
    parent_id: str,
    task_id: str,
    title: str,
    lane: str,
    priority: str,
    touched_paths: list[str],
    depends_on: list[str] | None = None,
    acceptance_criteria: list[str] | None = None,
    validation_commands: list[str] | None = None,
    produces: list[str] | None = None,
    consumes: list[str] | None = None,
    required_for_parent: bool = True,
) -> dict[str, Any]:
    _validate_repo_or_raise(root)
    parent = _parents_or_raise(root).get(parent_id)
    if parent is None:
        raise TaskOperationError(f"parent not found: {parent_id}")
    if parent.get("state") == "COMPLETE":
        raise TaskOperationError(f"cannot spawn child under COMPLETE parent {parent_id}")
    if task_path(root, task_id).exists():
        raise TaskOperationError(f"task already exists: {task_id}")
    candidate = _new_child_candidate(
        root,
        parent_id=parent_id,
        task_id=task_id,
        title=title,
        lane=lane,
        priority=priority,
        touched_paths=touched_paths,
        depends_on=depends_on,
        acceptance_criteria=acceptance_criteria,
        validation_commands=validation_commands,
        produces=produces,
        consumes=consumes,
        required_for_parent=required_for_parent,
    )
    _write_task_validated(root, task_id, None, candidate)
    return candidate


def integrate_child(
    root: Path,
    task_id: str,
    *,
    owner: str,
    target_parent_branch: str,
    validated_head_sha: str,
    at: str | None = None,
) -> dict[str, Any]:
    previous = load_task(root, task_id)
    if previous.get("schema_version") != 2 or previous.get("state") != "READY_FOR_INTEGRATION":
        raise TaskOperationError("integrate-child requires a READY_FOR_INTEGRATION schema-v2 child")
    _require_owner(previous, owner)
    parent = load_parent(root, str(previous.get("parent_id")))
    expected = parent.get("parent_branch")
    if target_parent_branch == "master" or target_parent_branch != expected:
        raise TaskOperationError(f"child must integrate into parent branch {expected!r}, not {target_parent_branch!r}")
    candidate = deepcopy(previous)
    stamp = at or iso_now()
    candidate["state"] = "INTEGRATING"
    candidate.setdefault("lease", {})["heartbeat_at"] = stamp
    candidate["child_integration"] = {
        "target_parent_branch": target_parent_branch,
        "validated_head_sha": validated_head_sha,
        "integrated_commit_sha": None,
        "verified_at": None,
    }
    _append_note(candidate, f"Child integration started into {target_parent_branch} at {stamp}.")
    _write_task_validated(root, task_id, previous, candidate)
    return candidate


def verify_child(
    root: Path,
    task_id: str,
    *,
    owner: str,
    integrated_commit_sha: str,
    at: str | None = None,
) -> dict[str, Any]:
    previous = load_task(root, task_id)
    if previous.get("schema_version") != 2 or previous.get("state") != "INTEGRATING":
        raise TaskOperationError("verify-child requires an INTEGRATING schema-v2 child")
    _require_owner(previous, owner)
    integration = previous.get("child_integration", {})
    if not integration.get("validated_head_sha") or not integration.get("target_parent_branch"):
        raise TaskOperationError("child integration is missing validated head or parent target")
    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = "MERGED_VERIFIED"
    candidate.setdefault("lease", {})["heartbeat_at"] = stamp
    candidate["child_integration"]["integrated_commit_sha"] = integrated_commit_sha
    candidate["child_integration"]["verified_at"] = stamp
    _append_note(candidate, f"Child integration verified at {stamp} ({integrated_commit_sha}).")
    _write_task_validated(root, task_id, previous, candidate)
    return candidate


def children_for_parent(tasks: dict[str, dict[str, Any]], parent_id: str) -> list[dict[str, Any]]:
    return [
        task for task in tasks.values()
        if task.get("schema_version") == 2 and task.get("parent_id") == parent_id
    ]


def _historically_integrated_child_ids(parent: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for entry in parent.get("integration_history", []):
        if isinstance(entry, dict):
            result.update(item for item in entry.get("child_ids", []) if isinstance(item, str))
    return result


def pending_children_for_parent(
    tasks: dict[str, dict[str, Any]],
    parent: dict[str, Any],
) -> list[dict[str, Any]]:
    historical = _historically_integrated_child_ids(parent)
    return [
        task for task in children_for_parent(tasks, str(parent["id"]))
        if task.get("id") not in historical
    ]


def parent_status(root: Path, parent_id: str) -> dict[str, Any]:
    tasks = _validate_repo_or_raise(root)
    parent = load_parent(root, parent_id)
    children = children_for_parent(tasks, parent_id)
    pending = pending_children_for_parent(tasks, parent)
    required_pending = [task for task in pending if task.get("required_for_parent", True)]
    incomplete = sorted(
        str(task["id"]) for task in required_pending if task.get("state") != "MERGED_VERIFIED"
    )
    verified = sorted(
        str(task["id"]) for task in pending if task.get("state") == "MERGED_VERIFIED"
    )
    states: dict[str, int] = {}
    for task in pending:
        state = str(task.get("state"))
        states[state] = states.get(state, 0) + 1
    return {
        "parent_id": parent_id,
        "role": parent.get("role"),
        "human_owner": parent.get("human_owner"),
        "children": len(children),
        "pending_children": len(pending),
        "required_pending_children": len(required_pending),
        "states": dict(sorted(states.items())),
        "blocked": sorted(str(task["id"]) for task in pending if task.get("state") == "BLOCKED"),
        "waiting_human": sorted(str(task["id"]) for task in pending if task.get("state") == "WAITING_HUMAN"),
        "incomplete_required": incomplete,
        "verified_pending": verified,
        "integration_batches": len(parent.get("integration_history", [])),
        "ready_for_parent_integration": bool(verified) and not incomplete,
    }


def fanout_children(
    root: Path,
    *,
    parent_id: str,
    specs: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Atomically add an arbitrary number of READY child tasks.

    All candidate files are written, the entire fabric is validated once, and
    every new file is removed if the batch violates an invariant. This permits
    sibling dependencies within one fan-out without leaving partial state.
    """
    _validate_repo_or_raise(root)
    parent = _parents_or_raise(root).get(parent_id)
    if parent is None:
        raise TaskOperationError(f"parent not found: {parent_id}")
    if parent.get("state") == "COMPLETE":
        raise TaskOperationError(f"cannot fan out under COMPLETE parent {parent_id}")

    specs_list = list(specs)
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    config = load_config(root)
    priorities = set(config.get("priorities", []))
    for spec in specs_list:
        task_id = spec.get("id")
        if not isinstance(task_id, str) or not fabric.TASK_ID_RE.fullmatch(task_id):
            raise TaskOperationError(f"invalid fanout child id: {task_id!r}")
        if task_id in seen or task_path(root, task_id).exists():
            raise TaskOperationError(f"duplicate/existing fanout child id: {task_id}")
        seen.add(task_id)
        lane = spec.get("lane", "quality-release")
        if not isinstance(lane, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", lane):
            raise TaskOperationError(f"fanout child {task_id} has invalid lane")
        priority = spec.get("priority", "P1")
        if priority not in priorities:
            raise TaskOperationError(f"fanout child {task_id} has invalid priority {priority!r}")
        paths = spec.get("touched_paths")
        if not isinstance(paths, list) or not paths:
            raise TaskOperationError(f"fanout child {task_id} requires touched_paths")
        for path in paths:
            if not isinstance(path, str):
                raise TaskOperationError(f"fanout child {task_id} touched_paths must be strings")
            fabric.normalize_owned_path(path)
        candidates.append(
            _new_child_candidate(
                root,
                parent_id=parent_id,
                task_id=task_id,
                title=str(spec.get("title") or task_id),
                lane=lane,
                priority=priority,
                touched_paths=list(paths),
                depends_on=list(spec.get("depends_on", [])),
                acceptance_criteria=list(spec.get("acceptance_criteria", [])),
                validation_commands=list(spec.get("validation_commands", [])),
                produces=list(spec.get("produces", [])),
                consumes=list(spec.get("consumes", [])),
                required_for_parent=bool(spec.get("required_for_parent", True)),
            )
        )

    written: list[Path] = []
    try:
        for candidate in candidates:
            path = task_path(root, str(candidate["id"]))
            _atomic_write(path, candidate)
            written.append(path)
        errors, _, _ = fabric.validate_repository(root)
        if errors:
            raise TaskOperationError("fanout rejected by fabric invariants:\n- " + "\n- ".join(errors))
    except Exception:
        for path in written:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        raise
    return candidates


def mark_parent_ready(root: Path, parent_id: str, *, at: str | None = None) -> dict[str, Any]:
    status = parent_status(root, parent_id)
    if not status["ready_for_parent_integration"]:
        raise TaskOperationError(
            f"parent {parent_id} not ready; incomplete required children: {status['incomplete_required']}"
        )
    previous = load_parent(root, parent_id)
    if previous.get("state") not in {"ACTIVE", "BLOCKED"}:
        raise TaskOperationError(f"parent-ready requires ACTIVE/BLOCKED, found {previous.get('state')}")
    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = "READY_FOR_INTEGRATION"
    candidate.setdefault("integration", {})["ready_for_integration_at"] = stamp
    candidate["integration"]["pr_state"] = "DRAFT"
    _append_note(candidate, f"Parent ready for master integration at {stamp}.")
    _write_parent_validated(root, parent_id, previous, candidate)
    return candidate


def _parent_unblocking_value(parent_id: str, tasks: dict[str, dict[str, Any]]) -> int:
    child_ids = {str(task["id"]) for task in children_for_parent(tasks, parent_id)}
    return sum(
        1
        for task in tasks.values()
        if task.get("state") not in {"MERGED_VERIFIED", "CANCELLED"}
        and child_ids.intersection(set(task.get("depends_on", [])))
    )


def integration_queue(root: Path) -> list[dict[str, Any]]:
    tasks = _validate_repo_or_raise(root)
    queue: list[dict[str, Any]] = []
    for parent_id, parent in _parents_or_raise(root).items():
        if parent.get("state") != "READY_FOR_INTEGRATION":
            continue
        queue.append(
            {
                "parent_id": parent_id,
                "priority": parent.get("priority"),
                "unblocking_value": _parent_unblocking_value(parent_id, tasks),
                "ready_for_integration_at": parent.get("integration", {}).get("ready_for_integration_at")
                or "9999-12-31T23:59:59Z",
            }
        )
    queue.sort(
        key=lambda item: (
            _priority_rank(str(item["priority"])),
            -int(item["unblocking_value"]),
            str(item["ready_for_integration_at"]),
            str(item["parent_id"]),
        )
    )
    return queue


def acquire_parent_integration(
    root: Path,
    parent_id: str,
    *,
    pull_request: int,
    current_master_sha: str,
    validated_head_sha: str,
    at: str | None = None,
) -> dict[str, Any]:
    queue = integration_queue(root)
    if not queue or queue[0]["parent_id"] != parent_id:
        raise TaskOperationError(f"parent {parent_id} is not first in the deterministic integration queue")
    parents = _parents_or_raise(root)
    for other_id, other in parents.items():
        if other_id != parent_id and other.get("state") in {"INTEGRATING", "MERGED_VERIFYING"}:
            raise TaskOperationError(f"master integration slot occupied by {other_id}")
    if not parent_status(root, parent_id)["ready_for_parent_integration"]:
        raise TaskOperationError(f"parent {parent_id} has incomplete required children")
    previous = load_parent(root, parent_id)
    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = "INTEGRATING"
    candidate.setdefault("integration", {}).update(
        {
            "pull_request": pull_request,
            "pr_state": "READY",
            "base_master_sha": current_master_sha,
            "validated_head_sha": validated_head_sha,
        }
    )
    _append_note(candidate, f"Acquired sole master integration slot at {stamp}.")
    _write_parent_validated(root, parent_id, previous, candidate)
    return candidate


def release_parent_integration(
    root: Path,
    parent_id: str,
    *,
    merge_sha: str,
    validated_head_sha: str,
    at: str | None = None,
) -> dict[str, Any]:
    previous = load_parent(root, parent_id)
    if previous.get("state") not in {"INTEGRATING", "MERGED_VERIFYING"}:
        raise TaskOperationError(
            f"release-integration requires INTEGRATING/MERGED_VERIFYING, found {previous.get('state')}"
        )
    integration = deepcopy(previous.get("integration", {}))
    if not isinstance(integration.get("pull_request"), int) or not integration.get("base_master_sha"):
        raise TaskOperationError("parent integration is missing PR/base-master evidence")
    status = parent_status(root, parent_id)
    child_ids = status["verified_pending"]
    if not child_ids:
        raise TaskOperationError("parent integration has no newly verified child work")
    stamp = at or iso_now()
    batch = {
        "pull_request": integration["pull_request"],
        "base_master_sha": integration["base_master_sha"],
        "validated_head_sha": validated_head_sha,
        "merge_sha": merge_sha,
        "post_merge_verified_at": stamp,
        "child_ids": child_ids,
    }
    candidate = deepcopy(previous)
    candidate.setdefault("integration_history", []).append(batch)
    candidate["state"] = "ACTIVE"
    candidate["integration"] = {
        "pull_request": None,
        "pr_state": None,
        "validated_head_sha": None,
        "merge_sha": None,
        "post_merge_verified_at": None,
        "ready_for_integration_at": None,
        "base_master_sha": None,
    }
    _append_note(candidate, f"Verified master batch {merge_sha} at {stamp}; parent returned to ACTIVE.")
    _write_parent_validated(root, parent_id, previous, candidate)
    return candidate


def request_parent_human_gate(
    root: Path,
    parent_id: str,
    *,
    kind: str,
    question: str,
    at: str | None = None,
) -> dict[str, Any]:
    if kind not in fabric.CRITICAL_HUMAN_GATES or not question.strip():
        raise TaskOperationError("parent human gate must be critical and ask one concrete question")
    previous = load_parent(root, parent_id)
    if previous.get("state") not in {"ACTIVE", "BLOCKED"}:
        raise TaskOperationError(f"parent gate request requires ACTIVE/BLOCKED, found {previous.get('state')}")
    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["state"] = "WAITING_HUMAN"
    candidate["human_gate"] = {
        "kind": kind,
        "status": "PENDING",
        "question": question,
        "decision": None,
        "decided_by": None,
        "decided_at": None,
    }
    _append_note(candidate, f"Critical parent human gate requested at {stamp}: {kind}.")
    _write_parent_validated(root, parent_id, previous, candidate)
    return candidate


def decide_parent_human_gate(
    root: Path,
    parent_id: str,
    *,
    status: str,
    decision: str,
    decided_by: str,
    at: str | None = None,
) -> dict[str, Any]:
    if status not in {"APPROVED", "REJECTED"}:
        raise TaskOperationError("human decision status must be APPROVED or REJECTED")
    previous = load_parent(root, parent_id)
    gate = previous.get("human_gate", {})
    if previous.get("state") != "WAITING_HUMAN" or gate.get("kind") not in fabric.CRITICAL_HUMAN_GATES:
        raise TaskOperationError("parent does not have a pending critical human gate")
    if gate.get("status") != "PENDING":
        raise TaskOperationError("parent human gate is not pending")
    stamp = at or iso_now()
    candidate = deepcopy(previous)
    candidate["human_gate"].update(
        {"status": status, "decision": decision, "decided_by": decided_by, "decided_at": stamp}
    )
    candidate["state"] = "ACTIVE"
    _append_note(candidate, f"Parent human gate {status.lower()} by {decided_by} at {stamp}: {decision}")
    _write_parent_validated(root, parent_id, previous, candidate)
    return candidate


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("summary")
    ready = sub.add_parser("ready")
    ready.add_argument("--parent")
    nxt = sub.add_parser("next")
    nxt.add_argument("--parent", required=True)

    show = sub.add_parser("show")
    show.add_argument("task_id")
    show_parent = sub.add_parser("show-parent")
    show_parent.add_argument("parent_id")

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

    spawn = sub.add_parser("spawn-child")
    spawn.add_argument("parent_id")
    spawn.add_argument("task_id")
    spawn.add_argument("--title", required=True)
    spawn.add_argument("--lane", required=True)
    spawn.add_argument("--priority", default="P1")
    spawn.add_argument("--path", action="append", required=True, dest="touched_paths")
    spawn.add_argument("--optional", action="store_true")

    integrate = sub.add_parser("integrate-child")
    integrate.add_argument("task_id")
    integrate.add_argument("--owner", required=True)
    integrate.add_argument("--target-parent-branch", required=True)
    integrate.add_argument("--validated-head-sha", required=True)
    integrate.add_argument("--at")

    verify = sub.add_parser("verify-child")
    verify.add_argument("task_id")
    verify.add_argument("--owner", required=True)
    verify.add_argument("--integrated-commit-sha", required=True)
    verify.add_argument("--at")

    fanout = sub.add_parser("fanout")
    fanout.add_argument("parent_id")
    fanout.add_argument("--spec-file", type=Path, required=True)

    pstatus = sub.add_parser("parent-status")
    pstatus.add_argument("parent_id")
    pready = sub.add_parser("parent-ready")
    pready.add_argument("parent_id")
    pready.add_argument("--at")
    sub.add_parser("queue")

    acquire = sub.add_parser("acquire-integration")
    acquire.add_argument("parent_id")
    acquire.add_argument("--pr", type=int, required=True)
    acquire.add_argument("--master-sha", required=True)
    acquire.add_argument("--validated-head-sha", required=True)
    acquire.add_argument("--at")

    release = sub.add_parser("release-integration")
    release.add_argument("parent_id")
    release.add_argument("--merge-sha", required=True)
    release.add_argument("--validated-head-sha", required=True)
    release.add_argument("--at")

    pgate = sub.add_parser("parent-human-gate")
    pgate.add_argument("parent_id")
    pgate.add_argument("--kind", required=True)
    pgate.add_argument("--question", required=True)
    pgate.add_argument("--at")

    pdecision = sub.add_parser("parent-human-decision")
    pdecision.add_argument("parent_id")
    pdecision.add_argument("--status", choices=["APPROVED", "REJECTED"], required=True)
    pdecision.add_argument("--decision", required=True)
    pdecision.add_argument("--by", required=True, dest="decided_by")
    pdecision.add_argument("--at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "summary":
            _print(summary(args.root))
        elif args.command == "ready":
            _print(list_ready(args.root, args.parent))
        elif args.command == "next":
            _print(next_ready(args.root, parent_id=args.parent))
        elif args.command == "show":
            _print(load_task(args.root, args.task_id))
        elif args.command == "show-parent":
            _print(load_parent(args.root, args.parent_id))
        elif args.command == "claim":
            _print(claim_task(args.root, args.task_id, owner=args.owner, branch=args.branch, at=args.at))
        elif args.command == "heartbeat":
            _print(heartbeat_task(args.root, args.task_id, owner=args.owner, at=args.at, note=args.note))
        elif args.command == "transition":
            _print(transition_task(
                args.root, args.task_id, owner=args.owner, target=args.target, at=args.at,
                note=args.note, pull_request=args.pull_request,
                validated_head_sha=args.validated_head_sha, merge_sha=args.merge_sha,
                blocker_reason=args.blocker_reason, blocker_evidence=args.blocker_evidence,
                blocker_next_action=args.blocker_next_action, human_kind=args.human_kind,
                human_question=args.human_question,
            ))
        elif args.command == "human-decision":
            _print(decide_human_gate(
                args.root, args.task_id, status=args.status, decision=args.decision,
                decided_by=args.decided_by, at=args.at,
            ))
        elif args.command == "spawn-child":
            _print(spawn_child(
                args.root, parent_id=args.parent_id, task_id=args.task_id, title=args.title,
                lane=args.lane, priority=args.priority, touched_paths=args.touched_paths,
                required_for_parent=not args.optional,
            ))
        elif args.command == "integrate-child":
            _print(integrate_child(
                args.root, args.task_id, owner=args.owner,
                target_parent_branch=args.target_parent_branch,
                validated_head_sha=args.validated_head_sha, at=args.at,
            ))
        elif args.command == "verify-child":
            _print(verify_child(
                args.root, args.task_id, owner=args.owner,
                integrated_commit_sha=args.integrated_commit_sha, at=args.at,
            ))
        elif args.command == "fanout":
            specs = json.loads(args.spec_file.read_text(encoding="utf-8"))
            if not isinstance(specs, list):
                raise TaskOperationError("fanout spec file must contain a JSON list")
            _print(fanout_children(args.root, parent_id=args.parent_id, specs=specs))
        elif args.command == "parent-status":
            _print(parent_status(args.root, args.parent_id))
        elif args.command == "parent-ready":
            _print(mark_parent_ready(args.root, args.parent_id, at=args.at))
        elif args.command == "queue":
            _print(integration_queue(args.root))
        elif args.command == "acquire-integration":
            _print(acquire_parent_integration(
                args.root, args.parent_id, pull_request=args.pr,
                current_master_sha=args.master_sha,
                validated_head_sha=args.validated_head_sha, at=args.at,
            ))
        elif args.command == "release-integration":
            _print(release_parent_integration(
                args.root, args.parent_id, merge_sha=args.merge_sha,
                validated_head_sha=args.validated_head_sha, at=args.at,
            ))
        elif args.command == "parent-human-gate":
            _print(request_parent_human_gate(
                args.root, args.parent_id, kind=args.kind, question=args.question, at=args.at,
            ))
        elif args.command == "parent-human-decision":
            _print(decide_parent_human_gate(
                args.root, args.parent_id, status=args.status, decision=args.decision,
                decided_by=args.decided_by, at=args.at,
            ))
    except (TaskOperationError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"agent-task: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
