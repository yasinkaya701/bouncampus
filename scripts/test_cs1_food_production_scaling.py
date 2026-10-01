#!/usr/bin/env python3
"""Regression gates for scalable/fail-closed CS1 food production optimization."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_optimizer():
    path = ROOT / "backend/app/decision/food_production.py"
    spec = importlib.util.spec_from_file_location("cs1_food_production", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_force(scenarios, capacity, waste_weight, shortage_weight):
    total = sum(row["weight"] for row in scenarios)
    rows = [(row["demand"], row["weight"] / total) for row in scenarios]

    def loss(quantity: int) -> float:
        return sum(
            probability
            * (
                waste_weight * max(quantity - demand, 0.0)
                + shortage_weight * max(demand - quantity, 0.0)
            )
            for demand, probability in rows
        )

    return min((loss(quantity), quantity) for quantity in range(capacity + 1))


def test_breakpoint_search_matches_integer_bruteforce() -> None:
    optimizer = load_optimizer()
    cases = [
        (
            [
                {"demand": 90, "weight": 0.25},
                {"demand": 100, "weight": 0.50},
                {"demand": 120, "weight": 0.25},
            ],
            130,
            1.0,
            3.0,
        ),
        (
            [{"demand": 3.2, "weight": 0.4}, {"demand": 8.8, "weight": 0.6}],
            10,
            2.0,
            1.0,
        ),
        (
            [{"demand": 2, "weight": 1.0}, {"demand": 9, "weight": 1.0}],
            7,
            1.0,
            1.0,
        ),
    ]
    for scenarios, capacity, waste, shortage in cases:
        expected_loss, expected_quantity = brute_force(
            scenarios, capacity, waste, shortage
        )
        result = optimizer.optimize_food_production(
            demand_scenarios=scenarios,
            max_capacity=capacity,
            waste_weight=waste,
            shortage_weight=shortage,
            method_eligibility="PILOT_ELIGIBLE",
        )
        assert result["recommended_production"] == expected_quantity
        assert math.isclose(
            result["expected_registered_loss"],
            expected_loss,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_large_capacity_does_not_expand_search_space() -> None:
    optimizer = load_optimizer()
    result = optimizer.optimize_food_production(
        demand_scenarios=[
            {"demand": 100, "weight": 0.7},
            {"demand": 140, "weight": 0.3},
        ],
        max_capacity=1_000_000_000,
        waste_weight=1.0,
        shortage_weight=4.0,
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert result["recommended_production"] == 140
    assert result["search_candidate_count"] <= 6
    assert result["max_capacity"] == 1_000_000_000
    assert (
        result["optimization_semantics"]
        == "EXACT_INTEGER_BREAKPOINT_SEARCH_PIECEWISE_LINEAR_LOSS"
    )


def test_unknown_method_fails_closed_but_keeps_analysis_candidate() -> None:
    optimizer = load_optimizer()
    result = optimizer.optimize_food_production(
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        waste_weight=1.0,
        shortage_weight=2.0,
        method_eligibility="MAGIC_READY",
    )
    assert result["candidate_production"] == 100
    assert result["recommended_production"] is None
    assert result["decision_readiness"] == "WITHHOLD"
    assert "UNKNOWN_METHOD_ELIGIBILITY" in result["reason_codes"]


def test_offline_method_cannot_emit_operator_recommendation() -> None:
    optimizer = load_optimizer()
    result = optimizer.optimize_food_production(
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        waste_weight=1.0,
        shortage_weight=2.0,
        method_eligibility="EVALUATED_OFFLINE",
    )
    assert result["candidate_production"] == 100
    assert result["recommended_production"] is None
    assert result["decision_readiness"] == "WITHHOLD"
    assert "METHOD_NOT_PILOT_ELIGIBLE" in result["reason_codes"]


def test_zero_objective_weights_are_not_actionable() -> None:
    optimizer = load_optimizer()
    result = optimizer.optimize_food_production(
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        max_capacity=120,
        waste_weight=0.0,
        shortage_weight=0.0,
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert result["candidate_production"] is None
    assert result["recommended_production"] is None
    assert result["decision_readiness"] == "WITHHOLD"


def main() -> int:
    tests = [
        test_breakpoint_search_matches_integer_bruteforce,
        test_large_capacity_does_not_expand_search_space,
        test_unknown_method_fails_closed_but_keeps_analysis_candidate,
        test_offline_method_cannot_emit_operator_recommendation,
        test_zero_objective_weights_are_not_actionable,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
