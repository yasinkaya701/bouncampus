from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

from app.decision.campus_operations import (
    DECISION_POLICY_VERSION,
    READINESS_PILOT,
    READINESS_REVIEW,
    READINESS_WITHHOLD,
    TRUTH_BOUNDARY,
)


def _number(value: Any, *, minimum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    if minimum is not None and number < minimum:
        return None
    return number


def _positive_int(value: Any) -> int | None:
    number = _number(value, minimum=0)
    if number is None:
        return None
    rounded = int(round(number))
    return rounded if rounded > 0 else None


def plan_space_service(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Choose a capacity-safe subset of flexible campus spaces to keep active.

    The policy is intentionally transparent: mandatory spaces are activated first,
    then optional spaces are ranked by relative energy cost per seat. It is a
    deterministic planning baseline, not a claim of globally optimal building
    operation or realized energy/carbon savings.
    """

    predicted_demand = _positive_int(payload.get("predicted_demand"))
    reserve_ratio = _number(payload.get("reserve_ratio"), minimum=0)
    reserve_ratio = 0.15 if reserve_ratio is None else min(reserve_ratio, 0.50)

    raw_spaces = payload.get("spaces")
    if (
        predicted_demand is None
        or not isinstance(raw_spaces, Sequence)
        or isinstance(raw_spaces, (str, bytes))
        or not raw_spaces
    ):
        return {
            "policy_version": DECISION_POLICY_VERSION,
            "domain": "SPACE",
            "readiness": READINESS_WITHHOLD,
            "predicted_demand": predicted_demand,
            "required_capacity": None,
            "active_capacity": 0,
            "capacity_shortfall": None,
            "active_space_ids": [],
            "standby_space_ids": [],
            "reason_codes": ["POSITIVE_DEMAND_AND_SPACE_INVENTORY_REQUIRED"],
            "operator_approval_required": True,
            "automatic_building_control": False,
            "truth_boundary": TRUTH_BOUNDARY,
        }

    valid_spaces: list[dict[str, Any]] = []
    invalid_rows = 0
    for index, item in enumerate(raw_spaces):
        if not isinstance(item, Mapping):
            invalid_rows += 1
            continue
        space_id = str(item.get("space_id") or "").strip()
        capacity = _positive_int(item.get("capacity"))
        energy_cost = _number(item.get("relative_energy_cost"), minimum=0)
        available = bool(item.get("available", True))
        must_open = bool(item.get("must_open", False))
        if not space_id or capacity is None or energy_cost is None:
            invalid_rows += 1
            continue
        valid_spaces.append(
            {
                "space_id": space_id,
                "capacity": capacity,
                "relative_energy_cost": energy_cost,
                "available": available,
                "must_open": must_open,
                "source_index": index,
            }
        )

    available_spaces = [space for space in valid_spaces if space["available"]]
    required_capacity = int(math.ceil(predicted_demand * (1.0 + reserve_ratio)))

    mandatory = [space for space in available_spaces if space["must_open"]]
    optional = [space for space in available_spaces if not space["must_open"]]
    optional.sort(
        key=lambda space: (
            space["relative_energy_cost"] / space["capacity"],
            space["relative_energy_cost"],
            -space["capacity"],
            space["space_id"],
        )
    )

    active = list(mandatory)
    active_capacity = sum(space["capacity"] for space in active)
    for space in optional:
        if active_capacity >= required_capacity:
            break
        active.append(space)
        active_capacity += space["capacity"]

    active_ids = [space["space_id"] for space in active]
    active_id_set = set(active_ids)
    standby_ids = [
        space["space_id"]
        for space in available_spaces
        if space["space_id"] not in active_id_set
    ]
    capacity_shortfall = max(0, required_capacity - active_capacity)
    active_relative_cost = sum(space["relative_energy_cost"] for space in active)
    all_open_relative_cost = sum(space["relative_energy_cost"] for space in available_spaces)
    relative_cost_avoided = max(0.0, all_open_relative_cost - active_relative_cost)

    reason_codes: list[str] = []
    if capacity_shortfall > 0:
        readiness = READINESS_WITHHOLD
        reason_codes.append("INSUFFICIENT_AVAILABLE_CAPACITY")
    elif invalid_rows:
        readiness = READINESS_REVIEW
        reason_codes.append("PARTIAL_INVALID_SPACE_INPUTS")
    else:
        readiness = READINESS_PILOT
        reason_codes.append("CAPACITY_SAFE_CONSOLIDATION_PLAN_AVAILABLE")

    unavailable_mandatory = [
        space["space_id"]
        for space in valid_spaces
        if space["must_open"] and not space["available"]
    ]
    if unavailable_mandatory:
        readiness = READINESS_WITHHOLD
        reason_codes.insert(0, "MANDATORY_SPACE_UNAVAILABLE")

    return {
        "policy_version": DECISION_POLICY_VERSION,
        "domain": "SPACE",
        "readiness": readiness,
        "predicted_demand": predicted_demand,
        "reserve_ratio": reserve_ratio,
        "required_capacity": required_capacity,
        "active_capacity": active_capacity,
        "capacity_headroom": max(0, active_capacity - required_capacity),
        "capacity_shortfall": capacity_shortfall,
        "active_space_ids": active_ids,
        "standby_space_ids": standby_ids,
        "invalid_space_rows": invalid_rows,
        "active_relative_energy_cost": round(active_relative_cost, 4),
        "all_open_relative_energy_cost": round(all_open_relative_cost, 4),
        "relative_energy_cost_avoided_vs_all_open": round(relative_cost_avoided, 4),
        "energy_metric_semantics": "RELATIVE_PLANNING_SCORE_NOT_MEASURED_KWH_OR_SAVINGS",
        "reason_codes": reason_codes,
        "provenance": "CAPACITY_SAFE_RELATIVE_ENERGY_HEURISTIC",
        "operator_approval_required": True,
        "automatic_building_control": False,
        "truth_boundary": TRUTH_BOUNDARY,
    }
