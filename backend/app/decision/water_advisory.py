"""Aggregate, fail-closed campus water-use advisory planning for CS1."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

POLICY_VERSION = "water-advisory-v1.0"
LIMITATIONS = (
    "NO_LIVE_WATER_METER_OR_VALVE_CLAIM",
    "EXPECTED_USAGE_INPUT_REQUIRES_EXTERNAL_PROVENANCE",
    "NO_AUTOMATIC_VALVE_ACTUATION",
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
        "scope": "WATER_USE_ADVISORY",
        "decision_readiness": "WITHHOLD",
        "zones": [],
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "automatic_valve_actuation": False,
        "water_savings_claim_allowed": False,
        "impact_claim_allowed": False,
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def plan_water_advisory(
    *,
    zones: Sequence[Mapping[str, Any]],
    elevated_ratio_threshold: Any,
    critical_ratio_threshold: Any,
) -> dict[str, Any]:
    """Classify aggregate water-use deviation for operator investigation.

    `expected_liters` and `observed_liters` are caller-supplied aggregate values.
    This policy does not infer source validity or achieved savings and never issues
    automatic valve/shutoff commands.
    """

    elevated = _number(elevated_ratio_threshold, minimum=1.0)
    critical = _number(critical_ratio_threshold, minimum=1.0)
    if elevated is None or critical is None or elevated >= critical:
        return _withhold("INVALID_WATER_RATIO_THRESHOLDS")
    if not isinstance(zones, Sequence) or isinstance(zones, (str, bytes)) or not zones:
        return _withhold("NO_WATER_ZONES_SUPPLIED")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in zones:
        if not isinstance(raw, Mapping):
            return _withhold("INVALID_WATER_ZONE")
        zone_id = str(raw.get("zone_id") or "").strip()
        expected = _number(raw.get("expected_liters"), minimum=0.0)
        observed = _number(raw.get("observed_liters"), minimum=0.0)
        if (
            not zone_id
            or zone_id in seen
            or expected is None
            or expected <= 0
            or observed is None
        ):
            return _withhold("INVALID_WATER_ZONE")
        seen.add(zone_id)
        ratio = observed / expected
        if ratio >= critical:
            mode = "LEAK_OR_OPERATIONAL_ANOMALY_REVIEW"
        elif ratio >= elevated:
            mode = "ELEVATED_USE_REVIEW"
        else:
            mode = "NORMAL_USE_REVIEW"
        normalized.append(
            {
                "zone_id": zone_id,
                "expected_liters": expected,
                "observed_liters": observed,
                "observed_to_expected_ratio": round(ratio, 4),
                "recommended_mode": mode,
                "recommendation_semantics": "OPERATOR_INVESTIGATION_NOT_VALVE_COMMAND",
            }
        )

    return {
        "policy_version": POLICY_VERSION,
        "scope": "WATER_USE_ADVISORY",
        "decision_readiness": "REVIEW_REQUIRED",
        "registered_thresholds": {
            "elevated_ratio": elevated,
            "critical_ratio": critical,
        },
        "zones": normalized,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "automatic_valve_actuation": False,
        "water_savings_claim_allowed": False,
        "impact_claim_allowed": False,
        "reason_codes": ["OPERATOR_REVIEW_REQUIRED"],
        "limitations": list(LIMITATIONS),
    }
