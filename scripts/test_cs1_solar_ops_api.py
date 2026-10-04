#!/usr/bin/env python3
"""Focused API regressions for CS1 solar/site planning surfaces."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def load_router():
    return importlib.import_module("app.routers.campus_ops")


def test_capabilities_publish_solar_and_site_orientation_modules() -> None:
    router = load_router()
    modules = set(router.capabilities()["modules"])
    assert {"solar_exposure", "site_orientation"}.issubset(modules)


def test_solar_endpoint_maps_direct_exposure_to_class_session() -> None:
    router = load_router()
    timestamp = "2026-10-01T12:00:00+03:00"
    result = router.solar_review(
        {
            "latitude_deg": 41.083,
            "longitude_deg": 29.052,
            "timestamps": [timestamp],
            "rooms": [
                {
                    "room_id": "S101",
                    "building_id": "B1",
                    "facade_azimuth_deg": 180,
                    "window_area_m2": 10,
                }
            ],
            "class_sessions": [
                {"class_id": "CMPE150", "room_id": "S101", "timestamp": timestamp}
            ],
            "affected_threshold": 0.1,
        }
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["affected_classes"][0]["class_id"] == "CMPE150"
    assert result["automatic_actuation"] is False


def test_site_orientation_endpoint_ranks_candidates_without_auto_selection() -> None:
    router = load_router()
    result = router.site_orientation(
        {
            "latitude_deg": 41.083,
            "longitude_deg": 29.052,
            "timestamps": ["2026-06-21T09:00:00+03:00", "2026-06-21T15:00:00+03:00"],
            "facade_program": [
                {
                    "facade_id": "classrooms",
                    "relative_azimuth_deg": 0,
                    "daylight_weight": 1.0,
                    "heat_weight": 2.0,
                },
                {
                    "facade_id": "service",
                    "relative_azimuth_deg": 180,
                    "daylight_weight": 0.2,
                    "heat_weight": 0.5,
                },
            ],
            "candidate_orientations_deg": [0, 90, 180, 270],
        }
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert len(result["candidates"]) == 4
    assert result["automatic_design_selection"] is False


def test_classes_endpoint_forwards_solar_exposure_weight() -> None:
    router = load_router()
    result = router.optimize_classes(
        {
            "classes": [
                {
                    "class_id": "CMPE150",
                    "planning_attendance": 20,
                    "allowed_slots": ["M10"],
                    "required_features": [],
                }
            ],
            "rooms": [
                {
                    "room_id": "A-hot",
                    "capacity": 30,
                    "features": [],
                    "building": "B1",
                    "solar_load_by_slot": {"M10": 0.9},
                },
                {
                    "room_id": "B-cool",
                    "capacity": 30,
                    "features": [],
                    "building": "B1",
                    "solar_load_by_slot": {"M10": 0.1},
                },
            ],
            "solar_exposure_weight": 10.0,
        }
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["room_id"] == "B-cool"


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} solar campus-ops API tests")
