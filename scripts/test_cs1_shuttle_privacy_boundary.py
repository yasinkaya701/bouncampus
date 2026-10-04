#!/usr/bin/env python3
"""Privacy regression for EE shuttle passenger-count measurements consumed by CS1."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_CONFIDENCE = 0.85


def load_contract():
    path = ROOT / "backend/app/decision/shuttle_truth.py"
    spec = importlib.util.spec_from_file_location("shuttle_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_event() -> dict:
    return {
        "deviceId": "counter-door-a",
        "vehicleId": "shuttle-01",
        "timestamp": "2026-10-04T08:05:00+03:00",
        "direction": "IN",
        "countDelta": 1,
        "quality": "VALID",
        "measurementConfidence": 0.95,
        "evidenceClass": "PHYSICAL_MEASUREMENT",
    }


def assert_privacy_rejected(event: dict) -> None:
    contract = load_contract()
    result = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "REJECTED"
    assert result["decision_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in result["reason_codes"]


def test_top_level_student_identity_is_rejected() -> None:
    event = valid_event()
    event["studentId"] = "student-123"
    assert_privacy_rejected(event)


def test_nested_card_or_person_identity_is_rejected() -> None:
    event = valid_event()
    event["metadata"] = {
        "sensorHealth": "OK",
        "capture": {"cardId": "card-991", "personName": "Example Person"},
    }
    assert_privacy_rejected(event)


def test_non_identity_operational_metadata_remains_allowed() -> None:
    contract = load_contract()
    event = valid_event()
    event["metadata"] = {
        "sensorHealth": "OK",
        "firmwareVersion": "1.2.3",
        "doorId": "front-a",
    }
    result = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["decision_eligible"] is True
    assert result["reason_codes"] == []


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle privacy-boundary contract tests")
