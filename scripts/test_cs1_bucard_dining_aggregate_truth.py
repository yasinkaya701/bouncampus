#!/usr/bin/env python3
"""Regression contract for privacy-preserving BUCard dining aggregate admission."""

from __future__ import annotations

from copy import deepcopy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.bucard_dining_truth import (  # noqa: E402
    project_reconciled_actual_served_observations,
    validate_bucard_dining_export,
)


def aggregate_row(index: int) -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    return {
        "service_id": f"north-lunch-{service_date}",
        "granularity": "CAMPUS_MEAL_SERVICE",
        "service_date": service_date,
        "campus_id": "north",
        "meal_period": "lunch",
        "count_value": 120 + index,
        "count_semantics": "MEAL_TRANSACTION_COUNT",
        "package_meal_count": 10 + index,
        "report_generated_at": f"2026-10-{day:02d}T15:30:00+03:00",
        "source_report_id": f"bucard-report-{service_date}-north-lunch",
        "evidence_class": "OFFICIAL_OPERATIONAL_EXPORT",
        "reconciliation_status": "UNRECONCILED",
        "semantic_mapping_status": "UNVERIFIED",
        "duplicate_reversal_rules_applied": False,
    }


def reconciled_row(index: int) -> dict:
    row = aggregate_row(index)
    row.update(
        {
            "reconciliation_status": "RECONCILED_BY_SKS",
            "reconciliation_record_id": f"sks-reconciliation-{index}",
            "semantic_mapping_status": "SKS_VERIFIED",
            "semantic_mapping_version": "bucard-to-served-v1",
            "duplicate_reversal_rules_applied": True,
        }
    )
    return row


def test_valid_aggregate_export_is_withheld_until_semantics_are_reconciled() -> None:
    result = validate_bucard_dining_export([aggregate_row(i) for i in range(3)])

    assert result["validation_status"] == "WITHHOLD_UNRECONCILED"
    assert result["eligible_as_actual_served"] is False
    assert result["decision_input_eligible"] is False
    assert result["privacy_safe"] is True
    assert "RECONCILIATION_REQUIRED_FOR_ACTUAL_SERVED" in result["reason_codes"]
    assert "SEMANTIC_MAPPING_REQUIRED_FOR_ACTUAL_SERVED" in result["reason_codes"]


def test_sks_reconciled_export_can_become_actual_served_outcome_candidate() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "ACCEPTED_RECONCILED_OUTCOME"
    assert result["eligible_as_actual_served"] is True
    assert result["decision_input_eligible"] is False
    assert result["reason_codes"] == []
    assert len(result["artifact_checksum_sha256"]) == 64

    projected = project_reconciled_actual_served_observations(rows)
    assert projected[0] == {
        "service_id": "north-lunch-2026-10-01",
        "service_date": "2026-10-01",
        "campus_id": "north",
        "meal_period": "lunch",
        "actual_served": 120,
        "outcome_reconciled": True,
        "outcome_source_record_id": "sks-reconciliation-0",
        "evidence_class": "OFFICIAL_OPERATIONAL_EXPORT",
    }


def test_projection_fails_closed_for_unreconciled_aggregate_counts() -> None:
    try:
        project_reconciled_actual_served_observations([aggregate_row(i) for i in range(3)])
    except ValueError as exc:
        assert "not eligible as actual_served" in str(exc)
    else:
        raise AssertionError("unreconciled BUCard counts must not project to actual_served")


def test_identity_bearing_fields_are_rejected_recursively() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    rows[0]["debug"] = {"cardUid": "person-linked-card-token"}
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_as_actual_served"] is False
    assert result["privacy_safe"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_CARDUID" in result["reason_codes"]


def test_non_identity_field_names_containing_card_substring_are_allowed() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    rows[0]["discarded_meal_count"] = 7
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "ACCEPTED_RECONCILED_OUTCOME"
    assert result["privacy_safe"] is True
    assert not any(
        code.startswith("PRIVACY_FIELD_NOT_ALLOWED_") for code in result["reason_codes"]
    )


def test_reconciled_projection_is_not_benchmark_admission() -> None:
    result = validate_bucard_dining_export([reconciled_row(i) for i in range(3)])

    assert result["eligible_as_actual_served"] is True
    assert result["benchmark_eligible"] is False
    assert "validate_service_truth_artifact" in result["claim_boundary"]
    assert "caller-supplied" in result["claim_boundary"]
    assert "does not prove authenticity" in result["claim_boundary"]


def test_counts_must_be_nonnegative_integers_and_timestamp_timezone_aware() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    rows[0]["count_value"] = 12.5
    rows[1]["package_meal_count"] = -1
    rows[2]["report_generated_at"] = "2026-10-03T15:30:00"
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert "COUNT_VALUE_MUST_BE_NONNEGATIVE_INTEGER" in result["reason_codes"]
    assert "PACKAGE_MEAL_COUNT_MUST_BE_NONNEGATIVE_INTEGER" in result["reason_codes"]
    assert "REPORT_GENERATED_AT_MUST_BE_TIMEZONE_AWARE" in result["reason_codes"]


def test_reconciliation_requires_record_mapping_version_and_correction_rules() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    del rows[0]["reconciliation_record_id"]
    del rows[1]["semantic_mapping_version"]
    rows[2]["duplicate_reversal_rules_applied"] = False
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "WITHHOLD_UNRECONCILED"
    assert result["eligible_as_actual_served"] is False
    assert "RECONCILIATION_RECORD_ID_REQUIRED" in result["reason_codes"]
    assert "SEMANTIC_MAPPING_VERSION_REQUIRED" in result["reason_codes"]
    assert "DUPLICATE_REVERSAL_RULES_REQUIRED" in result["reason_codes"]


def test_duplicate_service_ids_and_unknown_count_semantics_fail_closed() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    rows[1]["service_id"] = rows[0]["service_id"]
    rows[2]["count_semantics"] = "MAGIC_DEMAND_COUNT"
    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert "DUPLICATE_SERVICE_ID" in result["reason_codes"]
    assert "UNKNOWN_COUNT_SEMANTICS" in result["reason_codes"]


def test_artifact_checksum_is_order_stable_but_content_bound() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    forward = validate_bucard_dining_export(rows)
    reversed_result = validate_bucard_dining_export(list(reversed(rows)))
    changed = deepcopy(rows)
    changed[0]["count_value"] += 1
    changed_result = validate_bucard_dining_export(changed)

    assert forward["artifact_checksum_sha256"] == reversed_result["artifact_checksum_sha256"]
    assert forward["artifact_checksum_sha256"] != changed_result["artifact_checksum_sha256"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} BUCard dining aggregate-truth tests")
