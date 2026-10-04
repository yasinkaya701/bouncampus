#!/usr/bin/env python3
"""Regression tests for idempotent TrayGate store-and-forward retries."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEAL_ID = "2026-10-04-lunch-north"


def load_contract():
    path = ROOT / "backend/app/decision/traygate.py"
    assert path.exists(), "missing production module: backend/app/decision/traygate.py"
    spec = importlib.util.spec_from_file_location("traygate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ready_result(index: int) -> dict:
    return {
        "captureId": f"tg-2026-10-04-{index:06d}",
        "mealId": MEAL_ID,
        "trayId": f"anonymous-tray-{index:06d}",
        "items": [
            {"food": "pilav", "leftoverPercent": 30, "confidence": 0.91},
            {"food": "tavuk", "leftoverPercent": 8, "confidence": 0.94},
        ],
        "readiness": "READY",
        "modelVersion": "traygate-intelligence-v1",
    }


def test_identical_capture_replay_is_counted_once_without_rejecting_service() -> None:
    contract = load_contract()
    original = ready_result(1)
    replay = deepcopy(original)

    aggregate = contract.aggregate_traygate_service(
        [original, replay],
        expected_meal_id=MEAL_ID,
    )

    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["descriptive_analytics_available"] is True
    assert aggregate["total_result_count"] == 2
    assert aggregate["unique_result_count"] == 1
    assert aggregate["idempotent_replay_count"] == 1
    assert aggregate["ready_result_count"] == 1
    assert aggregate["excluded_result_count"] == 0
    assert aggregate["ready_fraction"] == 1.0
    assert aggregate["coverage_status"] == "FULL"
    assert aggregate["per_food"]["pilav"]["sample_count"] == 1
    assert aggregate["reason_codes"] == []


def test_same_capture_id_with_changed_payload_rejects_service() -> None:
    contract = load_contract()
    original = ready_result(2)
    conflicting_retry = deepcopy(original)
    conflicting_retry["items"][0]["leftoverPercent"] = 85

    aggregate = contract.aggregate_traygate_service(
        [original, conflicting_retry],
        expected_meal_id=MEAL_ID,
    )

    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_analytics_available"] is False
    assert aggregate["reason_codes"] == ["CAPTURE_ID_REPLAY_CONFLICT"]
    assert aggregate["per_food"] == {}


def test_distinct_capture_ids_cannot_reuse_same_tray_id() -> None:
    contract = load_contract()
    first = ready_result(3)
    duplicate_tray = ready_result(4)
    duplicate_tray["trayId"] = first["trayId"]

    aggregate = contract.aggregate_traygate_service(
        [first, duplicate_tray],
        expected_meal_id=MEAL_ID,
    )

    assert aggregate["aggregation_status"] == "REJECTED"
    assert "DUPLICATE_TRAY_ID" in aggregate["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate idempotent replay tests")
