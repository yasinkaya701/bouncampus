#!/usr/bin/env python3
"""Contract tests for the CS1 side of the TrayGate EHB↔CS1 boundary."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/traygate.py"
    assert path.exists(), "missing production module: backend/app/decision/traygate.py"
    spec = importlib.util.spec_from_file_location("traygate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_capture(*, quality: str = "VALID") -> dict:
    return {
        "deviceId": "traygate-01",
        "captureId": "tg-2026-10-04-000123",
        "timestamp": "2026-10-04T12:34:56+03:00",
        "rgbFrame": "object://traygate/tg-2026-10-04-000123.jpg",
        "depthFrame": None,
        "trayDetected": True,
        "captureQuality": quality,
        "cameraCalibrationVersion": "cam-cal-v1",
        "deviceSoftwareVersion": "tg-device-v1",
    }


def valid_result(*, readiness: str = "READY") -> dict:
    return {
        "captureId": "tg-2026-10-04-000123",
        "mealId": "2026-10-04-lunch-north",
        "trayId": "anonymous-tray-000123",
        "items": [
            {"food": "pilav", "leftoverPercent": 31, "confidence": 0.91},
            {"food": "tavuk", "leftoverPercent": 8, "confidence": 0.94},
        ],
        "readiness": readiness,
        "modelVersion": "traygate-intelligence-v1",
    }


def test_valid_capture_is_admitted_for_inference() -> None:
    contract = load_contract()
    result = contract.validate_traygate_capture(valid_capture())
    assert result["validation_status"] == "ACCEPTED"
    assert result["eligible_for_inference"] is True
    assert result["required_readiness"] is None
    assert result["reason_codes"] == []
    assert result["capture_id"] == "tg-2026-10-04-000123"


def test_non_valid_capture_quality_fails_closed_to_withhold() -> None:
    contract = load_contract()
    for quality in (
        "BLURRED",
        "UNDEREXPOSED",
        "OVEREXPOSED",
        "PARTIAL_TRAY",
        "DEPTH_INVALID",
        "DEVICE_ERROR",
    ):
        result = contract.validate_traygate_capture(valid_capture(quality=quality))
        assert result["validation_status"] == "WITHHOLD"
        assert result["eligible_for_inference"] is False
        assert result["required_readiness"] == "WITHHOLD"
        assert f"CAPTURE_QUALITY_{quality}" in result["reason_codes"]


def test_capture_contract_rejects_unknown_quality_and_naive_timestamp() -> None:
    contract = load_contract()
    capture = valid_capture(quality="MAYBE")
    capture["timestamp"] = "2026-10-04T12:34:56"
    result = contract.validate_traygate_capture(capture)
    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_inference"] is False
    assert "UNKNOWN_CAPTURE_QUALITY" in result["reason_codes"]
    assert "TIMESTAMP_MUST_BE_TIMEZONE_AWARE" in result["reason_codes"]


def test_capture_requires_stable_identity_and_rgb_reference() -> None:
    contract = load_contract()
    capture = valid_capture()
    capture["deviceId"] = ""
    capture["rgbFrame"] = None
    capture["cameraCalibrationVersion"] = ""
    result = contract.validate_traygate_capture(capture)
    assert result["validation_status"] == "REJECTED"
    assert "DEVICE_ID_REQUIRED" in result["reason_codes"]
    assert "RGB_FRAME_REQUIRED" in result["reason_codes"]
    assert "CAMERA_CALIBRATION_VERSION_REQUIRED" in result["reason_codes"]


def test_ready_inference_result_requires_bounded_item_measurements() -> None:
    contract = load_contract()
    accepted = contract.validate_traygate_result(valid_result())
    assert accepted["validation_status"] == "ACCEPTED"
    assert accepted["analytics_eligible"] is True
    assert accepted["reason_codes"] == []

    invalid = valid_result()
    invalid["items"][0]["leftoverPercent"] = 101
    invalid["items"][1]["confidence"] = -0.1
    rejected = contract.validate_traygate_result(invalid)
    assert rejected["validation_status"] == "REJECTED"
    assert rejected["analytics_eligible"] is False
    assert "INVALID_LEFTOVER_PERCENT" in rejected["reason_codes"]
    assert "INVALID_CONFIDENCE" in rejected["reason_codes"]


def test_withhold_result_may_abstain_without_fabricating_items() -> None:
    contract = load_contract()
    result_payload = valid_result(readiness="WITHHOLD")
    result_payload["items"] = []
    result = contract.validate_traygate_result(result_payload)
    assert result["validation_status"] == "WITHHOLD"
    assert result["analytics_eligible"] is False
    assert "MODEL_WITHHELD" in result["reason_codes"]


def test_result_capture_id_must_match_admitted_capture() -> None:
    contract = load_contract()
    result = contract.validate_traygate_result(
        valid_result(),
        expected_capture_id="tg-other",
    )
    assert result["validation_status"] == "REJECTED"
    assert result["analytics_eligible"] is False
    assert "CAPTURE_ID_MISMATCH" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate contract tests")
