from __future__ import annotations

import math
from typing import Any, Mapping

POLICY_VERSION = "food-decision-v1.1"
REACHABILITY_POLICY_VERSION = "decision-reachability-v1.1"
FORECAST_PROVENANCE = "MODEL_ESTIMATE"
DECISION_PROVENANCE = "POLICY_HEURISTIC"
BAND_SEMANTICS = "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
CALIBRATION_STATUS = "NOT_CALIBRATED"

SIGNAL_WEIGHTS_PCT = {
    "schedule": 50,
    "weather": 20,
    "menu": 20,
    "calendar": 10,
}
REQUIRED_SIGNALS = ("schedule",)
PILOT_READY_MIN_COVERAGE_PCT = 70
REVIEW_MIN_COVERAGE_PCT = 50
METHOD_ELIGIBILITY_STATES = (
    "SANDBOX_ONLY",
    "EVALUATED_OFFLINE",
    "PILOT_ELIGIBLE",
    "PILOT_EVALUATED",
    "RETIRED",
)

LIMITATIONS = (
    "NO_CAFETERIA_POS_OR_SERVED_MEAL_TELEMETRY",
    "HEURISTIC_BAND_NOT_CALIBRATED",
    "PILOT_OUTCOMES_NOT_YET_MEASURED",
)


def _normalize_demand(value: Any) -> int:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(numeric) or numeric <= 0:
        return 0
    return max(0, int(round(numeric)))


def _band_factors(coverage_pct: int) -> tuple[float, float]:
    if coverage_pct >= 80:
        return 0.96, 1.06
    if coverage_pct >= 60:
        return 0.93, 1.09
    return 0.90, 1.13


def _normalize_method_eligibility(value: Any) -> tuple[str, bool]:
    candidate = str(value or "SANDBOX_ONLY").upper()
    if candidate in METHOD_ELIGIBILITY_STATES:
        return candidate, False
    return "SANDBOX_ONLY", True


