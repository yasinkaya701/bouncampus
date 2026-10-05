#!/usr/bin/env python3
"""Regression contract for exposing dining physical counts through Campus Ops API."""

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


def valid_event() -> dict:
    return {
        "eventId": "dining-count-2026-10-05-000001",
        "deviceId": "serving-counter-north-01",
        "stationId": "north-dining-line-1",
        "timestamp": "2026-10-05T12:05:00+03:00",
        "measurementType": "SERVED_TRAY_DELTA",
        "value": 7,
        "unit": "TRAYS",
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "dining-counter-fw-0.1.0",
        "schemaVersion": "dining-count-event-v1",
    }


def test_dining_count_event_endpoint_exposes_measurement_without_truth_promotion() -> None:
    router = load_router()
    result = router.dining_count_event(valid_event())

    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["aggregation_eligible"] is True
    assert result["measurement_type"] == "SERVED_TRAY_DELTA"
    assert result["count_delta"] == 7
    assert result["reconciled_service_truth"] is False
    assert "actual_served" not in result
    assert "served_portions" not in result


def test_dining_count_window_endpoint_is_retry_safe_and_descriptive_only() -> None:
    router = load_router()
    event = valid_event()
    result = router.dining_count_window(
        {
            "events": [event, event.copy()],
            "station_id": "north-dining-line-1",
            "window_start": "2026-10-05T12:00:00+03:00",
            "window_end": "2026-10-05T13:00:00+03:00",
        }
    )

    assert result["aggregation_status"] == "AGGREGATED"
    assert result["total_event_count"] == 2
    assert result["unique_event_count"] == 1
    assert result["idempotent_replay_count"] == 1
    assert result["served_trays_observed"] == 7
    assert result["reconciled_service_truth"] is False
    assert "actual_served" not in result
    assert "served_portions_observed" not in result


def test_capabilities_exposes_dining_counts_without_claiming_live_integration() -> None:
    router = load_router()
    result = router.capabilities()

    assert "dining_physical_counts" in result["modules"]
    truth_boundary = result["truth_boundary"].lower()
    privacy_boundary = result["privacy_boundary"].lower()
    assert "dining" in truth_boundary
    assert "caller-supplied" in truth_boundary
    assert "live" in truth_boundary
    assert "dining" in privacy_boundary
    assert "anonymous" in privacy_boundary


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} dining count ops API tests")
