#!/usr/bin/env python3
"""Regression contract for physical dining count events from EHB nodes."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATION_ID = "north-dining-line-1"
WINDOW_START = "2026-10-04T11:00:00+03:00"
WINDOW_END = "2026-10-04T15:00:00+03:00"


def load_contract():
    path = ROOT / "backend/app/decision/dining_count_truth.py"
    assert path.exists(), "missing production module: backend/app/decision/dining_count_truth.py"
    spec = importlib.util.spec_from_file_location("dining_count_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def count_event(
    index: int,
    *,
    measurement_type: str = "SERVED_TRAY_DELTA",
    value: int = 1,
    unit: str = "TRAYS",
) -> dict:
    return {
        "eventId": f"dining-count-2026-10-04-{index:06d}",
        "deviceId": "serving-counter-north-01",
        "stationId": STATION_ID,
        "timestamp": f"2026-10-04T12:{index:02d}:00+03:00",
        "measurementType": measurement_type,
        "value": value,
        "unit": unit,
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "dining-counter-fw-0.1.0",
        "schemaVersion": "dining-count-event-v1",
    }


def test_valid_physical_count_event_is_admitted_without_truth_promotion() -> None:
    contract = load_contract()
    result = contract.validate_dining_count_event(count_event(1))

    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["aggregation_eligible"] is True
    assert result["measurement_type"] == "SERVED_TRAY_DELTA"
    assert result["count_delta"] == 1
    assert result["event_fingerprint_sha256"]
    assert result["reason_codes"] == []
    assert result["reconciled_service_truth"] is False


def test_nonphysical_or_nonvalid_event_is_withheld_not_promoted() -> None:
    contract = load_contract()
    nonphysical = count_event(2)
    nonphysical["source"] = "GENERATED_SANDBOX"
    result = contract.validate_dining_count_event(nonphysical)
    assert result["validation_status"] == "WITHHOLD"
    assert result["aggregation_eligible"] is False
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in result["reason_codes"]

    low_quality = count_event(3)
    low_quality["quality"] = "SUSPECT"
    result = contract.validate_dining_count_event(low_quality)
    assert result["validation_status"] == "WITHHOLD"
    assert "MEASUREMENT_QUALITY_NOT_VALID" in result["reason_codes"]


def test_identity_bearing_event_is_rejected_and_never_aggregated() -> None:
    contract = load_contract()
    identity_bearing = count_event(10)
    identity_bearing["metadata"] = {"studentId": "should-never-enter-count-contract"}

    result = contract.validate_dining_count_event(identity_bearing)
    assert result["validation_status"] == "REJECTED"
    assert result["aggregation_eligible"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_STUDENTID" in result["reason_codes"]

    aggregate = contract.aggregate_dining_count_events(
        [identity_bearing],
        expected_station_id=STATION_ID,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["descriptive_counts_available"] is False
    assert aggregate["admitted_event_count"] == 0
    assert aggregate["served_trays_observed"] == 0


def test_serving_counter_does_not_promote_trays_to_portions() -> None:
    contract = load_contract()
    unsupported = count_event(
        11,
        measurement_type="SERVED_PORTION_DELTA",
        value=1,
        unit="PORTIONS",
    )

    result = contract.validate_dining_count_event(unsupported)
    assert result["validation_status"] == "REJECTED"
    assert result["aggregation_eligible"] is False
    assert "UNKNOWN_MEASUREMENT_TYPE" in result["reason_codes"]


def test_aggregate_deduplicates_identical_retry_and_sums_only_unique_counts() -> None:
    contract = load_contract()
    produced = count_event(
        4,
        measurement_type="PRODUCED_PORTION_DELTA",
        value=120,
        unit="PORTIONS",
    )
    served = count_event(5, value=73)
    returned = count_event(
        6,
        measurement_type="RETURNED_TRAY_DELTA",
        value=65,
        unit="TRAYS",
    )
    retry = deepcopy(served)

    aggregate = contract.aggregate_dining_count_events(
        [produced, served, retry, returned],
        expected_station_id=STATION_ID,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )

    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["total_event_count"] == 4
    assert aggregate["unique_event_count"] == 3
    assert aggregate["idempotent_replay_count"] == 1
    assert aggregate["admitted_event_count"] == 3
    assert aggregate["produced_portions_observed"] == 120
    assert aggregate["served_trays_observed"] == 73
    assert aggregate["returned_trays_observed"] == 65
    assert aggregate["reconciled_service_truth"] is False
    assert "served_portions_observed" not in aggregate
    assert "actual_served" not in aggregate
    assert "waste_kg" not in aggregate
    assert "actual_surplus_portions" not in aggregate


def test_changed_payload_reusing_event_id_rejects_whole_window() -> None:
    contract = load_contract()
    original = count_event(7, value=10)
    conflict = deepcopy(original)
    conflict["value"] = 11

    aggregate = contract.aggregate_dining_count_events(
        [original, conflict],
        expected_station_id=STATION_ID,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )

    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_counts_available"] is False
    assert "EVENT_ID_REPLAY_CONFLICT" in aggregate["reason_codes"]
    assert aggregate["produced_portions_observed"] is None
    assert aggregate["served_trays_observed"] is None
    assert aggregate["returned_trays_observed"] is None


def test_station_mixing_and_out_of_window_events_fail_closed() -> None:
    contract = load_contract()
    wrong_station = count_event(8)
    wrong_station["stationId"] = "south-dining-line-1"
    aggregate = contract.aggregate_dining_count_events(
        [wrong_station],
        expected_station_id=STATION_ID,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert "STATION_ID_MISMATCH" in aggregate["reason_codes"]

    late = count_event(9)
    late["timestamp"] = "2026-10-04T16:00:00+03:00"
    aggregate = contract.aggregate_dining_count_events(
        [late],
        expected_station_id=STATION_ID,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert "EVENT_OUTSIDE_WINDOW" in aggregate["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} dining physical-count truth tests")
