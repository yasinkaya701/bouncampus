#!/usr/bin/env python3
"""Regression tests for CS1 decision-stability gates."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_stability():
    path = ROOT / "backend/app/decision/stability.py"
    if not path.exists():
        raise AssertionError("decision-stability gate missing")
    spec = importlib.util.spec_from_file_location("cs1_decision_stability", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_method_disagreement_requires_review_past_registered_gate() -> None:
    stability = load_stability()
    result = stability.assess_method_disagreement(
        {"baseline": 100.0, "model": 130.0},
        selected_method_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "PILOT_ELIGIBLE",
        },
        stage="PILOT",
        max_relative_disagreement_pct=10.0,
    )
    assert result["assessment_status"] == "REVIEW_REQUIRED"
    assert result["max_relative_disagreement_pct"] == 30.0
    assert "ELIGIBLE_METHOD_DISAGREEMENT_EXCEEDS_GATE" in result["reason_codes"]


def test_ineligible_method_cannot_trigger_disagreement_review() -> None:
    stability = load_stability()
    result = stability.assess_method_disagreement(
        {"baseline": 100.0, "model": 108.0, "sandbox": 180.0},
        selected_method_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "PILOT_ELIGIBLE",
            "sandbox": "SANDBOX_ONLY",
        },
        stage="PILOT",
        max_relative_disagreement_pct=10.0,
    )
    assert result["assessment_status"] == "STABLE"
    assert result["max_relative_disagreement_pct"] == 8.0
    assert result["method_assessments"]["sandbox"]["eligible_for_stage"] is False


def test_no_comparable_eligible_estimate_withholds_stability() -> None:
    stability = load_stability()
    result = stability.assess_method_disagreement(
        {"baseline": 100.0, "sandbox": 180.0},
        selected_method_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "sandbox": "SANDBOX_ONLY",
        },
        stage="PILOT",
        max_relative_disagreement_pct=10.0,
    )
    assert result["assessment_status"] == "WITHHOLD"
    assert result["max_relative_disagreement_pct"] is None
    assert "NO_COMPARABLE_ELIGIBLE_ESTIMATE" in result["reason_codes"]


def test_small_positive_selected_estimate_uses_true_relative_disagreement() -> None:
    stability = load_stability()
    result = stability.assess_method_disagreement(
        {"baseline": 0.25, "model": 0.50},
        selected_method_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "PILOT_ELIGIBLE",
        },
        stage="PILOT",
        max_relative_disagreement_pct=50.0,
    )
    assert result["assessment_status"] == "REVIEW_REQUIRED"
    assert result["max_relative_disagreement_pct"] == 100.0


def test_zero_selected_estimate_withholds_relative_disagreement() -> None:
    stability = load_stability()
    result = stability.assess_method_disagreement(
        {"baseline": 0.0, "model": 1.0},
        selected_method_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "PILOT_ELIGIBLE",
        },
        stage="PILOT",
        max_relative_disagreement_pct=10.0,
    )
    assert result["assessment_status"] == "WITHHOLD"
    assert result["max_relative_disagreement_pct"] is None
    assert "ZERO_SELECTED_ESTIMATE_NO_RELATIVE_DISAGREEMENT" in result["reason_codes"]


def test_policy_sensitivity_requires_review_when_target_is_unstable() -> None:
    stability = load_stability()
    result = stability.assess_policy_sensitivity(
        {
            "registered": 100.0,
            "lower_shortage_weight": 94.0,
            "higher_shortage_weight": 125.0,
        },
        reference_policy_id="registered",
        max_relative_target_change_pct=10.0,
        required_scenario_ids=("lower_shortage_weight", "higher_shortage_weight"),
    )
    assert result["assessment_status"] == "REVIEW_REQUIRED"
    assert result["max_relative_target_change_pct"] == 25.0
    assert "POLICY_SENSITIVITY_EXCEEDS_GATE" in result["reason_codes"]


def test_policy_sensitivity_withholds_when_required_scenario_is_missing() -> None:
    stability = load_stability()
    result = stability.assess_policy_sensitivity(
        {"registered": 100.0, "lower_shortage_weight": 97.0},
        reference_policy_id="registered",
        max_relative_target_change_pct=10.0,
        required_scenario_ids=("lower_shortage_weight", "higher_shortage_weight"),
    )
    assert result["assessment_status"] == "WITHHOLD"
    assert result["max_relative_target_change_pct"] is None
    assert "REQUIRED_SENSITIVITY_SCENARIO_UNAVAILABLE" in result["reason_codes"]


def test_small_positive_reference_uses_true_relative_sensitivity() -> None:
    stability = load_stability()
    result = stability.assess_policy_sensitivity(
        {"registered": 0.25, "higher_shortage_weight": 0.50},
        reference_policy_id="registered",
        max_relative_target_change_pct=50.0,
        required_scenario_ids=("higher_shortage_weight",),
    )
    assert result["assessment_status"] == "REVIEW_REQUIRED"
    assert result["max_relative_target_change_pct"] == 100.0


def test_zero_reference_target_withholds_relative_sensitivity() -> None:
    stability = load_stability()
    result = stability.assess_policy_sensitivity(
        {"registered": 0.0, "higher_shortage_weight": 1.0},
        reference_policy_id="registered",
        max_relative_target_change_pct=10.0,
        required_scenario_ids=("higher_shortage_weight",),
    )
    assert result["assessment_status"] == "WITHHOLD"
    assert result["max_relative_target_change_pct"] is None
    assert "ZERO_REFERENCE_TARGET_NO_RELATIVE_SENSITIVITY" in result["reason_codes"]


def main() -> int:
    tests = [
        test_method_disagreement_requires_review_past_registered_gate,
        test_ineligible_method_cannot_trigger_disagreement_review,
        test_no_comparable_eligible_estimate_withholds_stability,
        test_small_positive_selected_estimate_uses_true_relative_disagreement,
        test_zero_selected_estimate_withholds_relative_disagreement,
        test_policy_sensitivity_requires_review_when_target_is_unstable,
        test_policy_sensitivity_withholds_when_required_scenario_is_missing,
        test_small_positive_reference_uses_true_relative_sensitivity,
        test_zero_reference_target_withholds_relative_sensitivity,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
