#!/usr/bin/env python3
"""Regression contract for weather snapshots in service-truth admission."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixtures():
    return load_module(
        "service_truth_artifact_fixtures",
        ROOT / "scripts/test_cs1_service_truth_artifact_admission.py",
    )


def _contract():
    return load_module(
        "service_truth_weather_contract",
        ROOT / "backend/app/decision/service_truth.py",
    )


def _rows_with_weather() -> list[dict]:
    fixtures = _fixtures()
    rows = [fixtures.measured_row(0), fixtures.measured_row(1), fixtures.measured_row(2)]
    for row in rows:
        snapshot_id = f"weather-forecast-{row['service_date']}-cutoff"
        row["decision_inputs"].append(
            {
                "field": "weather_forecast",
                "snapshot_id": snapshot_id,
                "available_at": row["decision_cutoff_at"],
                "evidence_class": "OFFICIAL_SNAPSHOT",
            }
        )
        row["decision_audit"]["input_snapshot_ids"].append(snapshot_id)
    return rows


def test_weather_forecast_snapshot_is_required_for_dataset_admission() -> None:
    contract = _contract()
    fixtures = _fixtures()
    rows = [fixtures.measured_row(0), fixtures.measured_row(1), fixtures.measured_row(2)]

    result = contract.validate_service_truth_dataset(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "REQUIRED_DECISION_INPUT_MISSING_WEATHER_FORECAST" in result["reason_codes"]


def test_weather_forecast_source_contract_is_required_for_artifact_admission() -> None:
    contract = _contract()
    fixtures = _fixtures()

    result = contract.validate_service_truth_artifact(
        _rows_with_weather(),
        field_provenance=fixtures.source_contract(),
    )

    assert result["validation_status"] == "SOURCE_CONTRACT_INCOMPLETE"
    assert result["eligible_for_benchmark"] is False
    assert "weather_forecast" in result["source_contract_validation"]["missing_source_contract_fields"]
    assert "SOURCE_CONTRACT_INCOMPLETE" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth weather contract tests")
