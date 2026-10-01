#!/usr/bin/env python3
"""Regression tests for the CS1 executable decision gate."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_gate():
    path = ROOT / "backend/app/decision/decision_gate.py"
    if not path.exists():
        raise AssertionError("decision gate missing")
    spec = importlib.util.spec_from_file_location("cs1_decision_gate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_kwargs() -> dict[str, object]:
    return {
        "comparison": {
            "metrics": {
                "raw_reservation": {"mean_loss": 12.0},
                "corrected_reservation": {"mean_loss": 9.0},
            },
            "common_support_n": 20,
            "result_scope": "OFFLINE_DECISION_BENCHMARK_ONLY",
        },
        "baseline_id": "raw_reservation",
        "method_eligibility": {
            "raw_reservation": "PILOT_ELIGIBLE",
            "corrected_reservation": "EVALUATED_OFFLINE",
        },
        "stage": "OFFLINE_EVALUATION",
        "primary_metric": "mean_loss",
        "min_common_support_n": 10,
        "min_relative_improvement_pct": 10.0,
        "method_estimates": {
            "raw_reservation": 100.0,
            "corrected_reservation": 104.0,
        },
        "max_relative_disagreement_pct": 10.0,
        "policy_scenario_targets": {
            "registered": 104.0,
            "lower_shortage_weight": 101.0,
            "higher_shortage_weight": 108.0,
        },
        "reference_policy_id": "registered",
        "max_relative_target_change_pct": 10.0,
        "required_scenario_ids": (
            "lower_shortage_weight",
            "higher_shortage_weight",
        ),
    }


def test_stable_selected_method_becomes_human_gated_advisory_candidate() -> None:
    gate = load_gate()
    result = gate.run_decision_gate(**base_kwargs())
    assert result["decision_status"] == "ADVISORY_CANDIDATE"
    assert result["selected_method"] == "corrected_reservation"
    assert result["human_gate_required"] is True
    assert result["automatic_dispatch_allowed"] is False
    assert result["selection"]["selection_rule"] == "CANDIDATE_BEATS_BASELINE"
    assert result["method_stability"]["assessment_status"] == "STABLE"
    assert result["policy_sensitivity"]["assessment_status"] == "STABLE"


def test_selection_withhold_blocks_decision() -> None:
    gate = load_gate()
    kwargs = base_kwargs()
    kwargs["comparison"] = {
        **kwargs["comparison"],
        "common_support_n": 2,
    }
    result = gate.run_decision_gate(**kwargs)
    assert result["decision_status"] == "WITHHOLD"
    assert result["selected_method"] is None
    assert "SELECTION_WITHHELD" in result["reason_codes"]


def test_method_disagreement_requires_human_review() -> None:
    gate = load_gate()
    kwargs = base_kwargs()
    kwargs["method_estimates"] = {
        "raw_reservation": 100.0,
        "corrected_reservation": 140.0,
    }
    result = gate.run_decision_gate(**kwargs)
    assert result["decision_status"] == "REVIEW_REQUIRED"
    assert "METHOD_DISAGREEMENT_REQUIRES_REVIEW" in result["reason_codes"]


def test_policy_sensitivity_requires_human_review() -> None:
    gate = load_gate()
    kwargs = base_kwargs()
    kwargs["policy_scenario_targets"] = {
        "registered": 104.0,
        "lower_shortage_weight": 80.0,
        "higher_shortage_weight": 135.0,
    }
    result = gate.run_decision_gate(**kwargs)
    assert result["decision_status"] == "REVIEW_REQUIRED"
    assert "POLICY_SENSITIVITY_REQUIRES_REVIEW" in result["reason_codes"]


def main() -> int:
    tests = [
        test_stable_selected_method_becomes_human_gated_advisory_candidate,
        test_selection_withhold_blocks_decision,
        test_method_disagreement_requires_human_review,
        test_policy_sensitivity_requires_human_review,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
