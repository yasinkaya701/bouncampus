#!/usr/bin/env python3
"""Regression tests for content-verified service-truth decision snapshots."""

from __future__ import annotations

import hashlib
import importlib.util
import json
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


def canonical_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def snapshot_artifacts() -> dict[str, object]:
    artifacts: dict[str, object] = {
        "calendar-2026-fall-v1": {
            "term": "2026-fall",
            "instruction_days": ["2026-10-01", "2026-10-02", "2026-10-05"],
            "holidays": [],
        }
    }
    for day in range(1, 4):
        service_date = f"2026-10-{day:02d}"
        artifacts[f"menu-{service_date}-lunch"] = {
            "service_date": service_date,
            "meal_period": "lunch",
            "items": ["soup", "main", "side"],
        }
    return artifacts


def measured_row(index: int, artifacts: dict[str, object]) -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    menu_snapshot = f"menu-{service_date}-lunch"
    calendar_snapshot = "calendar-2026-fall-v1"
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
        "decision_inputs": [
            {
                "field": "menu",
                "snapshot_id": menu_snapshot,
                "snapshot_sha256": canonical_sha256(artifacts[menu_snapshot]),
                "available_at": f"2026-10-{day:02d}T07:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
            {
                "field": "academic_calendar",
                "snapshot_id": calendar_snapshot,
                "snapshot_sha256": canonical_sha256(artifacts[calendar_snapshot]),
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


def test_artifact_recomputes_digest_and_rejects_wrong_declared_hash() -> None:
    contract = load_contract()
    artifacts = snapshot_artifacts()
    rows = [measured_row(index, artifacts) for index in range(3)]
    rows[0]["decision_inputs"][0]["snapshot_sha256"] = "0" * 64

    result = contract.validate_service_truth_artifact(
        rows,
        field_provenance=source_contract(),
        snapshot_artifacts=artifacts,
    )

    assert result["validation_status"] == "SNAPSHOT_ARTIFACTS_REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_SNAPSHOT_DIGEST_MISMATCH" in result["reason_codes"]


def test_artifact_rejects_missing_snapshot_payload_even_with_well_formed_digest() -> None:
    contract = load_contract()
    artifacts = snapshot_artifacts()
    rows = [measured_row(index, artifacts) for index in range(3)]
    del artifacts["calendar-2026-fall-v1"]

    result = contract.validate_service_truth_artifact(
        rows,
        field_provenance=source_contract(),
        snapshot_artifacts=artifacts,
    )

    assert result["validation_status"] == "SNAPSHOT_ARTIFACTS_REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "DECISION_INPUT_SNAPSHOT_ARTIFACT_REQUIRED" in result["reason_codes"]


def test_artifact_accepts_only_when_digest_matches_canonical_snapshot_payload() -> None:
    contract = load_contract()
    artifacts = snapshot_artifacts()
    rows = [measured_row(index, artifacts) for index in range(3)]

    result = contract.validate_service_truth_artifact(
        rows,
        field_provenance=source_contract(),
        snapshot_artifacts=artifacts,
    )

    assert result["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert result["eligible_for_benchmark"] is True
    verification = result["snapshot_artifact_validation"]
    assert verification["validation_status"] == "VERIFIED"
    assert verification["verified_snapshot_count"] == 4
    assert len(verification["snapshot_artifacts_sha256"]) == 64


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth content-binding tests")
