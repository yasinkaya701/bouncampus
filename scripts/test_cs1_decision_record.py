#!/usr/bin/env python3
"""Regression tests for the CS1 prospective decision-record contract."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/decision_record.py"
    if not path.exists():
        raise AssertionError("decision-record contract missing")
    spec = importlib.util.spec_from_file_location("cs1_decision_record", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_record(**overrides):
    record = {
        "decision_id": "decision-2026-10-01-south-lunch-001",
        "service_id": "service-2026-10-01-south-lunch",
        "mode": "ADVISORY",
        "created_at": "2026-10-01T09:05:00+03:00",
        "information_cutoff_at": "2026-10-01T09:00:00+03:00",
        "decision_freeze_at": "2026-10-01T09:30:00+03:00",
        "input_snapshot_ids": ["snapshot-reservation-001", "snapshot-calendar-001"],
        "strategy_version": "reservation-correction-v1",
        "raw_reservation_count": 480,
        "simple_baseline": 505,
        "model_estimate_if_any": None,
        "planning_band": {"lower": 495, "upper": 520},
        "recommended_action": {"kind": "OPERATOR_DEFINED", "value": 505},
        "operator_action": {"kind": "OPERATOR_DEFINED", "value": 500},
        "operator_override": True,
        "operator_override_reason": "Kitchen retained a larger safety buffer.",
        "actual_served": None,
        "actual_surplus": None,
        "shortage_event": None,
        "accepted_service_record": None,
        "verification_state": "PENDING",
    }
    record.update(overrides)
    return record


def test_valid_advisory_record_is_audit_ready_but_not_pilot_evidence() -> None:
    contract = load_contract()
    result = contract.validate_decision_record(valid_record())
    assert result["record_status"] == "AUDIT_READY"
    assert result["reason_codes"] == []
    assert result["claim_scope"] == "PROSPECTIVE_AUDIT_CONTRACT_ONLY"
    assert result["impact_claim_allowed"] is False
    assert result["autonomous_dispatch_allowed"] is False


def test_record_fails_closed_when_decision_misses_freeze_or_uses_future_information() -> None:
    contract = load_contract()
    late = contract.validate_decision_record(
        valid_record(created_at="2026-10-01T09:31:00+03:00")
    )
    assert late["record_status"] == "RECONCILIATION_REQUIRED"
    assert "DECISION_CREATED_AFTER_FREEZE" in late["reason_codes"]

    leakage = contract.validate_decision_record(
        valid_record(information_cutoff_at="2026-10-01T09:10:00+03:00")
    )
    assert leakage["record_status"] == "RECONCILIATION_REQUIRED"
    assert "INFORMATION_CUTOFF_AFTER_DECISION_CREATED" in leakage["reason_codes"]


def test_record_fails_closed_when_created_exactly_at_freeze() -> None:
    contract = load_contract()
    at_freeze = contract.validate_decision_record(
        valid_record(created_at="2026-10-01T09:30:00+03:00")
    )
    assert at_freeze["record_status"] == "RECONCILIATION_REQUIRED"
    assert "DECISION_CREATED_AT_FREEZE" in at_freeze["reason_codes"]


def test_override_requires_reason_and_actionable_modes_require_operator_action() -> None:
    contract = load_contract()
    missing_reason = contract.validate_decision_record(
        valid_record(operator_override_reason=None)
    )
    assert missing_reason["record_status"] == "RECONCILIATION_REQUIRED"
    assert "OVERRIDE_REASON_REQUIRED" in missing_reason["reason_codes"]

    missing_action = contract.validate_decision_record(valid_record(operator_action=None))
    assert missing_action["record_status"] == "RECONCILIATION_REQUIRED"
    assert "OPERATOR_ACTION_REQUIRED" in missing_action["reason_codes"]


def test_operator_override_must_be_explicit_boolean() -> None:
    contract = load_contract()
    ambiguous = contract.validate_decision_record(
        valid_record(operator_override="false", operator_override_reason=None)
    )
    assert ambiguous["record_status"] == "RECONCILIATION_REQUIRED"
    assert "OPERATOR_OVERRIDE_MUST_BE_BOOLEAN" in ambiguous["reason_codes"]


def test_verified_outcome_requires_reconciled_service_truth() -> None:
    contract = load_contract()
    incomplete = contract.validate_decision_record(
        valid_record(verification_state="VERIFIED")
    )
    assert incomplete["record_status"] == "RECONCILIATION_REQUIRED"
    assert "VERIFIED_OUTCOME_REQUIRES_ACTUAL_SERVED" in incomplete["reason_codes"]
    assert "VERIFIED_OUTCOME_REQUIRES_ACTUAL_SURPLUS" in incomplete["reason_codes"]
    assert "VERIFIED_OUTCOME_REQUIRES_SHORTAGE_EVENT" in incomplete["reason_codes"]
    assert "VERIFIED_OUTCOME_REQUIRES_ACCEPTED_SERVICE_RECORD" in incomplete["reason_codes"]

    verified = contract.validate_decision_record(
        valid_record(
            verification_state="VERIFIED",
            actual_served=497,
            actual_surplus=3,
            shortage_event=False,
            accepted_service_record="control-org-record-2026-10-01-001",
        )
    )
    assert verified["record_status"] == "AUDIT_READY"
    assert verified["verification_state"] == "VERIFIED"
    assert verified["impact_claim_allowed"] is False


def test_shadow_mode_does_not_fake_operator_action() -> None:
    contract = load_contract()
    shadow = contract.validate_decision_record(
        valid_record(
            mode="SHADOW",
            operator_action=None,
            operator_override=False,
            operator_override_reason=None,
        )
    )
    assert shadow["record_status"] == "AUDIT_READY"
    assert shadow["operator_action_required"] is False
    assert shadow["claim_scope"] == "PROSPECTIVE_AUDIT_CONTRACT_ONLY"


if __name__ == "__main__":
    tests = [
        test_valid_advisory_record_is_audit_ready_but_not_pilot_evidence,
        test_record_fails_closed_when_decision_misses_freeze_or_uses_future_information,
        test_record_fails_closed_when_created_exactly_at_freeze,
        test_override_requires_reason_and_actionable_modes_require_operator_action,
        test_operator_override_must_be_explicit_boolean,
        test_verified_outcome_requires_reconciled_service_truth,
        test_shadow_mode_does_not_fake_operator_action,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} CS1 decision-record tests")
