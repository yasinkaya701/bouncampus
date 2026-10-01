#!/usr/bin/env python3
"""Focused tests for CS1 source-health normalization and decision-time eligibility."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_source_health():
    path = ROOT / "backend/app/decision/source_health.py"
    assert path.exists(), "missing production module: backend/app/decision/source_health.py"
    spec = importlib.util.spec_from_file_location("source_health", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_value_error(callable_, fragment: str) -> None:
    try:
        callable_()
    except ValueError as exc:
        assert fragment.lower() in str(exc).lower(), str(exc)
    else:
        raise AssertionError(f"expected ValueError containing {fragment!r}")


def test_normalizes_public_source_alias() -> None:
    health = load_source_health()
    result = health.normalize_source(
        "schedule",
        {
            "available": True,
            "provenance": "PUBLIC_SOURCE",
            "published_at": "2026-10-01T08:00:00Z",
        },
        "2026-10-01T10:00:00Z",
        domain="campus",
    )
    assert result["source_id"] == "schedule"
    assert result["domain"] == "campus"
    assert result["provenance"] == "OFFICIAL_PUBLIC"
    assert result["status"] == "VERIFIED"
    assert result["eligible_at_decision_time"] is True


def test_unknown_provenance_is_rejected() -> None:
    health = load_source_health()
    assert_value_error(
        lambda: health.normalize_source(
            "schedule",
            {
                "available": True,
                "provenance": "SCRAPED_MYSTERY_FEED",
                "published_at": "2026-10-01T08:00:00Z",
            },
            "2026-10-01T10:00:00Z",
        ),
        "provenance",
    )


def test_future_source_is_ineligible() -> None:
    health = load_source_health()
    result = health.normalize_source(
        "occupancy_model",
        {
            "available": True,
            "provenance": "MODEL_ESTIMATE",
            "published_at": "2026-10-01T11:00:00Z",
        },
        "2026-10-01T10:00:00Z",
    )
    assert result["status"] == "NOT_AVAILABLE_AT_DECISION_TIME"
    assert result["eligible_at_decision_time"] is False
    assert "SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_OCCUPANCY_MODEL" in result["reason_codes"]


def test_missing_required_source_is_unavailable() -> None:
    health = load_source_health()
    result = health.normalize_source(
        "schedule",
        {
            "available": False,
            "provenance": "PUBLIC_SOURCE",
            "published_at": "2026-10-01T08:00:00Z",
        },
        "2026-10-01T10:00:00Z",
    )
    assert result["status"] == "UNAVAILABLE"
    assert result["eligible_at_decision_time"] is False
    assert "SOURCE_UNAVAILABLE_SCHEDULE" in result["reason_codes"]


def test_timezone_aware_cutoff_is_respected() -> None:
    health = load_source_health()
    result = health.normalize_source(
        "schedule",
        {
            "available": True,
            "provenance": "OFFICIAL_PUBLIC",
            "published_at": "2026-10-01T12:00:00+03:00",
        },
        "2026-10-01T09:30:00Z",
    )
    assert result["status"] == "VERIFIED"
    assert result["eligible_at_decision_time"] is True


def test_naive_or_malformed_timestamps_are_rejected() -> None:
    health = load_source_health()
    for bad_timestamp in ("2026-10-01 08:00:00", "not-a-time", ""):
        assert_value_error(
            lambda bad_timestamp=bad_timestamp: health.normalize_source(
                "schedule",
                {
                    "available": True,
                    "provenance": "OFFICIAL_PUBLIC",
                    "published_at": bad_timestamp,
                },
                "2026-10-01T10:00:00Z",
            ),
            "timestamp",
        )


def test_normalize_sources_rejects_duplicate_or_non_mapping_entries() -> None:
    health = load_source_health()
    assert_value_error(
        lambda: health.normalize_sources(
            {"schedule": "not-a-mapping"},
            "2026-10-01T10:00:00Z",
        ),
        "mapping",
    )


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} source-health tests")
