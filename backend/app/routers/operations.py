from typing import Any

from fastapi import APIRouter, Body

from app.decision.campus_operations import (
    DECISION_POLICY_VERSION,
    TRUTH_BOUNDARY,
    allocate_classrooms,
    build_operations_snapshot,
    plan_food_service,
    plan_shuttle_service,
)

router = APIRouter(prefix="/api/v1/decision", tags=["decision-operations"])


@router.get("/capabilities")
def get_decision_capabilities() -> dict[str, Any]:
    return {
        "policy_version": DECISION_POLICY_VERSION,
        "domains": {
            "food": {
                "endpoint": "POST /api/v1/decision/food/plan",
                "decision": "operator-reviewed production quantity",
                "hard_boundary": "no automatic kitchen dispatch",
            },
            "shuttle": {
                "endpoint": "POST /api/v1/decision/shuttle/plan",
                "decision": "capacity allocation by departure",
                "hard_boundary": "no automatic vehicle dispatch",
            },
            "classroom": {
                "endpoint": "POST /api/v1/decision/classrooms/allocate",
                "decision": "capacity/conflict/energy-aware room assignment",
                "hard_boundary": "no automatic timetable commit",
            },
            "snapshot": {
                "endpoint": "POST /api/v1/decision/snapshot",
                "decision": "fail-closed cross-domain readiness view",
            },
        },
        "readiness_states": ["PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD"],
        "truth_boundary": TRUTH_BOUNDARY,
    }


@router.post("/food/plan")
def post_food_plan(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return plan_food_service(payload)


@router.post("/shuttle/plan")
def post_shuttle_plan(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return plan_shuttle_service(payload)


@router.post("/classrooms/allocate")
def post_classroom_allocation(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return allocate_classrooms(payload)


@router.post("/snapshot")
def post_operations_snapshot(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return build_operations_snapshot(payload)
