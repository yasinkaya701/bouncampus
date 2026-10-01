from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.decision.campus_contract import validate_no_person_level_data
from app.decision.campus_ops import (
    build_campus_ops_bundle,
    optimize_shuttle_plan,
    optimize_space_plan,
)
from app.decision.campus_state import build_campus_state
from app.decision.class_conflicts import optimize_conflict_aware_class_schedule
from app.decision.energy_advisory import plan_energy_advisory
from app.decision.food_production import optimize_food_production
from app.decision.resource_allocation import allocate_shared_capacity
from app.decision.water_advisory import plan_water_advisory

ALLOWED_MODULES = frozenset(
    {"food", "shuttle", "spaces", "classes", "resources", "energy", "water"}
)


def _mapping(value: Any, *, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def build_integrated_campus_plan(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Run one advisory campus-ops pass behind a shared decision-time state gate."""

    validate_no_person_level_data(payload, path="plan")
    state = build_campus_state(
        payload.get("zones", []),
        _mapping(payload.get("sources", {}), name="sources"),
        decision_time=str(payload.get("decision_time") or ""),
    )

    requested = _mapping(payload.get("modules", {}), name="modules")
    unknown = sorted(set(str(key) for key in requested) - ALLOWED_MODULES)
    if unknown:
        raise ValueError(f"unsupported campus ops modules: {unknown}")

    results: dict[str, dict[str, Any]] = {}
    if state["decision_readiness"] != "WITHHOLD":
        if "food" in requested:
            config = _mapping(requested["food"], name="modules.food")
            results["food"] = optimize_food_production(
                demand_scenarios=config.get("demand_scenarios", []),
                max_capacity=config.get("max_capacity"),
                waste_weight=config.get("waste_weight"),
                shortage_weight=config.get("shortage_weight"),
                method_eligibility=str(config.get("method_eligibility") or "SANDBOX_ONLY"),
            )
        if "shuttle" in requested:
            config = _mapping(requested["shuttle"], name="modules.shuttle")
            results["shuttle"] = optimize_shuttle_plan(
                demand_scenarios=config.get("demand_scenarios", []),
                departure_options=config.get("departure_options", []),
                empty_seat_weight=config.get("empty_seat_weight"),
                shortage_weight=config.get("shortage_weight"),
                min_point_service_ratio=config.get("min_point_service_ratio", 0.9),
            )
        if "spaces" in requested:
            config = _mapping(requested["spaces"], name="modules.spaces")
            results["spaces"] = optimize_space_plan(
                occupancy_scenarios=config.get("occupancy_scenarios", []),
                zones=config.get("zones", []),
                idle_capacity_weight=config.get("idle_capacity_weight"),
                shortage_weight=config.get("shortage_weight"),
                min_point_service_ratio=config.get("min_point_service_ratio", 0.9),
            )
        if "classes" in requested:
            config = _mapping(requested["classes"], name="modules.classes")
            results["classes"] = optimize_conflict_aware_class_schedule(
                classes=config.get("classes", []),
                rooms=config.get("rooms", []),
                building_mismatch_weight=config.get("building_mismatch_weight", 0.0),
            )
        if "resources" in requested:
            config = _mapping(requested["resources"], name="modules.resources")
            results["resources"] = allocate_shared_capacity(
                total_capacity=config.get("total_capacity"),
                requests=config.get("requests", []),
            )
        if "energy" in requested:
            config = _mapping(requested["energy"], name="modules.energy")
            results["energy"] = plan_energy_advisory(
                zones=state.get("zones", []),
                low_utilization_threshold=config.get("low_utilization_threshold"),
                medium_utilization_threshold=config.get("medium_utilization_threshold"),
            )
        if "water" in requested:
            config = _mapping(requested["water"], name="modules.water")
            results["water"] = plan_water_advisory(
                zones=config.get("zones", []),
                elevated_ratio_threshold=config.get("elevated_ratio_threshold"),
                critical_ratio_threshold=config.get("critical_ratio_threshold"),
            )

    bundle_inputs: dict[str, Mapping[str, Any]] = {"campus_state": state, **results}
    bundle = build_campus_ops_bundle(bundle_inputs)
    return {
        "state": state,
        "modules": results,
        "bundle": bundle,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "impact_claim_allowed": False,
    }
