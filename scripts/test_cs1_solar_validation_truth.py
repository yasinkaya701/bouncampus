#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/solar_validation_truth.py"
    if not path.exists():
        raise AssertionError("solar validation truth boundary missing")
    spec = importlib.util.spec_from_file_location("cs1_solar_validation_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_valid_physical_observation_is_measured_but_not_decision_eligible() -> None:
    policy = load_policy()
    result = policy.validate_solar_validation_event(
        {
            "eventId": "solar-evt-001",
            "deviceId": "solar-node-01",
            "stationId": "north-campus-facade-south-01",
            "timestamp": "2026-10-05T09:00:00+03:00",
            "measurementType": "SOLAR_IRRADIANCE",
            "value": 412.5,
            "unit": "W_PER_M2",
            "orientationAzimuthDeg": 180.0,
            "tiltDeg": 90.0,
            "placement": "EXTERIOR_FACADE_REFERENCE",
            "quality": "VALID",
            "calibrationVersion": "cal-2026-10-a",
            "evidenceClass": "PHYSICAL_MEASUREMENT",
            "firmwareVersion": "0.1.0",
            "schemaVersion": "solar-validation-v1",
        }
    )

    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["measurement_eligible"] is True
    assert result["decision_eligible"] is False
    assert result["model_validation_claim_allowed"] is False
    assert result["impact_claim_allowed"] is False
    assert result["automatic_actuation"] is False
    assert result["reason_codes"] == []
    assert result["event_fingerprint_sha256"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} solar-validation-truth tests")
