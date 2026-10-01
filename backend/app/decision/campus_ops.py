from __future__ import annotations

import itertools
import math
from typing import Any, Mapping, Sequence

POLICY_VERSION = "campus-ops-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
EVIDENCE_BOUNDARY = "ADVISORY_DECISION_SUPPORT_NOT_LIVE_AUTOMATION"
LIMITATIONS = (
    "NO_LIVE_CAFETERIA_POS_REQUIRED",
    "NO_LIVE_SHUTTLE_GPS_REQUIRED",
    "NO_LIVE_ROOM_OCCUPANCY_REQUIRED",
    "NO_AUTOMATIC_OPERATIONAL_ACTUATION",
    "RELATIVE_WEIGHTS_ARE_NOT_OBSERVED_ECONOMICS",
)

READINESS_ORDER = {
    "PILOT_READY": 0,
    "REVIEW_REQUIRED": 1,
    "WITHHOLD": 2,
}


def _finite_nonnegative(value: Any) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _finite_positive(value: Any) -> float | None:
    numeric = _finite_nonnegative(value)
    if numeric is None or numeric <= 0:
        return None
    return numeric


def _normalize_scenarios(
    demand_scenarios: Sequence[Mapping[str, Any]] | None,
) -> tuple[list[tuple[float, float]], list[str]]:
    rows: list[tuple[float, float]] = []
    reasons: list[str] = []
    for row in demand_scenarios or ():
        demand = _finite_nonnegative(row.get("demand"))
        weight = _finite_positive(row.get("weight"))
        if demand is None or weight is None:
            reasons.append("INVALID_DEMAND_SCENARIO_EXCLUDED")
            continue
        rows.append((demand, weight))

    if not rows:
        return [], reasons + ["NO_VALID_DEMAND_SCENARIOS"]

    weight_total = sum(weight for _, weight in rows)
    if weight_total <= 0:
        return [], reasons + ["NO_POSITIVE_SCENARIO_WEIGHT"]

    normalized = [(demand, weight / weight_total) for demand, weight in rows]
    normalized.sort(key=lambda item: item[0])
    return normalized, reasons


def _weighted_quantile(
    scenarios: Sequence[tuple[float, float]],
    quantile: float,
) -> float:
    running = 0.0
    for demand, weight in scenarios:
        running += weight
        if running + 1e-12 >= quantile:
            return demand
    return scenarios[-1][0]


def _weighted_median_demand(scenarios: Sequence[tuple[float, float]]) -> float:
    return _weighted_quantile(scenarios, 0.5)


def _expected_capacity_loss(
    capacity: float,
    scenarios: Sequence[tuple[float, float]],
    *,
    surplus_weight: float,
    shortage_weight: float,
) -> float:
    total = 0.0
    for demand, probability in scenarios:
        surplus = max(capacity - demand, 0.0)
        shortage = max(demand - capacity, 0.0)
        total += probability * (
            surplus_weight * surplus + shortage_weight * shortage
        )
    return total


