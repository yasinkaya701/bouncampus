#!/usr/bin/env python3
"""Regression contract for exposing shuttle passenger-count truth through Campus Ops API."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

MIN_CONFIDENCE = 0.85
WINDOW_START = "2026-10-05T08:00:00+03:00"
WINDOW_END = "2026-10-05T09:00:00+03:00"


def load_router():
    return importlib.import_module("app.routers.campus_ops")


def valid_event(
    index: int = 1,
    *,
    direction: str = "IN",
    count_delta: int = 1,
    confidence: float = 0.95,
    quality: str = "VALID",
    evidence_class: str = "PHYSICAL_MEASUREMENT",
    vehicle_id: str = "shuttle-01",
    timestamp: str | None = None,
) -> dict:
    return {
        "deviceId": "counter-door-a",
        "vehicleId": vehicle_id,
        "timestamp": timestamp or f"2026-10-05T08:{index:02d}:00+03:00",
        "direction": direction,
        "countDelta": count_delta,
        "quality": quality,
        "measurementConfidence": confidence,
        "evidenceClass": evidence_class,
    }


def test_shuttle_count_event_endpoint_uses_caller_supplied_ee_threshold() -> None:
    router = load_router()

    accepted = router.shuttle_count_event(
        {
            "event": valid_event(confidence=0.88),
            "min_measurement_confidence": 0.85,
        }
    )
    assert accepted["validation_status"] == "ACCEPTED_MEASURED"
    assert accepted["decision_eligible"] is True
    assert accepted["minimum_confidence_threshold"] == 0.85

    withheld = router.shuttle_count_event(
        {
            "event": valid_event(confidence=0.88),
            "min_measurement_confidence": 0.90,
        }
    )
    assert withheld["validation_status"] == "WITHHOLD"
    assert withheld["decision_eligible"] is False
    assert "MEASUREMENT_CONFIDENCE_BELOW_THRESHOLD" in withheld["reason_codes"]


def test_shuttle_count_event_endpoint_preserves_privacy_and_provenance_rejection() -> None:
    router = load_router()

    identity_payload = valid_event()
    identity_payload["metadata"] = {"capture": {"studentId": "forbidden"}}
    rejected = router.shuttle_count_event(
        {
            "event": identity_payload,
            "min_measurement_confidence": MIN_CONFIDENCE,
        }
    )
    assert rejected["validation_status"] == "REJECTED"
    assert rejected["event_fingerprint_sha256"] is None
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in rejected["reason_codes"]

    non_physical = router.shuttle_count_event(
        {
            "event": valid_event(evidence_class="MODEL_ESTIMATE"),
            "min_measurement_confidence": MIN_CONFIDENCE,
        }
    )
    assert non_physical["validation_status"] == "WITHHOLD"
    assert non_physical["decision_eligible"] is False
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in non_physical["reason_codes"]


def test_shuttle_count_window_endpoint_exposes_descriptive_delta_not_occupancy() -> None:
    router = load_router()
    result = router.shuttle_count_window(
        {
            "events": [
                valid_event(1, direction="IN", count_delta=3),
                valid_event(2, direction="IN", count_delta=2),
                valid_event(3, direction="OUT", count_delta=1),
            ],
            "expected_vehicle_id": "shuttle-01",
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "min_measurement_confidence": MIN_CONFIDENCE,
        }
    )
    assert result["aggregation_status"] == "AGGREGATED"
    assert result["coverage_status"] == "FULL"
    assert result["in_count"] == 5
    assert result["out_count"] == 1
    assert result["net_count_delta"] == 4
    assert "occupancy" not in result
    assert "absolute_occupancy" not in result
    assert "absolute occupancy" in str(result["claim_boundary"]).lower()


def test_shuttle_count_window_endpoint_preserves_duplicate_fail_closed_behavior() -> None:
    router = load_router()
    event = valid_event(1)
    result = router.shuttle_count_window(
        {
            "events": [event, event.copy()],
            "expected_vehicle_id": "shuttle-01",
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "min_measurement_confidence": MIN_CONFIDENCE,
        }
    )
    assert result["aggregation_status"] == "REJECTED"
    assert result["descriptive_counts_available"] is False
    assert "DUPLICATE_EVENT_FINGERPRINT" in result["reason_codes"]
    assert result["net_count_delta"] is None


def test_invalid_shuttle_count_api_payload_maps_to_http_422() -> None:
    from fastapi import HTTPException

    router = load_router()
    try:
        router.shuttle_count_window(
            {
                "events": [],
                "expected_vehicle_id": "shuttle-01",
                "window_start": "not-a-time",
                "window_end": WINDOW_END,
                "min_measurement_confidence": MIN_CONFIDENCE,
            }
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert "window_start" in str(exc.detail)
    else:
        raise AssertionError("invalid shuttle count window must map to HTTP 422")


def test_capabilities_exposes_shuttle_count_observations_without_live_claim() -> None:
    router = load_router()
    result = router.capabilities()
    assert "shuttle_count_observations" in result["modules"]
    assert result["automatic_actuation"] is False
    boundary = result["truth_boundary"].lower()
    assert "shuttle" in boundary
    assert "passenger" in boundary or "count" in boundary
    assert "live" in boundary


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle ops API tests")
