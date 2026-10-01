from __future__ import annotations

import math
from typing import Any, Mapping

POLICY_VERSION = "shuttle-capacity-decision-v1.0"
FORECAST_PROVENANCE = "MODEL_ESTIMATE"
DECISION_PROVENANCE = "POLICY_HEURISTIC"
BAND_SEMANTICS = "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
CALIBRATION_STATUS = "NOT_CALIBRATED"
TELEMETRY_STATUS = "NOT_CONNECTED"

SIGNAL_WEIGHTS_PCT = {
    "official_schedule": 40,
    "historical_boardings": 30,
    "course_schedule": 20,
    "calendar": 10,
}
REQUIRED_SIGNALS = ("official_schedule",)
PILOT_READY_MIN_COVERAGE_PCT = 70
REVIEW_MIN_COVERAGE_PCT = 50
METHOD_ELIGIBILITY_STATES = (
    "SANDBOX_ONLY",
    "EVALUATED_OFFLINE",
    "PILOT_ELIGIBLE",
    "PILOT_EVALUATED",
    "RETIRED",
)
VERIFIED_CAPACITY_PROVENANCE = ("OFFICIAL_PUBLIC", "MEASURED_OPERATIONAL")

LIMITATIONS = (
    "NO_SHUTTLE_GPS_TELEMETRY",
    "NO_REALTIME_OCCUPANCY_TELEMETRY",
    "HEURISTIC_BAND_NOT_CALIBRATED",
    "NO_AUTOMATIC_SHUTTLE_DISPATCH",
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


def _band_factors(coverage_pct: int) -> tuple[float, float]:
    if coverage_pct >= 80:
        return 0.92, 1.10
    if coverage_pct >= 60:
        return 0.88, 1.15
    return 0.82, 1.22


def build_shuttle_decision(
    expected_boardings: Any,
    *,
    scheduled_capacity: Any = None,
    signal_availability: Mapping[str, bool] | None = None,
    capacity_provenance: str = "UNAVAILABLE",
    method_eligibility: str = "SANDBOX_ONLY",
    route_id: str | None = None,
    model_id: str = "shuttle-demand-method",
) -> dict[str, Any]:
    """Build an operator-reviewed shuttle capacity-planning decision.

    The function never infers live vehicle occupancy or ETA. A capacity-sensitive
    action is allowed only when the caller supplies a positive service capacity
    whose provenance is official public data or measured operational data.
    Planning ranges are explicit policy heuristics, not calibrated intervals.
    """

    normalized_eligibility, unknown_eligibility = _normalize_method_eligibility(
        method_eligibility
    )
    boardings = _normalize_positive_count(expected_boardings)
    capacity = _normalize_positive_count(scheduled_capacity)
    normalized_capacity_provenance = str(capacity_provenance or "UNAVAILABLE").upper()

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

    lower_factor, upper_factor = _band_factors(coverage)
    planning_lower = int(round(boardings * lower_factor))
    planning_upper = int(round(boardings * upper_factor))
    capacity_gap = max(0, boardings - capacity) if capacity > 0 else None

    reason_codes = ["HEURISTIC_BAND_NOT_CALIBRATED"]
    reason_codes.extend(
        f"MISSING_{signal.upper()}"
        for signal, available in availability.items()
        if not available
    )
    if unknown_eligibility:
        reason_codes.append("UNKNOWN_METHOD_ELIGIBILITY_TREATED_AS_SANDBOX")

    required_missing = [signal for signal in REQUIRED_SIGNALS if not availability[signal]]
    capacity_verified = (
        capacity > 0
        and normalized_capacity_provenance in VERIFIED_CAPACITY_PROVENANCE
    )

    if boardings <= 0:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_POSITIVE_BOARDING_ESTIMATE")
    elif required_missing:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "MISSING_REQUIRED_OFFICIAL_SCHEDULE")
    elif capacity <= 0:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_VERIFIED_SERVICE_CAPACITY")
    elif not capacity_verified:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "UNVERIFIED_CAPACITY_PROVENANCE")
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
    if abstained:
        recommended_action = None
    elif capacity_gap and capacity_gap > 0:
        recommended_action = "REVIEW_CAPACITY_PLAN"
    else:
        recommended_action = "HOLD_CURRENT_CAPACITY"

    return {
        "policy_version": POLICY_VERSION,
        "route_id": route_id,
        "model_id": model_id,
        "method_eligibility": normalized_eligibility,
        "forecast_provenance": FORECAST_PROVENANCE,
        "decision_provenance": DECISION_PROVENANCE,
        "band_semantics": BAND_SEMANTICS,
        "calibration_status": CALIBRATION_STATUS,
        "expected_boardings": boardings,
        "planning_lower": planning_lower,
        "planning_upper": planning_upper,
        "scheduled_capacity": capacity if capacity > 0 else None,
        "capacity_provenance": normalized_capacity_provenance,
        "capacity_gap": capacity_gap,
        "recommended_action": recommended_action,
        "signal_coverage_pct": coverage,
        "decision_readiness": readiness,
        "abstained": abstained,
        "operator_approval_required": True,
        "automatic_shuttle_dispatch": False,
        "telemetry_status": TELEMETRY_STATUS,
        "live_eta_available": False,
        "live_occupancy_available": False,
        "signals": signals,
        "reason_codes": reason_codes,
        "limitations": list(LIMITATIONS),
    }