def optimize_food_production(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    max_capacity: Any,
    waste_weight: Any,
    shortage_weight: Any,
    method_eligibility: str = "EVALUATED_OFFLINE",
) -> dict[str, Any]:
    """Choose an advisory production target from registered demand scenarios.

    The optimizer uses asymmetric-loss critical-fractile logic, but all scenario
    weights and penalty weights are caller-supplied sensitivity inputs. It never
    interprets those weights as observed currency, waste cost, or service value.
    """

    scenarios, reasons = _normalize_scenarios(demand_scenarios)
    capacity = _finite_nonnegative(max_capacity)
    waste = _finite_positive(waste_weight)
    shortage = _finite_positive(shortage_weight)
    eligibility = str(method_eligibility or "SANDBOX_ONLY").upper()

    if not scenarios or capacity is None or waste is None or shortage is None:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "recommended_production": None,
            "objective_units": OBJECTIVE_UNITS,
            "automatic_dispatch": False,
            "operator_approval_required": True,
            "reason_codes": reasons + ["INVALID_FOOD_OPTIMIZATION_PARAMETERS"],
            "limitations": list(LIMITATIONS),
        }

    critical_fractile = shortage / (shortage + waste)
    unconstrained = _weighted_quantile(scenarios, critical_fractile)
    recommendation = min(unconstrained, capacity)
    expected_loss = _expected_capacity_loss(
        recommendation,
        scenarios,
        surplus_weight=waste,
        shortage_weight=shortage,
    )

    upper = scenarios[-1][0]
    if capacity < min(unconstrained, upper):
        reasons.append("PRODUCTION_CAPACITY_BINDING")

    if eligibility in {"SANDBOX_ONLY", "RETIRED"}:
        readiness = "WITHHOLD"
        reasons.insert(0, f"METHOD_{eligibility}")
        recommended: int | None = None
    elif eligibility == "PILOT_ELIGIBLE":
        readiness = "REVIEW_REQUIRED"
        reasons.insert(0, "REGISTERED_POLICY_INPUTS_REQUIRE_OPERATOR_REVIEW")
        recommended = int(round(recommendation))
    else:
        readiness = "REVIEW_REQUIRED"
        reasons.insert(0, "METHOD_NOT_YET_PILOT_ELIGIBLE")
        recommended = int(round(recommendation))

    return {
        "policy_version": POLICY_VERSION,
        "decision_readiness": readiness,
        "recommended_production": recommended,
        "unconstrained_target": int(round(unconstrained)),
        "max_capacity": int(round(capacity)),
        "critical_fractile": critical_fractile,
        "expected_registered_loss": expected_loss,
        "objective_units": OBJECTIVE_UNITS,
        "scenario_count": len(scenarios),
        "automatic_dispatch": False,
        "operator_approval_required": True,
        "reason_codes": reasons,
        "limitations": list(LIMITATIONS),
    }


def optimize_shuttle_plan(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    departure_options: Sequence[Mapping[str, Any]],
    empty_seat_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any = 0.9,
) -> dict[str, Any]:
    """Select a shuttle departure bundle by enumerating registered options."""

    scenarios, reasons = _normalize_scenarios(demand_scenarios)
    empty_weight = _finite_positive(empty_seat_weight)
    shortage = _finite_positive(shortage_weight)
    service_ratio = _finite_nonnegative(min_point_service_ratio)

    options: list[tuple[str, float, float]] = []
    seen: set[str] = set()
    for raw in departure_options or ():
        departure_id = str(raw.get("departure_id") or "").strip()
        capacity = _finite_positive(raw.get("capacity"))
        activation = _finite_nonnegative(raw.get("activation_weight", 0.0))
        if (
            not departure_id
            or capacity is None
            or activation is None
            or departure_id in seen
        ):
            reasons.append("INVALID_SHUTTLE_OPTION_EXCLUDED")
            continue
        seen.add(departure_id)
        options.append((departure_id, capacity, activation))

    if (
        not scenarios
        or empty_weight is None
        or shortage is None
        or service_ratio is None
        or service_ratio > 1.0
        or not options
    ):
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": 0,
            "automatic_dispatch": False,
            "operator_approval_required": True,
            "objective_units": OBJECTIVE_UNITS,
            "reason_codes": reasons + ["INVALID_SHUTTLE_OPTIMIZATION_INPUTS"],
            "limitations": list(LIMITATIONS),
        }

    point_demand = _weighted_median_demand(scenarios)
    service_floor = point_demand * service_ratio
    fleet_capacity = sum(capacity for _, capacity, _ in options)
    if fleet_capacity + 1e-12 < service_floor:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": int(round(fleet_capacity)),
            "service_floor": service_floor,
            "automatic_dispatch": False,
            "operator_approval_required": True,
            "objective_units": OBJECTIVE_UNITS,
            "reason_codes": reasons
            + ["FLEET_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR"],
            "limitations": list(LIMITATIONS),
        }

    best: tuple[float, float, tuple[str, ...]] | None = None
    for count in range(1, len(options) + 1):
        for subset in itertools.combinations(options, count):
            ids = tuple(sorted(item[0] for item in subset))
            capacity = sum(item[1] for item in subset)
            if capacity + 1e-12 < service_floor:
                continue
            activation_loss = sum(item[2] for item in subset)
            loss = activation_loss + _expected_capacity_loss(
                capacity,
                scenarios,
                surplus_weight=empty_weight,
                shortage_weight=shortage,
            )
            candidate = (loss, capacity, ids)
            if best is None or candidate < best:
                best = candidate

    if best is None:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": 0,
            "automatic_dispatch": False,
            "operator_approval_required": True,
            "objective_units": OBJECTIVE_UNITS,
            "reason_codes": reasons + ["NO_FEASIBLE_SHUTTLE_BUNDLE"],
            "limitations": list(LIMITATIONS),
        }

    loss, capacity, ids = best
    return {
        "policy_version": POLICY_VERSION,
        "decision_readiness": "REVIEW_REQUIRED",
        "selected_departure_ids": list(ids),
        "selected_capacity": int(round(capacity)),
        "service_floor": service_floor,
        "expected_registered_loss": loss,
        "objective_units": OBJECTIVE_UNITS,
        "automatic_dispatch": False,
        "operator_approval_required": True,
        "reason_codes": reasons
        + ["REGISTERED_POLICY_INPUTS_REQUIRE_OPERATOR_REVIEW"],
        "limitations": list(LIMITATIONS),
    }


