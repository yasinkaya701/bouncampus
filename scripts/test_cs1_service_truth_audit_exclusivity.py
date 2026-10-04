#!/usr/bin/env python3
"""Regression: one service decision audit must carry exactly one recommendation shape."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_decision_audit_rejects_quantity_and_band_together() -> None:
    contract = load_module(ROOT / "backend/app/decision/service_truth.py", "service_truth")
    fixtures = load_module(
        ROOT / "scripts/test_cs1_service_truth_contract.py",
        "service_truth_contract_fixtures",
    )
    rows = fixtures.valid_rows()
    rows[0]["decision_audit"]["recommended_quantity_band"] = {
        "lower": 100,
        "upper": 120,
    }

    result = contract.validate_service_truth_dataset(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_AUDIT_AMBIGUOUS_RECOMMENDATION" in result["reason_codes"]


if __name__ == "__main__":
    test_decision_audit_rejects_quantity_and_band_together()
    print("ok: decision-audit recommendation exclusivity regression")
