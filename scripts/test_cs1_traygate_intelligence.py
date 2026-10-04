#!/usr/bin/env python3
"""Contract tests for the CS1 side of the EHB↔CS1 TrayGate interface."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/traygate.py"
    assert path.exists(), f"missing production module: {path.relative_to(ROOT)}"
    spec = importlib.util.spec_from_file_location("traygate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_capture(**overrides):
    payload = {
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
    payload.update(overrides)
    return payload


def ready_result(*, capture_id="tg-2026-10-04-000123", meal_id="2026-10-04-lunch-north"):
    return {
        "captureId": capture_id,
        "mealId": meal_id,
        "trayId": f"anonymous-{capture_id}",
        "items": [
            {"food": "pilav", "leftoverPercent": 30.0, "confidence": 0.90},
            {"food": "tavuk", "leftoverPercent": 10.0, "confidence": 0.95},
        ],
        "readiness": "READY",
        "modelVersion": "traygate-intelligence-v1",
    }


def test_valid_ehb_capture_is_ready_for_cs1_inference() -> None:
    contract = load_contract()
    result = contract.assess_capture(valid_capture())

    assert result["accepted"] is True
    assert result["readiness"] == "READY_FOR_INFERENCE"
    assert result["reason_codes"] == []
    assert result["capture_id"] == "tg-2026-10-04-000123"


def test_capture_quality_and_privacy_fail_closed() -> None:
    contract = load_contract()

    blurred = contract.assess_capture(valid_capture(captureQuality="BLURRED"))
    assert blurred["accepted"] is False
    assert blurred["readiness"] == "WITHHOLD"
    assert "CAPTURE_QUALITY_BLURRED" in blurred["reason_codes"]

    identified = valid_capture()
    identified["studentId"] = "student-should-not-exist"
    privacy = contract.assess_capture(identified)
    assert privacy["accepted"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_STUDENTID" in privacy["reason_codes"]


def test_capture_requires_timezone_and_stable_capture_metadata() -> None:
    contract = load_contract()
    result = contract.assess_capture(
        valid_capture(
            timestamp="2026-10-04T12:34:56",
            cameraCalibrationVersion="",
            deviceSoftwareVersion="",
        )
    )

    assert result["accepted"] is False
    assert "TIMESTAMP_MUST_BE_TIMEZONE_AWARE" in result["reason_codes"]
    assert "CAMERA_CALIBRATION_VERSION_REQUIRED" in result["reason_codes"]
    assert "DEVICE_SOFTWARE_VERSION_REQUIRED" in result["reason_codes"]


def test_inference_result_enforces_ranges_and_abstention_semantics() -> None:
    contract = load_contract()
    accepted = contract.validate_inference_result(ready_result())
    assert accepted["valid"] is True
    assert accepted["reason_codes"] == []

    invalid = ready_result()
    invalid["items"][0]["leftoverPercent"] = 120
    invalid["items"][1]["confidence"] = 1.2
    rejected = contract.validate_inference_result(invalid)
    assert rejected["valid"] is False
    assert "LEFTOVER_PERCENT_OUT_OF_RANGE" in rejected["reason_codes"]
    assert "CONFIDENCE_OUT_OF_RANGE" in rejected["reason_codes"]

    withheld = ready_result()
    withheld["readiness"] = "WITHHOLD"
    withheld["items"] = []
    assert contract.validate_inference_result(withheld)["valid"] is True


def test_service_aggregation_excludes_non_ready_and_never_invents_mass() -> None:
    contract = load_contract()
    ready_one = ready_result(capture_id="c1")
    ready_two = ready_result(capture_id="c2")
    ready_two["items"][0]["leftoverPercent"] = 50.0

    withheld = ready_result(capture_id="c3")
    withheld["readiness"] = "WITHHOLD"
    withheld["items"] = []

    review = ready_result(capture_id="c4")
    review["readiness"] = "REVIEW_REQUIRED"

    aggregate = contract.aggregate_service_results(
        [ready_one, ready_two, withheld, review],
        meal_id="2026-10-04-lunch-north",
    )

    assert aggregate["capture_count"] == 4
    assert aggregate["ready_capture_count"] == 2
    assert aggregate["withheld_capture_count"] == 1
    assert aggregate["review_required_capture_count"] == 1
    assert aggregate["ready_coverage"] == 0.5
    assert aggregate["food_leftover_percent"]["pilav"]["mean"] == 40.0
    assert aggregate["food_leftover_percent"]["pilav"]["sample_count"] == 2
    assert "waste_kg" not in aggregate
    assert "mass" not in aggregate
    assert aggregate["result_scope"] == "TRAYGATE_PERCENT_ONLY_NO_MASS_CALIBRATION"


def test_service_aggregation_rejects_duplicate_or_cross_service_results() -> None:
    contract = load_contract()
    first = ready_result(capture_id="c1")
    duplicate = ready_result(capture_id="c1")
    try:
        contract.aggregate_service_results(
            [first, duplicate], meal_id="2026-10-04-lunch-north"
        )
    except ValueError as exc:
        assert "duplicate captureId" in str(exc)
    else:
        raise AssertionError("duplicate captureId must fail closed")

    wrong_meal = ready_result(capture_id="c2", meal_id="2026-10-04-dinner-north")
    try:
        contract.aggregate_service_results(
            [first, wrong_meal], meal_id="2026-10-04-lunch-north"
        )
    except ValueError as exc:
        assert "mealId" in str(exc)
    else:
        raise AssertionError("cross-service aggregation must fail closed")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate CS1 contract tests")
