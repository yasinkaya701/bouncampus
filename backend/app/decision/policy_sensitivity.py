from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

PARAMETER_PROVENANCE = "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"
SCOPE = "POLICY_SENSITIVITY_ONLY"


def _finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def assess_policy_sensitivity(
    reference_target: Any,
    scenarios: Sequence[Mapping[str, Any]],
    *,
    max_relative_target_span_pct: Any,
    policy_version: str,
) -> dict[str, Any]:
    reference = _finite_number(reference_target)
    threshold = _finite_number(max_relative_target_span_pct)
    if reference is None or reference <= 0:
        raise ValueError("reference_target must be a positive finite number")
    if threshold is None or threshold < 0:
        raise ValueError("max_relative_target_span_pct must be a non-negative finite number")
    if not str(policy_version).strip():
        raise ValueError("policy_version is required")
    if len(scenarios) < 2:
        raise ValueError("at least two policy scenarios are required")

    normalized = []
    for index, scenario in enumerate(scenarios):
        target = _finite_number(scenario.get("target"))
        shortage_weight = _finite_number(scenario.get("shortage_weight"))
        excess_weight = _finite_number(scenario.get("excess_weight"))
        buffer_pct = _finite_number(scenario.get("buffer_pct"))
        scenario_id = str(scenario.get("scenario_id") or "").strip()
        if not scenario_id:
            raise ValueError(f"scenario {index} requires scenario_id")
        if target is None or target <= 0:
            raise ValueError(f"scenario {scenario_id} target must be positive and finite")
        if shortage_weight is None or shortage_weight < 0:
            raise ValueError(f"scenario {scenario_id} shortage_weight must be non-negative and finite")
        if excess_weight is None or excess_weight < 0:
            raise ValueError(f"scenario {scenario_id} excess_weight must be non-negative and finite")
        if buffer_pct is None:
            raise ValueError(f"scenario {scenario_id} buffer_pct must be finite")
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
        "policy_version": str(policy_version).strip(),
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
        "limitations": [
            "NO_OBSERVED_ECONOMIC_WEIGHTS",
            "NO_OPERATIONAL_TARGET_SELECTED",
            "NO_IMPACT_CLAIM",
        ],
    }
