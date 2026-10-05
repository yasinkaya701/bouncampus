#!/usr/bin/env python3
"""Regression lock for repository-generated datasets that must never become measured truth."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "backend/data/PROVENANCE.json"

EXPECTED_GENERATED = {
    "occupancy_history.csv",
    "energy_consumption.csv",
    "cafeteria_sales.csv",
    "user_food_preferences.csv",
    "weather_history.csv",
}


def test_historical_generated_datasets_are_explicitly_sandbox_only() -> None:
    assert MANIFEST.exists(), "backend/data/PROVENANCE.json must classify generated datasets"
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert payload["manifest_version"] == "DATA_PROVENANCE_V1"
    datasets = payload["datasets"]
    assert EXPECTED_GENERATED <= set(datasets)

    for filename in EXPECTED_GENERATED:
        entry = datasets[filename]
        assert entry["evidence_class"] == "GENERATED_SANDBOX"
        assert entry["method_eligibility"] == "SANDBOX_ONLY"
        assert entry["measured_truth_eligible"] is False
        assert entry["source_kind"] == "HISTORICAL_REPOSITORY_GENERATOR"


def test_cafeteria_sales_is_not_service_truth_or_benchmark_evidence() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cafeteria = payload["datasets"]["cafeteria_sales.csv"]

    assert cafeteria["evidence_class"] == "GENERATED_SANDBOX"
    assert cafeteria["measured_truth_eligible"] is False
    assert cafeteria["service_truth_eligible"] is False
    assert cafeteria["benchmark_eligible"] is False
    assert "base_demand" in cafeteria["generation_semantics"]
    assert "actual_served" not in cafeteria.get("verified_operational_fields", [])


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} generated-data provenance regressions")
