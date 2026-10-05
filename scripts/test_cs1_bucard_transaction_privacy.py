#!/usr/bin/env python3
"""Regression guard for BUCard transaction identifiers in aggregate exports."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.bucard_dining_truth import validate_bucard_dining_export  # noqa: E402


def reconciled_row(index: int) -> dict:
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
        "reconciliation_status": "RECONCILED_BY_SKS",
        "reconciliation_record_id": f"sks-reconciliation-{index}",
        "semantic_mapping_status": "SKS_VERIFIED",
        "semantic_mapping_version": "bucard-to-served-v1",
        "duplicate_reversal_rules_applied": True,
    }


def test_transaction_identifier_remains_privacy_rejected() -> None:
    rows = [reconciled_row(i) for i in range(3)]
    rows[0]["debug"] = {"transactionId": "transaction-linked-record"}

    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_as_actual_served"] is False
    assert result["privacy_safe"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_TRANSACTIONID" in result["reason_codes"]


if __name__ == "__main__":
    test_transaction_identifier_remains_privacy_rejected()
    print("ok: BUCard transaction identifiers remain privacy-rejected")
