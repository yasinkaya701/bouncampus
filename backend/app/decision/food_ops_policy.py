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
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
ACTIONABLE_METHOD_STATES = frozenset({"PILOT_ELIGIBLE", "PILOT_EVALUATED"})

LIMITATIONS = (
    "NO_LIVE_CAFETERIA_POS_CLAIM",
    "NO_UNVERIFIED_KITCHEN_CAPACITY_CLAIM",
    "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND",
    "REGISTERED_WEIGHTS_NOT_OBSERVED_ECONOMICS",
    "NO_AUTOMATIC_KITCHEN_DISPATCH",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _finite_nonnegative(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _normalize_scenarios(
    demand_scenarios: Sequence[Mapping[str, Any]],
) -> list[tuple[float, float]] | None:
    if not isinstance(demand_scenarios, Sequence) or isinstance(
        demand_scenarios, (str, bytes, bytearray)
    ):
        return None

    rows: list[tuple[float, float]] = []
    for raw in demand_scenarios:
        if not isinstance(raw, Mapping):
            return None
        demand = _finite_nonnegative(raw.get("demand"))
        weight = _finite_nonnegative(raw.get("weight"))
        if demand is None or weight is None:
            return None
        rows.append((demand, weight))

    total_weight = sum(weight for _, weight in rows)
    if not rows or total_weight <= 0:
        return None
    return [(demand, weight / total_weight) for demand, weight in rows]


def _withhold(reason: str, *, capacity_provenance: str) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "recommended_production": None,
        "capacity_provenance": capacity_provenance,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS",
        "reservation_semantics": "INTENT_SIGNAL_NOT_SERVED_DEMAND",
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def plan_food_production(
    *,
    demand_scenarios: Sequence[Mapping[str, Any]],
    max_capacity: Any,
    capacity_provenance: str = "UNAVAILABLE",
    waste_weight: Any,
    shortage_weight: Any,
    method_eligibility: str,
    upstream_readiness: str = "REVIEW_REQUIRED",
) -> dict[str, Any]:
    """Choose an operator-reviewed food production target under registered loss.

    Scenario probabilities/weights and surplus/shortage weights are explicit policy
    inputs. They are not learned economic costs. Reservation-derived scenarios may
    be supplied, but reservation remains an intent signal rather than served demand.
    Production-capacity-sensitive output requires verified operational provenance.
    """

    CONTRACT.validate_no_person_level_data(demand_scenarios, path="demand_scenarios")
    normalized_capacity_provenance = CONTRACT.normalize_provenance(
        capacity_provenance, field="capacity_provenance"
    )

    upstream = str(upstream_readiness or "").strip().upper()
    if upstream not in CONTRACT.READINESS_STATES:
        return _withhold(
            "INVALID_UPSTREAM_READINESS",
            capacity_provenance=normalized_capacity_provenance,
        )
    if upstream == "WITHHOLD":
        return _withhold(
            "UPSTREAM_CAMPUS_STATE_WITHHELD",
            capacity_provenance=normalized_capacity_provenance,
        )

    scenarios = _normalize_scenarios(demand_scenarios)
    if scenarios is None:
        return _withhold(
            "INVALID_OR_UNUSABLE_DEMAND_SCENARIOS",
            capacity_provenance=normalized_capacity_provenance,
        )

    capacity = _finite_nonnegative(max_capacity)
    waste = _finite_nonnegative(waste_weight)
    shortage = _finite_nonnegative(shortage_weight)
    if capacity is None or waste is None or shortage is None:
        return _withhold(
            "INVALID_FOOD_POLICY_INPUTS",
            capacity_provenance=normalized_capacity_provenance,
        )
    if normalized_capacity_provenance not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        return _withhold(
            "UNVERIFIED_FOOD_CAPACITY",
            capacity_provenance=normalized_capacity_provenance,
        )
    if waste + shortage <= 0:
        return _withhold(
            "NON_IDENTIFYING_FOOD_OBJECTIVE",
            capacity_provenance=normalized_capacity_provenance,
        )

    max_units = int(math.floor(capacity))

    eligibility = str(method_eligibility or "").strip().upper()
    if eligibility not in ACTIONABLE_METHOD_STATES:
        return _withhold(
            "METHOD_NOT_ACTIONABLE",
            capacity_provenance=normalized_capacity_provenance,
        )

    def expected_loss(quantity: int) -> float:
        return sum(
            weight
            * (
                waste * max(quantity - demand, 0.0)
                + shortage * max(demand - quantity, 0.0)
            )
            for demand, weight in scenarios
        )

    scored = [(expected_loss(quantity), quantity) for quantity in range(max_units + 1)]
    objective, target = min(scored, key=lambda item: (item[0], item[1]))

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "recommended_production": target,
        "max_capacity": max_units,
        "capacity_provenance": normalized_capacity_provenance,
        "scenario_count": len(scenarios),
        "expected_registered_loss": objective,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS",
        "reservation_semantics": "INTENT_SIGNAL_NOT_SERVED_DEMAND",
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "reason_codes": ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