def _class_candidates(
    class_row: Mapping[str, Any],
    rooms: Sequence[Mapping[str, Any]],
    *,
    building_mismatch_weight: float,
) -> list[tuple[float, str, str]]:
    class_id = str(class_row.get("class_id") or "").strip()
    attendance = _finite_positive(class_row.get("planning_attendance"))
    allowed_slots = [
        str(value).strip()
        for value in class_row.get("allowed_slots", ())
        if str(value).strip()
    ]
    required = {
        str(value).strip()
        for value in class_row.get("required_features", ())
        if str(value).strip()
    }
    preferred_building = str(class_row.get("preferred_building") or "").strip()

    if not class_id or attendance is None or not allowed_slots:
        return []

    candidates: list[tuple[float, str, str]] = []
    for room in rooms:
        room_id = str(room.get("room_id") or "").strip()
        capacity = _finite_positive(room.get("capacity"))
        features = {
            str(value).strip()
            for value in room.get("features", ())
            if str(value).strip()
        }
        building = str(room.get("building") or "").strip()
        if not room_id or capacity is None or capacity + 1e-12 < attendance:
            continue
        if not required.issubset(features):
            continue
        unused = capacity - attendance
        building_penalty = (
            building_mismatch_weight
            if preferred_building and building != preferred_building
            else 0.0
        )
        for slot in allowed_slots:
            candidates.append((unused + building_penalty, slot, room_id))
    candidates.sort()
    return candidates


