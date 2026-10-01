"""Fail-closed campus operations decision primitives for CS1.

The functions in this module produce operator-review recommendations for food,
shuttle, room/slot scheduling, and shared-capacity allocation. Inputs such as
scenario weights, shortage/waste weights, service floors, and priorities are
registered policy inputs; they are not learned economics or evidence of impact.
No function authorizes automatic physical actuation.
"""

from __future__ import annotations

from itertools import combinations
import math
from typing import Any, Mapping, Sequence

OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"


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
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _normalize_scenarios(
    demand_scenarios: Sequence[Mapping[str, Any]],
) -> list[tuple[float, float]] | None:
    rows: list[tuple[float, float]] = []
    for row in demand_scenarios:
        if not isinstance(row, Mapping):
            return None
        demand = _number(row.get("demand"), minimum=0.0)
        weight = _number(row.get("weight"), minimum=0.0)
        if demand is None or weight is None:
            return None
        rows.append((demand, weight))
    total_weight = sum(weight for _, weight in rows)
    if not rows or total_weight <= 0:
        return None
    return [(demand, weight / total_weight) for demand, weight in rows]


def _base_result(scope: str) -> dict[str, Any]:
    return {
        "scope": scope,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "impact_claim_allowed": False,
    }


def optimize_food_production(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    max_capacity: Any,
    waste_weight: Any,
    shortage_weight: Any,
    method_eligibility: str = "SANDBOX_ONLY",
) -> dict[str, Any]:
    """Choose an integer production target under registered asymmetric loss."""

    result = _base_result("FOOD_PRODUCTION_RECOMMENDATION")
    scenarios = _normalize_scenarios(demand_scenarios)
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
    if max_units < 0:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "recommended_production": None,
            "reason_codes": ["INVALID_MAX_CAPACITY"],
        }

    def loss(quantity: int) -> float:
        return sum(
            weight
            * (
                waste * max(quantity - demand, 0.0)
                + shortage * max(demand - quantity, 0.0)
            )
            for demand, weight in scenarios
        )

    scored = [(loss(quantity), quantity) for quantity in range(max_units + 1)]
    objective, quantity = min(scored, key=lambda item: (item[0], item[1]))
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
        "expected_registered_loss": objective,
        "max_capacity": max_units,
        "scenario_count": len(scenarios),
        "reason_codes": reasons,
    }


