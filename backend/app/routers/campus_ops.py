from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.decision.campus_ops import (
    allocate_shared_capacity,
    build_campus_ops_bundle,
    optimize_class_schedule,
    optimize_food_production,
    optimize_shuttle_plan,
)

router = APIRouter(prefix="/api/v1/ops", tags=["campus-operations"])


def _payload_value(payload: dict[str, Any], key: str, default: Any) -> Any:
    value = payload.get(key, default)
    return default if value is None else value


@router.get("/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "modules": [
            "food",
            "shuttle",
            "class_scheduling",
            "shared_capacity",
            "bundle",
        ],
        "decision_mode": "ADVISORY",
        "automatic_actuation": False,
        "operator_approval_required": True,
        "truth_boundary": (
            "No live cafeteria POS, shuttle GPS, room-occupancy, or BMS telemetry "
            "is implied by these optimization endpoints."
        ),
        "objective_units": "REGISTERED_RELATIVE_SENSITIVITY_UNITS",
    }


@router.post("/food")
def optimize_food(payload: dict[str, Any]) -> dict[str, Any]:
    return optimize_food_production(
        demand_scenarios=_payload_value(payload, "demand_scenarios", []),
        max_capacity=_payload_value(payload, "max_capacity", None),
        waste_weight=_payload_value(payload, "waste_weight", None),
        shortage_weight=_payload_value(payload, "shortage_weight", None),
        method_eligibility=str(
            _payload_value(payload, "method_eligibility", "EVALUATED_OFFLINE")
        ),
    )


@router.post("/shuttle")
def optimize_shuttle(payload: dict[str, Any]) -> dict[str, Any]:
    return optimize_shuttle_plan(
        demand_scenarios=_payload_value(payload, "demand_scenarios", []),
        departure_options=_payload_value(payload, "departure_options", []),
        empty_seat_weight=_payload_value(payload, "empty_seat_weight", None),
        shortage_weight=_payload_value(payload, "shortage_weight", None),
        min_point_service_ratio=_payload_value(
            payload,
            "min_point_service_ratio",
            0.9,
        ),
    )


@router.post("/classes")
def optimize_classes(payload: dict[str, Any]) -> dict[str, Any]:
    return optimize_class_schedule(
        classes=_payload_value(payload, "classes", []),
        rooms=_payload_value(payload, "rooms", []),
        building_mismatch_weight=_payload_value(
            payload,
            "building_mismatch_weight",
            0.0,
        ),
    )


@router.post("/resources")
def allocate_resources(payload: dict[str, Any]) -> dict[str, Any]:
    return allocate_shared_capacity(
        total_capacity=_payload_value(payload, "total_capacity", None),
        requests=_payload_value(payload, "requests", []),
    )


@router.post("/bundle")
def bundle(payload: dict[str, Any]) -> dict[str, Any]:
    modules = _payload_value(payload, "modules", {})
    if not isinstance(modules, dict):
        modules = {}
    return build_campus_ops_bundle(modules)
