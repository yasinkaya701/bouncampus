from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.decision.campus_contract import CONTRACT_VERSION
from app.decision.campus_portfolio import build_campus_portfolio
from app.decision.campus_state import build_campus_state
from app.decision.classroom_policy import allocate_classrooms
from app.decision.shuttle_policy import plan_shuttle_capacity

router = APIRouter(prefix="/api/v1/campus-ops", tags=["campus-ops"])


class CampusStateRequest(BaseModel):
    decision_time: str
    zones: list[dict[str, Any]]
    sources: dict[str, dict[str, Any]]


class ShuttlePlanRequest(BaseModel):
    routes: list[dict[str, Any]]
    reserve_ratio: float = 0.10
    upstream_readiness: str = "REVIEW_REQUIRED"


class ClassroomAllocationRequest(BaseModel):
    sessions: list[dict[str, Any]]
    rooms: list[dict[str, Any]]
    upstream_readiness: str = "REVIEW_REQUIRED"


class CampusPortfolioRequest(BaseModel):
    campus_state: dict[str, Any]
    shuttle_plan: dict[str, Any] | None = None
    classroom_plan: dict[str, Any] | None = None
    food_decision: dict[str, Any] | None = None
    energy_decision: dict[str, Any] | None = None


class CampusOpsPlanRequest(BaseModel):
    decision_time: str
    zones: list[dict[str, Any]]
    sources: dict[str, dict[str, Any]]
    shuttle_routes: list[dict[str, Any]] = Field(default_factory=list)
    reserve_ratio: float = 0.10
    sessions: list[dict[str, Any]] = Field(default_factory=list)
    rooms: list[dict[str, Any]] = Field(default_factory=list)


def _unprocessable(exc: ValueError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(exc))


@router.get("/contract")
def get_campus_ops_contract() -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "domains": ["campus_state", "shuttle", "classroom", "portfolio"],
        "decision_readiness_states": ["PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD"],
        "provenance_states": [
            "PUBLIC_SOURCE",
            "MODEL_ESTIMATE",
            "POLICY_HEURISTIC",
            "MEASURED_PILOT",
        ],
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "privacy_boundary": (
            "Aggregate planning only; student identifiers, BUCard identifiers, "
            "scholarship data, and individual movement traces are rejected."
        ),
        "truth_boundary": (
            "No live BMS, turnstile/Wi-Fi occupancy, shuttle GPS, cafeteria POS, "
            "or registrar integration is claimed unless separately verified."
        ),
        "impact_boundary": (
            "Model outputs and policy heuristics are not achieved energy, carbon, "
            "water, food-waste, or cost savings."
        ),
    }


@router.post("/state")
def build_state(payload: CampusStateRequest) -> dict[str, Any]:
    try:
        return build_campus_state(
            payload.zones,
            payload.sources,
            decision_time=payload.decision_time,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/shuttle/plan")
def build_shuttle_plan(payload: ShuttlePlanRequest) -> dict[str, Any]:
    try:
        return plan_shuttle_capacity(
            payload.routes,
            reserve_ratio=payload.reserve_ratio,
            upstream_readiness=payload.upstream_readiness,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/classrooms/allocate")
def build_classroom_plan(payload: ClassroomAllocationRequest) -> dict[str, Any]:
    try:
        return allocate_classrooms(
            payload.sessions,
            payload.rooms,
            upstream_readiness=payload.upstream_readiness,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/portfolio")
def build_portfolio(payload: CampusPortfolioRequest) -> dict[str, Any]:
    try:
        return build_campus_portfolio(
            campus_state=payload.campus_state,
            shuttle_plan=payload.shuttle_plan,
            classroom_plan=payload.classroom_plan,
            food_decision=payload.food_decision,
            energy_decision=payload.energy_decision,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/plan")
def plan_campus_operations(payload: CampusOpsPlanRequest) -> dict[str, Any]:
    """Run one decision-cutoff-consistent advisory planning pass across CS1 domains."""

    try:
        state = build_campus_state(
            payload.zones,
            payload.sources,
            decision_time=payload.decision_time,
        )
        shuttle = plan_shuttle_capacity(
            payload.shuttle_routes,
            reserve_ratio=payload.reserve_ratio,
            upstream_readiness=state["decision_readiness"],
        )
        classroom = allocate_classrooms(
            payload.sessions,
            payload.rooms,
            upstream_readiness=state["decision_readiness"],
        )
        portfolio = build_campus_portfolio(
            campus_state=state,
            shuttle_plan=shuttle,
            classroom_plan=classroom,
        )
        return {
            "state": state,
            "shuttle": shuttle,
            "classroom": classroom,
            "portfolio": portfolio,
        }
    except ValueError as exc:
        raise _unprocessable(exc) from exc
