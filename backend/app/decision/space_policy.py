from __future__ import annotations

import math
from typing import Any, Iterable, Mapping, Sequence

POLICY_VERSION = "space-assignment-decision-v1.0"
DECISION_PROVENANCE = "POLICY_HEURISTIC"
ASSIGNMENT_METHOD = "MINIMUM_FEASIBLE_CAPACITY"
OCCUPANCY_TELEMETRY_STATUS = "NOT_CONNECTED"

SIGNAL_WEIGHTS_PCT = {
    "timetable": 35,
    "room_inventory": 30,
    "attendance": 25,
    "accessibility_metadata": 10,
}
BASE_REQUIRED_SIGNALS = ("timetable", "room_inventory", "attendance")
PILOT_READY_MIN_COVERAGE_PCT = 90
REVIEW_MIN_COVERAGE_PCT = 70
METHOD_ELIGIBILITY_STATES = (
    "SANDBOX_ONLY",
    "EVALUATED_OFFLINE",
    "PILOT_ELIGIBLE",
    "PILOT_EVALUATED",
    "RETIRED",
)
VERIFIED_INVENTORY_PROVENANCE = ("OFFICIAL_PUBLIC", "MEASURED_OPERATIONAL")

LIMITATIONS = (
    "NO_LIVE_ROOM_OCCUPANCY_TELEMETRY",
    "ATTENDANCE_ESTIMATE_MAY_DIFFER_FROM_REALIZED_ATTENDANCE",
    "NO_AUTOMATIC_ROOM_BOOKING",
    "CONSTRAINT_HEURISTIC_NOT_OPTIMIZATION_PROOF",
)


def _normalize_positive_count(value: Any) -> int:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(numeric) or numeric <= 0:
        return 0
    return max(0, int(round(numeric)))


def _normalize_method_eligibility(value: Any) -> tuple[str, bool]:
    candidate = str(value or "SANDBOX_ONLY").upper()
    if candidate in METHOD_ELIGIBILITY_STATES:
        return candidate, False
    return "SANDBOX_ONLY", True


def _normalize_features(features: Any) -> set[str] | None:
    if features is None:
        return set()
    if not isinstance(features, (list, tuple, set, frozenset)):
        return None
    normalized: set[str] = set()
    for feature in features:
        if not isinstance(feature, str) or not feature.strip():
            return None
        normalized.add(feature.strip().lower())
    return normalized


def _normalize_inventory(
    room_candidates: Sequence[Mapping[str, Any]] | None,
) -> tuple[list[dict[str, Any]], bool]:
    if room_candidates is None or isinstance(room_candidates, (str, bytes)):
        return [], False
    try:
        candidates = list(room_candidates)
    except TypeError:
        return [], False

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for raw in candidates:
        if not isinstance(raw, Mapping):
            return [], False
        room_id = str(raw.get("room_id") or "").strip()
        capacity = _normalize_positive_count(raw.get("capacity"))
        available = raw.get("available")
        accessible = raw.get("accessible")
        features = _normalize_features(raw.get("features"))

        if (
            not room_id
            or room_id in seen_ids
            or capacity <= 0
            or not isinstance(available, bool)
            or not isinstance(accessible, bool)
            or features is None
        ):
            return [], False

        seen_ids.add(room_id)
        normalized.append(
            {
                "room_id": room_id,
                "capacity": capacity,
                "available": available,
                "accessible": accessible,
                "features": features,
            }
        )

    return normalized, True


def _required_feature_set(required_features: Iterable[str] | None) -> set[str] | None:
    if required_features is None:
        return set()
    try:
        values = list(required_features)
    except TypeError:
        return None
    if any(not isinstance(value, str) or not value.strip() for value in values):
        return None
    return {value.strip().lower() for value in values}


