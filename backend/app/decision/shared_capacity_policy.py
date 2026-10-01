from __future__ import annotations

import importlib.util
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def _load_contract():
    try:
        from app.decision import campus_contract as contract  # type: ignore

        return contract
    except ModuleNotFoundError:
        path = Path(__file__).with_name("campus_contract.py")
        spec = importlib.util.spec_from_file_location("campus_contract_fallback", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load campus contract from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


CONTRACT = _load_contract()
CONTRACT_VERSION = CONTRACT.CONTRACT_VERSION
CAPACITY_SEMANTICS = "VERIFIED_AGGREGATE_RESOURCE_INVENTORY"

LIMITATIONS = (
    "REGISTERED_PRIORITY_WEIGHTS_NOT_OBSERVED_ECONOMICS",
    "NO_UNVERIFIED_SHARED_CAPACITY_CLAIM",
    "AGGREGATE_RESOURCE_ALLOCATION_ONLY",
    "NO_PERSON_LEVEL_ALLOCATION",
    "NO_AUTOMATIC_RESOURCE_ACTUATION",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _finite_nonnegative(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _withhold(reason: str, *, capacity_provenance: str) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "capacity_provenance": capacity_provenance,
        "capacity_semantics": CAPACITY_SEMANTICS,
        "allocations": [],
        "unallocated_capacity": None,
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def allocate_shared_capacity(
    *,
    total_capacity: Any,
    requests: Sequence[Mapping[str, Any]],
    capacity_provenance: str = "UNAVAILABLE",
) -> dict[str, Any]:
    """Allocate verified aggregate resource capacity using minimums then priorities."""

    CONTRACT.validate_no_person_level_data(requests, path="requests")
    normalized_capacity_provenance = CONTRACT.normalize_provenance(
        capacity_provenance, field="capacity_provenance"
    )
    capacity_number = _finite_nonnegative(total_capacity)
    if capacity_number is None or not capacity_number.is_integer():
        return _withhold(
            "INVALID_SHARED_CAPACITY",
            capacity_provenance=normalized_capacity_provenance,
        )
    if normalized_capacity_provenance not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        return _withhold(
            "UNVERIFIED_SHARED_CAPACITY",
            capacity_provenance=normalized_capacity_provenance,
        )
    capacity = int(capacity_number)

    if not isinstance(requests, Sequence) or isinstance(requests, (str, bytes, bytearray)) or not requests:
        return _withhold(
            "NO_SHARED_CAPACITY_REQUESTS",
            capacity_provenance=normalized_capacity_provenance,
        )

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in requests:
        if not isinstance(raw, Mapping):
            return _withhold(
                "INVALID_SHARED_CAPACITY_REQUEST",
                capacity_provenance=normalized_capacity_provenance,
            )
        request_id = str(raw.get("request_id", "")).strip()
        minimum = _finite_nonnegative(raw.get("minimum"))
        desired = _finite_nonnegative(raw.get("desired"))
        priority = _finite_nonnegative(raw.get("priority_weight"))
        if (
            not request_id
            or request_id in seen
            or minimum is None
            or desired is None
            or priority is None
            or not minimum.is_integer()
            or not desired.is_integer()
            or desired < minimum
        ):
            return _withhold(
                "INVALID_SHARED_CAPACITY_REQUEST",
                capacity_provenance=normalized_capacity_provenance,
            )
        seen.add(request_id)
        normalized.append(
            {
                "request_id": request_id,
                "minimum": int(minimum),
                "desired": int(desired),
                "priority_weight": priority,
            }
        )

    minimum_total = sum(row["minimum"] for row in normalized)
    if minimum_total > capacity:
        return _withhold(
            "REQUEST_MINIMUMS_EXCEED_SHARED_CAPACITY",
            capacity_provenance=normalized_capacity_provenance,
        )

    allocation = {row["request_id"]: row["minimum"] for row in normalized}
    remaining = capacity - minimum_total
    while remaining > 0:
        eligible = [
            row
            for row in normalized
            if allocation[row["request_id"]] < row["desired"]
        ]
        if not eligible:
            break
        selected = min(
            eligible,
            key=lambda row: (-row["priority_weight"], row["request_id"]),
        )
        allocation[selected["request_id"]] += 1
        remaining -= 1

    rows = [
        {
            "request_id": row["request_id"],
            "minimum": row["minimum"],
            "desired": row["desired"],
            "allocated": allocation[row["request_id"]],
            "priority_weight": row["priority_weight"],
        }
        for row in normalized
    ]
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "capacity_provenance": normalized_capacity_provenance,
        "capacity_semantics": CAPACITY_SEMANTICS,
        "allocations": rows,
        "unallocated_capacity": remaining,
        "reason_codes": ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
