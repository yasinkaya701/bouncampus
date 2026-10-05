#!/usr/bin/env python3
"""Regression contract: weather is optional unless a decision actually uses it."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.service_truth import validate_service_truth_artifact  # noqa: E402
from test_cs1_service_truth_artifact_admission import (  # noqa: E402
    measured_row,
    source_contract,
)


def artifact_without_weather() -> tuple[list[dict], dict]:
    rows = [deepcopy(measured_row(index)) for index in range(3)]
    for row in rows:
        weather_ids = {
            item.get("snapshot_id")
            for item in row["decision_inputs"]
            if item.get("field") == "weather_forecast"
        }
        row["decision_inputs"] = [
            item
            for item in row["decision_inputs"]
            if item.get("field") != "weather_forecast"
        ]
        row["decision_audit"]["input_snapshot_ids"] = [
            snapshot_id
            for snapshot_id in row["decision_audit"]["input_snapshot_ids"]
            if snapshot_id not in weather_ids
        ]

    provenance = deepcopy(source_contract())
    provenance.pop("weather_forecast", None)
    return rows, provenance


def test_weather_is_not_globally_required_when_decision_did_not_use_it() -> None:
    rows, provenance = artifact_without_weather()

    result = validate_service_truth_artifact(
        rows,
        field_provenance=provenance,
    )

    assert result["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert result["eligible_for_benchmark"] is True
    assert "weather_forecast" not in result["source_contract_validation"][
        "required_source_contract_fields"
    ]


def test_declared_weather_still_fails_closed_when_available_after_cutoff() -> None:
    rows = [deepcopy(measured_row(index)) for index in range(3)]
    for item in rows[0]["decision_inputs"]:
        if item.get("field") == "weather_forecast":
            item["available_at"] = "2026-10-01T09:00:00+03:00"
            break

    result = validate_service_truth_artifact(
        rows,
        field_provenance=source_contract(),
    )

    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_NOT_AVAILABLE_AT_CUTOFF" in result["reason_codes"]


def test_declared_weather_requires_matching_source_provenance() -> None:
    rows = [deepcopy(measured_row(index)) for index in range(3)]
    provenance = deepcopy(source_contract())
    provenance.pop("weather_forecast", None)

    result = validate_service_truth_artifact(
        rows,
        field_provenance=provenance,
    )

    assert result["validation_status"] == "SOURCE_CONTRACT_INCOMPLETE"
    assert result["eligible_for_benchmark"] is False
    assert "weather_forecast" in result["source_contract_validation"][
        "missing_source_contract_fields"
    ]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} optional-weather provenance tests")
