#!/usr/bin/env python3
"""Focused regression tests for classroom allocation under hard constraints."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rooms():
    return [
        {
            "room_id": "M101",
            "building_id": "B-SOUTH-M",
            "campus": "south",
            "capacity": 80,
            "accessible": True,
            "equipment": ["projector", "computer"],
            "energy_cost_score": 0.6,
        },
        {
            "room_id": "TB201",
            "building_id": "B-SOUTH-TB",
            "campus": "south",
            "capacity": 55,
            "accessible": False,
            "equipment": ["projector"],
            "energy_cost_score": 0.2,
        },
        {
            "room_id": "KB301",
            "building_id": "B-NORTH-KB",
            "campus": "north",
            "capacity": 120,
            "accessible": True,
            "equipment": ["projector", "computer"],
            "energy_cost_score": 0.8,
        },
    ]


def sessions():
    return [
        {
            "session_id": "CMPE150-1",
            "campus": "south",
            "start_minute": 540,
            "end_minute": 600,
            "expected_attendance": 70,
            "accessibility_required": True,
            "equipment_required": ["projector", "computer"],
        },
        {
            "session_id": "EC101-1",
            "campus": "south",
            "start_minute": 540,
            "end_minute": 600,
            "expected_attendance": 45,
            "accessibility_required": False,
            "equipment_required": ["projector"],
        },
    ]


def test_assigns_only_hard_constraint_feasible_rooms() -> None:
    policy = load_module("classroom_policy", "backend/app/decision/classroom_policy.py")
    result = policy.allocate_classrooms(
        sessions=sessions(),
        rooms=rooms(),
        upstream_readiness="REVIEW_REQUIRED",
    )
    assignments = {item["session_id"]: item for item in result["assignments"]}
    assert assignments["CMPE150-1"]["room_id"] == "M101"
    assert assignments["EC101-1"]["room_id"] == "TB201"
    assert result["unassigned"] == []
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True
    assert result["building_loads"]["B-SOUTH-M"]["assigned_attendance"] == 70
    assert result["building_loads"]["B-SOUTH-TB"]["assigned_attendance"] == 45


def test_accessibility_equipment_capacity_and_campus_are_hard_constraints() -> None:
    policy = load_module("classroom_policy_constraints", "backend/app/decision/classroom_policy.py")
    blocked = [
        {
            "session_id": "SPECIAL",
            "campus": "south",
            "start_minute": 600,
            "end_minute": 660,
            "expected_attendance": 90,
            "accessibility_required": True,
            "equipment_required": ["lab-bench"],
        }
    ]
    result = policy.allocate_classrooms(
        sessions=blocked,
        rooms=rooms(),
        upstream_readiness="REVIEW_REQUIRED",
    )
    assert result["assignments"] == []
    assert result["unassigned"][0]["session_id"] == "SPECIAL"
    assert "NO_FEASIBLE_ROOM_SPECIAL" in result["reason_codes"]
    assert result["decision_readiness"] == "REVIEW_REQUIRED"


def test_room_time_conflicts_are_never_double_booked() -> None:
    policy = load_module("classroom_policy_conflict", "backend/app/decision/classroom_policy.py")
    single_room = [rooms()[0]]
    overlapping = [
        {
            "session_id": "A",
            "campus": "south",
            "start_minute": 540,
            "end_minute": 600,
            "expected_attendance": 60,
            "equipment_required": ["projector"],
        },
        {
            "session_id": "B",
            "campus": "south",
            "start_minute": 570,
            "end_minute": 630,
            "expected_attendance": 50,
            "equipment_required": ["projector"],
        },
    ]
    result = policy.allocate_classrooms(
        sessions=overlapping,
        rooms=single_room,
        upstream_readiness="REVIEW_REQUIRED",
    )
    assert len(result["assignments"]) == 1
    assert len(result["unassigned"]) == 1
    assert len({item["room_id"] for item in result["assignments"]}) == 1


def test_withholds_on_upstream_withhold_and_rejects_malformed_sessions() -> None:
    policy = load_module("classroom_policy_invalid", "backend/app/decision/classroom_policy.py")
    withheld = policy.allocate_classrooms(
        sessions=sessions(),
        rooms=rooms(),
        upstream_readiness="WITHHOLD",
    )
    assert withheld["decision_readiness"] == "WITHHOLD"
    assert withheld["assignments"] == []
    assert withheld["abstained"] is True

    bad = sessions()[0].copy()
    bad["end_minute"] = bad["start_minute"]
    try:
        policy.allocate_classrooms(
            sessions=[bad],
            rooms=rooms(),
            upstream_readiness="REVIEW_REQUIRED",
        )
    except ValueError as exc:
        assert "time" in str(exc).lower()
    else:
        raise AssertionError("zero-duration session must be rejected")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} classroom-policy tests")
