#!/usr/bin/env python3
"""Cross-domain CS1 contract checks for food, shuttle, and space decisions."""

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


def representative_decisions():
    food = load_module("food_policy_contract", "backend/app/decision/food_policy.py")
    shuttle = load_module("shuttle_policy_contract", "backend/app/decision/shuttle_policy.py")
    space = load_module("space_policy_contract", "backend/app/decision/space_policy.py")

    food_decision = food.build_food_decision(
        500,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        method_eligibility="PILOT_ELIGIBLE",
    )
    shuttle_decision = shuttle.build_shuttle_decision(
        45,
        scheduled_capacity=50,
        signal_availability={
            "official_schedule": True,
            "historical_boardings": True,
            "course_schedule": True,
            "calendar": True,
        },
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    space_decision = space.build_space_decision(
        32,
        [
            {
                "room_id": "ROOM-40",
                "capacity": 40,
                "available": True,
                "accessible": True,
                "features": ["projector"],
            }
        ],
        signal_availability={
            "timetable": True,
            "room_inventory": True,
            "attendance": True,
            "accessibility_metadata": True,
        },
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    return food_decision, shuttle_decision, space_decision


def test_all_operational_domains_share_the_cs1_safety_envelope() -> None:
    required_fields = {
        "policy_version",
        "method_eligibility",
        "decision_provenance",
        "decision_readiness",
        "abstained",
        "operator_approval_required",
        "signal_coverage_pct",
        "signals",
        "reason_codes",
        "limitations",
    }

    for decision in representative_decisions():
        assert required_fields.issubset(decision)
        assert decision["decision_readiness"] in {
            "PILOT_READY",
            "REVIEW_REQUIRED",
            "WITHHOLD",
        }
        assert decision["operator_approval_required"] is True
        assert isinstance(decision["reason_codes"], list)
        assert isinstance(decision["limitations"], list)
        assert 0 <= decision["signal_coverage_pct"] <= 100


def test_no_domain_can_auto_execute_its_operator_recommendation() -> None:
    food, shuttle, space = representative_decisions()
    assert food["automatic_kitchen_dispatch"] is False
    assert shuttle["automatic_shuttle_dispatch"] is False
    assert space["automatic_room_booking"] is False


def test_unavailable_live_telemetry_is_not_promoted_to_fact() -> None:
    _, shuttle, space = representative_decisions()
    assert shuttle["telemetry_status"] == "NOT_CONNECTED"
    assert shuttle["live_eta_available"] is False
    assert shuttle["live_occupancy_available"] is False
    assert space["occupancy_telemetry_status"] == "NOT_CONNECTED"
    assert space["live_occupancy_available"] is False


def test_sandbox_methods_abstain_across_all_domains() -> None:
    food = load_module("food_policy_sandbox", "backend/app/decision/food_policy.py")
    shuttle = load_module("shuttle_policy_sandbox", "backend/app/decision/shuttle_policy.py")
    space = load_module("space_policy_sandbox", "backend/app/decision/space_policy.py")

    food_decision = food.build_food_decision(
        500,
        {"schedule": True, "weather": True, "menu": True, "calendar": True},
        method_eligibility="SANDBOX_ONLY",
    )
    shuttle_decision = shuttle.build_shuttle_decision(
        45,
        scheduled_capacity=50,
        signal_availability={
            "official_schedule": True,
            "historical_boardings": True,
            "course_schedule": True,
            "calendar": True,
        },
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="SANDBOX_ONLY",
    )
    space_decision = space.build_space_decision(
        32,
        [
            {
                "room_id": "ROOM-40",
                "capacity": 40,
                "available": True,
                "accessible": True,
                "features": [],
            }
        ],
        signal_availability={
            "timetable": True,
            "room_inventory": True,
            "attendance": True,
            "accessibility_metadata": True,
        },
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="SANDBOX_ONLY",
    )

    for decision in (food_decision, shuttle_decision, space_decision):
        assert decision["decision_readiness"] == "WITHHOLD"
        assert decision["abstained"] is True
        assert "METHOD_SANDBOX_ONLY" in decision["reason_codes"]

    assert food_decision["recommended_production"] is None
    assert shuttle_decision["recommended_action"] is None
    assert space_decision["recommended_room_id"] is None


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} CS1 campus-operations contract tests")
