"""Fail-closed campus operations decision primitives for CS1.

These functions create advisory recommendations only. Scenario weights, penalty
weights, service floors and priorities are registered policy inputs, not observed
economics. No function authorizes automatic physical actuation.
"""

from __future__ import annotations

from itertools import combinations
import math
from typing import Any, Mapping, Sequence

POLICY_VERSION = "campus-ops-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"
READINESS_ORDER = {"PILOT_READY": 0, "REVIEW_REQUIRED": 1, "WITHHOLD": 2}


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
    normalized = str(value or "").strip()
    return normalized or None


def _scenarios(
    rows: Sequence[Mapping[str, Any]] | None,
) -> list[tuple[float, float]] | None:
    normalized: list[tuple[float, float]] = []
    for row in rows or ():
        if not isinstance(row, Mapping):
            return None
        demand = _number(row.get("demand"), minimum=0.0)
        weight = _number(row.get("weight"), minimum=0.0)
        if demand is None or weight is None:
            return None
        normalized.append((demand, weight))
    total = sum(weight for _, weight in normalized)
    if not normalized or total <= 0:
        return None
    return [(demand, weight / total) for demand, weight in normalized]


def _base(scope: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": scope,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }


def optimize_food_production(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    max_capacity: Any,
    waste_weight: Any,
    shortage_weight: Any,
    method_eligibility: str = "EVALUATED_OFFLINE",
) -> dict[str, Any]:
    result = _base("FOOD_PRODUCTION_RECOMMENDATION")
    scenarios = _scenarios(demand_scenarios)
    capacity = _number(max_capacity, minimum=0.0)
    waste = _number(waste_weight, minimum=0.0)
    shortage = _number(shortage_weight, minimum=0.0)
    if scenarios is None or capacity is None or waste is None or shortage is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "recommended_production": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_FOOD_POLICY_INPUTS"],
        }

    max_units = int(math.floor(capacity))

    def loss(quantity: int) -> float:
        return sum(
            probability
            * (
                waste * max(quantity - demand, 0.0)
                + shortage * max(demand - quantity, 0.0)
            )
            for demand, probability in scenarios
        )

    objective, quantity = min(
        ((loss(q), q) for q in range(max_units + 1)),
        key=lambda pair: (pair[0], pair[1]),
    )
    eligibility = str(method_eligibility or "SANDBOX_ONLY").strip().upper()
    if eligibility in {"SANDBOX_ONLY", "RETIRED"}:
        readiness = "WITHHOLD"
        recommendation = None
        reasons = ["METHOD_NOT_ACTIONABLE_FOR_OPERATOR_RECOMMENDATION"]
    else:
        readiness = "REVIEW_REQUIRED"
        recommendation = quantity
        reasons = ["OPERATOR_REVIEW_REQUIRED"]

    return {
        **result,
        "decision_readiness": readiness,
        "recommended_production": recommendation,
        "max_capacity": max_units,
        "expected_registered_loss": objective,
        "scenario_count": len(scenarios),
        "reason_codes": reasons,
    }


