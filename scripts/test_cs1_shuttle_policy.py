#!/usr/bin/env python3
"""Focused regression tests for aggregate shuttle capacity planning."""

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


def route(**overrides):
    base = {
        "route_id": "south-north",
        "origin": "south",
        "destination": "north",
        "forecast_demand": 180,
        "vehicle_capacity": 50,
        "available_vehicles": 2,
        "capacity_provenance": "OFFICIAL_SNAPSHOT",
        "service_window_min": 120,
        "round_trip_min": 40,
        "min_headway_min": 10,
        "max_headway_min": 30,
    }
    base.update(overrides)
    return base


def test_recommends_capacity_without_claiming_live_gps() -> None:
    policy = load_module("shuttle_policy", "backend/app/decision/shuttle_policy.py")
    result = policy.plan_shuttle_capacity(
        [route()],
        reserve_ratio=0.10,
        upstream_readiness="REVIEW_REQUIRED",
    )
    item = result["routes"][0]
    assert result["contract_version"] == "campus-ops-v1.0"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_execution_allowed"] is False
    assert item["required_seats"] == 198
    assert item["trips_required"] == 4
    assert item["max_supported_trips"] == 6
    assert item["capacity_feasible"] is True
    assert item["capacity_provenance"] == "OFFICIAL_SNAPSHOT"
    assert item["capacity_verified"] is True
    assert 10 <= item["recommended_headway_min"] <= 30
    assert "NO_LIVE_SHUTTLE_GPS_CLAIM" in result["limitations"]


def test_oversubscribed_route_surfaces_shortage_for_review() -> None:
    policy = load_module("shuttle_policy_shortage", "backend/app/decision/shuttle_policy.py")
    result = policy.plan_shuttle_capacity(
        [route(forecast_demand=500, available_vehicles=1)],
        reserve_ratio=0.10,
        upstream_readiness="REVIEW_REQUIRED",
    )
    item = result["routes"][0]
    assert item["capacity_feasible"] is False
    assert item["unserved_seat_demand_estimate"] > 0
    assert "ROUTE_CAPACITY_SHORTFALL_SOUTH-NORTH" in result["reason_codes"]
    assert result["decision_readiness"] == "REVIEW_REQUIRED"


def test_service_window_shorter_than_round_trip_does_not_invent_trip_capacity() -> None:
    policy = load_module("shuttle_policy_short_window", "backend/app/decision/shuttle_policy.py")
    result = policy.plan_shuttle_capacity(
        [route(service_window_min=30, round_trip_min=40, forecast_demand=10)],
        reserve_ratio=0.0,
        upstream_readiness="REVIEW_REQUIRED",
    )
    item = result["routes"][0]
    assert item["max_supported_trips"] == 0
    assert item["capacity_feasible"] is False
    assert item["unserved_seat_demand_estimate"] == 10
    assert "ROUTE_CAPACITY_SHORTFALL_SOUTH-NORTH" in result["reason_codes"]


def test_unverified_capacity_withholds_capacity_sensitive_plan() -> None:
    policy = load_module("shuttle_policy_truth_boundary", "backend/app/decision/shuttle_policy.py")
    for provenance in (None, "MODEL_ESTIMATE", "POLICY_HEURISTIC"):
        candidate = route(capacity_provenance=provenance)
        result = policy.plan_shuttle_capacity(
            [candidate],
            reserve_ratio=0.10,
            upstream_readiness="REVIEW_REQUIRED",
        )
        assert result["decision_readiness"] == "WITHHOLD"
        assert result["abstained"] is True
        assert result["routes"] == []
        assert "UNVERIFIED_SHUTTLE_CAPACITY" in result["reason_codes"]


def test_withholds_when_upstream_state_is_withheld() -> None:
    policy = load_module("shuttle_policy_upstream", "backend/app/decision/shuttle_policy.py")
    result = policy.plan_shuttle_capacity(
        [route()],
        upstream_readiness="WITHHOLD",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["abstained"] is True
    assert result["routes"] == []
    assert "UPSTREAM_CAMPUS_STATE_WITHHELD" in result["reason_codes"]


def test_invalid_operational_inputs_fail_closed() -> None:
    policy = load_module("shuttle_policy_invalid", "backend/app/decision/shuttle_policy.py")
    invalid_routes = [
        route(vehicle_capacity=0),
        route(available_vehicles=-1),
        route(service_window_min=0),
        route(round_trip_min=0),
        route(forecast_demand=-5),
    ]
    for invalid in invalid_routes:
        try:
            policy.plan_shuttle_capacity([invalid], upstream_readiness="REVIEW_REQUIRED")
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid route must be rejected: {invalid}")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle-policy tests")
