#!/usr/bin/env python3
"""Contract tests for CS1 admission of EE shuttle passenger-count measurements."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOW_START = "2026-10-04T08:00:00+03:00"
WINDOW_END = "2026-10-04T09:00:00+03:00"
MIN_CONFIDENCE = 0.85


def load_contract():
    path = ROOT / "backend/app/decision/shuttle_truth.py"
    assert path.exists(), "missing production module: backend/app/decision/shuttle_truth.py"
    spec = importlib.util.spec_from_file_location("shuttle_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_event(
    index: int = 1,
    *,
    direction: str = "IN",
    count_delta: int = 1,
    confidence: float = 0.95,
    quality: str = "VALID",
    evidence_class: str = "PHYSICAL_MEASUREMENT",
    vehicle_id: str = "shuttle-01",
    timestamp: str | None = None,
) -> dict:
    return {
        "deviceId": "counter-door-a",
        "vehicleId": vehicle_id,
        "timestamp": timestamp or f"2026-10-04T08:{index:02d}:00+03:00",
        "direction": direction,
        "countDelta": count_delta,
        "quality": quality,
        "measurementConfidence": confidence,
        "evidenceClass": evidence_class,
    }


def test_valid_physical_event_is_decision_eligible_and_fingerprinted() -> None:
    contract = load_contract()
    event = valid_event()
    result = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["decision_eligible"] is True
    assert result["reason_codes"] == []
    assert len(result["event_fingerprint_sha256"]) == 64

    same_instant = valid_event(timestamp="2026-10-04T05:01:00+00:00")
    same_result = contract.validate_shuttle_count_event(
        same_instant,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert same_result["event_fingerprint_sha256"] == result["event_fingerprint_sha256"]


def test_explicit_non_valid_quality_fails_closed_without_redefining_ee_labels() -> None:
    contract = load_contract()
    result = contract.validate_shuttle_count_event(
        valid_event(quality="OCCLUDED"),
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "WITHHOLD"
    assert result["decision_eligible"] is False
    assert "MEASUREMENT_QUALITY_NOT_VALID" in result["reason_codes"]


def test_confidence_threshold_is_caller_supplied_and_fail_closed() -> None:
    contract = load_contract()
    event = valid_event(confidence=0.88)

    accepted = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=0.85,
    )
    assert accepted["decision_eligible"] is True

    withheld = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=0.90,
    )
    assert withheld["validation_status"] == "WITHHOLD"
    assert "MEASUREMENT_CONFIDENCE_BELOW_THRESHOLD" in withheld["reason_codes"]


def test_non_physical_evidence_cannot_enter_decision_truth() -> None:
    contract = load_contract()
    result = contract.validate_shuttle_count_event(
        valid_event(evidence_class="MODEL_ESTIMATE"),
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "WITHHOLD"
    assert result["decision_eligible"] is False
    assert "PHYSICAL_MEASUREMENT_REQUIRED" in result["reason_codes"]


def test_malformed_event_is_rejected() -> None:
    contract = load_contract()
    event = valid_event()
    event["deviceId"] = ""
    event["vehicleId"] = ""
    event["timestamp"] = "2026-10-04T08:01:00"
    event["direction"] = "SIDEWAYS"
    event["countDelta"] = 0
    event["measurementConfidence"] = 1.2

    result = contract.validate_shuttle_count_event(
        event,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert result["validation_status"] == "REJECTED"
    assert result["decision_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    for code in (
        "DEVICE_ID_REQUIRED",
        "VEHICLE_ID_REQUIRED",
        "TIMESTAMP_MUST_BE_TIMEZONE_AWARE",
        "INVALID_DIRECTION",
        "COUNT_DELTA_MUST_BE_POSITIVE_INTEGER",
        "INVALID_MEASUREMENT_CONFIDENCE",
    ):
        assert code in result["reason_codes"]


def test_service_window_aggregates_only_admitted_physical_counts() -> None:
    contract = load_contract()
    events = [
        valid_event(1, direction="IN", count_delta=3),
        valid_event(2, direction="IN", count_delta=2),
        valid_event(3, direction="OUT", count_delta=1),
    ]
    aggregate = contract.aggregate_shuttle_count_events(
        events,
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["descriptive_counts_available"] is True
    assert aggregate["total_event_count"] == 3
    assert aggregate["admitted_event_count"] == 3
    assert aggregate["excluded_event_count"] == 0
    assert aggregate["coverage_status"] == "FULL"
    assert aggregate["in_count"] == 5
    assert aggregate["out_count"] == 1
    assert aggregate["net_count_delta"] == 4
    assert "occupancy" not in aggregate
    assert "absolute_occupancy" not in aggregate


def test_withheld_events_are_excluded_with_explicit_partial_coverage() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_shuttle_count_events(
        [
            valid_event(1, direction="IN", count_delta=2),
            valid_event(2, direction="OUT", confidence=0.4),
            valid_event(3, quality="OCCLUDED"),
        ],
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert aggregate["aggregation_status"] == "AGGREGATED"
    assert aggregate["coverage_status"] == "PARTIAL"
    assert aggregate["admitted_event_count"] == 1
    assert aggregate["excluded_event_count"] == 2
    assert aggregate["admitted_fraction"] == 1 / 3
    assert aggregate["in_count"] == 2
    assert aggregate["out_count"] == 0
    assert aggregate["net_count_delta"] == 2
    assert aggregate["excluded_reason_counts"]["MEASUREMENT_CONFIDENCE_BELOW_THRESHOLD"] == 1
    assert aggregate["excluded_reason_counts"]["MEASUREMENT_QUALITY_NOT_VALID"] == 1


def test_duplicate_replay_rejects_whole_window() -> None:
    contract = load_contract()
    event = valid_event(1)
    aggregate = contract.aggregate_shuttle_count_events(
        [event, dict(event)],
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert aggregate["aggregation_status"] == "REJECTED"
    assert aggregate["descriptive_counts_available"] is False
    assert "DUPLICATE_EVENT_FINGERPRINT" in aggregate["reason_codes"]
    assert aggregate["in_count"] is None
    assert aggregate["out_count"] is None
    assert aggregate["net_count_delta"] is None


def test_mixed_vehicle_or_out_of_window_event_rejects_scope() -> None:
    contract = load_contract()
    mixed = contract.aggregate_shuttle_count_events(
        [valid_event(1), valid_event(2, vehicle_id="shuttle-99")],
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert mixed["aggregation_status"] == "REJECTED"
    assert "VEHICLE_ID_MISMATCH" in mixed["reason_codes"]

    out_of_window = contract.aggregate_shuttle_count_events(
        [valid_event(1), valid_event(2, timestamp="2026-10-04T09:00:00+03:00")],
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert out_of_window["aggregation_status"] == "REJECTED"
    assert "EVENT_OUTSIDE_WINDOW" in out_of_window["reason_codes"]


def test_empty_or_fully_withheld_window_never_becomes_observed_occupancy() -> None:
    contract = load_contract()
    aggregate = contract.aggregate_shuttle_count_events(
        [valid_event(1, confidence=0.2), valid_event(2, quality="OCCLUDED")],
        expected_vehicle_id="shuttle-01",
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        min_measurement_confidence=MIN_CONFIDENCE,
    )
    assert aggregate["aggregation_status"] == "NO_ADMITTED_MEASUREMENTS"
    assert aggregate["descriptive_counts_available"] is False
    assert aggregate["coverage_status"] == "NONE"
    assert aggregate["admitted_event_count"] == 0
    assert aggregate["in_count"] == 0
    assert aggregate["out_count"] == 0
    assert aggregate["net_count_delta"] == 0
    assert "occupancy" not in aggregate


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shuttle measurement-truth contract tests")
