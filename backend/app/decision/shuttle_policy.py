from __future__ import annotations

import importlib.util
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def _load_contract():
    try:
        from app.decision import campus_contract as contract  # type: ignore

        return contract
    except ModuleNotFoundError:
        path = Path(__file__).with_name("campus_contract.py")
        spec = importlib.util.spec_from_file_location("campus_contract_fallback", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load campus contract from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


CONTRACT = _load_contract()
CONTRACT_VERSION = CONTRACT.CONTRACT_VERSION

LIMITATIONS = (
    "NO_LIVE_SHUTTLE_GPS_CLAIM",
    "NO_LIVE_SHUTTLE_OCCUPANCY_CLAIM",
    "NO_UNVERIFIED_VEHICLE_CAPACITY_CLAIM",
    "NO_PASSENGER_LEVEL_TRACKING",
    "POLICY_HEURISTIC_CAPACITY_PLAN",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _finite(value: Any, *, field: str, minimum: float | None = None) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{field} must be finite")
    if minimum is not None and numeric < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return numeric


def _positive(value: Any, *, field: str) -> float:
    numeric = _finite(value, field=field, minimum=0.0)
    if numeric <= 0:
        raise ValueError(f"{field} must be greater than zero")
    return numeric


def _withhold(reason_code: str) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "routes": [],
        "reason_codes": [reason_code],
        "limitations": list(LIMITATIONS),
    }


def _normalize_route(route: Mapping[str, Any], reserve_ratio: float) -> dict[str, Any]:
    route_id = str(route.get("route_id", "")).strip()
    origin = str(route.get("origin", "")).strip().lower()
    destination = str(route.get("destination", "")).strip().lower()
    if not route_id:
        raise ValueError("route_id is required")
    if not origin or not destination or origin == destination:
        raise ValueError(f"route {route_id} must have distinct origin/destination")

    capacity_provenance = CONTRACT.normalize_provenance(
        route.get("capacity_provenance", "UNAVAILABLE"),
        field=f"route {route_id} capacity_provenance",
    )
    if capacity_provenance not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        raise ValueError(f"route {route_id} capacity provenance is not verified")

    demand = _finite(
        route.get("forecast_demand"), field=f"route {route_id} forecast_demand", minimum=0.0
    )
    vehicle_capacity = _positive(
        route.get("vehicle_capacity"), field=f"route {route_id} vehicle_capacity"
    )
    available_vehicles_float = _finite(
        route.get("available_vehicles"),
        field=f"route {route_id} available_vehicles",
        minimum=0.0,
    )
    if not available_vehicles_float.is_integer():
        raise ValueError(f"route {route_id} available_vehicles must be an integer")
    available_vehicles = int(available_vehicles_float)

    service_window = _positive(
        route.get("service_window_min"), field=f"route {route_id} service_window_min"
    )
    round_trip = _positive(
        route.get("round_trip_min"), field=f"route {route_id} round_trip_min"
    )
    min_headway = _positive(
        route.get("min_headway_min"), field=f"route {route_id} min_headway_min"
    )
    max_headway = _positive(
        route.get("max_headway_min"), field=f"route {route_id} max_headway_min"
    )
    if min_headway > max_headway:
        raise ValueError(f"route {route_id} min_headway_min cannot exceed max_headway_min")

    required_seats = int(math.ceil(demand * (1.0 + reserve_ratio) - 1e-9))
    trips_required = (
        int(math.ceil(required_seats / vehicle_capacity - 1e-12))
        if required_seats > 0
        else 0
    )
    trips_per_vehicle = int(math.floor(service_window / round_trip))
    max_supported_trips = available_vehicles * trips_per_vehicle
    supported_seats = int(round(max_supported_trips * vehicle_capacity))
    shortage = max(0, required_seats - supported_seats)
    feasible = trips_required <= max_supported_trips

    if trips_required <= 0:
        recommended_headway = max_headway
    else:
        raw_headway = service_window / trips_required
        recommended_headway = max(min_headway, min(max_headway, raw_headway))

    return {
        "route_id": route_id,
        "origin": origin,
        "destination": destination,
        "forecast_demand": int(round(demand)),
        "forecast_provenance": "MODEL_ESTIMATE",
        "reserve_ratio": reserve_ratio,
        "reserve_basis": "POLICY_HEURISTIC",
        "required_seats": required_seats,
        "vehicle_capacity": int(round(vehicle_capacity)),
        "available_vehicles": available_vehicles,
        "capacity_provenance": capacity_provenance,
        "capacity_verified": True,
        "trips_required": trips_required,
        "max_supported_trips": max_supported_trips,
        "capacity_feasible": feasible,
        "unserved_seat_demand_estimate": shortage,
        "recommended_headway_min": round(recommended_headway, 2),
        "headway_semantics": "PLANNING_TARGET_NOT_LIVE_DISPATCH",
    }


def plan_shuttle_capacity(
    routes: Sequence[Mapping[str, Any]],
    *,
    reserve_ratio: float = 0.10,
    upstream_readiness: str = "REVIEW_REQUIRED",
) -> dict[str, Any]:
    """Build an aggregate, human-reviewed shuttle capacity/headway plan.

    Capacity-sensitive output is emitted only when the supplied vehicle capacity
    snapshot has verified provenance. This function never implies live GPS,
    passenger occupancy, or autonomous dispatch.
    """

    CONTRACT.validate_no_person_level_data(routes, path="routes")
    reserve = _finite(reserve_ratio, field="reserve_ratio", minimum=0.0)
    if reserve > 1.0:
        raise ValueError("reserve_ratio must be <= 1.0")

    normalized_upstream = str(upstream_readiness).upper()
    if normalized_upstream not in CONTRACT.READINESS_STATES:
        raise ValueError(f"unsupported upstream_readiness: {upstream_readiness}")

    if normalized_upstream == "WITHHOLD":
        return _withhold("UPSTREAM_CAMPUS_STATE_WITHHELD")
    if not routes:
        return _withhold("NO_SHUTTLE_ROUTES_SUPPLIED")

    for raw_route in routes:
        if not isinstance(raw_route, Mapping):
            raise ValueError("each shuttle route must be a mapping")
        if not CONTRACT.is_verified_capacity_provenance(
            raw_route.get("capacity_provenance", "UNAVAILABLE")
        ):
            return _withhold("UNVERIFIED_SHUTTLE_CAPACITY")

    normalized_routes: list[dict[str, Any]] = []
    seen_route_ids: set[str] = set()
    reason_codes = ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"]
    for raw_route in routes:
        item = _normalize_route(raw_route, reserve)
        route_id = item["route_id"]
        if route_id in seen_route_ids:
            raise ValueError(f"duplicate route_id: {route_id}")
        seen_route_ids.add(route_id)
        normalized_routes.append(item)
        if not item["capacity_feasible"]:
            reason_codes.append(f"ROUTE_CAPACITY_SHORTFALL_{route_id.upper()}")

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "demand_provenance": "MODEL_ESTIMATE",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "routes": normalized_routes,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "limitations": list(LIMITATIONS),
    }
