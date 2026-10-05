#!/usr/bin/env python3
"""Regression tests for fail-closed SERVICE_TRUTH_V1 artifact file intake."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/cs1_service_truth_artifact_intake.py"


def snapshot_sha256(content: object) -> str:
    payload = json.dumps(
        content,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def measured_row(index: int, *, evidence_class: str = "OFFICIAL_OPERATIONAL_EXPORT") -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    menu_content = {
        "service_date": service_date,
        "meal_period": "lunch",
        "items": ["lentil_soup", "rice", "seasonal_main"],
    }
    calendar_content = {
        "term": "2026-fall",
        "instructional_day": True,
    }
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
        "evidence_class": evidence_class,
        "decision_inputs": [
            {
                "field": "menu",
                "snapshot_id": menu_snapshot,
                "snapshot_content": menu_content,
                "snapshot_sha256": snapshot_sha256(menu_content),
                "available_at": f"2026-10-{day:02d}T07:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
            {
                "field": "academic_calendar",
                "snapshot_id": calendar_snapshot,
                "snapshot_content": calendar_content,
                "snapshot_sha256": snapshot_sha256(calendar_content),
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

    def entry(source_system: str) -> dict:
        return {
            "owner": "VERIFIED_OWNER",
            "source_system": source_system,
            "availability_semantics": "TIMESTAMPED_AND_RECONCILED",
            "verification_status": verification_status,
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


def package(*, evidence_class: str = "OFFICIAL_OPERATIONAL_EXPORT", verified: bool = True) -> dict:
    return {
        "contract_version": "SERVICE_TRUTH_V1",
        "rows": [measured_row(i, evidence_class=evidence_class) for i in range(3)],
        "field_provenance": source_contract(verified=verified),
    }


def run_cli(payload: object) -> tuple[subprocess.CompletedProcess[str], str]:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    with tempfile.TemporaryDirectory() as directory:
        artifact = Path(directory) / "service-truth.json"
        artifact.write_text(raw, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(CLI), "--artifact", str(artifact)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    return completed, hashlib.sha256(raw.encode("utf-8")).hexdigest()


def test_valid_measured_package_is_accepted_with_file_and_admission_checksums() -> None:
    completed, file_sha = run_cli(package())

    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert result["intake_status"] == "ACCEPTED"
    assert result["eligible_for_benchmark"] is True
    assert result["intake_file_sha256"] == file_sha
    assert len(result["artifact_admission_fingerprint_sha256"]) == 64
    assert result["reason_codes"] == []


def test_sandbox_rows_are_structurally_readable_but_rejected_for_benchmark_intake() -> None:
    completed, file_sha = run_cli(package(evidence_class="GENERATED_SANDBOX"))

    assert completed.returncode == 2
    result = json.loads(completed.stdout)
    assert result["intake_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert result["intake_file_sha256"] == file_sha
    assert "MEASURED_EVIDENCE_REQUIRED" in result["reason_codes"]


def test_unverified_source_contract_is_rejected_without_promoting_data() -> None:
    completed, _ = run_cli(package(verified=False))

    assert completed.returncode == 2
    result = json.loads(completed.stdout)
    assert result["intake_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "SOURCE_CONTRACT_UNVERIFIED" in result["reason_codes"]


def test_wrong_contract_version_fails_before_service_truth_admission() -> None:
    payload = package()
    payload["contract_version"] = "SERVICE_TRUTH_V999"
    completed, file_sha = run_cli(payload)

    assert completed.returncode == 3
    result = json.loads(completed.stdout)
    assert result == {
        "intake_status": "INVALID_PACKAGE",
        "eligible_for_benchmark": False,
        "contract_version": "SERVICE_TRUTH_V999",
        "intake_file_sha256": file_sha,
        "reason_codes": ["UNSUPPORTED_CONTRACT_VERSION"],
    }


def test_missing_provenance_fails_closed_as_invalid_package() -> None:
    payload = package()
    del payload["field_provenance"]
    completed, file_sha = run_cli(payload)

    assert completed.returncode == 3
    result = json.loads(completed.stdout)
    assert result["intake_status"] == "INVALID_PACKAGE"
    assert result["eligible_for_benchmark"] is False
    assert result["intake_file_sha256"] == file_sha
    assert result["reason_codes"] == ["FIELD_PROVENANCE_REQUIRED"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth artifact intake tests")
