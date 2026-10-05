#!/usr/bin/env python3
"""Regression contract for exposing shuttle passenger-count observations via Campus Ops API."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

MIN_CONFIDENCE = 0.85


def load_router():
    return importlib.import_module("app.routers.campus_ops")


def valid_event(
    *,
    timestamp: str = "2026-10-05T08:10:00+03:00",
    direction: str = "IN",
    count_delta: int = 1,
    confidence: float = 0.95,
) -> dict:
    return {
        "deviceId": "shuttle-counter-01-door-a",
        "vehicleId": "shuttle-01",
        "timestamp": timestamp,
        "direction": direction,
        "countDelta": count_delta,
        "quality": "VALID",
        "measurementConfidence": confidence,
        "evidenceClass": "PHYSICAL_MEASUREMENT",
        "metadata": {"sensorHealth": "OK", "doorId": "front"},
    }


def test_shuttle_count_event_endpoint_preserves_measured_admission_semantics() -> None:
    router = load_router()
    result = router.shuttle_count_event(
        {"event": valid_event(), "min_measurement_confidence": MIN_CONFIDENCE}
    )
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["decision_eligible"] is True
    assert result["result_scope"] == "SHUTTLE_PASSENGER_COUNT_ADMISSION_ONLY"
    assert "absolute occupancy" in result["claim_boundary"].lower()


def test_shuttle_count_event_endpoint_preserves_structured_privacy_rejection() -> None:
    router = load_router()
    event = valid_event()
    event["metadata"] = {"capture": {"studentId": "forbidden"}}
    result = router.shuttle_count_event(
        {"event": event, "min_measurement_confidence": MIN_CONFIDENCE}
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
                valid_event(count_delta=3),
                valid_event(
                    timestamp="2026-10-05T08:20:00+03:00",
                    direction="OUT",
                    count_delta=1,
                ),
            ],
            "expected_vehicle_id": "shuttle-01",
            "window_start": "2026-10-05T08:00:00+03:00",
            "window_end": "2026-10-05T09:00:00+03:00",
            "min_measurement_confidence": MIN_CONFIDENCE,
        }
    )
    assert result["aggregation_status"] == "AGGREGATED"
    assert result["descriptive_counts_available"] is True
    assert result["in_count"] == 3
    assert result["out_count"] == 1
    assert result["net_count_delta"] == 2
    assert result["result_scope"] == "SHUTTLE_PASSENGER_COUNT_WINDOW_DELTA_ONLY"
    assert "not absolute occupancy" in result["claim_boundary"].lower()


def test_shuttle_count_endpoint_maps_invalid_threshold_to_http_422() -> None:
    from fastapi import HTTPException

    router = load_router()
    try:
        router.shuttle_count_event(
            {"event": valid_event(), "min_measurement_confidence": "invalid"}
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert "min_measurement_confidence" in str(exc.detail)
    else:
        raise AssertionError("invalid EE confidence threshold must map to HTTP 422")


def test_capabilities_exposes_shuttle_measurements_without_claiming_live_integration() -> None:
    router = load_router()
    result = router.capabilities()
    assert "shuttle_passenger_count_observations" in result["modules"]
    assert result["automatic_actuation"] is False
    boundary = result["truth_boundary"].lower()
    assert "shuttle" in boundary
    assert "caller-supplied" in boundary
    assert "live" in boundary


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle ops API tests")
