from __future__ import annotations

import importlib.util
import math
from collections.abc import Mapping, Sequence
from itertools import combinations
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
ACTIONABLE_OCCUPANCY_PROVENANCE = frozenset(
    set(CONTRACT.PROVENANCE_STATES)
    - {"UNAVAILABLE", "GENERATED_SANDBOX", "POLICY_HEURISTIC"}
)

LIMITATIONS = (
    "NO_LIVE_BMS_CLAIM",
    "NO_UNVERIFIED_ZONE_CAPACITY_CLAIM",
    "NO_AUTOMATIC_ZONE_OPEN_CLOSE_ACTUATION",
    "REGISTERED_WEIGHTS_NOT_OBSERVED_ECONOMICS",
    "ENERGY_SAVINGS_NOT_INFERRED_FROM_ZONE_SELECTION",
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
    rows: Sequence[Mapping[str, Any]],
) -> list[tuple[float, float]] | None:
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return None
    normalized: list[tuple[float, float]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            return None
        demand = _finite_nonnegative(row.get("demand"))
        weight = _finite_nonnegative(row.get("weight"))
        if demand is None or weight is None:
            return None
        normalized.append((demand, weight))
    total_weight = sum(weight for _, weight in normalized)
    if not normalized or total_weight <= 0:
        return None
    return [(demand, weight / total_weight) for demand, weight in normalized]


def _withhold(
    reason: str,
    *,
    zone_inventory_provenance: str,
    occupancy_provenance: str,
    selected_capacity: int | None = None,
) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "energy_savings_claim_allowed": False,
        "selected_zone_ids": [],
        "selected_capacity": selected_capacity,
        "zone_inventory_provenance": zone_inventory_provenance,
        "occupancy_provenance": occupancy_provenance,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS",
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def plan_space_activation(
    *,
    occupancy_scenarios: Sequence[Mapping[str, Any]],
    zones: Sequence[Mapping[str, Any]],
    idle_capacity_weight: Any,
    shortage_weight: Any,
    min_point_service_ratio: Any = 0.9,
    zone_inventory_provenance: str = "UNAVAILABLE",
    occupancy_provenance: str = "UNAVAILABLE",
    upstream_readiness: str = "REVIEW_REQUIRED",
) -> dict[str, Any]:
    """Choose an operator-reviewed zone bundle under aggregate occupancy uncertainty.

    Capacity-sensitive output requires verified physical zone inventory provenance.
    Occupancy can be an explicit model/scenario/measurement/public source, but
    sandbox, unavailable, or pure policy-heuristic evidence cannot drive an
    operator recommendation. Activation/idle/shortage weights are registered
    relative sensitivities, never kWh, TRY, carbon, or measured savings.
    """

    CONTRACT.validate_no_person_level_data(occupancy_scenarios, path="occupancy_scenarios")
    CONTRACT.validate_no_person_level_data(zones, path="zones")

    upstream = str(upstream_readiness or "").strip().upper()
    if upstream not in CONTRACT.READINESS_STATES:
        raise ValueError(f"unsupported upstream_readiness: {upstream_readiness}")

    zone_provenance = CONTRACT.normalize_provenance(
        zone_inventory_provenance, field="zone_inventory_provenance"
    )
    occupancy_source = CONTRACT.normalize_provenance(
        occupancy_provenance, field="occupancy_provenance"
    )

    if upstream == "WITHHOLD":
        return _withhold(
            "UPSTREAM_CAMPUS_STATE_WITHHELD",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )
    if zone_provenance not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        return _withhold(
            "UNVERIFIED_ZONE_INVENTORY",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )
    if occupancy_source not in ACTIONABLE_OCCUPANCY_PROVENANCE:
        return _withhold(
            "OCCUPANCY_EVIDENCE_NOT_ACTIONABLE",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )

    scenarios = _normalize_scenarios(occupancy_scenarios)
    idle_weight = _finite_nonnegative(idle_capacity_weight)
    shortage = _finite_nonnegative(shortage_weight)
    service_ratio = _finite_nonnegative(min_point_service_ratio)
    if (
        scenarios is None
        or idle_weight is None
        or shortage is None
        or service_ratio is None
        or service_ratio > 1.0
    ):
        return _withhold(
            "INVALID_OR_UNUSABLE_SPACE_POLICY_INPUTS",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )

    if not isinstance(zones, Sequence) or isinstance(zones, (str, bytes, bytearray)):
        return _withhold(
            "INVALID_OR_EXCESSIVE_SPACE_OPTIONS",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )

    normalized_zones: list[tuple[str, int, float]] = []
    seen: set[str] = set()
    for row in zones:
        if not isinstance(row, Mapping):
            normalized_zones = []
            break
        zone_id = str(row.get("zone_id", "")).strip()
        capacity = _finite_nonnegative(row.get("capacity"))
        activation = _finite_nonnegative(row.get("activation_weight", 0.0))
        if (
            not zone_id
            or zone_id in seen
            or capacity is None
            or capacity <= 0
            or not capacity.is_integer()
            or activation is None
        ):
            normalized_zones = []
            break
        seen.add(zone_id)
        normalized_zones.append((zone_id, int(capacity), activation))

    if not normalized_zones or len(normalized_zones) > 18:
        return _withhold(
            "INVALID_OR_EXCESSIVE_SPACE_OPTIONS",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )

    full_capacity = sum(capacity for _, capacity, _ in normalized_zones)
    if any(full_capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
        return _withhold(
            "SPACE_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
            selected_capacity=full_capacity,
        )

    candidates: list[tuple[float, int, tuple[str, ...]]] = []
    for size in range(1, len(normalized_zones) + 1):
        for subset in combinations(normalized_zones, size):
            zone_ids = tuple(sorted(item[0] for item in subset))
            capacity = sum(item[1] for item in subset)
            if any(capacity + 1e-9 < service_ratio * demand for demand, _ in scenarios):
                continue
            activation = sum(item[2] for item in subset)
            expected_loss = activation + sum(
                probability
                * (
                    idle_weight * max(capacity - demand, 0.0)
                    + shortage * max(demand - capacity, 0.0)
                )
                for demand, probability in scenarios
            )
            candidates.append((expected_loss, capacity, zone_ids))

    if not candidates:
        return _withhold(
            "NO_SPACE_BUNDLE_MEETS_SERVICE_FLOOR",
            zone_inventory_provenance=zone_provenance,
            occupancy_provenance=occupancy_source,
        )

    objective, selected_capacity, zone_ids = min(
        candidates, key=lambda item: (item[0], item[1], item[2])
    )
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "energy_savings_claim_allowed": False,
        "selected_zone_ids": list(zone_ids),
        "selected_capacity": selected_capacity,
        "expected_registered_loss": objective,
        "registered_min_point_service_ratio": service_ratio,
        "zone_inventory_provenance": zone_provenance,
        "occupancy_provenance": occupancy_source,
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS",
        "reason_codes": ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
