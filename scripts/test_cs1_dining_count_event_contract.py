#!/usr/bin/env python3
"""Contract tests for CS1 admission of EHB dining count-node events."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOW_START = "2026-10-04T11:00:00+03:00"
WINDOW_END = "2026-10-04T15:00:00+03:00"


def load_contract():
    path = ROOT / "backend/app/decision/dining_count_events.py"
    assert path.exists(), "missing production module: backend/app/decision/dining_count_events.py"
    spec = importlib.util.spec_from_file_location("dining_count_events", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_event(
    index: int = 1,
    *,
    event_id: str | None = None,
    station_id: str = "north-serving-line-a",
    measurement_type: str = "SERVED_PORTIONS",
    value: int = 1,
    quality: str = "VALID",
    source: str = "PHYSICAL_MEASUREMENT",
    timestamp: str | None = None,
) -> dict:
    return {
        "eventId": event_id or f"count-event-{index}",
        "deviceId": "count-node-01",
        "stationId": station_id,
        "timestamp": timestamp or f"2026-10-04T12:{index:02d}:00+03:00",
        "measurementType": measurement_type,
        "value": value,
        "unit": "count",
        "quality": quality,
        "source": source,
        "firmwareVersion": "1.0.0",
        "schemaVersion": "DINING_COUNT_EVENT_V1",
    }


def test_valid_physical_count_event_is_admitted_only_as_descriptive_evidence() -> None:
    contract = load_contract()
    result = contract.validate_dining_count_event(valid_event())
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["descriptive_eligible"] is True
    assert result["reason_codes"] == []
    assert result["event_id"] == "count-event-1"
    assert result["benchmark_truth_eligible"] is False


def test_malformed_or_non_physical_events_fail_closed() -> None:
    contract = load_contract()

    malformed = valid_event()
    malformed["eventId"] = ""
    malformed["timestamp"] = "2026-10-04T12:01:00"
    malformed["measurementType"] = "WASTE_KG"
    malformed["value"] = 0
    malformed["unit"] = "kg"
    result = contract.validate_dining_count_event(malformed)
    assert result["validation_status"] == "REJECTED"
    for code in (
        "EVENT_ID_REQUIRED",
        "TIMESTAMP_MUST_BE_TIMEZONE_AWARE",
        "UNSUPPORTED_MEASUREMENT_TYPE",
        "COUNT_VALUE_MUST_BE_POSITIVE_INTEGER",
        "COUNT_UNIT_REQUIRED",
    ):
        assert code in result["reason_codes"]

    non_physical = contract.validate_dining_count_event(
        valid_event(source="MODEL_ESTIMATE")
    )
    assert non_physical["validation_status"] == "WITHHOLD"
    assert non_physical["descriptive_eligible"] is False
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in non_physical["reason_codes"]

    low_quality = contract.validate_dining_count_event(valid_event(quality="DEGRADED"))
    assert low_quality["validation_status"] == "WITHHOLD"
    assert "MEASUREMENT_QUALITY_NOT_VALID" in low_quality["reason_codes"]


def test_identical_event_id_retry_is_idempotently_deduplicated() -> None:
    contract = load_contract()
    event = valid_event(value=3)
    aggregate = contract.aggregate_dining_count_events(
        [event, dict(event)],
        expected_station_id="north-serving-line-a",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["total_event_count"] == 2
    assert aggregate["unique_event_count"] == 1
    assert aggregate["idempotent_replay_count"] == 1
    assert aggregate["admitted_event_count"] == 1
    assert aggregate["served_portion_count"] == 3


def test_changed_payload_reusing_event_id_rejects_whole_window() -> None:
    contract = load_contract()
    first = valid_event(value=2)
    changed = dict(first)
    changed["value"] = 4
    aggregate = contract.aggregate_dining_count_events(
        [first, changed],
        expected_station_id="north-serving-line-a",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_counts_available"] is False
    assert aggregate["reason_codes"] == ["EVENT_ID_REPLAY_CONFLICT"]
    assert aggregate["produced_portion_count"] is None
    assert aggregate["served_portion_count"] is None
    assert aggregate["returned_tray_count"] is None


def test_aggregate_keeps_count_types_descriptive_and_separate() -> None:
    contract = load_contract()
    events = [
        valid_event(1, measurement_type="PRODUCED_PORTIONS", value=10),
        valid_event(2, measurement_type="SERVED_PORTIONS", value=8),
        valid_event(3, measurement_type="RETURNED_TRAYS", value=7),
    ]
    aggregate = contract.aggregate_dining_count_events(
        events,
        expected_station_id="north-serving-line-a",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["coverage_status"] == "FULL"
    assert aggregate["produced_portion_count"] == 10
    assert aggregate["served_portion_count"] == 8
    assert aggregate["returned_tray_count"] == 7
    for forbidden in (
        "actual_served",
        "actual_surplus_portions",
        "waste_kg",
        "shortage_or_early_sellout",
        "operator_status_quo_quantity",
        "benchmark_truth",
    ):
        assert forbidden not in aggregate
    assert aggregate["benchmark_truth_eligible"] is False


def test_station_or_time_scope_mismatch_rejects_aggregate() -> None:
    contract = load_contract()
    mixed_station = contract.aggregate_dining_count_events(
        [valid_event(1), valid_event(2, station_id="south-serving-line-a")],
        expected_station_id="north-serving-line-a",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert mixed_station["aggregation_status"] == "REJECTED"
    assert "STATION_ID_MISMATCH" in mixed_station["reason_codes"]

    out_of_window = contract.aggregate_dining_count_events(
        [valid_event(1, timestamp="2026-10-04T15:00:00+03:00")],
        expected_station_id="north-serving-line-a",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert out_of_window["aggregation_status"] == "REJECTED"
    assert "EVENT_OUTSIDE_WINDOW" in out_of_window["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} dining count-event contract tests")
