#!/usr/bin/env python3
"""Regression tests for evidence-aware classroom/study-space assignment."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/space_policy.py"
    spec = importlib.util.spec_from_file_location("space_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_context():
    return {
        "timetable": True,
        "room_inventory": True,
        "attendance": True,
        "accessibility_metadata": True,
    }


def rooms():
    return [
        {
            "room_id": "A-101",
            "capacity": 100,
            "available": True,
            "accessible": True,
            "features": ["projector", "whiteboard"],
        },
        {
            "room_id": "B-202",
            "capacity": 50,
            "available": True,
            "accessible": True,
            "features": ["projector"],
        },
        {
            "room_id": "C-303",
            "capacity": 40,
            "available": True,
            "accessible": False,
            "features": ["projector"],
        },
    ]


def test_selects_smallest_feasible_room_to_reduce_idle_capacity() -> None:
    policy = load_policy()
    decision = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
        session_id="CMPE150-2026-10-01-1",
        required_features=["projector"],
    )

    assert decision["policy_version"] == policy.POLICY_VERSION
    assert decision["session_id"] == "CMPE150-2026-10-01-1"
    assert decision["decision_readiness"] == "PILOT_READY"
    assert decision["abstained"] is False
    assert decision["recommended_room_id"] == "C-303"
    assert decision["recommended_room_capacity"] == 40
    assert decision["seat_slack"] == 2
    assert decision["expected_attendance"] == 38
    assert decision["operator_approval_required"] is True
    assert decision["automatic_room_booking"] is False
    assert decision["live_occupancy_available"] is False
    assert decision["assignment_method"] == "MINIMUM_FEASIBLE_CAPACITY"


def test_accessibility_and_required_features_are_hard_constraints() -> None:
    policy = load_policy()
    accessible = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
        accessible_required=True,
        required_features=["projector"],
    )
    assert accessible["recommended_room_id"] == "B-202"
    assert accessible["seat_slack"] == 12

    whiteboard = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
        required_features=["whiteboard"],
    )
    assert whiteboard["recommended_room_id"] == "A-101"


def test_missing_required_context_or_unverified_inventory_fails_closed() -> None:
    policy = load_policy()
    no_timetable = full_context()
    no_timetable["timetable"] = False
    decision = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=no_timetable,
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["decision_readiness"] == "WITHHOLD"
    assert decision["recommended_room_id"] is None
    assert "MISSING_REQUIRED_TIMETABLE" in decision["reason_codes"]

    unverified = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="MODEL_ESTIMATE",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert unverified["decision_readiness"] == "WITHHOLD"
    assert "UNVERIFIED_ROOM_INVENTORY_PROVENANCE" in unverified["reason_codes"]


def test_no_feasible_room_withholds_instead_of_violating_constraints() -> None:
    policy = load_policy()
    decision = policy.build_space_decision(
        120,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["decision_readiness"] == "WITHHOLD"
    assert decision["abstained"] is True
    assert decision["recommended_room_id"] is None
    assert decision["feasible_room_count"] == 0
    assert "NO_FEASIBLE_SPACE" in decision["reason_codes"]


def test_invalid_inventory_is_rejected_as_a_whole() -> None:
    policy = load_policy()
    invalid = rooms() + [
        {
            "room_id": "B-202",
            "capacity": 75,
            "available": True,
            "accessible": True,
            "features": [],
        }
    ]
    decision = policy.build_space_decision(
        38,
        invalid,
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
    )
    assert decision["decision_readiness"] == "WITHHOLD"
    assert decision["recommended_room_id"] is None
    assert "INVALID_ROOM_INVENTORY" in decision["reason_codes"]


def test_method_eligibility_controls_operational_readiness() -> None:
    policy = load_policy()
    sandbox = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="SANDBOX_ONLY",
    )
    assert sandbox["decision_readiness"] == "WITHHOLD"
    assert sandbox["recommended_room_id"] is None
    assert "METHOD_SANDBOX_ONLY" in sandbox["reason_codes"]

    offline = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=full_context(),
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="EVALUATED_OFFLINE",
    )
    assert offline["decision_readiness"] == "REVIEW_REQUIRED"
    assert offline["abstained"] is False
    assert offline["recommended_room_id"] == "C-303"
    assert "METHOD_NOT_YET_PILOT_ELIGIBLE" in offline["reason_codes"]


def test_accessibility_requirement_needs_accessibility_metadata() -> None:
    policy = load_policy()
    context = full_context()
    context["accessibility_metadata"] = False
    decision = policy.build_space_decision(
        38,
        rooms(),
        signal_availability=context,
        inventory_provenance="OFFICIAL_PUBLIC",
        method_eligibility="PILOT_ELIGIBLE",
        accessible_required=True,
    )
    assert decision["decision_readiness"] == "WITHHOLD"
    assert decision["recommended_room_id"] is None
    assert "MISSING_REQUIRED_ACCESSIBILITY_METADATA" in decision["reason_codes"]


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} CS1 space policy tests")
