#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def load_router():
    path = ROOT / "backend/app/routers/campus_ops.py"
    if not path.exists():
        raise AssertionError("campus-ops API router missing")
    return importlib.import_module("app.routers.campus_ops")


def test_food_endpoint_returns_advisory_contract() -> None:
    router = load_router()
    result = router.optimize_food({
        "demand_scenarios": [{"demand": 80, "weight": 0.5}, {"demand": 100, "weight": 0.5}],
        "max_capacity": 100,
        "waste_weight": 1,
        "shortage_weight": 2,
        "method_eligibility": "PILOT_ELIGIBLE",
    })
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_dispatch"] is False


def test_shuttle_endpoint_fails_closed_on_bad_payload() -> None:
    router = load_router()
    result = router.optimize_shuttle({})
    assert result["decision_readiness"] == "WITHHOLD"


def test_space_endpoint_exposes_advisory_zone_selection() -> None:
    router = load_router()
    result = router.optimize_spaces({
        "occupancy_scenarios": [{"demand": 40, "weight": 1.0}],
        "zones": [{"zone_id": "Z1", "capacity": 50, "activation_weight": 1.0}],
        "idle_capacity_weight": 1.0,
        "shortage_weight": 3.0,
        "min_point_service_ratio": 0.9,
    })
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_zone_ids"] == ["Z1"]
    assert result["energy_savings_claim_allowed"] is False


def test_class_endpoint_exposes_assignments() -> None:
    router = load_router()
    result = router.optimize_classes({
        "classes": [{"class_id": "C1", "planning_attendance": 10, "allowed_slots": ["T1"], "required_features": []}],
        "rooms": [{"room_id": "R1", "capacity": 20, "features": [], "building": "A"}],
    })
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["assignments"][0]["room_id"] == "R1"


def test_class_endpoint_enforces_conflict_keys() -> None:
    router = load_router()
    result = router.optimize_classes({
        "classes": [
            {
                "class_id": "C1",
                "planning_attendance": 10,
                "allowed_slots": ["T1"],
                "required_features": [],
                "conflict_keys": ["instructor:I1"],
            },
            {
                "class_id": "C2",
                "planning_attendance": 10,
                "allowed_slots": ["T1"],
                "required_features": [],
                "conflict_keys": ["instructor:I1"],
            },
        ],
        "rooms": [
            {"room_id": "R1", "capacity": 20, "features": [], "building": "A"},
            {"room_id": "R2", "capacity": 20, "features": [], "building": "A"},
        ],
    })
    assert result["decision_readiness"] == "WITHHOLD"
    assert "NO_CONFLICT_FREE_CLASS_SCHEDULE" in result["reason_codes"]


def test_capabilities_declares_truth_boundary() -> None:
    router = load_router()
    result = router.capabilities()
    assert "food" in result["modules"]
    assert "shuttle" in result["modules"]
    assert "space_activation" in result["modules"]
    assert "class_scheduling" in result["modules"]
    assert result["automatic_actuation"] is False


def test_fastapi_main_registers_campus_ops_router() -> None:
    source = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
    assert "campus_ops" in source, "campus_ops router is not imported by app.main"
    assert "app.include_router(campus_ops.router)" in source, "campus_ops router is not registered by app.main"


def main() -> int:
    tests = [
        test_food_endpoint_returns_advisory_contract,
        test_shuttle_endpoint_fails_closed_on_bad_payload,
        test_space_endpoint_exposes_advisory_zone_selection,
        test_class_endpoint_exposes_assignments,
        test_class_endpoint_enforces_conflict_keys,
        test_capabilities_declares_truth_boundary,
        test_fastapi_main_registers_campus_ops_router,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
