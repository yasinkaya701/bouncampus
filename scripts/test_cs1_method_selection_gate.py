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


def base_kwargs() -> dict[str, object]:
    return {
        "baseline_id": "baseline",
        "method_eligibility": {
            "baseline": "PILOT_ELIGIBLE",
            "model": "EVALUATED_OFFLINE",
        },
        "stage": "OFFLINE_EVALUATION",
        "primary_metric": "mae",
        "min_common_support_n": 10,
        "min_relative_improvement_pct": 0.0,
    }


def assert_raises_value_error(callable_obj, expected_text: str) -> None:
    try:
        callable_obj()
    except ValueError as exc:
        assert expected_text in str(exc)
    else:
        raise AssertionError(f"expected ValueError containing {expected_text!r}")


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


def test_no_comparable_eligible_candidate_withholds_instead_of_claiming_selection() -> None:
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
    assert result["selection_status"] == "WITHHOLD"
    assert result["selected_method"] is None
    assert "NO_COMPARABLE_ELIGIBLE_CANDIDATE" in result["reason_codes"]


def test_pilot_stage_excludes_offline_only_candidate_and_withholds() -> None:
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
    assert result["selection_status"] == "WITHHOLD"
    assert result["selected_method"] is None
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


def test_malformed_baseline_metric_fails_closed() -> None:
    gate = load_gate()
    data = comparison()
    data["metrics"]["baseline"]["mae"] = "not-a-number"
    result = gate.select_method(data, **base_kwargs())
    assert result["selection_status"] == "WITHHOLD"
    assert result["selected_method"] is None
    assert "DESIGNATED_BASELINE_METRIC_UNAVAILABLE" in result["reason_codes"]


def test_malformed_candidate_metric_withholds_when_no_comparable_candidate_remains() -> None:
    gate = load_gate()
    data = comparison()
    data["metrics"]["model"]["mae"] = "bad"
    result = gate.select_method(data, **base_kwargs())
    assert result["selection_status"] == "WITHHOLD"
    assert result["selected_method"] is None
    assert "METRIC_UNAVAILABLE" in result["candidate_assessments"]["model"]["reason_codes"]
    assert "NO_COMPARABLE_ELIGIBLE_CANDIDATE" in result["reason_codes"]


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


def test_explicit_candidate_subset_requires_at_least_one_comparable_candidate() -> None:
    gate = load_gate()
    result = gate.select_method(
        comparison(),
        **base_kwargs(),
        candidate_method_ids=[],
    )
    assert result["selection_status"] == "WITHHOLD"
    assert "NO_COMPARABLE_ELIGIBLE_CANDIDATE" in result["reason_codes"]


def test_fractional_or_boolean_support_controls_are_rejected() -> None:
    gate = load_gate()
    fractional_support = comparison()
    fractional_support["common_support_n"] = 10.9
    assert_raises_value_error(
        lambda: gate.select_method(fractional_support, **base_kwargs()),
        "common_support_n must be an integer",
    )

    kwargs = base_kwargs()
    kwargs["min_common_support_n"] = 10.5
    assert_raises_value_error(
        lambda: gate.select_method(comparison(), **kwargs),
        "min_common_support_n must be an integer",
    )

    kwargs = base_kwargs()
    kwargs["min_relative_improvement_pct"] = True
    assert_raises_value_error(
        lambda: gate.select_method(comparison(), **kwargs),
        "min_relative_improvement_pct must be finite and non-negative",
    )


def test_candidate_method_ids_must_not_be_a_string() -> None:
    gate = load_gate()
    assert_raises_value_error(
        lambda: gate.select_method(
            comparison(),
            **base_kwargs(),
            candidate_method_ids="model",
        ),
        "candidate_method_ids must be a sequence of method IDs",
    )


def main() -> int:
    tests = [
        test_candidate_must_earn_promotion_over_baseline,
        test_baseline_is_retained_when_complexity_does_not_clear_gate,
        test_no_comparable_eligible_candidate_withholds_instead_of_claiming_selection,
        test_pilot_stage_excludes_offline_only_candidate_and_withholds,
        test_insufficient_common_support_withholds_selection,
        test_malformed_baseline_metric_fails_closed,
        test_malformed_candidate_metric_withholds_when_no_comparable_candidate_remains,
        test_decision_loss_can_be_registered_as_primary_metric,
        test_explicit_candidate_subset_requires_at_least_one_comparable_candidate,
        test_fractional_or_boolean_support_controls_are_rejected,
        test_candidate_method_ids_must_not_be_a_string,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
