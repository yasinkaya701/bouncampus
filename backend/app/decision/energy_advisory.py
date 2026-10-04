"""Aggregate, operator-reviewed building-energy advisory planning for CS1."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

POLICY_VERSION = "energy-advisory-v1.0"
LIMITATIONS = (
    "NO_LIVE_BMS_OR_SMART_METER_CLAIM",
    "NO_CALIBRATED_ENERGY_MODEL",
    "OCCUPANCY_BASED_POLICY_HEURISTIC",
    "NO_AUTOMATIC_HVAC_OR_LIGHTING_ACTUATION",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


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


def _withhold(reason: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": "BUILDING_ENERGY_ADVISORY",
        "decision_readiness": "WITHHOLD",
        "zones": [],
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "energy_savings_claim_allowed": False,
        "impact_claim_allowed": False,
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def plan_energy_advisory(
    *,
    zones: Sequence[Mapping[str, Any]],
    low_utilization_threshold: Any,
    medium_utilization_threshold: Any,
) -> dict[str, Any]:
    """Return zone operating-mode reviews from aggregate occupancy ratios.

    Thresholds are caller-registered policy values, not learned savings coefficients.
    Modes are review labels only and never direct BMS commands.
    """

    low = _number(low_utilization_threshold, minimum=0.0)
    medium = _number(medium_utilization_threshold, minimum=0.0)
    if low is None or medium is None or low > 1.0 or medium > 1.0 or low >= medium:
        return _withhold("INVALID_UTILIZATION_THRESHOLDS")
    if not isinstance(zones, Sequence) or isinstance(zones, (str, bytes)) or not zones:
        return _withhold("NO_ENERGY_ZONES_SUPPLIED")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in zones:
        if not isinstance(raw, Mapping):
            return _withhold("INVALID_ENERGY_ZONE")
        zone_id = str(raw.get("zone_id") or "").strip()
        capacity = _number(raw.get("capacity"), minimum=0.0)
        occupancy = _number(raw.get("occupancy_estimate"), minimum=0.0)
        if (
            not zone_id
            or zone_id in seen
            or capacity is None
            or capacity <= 0
            or occupancy is None
        ):
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
        "policy_version": POLICY_VERSION,
        "scope": "BUILDING_ENERGY_ADVISORY",
        "decision_readiness": "REVIEW_REQUIRED",
        "registered_thresholds": {
            "low_utilization": low,
            "medium_utilization": medium,
        },
        "zones": normalized,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "energy_savings_claim_allowed": False,
        "impact_claim_allowed": False,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