def optimize_shuttle_plan(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    departure_options: Sequence[Mapping[str, Any]],
    empty_seat_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any = 0.9,
) -> dict[str, Any]:
    result = _base("SHUTTLE_CAPACITY_RECOMMENDATION")
    scenarios = _scenarios(demand_scenarios)
    empty_weight = _number(empty_seat_weight, minimum=0.0)
    shortage = _number(shortage_weight, minimum=0.0)
    service_ratio = _number(min_point_service_ratio, minimum=0.0)
    if (
        scenarios is None
        or empty_weight is None
        or shortage is None
        or service_ratio is None
        or service_ratio > 1.0
    ):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_SHUTTLE_POLICY_INPUTS"],
        }

    options: list[tuple[str, float, float]] = []
    seen: set[str] = set()
    for row in departure_options or ():
        if not isinstance(row, Mapping):
            options = []
            break
        departure_id = _text(row.get("departure_id"))
        capacity = _number(row.get("capacity"), minimum=0.0)
        activation = _number(row.get("activation_weight", 0.0), minimum=0.0)
        if (
            departure_id is None
            or departure_id in seen
            or capacity is None
            or capacity <= 0
            or activation is None
        ):
            options = []
            break
        seen.add(departure_id)
        options.append((departure_id, capacity, activation))

    if not options or len(options) > 18:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_EXCESSIVE_DEPARTURE_OPTIONS"],
        }

    full_capacity = sum(capacity for _, capacity, _ in options)
    if any(full_capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": int(round(full_capacity)),
            "reason_codes": ["FLEET_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR"],
        }

    candidates: list[tuple[float, float, tuple[str, ...]]] = []
    for size in range(1, len(options) + 1):
        for subset in combinations(options, size):
            ids = tuple(sorted(item[0] for item in subset))
            capacity = sum(item[1] for item in subset)
            if any(capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
                continue
            activation = sum(item[2] for item in subset)
            expected_loss = activation + sum(
                probability
                * (
                    empty_weight * max(capacity - demand, 0.0)
                    + shortage * max(demand - capacity, 0.0)
                )
                for demand, probability in scenarios
            )
            candidates.append((expected_loss, capacity, ids))

    if not candidates:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["NO_SHUTTLE_BUNDLE_MEETS_SERVICE_FLOOR"],
        }

    objective, capacity, ids = min(candidates, key=lambda item: (item[0], item[1], item[2]))
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "selected_departure_ids": list(ids),
        "selected_capacity": int(round(capacity)),
        "expected_registered_loss": objective,
        "registered_min_point_service_ratio": service_ratio,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def optimize_class_schedule(
    *,
    classes: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
    building_mismatch_weight: Any = 0.0,
) -> dict[str, Any]:
    result = _base("CLASS_ROOM_SLOT_RECOMMENDATION")
    mismatch = _number(building_mismatch_weight, minimum=0.0)
    if mismatch is None or not classes or not rooms:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
        }

    normalized_rooms: list[dict[str, Any]] = []
    room_ids: set[str] = set()
    for room in rooms:
        room_id = _text(room.get("room_id")) if isinstance(room, Mapping) else None
        capacity = _number(room.get("capacity"), minimum=0.0) if isinstance(room, Mapping) else None
        features = room.get("features", []) if isinstance(room, Mapping) else []
        if (
            room_id is None
            or room_id in room_ids
            or capacity is None
            or not isinstance(features, Sequence)
            or isinstance(features, (str, bytes))
        ):
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
            }
        room_ids.add(room_id)
        normalized_rooms.append(
            {
                "room_id": room_id,
                "capacity": capacity,
                "features": {str(feature).strip() for feature in features if str(feature).strip()},
                "building": _text(room.get("building")),
            }
        )

    candidates_by_class: dict[str, list[tuple[float, str, str]]] = {}
    seen_classes: set[str] = set()
    for item in classes:
        if not isinstance(item, Mapping):
            return {**result, "decision_readiness": "WITHHOLD", "assignments": [], "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"]}
        class_id = _text(item.get("class_id"))
        attendance = _number(item.get("planning_attendance"), minimum=0.0)
        slots = item.get("allowed_slots", [])
        features = item.get("required_features", [])
        preferred_building = _text(item.get("preferred_building"))
        if (
            class_id is None
            or class_id in seen_classes
            or attendance is None
            or not isinstance(slots, Sequence)
            or isinstance(slots, (str, bytes))
            or not isinstance(features, Sequence)
            or isinstance(features, (str, bytes))
        ):
            return {**result, "decision_readiness": "WITHHOLD", "assignments": [], "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"]}
        seen_classes.add(class_id)
        allowed_slots = [str(slot).strip() for slot in slots if str(slot).strip()]
        required = {str(feature).strip() for feature in features if str(feature).strip()}
        candidates: list[tuple[float, str, str]] = []
        for slot in allowed_slots:
            for room in normalized_rooms:
                if room["capacity"] + 1e-9 < attendance or not required.issubset(room["features"]):
                    continue
                score = room["capacity"] - attendance
                if preferred_building and room["building"] != preferred_building:
                    score += mismatch
                candidates.append((score, slot, room["room_id"]))
        candidates.sort()
        if not candidates:
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["CLASS_CONSTRAINTS_INFEASIBLE"],
            }
        candidates_by_class[class_id] = candidates

    order = sorted(candidates_by_class, key=lambda cid: (len(candidates_by_class[cid]), cid))
    used: set[tuple[str, str]] = set()
    current: list[dict[str, Any]] = []
    best: tuple[float, list[dict[str, Any]]] | None = None

    def search(position: int, score: float) -> None:
        nonlocal best
        if best is not None and score >= best[0] - 1e-12:
            return
        if position == len(order):
            best = (score, [dict(row) for row in current])
            return
        class_id = order[position]
        for candidate_score, slot, room_id in candidates_by_class[class_id]:
            key = (slot, room_id)
            if key in used:
                continue
            used.add(key)
            current.append({"class_id": class_id, "slot": slot, "room_id": room_id, "assignment_loss": candidate_score})
            search(position + 1, score + candidate_score)
            current.pop()
            used.remove(key)

    search(0, 0.0)
    if best is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["NO_COLLISION_FREE_CLASS_SCHEDULE"],
        }
    assignments = sorted(best[1], key=lambda row: row["class_id"])
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "assignments": assignments,
        "total_registered_loss": best[0],
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def allocate_shared_capacity(
    *,
    total_capacity: Any,
    requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    result = _base("SHARED_CAPACITY_ALLOCATION")
    capacity_number = _number(total_capacity, minimum=0.0)
    if capacity_number is None or not capacity_number.is_integer():
        return {**result, "decision_readiness": "WITHHOLD", "allocations": [], "reason_codes": ["INVALID_SHARED_CAPACITY"]}
    capacity = int(capacity_number)
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in requests or ():
        if not isinstance(row, Mapping):
            return {**result, "decision_readiness": "WITHHOLD", "allocations": [], "reason_codes": ["INVALID_SHARED_CAPACITY_REQUEST"]}
        request_id = _text(row.get("request_id"))
        minimum = _number(row.get("minimum"), minimum=0.0)
        desired = _number(row.get("desired"), minimum=0.0)
        priority = _number(row.get("priority_weight"), minimum=0.0)
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
            return {**result, "decision_readiness": "WITHHOLD", "allocations": [], "reason_codes": ["INVALID_SHARED_CAPACITY_REQUEST"]}
        seen.add(request_id)
        normalized.append({"request_id": request_id, "minimum": int(minimum), "desired": int(desired), "priority_weight": priority, "allocated": int(minimum)})

    if not normalized:
        return {**result, "decision_readiness": "WITHHOLD", "allocations": [], "reason_codes": ["NO_SHARED_CAPACITY_REQUESTS"]}
    minimum_total = sum(row["minimum"] for row in normalized)
    if minimum_total > capacity:
        return {**result, "decision_readiness": "WITHHOLD", "allocations": [], "reason_codes": ["REGISTERED_MINIMUMS_EXCEED_AVAILABLE_CAPACITY"]}

    remaining = capacity - minimum_total
    while remaining > 0:
        eligible = [row for row in normalized if row["allocated"] < row["desired"]]
        if not eligible:
            break
        eligible.sort(key=lambda row: (-row["priority_weight"], -(row["desired"] - row["allocated"]), row["request_id"]))
        eligible[0]["allocated"] += 1
        remaining -= 1

    allocations = [
        {key: row[key] for key in ("request_id", "allocated", "minimum", "desired", "priority_weight")}
        for row in sorted(normalized, key=lambda item: item["request_id"])
    ]
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "allocations": allocations,
        "unallocated_capacity": remaining,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def build_campus_ops_bundle(modules: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    result = _base("CAMPUS_OPERATIONS_BUNDLE")
    if not modules:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "module_states": {},
            "reason_codes": ["NO_CAMPUS_OPS_MODULES"],
        }

    module_states: dict[str, str] = {}
    reasons: list[str] = []
    for module_id, module_result in modules.items():
        state = str(module_result.get("decision_readiness") or "WITHHOLD").upper()
        if state not in READINESS_ORDER:
            state = "WITHHOLD"
            reasons.append(f"UNKNOWN_READINESS_{module_id}")
        module_states[str(module_id)] = state
    readiness = max(module_states.values(), key=lambda state: READINESS_ORDER[state])
    return {
        **result,
        "decision_readiness": readiness,
        "module_states": module_states,
        "reason_codes": reasons,
    }
