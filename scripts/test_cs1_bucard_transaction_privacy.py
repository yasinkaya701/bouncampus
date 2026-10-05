#!/usr/bin/env python3
"""Regression: BUCard transaction identifiers remain identity-bearing metadata."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.bucard_dining_truth import validate_bucard_dining_export  # noqa: E402
from test_cs1_bucard_dining_aggregate_truth import reconciled_row  # noqa: E402


def test_transaction_identifier_remains_rejected_recursively() -> None:
    rows = [deepcopy(reconciled_row(index)) for index in range(3)]
    rows[0]["debug"] = {"transactionId": "txn-person-linkable-001"}

    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["privacy_safe"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_TRANSACTIONID" in result["reason_codes"]


if __name__ == "__main__":
    test_transaction_identifier_remains_rejected_recursively()
    print("ok: BUCard transaction identifier remains privacy-rejected")
