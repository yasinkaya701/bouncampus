#!/usr/bin/env python3
"""Focused regression tests for cross-domain CS1 campus operations portfolio output."""

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


def campus_state(readiness: str = "REVIEW_REQUIRED"):
    return {
        "contract_version": "campus-ops-v1.0",
        "decision_readiness": readiness,
        "abstained": readiness == "WITHHOLD",
        "campus_totals": {
            "south": {"capacity": 1000, "occupancy_estimate": 600, "utilization_pct": 60.0},
            "north": {"capacity": 1500, "occupancy_estimate": 900, "utilization_pct": 60.0},
        },
        "reason_codes": [],
    }


def shuttle_plan():
    return {
        "decision_readiness": "REVIEW_REQUIRED",
        "routes": [{"route_id": "south-north", "capacity_feasible": False, "unserved_seat_demand_estimate": 35}],
        "reason_codes": ["ROUTE_CAPACITY_SHORTFALL_SOUTH-NORTH"],
    }


def classroom_plan():
    return {
        "decision_readiness": "REVIEW_REQUIRED",
        "assignments": [{"session_id": "A", "room_id": "M101", "building_id": "B-SOUTH-M"}],
        "unassigned": [{"session_id": "B", "reason": "NO_FEASIBLE_ROOM"}],
        "building_loads": {"B-SOUTH-M": {"assigned_sessions": 1, "assigned_attendance": 70, "assigned_room_capacity": 80}},
        "reason_codes": ["NO_FEASIBLE_ROOM_B"],
    }


def food_decision(readiness: str = "REVIEW_REQUIRED"):
    return {"decision_readiness": readiness, "recommended_production": None if readiness == "WITHHOLD" else 505, "objective_units": "REGISTERED_RELATIVE_SENSITIVITY_UNITS", "reason_codes": []}


def energy_decision(readiness: str = "REVIEW_REQUIRED"):
    return {"decision_readiness": readiness, "zones": [] if readiness == "WITHHOLD" else [{"zone_id": "Z1", "recommended_mode": "SETBACK_REVIEW"}, {"zone_id": "Z2", "recommended_mode": "NORMAL_SERVICE_REVIEW"}], "reason_codes": []}


def shared_capacity_decision(readiness: str = "REVIEW_REQUIRED"):
    return {
        "decision_readiness": readiness,
        "allocations": [] if readiness == "WITHHOLD" else [
            {"request_id": "study", "allocated": 7},
            {"request_id": "charging", "allocated": 3},
        ],
        "reason_codes": [],
    }


def test_portfolio_exposes_cross_domain_pressure_without_auto_execution() -> None:
    portfolio = load_module("campus_portfolio", "backend/app/decision/campus_portfolio.py")
    result = portfolio.build_campus_portfolio(
        campus_state=campus_state(),
        shuttle_plan=shuttle_plan(),
        classroom_plan=classroom_plan(),
        food_decision=food_decision(),
        energy_decision=energy_decision(),
        shared_capacity_decision=shared_capacity_decision(),
    )
    assert result["contract_version"] == "campus-ops-v1.0"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True
    assert result["cross_domain_signals"]["campus_demand_context"]["south"] == 600
    assert result["cross_domain_signals"]["campus_demand_context"]["north"] == 900
    assert result["cross_domain_signals"]["food_recommended_production"] == 505
    assert result["cross_domain_signals"]["energy_zone_modes"] == {"Z1": "SETBACK_REVIEW", "Z2": "NORMAL_SERVICE_REVIEW"}
    assert result["cross_domain_signals"]["shared_capacity_allocations"] == {"study": 7, "charging": 3}
    assert result["cross_domain_signals"]["shuttle_capacity_shortfall_routes"] == ["south-north"]
    assert result["cross_domain_signals"]["unassigned_sessions"] == ["B"]
    assert result["cross_domain_signals"]["building_attendance_targets"]["B-SOUTH-M"] == 70
    assert result["domain_status"]["shared_capacity"] == "REVIEW_REQUIRED"
    assert "CROSS_DOMAIN_CONFLICTS_REQUIRE_OPERATOR_REVIEW" in result["reason_codes"]


def test_portfolio_withholds_when_core_campus_state_is_withheld() -> None:
    portfolio = load_module("campus_portfolio_withhold", "backend/app/decision/campus_portfolio.py")
    result = portfolio.build_campus_portfolio(campus_state=campus_state("WITHHOLD"))
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["abstained"] is True
    assert result["cross_domain_signals"] == {}
    assert "CORE_CAMPUS_STATE_WITHHELD" in result["reason_codes"]


def test_partial_domain_withhold_does_not_fabricate_missing_signal() -> None:
    portfolio = load_module("campus_portfolio_partial", "backend/app/decision/campus_portfolio.py")
    result = portfolio.build_campus_portfolio(
        campus_state=campus_state(),
        shuttle_plan={"decision_readiness": "WITHHOLD", "routes": [], "reason_codes": ["UPSTREAM_CAMPUS_STATE_WITHHELD"]},
        classroom_plan=classroom_plan(),
        food_decision=food_decision("WITHHOLD"),
        energy_decision=energy_decision("WITHHOLD"),
        shared_capacity_decision=shared_capacity_decision("WITHHOLD"),
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["cross_domain_signals"]["shuttle_capacity_shortfall_routes"] == []
    assert result["cross_domain_signals"]["food_recommended_production"] is None
    assert result["cross_domain_signals"]["energy_zone_modes"] == {}
    assert result["cross_domain_signals"]["shared_capacity_allocations"] == {}
    assert "DOMAIN_WITHHELD_SHUTTLE" in result["reason_codes"]
    assert "DOMAIN_WITHHELD_FOOD" in result["reason_codes"]
    assert "DOMAIN_WITHHELD_ENERGY" in result["reason_codes"]
    assert "DOMAIN_WITHHELD_SHARED_CAPACITY" in result["reason_codes"]


def test_portfolio_contains_no_achieved_impact_claim_fields() -> None:
    portfolio = load_module("campus_portfolio_claims", "backend/app/decision/campus_portfolio.py")
    result = portfolio.build_campus_portfolio(
        campus_state=campus_state(),
        shuttle_plan=shuttle_plan(),
        classroom_plan=classroom_plan(),
        food_decision=food_decision(),
        energy_decision=energy_decision(),
        shared_capacity_decision=shared_capacity_decision(),
    )
    serialized = repr(result).lower()
    for forbidden in ("cost_saved", "co2_saved", "carbon_saved", "energy_saved_kwh", "waste_saved_kg", "water_saved"):
        assert forbidden not in serialized, f"unsupported achieved-impact claim leaked: {forbidden}"
    assert "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM" in result["limitations"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} campus-portfolio tests")