def optimize_shuttle_plan(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    departure_options: Sequence[Mapping[str, Any]],
    empty_seat_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any,
) -> dict[str, Any]:
    """Choose a departure-capacity bundle under a registered service floor."""

    result = _base_result("SHUTTLE_CAPACITY_RECOMMENDATION")
    scenarios = _normalize_scenarios(demand_scenarios)
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

    options: list[tuple[str, float, float, int]] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(departure_options):
        if not isinstance(row, Mapping):
            options = []
            break
        departure_id = _text(row.get("departure_id"))
        capacity = _number(row.get("capacity"), minimum=0.0)
        activation = _number(row.get("activation_weight"), minimum=0.0)
        if (
            departure_id is None
            or departure_id in seen_ids
            or capacity is None
            or capacity <= 0
            or activation is None
        ):
            options = []
            break
        seen_ids.add(departure_id)
        options.append((departure_id, capacity, activation, index))

    if not options or len(options) > 18:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_EXCESSIVE_DEPARTURE_OPTIONS"],
        }

    full_capacity = sum(item[1] for item in options)
    if any(full_capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["FLEET_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR"],
        }

    candidates: list[tuple[float, float, int, tuple[int, ...]]] = []
    for size in range(1, len(options) + 1):
        for indexes in combinations(range(len(options)), size):
            capacity = sum(options[index][1] for index in indexes)
            if any(capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
                continue
            activation = sum(options[index][2] for index in indexes)
            expected_loss = activation + sum(
                weight
                * (
                    empty_weight * max(capacity - demand, 0.0)
                    + shortage * max(demand - capacity, 0.0)
                )
                for demand, weight in scenarios
            )
            candidates.append((expected_loss, capacity, size, indexes))

    if not candidates:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["NO_SHUTTLE_BUNDLE_MEETS_SERVICE_FLOOR"],
        }

    objective, capacity, _, indexes = min(
        candidates,
        key=lambda item: (item[0], item[1], item[2], item[3]),
    )
    selected = [options[index][0] for index in indexes]
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "selected_departure_ids": selected,
        "selected_capacity": int(capacity) if capacity.is_integer() else capacity,
        "expected_registered_loss": objective,
        "registered_min_point_service_ratio": service_ratio,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def optimize_class_schedule(
    *,
    classes: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Assign every class to an allowed room/slot without collisions."""

    result = _base_result("CLASS_ROOM_SLOT_RECOMMENDATION")
    normalized_rooms: list[dict[str, Any]] = []
    room_ids: set[str] = set()
    for room in rooms:
        if not isinstance(room, Mapping):
            normalized_rooms = []
            break
        room_id = _text(room.get("room_id"))
        capacity = _number(room.get("capacity"), minimum=0.0)
        raw_features = room.get("features", [])
        if (
            room_id is None
            or room_id in room_ids
            or capacity is None
            or not isinstance(raw_features, Sequence)
            or isinstance(raw_features, (str, bytes))
        ):
            normalized_rooms = []
            break
        room_ids.add(room_id)
        normalized_rooms.append(
            {
                "room_id": room_id,
                "capacity": capacity,
                "features": {str(item).strip() for item in raw_features if str(item).strip()},
                "building": _text(room.get("building")),
            }
        )

    normalized_classes: list[dict[str, Any]] = []
    class_ids: set[str] = set()
    for item in classes:
        if not isinstance(item, Mapping):
            normalized_classes = []
            break
        class_id = _text(item.get("class_id"))
        attendance = _number(item.get("planning_attendance"), minimum=0.0)
        slots = item.get("allowed_slots")
        features = item.get("required_features", [])
        if (
            class_id is None
            or class_id in class_ids
            or attendance is None
            or not isinstance(slots, Sequence)
            or isinstance(slots, (str, bytes))
            or not isinstance(features, Sequence)
            or isinstance(features, (str, bytes))
        ):
            normalized_classes = []
            break
        allowed_slots = [str(slot).strip() for slot in slots if str(slot).strip()]
        if not allowed_slots:
            normalized_classes = []
            break
        class_ids.add(class_id)
        normalized_classes.append(
            {
                "class_id": class_id,
                "planning_attendance": attendance,
                "allowed_slots": allowed_slots,
                "required_features": {str(feature).strip() for feature in features if str(feature).strip()},
            }
        )

    if not normalized_rooms or not normalized_classes:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["INVALID_CLASS_OR_ROOM_INPUTS"],
        }

    candidates_by_class: dict[str, list[tuple[float, str, str]]] = {}
    for item in normalized_classes:
        candidates: list[tuple[float, str, str]] = []
        for slot in item["allowed_slots"]:
            for room in normalized_rooms:
                if room["capacity"] + 1e-9 < item["planning_attendance"]:
                    continue
                if not item["required_features"].issubset(room["features"]):
                    continue
                waste = room["capacity"] - item["planning_attendance"]
                candidates.append((waste, slot, room["room_id"]))
        candidates.sort(key=lambda row: (row[0], row[1], row[2]))
        if not candidates:
            return {
                **result,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "reason_codes": ["CLASS_CONSTRAINTS_INFEASIBLE"],
            }
        candidates_by_class[item["class_id"]] = candidates

    ordered_classes = sorted(
        normalized_classes,
        key=lambda item: (len(candidates_by_class[item["class_id"]]), item["class_id"]),
    )
    used: set[tuple[str, str]] = set()
    current: list[dict[str, Any]] = []
    best: tuple[float, list[dict[str, Any]]] | None = None

    def search(position: int, cost: float) -> None:
        nonlocal best
        if best is not None and cost >= best[0] - 1e-12:
            return
        if position == len(ordered_classes):
            best = (cost, [dict(row) for row in current])
            return
        item = ordered_classes[position]
        for waste, slot, room_id in candidates_by_class[item["class_id"]]:
            key = (slot, room_id)
            if key in used:
                continue
            used.add(key)
            current.append(
                {
                    "class_id": item["class_id"],
                    "slot": slot,
                    "room_id": room_id,
                    "planning_attendance": item["planning_attendance"],
                }
            )
            search(position + 1, cost + waste)
            current.pop()
            used.remove(key)

    search(0, 0.0)
    if best is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "reason_codes": ["CLASS_CONSTRAINTS_INFEASIBLE"],
        }

    assignments = sorted(best[1], key=lambda row: row["class_id"])
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "assignments": assignments,
        "total_unused_seats": best[0],
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def allocate_shared_capacity(
    *,
    total_capacity: Any,
    requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Allocate discrete shared capacity after satisfying registered minimums."""

    result = _base_result("SHARED_CAPACITY_ALLOCATION")
    capacity_number = _number(total_capacity, minimum=0.0)
    if capacity_number is None or not capacity_number.is_integer():
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["INVALID_SHARED_CAPACITY"],
        }
    capacity = int(capacity_number)

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in requests:
        if not isinstance(row, Mapping):
            normalized = []
            break
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
            normalized = []
            break
        seen.add(request_id)
        normalized.append(
            {
                "request_id": request_id,
                "minimum": int(minimum),
                "desired": int(desired),
                "priority_weight": priority,
            }
        )

    if not normalized:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["INVALID_SHARED_CAPACITY_REQUESTS"],
        }

    minimum_total = sum(row["minimum"] for row in normalized)
    if minimum_total > capacity:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["REQUEST_MINIMUMS_EXCEED_SHARED_CAPACITY"],
        }

    allocated = {row["request_id"]: row["minimum"] for row in normalized}
    remaining = capacity - minimum_total
    while remaining > 0:
        eligible = [
            row
            for row in normalized
            if allocated[row["request_id"]] < row["desired"]
        ]
        if not eligible:
            break
        choice = min(
            eligible,
            key=lambda row: (-row["priority_weight"], row["request_id"]),
        )
        allocated[choice["request_id"]] += 1
        remaining -= 1

    allocations = [
        {
            "request_id": row["request_id"],
            "allocated": allocated[row["request_id"]],
            "minimum": row["minimum"],
            "desired": row["desired"],
        }
        for row in normalized
    ]
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        "allocations": allocations,
        "unallocated_capacity": remaining,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def build_campus_ops_bundle(decisions: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate subsystem readiness without allowing a weaker gate to disappear."""

    severity = {
        "PILOT_READY": 0,
        "REVIEW_REQUIRED": 1,
        "WITHHOLD": 2,
    }
    statuses = [
        str(value.get("decision_readiness") or "WITHHOLD").upper()
        for value in decisions.values()
        if isinstance(value, Mapping)
    ]
    if not statuses:
        readiness = "WITHHOLD"
    elif any(status not in severity for status in statuses):
        readiness = "WITHHOLD"
    else:
        readiness = max(statuses, key=lambda status: severity[status])
    return {
        "scope": "CAMPUS_OPS_BUNDLE",
        "decision_readiness": readiness,
        "subsystem_readiness": {
            name: str(value.get("decision_readiness") or "WITHHOLD").upper()
            for name, value in decisions.items()
            if isinstance(value, Mapping)
        },
        "operator_approval_required": True,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }
