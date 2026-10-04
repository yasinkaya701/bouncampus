#!/usr/bin/env python3
"""Contract tests for service-level dining truth admission."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/service_truth.py"
    assert path.exists(), "missing production module: backend/app/decision/service_truth.py"
    spec = importlib.util.spec_from_file_location("service_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measured_row(day: int, *, evidence_class: str = "OFFICIAL_OPERATIONAL_EXPORT") -> dict:
    date = f"2026-09-{day:02d}"
    return {
        "service_id": f"NORTH-LUNCH-{date}",
        "granularity": "CAMPUS_MEAL_SERVICE",
        "service_date": date,
        "campus_id": "NORTH",
        "meal_period": "LUNCH",
        "decision_cutoff_at": f"{date}T08:00:00+03:00",
        "actual_served": 100 + day,
        "produced_portions": 110 + day,
        "actual_surplus_portions": 10,
        "waste_kg": None,
        "shortage_or_early_sellout": False,
        "outcome_reconciled": True,
        "outcome_source_record_id": f"ops:{date}:north:lunch",
        "evidence_class": evidence_class,
        "operator_status_quo_quantity": 108 + day,
        "reservation_workflow_active": False,
        "active_reservations_at_cutoff": None,
        "decision_inputs": [
            {
                "field": "menu",
                "snapshot_id": f"menu:{date}",
                "available_at": f"2026-09-{day - 1:02d}T12:00:00+03:00",
                "evidence_class": "OFFICIAL_PUBLIC",
            },
            {
                "field": "academic_calendar",
                "snapshot_id": "calendar:2026-fall-v1",
                "available_at": "2026-09-01T00:00:00+03:00",
                "evidence_class": "OFFICIAL_PUBLIC",
            },
        ],
    }


def valid_rows(*, evidence_class: str = "OFFICIAL_OPERATIONAL_EXPORT") -> list[dict]:
    return [measured_row(day, evidence_class=evidence_class) for day in (28, 29, 30)]


def test_accepts_measured_chronological_service_truth_and_hashes_it() -> None:
    contract = load_contract()
    result = contract.validate_service_truth_dataset(valid_rows())
    assert result["validation_status"] == "ACCEPTED_MEASURED"
    assert result["eligible_for_benchmark"] is True
    assert result["service_count"] == 3
    assert result["reason_codes"] == []
    assert len(result["artifact_checksum_sha256"]) == 64
    assert result["chronological_service_ids"][0].endswith("2026-09-28")
    assert result["contract_version"] == "SERVICE_TRUTH_V1"


def test_checksum_is_order_independent_for_same_rows() -> None:
    contract = load_contract()
    forward = contract.validate_service_truth_dataset(valid_rows())
    reverse = contract.validate_service_truth_dataset(list(reversed(valid_rows())))
    assert forward["artifact_checksum_sha256"] == reverse["artifact_checksum_sha256"]
    assert forward["chronological_service_ids"] == reverse["chronological_service_ids"]


def test_duplicate_service_id_fails_closed() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[1]["service_id"] = rows[0]["service_id"]
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DUPLICATE_SERVICE_ID" in result["reason_codes"]


def test_unreconciled_or_untraceable_outcome_is_rejected() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[1]["outcome_reconciled"] = False
    rows[1]["outcome_source_record_id"] = ""
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "UNRECONCILED_OUTCOME" in result["reason_codes"]
    assert "OUTCOME_SOURCE_RECORD_ID_REQUIRED" in result["reason_codes"]


def test_decision_input_published_after_cutoff_is_rejected() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["decision_inputs"][0]["available_at"] = "2026-09-28T09:00:00+03:00"
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "DECISION_INPUT_NOT_AVAILABLE_AT_CUTOFF" in result["reason_codes"]


def test_required_menu_and_calendar_snapshots_must_be_immutable_and_preknown() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["decision_inputs"] = [
        {
            "field": "menu",
            "snapshot_id": "",
            "available_at": "2026-09-27T12:00:00+03:00",
            "evidence_class": "OFFICIAL_PUBLIC",
        }
    ]
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "DECISION_INPUT_SNAPSHOT_ID_REQUIRED" in result["reason_codes"]
    assert "REQUIRED_DECISION_INPUT_MISSING_ACADEMIC_CALENDAR" in result["reason_codes"]


def test_reservation_count_is_required_only_when_workflow_is_active() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["reservation_workflow_active"] = True
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "ACTIVE_RESERVATIONS_REQUIRED_FOR_ACTIVE_WORKFLOW" in result["reason_codes"]


def test_served_reservation_decomposition_must_reconcile_when_present() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["reservation_served"] = 80
    rows[0]["unreserved_served"] = rows[0]["actual_served"] - 81
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "SERVED_DEMAND_DECOMPOSITION_MISMATCH" in result["reason_codes"]

    rows = valid_rows()
    rows[0]["reservation_served"] = 80
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "SERVED_DEMAND_DECOMPOSITION_INCOMPLETE" in result["reason_codes"]


def test_decision_audit_snapshots_must_resolve_to_known_inputs() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["decision_audit"] = {
        "input_snapshot_ids": [
            rows[0]["decision_inputs"][0]["snapshot_id"],
            "unknown:future-or-untracked-snapshot",
        ]
    }
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT" in result["reason_codes"]


def test_generated_sandbox_never_becomes_benchmark_truth() -> None:
    contract = load_contract()
    rows = valid_rows(evidence_class="GENERATED_SANDBOX")
    strict = contract.validate_service_truth_dataset(rows)
    assert strict["validation_status"] == "REJECTED"
    assert strict["eligible_for_benchmark"] is False
    assert "MEASURED_EVIDENCE_REQUIRED" in strict["reason_codes"]

    sandbox = contract.validate_service_truth_dataset(rows, require_measured=False)
    assert sandbox["validation_status"] == "SANDBOX_ONLY"
    assert sandbox["eligible_for_benchmark"] is False
    assert "GENERATED_SANDBOX_NOT_BENCHMARK_TRUTH" in sandbox["reason_codes"]


def test_aggregate_or_too_small_dataset_is_rejected() -> None:
    contract = load_contract()
    row = measured_row(28)
    row["granularity"] = "MONTHLY_CAMPUS_TOTAL"
    result = contract.validate_service_truth_dataset([row])
    assert result["validation_status"] == "REJECTED"
    assert "SERVICE_LEVEL_GRANULARITY_REQUIRED" in result["reason_codes"]
    assert "INSUFFICIENT_CHRONOLOGICAL_SERVICES" in result["reason_codes"]


def test_naive_timestamps_and_negative_measures_are_rejected() -> None:
    contract = load_contract()
    rows = valid_rows()
    rows[0]["decision_cutoff_at"] = "2026-09-28T08:00:00"
    rows[1]["actual_served"] = -1
    result = contract.validate_service_truth_dataset(rows)
    assert result["validation_status"] == "REJECTED"
    assert "DECISION_CUTOFF_MUST_BE_TIMEZONE_AWARE" in result["reason_codes"]
    assert "INVALID_ACTUAL_SERVED" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth contract tests")
