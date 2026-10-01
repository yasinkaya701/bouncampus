#!/usr/bin/env python3
"""Regression tests for evidence-aware CS1 shuttle capacity decisions."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/shuttle_policy.py"
    spec = importlib.util.spec_from_file_location("shuttle_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_context():
    return {
        "official_schedule": True,
        "historical_boardings": True,
        "course_schedule": True,
        "calendar": True,
    }


def test_capacity_gap_is_actionable_only_with_verified_capacity() -> None:
    policy = load_policy()
    decision = policy.build_shuttle_decision(
        55,
        scheduled_capacity=40,
        signal_availability=full_context(),
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
        route_id="south-north-loop",
    )

    assert decision["policy_version"] == policy.POLICY_VERSION
    assert decision["route_id"] == "south-north-loop"
    assert decision["decision_readiness"] == "PILOT_READY"
    assert decision["abstained"] is False
    assert decision["expected_boardings"] == 55
    assert decision["scheduled_capacity"] == 40
    assert decision["capacity_gap"] == 15
    assert decision["recommended_action"] == "REVIEW_CAPACITY_PLAN"
    assert decision["capacity_provenance"] == "OFFICIAL_PUBLIC"
    assert decision["telemetry_status"] == "NOT_CONNECTED"
    assert decision["live_eta_available"] is False
    assert decision["live_occupancy_available"] is False
    assert decision["operator_approval_required"] is True
    assert decision["automatic_shuttle_dispatch"] is False
    assert decision["band_semantics"] == "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
    assert decision["calibration_status"] == "NOT_CALIBRATED"


def test_unknown_or_unverified_capacity_fails_closed() -> None:
    policy = load_policy()

    missing = policy.build_shuttle_decision(
        55,
        scheduled_capacity=None,
        signal_availability=full_context(),
        capacity_provenance="UNAVAILABLE",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert missing["decision_readiness"] == "WITHHOLD"
    assert missing["abstained"] is True
    assert missing["recommended_action"] is None
    assert "NO_VERIFIED_SERVICE_CAPACITY" in missing["reason_codes"]

    modeled_capacity = policy.build_shuttle_decision(
        55,
        scheduled_capacity=40,
        signal_availability=full_context(),
        capacity_provenance="MODEL_ESTIMATE",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert modeled_capacity["decision_readiness"] == "WITHHOLD"
    assert "UNVERIFIED_CAPACITY_PROVENANCE" in modeled_capacity["reason_codes"]


def test_schedule_and_method_eligibility_are_hard_gates() -> None:
    policy = load_policy()

    no_schedule = full_context()
    no_schedule["official_schedule"] = False
    decision = policy.build_shuttle_decision(
        30,
        scheduled_capacity=40,
        signal_availability=no_schedule,
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["decision_readiness"] == "WITHHOLD"
    assert "MISSING_REQUIRED_OFFICIAL_SCHEDULE" in decision["reason_codes"]

    sandbox = policy.build_shuttle_decision(
        30,
        scheduled_capacity=40,
        signal_availability=full_context(),
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="SANDBOX_ONLY",
    )
    assert sandbox["decision_readiness"] == "WITHHOLD"
    assert "METHOD_SANDBOX_ONLY" in sandbox["reason_codes"]


def test_partial_context_requires_review_not_fake_confidence() -> None:
    policy = load_policy()
    decision = policy.build_shuttle_decision(
        30,
        scheduled_capacity=40,
        signal_availability={
            "official_schedule": True,
            "historical_boardings": False,
            "course_schedule": True,
            "calendar": False,
        },
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["signal_coverage_pct"] == 60
    assert decision["decision_readiness"] == "REVIEW_REQUIRED"
    assert decision["abstained"] is False
    assert "CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED" in decision["reason_codes"]


def test_invalid_demand_never_generates_an_operational_action() -> None:
    policy = load_policy()
    for value in (0, -1, float("nan"), float("inf"), "not-a-number"):
        decision = policy.build_shuttle_decision(
            value,
            scheduled_capacity=40,
            signal_availability=full_context(),
            capacity_provenance="OFFICIAL_PUBLIC",
            method_eligibility="PILOT_ELIGIBLE",
        )
        assert decision["decision_readiness"] == "WITHHOLD"
        assert decision["recommended_action"] is None
        assert "NO_POSITIVE_BOARDING_ESTIMATE" in decision["reason_codes"]


def test_unknown_method_eligibility_is_treated_as_sandbox() -> None:
    policy = load_policy()
    decision = policy.build_shuttle_decision(
        30,
        scheduled_capacity=40,
        signal_availability=full_context(),
        capacity_provenance="OFFICIAL_PUBLIC",
        method_eligibility="magic-model",
    )
    assert decision["method_eligibility"] == "SANDBOX_ONLY"
    assert decision["decision_readiness"] == "WITHHOLD"
    assert "UNKNOWN_METHOD_ELIGIBILITY_TREATED_AS_SANDBOX" in decision["reason_codes"]


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} CS1 shuttle policy tests")