def build_space_decision(
    expected_attendance: Any,
    room_candidates: Sequence[Mapping[str, Any]] | None,
    *,
    signal_availability: Mapping[str, bool] | None = None,
    inventory_provenance: str = "UNAVAILABLE",
    method_eligibility: str = "SANDBOX_ONLY",
    session_id: str | None = None,
    accessible_required: bool = False,
    required_features: Iterable[str] | None = None,
    model_id: str = "attendance-demand-method",
) -> dict[str, Any]:
    """Recommend a feasible room for operator review using explicit hard constraints.

    The policy minimizes unused seats among rooms that are currently represented as
    available in the supplied inventory and that satisfy capacity, accessibility,
    and requested feature constraints. It does not infer live occupancy and never
    writes a booking automatically.
    """

    attendance = _normalize_positive_count(expected_attendance)
    normalized_eligibility, unknown_eligibility = _normalize_method_eligibility(
        method_eligibility
    )
    normalized_inventory_provenance = str(inventory_provenance or "UNAVAILABLE").upper()
    inventory, inventory_valid = _normalize_inventory(room_candidates)
    required_feature_set = _required_feature_set(required_features)
    if not isinstance(accessible_required, bool):
        accessible_required = True
        inventory_valid = False

    availability = {
        signal: bool((signal_availability or {}).get(signal, False))
        for signal in SIGNAL_WEIGHTS_PCT
    }
    signals = [
        {
            "id": signal,
            "available": availability[signal],
            "policy_weight_pct": weight,
            "weight_basis": DECISION_PROVENANCE,
        }
        for signal, weight in SIGNAL_WEIGHTS_PCT.items()
    ]
    coverage = sum(
        signal["policy_weight_pct"] for signal in signals if signal["available"]
    )

    required_signals = list(BASE_REQUIRED_SIGNALS)
    if accessible_required:
        required_signals.append("accessibility_metadata")
    required_missing = [signal for signal in required_signals if not availability[signal]]

    rejected: list[dict[str, Any]] = []
    feasible: list[dict[str, Any]] = []
    if inventory_valid and required_feature_set is not None:
        for room in inventory:
            reasons: list[str] = []
            if not room["available"]:
                reasons.append("NOT_AVAILABLE")
            if room["capacity"] < attendance:
                reasons.append("INSUFFICIENT_CAPACITY")
            if accessible_required and not room["accessible"]:
                reasons.append("ACCESSIBILITY_CONSTRAINT")
            missing_features = sorted(required_feature_set - room["features"])
            if missing_features:
                reasons.append("MISSING_REQUIRED_FEATURES")

            if reasons:
                rejected.append({"room_id": room["room_id"], "reason_codes": reasons})
            else:
                feasible.append(room)

    feasible.sort(key=lambda room: (room["capacity"] - attendance, room["room_id"]))
    selected = feasible[0] if feasible else None

    reason_codes = ["NO_LIVE_OCCUPANCY_USED_FOR_ASSIGNMENT"]
    reason_codes.extend(
        f"MISSING_{signal.upper()}"
        for signal, available in availability.items()
        if not available
    )
    if unknown_eligibility:
        reason_codes.append("UNKNOWN_METHOD_ELIGIBILITY_TREATED_AS_SANDBOX")

    inventory_verified = (
        normalized_inventory_provenance in VERIFIED_INVENTORY_PROVENANCE
    )

    if attendance <= 0:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_POSITIVE_ATTENDANCE_ESTIMATE")
    elif required_feature_set is None or not inventory_valid:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "INVALID_ROOM_INVENTORY")
    elif required_missing:
        readiness = "WITHHOLD"
        missing = required_missing[0].upper()
        reason_codes.insert(0, f"MISSING_REQUIRED_{missing}")
    elif not inventory_verified:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "UNVERIFIED_ROOM_INVENTORY_PROVENANCE")
    elif selected is None:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_FEASIBLE_SPACE")
    elif normalized_eligibility == "SANDBOX_ONLY":
        readiness = "WITHHOLD"
        reason_codes.insert(0, "METHOD_SANDBOX_ONLY")
    elif normalized_eligibility == "RETIRED":
        readiness = "WITHHOLD"
        reason_codes.insert(0, "METHOD_RETIRED")
    elif coverage < REVIEW_MIN_COVERAGE_PCT:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "INSUFFICIENT_DECISION_CONTEXT")
    elif normalized_eligibility == "EVALUATED_OFFLINE":
        readiness = "REVIEW_REQUIRED"
        reason_codes.insert(0, "METHOD_NOT_YET_PILOT_ELIGIBLE")
    elif coverage >= PILOT_READY_MIN_COVERAGE_PCT:
        readiness = "PILOT_READY"
    else:
        readiness = "REVIEW_REQUIRED"
        reason_codes.insert(0, "CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED")

    abstained = readiness == "WITHHOLD"
    recommended_room_id = None if abstained or selected is None else selected["room_id"]
    recommended_capacity = None if abstained or selected is None else selected["capacity"]
    seat_slack = (
        None
        if abstained or selected is None
        else selected["capacity"] - attendance
    )

    return {
        "policy_version": POLICY_VERSION,
        "session_id": session_id,
        "model_id": model_id,
        "method_eligibility": normalized_eligibility,
        "decision_provenance": DECISION_PROVENANCE,
        "assignment_method": ASSIGNMENT_METHOD,
        "expected_attendance": attendance,
        "inventory_provenance": normalized_inventory_provenance,
        "candidate_room_count": len(inventory),
        "feasible_room_count": len(feasible),
        "recommended_room_id": recommended_room_id,
        "recommended_room_capacity": recommended_capacity,
        "seat_slack": seat_slack,
        "required_features": sorted(required_feature_set or set()),
        "accessible_required": accessible_required,
        "signal_coverage_pct": coverage,
        "decision_readiness": readiness,
        "abstained": abstained,
        "operator_approval_required": True,
        "automatic_room_booking": False,
        "occupancy_telemetry_status": OCCUPANCY_TELEMETRY_STATUS,
        "live_occupancy_available": False,
        "signals": signals,
        "rejected_candidates": rejected,
        "reason_codes": reason_codes,
        "limitations": list(LIMITATIONS),
    }
