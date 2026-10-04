#!/usr/bin/env python3
"""Regression: service-level benchmark truth must remain anonymous/aggregate."""

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


def test_identity_bearing_fields_are_rejected_even_when_nested() -> None:
    contract = load_module(ROOT / "backend/app/decision/service_truth.py", "service_truth")
    fixtures = load_module(
        ROOT / "scripts/test_cs1_service_truth_contract.py",
        "service_truth_contract_fixtures",
    )
    rows = fixtures.valid_rows()
    rows[0]["metadata"] = {
        "source": "operator-export",
        "studentId": "must-not-enter-service-truth",
    }

    result = contract.validate_service_truth_dataset(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_STUDENTID" in result["reason_codes"]


def test_identity_free_aggregate_service_rows_remain_accepted() -> None:
    contract = load_module(ROOT / "backend/app/decision/service_truth.py", "service_truth")
    fixtures = load_module(
        ROOT / "scripts/test_cs1_service_truth_contract.py",
        "service_truth_contract_fixtures_ok",
    )
    result = contract.validate_service_truth_dataset(fixtures.valid_rows())

    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["eligible_for_benchmark"] is True


if __name__ == "__main__":
    test_identity_bearing_fields_are_rejected_even_when_nested()
    test_identity_free_aggregate_service_rows_remain_accepted()
    print("ok: service-truth privacy regressions")