#!/usr/bin/env python3
"""Focused regression tests for CS1 cafeteria production planning."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_food_policy():
    path = ROOT / "backend/app/decision/food_ops_policy.py"
    if not path.exists():
        raise AssertionError("food-ops policy missing")
    spec = importlib.util.spec_from_file_location("cs1_food_ops_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plan(policy, **overrides):
    kwargs = {
        "demand_scenarios": [
            {"demand": 90, "weight": 0.25},
            {"demand": 100, "weight": 0.50},
            {"demand": 120, "weight": 0.25},
        ],
        "max_capacity": 130,
        "capacity_provenance": "OFFICIAL_SNAPSHOT",
        "waste_weight": 1.0,
        "shortage_weight": 3.0,
        "method_eligibility": "PILOT_ELIGIBLE",
    }
    kwargs.update(overrides)
    return policy.plan_food_production(**kwargs)


def test_registered_asymmetric_loss_selects_operator_review_target() -> None:
    policy = load_food_policy()
    result = plan(policy)
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended_production"] == 100
    assert result["max_capacity"] == 130
    assert result["capacity_provenance"] == "OFFICIAL_SNAPSHOT"
    assert result["objective_units"] == "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True
    assert result["reservation_semantics"] == "INTENT_SIGNAL_NOT_SERVED_DEMAND"


def test_unverified_capacity_fails_closed() -> None:
    policy = load_food_policy()
    for provenance in ("MODEL_ESTIMATE", "POLICY_HEURISTIC", "UNAVAILABLE"):
        result = plan(policy, capacity_provenance=provenance)
        assert result["decision_readiness"] == "WITHHOLD"
        assert result["recommended_production"] is None
        assert result["capacity_provenance"] == provenance
        assert "UNVERIFIED_FOOD_CAPACITY" in result["reason_codes"]


def test_unusable_scenarios_fail_closed() -> None:
    policy = load_food_policy()
    result = plan(
        policy,
        demand_scenarios=[{"demand": float("nan"), "weight": 1.0}],
        max_capacity=100,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended_production"] is None
    assert "INVALID_OR_UNUSABLE_DEMAND_SCENARIOS" in result["reason_codes"]


def test_zero_loss_weights_fail_closed_instead_of_inventing_zero_production() -> None:
    policy = load_food_policy()
    result = plan(
        policy,
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        waste_weight=0.0,
        shortage_weight=0.0,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended_production"] is None
    assert "NON_IDENTIFYING_FOOD_OBJECTIVE" in result["reason_codes"]


def test_sandbox_method_cannot_become_actionable_target() -> None:
    policy = load_food_policy()
    result = plan(
        policy,
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        method_eligibility="SANDBOX_ONLY",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended_production"] is None
    assert "METHOD_NOT_ACTIONABLE" in result["reason_codes"]


def test_upstream_withhold_propagates_without_inventing_food_target() -> None:
    policy = load_food_policy()
    result = plan(
        policy,
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        upstream_readiness="WITHHOLD",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended_production"] is None
    assert "UPSTREAM_CAMPUS_STATE_WITHHELD" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} food-ops policy tests")
