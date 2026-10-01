"""Scalable, fail-closed food production optimization for CS1.

The objective uses caller-registered relative waste/shortage sensitivity weights.
Those weights are not observed economics. The optimizer computes an exact integer
minimum for the piecewise-linear scenario loss by evaluating only loss breakpoints,
so runtime depends on scenario count rather than kitchen capacity.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

POLICY_VERSION = "food-production-optimizer-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"
OPTIMIZATION_SEMANTICS = "EXACT_INTEGER_BREAKPOINT_SEARCH_PIECEWISE_LINEAR_LOSS"
METHOD_ELIGIBILITY_STATES = {
    "SANDBOX_ONLY",
    "EVALUATED_OFFLINE",
    "PILOT_ELIGIBLE",
    "PILOT_EVALUATED",
    "RETIRED",
}
ACTIONABLE_METHOD_STATES = {"PILOT_ELIGIBLE", "PILOT_EVALUATED"}


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


def _normalize_scenarios(
    rows: Sequence[Mapping[str, Any]] | None,
) -> list[tuple[float, float]] | None:
    normalized: list[tuple[float, float]] = []
    if isinstance(rows, (str, bytes)):
        return None
    for row in rows or ():
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


def _candidate_quantities(
    scenarios: Sequence[tuple[float, float]],
    max_units: int,
) -> list[int]:
    candidates = {0, max_units}
    for demand, _probability in scenarios:
        floor_value = math.floor(demand)
        ceil_value = math.ceil(demand)
        candidates.add(min(max(floor_value, 0), max_units))
        candidates.add(min(max(ceil_value, 0), max_units))
    return sorted(candidates)


def optimize_food_production(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    max_capacity: Any,
    waste_weight: Any,
    shortage_weight: Any,
    method_eligibility: str = "SANDBOX_ONLY",
) -> dict[str, Any]:
    """Return an advisory production candidate and, when eligible, recommendation.

    The expected registered loss is convex and piecewise linear in production
    quantity. Therefore an exact integer optimum must occur at a capacity bound or
    immediately around a demand breakpoint. Enumerating those points avoids an
    O(max_capacity * scenario_count) brute-force scan.
    """

    base = {
        "policy_version": POLICY_VERSION,
        "scope": "FOOD_PRODUCTION_RECOMMENDATION",
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "optimization_semantics": OPTIMIZATION_SEMANTICS,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }
    scenarios = _normalize_scenarios(demand_scenarios)
    capacity = _number(max_capacity, minimum=0.0)
    waste = _number(waste_weight, minimum=0.0)
    shortage = _number(shortage_weight, minimum=0.0)
    if (
        scenarios is None
        or capacity is None
        or waste is None
        or shortage is None
        or waste + shortage <= 0
    ):
        return {
            **base,
            "decision_readiness": "WITHHOLD",
            "candidate_production": None,
            "recommended_production": None,
            "reason_codes": ["INVALID_OR_UNUSABLE_FOOD_POLICY_INPUTS"],
        }

    max_units = int(math.floor(capacity))
    candidates = _candidate_quantities(scenarios, max_units)

    def loss(quantity: int) -> float:
        return sum(
            probability
            * (
                waste * max(quantity - demand, 0.0)
                + shortage * max(demand - quantity, 0.0)
            )
            for demand, probability in scenarios
        )

    objective, quantity = min(
        ((loss(quantity), quantity) for quantity in candidates),
        key=lambda pair: (pair[0], pair[1]),
    )

    eligibility = str(method_eligibility or "SANDBOX_ONLY").strip().upper()
    if eligibility not in METHOD_ELIGIBILITY_STATES:
        readiness = "WITHHOLD"
        recommendation = None
        reasons = ["UNKNOWN_METHOD_ELIGIBILITY"]
    elif eligibility not in ACTIONABLE_METHOD_STATES:
        readiness = "WITHHOLD"
        recommendation = None
        reasons = ["METHOD_NOT_PILOT_ELIGIBLE"]
    else:
        readiness = "REVIEW_REQUIRED"
        recommendation = quantity
        reasons = ["OPERATOR_REVIEW_REQUIRED"]

    return {
        **base,
        "decision_readiness": readiness,
        "method_eligibility": eligibility,
        "candidate_production": quantity,
        "recommended_production": recommendation,
        "max_capacity": max_units,
        "expected_registered_loss": objective,
        "scenario_count": len(scenarios),
        "search_candidate_count": len(candidates),
        "reason_codes": reasons,
    }
