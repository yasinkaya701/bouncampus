"""Scalable shared-capacity allocation for CS1 campus operations."""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Mapping, Sequence

POLICY_VERSION = "shared-capacity-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_PRIORITY_UNITS"


def _number(value: Any, *, minimum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    if minimum is not None and numeric < minimum:
        return None
    return numeric


def _text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def _withhold(reason: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": "SHARED_CAPACITY_ALLOCATION",
        "objective_units": OBJECTIVE_UNITS,
        "decision_readiness": "WITHHOLD",
        "allocations": [],
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
        "reason_codes": [reason],
    }


def _allocate_equal_priority(rows: list[dict[str, Any]], units: int) -> int:
    """Match largest-unmet-gap + request-id tie-break without unit loops."""
    pending = sorted(
        rows,
        key=lambda row: (
            -(row["desired"] - row["allocated"]),
            row["request_id"],
        ),
    )
    active: list[dict[str, Any]] = []
    index = 0
    current_gap = (
        pending[0]["desired"] - pending[0]["allocated"] if pending else 0
    )

    while units > 0 and current_gap > 0:
        while index < len(pending):
            gap = pending[index]["desired"] - pending[index]["allocated"]
            if gap != current_gap:
                break
            active.append(pending[index])
            index += 1

        next_gap = (
            pending[index]["desired"] - pending[index]["allocated"]
            if index < len(pending)
            else 0
        )
        level_drop = current_gap - next_gap
        level_cost = level_drop * len(active)

        if units >= level_cost:
            for row in active:
                row["allocated"] += level_drop
            units -= level_cost
            current_gap = next_gap
            continue

        whole_rounds, remainder = divmod(units, len(active))
        for row in active:
            row["allocated"] += whole_rounds
        if remainder:
            for row in sorted(active, key=lambda row: row["request_id"])[:remainder]:
                row["allocated"] += 1
        units = 0

    return units


def allocate_shared_capacity(
    *,
    total_capacity: Any,
    requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Allocate by priority and unmet need in O(n log n), not O(capacity)."""
    capacity_number = _number(total_capacity, minimum=0.0)
    if capacity_number is None or not capacity_number.is_integer():
        return _withhold("INVALID_SHARED_CAPACITY")
    capacity = int(capacity_number)

    if not isinstance(requests, Sequence) or isinstance(requests, (str, bytes)):
        return _withhold("INVALID_SHARED_CAPACITY_REQUEST")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in requests:
        if not isinstance(raw, Mapping):
            return _withhold("INVALID_SHARED_CAPACITY_REQUEST")
        request_id = _text(raw.get("request_id"))
        minimum = _number(raw.get("minimum"), minimum=0.0)
        desired = _number(raw.get("desired"), minimum=0.0)
        priority = _number(raw.get("priority_weight"), minimum=0.0)
        if (
            request_id is None
            or request_id in seen
            or minimum is None
            or desired is None
            or priority is None
            or not minimum.is_integer()
            or not desired.is_integer()
            or desired < minimum
        ):
            return _withhold("INVALID_SHARED_CAPACITY_REQUEST")
        seen.add(request_id)
        normalized.append(
            {
                "request_id": request_id,
                "minimum": int(minimum),
                "desired": int(desired),
                "priority_weight": priority,
                "allocated": int(minimum),
            }
        )

    if not normalized:
        return _withhold("NO_SHARED_CAPACITY_REQUESTS")

    minimum_total = sum(row["minimum"] for row in normalized)
    if minimum_total > capacity:
        return _withhold("REGISTERED_MINIMUMS_EXCEED_AVAILABLE_CAPACITY")

    remaining = capacity - minimum_total
    by_priority: dict[float, list[dict[str, Any]]] = defaultdict(list)
    for row in normalized:
        by_priority[row["priority_weight"]].append(row)

    for priority in sorted(by_priority, reverse=True):
        group = by_priority[priority]
        group_gap = sum(row["desired"] - row["allocated"] for row in group)
        if group_gap <= 0:
            continue
        spend = min(remaining, group_gap)
        leftover = _allocate_equal_priority(group, spend)
        remaining -= spend - leftover
        if remaining <= 0:
            break

    allocations = [
        {
            key: row[key]
            for key in (
                "request_id",
                "allocated",
                "minimum",
                "desired",
                "priority_weight",
            )
        }
        for row in sorted(normalized, key=lambda row: row["request_id"])
    ]
    return {
        "policy_version": POLICY_VERSION,
        "scope": "SHARED_CAPACITY_ALLOCATION",
        "objective_units": OBJECTIVE_UNITS,
        "decision_readiness": "REVIEW_REQUIRED",
        "allocations": allocations,
        "unallocated_capacity": remaining,
        "allocation_semantics": "PRIORITY_FIRST_LARGEST_UNMET_GAP_BATCHED",
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }
