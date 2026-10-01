#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

import app.decision.class_conflicts as class_conflicts
from app.decision.class_conflicts import optimize_conflict_aware_class_schedule


def _rooms() -> list[dict[str, object]]:
    return [
        {"room_id": "R1", "capacity": 50, "features": ["projector"], "building": "A"},
        {"room_id": "R2", "capacity": 50, "features": ["projector"], "building": "A"},
    ]


def test_shared_conflict_key_cannot_use_same_slot() -> None:
    result = optimize_conflict_aware_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
                "conflict_keys": ["instructor:I1"],
            },
            {
                "class_id": "C2",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
                "conflict_keys": ["instructor:I1"],
            },
        ],
        rooms=_rooms(),
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["assignments"] == []
    assert "NO_CONFLICT_FREE_CLASS_SCHEDULE" in result["reason_codes"]


def test_shared_conflict_key_moves_class_to_alternate_slot() -> None:
    result = optimize_conflict_aware_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
                "conflict_keys": ["instructor:I1", "cohort:CMPE-1"],
            },
            {
                "class_id": "C2",
                "planning_attendance": 20,
                "allowed_slots": ["T1", "T2"],
                "required_features": ["projector"],
                "conflict_keys": ["instructor:I1"],
            },
        ],
        rooms=_rooms(),
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assignments = {row["class_id"]: row for row in result["assignments"]}
    assert assignments["C1"]["slot"] == "T1"
    assert assignments["C2"]["slot"] == "T2"
    assert result["conflict_constraints_enforced"] is True
    assert result["conflict_key_count"] == 2
    assert result["conflict_search_complete"] is True


def test_invalid_conflict_keys_fail_closed() -> None:
    result = optimize_conflict_aware_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": [],
                "conflict_keys": "instructor:I1",
            }
        ],
        rooms=_rooms(),
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["assignments"] == []
    assert "INVALID_CLASS_CONFLICT_KEYS" in result["reason_codes"]


def test_no_conflict_keys_preserves_existing_scheduler_behavior() -> None:
    result = optimize_conflict_aware_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 20,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
            }
        ],
        rooms=_rooms(),
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["class_id"] == "C1"
    assert result["conflict_constraints_enforced"] is False
    assert result["conflict_search_complete"] is True


def test_search_limit_is_explicit_when_feasible_plan_exists() -> None:
    original_limit = class_conflicts.MAX_CONFLICT_SLOT_PLANS
    class_conflicts.MAX_CONFLICT_SLOT_PLANS = 1
    try:
        result = class_conflicts.optimize_conflict_aware_class_schedule(
            classes=[
                {
                    "class_id": "C1",
                    "planning_attendance": 20,
                    "allowed_slots": ["T1", "T2"],
                    "required_features": ["projector"],
                    "conflict_keys": ["cohort:CMPE-1"],
                }
            ],
            rooms=_rooms(),
        )
    finally:
        class_conflicts.MAX_CONFLICT_SLOT_PLANS = original_limit

    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"]
    assert result["conflict_slot_plans_evaluated"] == 1
    assert result["conflict_search_complete"] is False
    assert "CLASS_CONFLICT_SEARCH_LIMIT_EXCEEDED" in result["reason_codes"]


def main() -> int:
    tests = [
        test_shared_conflict_key_cannot_use_same_slot,
        test_shared_conflict_key_moves_class_to_alternate_slot,
        test_invalid_conflict_keys_fail_closed,
        test_no_conflict_keys_preserves_existing_scheduler_behavior,
        test_search_limit_is_explicit_when_feasible_plan_exists,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
