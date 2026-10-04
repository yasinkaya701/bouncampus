#!/usr/bin/env python3
"""Regression contract for exposing RoomNode observations through Campus Ops API."""

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
        "eventId": "room-event-1",
        "deviceId": "roomnode-nb-301-a",
        "stationId": "north-building-room-301",
        "timestamp": "2026-10-04T14:05:00+03:00",
        "measurementType": "CO2_PPM",
        "value": 742,
        "unit": "PPM",
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "0.1.0",
        "schemaVersion": "ROOMNODE_EVENT_V1",
        "metadata": {"sensorHealth": "OK"},
    }


def test_roomnode_event_endpoint_exposes_descriptive_measurement_only() -> None:
    router = load_router()
    result = router.roomnode_event(valid_event())
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["measurement_eligible"] is True
    assert result["decision_eligible"] is False
    assert result["impact_claim_allowed"] is False
    assert result["automatic_actuation"] is False


def test_roomnode_event_endpoint_preserves_structured_privacy_rejection() -> None:
    router = load_router()
    payload = valid_event()
    payload["metadata"] = {"capture": {"studentId": "forbidden"}}
    result = router.roomnode_event(payload)
    assert result["validation_status"] == "REJECTED"
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in result["reason_codes"]
    assert result["event_fingerprint_sha256"] is None


def test_roomnode_window_endpoint_exposes_retry_safe_summary() -> None:
    router = load_router()
    event = valid_event()
    result = router.roomnode_window(
        {
            "events": [event, event.copy()],
            "station_id": "north-building-room-301",
            "window_start": "2026-10-04T14:00:00+03:00",
            "window_end": "2026-10-04T14:15:00+03:00",
        }
    )
    assert result["aggregation_status"] == "DESCRIPTIVE_ONLY"
    assert result["total_event_count"] == 2
    assert result["unique_event_count"] == 1
    assert result["idempotent_replay_count"] == 1
    assert result["decision_eligible"] is False
    assert result["per_measurement"]["CO2_PPM"]["sample_count"] == 1


def test_roomnode_window_bad_request_is_reported_as_http_422() -> None:
    from fastapi import HTTPException

    router = load_router()
    try:
        router.roomnode_window(
            {
                "events": [],
                "station_id": "north-building-room-301",
                "window_start": "not-a-time",
                "window_end": "2026-10-04T14:15:00+03:00",
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert "window_start" in str(exc.detail)
    else:
        raise AssertionError("invalid RoomNode window must map to HTTP 422")


def test_capabilities_exposes_roomnode_without_claiming_live_integration() -> None:
    router = load_router()
    result = router.capabilities()
    assert "roomnode_observations" in result["modules"]
    assert result["automatic_actuation"] is False
    assert "roomnode" in result["truth_boundary"].lower()
    assert "live" in result["truth_boundary"].lower()


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} RoomNode ops API tests")
