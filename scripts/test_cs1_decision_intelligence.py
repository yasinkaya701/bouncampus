#!/usr/bin/env python3
"""Regression tests for CS1 Decision Intelligence v1.

These tests intentionally exercise decision integrity rather than model accuracy:
readiness/abstention, provenance, naive baselines, evaluation metrics, and the
pre-pilot claim firewall.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERIFIED_REACHABILITY = {
    "decision_surface": "PRODUCTION_QUANTITY",
    "decision_surface_verified": True,
    "operator_authority_confirmed": True,
    "minutes_before_freeze": 90,
    "change_feasible_before_freeze": True,
}


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_policy_metadata_and_full_context() -> None:
    policy = load_module("food_policy", "backend/app/decision/food_policy.py")
    decision = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        model_id="measured-food-method-v1",
        method_eligibility="PILOT_ELIGIBLE",
        decision_reachability=VERIFIED_REACHABILITY,
    )
    assert decision["policy_version"] == policy.POLICY_VERSION
    assert decision["method_eligibility"] == "PILOT_ELIGIBLE"
    assert decision["forecast_provenance"] == "MODEL_ESTIMATE"
    assert decision["decision_provenance"] == "POLICY_HEURISTIC"
    assert decision["band_semantics"] == "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
    assert decision["calibration_status"] == "NOT_CALIBRATED"
    assert decision["signal_coverage_pct"] == 100
    assert decision["decision_reachability_status"] == "REACHABLE"
    assert decision["decision_surface_verified"] is True
    assert decision["change_feasible_before_freeze"] is True
    assert decision["decision_readiness"] == "PILOT_READY"
    assert decision["abstained"] is False
    assert decision["recommended_production"] == 1000
    assert decision["planning_lower"] == 960
    assert decision["planning_upper"] == 1060
    assert decision["operator_approval_required"] is True
    assert decision["automatic_kitchen_dispatch"] is False
    assert "HEURISTIC_BAND_NOT_CALIBRATED" in decision["reason_codes"]
    assert "DECISION_REACHABLE_BEFORE_FREEZE" in decision["reason_codes"]
    assert "PILOT_OUTCOMES_NOT_YET_MEASURED" in decision["limitations"]


def test_policy_degrades_and_abstains() -> None:
    policy = load_module("food_policy_degraded", "backend/app/decision/food_policy.py")
    review = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": False, "menu": False, "calendar": False},
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert review["signal_coverage_pct"] == 50
    assert review["decision_readiness"] == "REVIEW_REQUIRED"
    assert review["abstained"] is False
    assert review["recommended_production"] == 1000
    assert "CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED" in review["reason_codes"]

    withheld = policy.build_food_decision(
        1000,
        {"schedule": False, "weather": True, "menu": True, "calendar": True},
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert withheld["decision_readiness"] == "WITHHOLD"
    assert withheld["abstained"] is True
    assert withheld["recommended_production"] is None
    assert "MISSING_REQUIRED_SCHEDULE" in withheld["reason_codes"]


def test_policy_handles_invalid_demand_without_action() -> None:
    policy = load_module("food_policy_invalid", "backend/app/decision/food_policy.py")
    for value in (float("nan"), float("inf"), -50, 0):
        decision = policy.build_food_decision(
            value,
            {"schedule": True, "weather": True, "menu": True, "calendar": True},
            method_eligibility="PILOT_ELIGIBLE",
        )
        assert decision["predicted_demand"] == 0
        assert decision["decision_readiness"] == "WITHHOLD"
        assert decision["abstained"] is True
        assert decision["recommended_production"] is None
        assert "NO_POSITIVE_DEMAND_ESTIMATE" in decision["reason_codes"]


def test_signal_weights_are_explicit_policy_not_confidence() -> None:
    policy = load_module("food_policy_weights", "backend/app/decision/food_policy.py")
    assert sum(policy.SIGNAL_WEIGHTS_PCT.values()) == 100
    assert policy.REQUIRED_SIGNALS == ("schedule",)
    assert policy.PILOT_READY_MIN_COVERAGE_PCT == 70
    assert policy.REVIEW_MIN_COVERAGE_PCT == 50
    assert "SANDBOX_ONLY" in policy.METHOD_ELIGIBILITY_STATES
    assert "PILOT_ELIGIBLE" in policy.METHOD_ELIGIBILITY_STATES
    assert policy.REACHABILITY_POLICY_VERSION == "decision-reachability-v1.1"


def test_naive_baselines_do_not_use_future_values() -> None:
    baselines = load_module("food_baselines", "backend/app/decision/baselines.py")
    values = [100.0, 120.0, 110.0, 140.0]
    generated = baselines.generate_naive_baselines(values, rolling_window=2, seasonal_lag=2)
    assert generated["previous_service"] == [None, 100.0, 120.0, 110.0]
    assert generated["expanding_mean"] == [None, 100.0, 110.0, 110.0]
    assert generated["rolling_mean_2"] == [None, 100.0, 110.0, 115.0]
    assert generated["seasonal_lag_2"] == [None, None, 100.0, 120.0]


def test_forecast_metrics_and_ranking() -> None:
    baselines = load_module("food_baseline_metrics", "backend/app/decision/baselines.py")
    metrics = baselines.evaluate_predictions(
        [100.0, 120.0, 110.0],
        [90.0, 130.0, 110.0],
    )
    assert metrics["n"] == 3
    assert math.isclose(metrics["mae"], 20 / 3, rel_tol=1e-9)
    assert math.isclose(metrics["rmse"], math.sqrt(200 / 3), rel_tol=1e-9)
    assert math.isclose(metrics["wape_pct"], (20 / 330) * 100, rel_tol=1e-9)
    assert math.isclose(metrics["mean_error"], 0.0, abs_tol=1e-12)

    report = baselines.compare_forecasts(
        [100.0, 120.0, 110.0],
        {
            "strong": [100.0, 118.0, 112.0],
            "weak": [80.0, 90.0, 95.0],
        },
    )
    assert report["ranking_by_mae"][0] == "strong"
    assert report["metrics"]["strong"]["mae"] < report["metrics"]["weak"]["mae"]
    assert report["common_support_n"] == 3
    assert report["common_support_pct"] == 100.0


def test_metrics_reject_misaligned_inputs() -> None:
    baselines = load_module("food_baseline_alignment", "backend/app/decision/baselines.py")
    try:
        baselines.evaluate_predictions([1.0, 2.0], [1.0])
    except ValueError as exc:
        assert "same length" in str(exc)
    else:
        raise AssertionError("misaligned actual/predicted arrays must be rejected")

    try:
        baselines.compare_forecasts([1.0, 2.0], {"bad": [1.0]})
    except ValueError as exc:
        assert "same length" in str(exc)
    else:
        raise AssertionError("misaligned benchmark candidates must be rejected")


def test_backend_food_claim_firewall() -> None:
    food_route = (ROOT / "backend/app/routers/food.py").read_text(encoding="utf-8")
    dashboard_route = (ROOT / "backend/app/routers/dashboard.py").read_text(encoding="utf-8")
    actions_route = (ROOT / "backend/app/routers/actions.py").read_text(encoding="utf-8")
    optimizer = (ROOT / "backend/app/optimizers/food_optimizer.py").read_text(encoding="utf-8")
    schemas = (ROOT / "backend/app/schemas.py").read_text(encoding="utf-8")
    food_schema = schemas.split("class FoodDemandForecast", 1)[1].split("class ActionItem", 1)[0]

    forbidden = {"potential_waste_saved_kg", "waste_reduction", "cost_saved_tl"}
    for term in forbidden:
        assert term not in food_route, f"unsupported pre-pilot claim leaked into food route: {term}"
        assert term not in optimizer, f"unsupported pre-pilot claim leaked into food optimizer: {term}"
        assert term not in food_schema, f"unsupported pre-pilot claim leaked into food schema: {term}"

    for term in ("food_waste_saved_kg", "food_waste_avoided_kg=40.0", "base_meals * 1.15"):
        assert term not in dashboard_route, f"legacy food-impact claim leaked into dashboard: {term}"
    for term in ("Pre-portion 1,420", "impact_value=48.0", 'impact_unit="kg"'):
        assert term not in actions_route, f"legacy food-impact claim leaked into actions route: {term}"

    assert "food_waste_avoided_kg=None" in dashboard_route
    assert 'food_waste_impact_status="UNMEASURED"' in dashboard_route
    assert "automatic kitchen dispatch" in dashboard_route.lower()
    assert "automatic kitchen dispatch" in actions_route.lower()
    assert "provenance=" in dashboard_route
    assert "provenance=" in actions_route
    assert 'METHOD_ELIGIBILITY = "SANDBOX_ONLY"' in (ROOT / "backend/app/models/food_demand.py").read_text(encoding="utf-8")
    assert "method_eligibility=method_eligibility" in food_route


def test_frontend_contract_is_explicit() -> None:
    library = (ROOT / "frontend/src/lib/food-waste.ts").read_text(encoding="utf-8")
    eligibility = (ROOT / "frontend/src/lib/food-decision-eligibility.ts").read_text(encoding="utf-8")
    route = (ROOT / "frontend/src/app/api/v1/food/route.ts").read_text(encoding="utf-8")
    for marker in (
        "policyVersion",
        "POLICY_HEURISTIC",
        "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL",
        "NOT_CALIBRATED",
        "operatorApprovalRequired",
        "autoDispatchAllowed",
        "abstained",
    ):
        assert marker in library, f"frontend decision contract missing {marker}"
    for marker in ("MethodEligibility", "SANDBOX_ONLY", "METHOD_SANDBOX_ONLY"):
        assert marker in eligibility, f"frontend eligibility contract missing {marker}"
    for marker in (
        "forbiddenUntilMeasured",
        "humanApprovalRequired",
        "automaticKitchenDispatch",
        "decisionAssessment",
        "READY_FOR_MEASURED_DATA",
        "methodEligibility: 'SANDBOX_ONLY'",
    ):
        assert marker in route, f"food API truth boundary missing {marker}"


def test_registered_ui_preserves_provenance_boundary() -> None:
    food_page = (ROOT / "frontend/src/app/food-waste/page.tsx").read_text(encoding="utf-8")
    jury_page = (ROOT / "frontend/src/app/demo/jury/page.tsx").read_text(encoding="utf-8")

    for marker in ("MODEL_ESTIMATE", "POLICY_HEURISTIC", "NOT_CALIBRATED"):
        assert marker in food_page, f"food-waste UI missing provenance marker {marker}"
        assert marker in jury_page, f"jury UI missing provenance marker {marker}"

    assert "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL" in food_page
    assert "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL" in jury_page
    assert "<strong>MODEL_ESTIMATE.</strong>" not in food_page
    assert jury_page.count('tag="MODEL_ESTIMATE"') == 1, "only the point forecast may be tagged MODEL_ESTIMATE"
    assert jury_page.count('tag="POLICY_HEURISTIC"') == 3, "planning bounds/target must be policy heuristics"
    assert "AUTO_DISPATCH=false" in jury_page


def test_kreate_checker_enforces_food_decision_integrity() -> None:
    checker = (ROOT / "scripts/kreate_check.py").read_text(encoding="utf-8")
    assert "check_food_decision_integrity" in checker
    assert "POLICY_HEURISTIC" in checker
    assert "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL" in checker
    assert "backend/app/routers/dashboard.py" in checker
    assert "backend/app/routers/actions.py" in checker


def main() -> int:
    tests = [
        test_policy_metadata_and_full_context,
        test_policy_degrades_and_abstains,
        test_policy_handles_invalid_demand_without_action,
        test_signal_weights_are_explicit_policy_not_confidence,
        test_naive_baselines_do_not_use_future_values,
        test_forecast_metrics_and_ranking,
        test_metrics_reject_misaligned_inputs,
        test_backend_food_claim_firewall,
        test_frontend_contract_is_explicit,
        test_registered_ui_preserves_provenance_boundary,
        test_kreate_checker_enforces_food_decision_integrity,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
