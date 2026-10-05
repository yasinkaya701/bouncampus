#!/usr/bin/env python3
"""Regression: benchmark truth must include a cutoff-safe archived weather forecast."""

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


def test_weather_forecast_snapshot_is_required_for_benchmark_admission() -> None:
    contract = load_module(
        "service_truth_weather_regression",
        ROOT / "backend/app/decision/service_truth.py",
    )
    fixtures = load_module(
        "service_truth_contract_fixtures",
        ROOT / "scripts/test_cs1_service_truth_contract.py",
    )

    rows = fixtures.valid_rows()
    for row in rows:
        weather_snapshot = f"weather-forecast:{row['service_date']}:cutoff"
        row["decision_inputs"].append(
            {
                "field": "weather_forecast",
                "snapshot_id": weather_snapshot,
                "available_at": row["decision_cutoff_at"],
                "evidence_class": "EXTERNAL_LIVE",
            }
        )
        row["decision_audit"]["input_snapshot_ids"].append(weather_snapshot)

    missing_weather_row = rows[0]
    missing_weather_snapshot = next(
        item["snapshot_id"]
        for item in missing_weather_row["decision_inputs"]
        if item["field"] == "weather_forecast"
    )
    missing_weather_row["decision_inputs"] = [
        item
        for item in missing_weather_row["decision_inputs"]
        if item["field"] != "weather_forecast"
    ]
    missing_weather_row["decision_audit"]["input_snapshot_ids"] = [
        snapshot_id
        for snapshot_id in missing_weather_row["decision_audit"]["input_snapshot_ids"]
        if snapshot_id != missing_weather_snapshot
    ]

    result = contract.validate_service_truth_dataset(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "REQUIRED_DECISION_INPUT_MISSING_WEATHER_FORECAST" in result["reason_codes"]


if __name__ == "__main__":
    test_weather_forecast_snapshot_is_required_for_benchmark_admission()
    print("ok: weather forecast snapshot admission regression")
