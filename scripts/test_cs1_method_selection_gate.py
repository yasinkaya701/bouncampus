#!/usr/bin/env python3
"""Regression tests for CS1 baseline-first method-selection gates."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_gate():
    path = ROOT / "backend/app/decision/method_selection.py"
    if not path.exists():
        raise AssertionError("method-selection gate missing")
    spec = importlib.util.spec_from_file_location("cs1_method_selection", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def comparison(
    baseline_mae: float = 10.0,
    model_mae: float = 8.0,
    support: int = 20,
) -> dict[str, object]:
    return {
        "metrics": {
            "baseline": {
                "mae": baseline_mae,
                "rmse": baseline_mae + 1,
                "wape_pct": 10.0,
            },
            "model": {
                "mae": model_mae,
                "rmse": model_mae + 1,
                "wape_pct": 8.0,
            },
        },
        "common_support_n": support,
        "result_scope": "OFFLINE_BENCHMARK_ONLY",
    }


def test_candidate_must_earn_promotion_over_baseline() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(),
        baseline_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "EVALUATED_OFFLINE",
        },
        stage="OFFLINE_EVALUATION",
        primary_metric="mae",
        min_common_support_n=10,
        min_relative_improvement_pct=10.0,
    )
    assert result["selection_status"] == "SELECTED"
    assert result["selected_method"] == "model"
    assert result["selection_rule"] == "CANDIDATE_BEATS_BASELINE"
    assert result["relative_improvement_pct_vs_baseline"] == 20.0


def test_baseline_is_retained_when_complexity_does_not_clear_gate() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(model_mae=9.5),
        baseline_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "EVALUATED_OFFLINE",
        },
        stage="OFFLINE_EVALUATION",
        primary_metric="mae",
        min_common_support_n=10,
        min_relative_improvement_pct=10.0,
    )
    assert result["selected_method"] == "baseline"
    assert result["selection_rule"] == "BASELINE_RETAINED_COMPLEXITY_NOT_JUSTIFIED"
    assert "CANDIDATE_IMPROVEMENT_BELOW_REGISTERED_GATE" in result["reason_codes"]


def test_sandbox_candidate_fails_closed_even_if_metric_is_best() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(model_mae=1.0),
        baseline_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "SANDBOX_ONLY",
        },
        stage="OFFLINE_EVALUATION",
        primary_metric="mae",
        min_common_support_n=10,
        min_relative_improvement_pct=0.0,
    )
    assert result["selected_method"] == "baseline"
    assert result["candidate_assessments"]["model"]["eligible_for_stage"] is False
    assert (
        "METHOD_NOT_ELIGIBLE_FOR_STAGE"
        in result["candidate_assessments"]["model"]["reason_codes"]
    )


def test_pilot_stage_excludes_offline_only_candidate() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(model_mae=1.0),
        baseline_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "EVALUATED_OFFLINE",
        },
        stage="PILOT",
        primary_metric="mae",
        min_common_support_n=10,
        min_relative_improvement_pct=0.0,
    )
    assert result["selected_method"] == "baseline"
    assert result["candidate_assessments"]["model"]["eligible_for_stage"] is False


def test_insufficient_common_support_withholds_selection() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(support=4),
        baseline_id="baseline",
        method_eligibility={
            "baseline": "PILOT_ELIGIBLE",
            "model": "PILOT_ELIGIBLE",
        },
        stage="PILOT",
        primary_metric="mae",
        min_common_support_n=10,
        min_relative_improvement_pct=0.0,
    )
    assert result["selection_status"] == "WITHHOLD"
    assert result["selected_method"] is None
    assert "INSUFFICIENT_COMMON_SUPPORT" in result["reason_codes"]


def test_decision_loss_can_be_registered_as_primary_metric() -> None:
    gate = load_gate()
    result = gate.select_method(
        {
            "metrics": {
                "raw_reservation": {"mean_loss": 12.0},
                "corrected_reservation": {"mean_loss": 9.0},
            },
            "common_support_n": 20,
            "result_scope": "OFFLINE_DECISION_BENCHMARK_ONLY",
        },
        baseline_id="raw_reservation",
        method_eligibility={
            "raw_reservation": "PILOT_ELIGIBLE",
            "corrected_reservation": "EVALUATED_OFFLINE",
        },
        stage="OFFLINE_EVALUATION",
        primary_metric="mean_loss",
        min_common_support_n=10,
        min_relative_improvement_pct=10.0,
    )
    assert result["selected_method"] == "corrected_reservation"
    assert result["relative_improvement_pct_vs_baseline"] == 25.0


def main() -> int:
    tests = [
        test_candidate_must_earn_promotion_over_baseline,
        test_baseline_is_retained_when_complexity_does_not_clear_gate,
        test_sandbox_candidate_fails_closed_even_if_metric_is_best,
        test_pilot_stage_excludes_offline_only_candidate,
        test_insufficient_common_support_withholds_selection,
        test_decision_loss_can_be_registered_as_primary_metric,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
