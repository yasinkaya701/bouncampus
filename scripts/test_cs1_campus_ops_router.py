#!/usr/bin/env python3
"""Regression tests for the FastAPI campus-operations orchestration surface."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def request_payload():
    return {
        "decision_time": "2026-10-01T10:00:00Z",
        "zones": [
            {
                "zone_id": "south-academic",
                "campus": "south",
                "capacity": 1000,
                "occupancy_estimate": 620,
                "scheduled_load": 580,
                "event_load": 40,
            }
        ],
        "sources": {
            "schedule": {
                "available": True,
                "provenance": "PUBLIC_SOURCE",
                "published_at": "2026-10-01T08:00:00Z",
            },
            "occupancy_model": {
                "available": True,
                "provenance": "MODEL_ESTIMATE",
                "published_at": "2026-10-01T09:00:00Z",
            },
        },
        "shuttle_routes": [
            {
                "route_id": "south-north",
                "origin": "south",
                "destination": "north",
                "forecast_demand": 180,
                "vehicle_capacity": 50,
                "available_vehicles": 2,
                "service_window_min": 120,
                "round_trip_min": 40,
                "min_headway_min": 10,
                "max_headway_min": 30,
            }
        ],
        "sessions": [
            {
                "session_id": "CMPE150-1",
                "campus": "south",
                "start_minute": 540,
                "end_minute": 600,
                "expected_attendance": 70,
                "accessibility_required": True,
                "equipment_required": ["projector"],
            }
        ],
        "rooms": [
            {
                "room_id": "M101",
                "building_id": "B-SOUTH-M",
                "campus": "south",
                "capacity": 80,
                "accessible": True,
                "equipment": ["projector"],
                "energy_cost_score": 0.6,
            }
        ],
    }


def test_router_registers_domain_and_combined_endpoints() -> None:
    from app.routers import campus_ops

    paths = {route.path for route in campus_ops.router.routes}
    assert "/api/v1/campus-ops/contract" in paths
    assert "/api/v1/campus-ops/state" in paths
    assert "/api/v1/campus-ops/shuttle/plan" in paths
    assert "/api/v1/campus-ops/classrooms/allocate" in paths
    assert "/api/v1/campus-ops/portfolio" in paths
    assert "/api/v1/campus-ops/plan" in paths


def test_combined_plan_runs_all_domains_with_one_decision_cutoff() -> None:
    from app.routers import campus_ops

    payload = campus_ops.CampusOpsPlanRequest(**request_payload())
    result = campus_ops.plan_campus_operations(payload)
    assert set(result) == {"state", "shuttle", "classroom", "portfolio"}
    assert result["state"]["decision_time"] == "2026-10-01T10:00:00Z"
    assert result["shuttle"]["routes"][0]["route_id"] == "south-north"
    assert result["classroom"]["assignments"][0]["room_id"] == "M101"
    assert result["portfolio"]["automatic_execution_allowed"] is False
    assert result["portfolio"]["operator_approval_required"] is True


def test_contract_and_main_preserve_truth_boundary() -> None:
    from app.routers import campus_ops

    contract = campus_ops.get_campus_ops_contract()
    assert contract["contract_version"] == "campus-ops-v1.0"
    assert contract["automatic_execution_allowed"] is False
    assert "student identifiers" in contract["privacy_boundary"].lower()
    assert "live" in contract["truth_boundary"].lower()

    main_source = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
    assert "campus_ops" in main_source
    assert "app.include_router(campus_ops.router)" in main_source


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} campus-ops router tests")
