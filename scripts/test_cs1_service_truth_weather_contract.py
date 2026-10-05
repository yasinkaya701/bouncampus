#!/usr/bin/env python3
"""Regression contract for cutoff-safe archived weather in service-truth admission."""

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


def fixtures():
    return load_module(
        "service_truth_artifact_fixtures_weather",
        ROOT / "scripts/test_cs1_service_truth_artifact_admission.py",
    )


def contract():
    return load_module(
        "service_truth_weather_contract",
        ROOT / "backend/app/decision/service_truth.py",
    )


def rows() -> list[dict]:
    fx = fixtures()
    return [fx.measured_row(0), fx.measured_row(1), fx.measured_row(2)]


def weather_input(row: dict) -> dict:
    return next(
        item for item in row["decision_inputs"] if item.get("field") == "weather_forecast"
    )


def test_weather_forecast_snapshot_is_required_for_dataset_admission() -> None:
    module = contract()
    data = rows()
    for row in data:
        removed = weather_input(row)
        row["decision_inputs"].remove(removed)
        row["decision_audit"]["input_snapshot_ids"].remove(removed["snapshot_id"])

    result = module.validate_service_truth_dataset(data)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "REQUIRED_DECISION_INPUT_MISSING_WEATHER_FORECAST" in result["reason_codes"]


def test_weather_forecast_published_after_cutoff_is_rejected() -> None:
    module = contract()
    data = rows()
    weather_input(data[0])["available_at"] = "2026-10-01T09:00:00+03:00"

    result = module.validate_service_truth_dataset(data)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_NOT_AVAILABLE_AT_CUTOFF" in result["reason_codes"]
    assert "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT" in result["reason_codes"]


def test_weather_forecast_source_contract_is_required_for_artifact_admission() -> None:
    module = contract()
    fx = fixtures()
    provenance = fx.source_contract()
    del provenance["weather_forecast"]

    result = module.validate_service_truth_artifact(
        rows(),
        field_provenance=provenance,
    )

    assert result["validation_status"] == "SOURCE_CONTRACT_INCOMPLETE"
    assert result["eligible_for_benchmark"] is False
    assert "weather_forecast" in result["source_contract_validation"]["missing_source_contract_fields"]
    assert "SOURCE_CONTRACT_INCOMPLETE" in result["reason_codes"]


def test_content_bound_pre_cutoff_weather_is_eligible_but_not_accuracy_proof() -> None:
    module = contract()
    fx = fixtures()

    result = module.validate_service_truth_artifact(
        rows(),
        field_provenance=fx.source_contract(),
    )

    assert result["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert result["eligible_for_benchmark"] is True
    assert "forecast value" in result["dataset_validation"]["claim_boundary"]
    assert "model value" in result["claim_boundary"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth weather contract tests")
