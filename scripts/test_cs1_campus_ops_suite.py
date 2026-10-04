#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_ops():
    path = ROOT / "backend/app/decision/campus_ops.py"
    if not path.exists():
        raise AssertionError("campus-ops decision suite missing")
    spec = importlib.util.spec_from_file_location("cs1_campus_ops", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_food_uses_registered_scenarios_and_asymmetric_loss() -> None:
    ops = load_ops()
    result = ops.optimize_food_production(
        demand_scenarios=[
            {"demand": 90, "weight": 0.25},
            {"demand": 100, "weight": 0.50},
            {"demand": 120, "weight": 0.25},
        ],
        max_capacity=130,
        waste_weight=1.0,
        shortage_weight=3.0,
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended_production"] == 100
    assert result["automatic_dispatch"] is False
    assert result["objective_units"] == "REGISTERED_RELATIVE_SENSITIVITY_UNITS"


def test_food_withholds_on_unusable_scenarios() -> None:
    ops = load_ops()
    result = ops.optimize_food_production(
        demand_scenarios=[{"demand": float("nan"), "weight": 1.0}],
        max_capacity=100,
        waste_weight=1.0,
        shortage_weight=1.0,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended_production"] is None


def test_shuttle_selects_capacity_bundle_with_lowest_registered_loss() -> None:
    ops = load_ops()
    result = ops.optimize_shuttle_plan(
        demand_scenarios=[
            {"demand": 70, "weight": 0.25},
            {"demand": 90, "weight": 0.50},
            {"demand": 110, "weight": 0.25},
        ],
        departure_options=[
            {"departure_id": "A", "capacity": 50, "activation_weight": 1.0},
            {"departure_id": "B", "capacity": 60, "activation_weight": 1.0},
            {"departure_id": "C", "capacity": 40, "activation_weight": 1.0},
        ],
        empty_seat_weight=1.0,
        shortage_weight=5.0,
        min_point_service_ratio=0.9,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_departure_ids"] == ["A", "B"]
    assert result["selected_capacity"] == 110
    assert result["automatic_dispatch"] is False


def test_shuttle_withholds_if_even_full_fleet_misses_service_floor() -> None:
    ops = load_ops()
    result = ops.optimize_shuttle_plan(
        demand_scenarios=[{"demand": 100, "weight": 1.0}],
        departure_options=[
            {"departure_id": "A", "capacity": 50, "activation_weight": 1.0}
        ],
        empty_seat_weight=1.0,
        shortage_weight=5.0,
        min_point_service_ratio=0.8,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert "FLEET_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR" in result["reason_codes"]


def test_space_plan_selects_low_loss_zone_bundle() -> None:
    ops = load_ops()
    result = ops.optimize_space_plan(
        occupancy_scenarios=[
            {"demand": 60, "weight": 0.25},
            {"demand": 80, "weight": 0.50},
            {"demand": 100, "weight": 0.25},
        ],
        zones=[
            {"zone_id": "L1", "capacity": 60, "activation_weight": 2.0},
            {"zone_id": "L2", "capacity": 50, "activation_weight": 1.0},
            {"zone_id": "L3", "capacity": 40, "activation_weight": 0.5},
        ],
        idle_capacity_weight=0.5,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_zone_ids"] == ["L1", "L3"]
    assert result["selected_capacity"] == 100
    assert result["automatic_actuation"] is False
    assert result["energy_savings_claim_allowed"] is False


def test_space_plan_withholds_when_full_capacity_cannot_meet_floor() -> None:
    ops = load_ops()
    result = ops.optimize_space_plan(
        occupancy_scenarios=[{"demand": 120, "weight": 1.0}],
        zones=[{"zone_id": "L1", "capacity": 80, "activation_weight": 1.0}],
        idle_capacity_weight=1.0,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["selected_zone_ids"] == []
    assert "SPACE_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR" in result["reason_codes"]


def test_class_scheduler_assigns_rooms_and_slots_without_collisions() -> None:
    ops = load_ops()
    result = ops.optimize_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 80,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
            },
            {
                "class_id": "C2",
                "planning_attendance": 30,
                "allowed_slots": ["T1", "T2"],
                "required_features": ["lab"],
            },
        ],
        rooms=[
            {
                "room_id": "R1",
                "capacity": 100,
                "features": ["projector"],
                "building": "A",
            },
            {
                "room_id": "R2",
                "capacity": 40,
                "features": ["projector", "lab"],
                "building": "B",
            },
        ],
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert len(result["assignments"]) == 2
    keys = {(x["slot"], x["room_id"]) for x in result["assignments"]}
    assert len(keys) == 2
    assert {x["class_id"] for x in result["assignments"]} == {"C1", "C2"}


def test_class_scheduler_withholds_if_feature_constraints_are_infeasible() -> None:
    ops = load_ops()
    result = ops.optimize_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": ["wet_lab"],
            }
        ],
        rooms=[
            {
                "room_id": "R1",
                "capacity": 50,
                "features": ["projector"],
                "building": "A",
            }
        ],
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["assignments"] == []


def test_shared_capacity_respects_minimums_and_priority() -> None:
    ops = load_ops()
    result = ops.allocate_shared_capacity(
        total_capacity=10,
        requests=[
            {
                "request_id": "study",
                "minimum": 2,
                "desired": 7,
                "priority_weight": 3,
            },
            {
                "request_id": "charging",
                "minimum": 1,
                "desired": 5,
                "priority_weight": 1,
            },
        ],
    )
    allocations = {row["request_id"]: row["allocated"] for row in result["allocations"]}
    assert sum(allocations.values()) == 10
    assert allocations["study"] >= allocations["charging"]
    assert allocations["study"] >= 2
    assert allocations["charging"] >= 1


def test_shared_capacity_withholds_when_minimums_exceed_capacity() -> None:
    ops = load_ops()
    result = ops.allocate_shared_capacity(
        total_capacity=4,
        requests=[
            {"request_id": "a", "minimum": 3, "desired": 3, "priority_weight": 1},
            {"request_id": "b", "minimum": 2, "desired": 2, "priority_weight": 1},
        ],
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["allocations"] == []


def test_bundle_propagates_most_conservative_readiness() -> None:
    ops = load_ops()
    bundle = ops.build_campus_ops_bundle(
        {
            "food": {"decision_readiness": "REVIEW_REQUIRED"},
            "shuttle": {"decision_readiness": "WITHHOLD"},
            "rooms": {"decision_readiness": "PILOT_READY"},
        }
    )
    assert bundle["decision_readiness"] == "WITHHOLD"
    assert bundle["operator_approval_required"] is True
    assert bundle["automatic_actuation"] is False


def main() -> int:
    tests = [
        test_food_uses_registered_scenarios_and_asymmetric_loss,
        test_food_withholds_on_unusable_scenarios,
        test_shuttle_selects_capacity_bundle_with_lowest_registered_loss,
        test_shuttle_withholds_if_even_full_fleet_misses_service_floor,
        test_space_plan_selects_low_loss_zone_bundle,
        test_space_plan_withholds_when_full_capacity_cannot_meet_floor,
        test_class_scheduler_assigns_rooms_and_slots_without_collisions,
        test_class_scheduler_withholds_if_feature_constraints_are_infeasible,
        test_shared_capacity_respects_minimums_and_priority,
        test_shared_capacity_withholds_when_minimums_exceed_capacity,
        test_bundle_propagates_most_conservative_readiness,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
