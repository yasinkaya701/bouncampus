#!/usr/bin/env python3
"""API/orchestrator regression for CS1 building-energy advisory."""

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


def zones():
    return [
        {"zone_id": "low", "campus": "south", "capacity": 100, "occupancy_estimate": 10},
        {"zone_id": "high", "campus": "south", "capacity": 100, "occupancy_estimate": 80},
    ]


def test_router_exposes_energy_advisory_endpoint() -> None:
    from app.routers import campus_ops

    paths = {route.path for route in campus_ops.router.routes}
    assert "/api/v1/ops/energy" in paths
    result = campus_ops.optimize_energy({
        "zones": zones(),
        "low_utilization_threshold": 0.25,
        "medium_utilization_threshold": 0.60,
    })
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["energy_savings_claim_allowed"] is False
    assert result["automatic_actuation"] is False


def test_integrated_plan_runs_energy_from_accepted_state_zones() -> None:
    from app.routers import campus_ops

    result = campus_ops.plan({
        "decision_time": "2026-10-01T10:00:00+03:00",
        "zones": zones(),
        "sources": sources(),
        "modules": {
            "energy": {
                "low_utilization_threshold": 0.25,
                "medium_utilization_threshold": 0.60,
            }
        },
    })
    assert result["state"]["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["modules"]["energy"]["decision_readiness"] == "REVIEW_REQUIRED"
    modes = {row["zone_id"]: row["recommended_mode"] for row in result["modules"]["energy"]["zones"]}
    assert modes == {"low": "SETBACK_REVIEW", "high": "NORMAL_SERVICE_REVIEW"}
    assert result["bundle"]["decision_readiness"] == "REVIEW_REQUIRED"


def test_withheld_state_suppresses_energy_module() -> None:
    from app.routers import campus_ops

    bad_sources = sources()
    bad_sources["occupancy_model"]["available"] = False
    result = campus_ops.plan({
        "decision_time": "2026-10-01T10:00:00+03:00",
        "zones": zones(),
        "sources": bad_sources,
        "modules": {
            "energy": {
                "low_utilization_threshold": 0.25,
                "medium_utilization_threshold": 0.60,
            }
        },
    })
    assert result["state"]["decision_readiness"] == "WITHHOLD"
    assert result["modules"] == {}
    assert result["bundle"]["decision_readiness"] == "WITHHOLD"


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} energy integration tests")
