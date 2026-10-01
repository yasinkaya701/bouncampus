from __future__ import annotations

from dataclasses import dataclass
import math
from statistics import median
from typing import Any, Iterable, Mapping, Sequence

DECISION_POLICY_VERSION = "campus-operations-v1.0"
TRUTH_BOUNDARY = (
    "Decision-support only. Outputs are planning recommendations from supplied "
    "inputs; they are not evidence of realized savings, live telemetry, or calibrated probabilities."
)

READINESS_PILOT = "PILOT_READY"
READINESS_REVIEW = "REVIEW_REQUIRED"
READINESS_WITHHOLD = "WITHHOLD"


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


def _robust_center(values: Iterable[Any]) -> tuple[float | None, int]:
    clean = [n for n in (_number(v, minimum=0) for v in values) if n is not None]
    if not clean:
        return None, 0
    return float(median(clean)), len(clean)


def _quantile(values: Sequence[float], q: float) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    low = int(math.floor(pos))
    high = int(math.ceil(pos))
    if low == high:
        return ordered[low]
    frac = pos - low
    return ordered[low] * (1.0 - frac) + ordered[high] * frac


def _signal_coverage(signals: Mapping[str, bool], weights: Mapping[str, int]) -> int:
    return sum(weight for name, weight in weights.items() if bool(signals.get(name, False)))


