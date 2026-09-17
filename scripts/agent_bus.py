#!/usr/bin/env python3
"""Repository-native coordination bus for BOUNCAMPUS agents."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

ACTIVE_OWNERSHIP_STATES = {
    "ACTIVE",
    "READY_FOR_INTEGRATION",
    "INTEGRATING",
    "MERGED_VERIFYING",
    "BLOCKED",
}
TERMINAL_STATE = "MERGED_VERIFIED"
ALLOWED_STATES = ACTIVE_OWNERSHIP_STATES | {TERMINAL_STATE}
ALLOWED_MESSAGE_TYPES = {
    "INFO",
    "REQUEST",
    "DECISION",
    "BLOCKER",
    "HANDOFF",
    "REVIEW",
    "ACK",
}
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class AgentBusError(RuntimeError):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    return (dt or utcnow()).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def root_from(args: argparse.Namespace) -> Path:
    return Path(args.root).resolve()


def agents_dir(root: Path) -> Path:
    return root / ".agents"


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except Exception as exc:
        raise AgentBusError(f"invalid JSON in {path}: {exc}") from exc


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def config(root: Path) -> dict[str, Any]:
    path = agents_dir(root) / "config.json"
    if not path.exists():
        raise AgentBusError(f"missing config: {path}")
    data = read_json(path)
    if data.get("schema_version") != 1:
        raise AgentBusError("unsupported .agents/config.json schema_version")
    return data


def ensure_runtime_dirs(root: Path) -> None:
    base = agents_dir(root)
    for rel in ("tasks", "leases", "heartbeats", "messages", "acks", "locks"):
        (base / rel).mkdir(parents=True, exist_ok=True)


def slug(value: str, field: str) -> str:
    if not SLUG_RE.match(value):
        raise AgentBusError(f"{field} must match {SLUG_RE.pattern}; got {value!r}")
    return value


def task_path(root: Path, task_id: str) -> Path:
    return agents_dir(root) / "tasks" / f"{slug(task_id, 'task-id')}.json"


def lease_path(root: Path, task_id: str) -> Path:
    return agents_dir(root) / "leases" / f"{slug(task_id, 'task-id')}.json"


def heartbeat_path(root: Path, agent: str) -> Path:
    return agents_dir(root) / "heartbeats" / f"{slug(agent, 'agent')}.json"


def merge_lock_path(root: Path) -> Path:
    return agents_dir(root) / "locks" / "merge.json"


def iter_json(path: Path) -> Iterable[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.glob("*.json") if p.is_file())


def normalize_repo_path(value: str) -> str:
    p = value.strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    p = p.rstrip("/")
    if not p or p.startswith("/") or ".." in Path(p).parts:
        raise AgentBusError(f"invalid repository path: {value!r}")
    return p


def paths_overlap(a: str, b: str) -> bool:
    a = normalize_repo_path(a)
    b = normalize_repo_path(b)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def load_task(root: Path, task_id: str) -> dict[str, Any]:
    path = task_path(root, task_id)
    if not path.exists():
        raise AgentBusError(f"unknown task: {task_id}")
    task = read_json(path)
    if task.get("state") not in ALLOWED_STATES:
        raise AgentBusError(f"task {task_id} has invalid state {task.get('state')!r}")
    return task


def assert_owner(task: dict[str, Any], agent: str) -> None:
    if task.get("owner_agent") != agent:
        raise AgentBusError(
            f"task {task.get('task_id')} is owned by {task.get('owner_agent')}, not {agent}"
        )


def task_history(task: dict[str, Any], event: str, actor: str, **extra: Any) -> None:
    task.setdefault("history", []).append(
        {"at": iso(), "event": event, "actor": actor, **extra}
    )
    task["updated_at"] = iso()


def lease_expiry(root: Path) -> datetime:
    ttl = int(config(root).get("lease_ttl_minutes", 45))
    return utcnow() + timedelta(minutes=ttl)


def merge_lock_expiry(root: Path) -> datetime:
    ttl = int(config(root).get("merge_lock_ttl_minutes", 30))
    return utcnow() + timedelta(minutes=ttl)


def conflicting_task(
    root: Path, task_id: str, paths: list[str]
) -> tuple[str, str] | None:
    for path in iter_json(agents_dir(root) / "tasks"):
        other = read_json(path)
        if other.get("task_id") == task_id:
            continue
        if other.get("state") not in ACTIVE_OWNERSHIP_STATES:
            continue
        for owned in other.get("paths", []):
            for candidate in paths:
                if paths_overlap(owned, candidate):
                    return str(other.get("task_id")), owned
    return None


def write_lease(root: Path, task: dict[str, Any]) -> None:
    atomic_write(
        lease_path(root, str(task["task_id"])),
        {
            "schema_version": 1,
            "task_id": task["task_id"],
            "agent": task["owner_agent"],
            "lane": task["lane"],
            "paths": task["paths"],
            "renewed_at": iso(),
            "expires_at": iso(lease_expiry(root)),
        },
    )


def write_heartbeat(root: Path, agent: str, task_id: str | None) -> None:
    atomic_write(
        heartbeat_path(root, agent),
        {"schema_version": 1, "agent": agent, "task_id": task_id, "at": iso()},
    )


def create_message(
    root: Path,
    from_agent: str,
    to_agent: str,
    message_type: str,
    subject: str,
    body: str,
    task_id: str | None = None,
    requires_ack: bool = False,
) -> dict[str, Any]:
    ensure_runtime_dirs(root)
    from_agent = slug(from_agent, "from-agent")
    if to_agent != "all":
        to_agent = slug(to_agent, "to-agent")
    message_type = message_type.upper()
    if message_type not in ALLOWED_MESSAGE_TYPES:
        raise AgentBusError(
            f"invalid message type {message_type}; allowed: {sorted(ALLOWED_MESSAGE_TYPES)}"
        )
    if task_id is not None:
        slug(task_id, "task-id")
    now = utcnow()
    msg_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:12]}"
    payload = {
        "schema_version": 1,
        "message_id": msg_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "type": message_type,
        "task_id": task_id,
        "subject": subject.strip(),
        "body": body.strip(),
        "requires_ack": bool(requires_ack),
        "created_at": iso(now),
    }
    atomic_write(agents_dir(root) / "messages" / f"{msg_id}.json", payload)
    return payload


def ack_path(root: Path, message_id: str, agent: str) -> Path:
    return (
        agents_dir(root)
        / "acks"
        / slug(message_id, "message-id")
        / f"{slug(agent, 'agent')}.json"
    )


def cmd_init(args: argparse.Namespace) -> None:
    root = root_from(args)
    config(root)
    ensure_runtime_dirs(root)
    print(str(agents_dir(root)))


def cmd_claim(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    cfg = config(root)
    agent = slug(args.agent, "agent")
    task_id = slug(args.task_id, "task-id")
    lanes = set(cfg.get("lanes", []))
    if args.lane not in lanes:
        raise AgentBusError(f"unknown lane {args.lane!r}; allowed: {sorted(lanes)}")
    paths = [normalize_repo_path(p) for p in args.paths]
    if not paths:
        raise AgentBusError("at least one path is required")

    path = task_path(root, task_id)
    if path.exists():
        task = read_json(path)
        if task.get("state") == TERMINAL_STATE:
            raise AgentBusError(f"task {task_id} is already {TERMINAL_STATE}")
        if task.get("owner_agent") != agent:
            raise AgentBusError(
                f"task {task_id} already owned by {task.get('owner_agent')}"
            )
    conflict = conflicting_task(root, task_id, paths)
    if conflict:
        other, owned = conflict
        raise AgentBusError(f"path ownership conflict with task {other}: {owned}")

    now = iso()
    task = {
        "schema_version": 1,
        "task_id": task_id,
        "owner_agent": agent,
        "lane": args.lane,
        "branch": args.branch,
        "scope": args.scope,
        "paths": paths,
        "state": "ACTIVE",
        "claimed_at": now,
        "updated_at": now,
        "history": [
            {"at": now, "event": "CLAIMED", "actor": agent, "paths": paths}
        ],
        "evidence": [],
    }
    atomic_write(path, task)
    write_lease(root, task)
    write_heartbeat(root, agent, task_id)
    print(json.dumps(task, ensure_ascii=False))


def cmd_heartbeat(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] == TERMINAL_STATE:
        raise AgentBusError("cannot heartbeat a completed task")
    write_lease(root, task)
    write_heartbeat(root, agent, task["task_id"])
    task_history(task, "HEARTBEAT", agent)
    atomic_write(task_path(root, task["task_id"]), task)
    print("ok")


def cmd_send(args: argparse.Namespace) -> None:
    msg = create_message(
        root_from(args),
        args.from_agent,
        args.to_agent,
        args.type,
        args.subject,
        args.body,
        args.task_id,
        args.requires_ack,
    )
    print(json.dumps(msg, ensure_ascii=False))


def cmd_ack(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    msg_id = slug(args.message_id, "message-id")
    message_path = agents_dir(root) / "messages" / f"{msg_id}.json"
    if not message_path.exists():
        raise AgentBusError(f"unknown message: {msg_id}")
    msg = read_json(message_path)
    if msg.get("to_agent") not in {agent, "all"}:
        raise AgentBusError(f"message {msg_id} is not addressed to {agent}")
    atomic_write(
        ack_path(root, msg_id, agent),
        {
            "schema_version": 1,
            "message_id": msg_id,
            "agent": agent,
            "acknowledged_at": iso(),
        },
    )
    print("ok")


def cmd_inbox(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    messages: list[dict[str, Any]] = []
    for path in iter_json(agents_dir(root) / "messages"):
        msg = read_json(path)
        if msg.get("to_agent") not in {agent, "all"}:
            continue
        acknowledged = ack_path(root, str(msg["message_id"]), agent).exists()
        if args.unread_only and acknowledged:
            continue
        item = dict(msg)
        item["acknowledged"] = acknowledged
        messages.append(item)
    messages.sort(key=lambda item: item.get("created_at", ""))
    print(json.dumps(messages, ensure_ascii=False, indent=2))


def cmd_ready(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] != "ACTIVE":
        raise AgentBusError(f"ready requires ACTIVE; got {task['state']}")
    task["state"] = "READY_FOR_INTEGRATION"
    task["evidence"].extend(args.evidence or [])
    task_history(task, "READY_FOR_INTEGRATION", agent)
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    print("ok")


def cmd_block(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] == TERMINAL_STATE:
        raise AgentBusError("cannot block a completed task")
    task["state"] = "BLOCKED"
    task["blocker"] = {
        "reason": args.reason,
        "next_action": args.next_action,
        "at": iso(),
    }
    task_history(task, "BLOCKED", agent, reason=args.reason)
    atomic_write(task_path(root, task["task_id"]), task)
    create_message(
        root,
        agent,
        "all",
        "BLOCKER",
        f"{task['task_id']} blocked",
        f"{args.reason}\nNext action: {args.next_action}",
        task["task_id"],
        True,
    )
    print("ok")


def cmd_handoff(args: argparse.Namespace) -> None:
    root = root_from(args)
    from_agent = slug(args.from_agent, "from-agent")
    to_agent = slug(args.to_agent, "to-agent")
    task = load_task(root, args.task_id)
    assert_owner(task, from_agent)
    if task["state"] not in {"ACTIVE", "BLOCKED"}:
        raise AgentBusError(
            "handoff is only allowed during ACTIVE/BLOCKED work; integration ownership cannot be handed off"
        )
    task["owner_agent"] = to_agent
    task["state"] = "ACTIVE"
    task.pop("blocker", None)
    task_history(
        task,
        "HANDOFF",
        from_agent,
        to_agent=to_agent,
        reason=args.reason,
        next_action=args.next_action,
    )
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    write_heartbeat(root, to_agent, task["task_id"])
    create_message(
        root,
        from_agent,
        to_agent,
        "HANDOFF",
        f"Handoff: {task['task_id']}",
        f"Reason: {args.reason}\nNext action: {args.next_action}",
        task["task_id"],
        True,
    )
    print("ok")


def cmd_reassign(args: argparse.Namespace) -> None:
    root = root_from(args)
    actor = slug(args.actor, "actor")
    new_agent = slug(args.new_agent, "new-agent")
    task = load_task(root, args.task_id)
    if task["state"] not in {"ACTIVE", "BLOCKED"}:
        raise AgentBusError("reassignment is only allowed for ACTIVE/BLOCKED tasks")
    lease_file = lease_path(root, task["task_id"])
    if lease_file.exists():
        lease = read_json(lease_file)
        expired = parse_iso(str(lease["expires_at"])) <= utcnow()
    else:
        expired = True
    if not expired and not args.force:
        raise AgentBusError("lease is still active; use normal handoff or --force")
    previous = str(task["owner_agent"])
    task["owner_agent"] = new_agent
    task["state"] = "ACTIVE"
    task.pop("blocker", None)
    task_history(
        task,
        "REASSIGNED",
        actor,
        previous_agent=previous,
        new_agent=new_agent,
        reason=args.reason,
    )
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    write_heartbeat(root, new_agent, task["task_id"])
    create_message(
        root,
        actor,
        new_agent,
        "HANDOFF",
        f"Reassigned: {task['task_id']}",
        f"Previous owner: {previous}\nReason: {args.reason}",
        task["task_id"],
        True,
    )
    print("ok")


def cmd_lock_acquire(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] != "READY_FOR_INTEGRATION":
        raise AgentBusError(
            f"merge lock requires READY_FOR_INTEGRATION; got {task['state']}"
        )
    lock_path = merge_lock_path(root)
    if lock_path.exists():
        current = read_json(lock_path)
        expired = parse_iso(str(current["expires_at"])) <= utcnow()
        same = current.get("task_id") == task["task_id"] and current.get("agent") == agent
        if not same and not (expired and args.force_stale):
            raise AgentBusError(
                f"merge lock held by {current.get('agent')} for {current.get('task_id')}"
            )
    lock = {
        "schema_version": 1,
        "task_id": task["task_id"],
        "agent": agent,
        "acquired_at": iso(),
        "expires_at": iso(merge_lock_expiry(root)),
    }
    atomic_write(lock_path, lock)
    task["state"] = "INTEGRATING"
    task_history(task, "MERGE_LOCK_ACQUIRED", agent)
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    print(json.dumps(lock))


def cmd_lock_renew(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    lock_path = merge_lock_path(root)
    if not lock_path.exists():
        raise AgentBusError("merge lock is not held")
    lock = read_json(lock_path)
    if lock.get("agent") != agent or lock.get("task_id") != args.task_id:
        raise AgentBusError("merge lock is held by another task/agent")
    lock["expires_at"] = iso(merge_lock_expiry(root))
    lock["renewed_at"] = iso()
    atomic_write(lock_path, lock)
    task = load_task(root, args.task_id)
    write_lease(root, task)
    write_heartbeat(root, agent, task["task_id"])
    print("ok")


def cmd_merged(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] != "INTEGRATING":
        raise AgentBusError(f"merged requires INTEGRATING; got {task['state']}")
    lock_path = merge_lock_path(root)
    if not lock_path.exists():
        raise AgentBusError("merge lock missing")
    lock = read_json(lock_path)
    if lock.get("agent") != agent or lock.get("task_id") != task["task_id"]:
        raise AgentBusError("merge lock is held by another task/agent")
    task["state"] = "MERGED_VERIFYING"
    task["merge_sha"] = args.merge_sha
    task_history(task, "MERGED_VERIFYING", agent, merge_sha=args.merge_sha)
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    print("ok")


def cmd_verify(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] != "MERGED_VERIFYING":
        raise AgentBusError(f"verify requires MERGED_VERIFYING; got {task['state']}")
    task["state"] = TERMINAL_STATE
    task["evidence"].extend(args.evidence or [])
    task_history(task, "MERGED_VERIFIED", agent)
    atomic_write(task_path(root, task["task_id"]), task)
    lease_file = lease_path(root, task["task_id"])
    if lease_file.exists():
        lease_file.unlink()
    lock_path = merge_lock_path(root)
    if lock_path.exists():
        lock = read_json(lock_path)
        if lock.get("task_id") == task["task_id"] and lock.get("agent") == agent:
            lock_path.unlink()
    write_heartbeat(root, agent, None)
    print("ok")


def validate_message(msg: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "message_id",
        "from_agent",
        "to_agent",
        "type",
        "subject",
        "body",
        "requires_ack",
        "created_at",
    }
    missing = sorted(required - set(msg))
    if missing:
        errors.append(f"{path}: missing {missing}")
    if msg.get("type") not in ALLOWED_MESSAGE_TYPES:
        errors.append(f"{path}: invalid type {msg.get('type')!r}")
    return errors


def cmd_validate(args: argparse.Namespace) -> None:
    root = root_from(args)
    cfg = config(root)
    errors: list[str] = []
    tasks: list[dict[str, Any]] = []
    for path in iter_json(agents_dir(root) / "tasks"):
        try:
            task = read_json(path)
        except AgentBusError as exc:
            errors.append(str(exc))
            continue
        tasks.append(task)
        if task.get("state") not in ALLOWED_STATES:
            errors.append(f"{path}: invalid state {task.get('state')!r}")
        if task.get("lane") not in set(cfg.get("lanes", [])):
            errors.append(f"{path}: invalid lane {task.get('lane')!r}")
        if not isinstance(task.get("paths"), list) or not task.get("paths"):
            errors.append(f"{path}: paths must be a non-empty list")

    owning = [task for task in tasks if task.get("state") in ACTIVE_OWNERSHIP_STATES]
    for index, left in enumerate(owning):
        for right in owning[index + 1 :]:
            for left_path in left.get("paths", []):
                for right_path in right.get("paths", []):
                    try:
                        overlap = paths_overlap(left_path, right_path)
                    except AgentBusError as exc:
                        errors.append(str(exc))
                        overlap = False
                    if overlap:
                        errors.append(
                            "ownership overlap: "
                            f"{left.get('task_id')}:{left_path} <-> "
                            f"{right.get('task_id')}:{right_path}"
                        )

    for path in iter_json(agents_dir(root) / "messages"):
        try:
            errors.extend(validate_message(read_json(path), path))
        except AgentBusError as exc:
            errors.append(str(exc))

    lock_path = merge_lock_path(root)
    if lock_path.exists():
        try:
            lock = read_json(lock_path)
            matching = [
                task
                for task in tasks
                if task.get("task_id") == lock.get("task_id")
                and task.get("owner_agent") == lock.get("agent")
                and task.get("state") in {"INTEGRATING", "MERGED_VERIFYING"}
            ]
            if not matching:
                errors.append(
                    f"{lock_path}: lock does not match an INTEGRATING/MERGED_VERIFYING task"
                )
        except AgentBusError as exc:
            errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise AgentBusError(f"coordination validation failed with {len(errors)} error(s)")
    message_count = len(list(iter_json(agents_dir(root) / "messages")))
    print(f"ok: {len(tasks)} task(s), {message_count} message(s)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("claim")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--lane", required=True)
    p.add_argument("--branch", required=True)
    p.add_argument("--scope", required=True)
    p.add_argument("--paths", nargs="+", required=True)
    p.set_defaults(func=cmd_claim)

    p = sub.add_parser("heartbeat")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_heartbeat)

    p = sub.add_parser("send")
    p.add_argument("--from-agent", required=True)
    p.add_argument("--to-agent", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--task-id")
    p.add_argument("--subject", required=True)
    p.add_argument("--body", required=True)
    p.add_argument("--requires-ack", action="store_true")
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("inbox")
    p.add_argument("--agent", required=True)
    p.add_argument("--unread-only", action="store_true")
    p.set_defaults(func=cmd_inbox)

    p = sub.add_parser("ack")
    p.add_argument("--message-id", required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_ack)

    p = sub.add_parser("ready")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--evidence", action="append")
    p.set_defaults(func=cmd_ready)

    p = sub.add_parser("block")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--next-action", required=True)
    p.set_defaults(func=cmd_block)

    p = sub.add_parser("handoff")
    p.add_argument("--task-id", required=True)
    p.add_argument("--from-agent", required=True)
    p.add_argument("--to-agent", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--next-action", required=True)
    p.set_defaults(func=cmd_handoff)

    p = sub.add_parser("reassign")
    p.add_argument("--task-id", required=True)
    p.add_argument("--actor", required=True)
    p.add_argument("--new-agent", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_reassign)

    p = sub.add_parser("lock-acquire")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--force-stale", action="store_true")
    p.set_defaults(func=cmd_lock_acquire)

    p = sub.add_parser("lock-renew")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_lock_renew)

    p = sub.add_parser("merged")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--merge-sha", required=True)
    p.set_defaults(func=cmd_merged)

    p = sub.add_parser("verify")
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--evidence", action="append")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("validate")
    p.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except AgentBusError as exc:
        print(f"agent-bus: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
