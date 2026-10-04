#!/usr/bin/env python3
"""CS1 contract tests for anonymous RoomNode physical measurements.

RoomNode measurements remain descriptive physical observations. They must not be
promoted to calibrated occupancy truth, energy savings, or automatic actuation.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/roomnode_truth.py"
    spec = importlib.util.spec_from_file_location("roomnode_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_event(
    event_id: str,
    measurement_type: str,
    value: int | float,
    unit: str,
    *,
    timestamp: str = "2026-10-04T14:05:00+03:00",
) -> dict:
    return {
        "eventId": event_id,
        "deviceId": "roomnode-nb-301-a",
        "stationId": "north-building-room-301",
        "timestamp": timestamp,
        "measurementType": measurement_type,
        "value": value,
        "unit": unit,
        "quality": "VALID",
        "source": "PHYSICAL_MEASUREMENT",
        "firmwareVersion": "0.1.0",
        "schemaVersion": "ROOMNODE_EVENT_V1",
        "metadata": {"sensorHealth": "OK", "gatewayId": "gw-north-1"},
    }


def test_supported_physical_measurements_are_admitted_without_claim_upgrade() -> None:
    contract = load_contract()
    cases = [
        ("OCCUPANCY_COUNT", 17, "PEOPLE"),
        ("CO2_PPM", 742.5, "PPM"),
        ("AIR_TEMPERATURE_C", 22.4, "CELSIUS"),
        ("RELATIVE_HUMIDITY_PERCENT", 44.0, "PERCENT"),
    ]
    for index, (measurement_type, value, unit) in enumerate(cases):
        result = contract.validate_roomnode_event(
            valid_event(f"event-{index}", measurement_type, value, unit)
        )
        assert result["validation_status"] == "ACCEPTED_MEASURED"
        assert result["measurement_eligible"] is True
        assert result["decision_eligible"] is False
        assert result["reason_codes"] == []
        assert len(result["event_fingerprint_sha256"]) == 64
        assert result["impact_claim_allowed"] is False


def test_type_unit_and_value_semantics_fail_closed() -> None:
    contract = load_contract()

    wrong_unit = valid_event("wrong-unit", "CO2_PPM", 700, "PEOPLE")
    wrong_unit_result = contract.validate_roomnode_event(wrong_unit)
    assert wrong_unit_result["validation_status"] == "REJECTED"
    assert "MEASUREMENT_UNIT_MISMATCH" in wrong_unit_result["reason_codes"]

    fractional_people = valid_event("fractional", "OCCUPANCY_COUNT", 4.5, "PEOPLE")
    fractional_result = contract.validate_roomnode_event(fractional_people)
    assert fractional_result["validation_status"] == "REJECTED"
    assert "OCCUPANCY_COUNT_MUST_BE_NONNEGATIVE_INTEGER" in fractional_result["reason_codes"]

    bad_humidity = valid_event("humidity", "RELATIVE_HUMIDITY_PERCENT", 101, "PERCENT")
    humidity_result = contract.validate_roomnode_event(bad_humidity)
    assert humidity_result["validation_status"] == "REJECTED"
    assert "RELATIVE_HUMIDITY_OUT_OF_RANGE" in humidity_result["reason_codes"]


def test_identity_bearing_metadata_is_rejected_before_fingerprint() -> None:
    contract = load_contract()
    event = valid_event("privacy", "CO2_PPM", 700, "PPM")
    event["metadata"]["capture"] = {"studentId": "should-never-enter-roomnode-truth"}

    result = contract.validate_roomnode_event(event)

    assert result["validation_status"] == "REJECTED"
    assert result["measurement_eligible"] is False
    assert result["event_fingerprint_sha256"] is None
    assert "IDENTITY_BEARING_PAYLOAD_FORBIDDEN" in result["reason_codes"]


def test_nonvalid_or_nonphysical_observations_are_withheld_not_upgraded() -> None:
    contract = load_contract()
    degraded = valid_event("degraded", "CO2_PPM", 700, "PPM")
    degraded["quality"] = "DEGRADED"
    degraded_result = contract.validate_roomnode_event(degraded)
    assert degraded_result["validation_status"] == "WITHHOLD"
    assert degraded_result["measurement_eligible"] is False
    assert "MEASUREMENT_QUALITY_NOT_VALID" in degraded_result["reason_codes"]

    modeled = valid_event("modeled", "AIR_TEMPERATURE_C", 22, "CELSIUS")
    modeled["source"] = "MODEL_ESTIMATE"
    modeled_result = contract.validate_roomnode_event(modeled)
    assert modeled_result["validation_status"] == "WITHHOLD"
    assert modeled_result["measurement_eligible"] is False
    assert "PHYSICAL_MEASUREMENT_SOURCE_REQUIRED" in modeled_result["reason_codes"]


def test_window_summary_deduplicates_exact_retries_and_rejects_conflicting_event_ids() -> None:
    contract = load_contract()
    occupancy = valid_event("occ-1", "OCCUPANCY_COUNT", 17, "PEOPLE")
    co2 = valid_event("co2-1", "CO2_PPM", 742, "PPM", timestamp="2026-10-04T14:06:00+03:00")

    summary = contract.summarize_roomnode_window(
        [occupancy, occupancy.copy(), co2],
        station_id="north-building-room-301",
        window_start="2026-10-04T14:00:00+03:00",
        window_end="2026-10-04T14:15:00+03:00",
    )
    assert summary["aggregation_status"] == "DESCRIPTIVE_ONLY"
    assert summary["total_event_count"] == 3
    assert summary["unique_event_count"] == 2
    assert summary["idempotent_replay_count"] == 1
    assert summary["per_measurement"]["OCCUPANCY_COUNT"]["sample_count"] == 1
    assert summary["per_measurement"]["OCCUPANCY_COUNT"]["mean"] == 17.0
    assert summary["decision_eligible"] is False
    assert summary["impact_claim_allowed"] is False

    conflict = occupancy.copy()
    conflict["value"] = 18
    rejected = contract.summarize_roomnode_window(
        [occupancy, conflict],
        station_id="north-building-room-301",
        window_start="2026-10-04T14:00:00+03:00",
        window_end="2026-10-04T14:15:00+03:00",
    )
    assert rejected["aggregation_status"] == "REJECTED"
    assert "EVENT_ID_REPLAY_CONFLICT" in rejected["reason_codes"]
    assert rejected["per_measurement"] == {}


def test_window_summary_rejects_station_or_time_leakage() -> None:
    contract = load_contract()
    wrong_station = valid_event("station", "CO2_PPM", 700, "PPM")
    wrong_station["stationId"] = "south-room-101"
    outside = valid_event(
        "outside",
        "CO2_PPM",
        700,
        "PPM",
        timestamp="2026-10-04T15:00:00+03:00",
    )
    result = contract.summarize_roomnode_window(
        [wrong_station, outside],
        station_id="north-building-room-301",
        window_start="2026-10-04T14:00:00+03:00",
        window_end="2026-10-04T14:15:00+03:00",
    )
    assert result["aggregation_status"] == "REJECTED"
    assert "STATION_ID_MISMATCH" in result["reason_codes"]
    assert "EVENT_OUTSIDE_WINDOW" in result["reason_codes"]
    assert result["per_measurement"] == {}


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} RoomNode measurement-truth contract tests")
