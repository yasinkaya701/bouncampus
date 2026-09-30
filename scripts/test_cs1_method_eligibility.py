#!/usr/bin/env python3
"""Regression tests for CS1 method eligibility and fair baseline comparison."""

from __future__ import annotations

import importlib.util
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


def test_sandbox_method_can_never_be_pilot_ready() -> None:
    policy = load_module("food_policy_eligibility", "backend/app/decision/food_policy.py")
    decision = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        model_id="food-demand-xgboost",
        method_eligibility="SANDBOX_ONLY",
    )
    assert decision["method_eligibility"] == "SANDBOX_ONLY"
    assert decision["decision_readiness"] == "WITHHOLD"
    assert decision["abstained"] is True
    assert decision["recommended_production"] is None
    assert "METHOD_SANDBOX_ONLY" in decision["reason_codes"]


def test_pilot_eligible_method_may_be_pilot_ready_with_healthy_context() -> None:
    policy = load_module("food_policy_pilot_eligibility", "backend/app/decision/food_policy.py")
    decision = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        model_id="measured-baseline-v1",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["decision_readiness"] == "PILOT_READY"
    assert decision["abstained"] is False
    assert decision["recommended_production"] == 1000


def test_offline_only_method_requires_review_not_pilot_ready() -> None:
    policy = load_module("food_policy_offline_eligibility", "backend/app/decision/food_policy.py")
    decision = policy.build_food_decision(
        1000,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        model_id="offline-candidate-v1",
        method_eligibility="EVALUATED_OFFLINE",
    )
    assert decision["decision_readiness"] == "REVIEW_REQUIRED"
    assert decision["abstained"] is False
    assert "METHOD_NOT_YET_PILOT_ELIGIBLE" in decision["reason_codes"]


def test_forecast_ranking_uses_identical_common_support() -> None:
    baselines = load_module("food_baselines_common_support", "backend/app/decision/baselines.py")
    report = baselines.compare_forecasts(
        [100.0, 110.0, 120.0, 130.0],
        {
            "complete": [105.0, 115.0, 125.0, 135.0],
            "sparse": [100.0, None, 120.0, None],
        },
    )
    assert report["common_support_n"] == 2
    assert report["common_support_pct"] == 50.0
    assert report["metrics"]["complete"]["n"] == 2
    assert report["metrics"]["sparse"]["n"] == 2
    assert report["evaluation_indices"] == [0, 2]


def test_frontend_contract_blocks_sandbox_pilot_readiness() -> None:
    library = (ROOT / "frontend/src/lib/food-waste.ts").read_text(encoding="utf-8")
    route = (ROOT / "frontend/src/app/api/v1/food/route.ts").read_text(encoding="utf-8")
    for marker in ("MethodEligibility", "methodEligibility", "SANDBOX_ONLY", "METHOD_SANDBOX_ONLY"):
        assert marker in library, f"frontend decision contract missing method-eligibility marker {marker}"
    assert "methodEligibility: 'SANDBOX_ONLY'" in route


def main() -> int:
    tests = [
        test_sandbox_method_can_never_be_pilot_ready,
        test_pilot_eligible_method_may_be_pilot_ready_with_healthy_context,
        test_offline_only_method_requires_review_not_pilot_ready,
        test_forecast_ranking_uses_identical_common_support,
        test_frontend_contract_blocks_sandbox_pilot_readiness,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
