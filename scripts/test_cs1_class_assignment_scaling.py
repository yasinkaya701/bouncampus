#!/usr/bin/env python3
"""Regression gates for polynomial CS1 room/slot assignment."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_solver():
    path = ROOT / "backend/app/decision/class_assignment.py"
    spec = importlib.util.spec_from_file_location("cs1_class_assignment", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rooms(count: int = 10) -> list[dict]:
    return [
        {
            "room_id": f"R{index:02d}",
            "capacity": 20 + index,
            "features": [],
            "building": "A",
        }
        for index in range(count)
    ]


def classes(count: int) -> list[dict]:
    return [
        {
            "class_id": f"C{index:02d}",
            "planning_attendance": 10,
            "allowed_slots": [f"T{slot}" for slot in range(5)],
            "required_features": [],
        }
        for index in range(count)
    ]


def test_basic_assignment_preserves_constraints() -> None:
    solver = load_solver()
    result = solver.optimize_class_schedule(
        classes=[
            {
                "class_id": "C1",
                "planning_attendance": 80,
                "allowed_slots": ["T1"],
                "required_features": ["projector"],
            },
            {
                "class_id": "C2",
                "planning_attendance": 30,
                "allowed_slots": ["T1", "T2"],
                "required_features": ["lab"],
            },
        ],
        rooms=[
            {"room_id": "R1", "capacity": 100, "features": ["projector"], "building": "A"},
            {"room_id": "R2", "capacity": 40, "features": ["projector", "lab"], "building": "B"},
        ],
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert len(result["assignments"]) == 2
    assert len({(row["slot"], row["room_id"]) for row in result["assignments"]}) == 2
    assert result["solver_semantics"] == "MIN_COST_BIPARTITE_ROOM_SLOT_ASSIGNMENT"


def test_fifty_classes_fill_fifty_room_slot_resources() -> None:
    solver = load_solver()
    result = solver.optimize_class_schedule(classes=classes(50), rooms=rooms(10))
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert len(result["assignments"]) == 50
    assert len({(row["slot"], row["room_id"]) for row in result["assignments"]}) == 50


def test_more_classes_than_room_slot_resources_fail_closed() -> None:
    solver = load_solver()
    result = solver.optimize_class_schedule(classes=classes(51), rooms=rooms(10))
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["assignments"] == []
    assert "NO_COLLISION_FREE_CLASS_SCHEDULE" in result["reason_codes"]


def test_conflict_layer_routes_to_polynomial_base_solver() -> None:
    source = (ROOT / "backend/app/decision/class_conflicts.py").read_text(encoding="utf-8")
    assert "from app.decision.class_assignment import _base, optimize_class_schedule" in source
    assert "from app.decision.campus_ops import _base, optimize_class_schedule" not in source


def main() -> int:
    tests = [
        test_basic_assignment_preserves_constraints,
        test_fifty_classes_fill_fifty_room_slot_resources,
        test_more_classes_than_room_slot_resources_fail_closed,
        test_conflict_layer_routes_to_polynomial_base_solver,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