def plan_food_service(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Produce a conservative food-production planning recommendation.

    This is a transparent baseline-first policy. It combines a robust historical
    center with bounded, caller-supplied context multipliers and optionally uses
    reservations as an intent floor. It deliberately abstains when the minimum
    information needed for an operator-reviewed decision is absent.
    """

    history = payload.get("historical_served", [])
    if not isinstance(history, Sequence) or isinstance(history, (str, bytes)):
        history = []
    historical_center, history_n = _robust_center(history)

    baseline = _number(payload.get("baseline_estimate"), minimum=0)
    if baseline is None:
        baseline = historical_center

    reservations = _number(payload.get("reservations"), minimum=0)
    signals = payload.get("signals") if isinstance(payload.get("signals"), Mapping) else {}
    weights = {"schedule": 35, "menu": 25, "calendar": 15, "weather": 10, "reservation": 15}
    availability = {name: bool(signals.get(name, False)) for name in weights}
    if reservations is not None:
        availability["reservation"] = True
    coverage = _signal_coverage(availability, weights)

    context = payload.get("context_multipliers")
    context = context if isinstance(context, Mapping) else {}
    applied: list[dict[str, Any]] = []
    multiplier = 1.0
    for name in ("schedule", "menu", "calendar", "weather"):
        raw = _number(context.get(name), minimum=0)
        if raw is None or not availability.get(name, False):
            continue
        bounded = min(max(raw, 0.85), 1.15)
        multiplier *= bounded
        applied.append({"signal": name, "requested": raw, "applied": bounded})

    reason_codes: list[str] = []
    if baseline is None or baseline <= 0:
        return {
            "policy_version": DECISION_POLICY_VERSION,
            "domain": "FOOD",
            "readiness": READINESS_WITHHOLD,
            "recommended_production": None,
            "estimate": None,
            "planning_lower": None,
            "planning_upper": None,
            "signal_coverage_pct": coverage,
            "reason_codes": ["NO_USABLE_BASELINE"],
            "provenance": "TRANSPARENT_POLICY_BASELINE",
            "operator_approval_required": True,
            "automatic_dispatch": False,
            "truth_boundary": TRUTH_BOUNDARY,
        }

    estimate = baseline * multiplier
    if reservations is not None:
        reservation_floor = reservations * 0.90
        if reservation_floor > estimate:
            estimate = reservation_floor
            reason_codes.append("RESERVATION_INTENT_FLOOR_APPLIED")

    clean_history = [n for n in (_number(v, minimum=0) for v in history) if n is not None]
    if len(clean_history) >= 5:
        q25 = _quantile(clean_history, 0.25)
        q75 = _quantile(clean_history, 0.75)
        empirical_half_width = max((q75 - q25) * 0.75, estimate * 0.04)
        band_semantics = "EMPIRICAL_PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
    else:
        empirical_half_width = estimate * (0.08 if coverage >= 70 else 0.12)
        band_semantics = "HEURISTIC_PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
        reason_codes.append("LIMITED_HISTORY_FOR_EMPIRICAL_RANGE")

    lower = max(0, int(round(estimate - empirical_half_width)))
    upper = max(lower, int(round(estimate + empirical_half_width)))

    shortage_weight = _number(payload.get("shortage_weight"), minimum=0)
    surplus_weight = _number(payload.get("surplus_weight"), minimum=0)
    shortage_weight = 1.0 if shortage_weight is None else shortage_weight
    surplus_weight = 1.0 if surplus_weight is None else surplus_weight
    total_cost = shortage_weight + surplus_weight
    target_q = 0.5 if total_cost <= 0 else shortage_weight / total_cost

    recommended = int(round(lower + target_q * (upper - lower)))
    recommended = min(max(recommended, lower), upper)

    required_schedule = availability.get("schedule", False)
    if not required_schedule:
        readiness = READINESS_WITHHOLD
        reason_codes.insert(0, "SCHEDULE_SIGNAL_REQUIRED")
        recommended_output: int | None = None
    elif coverage >= 70 and history_n >= 3:
        readiness = READINESS_PILOT
        recommended_output = recommended
    elif coverage >= 50:
        readiness = READINESS_REVIEW
        recommended_output = recommended
        reason_codes.insert(0, "PARTIAL_CONTEXT_OPERATOR_REVIEW_REQUIRED")
    else:
        readiness = READINESS_WITHHOLD
        recommended_output = None
        reason_codes.insert(0, "INSUFFICIENT_DECISION_CONTEXT")

    return {
        "policy_version": DECISION_POLICY_VERSION,
        "domain": "FOOD",
        "readiness": readiness,
        "estimate": int(round(estimate)),
        "planning_lower": lower,
        "planning_upper": upper,
        "recommended_production": recommended_output,
        "signal_coverage_pct": coverage,
        "history_n": history_n,
        "baseline_estimate": int(round(baseline)),
        "cost_target_quantile": round(target_q, 4),
        "context_adjustments": applied,
        "band_semantics": band_semantics,
        "reason_codes": reason_codes,
        "provenance": "TRANSPARENT_POLICY_BASELINE",
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "truth_boundary": TRUTH_BOUNDARY,
    }


def plan_shuttle_service(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Allocate vehicle capacity across departures using demand and queue risk."""

    departures = payload.get("departures")
    if not isinstance(departures, Sequence) or isinstance(departures, (str, bytes)):
        departures = []
    vehicle_capacity = _positive_int(payload.get("vehicle_capacity"))
    reserve_ratio = _number(payload.get("reserve_ratio"), minimum=0)
    reserve_ratio = 0.10 if reserve_ratio is None else min(reserve_ratio, 0.50)

    if not departures or vehicle_capacity is None:
        return {
            "policy_version": DECISION_POLICY_VERSION,
            "domain": "SHUTTLE",
            "readiness": READINESS_WITHHOLD,
            "reason_codes": ["DEPARTURES_AND_VEHICLE_CAPACITY_REQUIRED"],
            "plan": [],
            "truth_boundary": TRUTH_BOUNDARY,
        }

    plan: list[dict[str, Any]] = []
    invalid = 0
    total_demand = 0
    total_seats = 0
    overflow_total = 0

    for index, item in enumerate(departures):
        if not isinstance(item, Mapping):
            invalid += 1
            continue
        demand = _number(item.get("predicted_demand"), minimum=0)
        if demand is None:
            invalid += 1
            continue
        queue = _number(item.get("waiting_queue"), minimum=0) or 0.0
        scheduled = _positive_int(item.get("scheduled_vehicles")) or 1
        demand_with_queue = int(math.ceil(demand + queue))
        seats_per_vehicle = max(1, int(math.floor(vehicle_capacity * (1.0 - reserve_ratio))))
        required = max(1, int(math.ceil(demand_with_queue / seats_per_vehicle)))
        recommended_vehicles = max(scheduled, required)
        seats = recommended_vehicles * vehicle_capacity
        overflow = max(0, demand_with_queue - seats)
        load_ratio = 0.0 if seats == 0 else demand_with_queue / seats

        total_demand += demand_with_queue
        total_seats += seats
        overflow_total += overflow

        plan.append({
            "departure_id": str(item.get("departure_id") or f"departure-{index + 1}"),
            "predicted_demand_with_queue": demand_with_queue,
            "scheduled_vehicles": scheduled,
            "recommended_vehicles": recommended_vehicles,
            "added_vehicles": max(0, recommended_vehicles - scheduled),
            "planned_seats": seats,
            "planned_load_ratio": round(load_ratio, 4),
            "projected_overflow": overflow,
            "reason_codes": (
                ["CAPACITY_AUGMENTATION_RECOMMENDED"]
                if recommended_vehicles > scheduled
                else ["SCHEDULED_CAPACITY_SUFFICIENT"]
            ),
        })

    if not plan:
        readiness = READINESS_WITHHOLD
        reasons = ["NO_VALID_DEPARTURE_DEMAND"]
    elif invalid:
        readiness = READINESS_REVIEW
        reasons = ["PARTIAL_INVALID_DEPARTURE_INPUTS"]
    elif overflow_total > 0:
        readiness = READINESS_REVIEW
        reasons = ["PROJECTED_OVERFLOW_REMAINS"]
    else:
        readiness = READINESS_PILOT
        reasons = []

    return {
        "policy_version": DECISION_POLICY_VERSION,
        "domain": "SHUTTLE",
        "readiness": readiness,
        "vehicle_capacity": vehicle_capacity,
        "reserve_ratio": reserve_ratio,
        "total_predicted_demand_with_queue": total_demand,
        "total_planned_seats": total_seats,
        "projected_overflow": overflow_total,
        "plan": plan,
        "reason_codes": reasons,
        "provenance": "CAPACITY_AND_QUEUE_HEURISTIC",
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "truth_boundary": TRUTH_BOUNDARY,
    }


@dataclass(frozen=True)
class _Room:
    room_id: str
    capacity: int
    building_id: str
    energy_cost: float
    available_slots: frozenset[str]


def _parse_rooms(raw_rooms: Any) -> tuple[list[_Room], list[str]]:
    if not isinstance(raw_rooms, Sequence) or isinstance(raw_rooms, (str, bytes)):
        return [], ["ROOMS_REQUIRED"]
    rooms: list[_Room] = []
    errors: list[str] = []
    for index, item in enumerate(raw_rooms):
        if not isinstance(item, Mapping):
            errors.append(f"ROOM_{index}_INVALID")
            continue
        room_id = str(item.get("room_id") or "").strip()
        capacity = _positive_int(item.get("capacity"))
        building_id = str(item.get("building_id") or "UNKNOWN").strip() or "UNKNOWN"
        energy = _number(item.get("energy_cost"), minimum=0)
        slots = item.get("available_slots")
        if (
            not room_id
            or capacity is None
            or energy is None
            or not isinstance(slots, Sequence)
            or isinstance(slots, (str, bytes))
        ):
            errors.append(f"ROOM_{index}_INVALID")
            continue
        rooms.append(
            _Room(
                room_id=room_id,
                capacity=capacity,
                building_id=building_id,
                energy_cost=energy,
                available_slots=frozenset(str(slot) for slot in slots),
            )
        )
    return rooms, errors


def allocate_classrooms(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Allocate sessions to rooms with capacity/conflict hard constraints."""

    rooms, room_errors = _parse_rooms(payload.get("rooms"))
    sessions = payload.get("sessions")
    if not isinstance(sessions, Sequence) or isinstance(sessions, (str, bytes)):
        sessions = []

    valid_sessions: list[dict[str, Any]] = []
    invalid_session_ids: list[str] = []
    for index, session in enumerate(sessions):
        if not isinstance(session, Mapping):
            invalid_session_ids.append(f"session-{index + 1}")
            continue
        sid = str(session.get("session_id") or f"session-{index + 1}")
        slot = str(session.get("slot") or "").strip()
        expected = _positive_int(session.get("expected_attendance"))
        if not slot or expected is None:
            invalid_session_ids.append(sid)
            continue
        valid_sessions.append({
            "session_id": sid,
            "slot": slot,
            "expected_attendance": expected,
        })

    valid_sessions.sort(key=lambda item: (-item["expected_attendance"], item["session_id"]))
    occupied: set[tuple[str, str]] = set()
    active_buildings: dict[str, set[str]] = {}
    assignments: list[dict[str, Any]] = []
    unassigned: list[dict[str, Any]] = []

    seat_weight = _number(payload.get("unused_seat_weight"), minimum=0)
    energy_weight = _number(payload.get("energy_weight"), minimum=0)
    activation_penalty = _number(payload.get("building_activation_penalty"), minimum=0)
    seat_weight = 1.0 if seat_weight is None else seat_weight
    energy_weight = 1.0 if energy_weight is None else energy_weight
    activation_penalty = 20.0 if activation_penalty is None else activation_penalty

    for session in valid_sessions:
        slot = session["slot"]
        expected = session["expected_attendance"]
        slot_active = active_buildings.setdefault(slot, set())
        candidates: list[tuple[float, _Room]] = []
        for room in rooms:
            if slot not in room.available_slots:
                continue
            if room.capacity < expected:
                continue
            if (room.room_id, slot) in occupied:
                continue
            unused = room.capacity - expected
            activation = 0.0 if room.building_id in slot_active else activation_penalty
            score = unused * seat_weight + room.energy_cost * energy_weight + activation
            candidates.append((score, room))

        if not candidates:
            unassigned.append({
                **session,
                "reason_codes": ["NO_ROOM_MEETS_CAPACITY_AND_AVAILABILITY"],
            })
            continue

        candidates.sort(key=lambda pair: (pair[0], pair[1].capacity, pair[1].room_id))
        score, chosen = candidates[0]
        occupied.add((chosen.room_id, slot))
        slot_active.add(chosen.building_id)
        assignments.append({
            **session,
            "room_id": chosen.room_id,
            "building_id": chosen.building_id,
            "room_capacity": chosen.capacity,
            "unused_seats": chosen.capacity - expected,
            "energy_cost": chosen.energy_cost,
            "allocation_score": round(score, 4),
        })

    if not assignments and valid_sessions:
        readiness = READINESS_WITHHOLD
    elif unassigned or invalid_session_ids or room_errors:
        readiness = READINESS_REVIEW
    elif assignments:
        readiness = READINESS_PILOT
    else:
        readiness = READINESS_WITHHOLD

    return {
        "policy_version": DECISION_POLICY_VERSION,
        "domain": "CLASSROOM",
        "readiness": readiness,
        "assignments": assignments,
        "unassigned": unassigned,
        "invalid_session_ids": invalid_session_ids,
        "input_errors": room_errors,
        "assigned_count": len(assignments),
        "unassigned_count": len(unassigned) + len(invalid_session_ids),
        "objective": {
            "unused_seat_weight": seat_weight,
            "energy_weight": energy_weight,
            "building_activation_penalty": activation_penalty,
        },
        "provenance": "CAPACITY_CONFLICT_ENERGY_HEURISTIC",
        "operator_approval_required": True,
        "automatic_timetable_commit": False,
        "truth_boundary": TRUTH_BOUNDARY,
    }


def build_operations_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Build a cross-domain decision snapshot without inventing impact claims."""

    food = plan_food_service(payload.get("food", {}) if isinstance(payload.get("food"), Mapping) else {})
    shuttle = plan_shuttle_service(payload.get("shuttle", {}) if isinstance(payload.get("shuttle"), Mapping) else {})
    classroom = allocate_classrooms(payload.get("classroom", {}) if isinstance(payload.get("classroom"), Mapping) else {})

    readiness_order = {READINESS_PILOT: 0, READINESS_REVIEW: 1, READINESS_WITHHOLD: 2}
    domains = [food, shuttle, classroom]
    overall = max((d["readiness"] for d in domains), key=lambda status: readiness_order[status])

    return {
        "policy_version": DECISION_POLICY_VERSION,
        "overall_readiness": overall,
        "domains": {
            "food": food,
            "shuttle": shuttle,
            "classroom": classroom,
        },
        "claim_boundary": (
            "Cross-domain snapshot reports planning state only; no realized carbon, "
            "cost, waste, service-quality, or utilization improvement is claimed."
        ),
    }
