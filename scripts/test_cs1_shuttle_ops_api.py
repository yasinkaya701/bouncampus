#!/usr/bin/env python3
"""Regression contract for exposing anonymous shuttle count truth through Campus Ops."""

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


def valid_event(*, direction: str = "IN", count_delta: int = 1, minute: int = 5) -> dict:
    return {
        "deviceId": "shuttle-counter-bus-12-door-a",
        "vehicleId": "bus-12",
        "timestamp": f"2026-10-05T08:{minute:02d}:00+03:00",
        "direction": direction,
        "countDelta": count_delta,
        "quality": "VALID",
        "measurementConfidence": 0.96,
        "evidenceClass": "PHYSICAL_MEASUREMENT",
        "metadata": {"sensorHealth": "OK"},
    }


def test_shuttle_count_event_endpoint_exposes_admitted_measurement_only() -> None:
    router = load_router()
    result = router.shuttle_count_event(
        {
            "event": valid_event(),
            "min_measurement_confidence": 0.9,
        }
    )
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["decision_eligible"] is True
    assert result["result_scope"] == "SHUTTLE_PASSENGER_COUNT_ADMISSION_ONLY"
    assert "absolute occupancy" in result["claim_boundary"].lower()
    assert "occupancy" not in result


def test_shuttle_count_event_endpoint_preserves_structured_privacy_rejection() -> None:
    router = load_router()
    payload = valid_event()
    payload["metadata"] = {"capture": {"studentId": "forbidden"}}
    result = router.shuttle_count_event(
        {
            "event": payload,
            "min_measurement_confidence": 0.9,
        }
    )
    assert result["validation_status"] == "REJECTED"
    assert result["decision_eligible"] is False
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in result["reason_codes"]
    assert result["event_fingerprint_sha256"] is None


def test_shuttle_count_window_endpoint_exposes_delta_not_absolute_occupancy() -> None:
    router = load_router()
    result = router.shuttle_count_window(
        {
            "events": [
                valid_event(direction="IN", count_delta=4, minute=5),
                valid_event(direction="OUT", count_delta=1, minute=10),
            ],
            "expected_vehicle_id": "bus-12",
            "window_start": "2026-10-05T08:00:00+03:00",
            "window_end": "2026-10-05T08:15:00+03:00",
            "min_measurement_confidence": 0.9,
        }
    )
    assert result["aggregation_status"] == "AGGREGATED"
    assert result["coverage_status"] == "FULL"
    assert result["in_count"] == 4
    assert result["out_count"] == 1
    assert result["net_count_delta"] == 3
    assert result["result_scope"] == "SHUTTLE_PASSENGER_COUNT_WINDOW_DELTA_ONLY"
    assert "absolute occupancy" in result["claim_boundary"].lower()
    assert "occupancy" not in result


def test_shuttle_count_window_bad_request_is_reported_as_http_422() -> None:
    from fastapi import HTTPException

    router = load_router()
    try:
        router.shuttle_count_window(
            {
                "events": [],
                "expected_vehicle_id": "bus-12",
                "window_start": "not-a-time",
                "window_end": "2026-10-05T08:15:00+03:00",
                "min_measurement_confidence": 0.9,
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert "window_start" in str(exc.detail)
    else:
        raise AssertionError("invalid shuttle count window must map to HTTP 422")


def test_capabilities_exposes_shuttle_counts_without_claiming_live_integration() -> None:
    router = load_router()
    result = router.capabilities()
    assert "shuttle_count_observations" in result["modules"]
    assert result["automatic_actuation"] is False
    boundary = result["truth_boundary"].lower()
    assert "shuttle" in boundary
    assert "live" in boundary


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle ops API tests")
