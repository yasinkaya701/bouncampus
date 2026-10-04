#!/usr/bin/env python3
"""Fail-closed hardening regressions for CS1 dining truth intake."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dining = _load(ROOT / "backend/app/decision/dining_truth.py", "cs1_dining_truth_hardening")
contract = _load(ROOT / "scripts/test_cs1_dining_truth_contract.py", "cs1_dining_truth_contract_fixture")


def test_service_without_reservation_workflow_can_omit_reservation_snapshot() -> None:
    row = contract.sandbox_row()
    reservation_id = row["context"]["reservation"]["snapshot_id"]
    del row["context"]["reservation"]
    row["decision_audit"]["input_snapshot_ids"].remove(reservation_id)

    result = dining.assess_service_row(row)

    assert result["contract_complete"] is True, result
    assert result["decision_audit_complete"] is True, result
    assert result["benchmark_eligible"] is False


def test_after_cutoff_snapshot_cannot_satisfy_decision_audit_provenance() -> None:
    row = contract.sandbox_row()
    row["context"]["reservation"]["available_at"] = "2026-09-30T18:00:01+03:00"

    result = dining.assess_service_row(row)

    assert result["contract_complete"] is False
    assert result["decision_audit_complete"] is False
    assert "CONTEXT_AFTER_DECISION_CUTOFF_RESERVATION" in result["reason_codes"]
    assert "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT" in result["reason_codes"]


def test_incomplete_decision_audit_blocks_measured_row_benchmark_eligibility() -> None:
    row = copy.deepcopy(contract.sandbox_row())
    row["evidence_class"] = dining.MEASURED_EVIDENCE_CLASS
    row["decision_audit"]["input_snapshot_ids"].append("unknown-cutoff-input")

    result = dining.assess_service_row(row)

    assert result["decision_audit_complete"] is False
    assert result["contract_complete"] is False
    assert result["benchmark_eligible"] is False
    assert "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT" in result["reason_codes"]


def main() -> int:
    tests = [
        test_service_without_reservation_workflow_can_omit_reservation_snapshot,
        test_after_cutoff_snapshot_cannot_satisfy_decision_audit_provenance,
        test_incomplete_decision_audit_blocks_measured_row_benchmark_eligibility,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
