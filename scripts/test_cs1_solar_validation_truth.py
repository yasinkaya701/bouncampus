#!/usr/bin/env python3
"""Regression contract for CS1 consumption of EE solar-validation measurements."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.solar_validation_truth import validate_solar_validation_event


def valid_event() -> dict:
    return {
        "deviceId": "solar-node-north-01",
        "stationId": "north-building-room-301-west-window",
        "timestamp": "2026-10-05T11:30:00+03:00",
        "measurementType": "IRRADIANCE",
        "value": 412.5,
        "unit": "W_M2",
        "orientationDeg": 270.0,
        "tiltDeg": 90.0,
        "placement": {
            "buildingId": "north-building",
            "roomId": "301",
            "surface": "WEST_WINDOW",
            "position": "INTERIOR_GLAZING_PLANE",
        },
        "quality": "VALID",
        "calibrationVersion": "solar-cal-2026-10-v1",
        "evidenceClass": "PHYSICAL_MEASUREMENT",
    }


def test_valid_physical_event_is_descriptive_measurement_only() -> None:
    result = validate_solar_validation_event(valid_event())
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["measurement_eligible"] is True
    assert result["decision_eligible"] is False
    assert result["model_validation_eligible"] is False
    assert result["automatic_actuation"] is False
    assert result["impact_claim_allowed"] is False
    assert result["event_fingerprint_sha256"]
    assert result["reason_codes"] == []


def test_geometry_and_calibration_metadata_fail_closed_when_missing() -> None:
    event = valid_event()
    del event["orientationDeg"]
    del event["tiltDeg"]
    del event["placement"]
    del event["calibrationVersion"]
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "REJECTED"
    assert result["measurement_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    assert result["placement"] is None
    assert "ORIENTATION_REQUIRED" in result["reason_codes"]
    assert "TILT_REQUIRED" in result["reason_codes"]
    assert "PLACEMENT_REQUIRED" in result["reason_codes"]
    assert "CALIBRATION_VERSION_REQUIRED" in result["reason_codes"]


def test_orientation_tilt_value_and_timestamp_are_structurally_bounded() -> None:
    event = valid_event()
    event["timestamp"] = "2026-10-05T11:30:00"
    event["orientationDeg"] = 361
    event["tiltDeg"] = 91
    event["value"] = float("nan")
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "REJECTED"
    assert result["placement"] is None
    assert "TIMESTAMP_MUST_BE_TIMEZONE_AWARE" in result["reason_codes"]
    assert "INVALID_ORIENTATION_DEG" in result["reason_codes"]
    assert "INVALID_TILT_DEG" in result["reason_codes"]
    assert "INVALID_MEASUREMENT_VALUE" in result["reason_codes"]


def test_non_valid_or_non_physical_event_is_withheld_not_promoted() -> None:
    event = valid_event()
    event["quality"] = "DEGRADED"
    event["evidenceClass"] = "SIMULATION"
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "WITHHOLD"
    assert result["measurement_eligible"] is False
    assert result["decision_eligible"] is False
    assert result["placement"] == event["placement"]
    assert "MEASUREMENT_QUALITY_NOT_VALID" in result["reason_codes"]
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in result["reason_codes"]


def test_identity_bearing_nested_metadata_is_rejected_before_fingerprinting() -> None:
    event = valid_event()
    event["placement"]["diagnostics"] = {"studentId": "forbidden"}
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "REJECTED"
    assert result["measurement_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    assert result["placement"] is None
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in result["reason_codes"]


def test_operational_device_station_and_room_identifiers_remain_allowed() -> None:
    event = valid_event()
    event["placement"]["sensorMountId"] = "mount-west-03"
    event["placement"]["facadeId"] = "north-building-west"
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["measurement_eligible"] is True


def test_orientation_360_is_canonicalized_to_north_for_stable_fingerprint() -> None:
    north = valid_event()
    north["orientationDeg"] = 0
    wrapped_north = valid_event()
    wrapped_north["orientationDeg"] = 360
    first = validate_solar_validation_event(north)
    second = validate_solar_validation_event(wrapped_north)
    assert first["validation_status"] == "ACCEPTED_MEASURED"
    assert second["validation_status"] == "ACCEPTED_MEASURED"
    assert second["orientation_deg"] == 0.0
    assert first["event_fingerprint_sha256"] == second["event_fingerprint_sha256"]


def test_non_json_placement_metadata_is_rejected_before_fingerprinting() -> None:
    event = valid_event()
    event["placement"]["diagnosticTags"] = {"west", "window"}
    result = validate_solar_validation_event(event)
    assert result["validation_status"] == "REJECTED"
    assert result["measurement_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    assert result["placement"] is None
    assert "PLACEMENT_MUST_BE_JSON_SERIALIZABLE" in result["reason_codes"]


def test_fingerprint_is_stable_for_semantically_identical_payload() -> None:
    first = validate_solar_validation_event(valid_event())
    second = validate_solar_validation_event(valid_event())
    assert first["event_fingerprint_sha256"] == second["event_fingerprint_sha256"]


def test_claim_boundary_does_not_overstate_solar_model_or_energy_validation() -> None:
    result = validate_solar_validation_event(valid_event())
    boundary = result["claim_boundary"].lower()
    assert "descriptive" in boundary
    assert "model" in boundary
    assert "energy" in boundary
    assert "savings" in boundary


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} solar validation truth regressions")
