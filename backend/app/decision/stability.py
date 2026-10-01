"""Fail-closed stability diagnostics for CS1 decision intelligence."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

STAGE_ELIGIBILITY = {
    "OFFLINE_EVALUATION": frozenset(
        {"EVALUATED_OFFLINE", "PILOT_ELIGIBLE", "PILOT_EVALUATED"}
    ),
    "PILOT": frozenset({"PILOT_ELIGIBLE", "PILOT_EVALUATED"}),
}


def _finite_nonnegative(value):
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _validate_pct(value: float, *, name: str) -> float:
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return numeric


def _validate_floor(value: float) -> float:
    numeric = float(value)
    if not math.isfinite(numeric) or numeric <= 0:
        raise ValueError("denominator_floor must be finite and > 0")
    return numeric


def assess_method_disagreement(
    method_estimates: Mapping[str, object],
    *,
    selected_method_id: str,
    method_eligibility: Mapping[str, str],
    stage: str,
    max_relative_disagreement_pct: float,
    denominator_floor: float = 1.0,
) -> dict[str, object]:
    """Expose eligible-method disagreement without turning it into readiness proof.

    The threshold is an explicit registered policy input. Ineligible methods are
    reported but cannot trigger review for the requested stage.
    """

    if stage not in STAGE_ELIGIBILITY:
        raise ValueError(f"unsupported selection stage {stage!r}")
    gate = _validate_pct(
        max_relative_disagreement_pct,
        name="max_relative_disagreement_pct",
    )
    floor = _validate_floor(denominator_floor)
    allowed_states = STAGE_ELIGIBILITY[stage]

    selected_state = method_eligibility.get(selected_method_id, "SANDBOX_ONLY")
    selected_estimate = _finite_nonnegative(method_estimates.get(selected_method_id))
    if selected_state not in allowed_states:
        return {
            "assessment_status": "WITHHOLD",
            "selected_method_id": selected_method_id,
            "selected_estimate": selected_estimate,
            "max_relative_disagreement_pct": None,
            "max_allowed_relative_disagreement_pct": gate,
            "method_assessments": {},
            "reason_codes": ["SELECTED_METHOD_NOT_ELIGIBLE_FOR_STAGE"],
            "stage": stage,
            "result_scope": "METHOD_DISAGREEMENT_GATE_ONLY",
            "claim_boundary": (
                "Disagreement diagnostics do not establish operational readiness or achieved impact."
            ),
        }
    if selected_estimate is None:
        return {
            "assessment_status": "WITHHOLD",
            "selected_method_id": selected_method_id,
            "selected_estimate": None,
            "max_relative_disagreement_pct": None,
            "max_allowed_relative_disagreement_pct": gate,
            "method_assessments": {},
            "reason_codes": ["SELECTED_METHOD_ESTIMATE_UNAVAILABLE"],
            "stage": stage,
            "result_scope": "METHOD_DISAGREEMENT_GATE_ONLY",
            "claim_boundary": (
                "Disagreement diagnostics do not establish operational readiness or achieved impact."
            ),
        }

    denominator = max(abs(selected_estimate), floor)
    assessments: dict[str, dict[str, object]] = {}
    comparable_disagreements: list[float] = []

    for method_id, raw_estimate in method_estimates.items():
        eligibility = method_eligibility.get(method_id, "SANDBOX_ONLY")
        eligible_for_stage = eligibility in allowed_states
        estimate = _finite_nonnegative(raw_estimate)
        reasons: list[str] = []
        relative_disagreement = None

        if not eligible_for_stage:
            reasons.append("METHOD_NOT_ELIGIBLE_FOR_STAGE")
        if estimate is None:
            reasons.append("ESTIMATE_UNAVAILABLE")
        if method_id == selected_method_id and estimate is not None:
            relative_disagreement = 0.0
        elif eligible_for_stage and estimate is not None:
            relative_disagreement = (
                abs(estimate - selected_estimate) / denominator
            ) * 100.0
            comparable_disagreements.append(relative_disagreement)

        assessments[method_id] = {
            "eligibility": eligibility,
            "eligible_for_stage": eligible_for_stage,
            "estimate": estimate,
            "relative_disagreement_pct_vs_selected": relative_disagreement,
            "reason_codes": reasons,
        }

    if not comparable_disagreements:
        status = "NOT_ASSESSABLE"
        maximum = None
        reason_codes = ["NO_COMPARABLE_ELIGIBLE_ESTIMATE"]
    else:
        maximum = max(comparable_disagreements)
        if maximum > gate:
            status = "REVIEW_REQUIRED"
            reason_codes = ["ELIGIBLE_METHOD_DISAGREEMENT_EXCEEDS_GATE"]
        else:
            status = "STABLE"
            reason_codes = ["ELIGIBLE_METHOD_DISAGREEMENT_WITHIN_GATE"]

    return {
        "assessment_status": status,
        "selected_method_id": selected_method_id,
        "selected_estimate": selected_estimate,
        "max_relative_disagreement_pct": maximum,
        "max_allowed_relative_disagreement_pct": gate,
        "method_assessments": assessments,
        "reason_codes": reason_codes,
        "stage": stage,
        "result_scope": "METHOD_DISAGREEMENT_GATE_ONLY",
        "claim_boundary": (
            "Disagreement diagnostics do not establish operational readiness or achieved impact."
        ),
    }


def assess_policy_sensitivity(
    scenario_targets: Mapping[str, object],
    *,
    reference_policy_id: str,
    max_relative_target_change_pct: float,
    required_scenario_ids: Sequence[str] | None = None,
    denominator_floor: float = 1.0,
) -> dict[str, object]:
    """Gate target instability across caller-defined policy sensitivity scenarios.

    Scenario definitions and thresholds must be registered by the caller. This
    function does not infer economic weights or claim that the scenarios are learned.
    """

    gate = _validate_pct(
        max_relative_target_change_pct,
        name="max_relative_target_change_pct",
    )
    floor = _validate_floor(denominator_floor)
    reference_target = _finite_nonnegative(scenario_targets.get(reference_policy_id))

    if reference_target is None:
        return {
            "assessment_status": "WITHHOLD",
            "reference_policy_id": reference_policy_id,
            "reference_target": None,
            "max_relative_target_change_pct": None,
            "max_allowed_relative_target_change_pct": gate,
            "scenario_assessments": {},
            "reason_codes": ["REFERENCE_POLICY_TARGET_UNAVAILABLE"],
            "result_scope": "POLICY_SENSITIVITY_GATE_ONLY",
            "policy_weight_semantics": "REGISTERED_SCENARIO_INPUTS_NOT_LEARNED_ECONOMICS",
            "claim_boundary": (
                "Policy sensitivity is a stability diagnostic, not evidence of economic value or achieved impact."
            ),
        }

    required = tuple(required_scenario_ids or ())
    missing_required = [
        scenario_id
        for scenario_id in required
        if _finite_nonnegative(scenario_targets.get(scenario_id)) is None
    ]
    if missing_required:
        return {
            "assessment_status": "WITHHOLD",
            "reference_policy_id": reference_policy_id,
            "reference_target": reference_target,
            "max_relative_target_change_pct": None,
            "max_allowed_relative_target_change_pct": gate,
            "scenario_assessments": {},
            "missing_required_scenario_ids": missing_required,
            "reason_codes": ["REQUIRED_SENSITIVITY_SCENARIO_UNAVAILABLE"],
            "result_scope": "POLICY_SENSITIVITY_GATE_ONLY",
            "policy_weight_semantics": "REGISTERED_SCENARIO_INPUTS_NOT_LEARNED_ECONOMICS",
            "claim_boundary": (
                "Policy sensitivity is a stability diagnostic, not evidence of economic value or achieved impact."
            ),
        }

    denominator = max(abs(reference_target), floor)
    assessments: dict[str, dict[str, object]] = {}
    relative_changes: list[float] = []

    for scenario_id, raw_target in scenario_targets.items():
        target = _finite_nonnegative(raw_target)
        reasons: list[str] = []
        relative_change = None
        if target is None:
            reasons.append("SCENARIO_TARGET_UNAVAILABLE")
        elif scenario_id == reference_policy_id:
            relative_change = 0.0
        else:
            relative_change = abs(target - reference_target) / denominator * 100.0
            relative_changes.append(relative_change)

        assessments[scenario_id] = {
            "target": target,
            "relative_target_change_pct_vs_reference": relative_change,
            "reason_codes": reasons,
        }

    if not relative_changes:
        status = "WITHHOLD"
        maximum = None
        reason_codes = ["NO_VALID_SENSITIVITY_SCENARIO"]
    else:
        maximum = max(relative_changes)
        if maximum > gate:
            status = "REVIEW_REQUIRED"
            reason_codes = ["POLICY_SENSITIVITY_EXCEEDS_GATE"]
        else:
            status = "STABLE"
            reason_codes = ["POLICY_SENSITIVITY_WITHIN_GATE"]

    return {
        "assessment_status": status,
        "reference_policy_id": reference_policy_id,
        "reference_target": reference_target,
        "max_relative_target_change_pct": maximum,
        "max_allowed_relative_target_change_pct": gate,
        "scenario_assessments": assessments,
        "reason_codes": reason_codes,
        "result_scope": "POLICY_SENSITIVITY_GATE_ONLY",
        "policy_weight_semantics": "REGISTERED_SCENARIO_INPUTS_NOT_LEARNED_ECONOMICS",
        "claim_boundary": (
            "Policy sensitivity is a stability diagnostic, not evidence of economic value or achieved impact."
        ),
    }