def _normalize_minutes_before_freeze(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    numeric = float(value)
    if not math.isfinite(numeric):
        return None
    return numeric


def _normalize_optional_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _assess_decision_reachability(
    decision_reachability: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Classify whether a recommendation can still reach a verified real decision.

    Reachability is operational, not predictive. A free-form control-surface name is
    insufficient by itself: the surface must have been verified, operator authority
    must be confirmed, the decision window must still be open, and the workflow must
    be confirmed changeable before freeze. Unknown evidence prevents `PILOT_READY`;
    known impossibility fails closed to `WITHHOLD`.
    """

    if not isinstance(decision_reachability, Mapping):
        return {
            "status": "UNVERIFIED",
            "decision_surface": None,
            "decision_surface_verified": None,
            "operator_authority_confirmed": None,
            "minutes_before_freeze": None,
            "change_feasible_before_freeze": None,
            "reason_codes": ["DECISION_REACHABILITY_UNVERIFIED"],
        }

    raw_surface = decision_reachability.get("decision_surface")
    decision_surface = (
        raw_surface.strip().upper()
        if isinstance(raw_surface, str)
        else ""
    )
    if not decision_surface:
        decision_surface = None

    surface_verified = _normalize_optional_bool(
        decision_reachability.get("decision_surface_verified")
    )
    authority_confirmed = _normalize_optional_bool(
        decision_reachability.get("operator_authority_confirmed")
    )
    minutes_before_freeze = _normalize_minutes_before_freeze(
        decision_reachability.get("minutes_before_freeze")
    )
    change_feasible_before_freeze = _normalize_optional_bool(
        decision_reachability.get("change_feasible_before_freeze")
    )

    reasons: list[str] = []
    hard_block = False

    if decision_surface is None:
        reasons.append("DECISION_SURFACE_UNSPECIFIED")
    if surface_verified is not True:
        reasons.append("DECISION_SURFACE_UNVERIFIED")

    if authority_confirmed is False:
        reasons.append("DECISION_AUTHORITY_DENIED")
        hard_block = True
    elif authority_confirmed is None:
        reasons.append("DECISION_AUTHORITY_UNKNOWN")

    if minutes_before_freeze is None:
        reasons.append("DECISION_FREEZE_TIME_UNKNOWN")
    elif minutes_before_freeze <= 0:
        reasons.append("DECISION_WINDOW_CLOSED")
        hard_block = True

    if change_feasible_before_freeze is False:
        reasons.append("DECISION_CHANGE_NOT_FEASIBLE_BEFORE_FREEZE")
        hard_block = True
    elif change_feasible_before_freeze is None:
        reasons.append("DECISION_CHANGE_FEASIBILITY_UNKNOWN")

    if hard_block:
        status = "UNREACHABLE"
    elif reasons:
        status = "UNVERIFIED"
    else:
        status = "REACHABLE"
        reasons.append("DECISION_REACHABLE_BEFORE_FREEZE")

    return {
        "status": status,
        "decision_surface": decision_surface,
        "decision_surface_verified": surface_verified,
        "operator_authority_confirmed": authority_confirmed,
        "minutes_before_freeze": minutes_before_freeze,
        "change_feasible_before_freeze": change_feasible_before_freeze,
        "reason_codes": reasons,
    }


def build_food_decision(
    predicted_demand: Any,
    signal_availability: Mapping[str, bool] | None = None,
    *,
    model_id: str = "food-demand-model",
    method_eligibility: str = "SANDBOX_ONLY",
    decision_reachability: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an operator-reviewed food-production decision contract.

    Signal weights and planning ranges are explicit policy heuristics. They are not
    probabilities or calibrated confidence intervals. Method eligibility is a hard
    readiness gate: generated/sandbox methods may be inspected but cannot produce
    an actionable pilot recommendation. Operational reachability is a separate gate:
    `PILOT_READY` requires a verified decision surface, confirmed operator authority,
    an open decision window, and confirmed ability to change the decision before
    freeze. Known non-reachability forces `WITHHOLD`.
    """

    normalized_eligibility, unknown_eligibility = _normalize_method_eligibility(
        method_eligibility
    )
    reachability = _assess_decision_reachability(decision_reachability)
    availability = {
        signal: bool((signal_availability or {}).get(signal, False))
        for signal in SIGNAL_WEIGHTS_PCT
    }
    demand = _normalize_demand(predicted_demand)
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
    lower = int(round(demand * lower_factor))
    upper = int(round(demand * upper_factor))

    reason_codes = ["HEURISTIC_BAND_NOT_CALIBRATED"]
    missing = [signal for signal, available in availability.items() if not available]
    reason_codes.extend(f"MISSING_{signal.upper()}" for signal in missing)
    if unknown_eligibility:
        reason_codes.append("UNKNOWN_METHOD_ELIGIBILITY_TREATED_AS_SANDBOX")

    required_missing = [signal for signal in REQUIRED_SIGNALS if not availability[signal]]
    if demand <= 0:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_POSITIVE_DEMAND_ESTIMATE")
    elif required_missing:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "MISSING_REQUIRED_SCHEDULE")
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

    reason_codes.extend(reachability["reason_codes"])
    if reachability["status"] == "UNREACHABLE":
        readiness = "WITHHOLD"
    elif reachability["status"] == "UNVERIFIED" and readiness == "PILOT_READY":
        readiness = "REVIEW_REQUIRED"

    abstained = readiness == "WITHHOLD"
    return {
        "policy_version": POLICY_VERSION,
        "reachability_policy_version": REACHABILITY_POLICY_VERSION,
        "model_id": model_id,
        "method_eligibility": normalized_eligibility,
        "forecast_provenance": FORECAST_PROVENANCE,
        "decision_provenance": DECISION_PROVENANCE,
        "band_semantics": BAND_SEMANTICS,
        "calibration_status": CALIBRATION_STATUS,
        "predicted_demand": demand,
        "planning_lower": lower,
        "recommended_production": None if abstained else demand,
        "planning_upper": upper,
        "signal_coverage_pct": coverage,
        "decision_readiness": readiness,
        "decision_reachability_status": reachability["status"],
        "decision_surface": reachability["decision_surface"],
        "decision_surface_verified": reachability["decision_surface_verified"],
        "operator_authority_confirmed": reachability["operator_authority_confirmed"],
        "minutes_before_freeze": reachability["minutes_before_freeze"],
        "change_feasible_before_freeze": reachability[
            "change_feasible_before_freeze"
        ],
        "abstained": abstained,
        "operator_approval_required": True,
        "automatic_kitchen_dispatch": False,
        "signals": signals,
        "reason_codes": reason_codes,
        "limitations": list(LIMITATIONS),
    }
