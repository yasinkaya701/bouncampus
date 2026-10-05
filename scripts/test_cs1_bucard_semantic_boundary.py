#!/usr/bin/env python3
"""Regression contract for BUCard aggregate privacy and benchmark boundaries."""

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


def test_aggregate_metrics_with_card_text_are_not_identity_fields() -> None:
    rows = [deepcopy(reconciled_row(index)) for index in range(3)]
    rows[0]["discarded_meal_count"] = 7
    rows[1]["aggregate_card_count"] = 91

    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "ACCEPTED_RECONCILED_OUTCOME"
    assert result["privacy_safe"] is True
    assert not any(
        code.startswith("PRIVACY_FIELD_NOT_ALLOWED_") for code in result["reason_codes"]
    )


def test_exact_identity_field_is_still_rejected_recursively() -> None:
    rows = [deepcopy(reconciled_row(index)) for index in range(3)]
    rows[0]["debug"] = {"cardUid": "person-linked-card-token"}

    result = validate_bucard_dining_export(rows)

    assert result["validation_status"] == "REJECTED"
    assert result["privacy_safe"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_CARDUID" in result["reason_codes"]


def test_reconciled_projection_never_promotes_itself_to_benchmark_truth() -> None:
    result = validate_bucard_dining_export([reconciled_row(index) for index in range(3)])

    assert result["eligible_as_actual_served"] is True
    assert result["benchmark_eligible"] is False
    assert "validate_service_truth_artifact" in result["claim_boundary"]
    assert "caller-supplied" in result["claim_boundary"]
    assert "does not prove authenticity" in result["claim_boundary"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} BUCard semantic-boundary tests")
