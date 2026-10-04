#!/usr/bin/env python3
"""Fail-closed privacy regressions for nested TrayGate capture/result payloads."""

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


def valid_result(*, capture_id: str = "c1", tray_id: str = "anonymous-c1") -> dict:
    return {
        "captureId": capture_id,
        "mealId": "2026-10-04-lunch-north",
        "trayId": tray_id,
        "items": [
            {"food": "pilav", "leftoverPercent": 30.0, "confidence": 0.90},
            {"food": "tavuk", "leftoverPercent": 10.0, "confidence": 0.95},
        ],
        "readiness": "READY",
        "modelVersion": "traygate-intelligence-v1",
    }


def test_nested_capture_identity_field_fails_closed() -> None:
    contract = load_contract()
    payload = valid_capture()
    payload["metadata"] = {"operator": {"student_id": "must-not-cross-boundary"}}

    result = contract.validate_traygate_capture(payload)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_inference"] is False
    assert result["required_readiness"] == "WITHHOLD"
    assert "PRIVACY_FIELD_NOT_ALLOWED_STUDENTID" in result["reason_codes"]


def test_top_level_result_identity_field_fails_closed() -> None:
    contract = load_contract()
    payload = valid_result()
    payload["buCardId"] = "must-not-cross-boundary"

    result = contract.validate_traygate_result(payload)

    assert result["validation_status"] == "REJECTED"
    assert result["analytics_eligible"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_BUCARDID" in result["reason_codes"]


def test_nested_result_identity_field_fails_closed() -> None:
    contract = load_contract()
    payload = valid_result()
    payload["items"][0]["metadata"] = {
        "diagnostics": {"faceEmbedding": [0.1, 0.2, 0.3]}
    }

    result = contract.validate_traygate_result(payload)

    assert result["validation_status"] == "REJECTED"
    assert result["analytics_eligible"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_FACEEMBEDDING" in result["reason_codes"]


def test_anonymous_result_remains_analytics_eligible() -> None:
    contract = load_contract()
    result = contract.validate_traygate_result(valid_result())

    assert result["validation_status"] == "ACCEPTED"
    assert result["analytics_eligible"] is True
    assert result["reason_codes"] == []


def test_privacy_rejected_result_cannot_contribute_to_service_analytics() -> None:
    contract = load_contract()
    clean = valid_result(capture_id="clean", tray_id="anonymous-clean")
    identity_bearing = valid_result(capture_id="bad", tray_id="anonymous-bad")
    identity_bearing["items"][0]["metadata"] = {"person-id": "forbidden"}

    aggregate = contract.aggregate_traygate_service(
        [clean, identity_bearing],
        expected_meal_id="2026-10-04-lunch-north",
    )

    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["ready_result_count"] == 1
    assert aggregate["excluded_result_count"] == 1
    assert aggregate["ready_fraction"] == 0.5
    assert aggregate["per_food"]["pilav"]["sample_count"] == 1
    assert aggregate["excluded_reason_counts"]["PRIVACY_FIELD_NOT_ALLOWED_PERSONID"] == 1


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} nested/result TrayGate privacy tests")
