#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/solar_site_planning.py"
    if not path.exists():
        raise AssertionError("solar site planning policy missing")
    spec = importlib.util.spec_from_file_location("cs1_solar_site_planning", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_istanbul_summer_solar_noon_sun_is_high_and_southerly() -> None:
    policy = load_policy()
    pos = policy.solar_position(41.083, 29.052, "2026-06-21T13:00:00+03:00")
    assert pos["elevation_deg"] > 65
    assert 150 <= pos["azimuth_deg"] <= 220


def test_south_facade_receives_more_direct_sun_than_north_at_noon() -> None:
    policy = load_policy()
    result = policy.analyze_room_solar_exposure(
        latitude_deg=41.083,
        longitude_deg=29.052,
        timestamps=["2026-10-01T12:00:00+03:00"],
        rooms=[
            {"room_id": "south", "building_id": "B1", "facade_azimuth_deg": 180, "window_area_m2": 8},
            {"room_id": "north", "building_id": "B1", "facade_azimuth_deg": 0, "window_area_m2": 8},
        ],
        class_sessions=[],
        affected_threshold=0.2,
    )
    by_room = {row["room_id"]: row for row in result["room_exposure"]}
    assert by_room["south"]["mean_direct_exposure_index"] > by_room["north"]["mean_direct_exposure_index"]
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_actuation"] is False


def test_obstruction_horizon_blocks_direct_exposure() -> None:
    policy = load_policy()
    result = policy.analyze_room_solar_exposure(
        latitude_deg=41.083,
        longitude_deg=29.052,
        timestamps=["2026-12-21T09:00:00+03:00"],
        rooms=[
            {
                "room_id": "blocked",
                "building_id": "B1",
                "facade_azimuth_deg": 140,
                "window_area_m2": 8,
                "obstruction_elevation_deg": 80,
            },
        ],
        class_sessions=[],
        affected_threshold=0.2,
    )
    assert result["room_exposure"][0]["mean_direct_exposure_index"] == 0.0


def test_class_sessions_are_linked_to_room_exposure() -> None:
    policy = load_policy()
    ts = "2026-10-01T12:00:00+03:00"
    result = policy.analyze_room_solar_exposure(
        latitude_deg=41.083,
        longitude_deg=29.052,
        timestamps=[ts],
        rooms=[{"room_id": "S101", "building_id": "B1", "facade_azimuth_deg": 180, "window_area_m2": 10}],
        class_sessions=[{"class_id": "CMPE150", "room_id": "S101", "timestamp": ts}],
        affected_threshold=0.1,
    )
    assert result["affected_classes"][0]["class_id"] == "CMPE150"
    assert result["affected_classes"][0]["room_id"] == "S101"
    assert result["affected_classes"][0]["direct_exposure_index"] >= 0.1


def test_new_building_orientation_ranking_is_deterministic_and_review_only() -> None:
    policy = load_policy()
    result = policy.rank_new_building_orientations(
        latitude_deg=41.083,
        longitude_deg=29.052,
        timestamps=["2026-06-21T09:00:00+03:00", "2026-06-21T15:00:00+03:00"],
        facade_program=[
            {"facade_id": "classrooms", "relative_azimuth_deg": 0, "daylight_weight": 1.0, "heat_weight": 2.0},
            {"facade_id": "service", "relative_azimuth_deg": 180, "daylight_weight": 0.2, "heat_weight": 0.5},
        ],
        candidate_orientations_deg=[0, 90, 180, 270],
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_design_selection"] is False
    assert len(result["candidates"]) == 4
    assert result["candidates"] == sorted(
        result["candidates"],
        key=lambda row: (row["registered_loss"], row["orientation_deg"]),
    )


def test_malformed_geometry_fails_closed() -> None:
    policy = load_policy()
    result = policy.analyze_room_solar_exposure(
        latitude_deg=100,
        longitude_deg=29.052,
        timestamps=["2026-10-01T12:00:00+03:00"],
        rooms=[{"room_id": "S101", "building_id": "B1", "facade_azimuth_deg": 180, "window_area_m2": 10}],
        class_sessions=[],
        affected_threshold=0.1,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert "INVALID_SOLAR_GEOMETRY_INPUT" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} solar-site-planning tests")
