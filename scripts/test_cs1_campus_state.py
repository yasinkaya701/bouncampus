#!/usr/bin/env python3
"""Regression tests for decision-time-safe aggregate campus state on canonical #84."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_state():
    path = ROOT / "backend/app/decision/campus_state.py"
    if not path.exists():
        raise AssertionError("campus state module missing")
    spec = importlib.util.spec_from_file_location("cs1_campus_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_sources():
    return {
        "schedule": {
            "available": True,
            "provenance": "PUBLIC_SOURCE",
            "published_at": "2026-10-01T08:00:00+03:00",
        },
        "occupancy_model": {
            "available": True,
            "provenance": "MODEL_ESTIMATE",
            "published_at": "2026-10-01T09:00:00+03:00",
        },
    }


def valid_zones():
    return [
        {
            "zone_id": "south-academic",
            "campus": "south",
            "capacity": 1000,
            "occupancy_estimate": 620,
            "scheduled_load": 580,
            "event_load": 40,
        }
    ]


def test_complete_decision_time_state_requires_operator_review() -> None:
    state = load_state()
    result = state.build_campus_state(
        valid_zones(),
        valid_sources(),
        decision_time="2026-10-01T10:00:00+03:00",
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["operator_approval_required"] is True
    assert result["automatic_execution_allowed"] is False
    assert result["zones"][0]["zone_id"] == "south-academic"
    assert result["source_status"]["schedule"]["accepted_at_decision_time"] is True


def test_future_or_missing_required_source_fails_closed() -> None:
    state = load_state()
    sources = valid_sources()
    sources["occupancy_model"]["published_at"] = "2026-10-01T11:00:00+03:00"
    result = state.build_campus_state(
        valid_zones(),
        sources,
        decision_time="2026-10-01T10:00:00+03:00",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["abstained"] is True
    assert "SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_OCCUPANCY_MODEL" in result["reason_codes"]


def test_person_level_identifiers_are_rejected() -> None:
    state = load_state()
    zones = valid_zones()
    zones[0]["student_id"] = "forbidden"
    try:
        state.build_campus_state(
            zones,
            valid_sources(),
            decision_time="2026-10-01T10:00:00+03:00",
        )
    except ValueError as exc:
        assert "person-level data" in str(exc)
    else:
        raise AssertionError("person-level identifier must be rejected")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} campus-state tests")
