#!/usr/bin/env python3
"""Validate the BOUNCAMPUS autonomous parent/child agent fabric."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ".agents/fabric.json"
TEMPLATE_PATH = ".agents/TASK_TEMPLATE.json"
PARENT_TEMPLATE_PATH = ".agents/PARENT_WORKSTREAM_TEMPLATE.json"

REQUIRED_TASK_KEYS_V1 = {
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
REQUIRED_TASK_KEYS_V2 = REQUIRED_TASK_KEYS_V1 | {
    "parent_id",
    "required_for_parent",
    "produces",
    "consumes",
    "child_integration",
}
REQUIRED_PARENT_KEYS = {
    "schema_version",
    "id",
    "role",
    "human_owner",
    "objective",
    "priority",
    "state",
    "parent_branch",
    "child_ids",
    "human_gate",
    "integration",
    "integration_history",
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
CRITICAL_HUMAN_GATES = {
    "EVIDENCE_ATTESTATION",
    "IRREVERSIBLE_ACTION",
    "PHYSICAL_SAFETY",
    "EXTERNAL_COMMITMENT",
    "PRODUCT_DIRECTION",
}
DEFAULT_PARENT_STATES = {
    "ACTIVE",
    "BLOCKED",
    "WAITING_HUMAN",
    "READY_FOR_INTEGRATION",
    "INTEGRATING",
    "MERGED_VERIFYING",
    "COMPLETE",
}
TASK_ID_RE = re.compile(r"^TASK-[A-Z0-9][A-Z0-9-]{2,63}$")
PARENT_ID_RE = re.compile(r"^HUMAN-(IE|EE|CS1|CS2)(?:-[A-Z0-9-]+)?$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")


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


def _validate_string_list(value: Any, source: str, field: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{source}: {field} must be a list")
        return
    bad = [item for item in value if not isinstance(item, str) or not item.strip()]
    if bad:
        errors.append(f"{source}: {field} entries must be non-empty strings")
    if len(value) != len(set(value)):
        errors.append(f"{source}: duplicate {field} entries are not allowed")


def _validate_sha(value: Any, source: str, field: str, errors: list[str], *, required: bool = True) -> None:
    if value is None and not required:
        return
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        errors.append(f"{source}: {field} must be a git SHA string")


def _validate_human_gate(
    gate: Any,
    *,
    source: str,
    state: str,
    config: dict[str, Any],
    errors: list[str],
) -> None:
    if not isinstance(gate, dict):
        errors.append(f"{source}: human_gate must be an object")
        return
    kind = gate.get("kind")
    status = gate.get("status")
    allowed_kinds = set(config.get("human_gate_kinds", []))
    allowed_statuses = set(config.get("human_gate_statuses", []))
    if kind not in allowed_kinds:
        errors.append(f"{source}: invalid human_gate.kind {kind!r}")
    if kind not in CRITICAL_HUMAN_GATES | {"NONE"}:
        errors.append(f"{source}: human gate {kind!r} is not a critical gate")
    if status not in allowed_statuses:
        errors.append(f"{source}: invalid human_gate.status {status!r}")
    if kind == "NONE" and status != "NOT_REQUIRED":
        errors.append(f"{source}: NONE human gate must use NOT_REQUIRED")
    if kind != "NONE" and status == "NOT_REQUIRED":
        errors.append(f"{source}: non-NONE human gate cannot use NOT_REQUIRED")
    if state == "WAITING_HUMAN":
        if kind not in CRITICAL_HUMAN_GATES or status != "PENDING":
            errors.append(f"{source}: WAITING_HUMAN requires a critical PENDING human gate")
        question = gate.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"{source}: WAITING_HUMAN requires one concrete human_gate.question")
    if status in {"APPROVED", "REJECTED"}:
        for field in ("decision", "decided_by", "decided_at"):
            value = gate.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{source}: {status} human gate requires {field}")
        decided_at = gate.get("decided_at")
        if isinstance(decided_at, str) and decided_at.strip():
            try:
                parse_timestamp(decided_at)
            except ValueError as exc:
                errors.append(f"{source}: invalid human gate decided_at: {exc}")


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

    schema = config.get("schema_version")
    if schema not in {1, 2}:
        errors.append(f"{CONFIG_PATH}: schema_version must be 1 or 2")
    if config.get("autonomy_default") != "AUTONOMOUS":
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

    if set(config.get("human_gate_kinds", [])) != CRITICAL_HUMAN_GATES | {"NONE"}:
        errors.append(f"{CONFIG_PATH}: human gates must be NONE plus the five critical gate kinds")
    ttl = config.get("lease", {}).get("default_ttl_minutes")
    if not isinstance(ttl, int) or ttl <= 0:
        errors.append(f"{CONFIG_PATH}: default_ttl_minutes must be a positive integer")
    try:
        re.compile(config.get("branch_pattern", ""))
    except re.error as exc:
        errors.append(f"{CONFIG_PATH}: invalid branch_pattern: {exc}")

    integration = config.get("integration", {})
    if integration.get("merge_method") != "merge":
        errors.append(f"{CONFIG_PATH}: merge_method must remain 'merge'")

    if schema == 1:
        if integration.get("max_open_pull_requests") != 1:
            errors.append(f"{CONFIG_PATH}: schema-v1 max_open_pull_requests must remain 1")
        return

    v2_required = {
        "coordination_parent_dir",
        "parent_branch_pattern",
        "parent_roles",
        "human_parent_limit_per_role",
        "child_agent_limit",
        "parent_states",
    }
    missing_v2 = sorted(v2_required - set(config))
    if missing_v2:
        errors.append(f"{CONFIG_PATH}: schema-v2 missing {missing_v2}")
        return
    if config.get("parent_roles") != ["IE", "EE", "CS1", "CS2"]:
        errors.append(f"{CONFIG_PATH}: parent_roles must be exactly IE, EE, CS1, CS2")
    if config.get("human_parent_limit_per_role") != 1:
        errors.append(f"{CONFIG_PATH}: human_parent_limit_per_role must be 1")
    if config.get("child_agent_limit") is not None:
        errors.append(f"{CONFIG_PATH}: child_agent_limit must be null; safety is contract-limited, not count-limited")
    if set(config.get("parent_states", [])) != DEFAULT_PARENT_STATES:
        errors.append(f"{CONFIG_PATH}: parent_states do not match persistent parent lifecycle")
    try:
        re.compile(config.get("parent_branch_pattern", ""))
    except re.error as exc:
        errors.append(f"{CONFIG_PATH}: invalid parent_branch_pattern: {exc}")
    if integration.get("max_parent_pull_requests") != 4:
        errors.append(f"{CONFIG_PATH}: max_parent_pull_requests must be 4")
    if integration.get("max_integration_ready_pull_requests") != 1:
        errors.append(f"{CONFIG_PATH}: max_integration_ready_pull_requests must be 1")
    if integration.get("child_target_must_be_parent_branch") is not True:
        errors.append(f"{CONFIG_PATH}: child_target_must_be_parent_branch must be true")


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
    schema = task.get("schema_version")
    if schema not in {1, 2}:
        errors.append(f"{source}: schema_version must be 1 or 2")
        return
    required = REQUIRED_TASK_KEYS_V2 if schema == 2 else REQUIRED_TASK_KEYS_V1
    missing = sorted(required - set(task))
    if missing:
        errors.append(f"{source}: missing required keys {missing}")
        return
    if config.get("schema_version") == 1 and schema != 1:
        errors.append(f"{source}: schema-v2 task requires fabric schema v2")

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
    if schema == 2:
        for field in ("produces", "consumes"):
            _validate_string_list(task.get(field), source, field, errors)
        if not isinstance(task.get("required_for_parent"), bool):
            errors.append(f"{source}: required_for_parent must be boolean")

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

    if schema == 2:
        parent_id = task.get("parent_id")
        if not isinstance(parent_id, str) or not PARENT_ID_RE.fullmatch(parent_id):
            errors.append(f"{source}: schema-v2 task requires valid parent_id")
        child_integration = task.get("child_integration")
        if not isinstance(child_integration, dict):
            errors.append(f"{source}: child_integration must be an object")
        else:
            target = child_integration.get("target_parent_branch")
            if target == "master":
                errors.append(f"{source}: child integration may not target master")
            if state == "INTEGRATING":
                if not isinstance(target, str) or not target.strip():
                    errors.append(f"{source}: INTEGRATING child requires child_integration.target_parent_branch")
                _validate_sha(child_integration.get("validated_head_sha"), source, "child_integration.validated_head_sha", errors)
            if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
                _validate_sha(child_integration.get("validated_head_sha"), source, "child_integration.validated_head_sha", errors)
                _validate_sha(child_integration.get("integrated_commit_sha"), source, "child_integration.integrated_commit_sha", errors)
            if state == "MERGED_VERIFIED":
                verified_at = child_integration.get("verified_at")
                if not isinstance(verified_at, str) or not verified_at.strip():
                    errors.append(f"{source}: MERGED_VERIFIED child requires child_integration.verified_at")
                else:
                    try:
                        parse_timestamp(verified_at)
                    except ValueError as exc:
                        errors.append(f"{source}: invalid child verified_at: {exc}")

    owner = task.get("owner_agent")
    branch = task.get("branch")
    if state in ACTIVE_OWNERSHIP_STATES or state == "MERGED_VERIFIED":
        if not isinstance(owner, str) or not owner.strip():
            errors.append(f"{source}: {state} task requires owner_agent")
        elif schema == 2 and not owner.startswith("agent:"):
            errors.append(f"{source}: schema-v2 owner_agent must use agent:<identity>")
        if not isinstance(branch, str) or not branch.strip():
            errors.append(f"{source}: {state} task requires branch")
        elif not re.fullmatch(config.get("branch_pattern", ""), branch):
            errors.append(f"{source}: branch {branch!r} does not match configured pattern")

    if state in VALIDATION_REQUIRED_STATES:
        if not task.get("acceptance_criteria"):
            errors.append(f"{source}: {state} task requires acceptance_criteria")
        if not task.get("validation_commands"):
            errors.append(f"{source}: {state} task requires validation_commands")

    _validate_human_gate(task.get("human_gate"), source=source, state=state, config=config, errors=errors)

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

    if schema == 1:
        integration = task.get("integration")
        if not isinstance(integration, dict):
            errors.append(f"{source}: integration must be an object")
        else:
            if state == "INTEGRATING" and not isinstance(integration.get("pull_request"), int):
                errors.append(f"{source}: INTEGRATING requires integration.pull_request")
            if state in {"MERGED_VERIFYING", "MERGED_VERIFIED"}:
                _validate_sha(integration.get("merge_sha"), source, "integration.merge_sha", errors)
            if state == "MERGED_VERIFIED":
                if not isinstance(integration.get("pull_request"), int):
                    errors.append(f"{source}: MERGED_VERIFIED requires integration.pull_request")
                _validate_sha(integration.get("validated_head_sha"), source, "integration.validated_head_sha", errors)
                verified = integration.get("post_merge_verified_at")
                if not isinstance(verified, str) or not verified.strip():
                    errors.append(f"{source}: MERGED_VERIFIED requires integration.post_merge_verified_at")
                else:
                    try:
                        parse_timestamp(verified)
                    except ValueError as exc:
                        errors.append(f"{source}: invalid post_merge_verified_at: {exc}")


def _validate_parent_history(parent: dict[str, Any], source: str, errors: list[str]) -> None:
    history = parent.get("integration_history")
    if not isinstance(history, list):
        errors.append(f"{source}: integration_history must be a list")
        return
    seen_prs: set[int] = set()
    integrated_children: set[str] = set()
    for index, entry in enumerate(history):
        label = f"{source}: integration_history[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        pr = entry.get("pull_request")
        if not isinstance(pr, int):
            errors.append(f"{label}.pull_request must be integer")
        elif pr in seen_prs:
            errors.append(f"{label}: duplicate pull request {pr}")
        else:
            seen_prs.add(pr)
        for field in ("base_master_sha", "validated_head_sha", "merge_sha"):
            _validate_sha(entry.get(field), label, field, errors)
        verified_at = entry.get("post_merge_verified_at")
        if not isinstance(verified_at, str) or not verified_at.strip():
            errors.append(f"{label}.post_merge_verified_at is required")
        else:
            try:
                parse_timestamp(verified_at)
            except ValueError as exc:
                errors.append(f"{label}: invalid post_merge_verified_at: {exc}")
        children = entry.get("child_ids")
        if not isinstance(children, list) or not children:
            errors.append(f"{label}.child_ids must be a non-empty list")
        else:
            for child_id in children:
                if not isinstance(child_id, str) or not TASK_ID_RE.fullmatch(child_id):
                    errors.append(f"{label}: invalid child id {child_id!r}")
                elif child_id in integrated_children:
                    errors.append(f"{label}: child {child_id} appears in multiple verified parent batches")
                else:
                    integrated_children.add(child_id)


def validate_parent(
    parent: dict[str, Any],
    source: str,
    config: dict[str, Any],
    errors: list[str],
    *,
    template: bool,
) -> None:
    missing = sorted(REQUIRED_PARENT_KEYS - set(parent))
    if missing:
        errors.append(f"{source}: missing required keys {missing}")
        return
    if parent.get("schema_version") != 2:
        errors.append(f"{source}: parent schema_version must be 2")
    parent_id = parent.get("id")
    if not isinstance(parent_id, str):
        errors.append(f"{source}: parent id must be a string")
    elif not template and not PARENT_ID_RE.fullmatch(parent_id):
        errors.append(f"{source}: invalid parent id {parent_id!r}")
    role = parent.get("role")
    if role not in config.get("parent_roles", []):
        errors.append(f"{source}: invalid parent role {role!r}")
    human_owner = parent.get("human_owner")
    if not isinstance(human_owner, str) or not human_owner.startswith("human:") or len(human_owner) <= 6:
        errors.append(f"{source}: human_owner must use human:<identity>")
    objective = parent.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        errors.append(f"{source}: objective must be non-empty")
    if parent.get("priority") not in config.get("priorities", []):
        errors.append(f"{source}: invalid priority {parent.get('priority')!r}")
    state = parent.get("state")
    if state not in set(config.get("parent_states", DEFAULT_PARENT_STATES)):
        errors.append(f"{source}: invalid parent state {state!r}")
        return
    branch = parent.get("parent_branch")
    if not isinstance(branch, str) or not re.fullmatch(config.get("parent_branch_pattern", ""), branch):
        errors.append(f"{source}: invalid parent_branch {branch!r}")
    _validate_string_list(parent.get("child_ids"), source, "child_ids", errors)
    _validate_string_list(parent.get("notes"), source, "notes", errors)
    _validate_human_gate(parent.get("human_gate"), source=source, state=state, config=config, errors=errors)
    _validate_parent_history(parent, source, errors)

    integration = parent.get("integration")
    if not isinstance(integration, dict):
        errors.append(f"{source}: integration must be an object")
        return
    pr_state = integration.get("pr_state")
    if pr_state is not None and pr_state not in config.get("parent_pr_states", []):
        errors.append(f"{source}: invalid parent integration.pr_state {pr_state!r}")
    if state == "READY_FOR_INTEGRATION":
        ready_at = integration.get("ready_for_integration_at")
        if not isinstance(ready_at, str) or not ready_at.strip():
            errors.append(f"{source}: READY_FOR_INTEGRATION requires ready_for_integration_at")
        elif template is False:
            try:
                parse_timestamp(ready_at)
            except ValueError as exc:
                errors.append(f"{source}: invalid ready_for_integration_at: {exc}")
        if pr_state != "DRAFT":
            errors.append(f"{source}: READY_FOR_INTEGRATION requires integration.pr_state DRAFT")
    if state in {"INTEGRATING", "MERGED_VERIFYING"}:
        if not isinstance(integration.get("pull_request"), int):
            errors.append(f"{source}: {state} parent requires integration.pull_request")
        if pr_state != "READY":
            errors.append(f"{source}: {state} parent requires integration.pr_state READY")
        _validate_sha(integration.get("base_master_sha"), source, "integration.base_master_sha", errors)
        _validate_sha(integration.get("validated_head_sha"), source, "integration.validated_head_sha", errors)
    if state == "MERGED_VERIFYING":
        _validate_sha(integration.get("merge_sha"), source, "integration.merge_sha", errors)


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


def load_parents(root: Path, config: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    if config.get("schema_version") != 2:
        return {}
    parent_dir = root / config.get("coordination_parent_dir", "")
    if not parent_dir.is_dir():
        return {}
    parents: dict[str, dict[str, Any]] = {}
    for path in sorted(parent_dir.glob("*.json")):
        try:
            parent = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: cannot read parent JSON: {exc}")
            continue
        parent_id = parent.get("id")
        source = str(path.relative_to(root))
        if isinstance(parent_id, str):
            if parent_id in parents:
                errors.append(f"{source}: duplicate parent id {parent_id}")
            else:
                parents[parent_id] = parent
        else:
            errors.append(f"{source}: parent id missing or non-string")
    return parents


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
    active = [(task_id, task) for task_id, task in tasks.items() if task.get("state") in ACTIVE_OWNERSHIP_STATES]
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
                            f"path ownership conflict: {left_id} owns {left_path!r} and {right_id} owns {right_path!r}"
                        )


def validate_parent_uniqueness(parents: dict[str, dict[str, Any]], errors: list[str]) -> None:
    by_role: dict[str, str] = {}
    by_human: dict[str, str] = {}
    for parent_id, parent in parents.items():
        role = parent.get("role")
        human = parent.get("human_owner")
        if isinstance(role, str):
            if role in by_role:
                errors.append(f"duplicate active parent role {role}: {by_role[role]} and {parent_id}")
            else:
                by_role[role] = parent_id
        if isinstance(human, str):
            if human in by_human:
                errors.append(f"human owner {human} has multiple active parents: {by_human[human]} and {parent_id}")
            else:
                by_human[human] = parent_id


def validate_child_parents(
    tasks: dict[str, dict[str, Any]],
    parents: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    for task_id, task in tasks.items():
        if task.get("schema_version") != 2:
            continue
        parent_id = task.get("parent_id")
        if parent_id not in parents:
            errors.append(f"{task_id}: parent {parent_id} does not exist")
            continue
        parent = parents[parent_id]
        if parent.get("state") == "COMPLETE" and task.get("state") not in {"CANCELLED", "MERGED_VERIFIED"}:
            errors.append(f"{task_id}: active child cannot belong to COMPLETE parent {parent_id}")
        child_integration = task.get("child_integration", {})
        target = child_integration.get("target_parent_branch") if isinstance(child_integration, dict) else None
        if target is not None and target != parent.get("parent_branch"):
            errors.append(
                f"{task_id}: child integration target {target!r} must equal parent branch {parent.get('parent_branch')!r}"
            )


def validate_parent_history_links(
    tasks: dict[str, dict[str, Any]],
    parents: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    for parent_id, parent in parents.items():
        for index, entry in enumerate(parent.get("integration_history", [])):
            if not isinstance(entry, dict):
                continue
            for child_id in entry.get("child_ids", []):
                child = tasks.get(child_id)
                if child is None:
                    errors.append(f"{parent_id}: integration_history[{index}] references missing child {child_id}")
                elif child.get("schema_version") == 2 and child.get("parent_id") != parent_id:
                    errors.append(f"{parent_id}: historical child {child_id} belongs to {child.get('parent_id')}")
                elif child.get("state") != "MERGED_VERIFIED":
                    errors.append(f"{parent_id}: historical child {child_id} is not MERGED_VERIFIED")


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

    if config.get("schema_version") == 2:
        parent_template_file = root / PARENT_TEMPLATE_PATH
        if not parent_template_file.is_file():
            errors.append(f"missing required file: {PARENT_TEMPLATE_PATH}")
        else:
            try:
                parent_template = load_json(parent_template_file)
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{PARENT_TEMPLATE_PATH}: cannot read JSON: {exc}")
                parent_template = None
            if isinstance(parent_template, dict):
                validate_parent(parent_template, PARENT_TEMPLATE_PATH, config, errors, template=True)
            elif parent_template is not None:
                errors.append(f"{PARENT_TEMPLATE_PATH}: top-level value must be an object")

    tasks = load_tasks(root, config, errors)
    for task_id, task in tasks.items():
        validate_task(
            task,
            f"{config.get('coordination_task_dir')}/{task_id}.json",
            config,
            errors,
            warnings,
            template=False,
            now=now,
            strict_stale=strict_stale,
        )

    parents = load_parents(root, config, errors)
    for parent_id, parent in parents.items():
        validate_parent(
            parent,
            f"{config.get('coordination_parent_dir')}/{parent_id}.json",
            config,
            errors,
            template=False,
        )

    validate_dependencies(tasks, errors)
    validate_path_ownership(tasks, errors)
    if config.get("schema_version") == 2:
        validate_parent_uniqueness(parents, errors)
        validate_child_parents(tasks, parents, errors)
        validate_parent_history_links(tasks, parents, errors)
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
    print("- task and parent templates are structurally valid")
    print(f"- coordination tasks validated: {len(tasks)}")
    print("- dependency graph and active path ownership are conflict-free")
    print("- persistent parent/child, lease, human-gate, and integration invariants hold")
    if args.summary:
        print_summary(tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
