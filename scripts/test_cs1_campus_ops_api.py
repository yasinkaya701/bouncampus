#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys
from pathlib import Path

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def load_router():
    path = ROOT / "backend/app/routers/campus_ops.py"
    if not path.exists():
        raise AssertionError("campus-ops API router missing")
    return importlib.import_module("app.routers.campus_ops")


def sources():
    return {
        "schedule": {"available": True, "provenance": "PUBLIC_SOURCE", "published_at": "2026-10-01T08:00:00+03:00"},
        "occupancy_model": {"available": True, "provenance": "MODEL_ESTIMATE", "published_at": "2026-10-01T09:00:00+03:00"},
    }


def zones():
    return [{"zone_id": "south-academic", "campus": "south", "capacity": 1000, "occupancy_estimate": 620, "scheduled_load": 580, "event_load": 40}]


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
            {"class_id": "C1", "planning_attendance": 10, "allowed_slots": ["T1"], "required_features": [], "conflict_keys": ["instructor:I1"]},
            {"class_id": "C2", "planning_attendance": 10, "allowed_slots": ["T1"], "required_features": [], "conflict_keys": ["instructor:I1"]},
        ],
        "rooms": [
            {"room_id": "R1", "capacity": 20, "features": [], "building": "A"},
            {"room_id": "R2", "capacity": 20, "features": [], "building": "A"},
        ],
    })
    assert result["decision_readiness"] == "WITHHOLD"
    assert "NO_CONFLICT_FREE_CLASS_SCHEDULE" in result["reason_codes"]


def test_decision_time_state_endpoint_rejects_future_information() -> None:
    router = load_router()
    payload = {"decision_time": "2026-10-01T10:00:00+03:00", "zones": zones(), "sources": sources()}
    payload["sources"]["occupancy_model"]["published_at"] = "2026-10-01T11:00:00+03:00"
    result = router.state(payload)
    assert result["decision_readiness"] == "WITHHOLD"
    assert "SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_OCCUPANCY_MODEL" in result["reason_codes"]


def integrated_payload():
    return {
        "decision_time": "2026-10-01T10:00:00+03:00",
        "zones": zones(),
        "sources": sources(),
        "modules": {
            "food": {
                "demand_scenarios": [{"demand": 90, "weight": 0.5}, {"demand": 100, "weight": 0.5}],
                "max_capacity": 120,
                "waste_weight": 1.0,
                "shortage_weight": 2.0,
                "method_eligibility": "PILOT_ELIGIBLE",
            },
            "resources": {
                "total_capacity": 10,
                "requests": [
                    {"request_id": "study", "minimum": 2, "desired": 7, "priority_weight": 3},
                    {"request_id": "charging", "minimum": 1, "desired": 5, "priority_weight": 1},
                ],
            },
        },
    }


def test_integrated_plan_runs_registered_modules_behind_one_state_gate() -> None:
    router = load_router()
    result = router.plan(integrated_payload())
    assert result["state"]["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["modules"]["food"]["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["modules"]["resources"]["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["bundle"]["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True


def test_integrated_plan_does_not_run_modules_when_state_withholds() -> None:
    router = load_router()
    payload = integrated_payload()
    payload["sources"]["occupancy_model"]["available"] = False
    result = router.plan(payload)
    assert result["state"]["decision_readiness"] == "WITHHOLD"
    assert result["modules"] == {}
    assert result["bundle"]["decision_readiness"] == "WITHHOLD"


def test_integrated_plan_rejects_unknown_module() -> None:
    router = load_router()
    payload = integrated_payload()
    payload["modules"]["mystery"] = {}
    try:
        router.plan(payload)
    except HTTPException as exc:
        assert exc.status_code == 422
        assert "unsupported campus ops modules" in str(exc.detail)
    else:
        raise AssertionError("unknown module must fail closed")


def test_person_level_payload_is_rejected_at_api_boundary() -> None:
    router = load_router()
    try:
        router.optimize_food({
            "student_id": "forbidden",
            "demand_scenarios": [{"demand": 10, "weight": 1.0}],
            "max_capacity": 20,
            "waste_weight": 1,
            "shortage_weight": 1,
            "method_eligibility": "PILOT_ELIGIBLE",
        })
    except HTTPException as exc:
        assert exc.status_code == 422
    else:
        raise AssertionError("person-level payload must fail at API boundary")


def test_capabilities_declares_truth_and_privacy_boundary() -> None:
    router = load_router()
    result = router.capabilities()
    assert {"food", "shuttle", "space_activation", "class_scheduling", "campus_state", "integrated_plan"}.issubset(set(result["modules"]))
    assert result["automatic_actuation"] is False
    assert "person-level" in result["privacy_boundary"].lower()


def test_fastapi_main_registers_campus_ops_router() -> None:
    source = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")
    assert "campus_ops" in source
    assert "app.include_router(campus_ops.router)" in source


def main() -> int:
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
        print(f"PASS {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
