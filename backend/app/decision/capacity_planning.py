"""Scalable exact capacity-subset planning for CS1 shuttle and space decisions.

The previous implementation enumerated every subset and rejected more than 18
options. Campus capacities are naturally fixed-decimal quantities, so this module
uses a sparse dynamic program keyed by achievable total capacity. For each capacity
it keeps only the lowest-activation subset, which is sufficient because the
uncertainty loss depends on a subset only through total capacity.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any

POLICY_VERSION = "capacity-planning-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"
SOLVER_SEMANTICS = "EXACT_SPARSE_FIXED_DECIMAL_CAPACITY_DP"
MAX_DECIMAL_PLACES = 3
MAX_DP_STATES = 250_000
EPSILON = 1e-12


def _base(scope: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": scope,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }


def _number(value: Any, *, minimum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    if minimum is not None and numeric < minimum:
        return None
    return numeric


def _text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def _scenarios(rows: Sequence[Mapping[str, Any]] | Any) -> list[tuple[float, float]] | None:
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        return None
    normalized: list[tuple[float, float]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        demand = _number(row.get("demand"), minimum=0.0)
        weight = _number(row.get("weight"), minimum=0.0)
        if demand is None or weight is None:
            return None
        if weight > 0:
            normalized.append((demand, weight))
    total = sum(weight for _, weight in normalized)
    if not normalized or total <= 0:
        return None
    return [(demand, weight / total) for demand, weight in normalized]


def _capacity_decimal(value: Any) -> tuple[Decimal, int] | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    if not decimal_value.is_finite() or decimal_value <= 0:
        return None
    normalized = decimal_value.normalize()
    places = max(0, -normalized.as_tuple().exponent)
    if places > MAX_DECIMAL_PLACES:
        return None
    return decimal_value, places


def _normalize_options(
    rows: Sequence[Mapping[str, Any]] | Any,
    *,
    id_key: str,
) -> tuple[list[tuple[str, int, float]], int] | None:
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)) or not rows:
        return None

    parsed: list[tuple[str, Decimal, int, float]] = []
    seen: set[str] = set()
    max_places = 0
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        option_id = _text(row.get(id_key))
        capacity_result = _capacity_decimal(row.get("capacity"))
        activation = _number(row.get("activation_weight", 0.0), minimum=0.0)
        if (
            option_id is None
            or option_id in seen
            or capacity_result is None
            or activation is None
        ):
            return None
        capacity, places = capacity_result
        seen.add(option_id)
        max_places = max(max_places, places)
        parsed.append((option_id, capacity, places, activation))

    scale = 10**max_places
    normalized: list[tuple[str, int, float]] = []
    for option_id, capacity, _places, activation in parsed:
        scaled = capacity * scale
        if scaled != scaled.to_integral_value():
            return None
        units = int(scaled)
        if units <= 0:
            return None
        normalized.append((option_id, units, activation))
    normalized.sort(key=lambda row: row[0])
    return normalized, scale


def _expected_loss(
    capacity: float,
    activation: float,
    scenarios: Sequence[tuple[float, float]],
    *,
    idle_weight: float,
    shortage_weight: float,
) -> float:
    return activation + sum(
        probability
        * (
            idle_weight * max(capacity - demand, 0.0)
            + shortage_weight * max(demand - capacity, 0.0)
        )
        for demand, probability in scenarios
    )


def _candidate_is_better(
    candidate: tuple[float, float, tuple[str, ...]],
    incumbent: tuple[float, float, tuple[str, ...]] | None,
) -> bool:
    if incumbent is None:
        return True
    objective, capacity, ids = candidate
    best_objective, best_capacity, best_ids = incumbent
    if objective < best_objective - EPSILON:
        return True
    return math.isclose(
        objective,
        best_objective,
        rel_tol=0.0,
        abs_tol=EPSILON,
    ) and (capacity, ids) < (best_capacity, best_ids)


def _sparse_capacity_dp(
    options: Sequence[tuple[str, int, float]],
) -> tuple[dict[int, tuple[float, tuple[str, ...]]], bool]:
    """Map capacity -> minimum activation subset; second value flags state overflow."""

    states: dict[int, tuple[float, tuple[str, ...]]] = {0: (0.0, ())}
    for option_id, option_capacity, option_activation in options:
        updated = dict(states)
        for capacity, (activation, ids) in states.items():
            new_capacity = capacity + option_capacity
            candidate_activation = activation + option_activation
            candidate_ids = ids + (option_id,)
            existing = updated.get(new_capacity)
            if existing is None:
                updated[new_capacity] = (candidate_activation, candidate_ids)
                continue
            existing_activation, existing_ids = existing
            if (
                candidate_activation < existing_activation - EPSILON
                or (
                    math.isclose(
                        candidate_activation,
                        existing_activation,
                        rel_tol=0.0,
                        abs_tol=EPSILON,
                    )
                    and candidate_ids < existing_ids
                )
            ):
                updated[new_capacity] = (candidate_activation, candidate_ids)
        if len(updated) > MAX_DP_STATES:
            return {}, True
        states = updated
    return states, False


def _optimize_capacity_subset(
    *,
    scope: str,
    scenarios: Sequence[tuple[float, float]],
    options: Sequence[tuple[str, int, float]],
    scale: int,
    idle_weight: float,
    shortage_weight: float,
    service_ratio: float,
    selected_ids_key: str,
    full_capacity_reason: str,
    no_bundle_reason: str,
    state_limit_reason: str,
    extra_fields: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result = {**_base(scope), **dict(extra_fields or {})}
    full_capacity_units = sum(capacity for _, capacity, _ in options)
    full_capacity = full_capacity_units / scale
    required_capacity = max(service_ratio * demand for demand, _ in scenarios)
    if full_capacity + 1e-9 < required_capacity:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            selected_ids_key: [],
            "selected_capacity": int(round(full_capacity)),
            "reason_codes": [full_capacity_reason],
        }

    states, overflow = _sparse_capacity_dp(options)
    if overflow:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            selected_ids_key: [],
            "selected_capacity": None,
            "solver_semantics": SOLVER_SEMANTICS,
            "reason_codes": [state_limit_reason],
        }

    best: tuple[float, float, tuple[str, ...]] | None = None
    for capacity_units, (activation, ids) in states.items():
        if capacity_units == 0:
            continue
        capacity = capacity_units / scale
        if capacity + 1e-9 < required_capacity:
            continue
        objective = _expected_loss(
            capacity,
            activation,
            scenarios,
            idle_weight=idle_weight,
            shortage_weight=shortage_weight,
        )
        ranked = (objective, capacity, ids)
        if _candidate_is_better(ranked, best):
            best = ranked

    if best is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            selected_ids_key: [],
            "selected_capacity": None,
            "reason_codes": [no_bundle_reason],
        }

    objective, capacity, ids = best
    return {
        **result,
        "decision_readiness": "REVIEW_REQUIRED",
        selected_ids_key: list(ids),
        "selected_capacity": int(round(capacity)),
        "selected_capacity_exact": capacity,
        "expected_registered_loss": objective,
        "registered_min_point_service_ratio": service_ratio,
        "solver_semantics": SOLVER_SEMANTICS,
        "capacity_scale": scale,
        "capacity_state_count": len(states),
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
    }


def optimize_shuttle_plan(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    departure_options: Sequence[Mapping[str, Any]],
    empty_seat_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any = 0.9,
) -> dict[str, Any]:
    result = _base("SHUTTLE_CAPACITY_RECOMMENDATION")
    scenarios = _scenarios(demand_scenarios)
    empty_weight = _number(empty_seat_weight, minimum=0.0)
    shortage = _number(shortage_weight, minimum=0.0)
    service_ratio = _number(min_point_service_ratio, minimum=0.0)
    normalized_options = _normalize_options(departure_options, id_key="departure_id")
    if (
        scenarios is None
        or empty_weight is None
        or shortage is None
        or service_ratio is None
        or service_ratio > 1.0
    ):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_SHUTTLE_POLICY_INPUTS"],
        }
    if normalized_options is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_departure_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_DEPARTURE_OPTIONS"],
        }
    options, scale = normalized_options
    return _optimize_capacity_subset(
        scope="SHUTTLE_CAPACITY_RECOMMENDATION",
        scenarios=scenarios,
        options=options,
        scale=scale,
        idle_weight=empty_weight,
        shortage_weight=shortage,
        service_ratio=service_ratio,
        selected_ids_key="selected_departure_ids",
        full_capacity_reason="FLEET_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR",
        no_bundle_reason="NO_SHUTTLE_BUNDLE_MEETS_SERVICE_FLOOR",
        state_limit_reason="SHUTTLE_CAPACITY_DP_STATE_LIMIT_EXCEEDED",
    )


def optimize_space_plan(
    *,
    occupancy_scenarios: Sequence[Mapping[str, Any]],
    zones: Sequence[Mapping[str, Any]],
    idle_capacity_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any = 0.9,
) -> dict[str, Any]:
    result = {
        **_base("SPACE_ACTIVATION_RECOMMENDATION"),
        "energy_savings_claim_allowed": False,
    }
    scenarios = _scenarios(occupancy_scenarios)
    idle_weight = _number(idle_capacity_weight, minimum=0.0)
    shortage = _number(shortage_weight, minimum=0.0)
    service_ratio = _number(min_point_service_ratio, minimum=0.0)
    normalized_options = _normalize_options(zones, id_key="zone_id")
    if (
        scenarios is None
        or idle_weight is None
        or shortage is None
        or service_ratio is None
        or service_ratio > 1.0
    ):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_zone_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_SPACE_POLICY_INPUTS"],
        }
    if normalized_options is None:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "selected_zone_ids": [],
            "selected_capacity": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_SPACE_OPTIONS"],
        }
    options, scale = normalized_options
    return _optimize_capacity_subset(
        scope="SPACE_ACTIVATION_RECOMMENDATION",
        scenarios=scenarios,
        options=options,
        scale=scale,
        idle_weight=idle_weight,
        shortage_weight=shortage,
        service_ratio=service_ratio,
        selected_ids_key="selected_zone_ids",
        full_capacity_reason="SPACE_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR",
        no_bundle_reason="NO_SPACE_BUNDLE_MEETS_SERVICE_FLOOR",
        state_limit_reason="SPACE_CAPACITY_DP_STATE_LIMIT_EXCEEDED",
        extra_fields={"energy_savings_claim_allowed": False},
    )
