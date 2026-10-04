#!/usr/bin/env python3
"""Fail-closed privacy regressions for the anonymous TrayGate capture boundary."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/traygate.py"
    spec = importlib.util.spec_from_file_location("traygate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_capture() -> dict:
    return {
        "deviceId": "traygate-01",
        "captureId": "tg-2026-10-04-000123",
        "timestamp": "2026-10-04T12:34:56+03:00",
        "rgbFrame": "object://traygate/tg-2026-10-04-000123.jpg",
        "depthFrame": None,
        "trayDetected": True,
        "captureQuality": "VALID",
        "cameraCalibrationVersion": "cam-cal-v1",
        "deviceSoftwareVersion": "tg-device-v1",
    }


def test_person_identifiers_fail_closed_across_common_key_styles() -> None:
    contract = load_contract()
    forbidden = (
        "studentId",
        "student_id",
        "person-id",
        "userId",
        "buCardId",
        "faceEmbedding",
        "biometric_id",
        "studentIdentity",
    )

    for key in forbidden:
        payload = valid_capture()
        payload[key] = "must-not-cross-anonymous-traygate-boundary"
        result = contract.validate_traygate_capture(payload)
        normalized = "".join(ch for ch in key.upper() if ch.isalnum())
        assert result["validation_status"] == "REJECTED"
        assert result["eligible_for_inference"] is False
        assert result["required_readiness"] == "WITHHOLD"
        assert f"PRIVACY_FIELD_NOT_ALLOWED_{normalized}" in result["reason_codes"]


def test_anonymous_capture_remains_admissible() -> None:
    contract = load_contract()
    result = contract.validate_traygate_capture(valid_capture())
    assert result["validation_status"] == "ACCEPTED"
    assert result["eligible_for_inference"] is True
    assert result["reason_codes"] == []


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate privacy-boundary tests")
