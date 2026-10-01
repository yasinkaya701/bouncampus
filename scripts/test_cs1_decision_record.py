#!/usr/bin/env python3
"""Regression tests for prospective CS1 decision audit records."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "backend/app/decision/decision_record.py"
    spec = importlib.util.spec_from_file_location("cs1_decision_record", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_kwargs():
    return {
        "decision_id": "dec-001",
        "service_id": "svc-2026-10-15-lunch-north",
        "created_at": "2026-10-15T08:00:00+03:00",
        "information_cutoff_at": "2026-10-15T07:30:00+03:00",
        "input_snapshot_ids": ["reservation-cutoff-v1", "calendar-v3"],
        "strategy_version": "reservation-corrected-v1",
        "stage": "SHADOW",
        "recommended_action": {"type": "PRODUCTION_QUANTITY", "value": 510},
        "raw_reservation_count": 500,
        "simple_baseline": 505,
        "model_estimate_if_any": 510,
        "planning_band": [495, 530],
    }


def test_shadow_record_starts_without_operator_or_outcome_claims():
    module = load_module()
    record = module.create_decision_record(**base_kwargs())
    assert record["decision_stage"] == "SHADOW"
    assert record["operator_action"] is None
    assert record["operator_override"] is None
    assert record["actual_served"] is None
    assert record["verification_state"] == "PENDING"
    assert record["automatic_kitchen_dispatch"] is False
    assert record["generalized_impact_claim_allowed"] is False
    assert record["record_scope"] == "PROSPECTIVE_DECISION_AUDIT_ONLY"


def test_information_cutoff_cannot_be_after_decision_creation():
    module = load_module()
    kwargs = base_kwargs()
    kwargs["information_cutoff_at"] = "2026-10-15T08:01:00+03:00"
    try:
        module.create_decision_record(**kwargs)
    except ValueError as exc:
        assert "information_cutoff_at" in str(exc)
    else:
        raise AssertionError("future information cutoff must be rejected")


def test_advisory_override_requires_reason_and_non_override_must_match_recommendation():
    module = load_module()
    kwargs = base_kwargs()
    kwargs["stage"] = "ADVISORY"
    record = module.create_decision_record(**kwargs)

    try:
        module.record_operator_action(
            record,
            {"type": "PRODUCTION_QUANTITY", "value": 525},
            operator_override=True,
        )
    except ValueError as exc:
        assert "override reason" in str(exc).lower()
    else:
        raise AssertionError("override without reason must be rejected")

    try:
        module.record_operator_action(
            record,
            {"type": "PRODUCTION_QUANTITY", "value": 525},
            operator_override=False,
        )
    except ValueError as exc:
        assert "must match" in str(exc).lower()
    else:
        raise AssertionError("non-override action must equal recommendation")

    updated = module.record_operator_action(
        record,
        {"type": "PRODUCTION_QUANTITY", "value": 525},
        operator_override=True,
        operator_override_reason="Kitchen lead retained safety buffer",
    )
    assert updated["operator_override"] is True
    assert updated["operator_override_reason"] == "Kitchen lead retained safety buffer"
    assert updated["operator_action"]["value"] == 525


def test_shadow_mode_rejects_operator_action():
    module = load_module()
    record = module.create_decision_record(**base_kwargs())
    try:
        module.record_operator_action(
            record,
            {"type": "PRODUCTION_QUANTITY", "value": 510},
            operator_override=False,
        )
    except ValueError as exc:
        assert "shadow" in str(exc).lower()
    else:
        raise AssertionError("shadow mode must not record operator action")


def test_outcome_is_separate_and_requires_accepted_record_for_verified_state():
    module = load_module()
    record = module.create_decision_record(**base_kwargs())
    provisional = module.attach_service_outcome(
        record,
        actual_served=503,
        actual_surplus=7,
        shortage_event=False,
        accepted_service_record=None,
    )
    assert provisional["verification_state"] == "RECONCILIATION_REQUIRED"
    assert provisional["outcome_evidence_class"] == "UNVERIFIED_SERVICE_OUTCOME"
    assert provisional["generalized_impact_claim_allowed"] is False

    verified = module.attach_service_outcome(
        record,
        actual_served=503,
        actual_surplus=7,
        shortage_event=False,
        accepted_service_record="control-record-2026-10-15-001",
    )
    assert verified["verification_state"] == "VERIFIED"
    assert verified["outcome_evidence_class"] == "MEASURED_SERVICE_OUTCOME"
    assert verified["actual_served"] == 503
    assert verified["actual_surplus"] == 7


def test_invalid_identifiers_timestamps_counts_and_planning_band_fail_closed():
    module = load_module()
    bad_cases = [
        ("decision_id", ""),
        ("service_id", " "),
        ("created_at", "2026-10-15T08:00:00"),
        ("raw_reservation_count", -1),
        ("planning_band", [530, 495]),
    ]
    for field, value in bad_cases:
        kwargs = base_kwargs()
        kwargs[field] = value
        try:
            module.create_decision_record(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{field}={value!r} must be rejected")


def main() -> int:
    tests = [
        test_shadow_record_starts_without_operator_or_outcome_claims,
        test_information_cutoff_cannot_be_after_decision_creation,
        test_advisory_override_requires_reason_and_non_override_must_match_recommendation,
        test_shadow_mode_rejects_operator_action,
        test_outcome_is_separate_and_requires_accepted_record_for_verified_state,
        test_invalid_identifiers_timestamps_counts_and_planning_band_fail_closed,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
