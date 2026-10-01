from typing import Any

from fastapi import APIRouter, Body, HTTPException

from app.decision.campus_operations import (
    DECISION_POLICY_VERSION,
    TRUTH_BOUNDARY,
    allocate_classrooms,
    build_operations_snapshot,
    plan_food_service,
    plan_shuttle_service,
)
from app.decision.meal_recommendation import (
    build_recommendation_impression,
    rank_menu_items,
)
from app.decision.space_operations import plan_space_service

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
            "meal_recommendation": {
                "endpoint": "POST /api/v1/decision/meals/recommend",
                "impression_endpoint": "POST /api/v1/decision/meals/impression",
                "decision": "auditable student-facing menu ranking baseline",
                "hard_boundary": "no generated-data collaborative model promoted as validated",
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
            "space": {
                "endpoint": "POST /api/v1/decision/spaces/plan",
                "decision": "capacity-safe flexible-space consolidation",
                "hard_boundary": "no automatic building/HVAC control",
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


@router.post("/meals/recommend")
def post_meal_recommendation(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return rank_menu_items(payload)


@router.post("/meals/impression")
def post_meal_impression(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    ranking = payload.get("ranking")
    if not isinstance(ranking, dict):
        raise HTTPException(status_code=422, detail="ranking object is required")
    try:
        return build_recommendation_impression(
            ranking,
            request_id=str(payload.get("request_id") or ""),
            context=payload.get("context") if isinstance(payload.get("context"), dict) else {},
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/shuttle/plan")
def post_shuttle_plan(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return plan_shuttle_service(payload)


@router.post("/classrooms/allocate")
def post_classroom_allocation(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return allocate_classrooms(payload)


@router.post("/spaces/plan")
def post_space_plan(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return plan_space_service(payload)


@router.post("/snapshot")
def post_operations_snapshot(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return build_operations_snapshot(payload)
