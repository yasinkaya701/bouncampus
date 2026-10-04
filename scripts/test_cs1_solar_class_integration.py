#!/usr/bin/env python3
"""Regressions for solar-aware CS1 room/slot assignment."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.decision.class_assignment import optimize_class_schedule  # noqa: E402
from app.decision.class_conflicts import optimize_conflict_aware_class_schedule  # noqa: E402


def _class() -> list[dict[str, object]]:
    return [
        {
            "class_id": "CMPE150",
            "planning_attendance": 20,
            "allowed_slots": ["M10"],
            "required_features": [],
        }
    ]


def _rooms() -> list[dict[str, object]]:
    return [
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
    ]


def test_active_solar_weight_prefers_lower_exposure_room() -> None:
    result = optimize_class_schedule(
        classes=_class(),
        rooms=_rooms(),
        building_mismatch_weight=0.0,
        solar_exposure_weight=10.0,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["room_id"] == "B-cool"
    assert result["assignments"][0]["solar_exposure_index"] == 0.1
    assert result["assignments"][0]["solar_loss_component"] == 1.0
    assert "SOLAR_EXPOSURE_LOSS_ACTIVE" in result["reason_codes"]


def test_zero_solar_weight_preserves_legacy_tie_breaking() -> None:
    rooms = _rooms()
    rooms[0]["solar_load_by_slot"] = {"M10": 99}
    result = optimize_class_schedule(
        classes=_class(),
        rooms=rooms,
        building_mismatch_weight=0.0,
        solar_exposure_weight=0.0,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["room_id"] == "A-hot"
    assert "SOLAR_EXPOSURE_LOSS_ACTIVE" not in result["reason_codes"]


def test_invalid_solar_map_fails_closed_when_weight_is_active() -> None:
    rooms = _rooms()
    rooms[0]["solar_load_by_slot"] = {"M10": 1.2}
    result = optimize_class_schedule(
        classes=_class(),
        rooms=rooms,
        building_mismatch_weight=0.0,
        solar_exposure_weight=1.0,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["assignments"] == []
    assert "INVALID_ROOM_SOLAR_LOAD" in result["reason_codes"]


def test_conflict_aware_wrapper_propagates_solar_weight() -> None:
    classes = _class()
    classes[0]["conflict_keys"] = []
    result = optimize_conflict_aware_class_schedule(
        classes=classes,
        rooms=_rooms(),
        building_mismatch_weight=0.0,
        solar_exposure_weight=10.0,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["room_id"] == "B-cool"


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} solar-class integration tests")
