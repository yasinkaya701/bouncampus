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
        model_id="food-demand-xgboost",
    )
    assert decision["policy_version"] == policy.POLICY_VERSION
    assert decision["forecast_provenance"] == "MODEL_ESTIMATE"
    assert decision["decision_provenance"] == "POLICY_HEURISTIC"
    assert decision["band_semantics"] == "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
    assert decision["calibration_status"] == "NOT_CALIBRATED"
    assert decision["signal_coverage_pct"] == 100
    assert decision["decision_readiness"] == "PILOT_READY"
    assert decision["abstained"] is False
    assert decision["recommended_production"] == 1000
    assert decision["planning_lower"] == 960
    assert decision["planning_upper"] == 1060
    assert decision["operator_approval_required"] is True
    assert decision["automatic_kitchen_dispatch"] is False
    assert "HEURISTIC_BAND_NOT_CALIBRATED" in decision["reason_codes"]
    assert "PILOT_OUTCOMES_NOT_YET_MEASURED" in decision["limitations"]


def test_policy_degrades_and_abstains() -> None:
    policy = load_module("food_policy_degraded", "backend/app/decision/food_policy.py")
    review = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": False, "menu": False, "calendar": False},
    )
    assert review["signal_coverage_pct"] == 50
    assert review["decision_readiness"] == "REVIEW_REQUIRED"
    assert review["abstained"] is False
    assert review["recommended_production"] == 1000
    assert "CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED" in review["reason_codes"]

    withheld = policy.build_food_decision(
        1000,
        {"schedule": False, "weather": True, "menu": True, "calendar": True},
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


def test_metrics_reject_misaligned_inputs() -> None:
    baselines = load_module("food_baseline_alignment", "backend/app/decision/baselines.py")
    try:
        baselines.evaluate_predictions([1.0, 2.0], [1.0])
    except ValueError as exc:
        assert "same length" in str(exc)
    else:
        raise AssertionError("misaligned actual/predicted arrays must be rejected")


def test_backend_food_claim_firewall() -> None:
    router = (ROOT / "backend/app/routers/food.py").read_text(encoding="utf-8")
    optimizer = (ROOT / "backend/app/optimizers/food_optimizer.py").read_text(encoding="utf-8")
    schemas = (ROOT / "backend/app/schemas.py").read_text(encoding="utf-8")
    food_schema = schemas.split("class FoodDemandForecast", 1)[1].split("class ActionItem", 1)[0]

    forbidden = ("potential_waste_saved_kg", "waste_reduction", "cost_saved_tl")
    for term in forbidden:
        assert term not in router, f"unsupported pre-pilot claim leaked into food route: {term}"
        assert term not in optimizer, f"unsupported pre-pilot claim leaked into food optimizer: {term}"
        assert term not in food_schema, f"unsupported pre-pilot claim leaked into food schema: {term}"


def test_frontend_contract_is_explicit() -> None:
    library = (ROOT / "frontend/src/lib/food-waste.ts").read_text(encoding="utf-8")
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
    for marker in ("forbiddenUntilMeasured", "humanApprovalRequired", "automaticKitchenDispatch"):
        assert marker in route, f"food API truth boundary missing {marker}"


def test_kreate_checker_enforces_food_decision_integrity() -> None:
    checker = (ROOT / "scripts/kreate_check.py").read_text(encoding="utf-8")
    assert "check_food_decision_integrity" in checker
    assert "POLICY_HEURISTIC" in checker
    assert "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL" in checker


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
        test_kreate_checker_enforces_food_decision_integrity,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
