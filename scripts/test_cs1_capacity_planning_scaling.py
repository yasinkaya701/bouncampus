#!/usr/bin/env python3
"""Exactness/scaling regressions for CS1 shuttle and space capacity planning."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_planner():
    path = ROOT / "backend/app/decision/capacity_planning.py"
    if not path.exists():
        raise AssertionError("canonical capacity planning module missing")
    spec = importlib.util.spec_from_file_location("cs1_capacity_planning", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exhaustive(scenarios, options, *, idle_weight, shortage_weight, service_ratio, id_key):
    total_weight = sum(row["weight"] for row in scenarios)
    normalized = [(row["demand"], row["weight"] / total_weight) for row in scenarios]
    best = None
    for size in range(1, len(options) + 1):
        for subset in itertools.combinations(options, size):
            capacity = sum(row["capacity"] for row in subset)
            if any(capacity + 1e-9 < service_ratio * demand for demand, _ in normalized):
                continue
            activation = sum(row.get("activation_weight", 0.0) for row in subset)
            loss = activation + sum(
                probability
                * (
                    idle_weight * max(capacity - demand, 0.0)
                    + shortage_weight * max(demand - capacity, 0.0)
                )
                for demand, probability in normalized
            )
            ids = tuple(sorted(row[id_key] for row in subset))
            ranked = (loss, capacity, ids)
            if best is None or ranked < best:
                best = ranked
    return best


def test_shuttle_matches_exhaustive_small_random_cases() -> None:
    planner = load_planner()
    random.seed(701)
    for _ in range(80):
        option_count = random.randint(1, 8)
        options = [
            {
                "departure_id": f"D{i}",
                "capacity": random.randint(5, 30),
                "activation_weight": random.randint(0, 6) / 2,
            }
            for i in range(option_count)
        ]
        scenarios = [
            {"demand": random.randint(5, 100), "weight": random.randint(1, 5)}
            for _ in range(random.randint(1, 4))
        ]
        empty = random.randint(0, 5) / 2
        shortage = random.randint(0, 8) / 2
        service = random.choice([0.5, 0.75, 0.9, 1.0])
        expected = exhaustive(
            scenarios,
            options,
            idle_weight=empty,
            shortage_weight=shortage,
            service_ratio=service,
            id_key="departure_id",
        )
        result = planner.optimize_shuttle_plan(
            demand_scenarios=scenarios,
            departure_options=options,
            empty_seat_weight=empty,
            shortage_weight=shortage,
            min_point_service_ratio=service,
        )
        if expected is None:
            assert result["decision_readiness"] == "WITHHOLD"
            continue
        assert result["decision_readiness"] == "REVIEW_REQUIRED"
        assert tuple(result["selected_departure_ids"]) == expected[2]
        assert math.isclose(result["expected_registered_loss"], expected[0], abs_tol=1e-9)


def test_space_matches_exhaustive_fractional_capacity_case() -> None:
    planner = load_planner()
    options = [
        {"zone_id": "A", "capacity": 12.5, "activation_weight": 1.0},
        {"zone_id": "B", "capacity": 17.5, "activation_weight": 1.5},
        {"zone_id": "C", "capacity": 25.0, "activation_weight": 2.0},
        {"zone_id": "D", "capacity": 30.0, "activation_weight": 2.5},
    ]
    scenarios = [{"demand": 30, "weight": 0.4}, {"demand": 50, "weight": 0.6}]
    expected = exhaustive(
        scenarios,
        options,
        idle_weight=0.5,
        shortage_weight=3.0,
        service_ratio=0.8,
        id_key="zone_id",
    )
    result = planner.optimize_space_plan(
        occupancy_scenarios=scenarios,
        zones=options,
        idle_capacity_weight=0.5,
        shortage_weight=3.0,
        min_point_service_ratio=0.8,
    )
    assert expected is not None
    assert tuple(result["selected_zone_ids"]) == expected[2]
    assert math.isclose(result["expected_registered_loss"], expected[0], abs_tol=1e-9)


def test_float_noise_uses_policy_tie_break_not_binary_rounding() -> None:
    planner = load_planner()
    result = planner.optimize_shuttle_plan(
        demand_scenarios=[{"demand": 25, "weight": 1.0}],
        departure_options=[
            {"departure_id": "D0", "capacity": 4.4, "activation_weight": 1.5},
            {"departure_id": "D1", "capacity": 6.5, "activation_weight": 2.0},
            {"departure_id": "D2", "capacity": 7.2, "activation_weight": 2.0},
            {"departure_id": "D3", "capacity": 0.3, "activation_weight": 0.3},
            {"departure_id": "D4", "capacity": 13.0, "activation_weight": 2.0},
        ],
        empty_seat_weight=0.0,
        shortage_weight=2.0,
        min_point_service_ratio=0.5,
    )
    # Both 24.9 and 26.7 have registered loss 6.0 mathematically. The policy
    # tie-break is lower capacity, then lexicographic IDs; binary float noise must
    # not flip that deterministic choice.
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_capacity_exact"] == 24.9
    assert result["selected_departure_ids"] == ["D0", "D2", "D3", "D4"]
    assert math.isclose(result["expected_registered_loss"], 6.0, abs_tol=1e-9)


def test_forty_shuttle_options_are_supported_exactly() -> None:
    planner = load_planner()
    options = [
        {"departure_id": f"D{i:02d}", "capacity": 10, "activation_weight": 0.1}
        for i in range(40)
    ]
    result = planner.optimize_shuttle_plan(
        demand_scenarios=[{"demand": 250, "weight": 1.0}],
        departure_options=options,
        empty_seat_weight=1.0,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert len(result["selected_departure_ids"]) == 25
    assert result["selected_capacity"] == 250
    assert result["solver_semantics"] == "EXACT_SPARSE_FIXED_DECIMAL_CAPACITY_DP"


def test_thirty_space_options_are_supported_exactly() -> None:
    planner = load_planner()
    zones = [
        {"zone_id": f"Z{i:02d}", "capacity": 100, "activation_weight": 1.0}
        for i in range(30)
    ]
    result = planner.optimize_space_plan(
        occupancy_scenarios=[{"demand": 1700, "weight": 1.0}],
        zones=zones,
        idle_capacity_weight=1.0,
        shortage_weight=3.0,
        min_point_service_ratio=0.9,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_capacity"] == 1700
    assert len(result["selected_zone_ids"]) == 17
    assert result["solver_semantics"] == "EXACT_SPARSE_FIXED_DECIMAL_CAPACITY_DP"
    assert result["energy_savings_claim_allowed"] is False


def test_api_and_orchestrator_route_to_scalable_capacity_planner() -> None:
    expected = (
        "from app.decision.capacity_planning import optimize_shuttle_plan, optimize_space_plan"
    )
    router = (ROOT / "backend/app/routers/campus_ops.py").read_text(encoding="utf-8")
    orchestrator = (
        ROOT / "backend/app/decision/campus_orchestrator.py"
    ).read_text(encoding="utf-8")
    assert expected in router
    assert expected in orchestrator


def main() -> int:
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
        print(f"PASS {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
