from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.decision.building_energy_policy import plan_building_energy
from app.decision.campus_contract import CONTRACT_VERSION, PROVENANCE_STATES
from app.decision.campus_portfolio import build_campus_portfolio
from app.decision.campus_state import build_campus_state
from app.decision.classroom_policy import allocate_classrooms
from app.decision.food_ops_policy import plan_food_production
from app.decision.shared_capacity_policy import allocate_shared_capacity
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
    room_inventory_provenance: str = "UNAVAILABLE"
    attendance_provenance: str = "UNAVAILABLE"
    upstream_readiness: str = "REVIEW_REQUIRED"


class FoodPlanRequest(BaseModel):
    demand_scenarios: list[dict[str, Any]]
    max_capacity: float
    waste_weight: float
    shortage_weight: float
    method_eligibility: str
    upstream_readiness: str = "REVIEW_REQUIRED"


class EnergyPlanRequest(BaseModel):
    zones: list[dict[str, Any]]
    low_utilization_threshold: float
    medium_utilization_threshold: float
    upstream_readiness: str = "REVIEW_REQUIRED"


class SharedCapacityRequest(BaseModel):
    total_capacity: int
    requests: list[dict[str, Any]]


class FoodPlanConfig(BaseModel):
    demand_scenarios: list[dict[str, Any]]
    max_capacity: float
    waste_weight: float
    shortage_weight: float
    method_eligibility: str


class EnergyPlanConfig(BaseModel):
    low_utilization_threshold: float
    medium_utilization_threshold: float


class SharedCapacityConfig(BaseModel):
    total_capacity: int
    requests: list[dict[str, Any]]


class CampusPortfolioRequest(BaseModel):
    campus_state: dict[str, Any]
    shuttle_plan: dict[str, Any] | None = None
    classroom_plan: dict[str, Any] | None = None
    food_decision: dict[str, Any] | None = None
    energy_decision: dict[str, Any] | None = None
    shared_capacity_decision: dict[str, Any] | None = None


class CampusOpsPlanRequest(BaseModel):
    decision_time: str
    zones: list[dict[str, Any]]
    sources: dict[str, dict[str, Any]]
    shuttle_routes: list[dict[str, Any]] = Field(default_factory=list)
    reserve_ratio: float = 0.10
    sessions: list[dict[str, Any]] = Field(default_factory=list)
    rooms: list[dict[str, Any]] = Field(default_factory=list)
    room_inventory_provenance: str = "UNAVAILABLE"
    attendance_provenance: str = "UNAVAILABLE"
    food: FoodPlanConfig | None = None
    energy: EnergyPlanConfig | None = None
    shared_capacity: SharedCapacityConfig | None = None


def _unprocessable(exc: ValueError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(exc))


@router.get("/contract")
def get_campus_ops_contract() -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "domains": [
            "campus_state",
            "shuttle",
            "classroom",
            "food",
            "energy",
            "shared_capacity",
            "portfolio",
        ],
        "decision_readiness_states": ["PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD"],
        "provenance_states": list(PROVENANCE_STATES),
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
            room_inventory_provenance=payload.room_inventory_provenance,
            attendance_provenance=payload.attendance_provenance,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/food/plan")
def build_food_plan(payload: FoodPlanRequest) -> dict[str, Any]:
    try:
        return plan_food_production(
            demand_scenarios=payload.demand_scenarios,
            max_capacity=payload.max_capacity,
            waste_weight=payload.waste_weight,
            shortage_weight=payload.shortage_weight,
            method_eligibility=payload.method_eligibility,
            upstream_readiness=payload.upstream_readiness,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/energy/plan")
def build_energy_plan(payload: EnergyPlanRequest) -> dict[str, Any]:
    try:
        return plan_building_energy(
            zones=payload.zones,
            low_utilization_threshold=payload.low_utilization_threshold,
            medium_utilization_threshold=payload.medium_utilization_threshold,
            upstream_readiness=payload.upstream_readiness,
        )
    except ValueError as exc:
        raise _unprocessable(exc) from exc


@router.post("/shared-capacity/allocate")
def build_shared_capacity_plan(payload: SharedCapacityRequest) -> dict[str, Any]:
    try:
        return allocate_shared_capacity(
            total_capacity=payload.total_capacity,
            requests=payload.requests,
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
            shared_capacity_decision=payload.shared_capacity_decision,
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
        readiness = state["decision_readiness"]
        shuttle = plan_shuttle_capacity(
            payload.shuttle_routes,
            reserve_ratio=payload.reserve_ratio,
            upstream_readiness=readiness,
        )
        classroom = allocate_classrooms(
            payload.sessions,
            payload.rooms,
            upstream_readiness=readiness,
            room_inventory_provenance=payload.room_inventory_provenance,
            attendance_provenance=payload.attendance_provenance,
        )

        food = None
        if payload.food is not None:
            food = plan_food_production(
                demand_scenarios=payload.food.demand_scenarios,
                max_capacity=payload.food.max_capacity,
                waste_weight=payload.food.waste_weight,
                shortage_weight=payload.food.shortage_weight,
                method_eligibility=payload.food.method_eligibility,
                upstream_readiness=readiness,
            )

        energy = None
        if payload.energy is not None:
            energy = plan_building_energy(
                zones=state["zones"],
                low_utilization_threshold=payload.energy.low_utilization_threshold,
                medium_utilization_threshold=payload.energy.medium_utilization_threshold,
                upstream_readiness=readiness,
            )

        shared_capacity = None
        if payload.shared_capacity is not None:
            shared_capacity = allocate_shared_capacity(
                total_capacity=payload.shared_capacity.total_capacity,
                requests=payload.shared_capacity.requests,
            )

        portfolio = build_campus_portfolio(
            campus_state=state,
            shuttle_plan=shuttle,
            classroom_plan=classroom,
            food_decision=food,
            energy_decision=energy,
            shared_capacity_decision=shared_capacity,
        )
        return {
            "state": state,
            "shuttle": shuttle,
            "classroom": classroom,
            "food": food,
            "energy": energy,
            "shared_capacity": shared_capacity,
            "portfolio": portfolio,
        }
    except ValueError as exc:
        raise _unprocessable(exc) from exc