def optimize_class_schedule(
    *,
    classes: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
    building_mismatch_weight: Any = 0.0,
) -> dict[str, Any]:
    """Assign each class to an allowed time slot and compatible room."""

    mismatch = _finite_nonnegative(building_mismatch_weight)
    if mismatch is None or not classes or not rooms:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "automatic_actuation": False,
            "operator_approval_required": True,
            "objective_units": OBJECTIVE_UNITS,
            "reason_codes": ["INVALID_CLASS_SCHEDULING_INPUTS"],
            "limitations": list(LIMITATIONS),
        }

    room_ids: set[str] = set()
    for room in rooms:
        room_id = str(room.get("room_id") or "").strip()
        if not room_id or room_id in room_ids:
            return {
                "policy_version": POLICY_VERSION,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "automatic_actuation": False,
                "operator_approval_required": True,
                "objective_units": OBJECTIVE_UNITS,
                "reason_codes": ["INVALID_OR_DUPLICATE_ROOM_ID"],
                "limitations": list(LIMITATIONS),
            }
        room_ids.add(room_id)

    candidates_by_class: dict[str, list[tuple[float, str, str]]] = {}
    for row in classes:
        class_id = str(row.get("class_id") or "").strip()
        if not class_id or class_id in candidates_by_class:
            return {
                "policy_version": POLICY_VERSION,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "automatic_actuation": False,
                "operator_approval_required": True,
                "objective_units": OBJECTIVE_UNITS,
                "reason_codes": ["INVALID_OR_DUPLICATE_CLASS_ID"],
                "limitations": list(LIMITATIONS),
            }
        candidates = _class_candidates(
            row,
            rooms,
            building_mismatch_weight=mismatch,
        )
        if not candidates:
            return {
                "policy_version": POLICY_VERSION,
                "decision_readiness": "WITHHOLD",
                "assignments": [],
                "automatic_actuation": False,
                "operator_approval_required": True,
                "objective_units": OBJECTIVE_UNITS,
                "reason_codes": ["CLASS_CONSTRAINTS_INFEASIBLE"],
                "blocking_class_id": class_id,
                "limitations": list(LIMITATIONS),
            }
        candidates_by_class[class_id] = candidates

    order = sorted(
        candidates_by_class,
        key=lambda class_id: (len(candidates_by_class[class_id]), class_id),
    )
    best_score = math.inf
    best_assignments: list[dict[str, Any]] | None = None
    used: set[tuple[str, str]] = set()

    def search(index: int, score: float, current: list[dict[str, Any]]) -> None:
        nonlocal best_score, best_assignments
        if score >= best_score - 1e-12:
            return
        if index >= len(order):
            best_score = score
            best_assignments = [dict(row) for row in current]
            return
        class_id = order[index]
        for candidate_score, slot, room_id in candidates_by_class[class_id]:
            key = (slot, room_id)
            if key in used:
                continue
            used.add(key)
            current.append(
                {
                    "class_id": class_id,
                    "slot": slot,
                    "room_id": room_id,
                    "assignment_loss": candidate_score,
                }
            )
            search(index + 1, score + candidate_score, current)
            current.pop()
            used.remove(key)

    search(0, 0.0, [])

    if best_assignments is None:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "assignments": [],
            "automatic_actuation": False,
            "operator_approval_required": True,
            "objective_units": OBJECTIVE_UNITS,
            "reason_codes": ["NO_COLLISION_FREE_CLASS_SCHEDULE"],
            "limitations": list(LIMITATIONS),
        }

    best_assignments.sort(key=lambda row: row["class_id"])
    return {
        "policy_version": POLICY_VERSION,
        "decision_readiness": "REVIEW_REQUIRED",
        "assignments": best_assignments,
        "total_registered_loss": best_score,
        "objective_units": OBJECTIVE_UNITS,
        "automatic_actuation": False,
        "operator_approval_required": True,
        "reason_codes": ["REGISTERED_SCHEDULE_REQUIRES_OPERATOR_REVIEW"],
        "limitations": list(LIMITATIONS),
    }


