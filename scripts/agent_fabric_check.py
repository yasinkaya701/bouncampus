#!/usr/bin/env python3
"""Validate the lightweight BOUNCAMPUS autonomous multi-agent control plane."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ".agents/fabric.json"
TEMPLATE_PATH = ".agents/TASK_TEMPLATE.json"

REQUIRED_TASK_KEYS = {
    "schema_version",
    "id",
    "title",
    "priority",
    "lane",
    "state",
    "owner_agent",
    "branch",
    "depends_on",
    "touched_paths",
    "acceptance_criteria",
    "validation_commands",
    "human_gate",
    "lease",
    "blocker",
    "integration",
    "notes",
}

ACTIVE_OWNERSHIP_STATES = {
    "CLAIMED",
    "ACTIVE",
    "BLOCKED",
    "WAITING_HUMAN",
    "READY_FOR_INTEGRATION",
    "INTEGRATING",
    "MERGED_VERIFYING",
}
POST_DEPENDENCY_STATES = ACTIVE_OWNERSHIP_STATES | {"MERGED_VERIFIED"}
VALIDATION_REQUIRED_STATES = {
    "READY_FOR_INTEGRATION",
    "INTEGRATING",
    "MERGED_VERIFYING",
    "MERGED_VERIFIED",
}
TASK_ID_RE = re.compile(r"^TASK-[A-Z0-9][A-Z0-9-]{2,63}$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def normalize_owned_path(raw: str) -> str:
    value = raw.strip().replace("\\", "/")
    if not value:
        raise ValueError("empty path")
    if value.startswith("/"):
        raise ValueError("absolute paths are not allowed")
    if value.startswith("./"):
        value = value[2:]
    if value.endswith("/**"):
        value = value[:-3]
    value = value.rstrip("/")
    if not value:
        raise ValueError("repository root ownership is not allowed")
    parts = [part for part in value.split("/") if part]
    if any(part in {".", ".."} for part in parts):
        raise ValueError("relative traversal is not allowed")
    return "/".join(parts)


def paths_overlap(left: str, right: str) -> bool:
    a = normalize_owned_path(left)
    b = normalize_owned_path(right)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def validate_config(config: dict[str, Any], errors: list[str]) -> None:
    required = {
        "schema_version",
        "control_branch",
        "coordination_task_dir",
        "branch_pattern",
        "integration",
        "lease",
        "priorities",
        "states",
        "active_states",
        "terminal_states",
        "human_gate_kinds",
        "human_gate_statuses",
        "autonomy_default",
    }
    missing = sorted(required - set(config))
    if missing:
        errors.append(f"{CONFIG_PATH}: missing required keys {missing}")
        return
    if config["schema_version"] != 1:
        errors.append(f"{CONFIG_PATH}: schema_version must be 1")
    if config["autonomy_default"] != "AUTONOMOUS":
        errors.append(f"{CONFIG_PATH}: autonomy_default must be AUTONOMOUS")
    states = set(config.get("states", []))
    active = set(config.get("active_states", []))
    terminal = set(config.get("terminal_states", []))
    if not active <= states:
        errors.append(f"{CONFIG_PATH}: active_states contains values not present in states")
    if not terminal <= states:
        errors.append(f"{CONFIG_PATH}: terminal_states contains values not present in states")
    if active & terminal:
        errors.append(f"{CONFIG_PATH}: active_states and terminal_states must be disjoint")
    if config.get("integration", {}).get("max_open_pull_requests") != 1:
        errors.append(f"{CONFIG_PATH}: max_open_pull_requests must remain 1")
    if config.get("integration", {}).get("merge_method") != "merge":
        errors.append(f"{CONFIG_PATH}: merge_method must remain 'merge'")
    ttl = config.get("lease", {}).get("default_ttl_minutes")
    if not isinstance(ttl, int) or ttl <= 0:
        errors.append(f"{CONFIG_PATH}: default_ttl_minutes must be a positive integer")
    try:
        re.compile(config.get("branch_pattern", ""))
    except re.error as exc:
        errors.append(f"{CONFIG_PATH}: invalid branch_pattern: {exc}")


def validate_task(
    task: dict[str, Any],
    source: str,
    config: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    *,
    template: bool,
    now: datetime,
    strict_stale: bool,
) -> None:
    missing = sorted(REQUIRED_TASK_KEYS - set(task))
    if missing:
        errors.append(f"{source}: missing required keys {missing}")
        return

    if task.get("schema_version") != config.get("schema_version"):
        errors.append(f"{source}: schema_version must match fabric schema")

    task_id = task.get("id")
    if not isinstance(task_id, str):
        errors.append(f"{source}: id must be a string")
    elif not template and not TASK_ID_RE.fullmatch(task_id):
        errors.append(f"{source}: invalid task id {task_id!r}")

    title = task.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"{source}: title must be non-empty")

    if task.get("priority") not in config.get("priorities", []):
        errors.append(f"{source}: invalid priority {task.get('priority')!r}")
    state = task.get("state")
    if state not in config.get("states", []):
        errors.append(f"{source}: invalid state {state!r}")
        return

    lane = task.get("lane")
    if not isinstance(lane, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", lane):
        errors.append(f"{source}: lane must be a lowercase slug")

    for field in ("depends_on", "touched_paths", "acceptance_criteria", "validation_commands", "notes"):
        if not isinstance(task.get(field), list):
            errors.append(f"{source}: {field} must be a list")

    if template:
        return

    depends_on = task.get("depends_on", [])
    if any(not isinstance(item, str) for item in depends_on):
        errors.append(f"{source}: depends_on entries must be task IDs")
    if task_id in depends_on:
        errors.append(f"{source}: task cannot depend on itself")
    if len(depends_on) != len(set(depends_on)):
        errors.append(f"{source}: duplicate dependency IDs are not allowed")

    touched_paths = task.get("touched_paths", [])
    for owned in touched_paths:
        if not isinstance(owned, str):
            errors.append(f"{source}: touched_paths entries must be strings")
            continue
        try:
            normalize_owned_path(owned)
        except ValueError as exc:
            errors.append(f"{source}: invalid touched path {owned!r}: {exc}")
    if state not in {"BACKLOG", "CANCELLED"} and not touched_paths:
        errors.append(f"{source}: {state} task must declare touched_paths")

    owner = task.get("owner_agent")
    branch = task.get("branch")
    if state in ACTIVE_OWNERSHIP_STATES or state == "MERGED_VERIFIED":
        if not isinstance(owner, str) or not owner.strip():
            errors.append(f"{source}: {state} task requires owner_agent")
        if not isinstance(branch, str) or not branch.strip():
            errors.append(f"{source}: {state} task requires branch")
        elif not re.fullmatch(config["branch_pattern"], branch):
            errors.append(f"{source}: branch {branch!r} does not match configured pattern")

    if state in VALIDATION_REQUIRED_STATES:
        if not task.get("acceptance_criteria"):
            errors.append(f"{source}: {state} task requires acceptance_criteria")
        if not task.get("validation_commands"):
            errors.append(f"{source}: {state} task requires validation_commands")

    gate = task.get("human_gate")
    if not isinstance(gate, dict):
        errors.append(f"{source}: human_gate must be an object")
    else:
        gate_kind = gate.get("kind")
        gate_status = gate.get("status")
        if gate_kind not in config.get("human_gate_kinds", []):
            errors.append(f"{source}: invalid human_gate.kind {gate_kind!r}")
        if gate_status not in config.get("human_gate_statuses", []):
            errors.append(f"{source}: invalid human_gate.status {gate_status!r}")
        if gate_kind == "NONE" and gate_status != "NOT_REQUIRED":
            errors.append(f"{source}: NONE human gate must use NOT_REQUIRED")
        if gate_kind != "NONE" and gate_status == "NOT_REQUIRED":
            errors.append(f"{source}: non-NONE human gate cannot use NOT_REQUIRED")
        if state == "WAITING_HUMAN":
            if gate_kind == "NONE" or gate_status != "PENDING":
                errors.append(f"{source}: WAITING_HUMAN requires a non-NONE PENDING human gate")
            if not isinstance(gate.get("question"), str) or not gate.get("question", "").strip():
                errors.append(f"{source}: WAITING_HUMAN requires one concrete human_gate.question")
        if gate_status in {"APPROVED", "REJECTED"}:
            for field in ("decision", "decided_by", "decided_at"):
                value = gate.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{source}: {gate_status} human gate requires {field}")
            if isinstance(gate.get("decided_at"), str) and gate.get("decided_at"):
                try:
                    parse_timestamp(gate["decided_at"])
                except ValueError as exc:
                    errors.append(f"{source}: invalid human gate decided_at: {exc}")

    lease = task.get("lease")
    if not isinstance(lease, dict):
        errors.append(f"{source}: lease must be an object")
    else:
        ttl = lease.get("ttl_minutes")
        if not isinstance(ttl, int) or ttl <= 0:
            errors.append(f"{source}: lease.ttl_minutes must be a positive integer")
        if state in ACTIVE_OWNERSHIP_STATES or state == "MERGED_VERIFIED":
            for field in ("claimed_at", "heartbeat_at"):
                value = lease.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{source}: {state} task requires lease.{field}")
            heartbeat = lease.get("heartbeat_at")
            if isinstance(heartbeat, str) and heartbeat.strip() and isinstance(ttl, int) and ttl > 0:
                try:
                    heartbeat_at = parse_timestamp(heartbeat)
                    if state not in {"INTEGRATING", "MERGED_VERIFYING", "MERGED_VERIFIED"}:
                        expires_at = heartbeat_at + timedelta(minutes=ttl)
                        if now > expires_at:
                            message = (
                                f"{source}: lease is stale since {expires_at.isoformat()} "
                                f"(heartbeat {heartbeat_at.isoformat()}, ttl={ttl}m)"
                            )
                            (errors if strict_stale else warnings).append(message)
                except ValueError as exc:
                    errors.append(f"{source}: invalid lease.heartbeat_at: {exc}")
            claimed = lease.get("claimed_at")
            if isinstance(claimed, str) and claimed.strip():
                try:
                    parse_timestamp(claimed)
                except ValueError as exc:
                    errors.append(f"{source}: invalid lease.claimed_at: {exc}")

    blocker = task.get("blocker")
    if state == "BLOCKED":
        if not isinstance(blocker, dict):
            errors.append(f"{source}: BLOCKED task requires blocker object")
        else:
            for field in ("reason", "evidence", "next_action"):
                value = blocker.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{source}: BLOCKED task requires blocker.{field}")

    integration = task.get("integration")
    if not isinstance(integration, dict):
        errors.append(f"{source}: integration must be an object")
    else:
        if state == "INTEGRATING" and not isinstance(integration.get("pull_request"), int):
            errors.append(f"{source}: INTEGRATING requires integration.pull_request")
        if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
            if not isinstance(integration.get("merge_sha"), str) or not integration.get("merge_sha", "").strip():
                errors.append(f"{source}: {state} requires integration.merge_sha")
        if state == "MERGED_VERIFIED":
            for field in ("pull_request", "validated_head_sha", "merge_sha", "post_merge_verified_at"):
                value = integration.get(field)
                if field == "pull_request":
                    if not isinstance(value, int):
                        errors.append(f"{source}: MERGED_VERIFIED requires integration.pull_request")
                elif not isinstance(value, str) or not value.strip():
                    errors.append(f"{source}: MERGED_VERIFIED requires integration.{field}")
            verified = integration.get("post_merge_verified_at")
            if isinstance(verified, str) and verified.strip():
                try:
                    parse_timestamp(verified)
                except ValueError as exc:
                    errors.append(f"{source}: invalid post_merge_verified_at: {exc}")


def load_tasks(root: Path, config: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    task_dir = root / config.get("coordination_task_dir", "")
    if not task_dir.is_dir():
        return {}
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(task_dir.glob("*.json")):
        try:
            task = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: cannot read task JSON: {exc}")
            continue
        task_id = task.get("id")
        source = str(path.relative_to(root))
        if isinstance(task_id, str):
            if task_id in tasks:
                errors.append(f"{source}: duplicate task id {task_id}")
            else:
                tasks[task_id] = task
        else:
            errors.append(f"{source}: task id missing or non-string")
    return tasks


def validate_dependencies(tasks: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for task_id, task in tasks.items():
        for dep in task.get("depends_on", []):
            if dep not in tasks:
                errors.append(f"{task_id}: dependency {dep} does not exist")
                continue
            if task.get("state") in POST_DEPENDENCY_STATES and tasks[dep].get("state") != "MERGED_VERIFIED":
                errors.append(
                    f"{task_id}: state {task.get('state')} requires dependency {dep} to be MERGED_VERIFIED "
                    f"(found {tasks[dep].get('state')})"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, stack: list[str]) -> None:
        if task_id in visited:
            return
        if task_id in visiting:
            start = stack.index(task_id) if task_id in stack else 0
            errors.append("dependency cycle: " + " -> ".join(stack[start:] + [task_id]))
            return
        visiting.add(task_id)
        stack.append(task_id)
        for dep in tasks[task_id].get("depends_on", []):
            if dep in tasks:
                visit(dep, stack)
        stack.pop()
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id, [])


def validate_path_ownership(tasks: dict[str, dict[str, Any]], errors: list[str]) -> None:
    active = [
        (task_id, task)
        for task_id, task in tasks.items()
        if task.get("state") in ACTIVE_OWNERSHIP_STATES
    ]
    for index, (left_id, left_task) in enumerate(active):
        for right_id, right_task in active[index + 1 :]:
            for left_path in left_task.get("touched_paths", []):
                for right_path in right_task.get("touched_paths", []):
                    if not isinstance(left_path, str) or not isinstance(right_path, str):
                        continue
                    try:
                        overlaps = paths_overlap(left_path, right_path)
                    except ValueError:
                        continue
                    if overlaps:
                        errors.append(
                            f"path ownership conflict: {left_id} owns {left_path!r} and "
                            f"{right_id} owns {right_path!r}"
                        )


def validate_repository(
    root: Path,
    *,
    now: datetime | None = None,
    strict_stale: bool = False,
) -> tuple[list[str], list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    warnings: list[str] = []
    now = now or datetime.now(timezone.utc)

    config_file = root / CONFIG_PATH
    template_file = root / TEMPLATE_PATH
    if not config_file.is_file():
        return [f"missing required file: {CONFIG_PATH}"], warnings, {}
    if not template_file.is_file():
        return [f"missing required file: {TEMPLATE_PATH}"], warnings, {}

    try:
        config = load_json(config_file)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{CONFIG_PATH}: cannot read JSON: {exc}"], warnings, {}
    if not isinstance(config, dict):
        return [f"{CONFIG_PATH}: top-level value must be an object"], warnings, {}

    validate_config(config, errors)

    try:
        template = load_json(template_file)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{TEMPLATE_PATH}: cannot read JSON: {exc}")
        template = None
    if isinstance(template, dict):
        validate_task(
            template,
            TEMPLATE_PATH,
            config,
            errors,
            warnings,
            template=True,
            now=now,
            strict_stale=strict_stale,
        )
    elif template is not None:
        errors.append(f"{TEMPLATE_PATH}: top-level value must be an object")

    tasks = load_tasks(root, config, errors)
    for task_id, task in tasks.items():
        source = f"{config.get('coordination_task_dir')}/{task_id}.json"
        validate_task(
            task,
            source,
            config,
            errors,
            warnings,
            template=False,
            now=now,
            strict_stale=strict_stale,
        )

    validate_dependencies(tasks, errors)
    validate_path_ownership(tasks, errors)
    return errors, warnings, tasks


def ready_task_ids(tasks: dict[str, dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for task_id, task in tasks.items():
        if task.get("state") != "READY":
            continue
        deps = task.get("depends_on", [])
        if all(tasks.get(dep, {}).get("state") == "MERGED_VERIFIED" for dep in deps):
            gate = task.get("human_gate", {})
            if gate.get("status") not in {"PENDING", "REJECTED"}:
                result.append(task_id)
    return sorted(result)


def print_summary(tasks: dict[str, dict[str, Any]]) -> None:
    counts: dict[str, int] = {}
    human_waiting: list[str] = []
    for task_id, task in tasks.items():
        state = str(task.get("state"))
        counts[state] = counts.get(state, 0) + 1
        if state == "WAITING_HUMAN":
            human_waiting.append(task_id)
    print("AGENT FABRIC SUMMARY")
    print("states:", json.dumps(dict(sorted(counts.items())), sort_keys=True))
    print("ready:", json.dumps(ready_task_ids(tasks)))
    print("waiting_human:", json.dumps(sorted(human_waiting)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    parser.add_argument("--strict-stale", action="store_true", help="treat stale leases as errors")
    parser.add_argument("--summary", action="store_true", help="print task-state summary")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, warnings, tasks = validate_repository(args.root, strict_stale=args.strict_stale)

    for warning in warnings:
        print(f"AGENT FABRIC WARNING: {warning}")

    if errors:
        print("AGENT FABRIC VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AGENT FABRIC VALIDATION: PASS")
    print("- fabric configuration is valid")
    print("- task template is structurally valid")
    print(f"- coordination tasks validated: {len(tasks)}")
    print("- dependency graph and active path ownership are conflict-free")
    print("- lease, blocker, human-gate, and integration invariants hold")
    if args.summary:
        print_summary(tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
