#!/usr/bin/env python3
"""Regression tests for immutable decision-input snapshots in service truth."""

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


def digest(snapshot_id: str) -> str:
    return hashlib.sha256(snapshot_id.encode("utf-8")).hexdigest()


def measured_row(index: int, *, include_hashes: bool = True) -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    menu_snapshot = f"menu-{service_date}-lunch"
    calendar_snapshot = "calendar-2026-fall-v1"
    menu_input = {
        "field": "menu",
        "snapshot_id": menu_snapshot,
        "available_at": f"2026-10-{day:02d}T07:00:00+03:00",
        "evidence_class": "OFFICIAL_SNAPSHOT",
    }
    calendar_input = {
        "field": "academic_calendar",
        "snapshot_id": calendar_snapshot,
        "available_at": "2026-09-01T00:00:00+03:00",
        "evidence_class": "OFFICIAL_SNAPSHOT",
    }
    if include_hashes:
        menu_input["snapshot_sha256"] = digest(menu_snapshot)
        calendar_input["snapshot_sha256"] = digest(calendar_snapshot)
    return {
        "service_id": f"north-lunch-{service_date}",
        "granularity": "CAMPUS_MEAL_SERVICE",
        "service_date": service_date,
        "campus_id": "north",
        "meal_period": "lunch",
        "decision_cutoff_at": f"2026-10-{day:02d}T08:00:00+03:00",
        "actual_served": 100 + index,
        "produced_portions": 110 + index,
        "actual_surplus_portions": 10,
        "shortage_or_early_sellout": False,
        "outcome_reconciled": True,
        "outcome_source_record_id": f"ops-record-{index}",
        "operator_status_quo_quantity": 108 + index,
        "reservation_workflow_active": False,
        "evidence_class": "OFFICIAL_OPERATIONAL_EXPORT",
        "decision_inputs": [menu_input, calendar_input],
        "decision_audit": {
            "method_version": "operator-status-quo-v1",
            "recommended_quantity": 108 + index,
            "operator_action": "ACCEPT_RECOMMENDATION",
            "input_snapshot_ids": [menu_snapshot, calendar_snapshot],
        },
    }


def source_contract() -> dict:
    def entry(source_system: str) -> dict:
        return {
            "owner": "VERIFIED_OWNER",
            "source_system": source_system,
            "availability_semantics": "TIMESTAMPED_AND_RECONCILED",
            "verification_status": "VERIFIED",
        }

    return {
        "actual_served": entry("SERVICE_EXPORT"),
        "produced_portions": entry("PRODUCTION_LOG"),
        "surplus_or_waste": entry("SURPLUS_LOG"),
        "shortage_or_early_sellout": entry("SERVICE_STATUS"),
        "operator_status_quo_quantity": entry("PRODUCTION_PLAN"),
        "menu": entry("OFFICIAL_MENU"),
        "academic_calendar": entry("OFFICIAL_ACADEMIC_CALENDAR"),
    }


def test_artifact_admission_rejects_decision_inputs_without_content_hashes() -> None:
    contract = load_contract()
    rows = [measured_row(index, include_hashes=False) for index in range(3)]
    result = contract.validate_service_truth_artifact(rows, field_provenance=source_contract())

    assert result["validation_status"] == "DATASET_REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_SNAPSHOT_SHA256_REQUIRED" in result["reason_codes"]


def test_artifact_admission_rejects_snapshot_id_reused_with_different_hash() -> None:
    contract = load_contract()
    rows = [measured_row(index) for index in range(3)]
    rows[1]["decision_inputs"][1]["snapshot_sha256"] = "f" * 64
    result = contract.validate_service_truth_artifact(rows, field_provenance=source_contract())

    assert result["validation_status"] == "DATASET_REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_SNAPSHOT_HASH_CONFLICT" in result["reason_codes"]


def test_artifact_admission_accepts_stable_hashed_snapshots() -> None:
    contract = load_contract()
    rows = [measured_row(index) for index in range(3)]
    result = contract.validate_service_truth_artifact(rows, field_provenance=source_contract())

    assert result["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert result["eligible_for_benchmark"] is True


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth snapshot-integrity tests")
