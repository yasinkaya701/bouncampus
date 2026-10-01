from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

PARAMETER_PROVENANCE = "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"
SCOPE = "POLICY_SENSITIVITY_ONLY"
LIMITATIONS = (
    "NO_OBSERVED_ECONOMIC_WEIGHTS",
    "NO_OPERATIONAL_TARGET_SELECTED",
    "NO_IMPACT_CLAIM",
)


def _finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _withhold(*, policy_version: str, reason: str) -> dict[str, Any]:
    return {
        "scope": SCOPE,
        "policy_version": str(policy_version).strip(),
        "parameter_provenance": PARAMETER_PROVENANCE,
        "reference_target": None,
        "scenario_count": 0,
        "scenarios": [],
        "min_target": None,
        "max_target": None,
        "target_span": None,
        "relative_target_span_pct": None,
        "registered_max_relative_target_span_pct": None,
        "sensitivity_state": "WITHHOLD",
        "readiness_effect": "WITHHOLD",
        "selected_operational_target": None,
        "reason_codes": [reason],
        "limitations": list(LIMITATIONS),
    }


def assess_policy_sensitivity(
    reference_target: Any,
    scenarios: Sequence[Mapping[str, Any]],
    *,
    max_relative_target_span_pct: Any,
    policy_version: str,
) -> dict[str, Any]:
    reference = _finite_number(reference_target)
    threshold = _finite_number(max_relative_target_span_pct)
    normalized_policy_version = str(policy_version).strip()

    if reference is None or reference <= 0:
        return _withhold(
            policy_version=normalized_policy_version,
            reason="INVALID_POLICY_SENSITIVITY_REFERENCE_TARGET",
        )
    if threshold is None or threshold < 0:
        return _withhold(
            policy_version=normalized_policy_version,
            reason="INVALID_POLICY_SENSITIVITY_THRESHOLD",
        )
    if not normalized_policy_version:
        return _withhold(
            policy_version="",
            reason="MISSING_POLICY_VERSION",
        )
    if len(scenarios) < 2:
        return _withhold(
            policy_version=normalized_policy_version,
            reason="INSUFFICIENT_POLICY_SENSITIVITY_SCENARIOS",
        )

    normalized = []
    seen_ids: set[str] = set()
    for scenario in scenarios:
        target = _finite_number(scenario.get("target"))
        shortage_weight = _finite_number(scenario.get("shortage_weight"))
        excess_weight = _finite_number(scenario.get("excess_weight"))
        buffer_pct = _finite_number(scenario.get("buffer_pct"))
        scenario_id = str(scenario.get("scenario_id") or "").strip()
        invalid = (
            not scenario_id
            or scenario_id in seen_ids
            or target is None
            or target <= 0
            or shortage_weight is None
            or shortage_weight < 0
            or excess_weight is None
            or excess_weight < 0
            or buffer_pct is None
        )
        if invalid:
            return _withhold(
                policy_version=normalized_policy_version,
                reason="INVALID_POLICY_SENSITIVITY_SCENARIO",
            )
        seen_ids.add(scenario_id)
        normalized.append(
            {
                "scenario_id": scenario_id,
                "target": target,
                "shortage_weight": shortage_weight,
                "excess_weight": excess_weight,
                "buffer_pct": buffer_pct,
                "relative_delta_pct": ((target - reference) / reference) * 100.0,
            }
        )

    targets = [row["target"] for row in normalized]
    minimum = min(targets)
    maximum = max(targets)
    relative_span = ((maximum - minimum) / reference) * 100.0
    high = relative_span > threshold

    return {
        "scope": SCOPE,
        "policy_version": normalized_policy_version,
        "parameter_provenance": PARAMETER_PROVENANCE,
        "reference_target": reference,
        "scenario_count": len(normalized),
        "scenarios": normalized,
        "min_target": minimum,
        "max_target": maximum,
        "target_span": maximum - minimum,
        "relative_target_span_pct": relative_span,
        "registered_max_relative_target_span_pct": threshold,
        "sensitivity_state": "HIGH" if high else "STABLE",
        "readiness_effect": "REVIEW_REQUIRED" if high else "NO_DOWNGRADE",
        "selected_operational_target": None,
        "reason_codes": ["POLICY_SENSITIVITY_HIGH" if high else "POLICY_SENSITIVITY_STABLE"],
        "limitations": list(LIMITATIONS),
    }
