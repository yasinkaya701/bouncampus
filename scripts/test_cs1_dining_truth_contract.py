#!/usr/bin/env python3
"""Contract tests for fail-closed CS1 dining service-truth intake.

All row fixtures in this file are explicitly GENERATED_SANDBOX. They exercise
schema/cutoff semantics only and must never be interpreted as measured campus data.
"""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_dining_truth():
    path = ROOT / "backend/app/decision/dining_truth.py"
    assert path.exists(), "missing production module: backend/app/decision/dining_truth.py"
    spec = importlib.util.spec_from_file_location("cs1_dining_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sandbox_row(service_id: str = "sandbox-north-lunch-2026-10-01") -> dict:
    return {
        "service_id": service_id,
        "service_date": "2026-10-01",
        "campus_id": "north",
        "meal_period": "lunch",
        "decision_cutoff_at": "2026-09-30T18:00:00+03:00",
        "evidence_class": "GENERATED_SANDBOX",
        "outcome": {
            "actual_served": 108,
            "produced_portions": 115,
            "actual_surplus_portions": 7,
            "shortage_or_early_sellout": False,
            "reconciled": True,
            "source_record_id": "sandbox-outcome-001",
            "reservation_served": 80,
            "unreserved_served": 28,
        },
        "operator_estimate": {
            "value": 110,
            "snapshot_id": "sandbox-operator-001",
            "available_at": "2026-09-30T17:30:00+03:00",
        },
        "context": {
            "menu": {
                "snapshot_id": "sandbox-menu-001",
                "available_at": "2026-09-29T12:00:00+03:00",
            },
            "academic_calendar": {
                "snapshot_id": "sandbox-calendar-001",
                "available_at": "2026-09-01T09:00:00+03:00",
            },
            "weather_forecast": {
                "snapshot_id": "sandbox-weather-001",
                "available_at": "2026-09-30T12:00:00+03:00",
            },
            "reservation": {
                "snapshot_id": "sandbox-reservation-001",
                "available_at": "2026-09-30T17:55:00+03:00",
                "active_at_cutoff": 100,
                "coverage_scope": "SANDBOX_ONLY",
            },
        },
        "decision_audit": {
            "baseline_version": "sandbox-baseline-v1",
            "method_version": "sandbox-method-v1",
            "recommended_quantity": 112,
            "operator_action": "FOLLOWED",
            "input_snapshot_ids": [
                "sandbox-operator-001",
                "sandbox-menu-001",
                "sandbox-calendar-001",
                "sandbox-weather-001",
                "sandbox-reservation-001",
            ],
        },
    }


def source_contract() -> dict:
    return {
        "actual_served": {
            "owner": "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "source_system": "SERVICE_RECONCILIATION_EXPORT_TO_BE_CONFIRMED",
            "availability_semantics": "POST_SERVICE_RECONCILED",
        },
        "produced_portions": {
            "owner": "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "source_system": "PRODUCTION_RECORD_TO_BE_CONFIRMED",
            "availability_semantics": "POST_PRODUCTION_RECORDED",
        },
        "surplus_or_waste": {
            "owner": "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "source_system": "SURPLUS_OR_WASTE_RECORD_TO_BE_CONFIRMED",
            "availability_semantics": "POST_SERVICE_MEASURED",
        },
        "shortage_or_early_sellout": {
            "owner": "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "source_system": "SERVICE_STATUS_RECORD_TO_BE_CONFIRMED",
            "availability_semantics": "POST_SERVICE_RECORDED",
        },
        "operator_estimate": {
            "owner": "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "source_system": "OPERATOR_PLAN_TO_BE_CONFIRMED",
            "availability_semantics": "MUST_EXIST_BY_DECISION_CUTOFF",
        },
        "menu": {
            "owner": "OFFICIAL_DINING_MENU",
            "source_system": "OFFICIAL_MENU_SNAPSHOT",
            "availability_semantics": "MUST_EXIST_BY_DECISION_CUTOFF",
        },
        "academic_calendar": {
            "owner": "OFFICIAL_ACADEMIC_CALENDAR",
            "source_system": "OFFICIAL_CALENDAR_SNAPSHOT",
            "availability_semantics": "MUST_EXIST_BY_DECISION_CUTOFF",
        },
        "weather_forecast": {
            "owner": "ARCHIVED_FORECAST_PROVIDER",
            "source_system": "HISTORICAL_FORECAST_SNAPSHOT",
            "availability_semantics": "FORECAST_MUST_HAVE_BEEN_AVAILABLE_BY_DECISION_CUTOFF",
        },
    }


def test_sandbox_row_can_be_contract_complete_but_never_benchmark_truth() -> None:
    dining = load_dining_truth()
    result = dining.assess_service_row(sandbox_row())
    assert result["contract_complete"] is True
    assert result["benchmark_eligible"] is False
    assert "GENERATED_SANDBOX_NOT_BENCHMARK_TRUTH" in result["reason_codes"]
    assert result["truth_boundary"] == "REAL_RECONCILED_SERVICE_LEVEL_MEASUREMENTS_ONLY"
    assert result["reservation_semantics"] == "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND"


def test_context_snapshot_after_cutoff_fails_closed() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    row["context"]["menu"]["available_at"] = "2026-09-30T18:00:01+03:00"
    result = dining.assess_service_row(row)
    assert result["contract_complete"] is False
    assert "CONTEXT_AFTER_DECISION_CUTOFF_MENU" in result["reason_codes"]


def test_unreconciled_outcome_is_not_training_eligible() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    row["outcome"]["reconciled"] = False
    result = dining.assess_service_row(row)
    assert result["contract_complete"] is False
    assert result["benchmark_eligible"] is False
    assert "OUTCOME_NOT_RECONCILED" in result["reason_codes"]


def test_surplus_or_waste_measurement_is_required() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    del row["outcome"]["actual_surplus_portions"]
    result = dining.assess_service_row(row)
    assert result["contract_complete"] is False
    assert "SURPLUS_OR_WASTE_MEASUREMENT_REQUIRED" in result["reason_codes"]


def test_reservation_decomposition_must_reconcile_when_present() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    row["outcome"]["unreserved_served"] = 27
    result = dining.assess_service_row(row)
    assert result["contract_complete"] is False
    assert "SERVED_DEMAND_DECOMPOSITION_MISMATCH" in result["reason_codes"]


def test_decision_audit_snapshot_ids_must_match_available_inputs() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    row["decision_audit"]["input_snapshot_ids"].append("sandbox-future-mystery-source")
    result = dining.assess_service_row(row)
    assert result["decision_audit_complete"] is False
    assert "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT" in result["reason_codes"]


def test_dataset_freeze_is_deterministic_and_never_promotes_sandbox() -> None:
    dining = load_dining_truth()
    rows = [
        sandbox_row("sandbox-north-lunch-2026-10-01"),
        sandbox_row("sandbox-north-dinner-2026-10-01"),
    ]
    rows[1]["meal_period"] = "dinner"
    first = dining.freeze_dataset(
        rows,
        dataset_id="sandbox-contract-test",
        field_provenance=source_contract(),
    )
    second = dining.freeze_dataset(
        list(reversed(copy.deepcopy(rows))),
        dataset_id="sandbox-contract-test",
        field_provenance=copy.deepcopy(source_contract()),
    )
    assert first["data_sha256"] == second["data_sha256"]
    assert first["source_contract_sha256"] == second["source_contract_sha256"]
    assert first["row_count"] == 2
    assert first["contract_complete_row_count"] == 2
    assert first["benchmark_eligible_row_count"] == 0
    assert first["generated_sandbox_row_count"] == 2
    assert first["source_contract_complete"] is True
    assert first["promotion_scope"] == "OFFLINE_BENCHMARK_INPUT_ONLY_AFTER_REAL_MEASURED_DATA"


def test_dataset_freeze_rejects_duplicate_service_ids() -> None:
    dining = load_dining_truth()
    row = sandbox_row()
    try:
        dining.freeze_dataset(
            [row, copy.deepcopy(row)],
            dataset_id="sandbox-duplicate-test",
            field_provenance=source_contract(),
        )
    except ValueError as exc:
        assert "duplicate service_id" in str(exc)
    else:
        raise AssertionError("duplicate service ids must fail closed")


def test_source_contract_exposes_missing_operational_ownership() -> None:
    dining = load_dining_truth()
    contract = source_contract()
    del contract["actual_served"]
    frozen = dining.freeze_dataset(
        [sandbox_row()],
        dataset_id="sandbox-missing-source-contract",
        field_provenance=contract,
    )
    assert frozen["source_contract_complete"] is False
    assert "actual_served" in frozen["missing_source_contract_fields"]


def main() -> int:
    tests = [
        test_sandbox_row_can_be_contract_complete_but_never_benchmark_truth,
        test_context_snapshot_after_cutoff_fails_closed,
        test_unreconciled_outcome_is_not_training_eligible,
        test_surplus_or_waste_measurement_is_required,
        test_reservation_decomposition_must_reconcile_when_present,
        test_decision_audit_snapshot_ids_must_match_available_inputs,
        test_dataset_freeze_is_deterministic_and_never_promotes_sandbox,
        test_dataset_freeze_rejects_duplicate_service_ids,
        test_source_contract_exposes_missing_operational_ownership,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
