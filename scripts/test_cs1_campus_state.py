#!/usr/bin/env python3
"""Focused regression tests for the CS1 aggregate campus state engine."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    assert path.exists(), f"missing production module: {relative_path}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def healthy_sources():
    return {
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
        "events": {
            "available": True,
            "provenance": "PUBLIC_SOURCE",
            "published_at": "2026-10-01T07:00:00Z",
        },
    }


def sample_zone(**overrides):
    zone = {
        "zone_id": "north-academic",
        "campus": "north",
        "capacity": 1000,
        "occupancy_estimate": 700,
        "scheduled_load": 650,
        "event_load": 20,
    }
    zone.update(overrides)
    return zone


def assert_value_error(callable_, fragment: str) -> None:
    try:
        callable_()
    except ValueError as exc:
        assert fragment.lower() in str(exc).lower(), str(exc)
    else:
        raise AssertionError(f"expected ValueError containing {fragment!r}")


def test_builds_aggregate_state_without_person_level_data() -> None:
    state = load_module("campus_state", "backend/app/decision/campus_state.py")
    result = state.build_campus_state(
        zones=[
            {
                "zone_id": "south-academic",
                "campus": "south",
                "capacity": 1000,
                "occupancy_estimate": 620,
                "scheduled_load": 580,
                "event_load": 40,
            },
            {
                "zone_id": "north-academic",
                "campus": "north",
                "capacity": 1500,
                "occupancy_estimate": 900,
                "scheduled_load": 840,
                "event_load": 80,
            },
        ],
        sources=healthy_sources(),
        decision_time="2026-10-01T10:00:00Z",
    )

    assert result["contract_version"] == "campus-ops-v1.0"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["abstained"] is False
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True
    assert result["campus_totals"]["south"]["occupancy_estimate"] == 620
    assert result["campus_totals"]["north"]["occupancy_estimate"] == 900
    assert result["campus_totals"]["north"]["utilization_pct"] == 60.0
    assert "NO_LIVE_TELEMETRY_CLAIM" in result["limitations"]
    schedule = next(item for item in result["source_health"] if item["source_id"] == "schedule")
    assert schedule["provenance"] == "OFFICIAL_PUBLIC"


def test_required_schedule_or_occupancy_source_missing_fails_closed() -> None:
    state = load_module("campus_state_missing", "backend/app/decision/campus_state.py")

    for required_source in ("schedule", "occupancy_model"):
        sources = healthy_sources()
        sources[required_source]["available"] = False
        result = state.build_campus_state(
            zones=[sample_zone()],
            sources=sources,
            decision_time="2026-10-01T10:00:00Z",
        )
        assert result["decision_readiness"] == "WITHHOLD"
        assert result["abstained"] is True
        assert f"MISSING_REQUIRED_SOURCE_{required_source.upper()}" in result["reason_codes"]


def test_future_information_is_not_accepted_at_decision_time() -> None:
    state = load_module("campus_state_future", "backend/app/decision/campus_state.py")
    sources = healthy_sources()
    sources["occupancy_model"]["published_at"] = "2026-10-01T11:00:00Z"
    result = state.build_campus_state(
        zones=[sample_zone()],
        sources=sources,
        decision_time="2026-10-01T10:00:00Z",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert "SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_OCCUPANCY_MODEL" in result["reason_codes"]


def test_rejects_person_identifiers() -> None:
    state = load_module("campus_state_privacy", "backend/app/decision/campus_state.py")
    for field in ("student_id", "person_id", "email", "device_id", "wifi_client_id"):
        assert_value_error(
            lambda field=field: state.build_campus_state(
                zones=[sample_zone(**{field: "private-value"})],
                sources=healthy_sources(),
                decision_time="2026-10-01T10:00:00Z",
            ),
            "person-level",
        )


def test_rejects_invalid_zone_values_and_duplicates() -> None:
    state = load_module("campus_state_validation", "backend/app/decision/campus_state.py")

    assert_value_error(
        lambda: state.build_campus_state(
            zones=[sample_zone(capacity=-1)],
            sources=healthy_sources(),
            decision_time="2026-10-01T10:00:00Z",
        ),
        "capacity",
    )
    for field in ("capacity", "occupancy_estimate", "scheduled_load", "event_load"):
        for bad_value in (math.nan, math.inf, -math.inf):
            assert_value_error(
                lambda field=field, bad_value=bad_value: state.build_campus_state(
                    zones=[sample_zone(**{field: bad_value})],
                    sources=healthy_sources(),
                    decision_time="2026-10-01T10:00:00Z",
                ),
                field,
            )
    assert_value_error(
        lambda: state.build_campus_state(
            zones=[sample_zone(), sample_zone(campus="south")],
            sources=healthy_sources(),
            decision_time="2026-10-01T10:00:00Z",
        ),
        "duplicate zone_id",
    )


def test_rejects_bad_source_contracts() -> None:
    state = load_module("campus_state_sources", "backend/app/decision/campus_state.py")

    sources = healthy_sources()
    sources["schedule"]["provenance"] = "MADE_UP_SOURCE"
    assert_value_error(
        lambda: state.build_campus_state(
            zones=[sample_zone()],
            sources=sources,
            decision_time="2026-10-01T10:00:00Z",
        ),
        "provenance",
    )

    sources = healthy_sources()
    sources["schedule"]["published_at"] = "2026-10-01 08:00:00"
    assert_value_error(
        lambda: state.build_campus_state(
            zones=[sample_zone()],
            sources=sources,
            decision_time="2026-10-01T10:00:00Z",
        ),
        "timestamp",
    )


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} campus-state tests")