def allocate_shared_capacity(
    *,
    total_capacity: Any,
    requests: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Allocate integer shared capacity after satisfying registered minimums."""

    capacity = _finite_nonnegative(total_capacity)
    if capacity is None or int(capacity) != capacity:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["TOTAL_CAPACITY_MUST_BE_NONNEGATIVE_INTEGER"],
            "automatic_actuation": False,
            "operator_approval_required": True,
            "limitations": list(LIMITATIONS),
        }
    remaining = int(capacity)
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in requests or ():
        request_id = str(raw.get("request_id") or "").strip()
        minimum = _finite_nonnegative(raw.get("minimum"))
        desired = _finite_nonnegative(raw.get("desired"))
        priority = _finite_positive(raw.get("priority_weight"))
        if (
            not request_id
            or request_id in seen
            or minimum is None
            or desired is None
            or priority is None
            or int(minimum) != minimum
            or int(desired) != desired
            or desired < minimum
        ):
            return {
                "policy_version": POLICY_VERSION,
                "decision_readiness": "WITHHOLD",
                "allocations": [],
                "reason_codes": ["INVALID_SHARED_CAPACITY_REQUEST"],
                "automatic_actuation": False,
                "operator_approval_required": True,
                "limitations": list(LIMITATIONS),
            }
        seen.add(request_id)
        normalized.append(
            {
                "request_id": request_id,
                "minimum": int(minimum),
                "desired": int(desired),
                "priority_weight": float(priority),
                "allocated": int(minimum),
            }
        )

    if not normalized:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["NO_SHARED_CAPACITY_REQUESTS"],
            "automatic_actuation": False,
            "operator_approval_required": True,
            "limitations": list(LIMITATIONS),
        }

    minimum_total = sum(row["minimum"] for row in normalized)
    if minimum_total > remaining:
        return {
            "policy_version": POLICY_VERSION,
            "decision_readiness": "WITHHOLD",
            "allocations": [],
            "reason_codes": ["REGISTERED_MINIMUMS_EXCEED_AVAILABLE_CAPACITY"],
            "automatic_actuation": False,
            "operator_approval_required": True,
            "limitations": list(LIMITATIONS),
        }

    remaining -= minimum_total
    while remaining > 0:
        eligible = [row for row in normalized if row["allocated"] < row["desired"]]
        if not eligible:
            break
        eligible.sort(
            key=lambda row: (
                -row["priority_weight"],
                -(row["desired"] - row["allocated"]),
                row["request_id"],
            )
        )
        eligible[0]["allocated"] += 1
        remaining -= 1

    allocations = [
        {
            "request_id": row["request_id"],
            "allocated": row["allocated"],
            "minimum": row["minimum"],
            "desired": row["desired"],
            "priority_weight": row["priority_weight"],
        }
        for row in sorted(normalized, key=lambda item: item["request_id"])
    ]
    return {
        "policy_version": POLICY_VERSION,
        "decision_readiness": "REVIEW_REQUIRED",
        "allocations": allocations,
        "unallocated_capacity": remaining,
        "objective_units": OBJECTIVE_UNITS,
        "automatic_actuation": False,
        "operator_approval_required": True,
        "reason_codes": ["REGISTERED_PRIORITIES_REQUIRE_OPERATOR_REVIEW"],
        "limitations": list(LIMITATIONS),
    }


def build_campus_ops_bundle(
    modules: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Combine module states using the most conservative readiness."""

    if not modules:
        readiness = "WITHHOLD"
        reasons = ["NO_CAMPUS_OPS_MODULES"]
    else:
        normalized: list[tuple[str, str]] = []
        reasons = []
        for module_id, result in modules.items():
            state = str(result.get("decision_readiness") or "WITHHOLD").upper()
            if state not in READINESS_ORDER:
                state = "WITHHOLD"
                reasons.append(f"UNKNOWN_READINESS_{module_id}")
            normalized.append((str(module_id), state))
        readiness = max(
            (state for _, state in normalized),
            key=lambda state: READINESS_ORDER[state],
        )

    return {
        "policy_version": POLICY_VERSION,
        "decision_readiness": readiness,
        "operator_approval_required": True,
        "automatic_actuation": False,
        "evidence_boundary": EVIDENCE_BOUNDARY,
        "module_states": {
            str(module_id): str(result.get("decision_readiness") or "WITHHOLD").upper()
            for module_id, result in modules.items()
        },
        "reason_codes": reasons,
        "limitations": list(LIMITATIONS),
    }
