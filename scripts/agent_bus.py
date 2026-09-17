#!/usr/bin/env python3
"""BOUNCAMPUS multi-agent coordination and branch-independent message bus."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
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
DEFAULT_MESSAGE_TYPES = {
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
    """Expected coordination/runtime failure."""


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
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except Exception as exc:  # pragma: no cover - exact decoder text varies
        raise AgentBusError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AgentBusError(f"expected JSON object in {path}")
    return value


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
    for rel in (
        "tasks",
        "leases",
        "heartbeats",
        "messages",
        "acks",
        "locks",
        "remote-cache",
    ):
        (base / rel).mkdir(parents=True, exist_ok=True)


def slug(value: str, field: str) -> str:
    if not SLUG_RE.match(value):
        raise AgentBusError(f"{field} must match {SLUG_RE.pattern}; got {value!r}")
    return value


def iter_json(path: Path) -> Iterable[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.glob("*.json") if p.is_file())


def normalize_repo_path(value: str) -> str:
    path = value.strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    path = path.rstrip("/")
    if not path or path.startswith("/") or ".." in Path(path).parts:
        raise AgentBusError(f"invalid repository path: {value!r}")
    return path


def paths_overlap(left: str, right: str) -> bool:
    left = normalize_repo_path(left)
    right = normalize_repo_path(right)
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def task_path(root: Path, task_id: str) -> Path:
    return agents_dir(root) / "tasks" / f"{slug(task_id, 'task-id')}.json"


def lease_path(root: Path, task_id: str) -> Path:
    return agents_dir(root) / "leases" / f"{slug(task_id, 'task-id')}.json"


def heartbeat_path(root: Path, agent: str) -> Path:
    return agents_dir(root) / "heartbeats" / f"{slug(agent, 'agent')}.json"


def merge_lock_path(root: Path) -> Path:
    return agents_dir(root) / "locks" / "merge.json"


def message_path(root: Path, message_id: str) -> Path:
    return agents_dir(root) / "messages" / f"{slug(message_id, 'message-id')}.json"


def ack_path(root: Path, message_id: str, agent: str) -> Path:
    return (
        agents_dir(root)
        / "acks"
        / slug(message_id, "message-id")
        / f"{slug(agent, 'agent')}.json"
    )


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


def conflicting_task(root: Path, task_id: str, paths: list[str]) -> tuple[str, str] | None:
    for path in iter_json(agents_dir(root) / "tasks"):
        other = read_json(path)
        if other.get("task_id") == task_id:
            continue
        if other.get("state") not in ACTIVE_OWNERSHIP_STATES:
            continue
        for owned in other.get("paths", []):
            for candidate in paths:
                if paths_overlap(str(owned), candidate):
                    return str(other.get("task_id")), str(owned)
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


def configured_message_types(root: Path) -> set[str]:
    values = config(root).get("message_types", sorted(DEFAULT_MESSAGE_TYPES))
    return {str(value).upper() for value in values}


def create_message(
    root: Path,
    from_agent: str,
    to_agent: str,
    message_type: str,
    subject: str,
    body: str,
    task_id: str | None = None,
    requires_ack: bool = False,
    reply_to: str | None = None,
    retry_of: str | None = None,
) -> dict[str, Any]:
    ensure_runtime_dirs(root)
    from_agent = slug(from_agent, "from-agent")
    if to_agent != "all":
        to_agent = slug(to_agent, "to-agent")
    message_type = message_type.upper()
    allowed = configured_message_types(root)
    if message_type not in allowed:
        raise AgentBusError(f"invalid message type {message_type}; allowed: {sorted(allowed)}")
    if task_id is not None:
        slug(task_id, "task-id")
    if reply_to is not None:
        slug(reply_to, "reply-to")
    if retry_of is not None:
        slug(retry_of, "retry-of")
    if not subject.strip() or not body.strip():
        raise AgentBusError("message subject and body must be non-empty")

    now = utcnow()
    message_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:12]}"
    payload: dict[str, Any] = {
        "schema_version": 1,
        "message_id": message_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "type": message_type,
        "task_id": task_id,
        "subject": subject.strip(),
        "body": body.strip(),
        "requires_ack": bool(requires_ack),
        "created_at": iso(now),
    }
    if reply_to:
        payload["reply_to"] = reply_to
    if retry_of:
        payload["retry_of"] = retry_of
    atomic_write(message_path(root, message_id), payload)
    return payload


def remote_bus_config(root: Path) -> dict[str, Any]:
    value = config(root).get("remote_bus", {})
    if not isinstance(value, dict):
        raise AgentBusError("remote_bus config must be an object")
    return value


def remote_enabled(root: Path) -> bool:
    return bool(remote_bus_config(root).get("enabled", False))


def github_token(root: Path) -> str | None:
    names = remote_bus_config(root).get("token_env", ["GITHUB_TOKEN", "GH_TOKEN"])
    for name in names:
        value = os.environ.get(str(name))
        if value:
            return value
    return None


def require_remote_token(root: Path, offline: bool) -> str | None:
    if offline or not remote_enabled(root):
        return None
    token = github_token(root)
    if not token:
        raise AgentBusError(
            "remote agent bus is enabled but no GITHUB_TOKEN/GH_TOKEN is available; "
            "use --offline only when branch-independent delivery is intentionally not required"
        )
    return token


def github_request(
    root: Path,
    method: str,
    api_path: str,
    payload: dict[str, Any] | None = None,
) -> Any:
    token = github_token(root)
    if not token:
        raise AgentBusError("GitHub token missing for remote agent bus")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.github.com{api_path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "bouncampus-agent-bus/1",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AgentBusError(f"GitHub API {exc.code} for {api_path}: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise AgentBusError(f"GitHub API unavailable for {api_path}: {exc}") from exc
    return json.loads(raw) if raw else None


def remote_issue_parts(root: Path) -> tuple[str, int, str]:
    remote = remote_bus_config(root)
    if remote.get("transport") != "github_issue":
        raise AgentBusError("unsupported remote bus transport")
    repository = str(config(root).get("repository", ""))
    if "/" not in repository:
        raise AgentBusError("config.repository must be owner/name")
    issue = int(remote.get("issue_number", 0))
    if issue <= 0:
        raise AgentBusError("remote_bus.issue_number must be positive")
    marker = str(remote.get("marker", "BOUNCAMPUS_AGENT_BUS_V1"))
    return repository, issue, marker


def render_remote_envelope(root: Path, payload: dict[str, Any]) -> str:
    _, _, marker = remote_issue_parts(root)
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return f"<!-- {marker} -->\n```json\n{rendered}\n```"


def parse_remote_envelope(root: Path, body: str) -> dict[str, Any] | None:
    _, _, marker = remote_issue_parts(root)
    if f"<!-- {marker} -->" not in body:
        return None
    match = re.search(r"```json\s*(\{.*?\})\s*```", body, flags=re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        return None
    return payload


def publish_remote(root: Path, payload: dict[str, Any], offline: bool) -> None:
    require_remote_token(root, offline)
    if offline or not remote_enabled(root):
        return
    repository, issue, _ = remote_issue_parts(root)
    github_request(
        root,
        "POST",
        f"/repos/{repository}/issues/{issue}/comments",
        {"body": render_remote_envelope(root, payload)},
    )


def fetch_remote_messages(root: Path, offline: bool) -> list[dict[str, Any]]:
    require_remote_token(root, offline)
    if offline or not remote_enabled(root):
        return []
    repository, issue, _ = remote_issue_parts(root)
    messages: list[dict[str, Any]] = []
    page = 1
    while True:
        comments = github_request(
            root,
            "GET",
            f"/repos/{repository}/issues/{issue}/comments?per_page=100&page={page}",
        )
        if not isinstance(comments, list):
            raise AgentBusError("unexpected GitHub comments response")
        for comment in comments:
            if not isinstance(comment, dict):
                continue
            payload = parse_remote_envelope(root, str(comment.get("body", "")))
            if payload is None:
                continue
            payload = dict(payload)
            payload["remote_comment_id"] = comment.get("id")
            messages.append(payload)
        if len(comments) < 100:
            break
        page += 1
    messages.sort(key=lambda item: (str(item.get("created_at", "")), str(item.get("message_id", ""))))
    return messages


def sync_remote(root: Path, offline: bool) -> int:
    ensure_runtime_dirs(root)
    count = 0
    for payload in fetch_remote_messages(root, offline):
        message_id = payload.get("message_id")
        if not isinstance(message_id, str) or not SLUG_RE.match(message_id):
            continue
        path = message_path(root, message_id)
        if path.exists():
            continue
        atomic_write(path, payload)
        count += 1
    return count


def message_acknowledged(root: Path, message: dict[str, Any]) -> bool:
    message_id = str(message.get("message_id", ""))
    ack_dir = agents_dir(root) / "acks" / message_id
    if ack_dir.exists() and any(ack_dir.glob("*.json")):
        return True
    for path in iter_json(agents_dir(root) / "messages"):
        candidate = read_json(path)
        if candidate.get("type") == "ACK" and candidate.get("reply_to") == message_id:
            return True
    return False


def cmd_init(args: argparse.Namespace) -> None:
    root = root_from(args)
    config(root)
    ensure_runtime_dirs(root)
    print(str(agents_dir(root)))


def cmd_sync(args: argparse.Namespace) -> None:
    root = root_from(args)
    if args.agent:
        slug(args.agent, "agent")
    count = sync_remote(root, args.offline)
    print(f"synced {count} new message(s)")


def cmd_claim(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    cfg = config(root)
    agent = slug(args.agent, "agent")
    task_id = slug(args.task_id, "task-id")
    lanes = set(cfg.get("lanes", []))
    if args.lane not in lanes:
        raise AgentBusError(f"unknown lane {args.lane!r}; allowed: {sorted(lanes)}")
    paths = [normalize_repo_path(value) for value in args.paths]
    if not paths:
        raise AgentBusError("at least one path is required")
    path = task_path(root, task_id)
    if path.exists():
        task = read_json(path)
        if task.get("state") == TERMINAL_STATE:
            raise AgentBusError(f"task {task_id} is already {TERMINAL_STATE}")
        if task.get("owner_agent") != agent:
            raise AgentBusError(f"task {task_id} already owned by {task.get('owner_agent')}")
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
        "history": [{"at": now, "event": "CLAIMED", "actor": agent, "paths": paths}],
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
    root = root_from(args)
    message = create_message(
        root,
        args.from_agent,
        args.to_agent,
        args.type,
        args.subject,
        args.body,
        args.task_id,
        args.requires_ack,
    )
    publish_remote(root, message, args.offline)
    print(json.dumps(message, ensure_ascii=False))


def cmd_inbox(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    sync_remote(root, args.offline)
    messages: list[dict[str, Any]] = []
    for path in iter_json(agents_dir(root) / "messages"):
        message = read_json(path)
        if message.get("to_agent") not in {agent, "all"}:
            continue
        acknowledged = message_acknowledged(root, message)
        if args.unread_only and acknowledged:
            continue
        item = dict(message)
        item["acknowledged"] = acknowledged
        messages.append(item)
    messages.sort(key=lambda item: (str(item.get("created_at", "")), str(item.get("message_id", ""))))
    print(json.dumps(messages, ensure_ascii=False, indent=2))


def cmd_ack(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    sync_remote(root, args.offline)
    message_id = slug(args.message_id, "message-id")
    path = message_path(root, message_id)
    if not path.exists():
        raise AgentBusError(f"unknown message: {message_id}")
    message = read_json(path)
    if message.get("to_agent") not in {agent, "all"}:
        raise AgentBusError(f"message {message_id} is not addressed to {agent}")
    atomic_write(
        ack_path(root, message_id, agent),
        {
            "schema_version": 1,
            "message_id": message_id,
            "agent": agent,
            "acknowledged_at": iso(),
        },
    )
    ack_message = create_message(
        root,
        agent,
        str(message.get("from_agent")),
        "ACK",
        f"ACK: {message.get('subject', message_id)}",
        f"Acknowledged message {message_id}.",
        message.get("task_id"),
        False,
        reply_to=message_id,
    )
    publish_remote(root, ack_message, args.offline)
    print("ok")


def cmd_pending_acks(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    sync_remote(root, args.offline)
    pending: list[dict[str, Any]] = []
    for path in iter_json(agents_dir(root) / "messages"):
        message = read_json(path)
        if message.get("from_agent") != agent or not message.get("requires_ack"):
            continue
        if not message_acknowledged(root, message):
            pending.append(message)
    print(json.dumps(pending, ensure_ascii=False, indent=2))


def cmd_retry(args: argparse.Namespace) -> None:
    root = root_from(args)
    sync_remote(root, args.offline)
    message_id = slug(args.message_id, "message-id")
    path = message_path(root, message_id)
    if not path.exists():
        raise AgentBusError(f"unknown message: {message_id}")
    original = read_json(path)
    if message_acknowledged(root, original) and not args.force:
        raise AgentBusError("message is already acknowledged; use --force to retry anyway")
    retried = create_message(
        root,
        str(original["from_agent"]),
        str(original["to_agent"]),
        str(original["type"]),
        f"RETRY: {original['subject']}",
        str(original["body"]),
        original.get("task_id"),
        bool(original.get("requires_ack")),
        retry_of=message_id,
    )
    publish_remote(root, retried, args.offline)
    print(json.dumps(retried, ensure_ascii=False))


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
    task["blocker"] = {"reason": args.reason, "next_action": args.next_action, "at": iso()}
    task_history(task, "BLOCKED", agent, reason=args.reason)
    atomic_write(task_path(root, task["task_id"]), task)
    message = create_message(
        root,
        agent,
        "all",
        "BLOCKER",
        f"{task['task_id']} blocked",
        f"{args.reason}\nNext action: {args.next_action}",
        task["task_id"],
        False,
    )
    publish_remote(root, message, args.offline)
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
    message = create_message(
        root,
        from_agent,
        to_agent,
        "HANDOFF",
        f"Handoff: {task['task_id']}",
        f"Reason: {args.reason}\nNext action: {args.next_action}",
        task["task_id"],
        True,
    )
    publish_remote(root, message, args.offline)
    print("ok")


def cmd_reassign(args: argparse.Namespace) -> None:
    root = root_from(args)
    actor = slug(args.actor, "actor")
    new_agent = slug(args.new_agent, "new-agent")
    task = load_task(root, args.task_id)
    if task["state"] not in {"ACTIVE", "BLOCKED"}:
        raise AgentBusError("reassignment is only allowed for ACTIVE/BLOCKED tasks")
    lease_file = lease_path(root, task["task_id"])
    expired = True
    if lease_file.exists():
        lease = read_json(lease_file)
        expired = parse_iso(str(lease["expires_at"])) <= utcnow()
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
    print("ok")


def cmd_lock_acquire(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    agent = slug(args.agent, "agent")
    task = load_task(root, args.task_id)
    assert_owner(task, agent)
    if task["state"] != "READY_FOR_INTEGRATION":
        raise AgentBusError(f"merge lock requires READY_FOR_INTEGRATION; got {task['state']}")
    path = merge_lock_path(root)
    if path.exists():
        current = read_json(path)
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
    atomic_write(path, lock)
    task["state"] = "INTEGRATING"
    task_history(task, "MERGE_LOCK_ACQUIRED", agent)
    atomic_write(task_path(root, task["task_id"]), task)
    write_lease(root, task)
    print(json.dumps(lock))


def cmd_lock_renew(args: argparse.Namespace) -> None:
    root = root_from(args)
    agent = slug(args.agent, "agent")
    path = merge_lock_path(root)
    if not path.exists():
        raise AgentBusError("merge lock is not held")
    lock = read_json(path)
    if lock.get("agent") != agent or lock.get("task_id") != args.task_id:
        raise AgentBusError("merge lock is held by another task/agent")
    lock["expires_at"] = iso(merge_lock_expiry(root))
    lock["renewed_at"] = iso()
    atomic_write(path, lock)
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
    path = merge_lock_path(root)
    if not path.exists():
        raise AgentBusError("merge lock missing")
    lock = read_json(path)
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


def validate_message(root: Path, message: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "message_id",
        "from_agent",
        "to_agent",
        "type",
        "subject",
        "body",
        "requires_ack",
        "created_at",
    }
    missing = sorted(required - set(message))
    if missing:
        errors.append(f"{path}: missing {missing}")
    if message.get("type") not in configured_message_types(root):
        errors.append(f"{path}: invalid type {message.get('type')!r}")
    if message.get("schema_version") != 1:
        errors.append(f"{path}: unsupported schema_version")
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
                        overlap = paths_overlap(str(left_path), str(right_path))
                    except AgentBusError as exc:
                        errors.append(str(exc))
                        overlap = False
                    if overlap:
                        errors.append(
                            "ownership overlap: "
                            f"{left.get('task_id')}:{left_path} <-> {right.get('task_id')}:{right_path}"
                        )

    for path in iter_json(agents_dir(root) / "messages"):
        try:
            errors.extend(validate_message(root, read_json(path), path))
        except AgentBusError as exc:
            errors.append(str(exc))

    ack_root = agents_dir(root) / "acks"
    if ack_root.exists():
        for path in sorted(ack_root.glob("*/*.json")):
            try:
                ack = read_json(path)
                if ack.get("schema_version") != 1 or not ack.get("message_id") or not ack.get("agent"):
                    errors.append(f"{path}: invalid acknowledgement")
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


def cmd_status(args: argparse.Namespace) -> None:
    root = root_from(args)
    ensure_runtime_dirs(root)
    tasks = [read_json(path) for path in iter_json(agents_dir(root) / "tasks")]
    lock = read_json(merge_lock_path(root)) if merge_lock_path(root).exists() else None
    pending = 0
    for path in iter_json(agents_dir(root) / "messages"):
        message = read_json(path)
        if message.get("requires_ack") and not message_acknowledged(root, message):
            pending += 1
    print(
        json.dumps(
            {"tasks": tasks, "merge_lock": lock, "pending_ack_messages": pending},
            ensure_ascii=False,
            indent=2,
        )
    )


def add_offline(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--offline",
        action="store_true",
        help="do not access the branch-independent GitHub issue bus",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("sync")
    p.add_argument("--agent")
    add_offline(p)
    p.set_defaults(func=cmd_sync)

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
    add_offline(p)
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("inbox")
    p.add_argument("--agent", required=True)
    p.add_argument("--unread-only", action="store_true")
    add_offline(p)
    p.set_defaults(func=cmd_inbox)

    p = sub.add_parser("ack")
    p.add_argument("--message-id", required=True)
    p.add_argument("--agent", required=True)
    add_offline(p)
    p.set_defaults(func=cmd_ack)

    p = sub.add_parser("pending-acks")
    p.add_argument("--agent", required=True)
    add_offline(p)
    p.set_defaults(func=cmd_pending_acks)

    p = sub.add_parser("retry")
    p.add_argument("--message-id", required=True)
    p.add_argument("--force", action="store_true")
    add_offline(p)
    p.set_defaults(func=cmd_retry)

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
    add_offline(p)
    p.set_defaults(func=cmd_block)

    p = sub.add_parser("handoff")
    p.add_argument("--task-id", required=True)
    p.add_argument("--from-agent", required=True)
    p.add_argument("--to-agent", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--next-action", required=True)
    add_offline(p)
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
    add_offline(p)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

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
