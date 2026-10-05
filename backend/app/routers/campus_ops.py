from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.decision.campus_bundle import build_campus_ops_bundle
from app.decision.campus_contract import validate_no_person_level_data
from app.decision.capacity_planning import optimize_shuttle_plan, optimize_space_plan
from app.decision.campus_orchestrator import build_integrated_campus_plan
from app.decision.campus_state import build_campus_state
from app.decision.class_conflicts import optimize_conflict_aware_class_schedule
from app.decision.dining_count_truth import aggregate_dining_count_events, validate_dining_count_event
from app.decision.energy_advisory import plan_energy_advisory
from app.decision.food_production import optimize_food_production
from app.decision.resource_allocation import allocate_shared_capacity
from app.decision.roomnode_truth import summarize_roomnode_window, validate_roomnode_event
from app.decision.solar_site_planning import analyze_room_solar_exposure, rank_new_building_orientations
from app.decision.water_advisory import plan_water_advisory

router = APIRouter(prefix="/api/v1/ops", tags=["campus-operations"])


def _payload_value(payload: dict[str, Any], key: str, default: Any) -> Any:
    value = payload.get(key, default)
    return default if value is None else value


def _validate(payload: dict[str, Any]) -> None:
    try:
        validate_no_person_level_data(payload, path="api_payload")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "modules": [
            "campus_state",
            "food",
            "shuttle",
            "space_activation",
            "class_scheduling",
            "solar_exposure",
            "site_orientation",
            "shared_capacity",
            "energy_advisory",
            "water_advisory",
            "roomnode_observations",
            "dining_physical_counts",
            "bundle",
            "integrated_plan",
        ],
        "decision_mode": "ADVISORY",
        "automatic_actuation": False,
        "operator_approval_required": True,
        "truth_boundary": "RoomNode and dining physical-count observation endpoints validate caller-supplied physical event payloads only and do not imply a live RoomNode or dining counter connection. Dining counts remain descriptive device observations: serving tray counts are not promoted to portions or actual_served, and no reconciled service truth, savings, or operational impact is implied. No live cafeteria POS, shuttle GPS, room-occupancy feed, BMS, smart-meter/water-meter, Wi-Fi/turnstile, registrar telemetry, calibrated daylight simulation, or calibrated building thermal model is implied by these optimization endpoints.",
        "privacy_boundary": "Aggregate planning only; person-level identifiers and individual movement traces are rejected. RoomNode and dining physical-count event payloads use dedicated fail-closed anonymous measurement contracts.",
        "objective_units": "REGISTERED_RELATIVE_SENSITIVITY_UNITS",
    }


