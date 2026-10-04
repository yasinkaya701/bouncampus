#!/usr/bin/env python3
"""Contract tests for service-level aggregation of admitted TrayGate results."""

from __future__ import annotations

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


def ready_result(index: int, *, meal_id: str = MEAL_ID) -> dict:
    return {
        "captureId": f"tg-2026-10-04-{index:06d}",
        "mealId": meal_id,
        "trayId": f"anonymous-tray-{index:06d}",
        "items": [
            {"food": "pilav", "leftoverPercent": 20 + 10 * index, "confidence": 0.9},
            {"food": "tavuk", "leftoverPercent": 5 + 5 * index, "confidence": 0.95},
        ],
        "readiness": "READY",
        "modelVersion": "traygate-intelligence-v1",
    }


def abstained_result(index: int, *, readiness: str = "WITHHOLD") -> dict:
    result = ready_result(index)
    result["readiness"] = readiness
    if readiness == "WITHHOLD":
        result["items"] = []
    return result


def test_aggregates_only_ready_results_with_explicit_coverage() -> None:
    contract = load_contract()
    results = [
        ready_result(1),
        ready_result(2),
        abstained_result(3, readiness="WITHHOLD"),
        abstained_result(4, readiness="REVIEW_REQUIRED"),
    ]
    aggregate = contract.aggregate_traygate_service(results, expected_meal_id=MEAL_ID)

    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["descriptive_analytics_available"] is True
    assert aggregate["total_result_count"] == 4
    assert aggregate["ready_result_count"] == 2
    assert aggregate["excluded_result_count"] == 2
    assert aggregate["ready_fraction"] == 0.5
    assert aggregate["coverage_status"] == "PARTIAL"
    assert aggregate["per_food"]["pilav"] == {
        "sample_count": 2,
        "mean_leftover_percent": 35.0,
        "min_leftover_percent": 30.0,
        "max_leftover_percent": 40.0,
    }
    assert aggregate["per_food"]["tavuk"]["mean_leftover_percent"] == 12.5
    assert aggregate["excluded_reason_counts"]["MODEL_WITHHELD"] == 1
    assert aggregate["excluded_reason_counts"]["MODEL_REVIEW_REQUIRED"] == 1
    assert "waste_kg" not in aggregate
    assert "estimated_grams" not in aggregate


def test_full_ready_set_reports_full_coverage() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_traygate_service(
        [ready_result(1), ready_result(2)],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["coverage_status"] == "FULL"
    assert aggregate["ready_fraction"] == 1.0
    assert aggregate["reason_codes"] == []


def test_invalid_result_is_excluded_and_reason_is_counted() -> None:
    contract = load_contract()
    invalid = ready_result(9)
    invalid["items"][0]["leftoverPercent"] = 130
    aggregate = contract.aggregate_traygate_service(
        [ready_result(1), invalid],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["ready_result_count"] == 1
    assert aggregate["excluded_result_count"] == 1
    assert aggregate["excluded_reason_counts"]["INVALID_LEFTOVER_PERCENT"] == 1
    assert aggregate["coverage_status"] == "PARTIAL"


def test_duplicate_capture_or_tray_rejects_whole_aggregate() -> None:
    contract = load_contract()
    first = ready_result(1)
    duplicate_capture = ready_result(2)
    duplicate_capture["captureId"] = first["captureId"]
    aggregate = contract.aggregate_traygate_service(
        [first, duplicate_capture],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_analytics_available"] is False
    assert "DUPLICATE_CAPTURE_ID" in aggregate["reason_codes"]
    assert aggregate["per_food"] == {}

    duplicate_tray = ready_result(2)
    duplicate_tray["trayId"] = first["trayId"]
    aggregate = contract.aggregate_traygate_service(
        [first, duplicate_tray],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert "DUPLICATE_TRAY_ID" in aggregate["reason_codes"]


def test_cross_meal_mixing_rejects_whole_aggregate() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_traygate_service(
        [ready_result(1), ready_result(2, meal_id="2026-10-04-dinner-north")],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_analytics_available"] is False
    assert "MEAL_ID_MISMATCH" in aggregate["reason_codes"]
    assert aggregate["per_food"] == {}


def test_no_ready_results_is_explicit_and_not_analytics_available() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_traygate_service(
        [abstained_result(1), abstained_result(2, readiness="REVIEW_REQUIRED")],
        expected_meal_id=MEAL_ID,
    )
    assert aggregate["aggregation_status"] == "NO_READY_RESULTS"
    assert aggregate["descriptive_analytics_available"] is False
    assert aggregate["coverage_status"] == "NONE"
    assert aggregate["ready_fraction"] == 0.0
    assert aggregate["per_food"] == {}


def test_aggregation_is_order_independent_for_same_admitted_results() -> None:
    contract = load_contract()
    rows = [ready_result(1), ready_result(2), abstained_result(3)]
    forward = contract.aggregate_traygate_service(rows, expected_meal_id=MEAL_ID)
    reverse = contract.aggregate_traygate_service(list(reversed(rows)), expected_meal_id=MEAL_ID)
    assert forward["per_food"] == reverse["per_food"]
    assert forward["ready_fraction"] == reverse["ready_fraction"]
    assert forward["excluded_reason_counts"] == reverse["excluded_reason_counts"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} TrayGate service aggregation tests")
