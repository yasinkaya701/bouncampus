"""Executable, human-gated orchestration for CS1 decision evidence."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Mapping, Sequence


def _load_sibling(module_name: str):
    path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(f"cs1_{module_name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_method_selection = _load_sibling("method_selection")
_stability = _load_sibling("stability")


def _not_run(scope: str) -> dict[str, object]:
    return {
        "assessment_status": "NOT_RUN",
        "result_scope": scope,
        "reason_codes": [],
    }


def _result(
    *,
    decision_status: str,
    selected_method: str | None,
    selection: Mapping[str, object],
    method_stability: Mapping[str, object],
    policy_sensitivity: Mapping[str, object],
    reason_codes: Sequence[str],
) -> dict[str, object]:
    return {
        "decision_status": decision_status,
        "selected_method": selected_method,
        "human_gate_required": True,
        "automatic_dispatch_allowed": False,
        "selection": dict(selection),
        "method_stability": dict(method_stability),
        "policy_sensitivity": dict(policy_sensitivity),
        "reason_codes": list(reason_codes),
        "result_scope": "CS1_HUMAN_GATED_DECISION_EVIDENCE_ONLY",
        "claim_boundary": (
            "This result can nominate an advisory candidate for human review, but it does not establish PILOT_READY, authorize automatic dispatch, or prove achieved impact."
        ),
    }


def run_decision_gate(
    comparison: Mapping[str, object],
    *,
    baseline_id: str,
    method_eligibility: Mapping[str, str],
    stage: str,
    primary_metric: str,
    min_common_support_n: int,
    min_relative_improvement_pct: float,
    method_estimates: Mapping[str, object],
    max_relative_disagreement_pct: float,
    policy_scenario_targets: Mapping[str, object] | None = None,
    reference_policy_id: str | None = None,
    max_relative_target_change_pct: float | None = None,
    required_scenario_ids: Sequence[str] | None = None,
) -> dict[str, object]:
    """Run baseline selection and stability checks before human advisory use.

    The input ``comparison`` intentionally matches the common-support ``metrics`` /
    ``common_support_n`` shape emitted by the CS1 benchmark work. All thresholds
    remain caller-registered policy inputs. This function composes evidence; it
    does not create economic semantics or operational authority.
    """

    selection = _method_selection.select_method(
        comparison,
        baseline_id=baseline_id,
        method_eligibility=method_eligibility,
        stage=stage,
        primary_metric=primary_metric,
        min_common_support_n=min_common_support_n,
        min_relative_improvement_pct=min_relative_improvement_pct,
    )
    method_stability = _not_run("METHOD_DISAGREEMENT_GATE_ONLY")
    policy_sensitivity = _not_run("POLICY_SENSITIVITY_GATE_ONLY")

    if selection.get("selection_status") != "SELECTED":
        return _result(
            decision_status="WITHHOLD",
            selected_method=None,
            selection=selection,
            method_stability=method_stability,
            policy_sensitivity=policy_sensitivity,
            reason_codes=["SELECTION_WITHHELD"],
        )

    selected_method = selection.get("selected_method")
    if not isinstance(selected_method, str) or not selected_method:
        return _result(
            decision_status="WITHHOLD",
            selected_method=None,
            selection=selection,
            method_stability=method_stability,
            policy_sensitivity=policy_sensitivity,
            reason_codes=["SELECTED_METHOD_UNAVAILABLE"],
        )

    method_stability = _stability.assess_method_disagreement(
        method_estimates,
        selected_method_id=selected_method,
        method_eligibility=method_eligibility,
        stage=stage,
        max_relative_disagreement_pct=max_relative_disagreement_pct,
    )
    method_status = method_stability.get("assessment_status")
    if method_status in {"WITHHOLD", "NOT_ASSESSABLE"}:
        return _result(
            decision_status="WITHHOLD",
            selected_method=selected_method,
            selection=selection,
            method_stability=method_stability,
            policy_sensitivity=policy_sensitivity,
            reason_codes=["METHOD_STABILITY_NOT_DEFENSIBLE"],
        )
    if method_status == "REVIEW_REQUIRED":
        return _result(
            decision_status="REVIEW_REQUIRED",
            selected_method=selected_method,
            selection=selection,
            method_stability=method_stability,
            policy_sensitivity=policy_sensitivity,
            reason_codes=["METHOD_DISAGREEMENT_REQUIRES_REVIEW"],
        )
    if method_status != "STABLE":
        return _result(
            decision_status="WITHHOLD",
            selected_method=selected_method,
            selection=selection,
            method_stability=method_stability,
            policy_sensitivity=policy_sensitivity,
            reason_codes=["UNKNOWN_METHOD_STABILITY_STATUS"],
        )

    if policy_scenario_targets is not None:
        if reference_policy_id is None or max_relative_target_change_pct is None:
            return _result(
                decision_status="WITHHOLD",
                selected_method=selected_method,
                selection=selection,
                method_stability=method_stability,
                policy_sensitivity=policy_sensitivity,
                reason_codes=["POLICY_SENSITIVITY_CONFIGURATION_INCOMPLETE"],
            )
        policy_sensitivity = _stability.assess_policy_sensitivity(
            policy_scenario_targets,
            reference_policy_id=reference_policy_id,
            max_relative_target_change_pct=max_relative_target_change_pct,
            required_scenario_ids=required_scenario_ids,
        )
        policy_status = policy_sensitivity.get("assessment_status")
        if policy_status == "WITHHOLD":
            return _result(
                decision_status="WITHHOLD",
                selected_method=selected_method,
                selection=selection,
                method_stability=method_stability,
                policy_sensitivity=policy_sensitivity,
                reason_codes=["POLICY_SENSITIVITY_WITHHELD"],
            )
        if policy_status == "REVIEW_REQUIRED":
            return _result(
                decision_status="REVIEW_REQUIRED",
                selected_method=selected_method,
                selection=selection,
                method_stability=method_stability,
                policy_sensitivity=policy_sensitivity,
                reason_codes=["POLICY_SENSITIVITY_REQUIRES_REVIEW"],
            )
        if policy_status != "STABLE":
            return _result(
                decision_status="WITHHOLD",
                selected_method=selected_method,
                selection=selection,
                method_stability=method_stability,
                policy_sensitivity=policy_sensitivity,
                reason_codes=["UNKNOWN_POLICY_SENSITIVITY_STATUS"],
            )

    return _result(
        decision_status="ADVISORY_CANDIDATE",
        selected_method=selected_method,
        selection=selection,
        method_stability=method_stability,
        policy_sensitivity=policy_sensitivity,
        reason_codes=["EVIDENCE_GATES_CLEARED_FOR_HUMAN_REVIEW"],
    )
