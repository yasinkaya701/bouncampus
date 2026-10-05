#!/usr/bin/env python3
"""Contract tests for source-bound CS1 service-truth artifact admission."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/service_truth.py"
    spec = importlib.util.spec_from_file_location("service_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot_sha256(snapshot_id: str) -> str:
    return hashlib.sha256(snapshot_id.encode("utf-8")).hexdigest()


def measured_row(index: int, *, evidence_class: str = "OFFICIAL_OPERATIONAL_EXPORT") -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    cutoff = f"2026-10-{day:02d}T08:00:00+03:00"
    menu_snapshot = f"menu-{service_date}-lunch"
    calendar_snapshot = "calendar-2026-fall-v1"
    return {
        "service_id": f"north-lunch-{service_date}",
        "granularity": "CAMPUS_MEAL_SERVICE",
        "service_date": service_date,
        "campus_id": "north",
        "meal_period": "lunch",
        "decision_cutoff_at": cutoff,
        "actual_served": 100 + index,
        "produced_portions": 110 + index,
        "actual_surplus_portions": 10,
        "shortage_or_early_sellout": False,
        "outcome_reconciled": True,
        "outcome_source_record_id": f"ops-record-{index}",
        "operator_status_quo_quantity": 108 + index,
        "reservation_workflow_active": False,
        "evidence_class": evidence_class,
        "decision_inputs": [
            {
                "field": "menu",
                "snapshot_id": menu_snapshot,
                "snapshot_sha256": snapshot_sha256(menu_snapshot),
                "available_at": f"2026-10-{day:02d}T07:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
            {
                "field": "academic_calendar",
                "snapshot_id": calendar_snapshot,
                "snapshot_sha256": snapshot_sha256(calendar_snapshot),
                "available_at": "2026-09-01T00:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
        ],
        "decision_audit": {
            "method_version": "operator-status-quo-v1",
            "recommended_quantity": 108 + index,
            "operator_action": "ACCEPT_RECOMMENDATION",
            "input_snapshot_ids": [menu_snapshot, calendar_snapshot],
        },
    }


def source_contract(*, verified: bool = True) -> dict:
    verification_status = "VERIFIED" if verified else "UNVERIFIED"

    def entry(owner: str, source_system: str, availability_semantics: str) -> dict:
        return {
            "owner": owner,
            "source_system": source_system,
            "availability_semantics": availability_semantics,
            "verification_status": verification_status,
        }

    return {
        "actual_served": entry("DINING_OPERATIONS", "SERVICE_EXPORT", "POST_SERVICE_RECONCILED"),
        "produced_portions": entry("DINING_OPERATIONS", "PRODUCTION_LOG", "POST_PRODUCTION_RECORDED"),
        "surplus_or_waste": entry("DINING_OPERATIONS", "SURPLUS_LOG", "POST_SERVICE_MEASURED"),
        "shortage_or_early_sellout": entry("DINING_OPERATIONS", "SERVICE_STATUS", "POST_SERVICE_RECORDED"),
        "operator_status_quo_quantity": entry("DINING_OPERATIONS", "PRODUCTION_PLAN", "MUST_EXIST_BY_DECISION_CUTOFF"),
        "menu": entry("DINING_OPERATIONS", "OFFICIAL_MENU", "MUST_EXIST_BY_DECISION_CUTOFF"),
        "academic_calendar": entry("UNIVERSITY", "OFFICIAL_ACADEMIC_CALENDAR", "MUST_EXIST_BY_DECISION_CUTOFF"),
    }


def test_verified_measured_artifact_is_bound_and_benchmark_eligible() -> None:
    contract = load_contract()
    result = contract.validate_service_truth_artifact(
        [measured_row(0), measured_row(1), measured_row(2)],
        field_provenance=source_contract(),
    )

    assert result["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert result["eligible_for_benchmark"] is True
    assert result["dataset_validation"]["validation_status"] == "ACCEPTED_MEASURED"
    assert result["dataset_validation"]["snapshot_integrity_required"] is True
    assert result["source_contract_validation"]["source_contract_verified"] is True
    assert len(result["artifact_admission_fingerprint_sha256"]) == 64
    assert result["reason_codes"] == []


def test_unverified_source_contract_blocks_otherwise_valid_measured_rows() -> None:
    contract = load_contract()
    result = contract.validate_service_truth_artifact(
        [measured_row(0), measured_row(1), measured_row(2)],
        field_provenance=source_contract(verified=False),
    )

    assert result["dataset_validation"]["validation_status"] == "ACCEPTED_MEASURED"
    assert result["source_contract_validation"]["source_contract_complete"] is True
    assert result["source_contract_validation"]["source_contract_verified"] is False
    assert result["validation_status"] == "SOURCE_CONTRACT_UNVERIFIED"
    assert result["eligible_for_benchmark"] is False
    assert "SOURCE_CONTRACT_UNVERIFIED" in result["reason_codes"]


def test_incomplete_source_contract_stays_explicit_and_noneligible() -> None:
    contract = load_contract()
    provenance = source_contract()
    del provenance["actual_served"]
    result = contract.validate_service_truth_artifact(
        [measured_row(0), measured_row(1), measured_row(2)],
        field_provenance=provenance,
    )

    assert result["validation_status"] == "SOURCE_CONTRACT_INCOMPLETE"
    assert result["eligible_for_benchmark"] is False
    assert "actual_served" in result["source_contract_validation"]["missing_source_contract_fields"]
    assert "SOURCE_CONTRACT_INCOMPLETE" in result["reason_codes"]


def test_sandbox_rows_never_become_benchmark_truth_from_verified_metadata() -> None:
    contract = load_contract()
    rows = [
        measured_row(0, evidence_class="GENERATED_SANDBOX"),
        measured_row(1, evidence_class="GENERATED_SANDBOX"),
        measured_row(2, evidence_class="GENERATED_SANDBOX"),
    ]
    result = contract.validate_service_truth_artifact(
        rows,
        field_provenance=source_contract(),
        require_measured=False,
    )

    assert result["dataset_validation"]["validation_status"] == "SANDBOX_ONLY"
    assert result["source_contract_validation"]["source_contract_verified"] is True
    assert result["validation_status"] == "SANDBOX_ONLY"
    assert result["eligible_for_benchmark"] is False


def test_admission_fingerprint_is_order_stable_and_binds_source_metadata() -> None:
    contract = load_contract()
    rows = [measured_row(0), measured_row(1), measured_row(2)]
    provenance = source_contract()
    forward = contract.validate_service_truth_artifact(rows, field_provenance=provenance)
    reordered = contract.validate_service_truth_artifact(
        list(reversed(rows)),
        field_provenance=dict(reversed(list(provenance.items()))),
    )
    changed = source_contract()
    changed["actual_served"]["source_system"] = "DIFFERENT_VERIFIED_EXPORT"
    changed_result = contract.validate_service_truth_artifact(rows, field_provenance=changed)

    assert forward["artifact_admission_fingerprint_sha256"] == reordered["artifact_admission_fingerprint_sha256"]
    assert forward["artifact_admission_fingerprint_sha256"] != changed_result["artifact_admission_fingerprint_sha256"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth artifact admission tests")
