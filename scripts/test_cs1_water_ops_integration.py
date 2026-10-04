#!/usr/bin/env python3
"""API/orchestrator regression for CS1 water-use advisory."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def sources():
    return {
        "schedule": {"available": True, "provenance": "PUBLIC_SOURCE", "published_at": "2026-10-01T08:00:00+03:00"},
        "occupancy_model": {"available": True, "provenance": "MODEL_ESTIMATE", "published_at": "2026-10-01T09:00:00+03:00"},
    }


def campus_zones():
    return [{"zone_id": "south", "campus": "south", "capacity": 1000, "occupancy_estimate": 600}]


def water_zones():
    return [
        {"zone_id": "dorm-a", "expected_liters": 1000, "observed_liters": 1100},
        {"zone_id": "dorm-b", "expected_liters": 1000, "observed_liters": 1700},
    ]


def test_router_exposes_water_advisory_endpoint() -> None:
    from app.routers import campus_ops

    paths = {route.path for route in campus_ops.router.routes}
    assert "/api/v1/ops/water" in paths
    result = campus_ops.optimize_water({
        "zones": water_zones(),
        "elevated_ratio_threshold": 1.20,
        "critical_ratio_threshold": 1.50,
    })
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["water_savings_claim_allowed"] is False
    assert result["automatic_valve_actuation"] is False


def test_integrated_plan_runs_water_only_after_state_gate() -> None:
    from app.routers import campus_ops

    result = campus_ops.plan({
        "decision_time": "2026-10-01T10:00:00+03:00",
        "zones": campus_zones(),
        "sources": sources(),
        "modules": {
            "water": {
                "zones": water_zones(),
                "elevated_ratio_threshold": 1.20,
                "critical_ratio_threshold": 1.50,
            }
        },
    })
    assert result["state"]["decision_readiness"] == "REVIEW_REQUIRED"
    water = result["modules"]["water"]
    assert water["decision_readiness"] == "REVIEW_REQUIRED"
    modes = {row["zone_id"]: row["recommended_mode"] for row in water["zones"]}
    assert modes["dorm-b"] == "LEAK_OR_OPERATIONAL_ANOMALY_REVIEW"
    assert result["bundle"]["decision_readiness"] == "REVIEW_REQUIRED"


def test_withheld_state_suppresses_water_module() -> None:
    from app.routers import campus_ops

    bad_sources = sources()
    bad_sources["occupancy_model"]["available"] = False
    result = campus_ops.plan({
        "decision_time": "2026-10-01T10:00:00+03:00",
        "zones": campus_zones(),
        "sources": bad_sources,
        "modules": {
            "water": {
                "zones": water_zones(),
                "elevated_ratio_threshold": 1.20,
                "critical_ratio_threshold": 1.50,
            }
        },
    })
    assert result["state"]["decision_readiness"] == "WITHHOLD"
    assert result["modules"] == {}


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} water integration tests")
