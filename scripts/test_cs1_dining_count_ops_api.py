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


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} dining count ops API tests")
