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
    "NO_LIVE_BMS_CLAIM",
    "NO_AUTOMATIC_HVAC_OR_LIGHTING_ACTUATION",
    "OCCUPANCY_BASED_POLICY_HEURISTIC",
    "NO_CALIBRATED_ENERGY_MODEL",
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


def _withhold(reason: str) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "zones": [],
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def plan_building_energy(
    *,
    zones: Sequence[Mapping[str, Any]],
    low_utilization_threshold: Any,
    medium_utilization_threshold: Any,
    upstream_readiness: str = "REVIEW_REQUIRED",
) -> dict[str, Any]:
    """Recommend zone operating modes from aggregate occupancy context.

    Thresholds are explicit caller-registered policy inputs. Recommendations are
    operator-review labels only; this module never estimates achieved kWh/cost/carbon
    savings and never authorizes direct BMS actuation.
    """

    CONTRACT.validate_no_person_level_data(zones, path="zones")

    upstream = str(upstream_readiness or "").strip().upper()
    if upstream not in CONTRACT.READINESS_STATES:
        return _withhold("INVALID_UPSTREAM_READINESS")
    if upstream == "WITHHOLD":
        return _withhold("UPSTREAM_CAMPUS_STATE_WITHHELD")

    low = _finite_nonnegative(low_utilization_threshold)
    medium = _finite_nonnegative(medium_utilization_threshold)
    if low is None or medium is None or low > 1.0 or medium > 1.0 or low >= medium:
        return _withhold("INVALID_UTILIZATION_THRESHOLDS")

    if not isinstance(zones, Sequence) or isinstance(zones, (str, bytes, bytearray)) or not zones:
        return _withhold("NO_ENERGY_ZONES_SUPPLIED")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in zones:
        if not isinstance(raw, Mapping):
            return _withhold("INVALID_ENERGY_ZONE")
        zone_id = str(raw.get("zone_id", "")).strip()
        capacity = _finite_nonnegative(raw.get("capacity"))
        occupancy = _finite_nonnegative(raw.get("occupancy_estimate"))
        if not zone_id or zone_id in seen or capacity is None or capacity <= 0 or occupancy is None:
            return _withhold("INVALID_ENERGY_ZONE")
        if occupancy > capacity:
            return _withhold("OCCUPANCY_EXCEEDS_ZONE_CAPACITY")
        seen.add(zone_id)
        utilization = occupancy / capacity
        if utilization <= low:
            mode = "SETBACK_REVIEW"
        elif utilization <= medium:
            mode = "PARTIAL_LOAD_REVIEW"
        else:
            mode = "NORMAL_SERVICE_REVIEW"
        normalized.append(
            {
                "zone_id": zone_id,
                "capacity": int(round(capacity)),
                "occupancy_estimate": int(round(occupancy)),
                "utilization_ratio": round(utilization, 4),
                "recommended_mode": mode,
                "recommendation_semantics": "OPERATOR_REVIEW_NOT_BMS_COMMAND",
            }
        )

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "registered_thresholds": {
            "low_utilization": low,
            "medium_utilization": medium,
        },
        "zones": normalized,
        "reason_codes": ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