@router.post("/dining-count/event")
def dining_count_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate one caller-supplied anonymous dining physical-count event."""

    try:
        return validate_dining_count_event(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/dining-count/window")
def dining_count_window(payload: dict[str, Any]) -> dict[str, Any]:
    """Expose retry-safe descriptive dining count aggregation for one station/time window."""

    try:
        return aggregate_dining_count_events(
            _payload_value(payload, "events", []),
            expected_station_id=str(_payload_value(payload, "station_id", "")),
            window_start=str(_payload_value(payload, "window_start", "")),
            window_end=str(_payload_value(payload, "window_end", "")),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/roomnode/event")
def roomnode_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate one caller-supplied RoomNode observation without promoting it to a decision."""

    try:
        return validate_roomnode_event(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/roomnode/window")
def roomnode_window(payload: dict[str, Any]) -> dict[str, Any]:
    """Expose retry-safe descriptive RoomNode aggregation for one station/time window."""

    try:
        return summarize_roomnode_window(
            _payload_value(payload, "events", []),
            station_id=str(_payload_value(payload, "station_id", "")),
            window_start=str(_payload_value(payload, "window_start", "")),
            window_end=str(_payload_value(payload, "window_end", "")),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/state")
def state(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    try:
        return build_campus_state(
            _payload_value(payload, "zones", []),
            _payload_value(payload, "sources", {}),
            decision_time=str(_payload_value(payload, "decision_time", "")),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/food")
def optimize_food(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return optimize_food_production(
        demand_scenarios=_payload_value(payload, "demand_scenarios", []),
        max_capacity=_payload_value(payload, "max_capacity", None),
        waste_weight=_payload_value(payload, "waste_weight", None),
        shortage_weight=_payload_value(payload, "shortage_weight", None),
        method_eligibility=str(_payload_value(payload, "method_eligibility", "SANDBOX_ONLY")),
    )


@router.post("/shuttle")
def optimize_shuttle(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return optimize_shuttle_plan(
        demand_scenarios=_payload_value(payload, "demand_scenarios", []),
        departure_options=_payload_value(payload, "departure_options", []),
        empty_seat_weight=_payload_value(payload, "empty_seat_weight", None),
        shortage_weight=_payload_value(payload, "shortage_weight", None),
        min_point_service_ratio=_payload_value(payload, "min_point_service_ratio", 0.9),
    )


@router.post("/spaces")
def optimize_spaces(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return optimize_space_plan(
        occupancy_scenarios=_payload_value(payload, "occupancy_scenarios", []),
        zones=_payload_value(payload, "zones", []),
        idle_capacity_weight=_payload_value(payload, "idle_capacity_weight", None),
        shortage_weight=_payload_value(payload, "shortage_weight", None),
        min_point_service_ratio=_payload_value(payload, "min_point_service_ratio", 0.9),
    )


@router.post("/classes")
def optimize_classes(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return optimize_conflict_aware_class_schedule(
        classes=_payload_value(payload, "classes", []),
        rooms=_payload_value(payload, "rooms", []),
        building_mismatch_weight=_payload_value(payload, "building_mismatch_weight", 0.0),
        solar_exposure_weight=_payload_value(payload, "solar_exposure_weight", 0.0),
    )


@router.post("/solar")
def solar_review(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return analyze_room_solar_exposure(
        latitude_deg=_payload_value(payload, "latitude_deg", None),
        longitude_deg=_payload_value(payload, "longitude_deg", None),
        timestamps=_payload_value(payload, "timestamps", []),
        rooms=_payload_value(payload, "rooms", []),
        class_sessions=_payload_value(payload, "class_sessions", []),
        affected_threshold=_payload_value(payload, "affected_threshold", 0.25),
    )


@router.post("/site-orientation")
def site_orientation(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return rank_new_building_orientations(
        latitude_deg=_payload_value(payload, "latitude_deg", None),
        longitude_deg=_payload_value(payload, "longitude_deg", None),
        timestamps=_payload_value(payload, "timestamps", []),
        facade_program=_payload_value(payload, "facade_program", []),
        candidate_orientations_deg=_payload_value(payload, "candidate_orientations_deg", []),
    )


@router.post("/resources")
def allocate_resources(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return allocate_shared_capacity(
        total_capacity=_payload_value(payload, "total_capacity", None),
        requests=_payload_value(payload, "requests", []),
    )


@router.post("/energy")
def optimize_energy(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return plan_energy_advisory(
        zones=_payload_value(payload, "zones", []),
        low_utilization_threshold=_payload_value(payload, "low_utilization_threshold", None),
        medium_utilization_threshold=_payload_value(payload, "medium_utilization_threshold", None),
    )


@router.post("/water")
def optimize_water(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    return plan_water_advisory(
        zones=_payload_value(payload, "zones", []),
        elevated_ratio_threshold=_payload_value(payload, "elevated_ratio_threshold", None),
        critical_ratio_threshold=_payload_value(payload, "critical_ratio_threshold", None),
    )


@router.post("/bundle")
def bundle(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    modules = _payload_value(payload, "modules", {})
    if not isinstance(modules, dict):
        modules = {}
    return build_campus_ops_bundle(modules)


@router.post("/plan")
def plan(payload: dict[str, Any]) -> dict[str, Any]:
    _validate(payload)
    try:
        return build_integrated_campus_plan(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
