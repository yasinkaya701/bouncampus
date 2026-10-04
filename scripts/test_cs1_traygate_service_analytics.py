#!/usr/bin/env python3
"""Regression tests for TrayGate privacy hardening and service aggregation."""

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


def ready_result(*, capture_id="c1", meal_id="2026-10-04-lunch-north"):
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


def test_capture_rejects_person_identity_fields() -> None:
    contract = load_contract()

    for forbidden_key in ("studentId", "student_id", "person-id", "faceEmbedding"):
        capture = valid_capture()
        capture[forbidden_key] = "must-not-cross-traygate-boundary"
        result = contract.validate_traygate_capture(capture)
        assert result["validation_status"] == "REJECTED"
        assert result["eligible_for_inference"] is False
        normalized = "".join(ch for ch in forbidden_key.upper() if ch.isalnum())
        assert f"PRIVACY_FIELD_NOT_ALLOWED_{normalized}" in result["reason_codes"]


def test_service_aggregation_uses_only_ready_results() -> None:
    contract = load_contract()
    ready_one = ready_result(capture_id="c1")
    ready_two = ready_result(capture_id="c2")
    ready_two["items"][0]["leftoverPercent"] = 50.0

    withheld = ready_result(capture_id="c3")
    withheld["readiness"] = "WITHHOLD"
    withheld["items"] = []

    review = ready_result(capture_id="c4")
    review["readiness"] = "REVIEW_REQUIRED"

    aggregate = contract.aggregate_traygate_service_results(
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
    assert aggregate["result_scope"] == "TRAYGATE_PERCENT_ONLY_NO_MASS_CALIBRATION"


def test_service_aggregation_never_invents_mass_metrics() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_traygate_service_results(
        [ready_result()],
        meal_id="2026-10-04-lunch-north",
    )

    assert "waste_kg" not in aggregate
    assert "mass" not in aggregate
    serialized_keys = " ".join(aggregate.keys()).lower()
    assert "gram" not in serialized_keys
    assert "kg" not in serialized_keys


def test_service_aggregation_rejects_duplicate_capture_ids() -> None:
    contract = load_contract()
    first = ready_result(capture_id="same")
    duplicate = ready_result(capture_id="same")

    try:
        contract.aggregate_traygate_service_results(
            [first, duplicate], meal_id="2026-10-04-lunch-north"
        )
    except ValueError as exc:
        assert "duplicate captureId" in str(exc)
    else:
        raise AssertionError("duplicate captureId must fail closed")


def test_service_aggregation_rejects_cross_service_mixing() -> None:
    contract = load_contract()
    lunch = ready_result(capture_id="c1")
    dinner = ready_result(
        capture_id="c2", meal_id="2026-10-04-dinner-north"
    )

    try:
        contract.aggregate_traygate_service_results(
            [lunch, dinner], meal_id="2026-10-04-lunch-north"
        )
    except ValueError as exc:
        assert "mealId" in str(exc)
    else:
        raise AssertionError("cross-service aggregation must fail closed")


def test_service_aggregation_rejects_structurally_invalid_results() -> None:
    contract = load_contract()
    invalid = ready_result()
    invalid["items"][0]["leftoverPercent"] = 101.0

    try:
        contract.aggregate_traygate_service_results(
            [invalid], meal_id="2026-10-04-lunch-north"
        )
    except ValueError as exc:
        assert "invalid TrayGate result" in str(exc)
    else:
        raise AssertionError("invalid result must fail closed")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate service-analytics tests")
