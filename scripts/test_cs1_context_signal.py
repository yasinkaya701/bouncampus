#!/usr/bin/env python3
"""Regression tests for CS1 contextual-signal correction and ablation."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_context_signal():
    path = ROOT / "backend/app/decision/context_signal.py"
    if not path.exists():
        raise AssertionError("context-signal module missing")
    spec = importlib.util.spec_from_file_location("cs1_context_signal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ts(day: int, hour: int) -> str:
    return f"2026-10-{day:02d}T{hour:02d}:00:00+03:00"


def reconciled(n: int = 4) -> list[bool]:
    return [True] * n


def reconciled_times(n: int = 4) -> list[str]:
    return [ts(day, 18) for day in range(1, n + 1)]


def test_context_correction_is_strictly_past_only() -> None:
    context_signal = load_context_signal()
    kwargs = dict(
        base_forecasts=[100, 100, 100, 100],
        context_keys=["menu:A", "menu:A", "menu:B", "menu:A"],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8), ts(4, 8)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10), ts(4, 10)],
        outcome_reconciled=reconciled(),
        outcome_reconciled_at=reconciled_times(),
        min_history=2,
        min_context_history=2,
        shrinkage_strength=2.0,
    )
    first = context_signal.generate_context_residual_forecasts(
        actual_demand=[110, 120, 90, 999],
        **kwargs,
    )
    changed_future = context_signal.generate_context_residual_forecasts(
        actual_demand=[110, 120, 90, 1],
        **kwargs,
    )

    assert first["context_forecast"] == changed_future["context_forecast"]
    assert first["history_n"] == [0, 1, 2, 3]
    assert first["context_history_n"] == [0, 1, 0, 2]
    assert first["context_applied"] == [False, False, False, True]
    assert math.isclose(first["baseline_forecast"][3], 106.66666666666667)
    assert math.isclose(first["context_forecast"][3], 110.83333333333334)
    assert first["leakage_policy"] == "PAST_RECONCILED_ROWS_VISIBLE_BY_CUTOFF_ONLY"
    assert first["reconciliation_policy"] == "EXPLICIT_CALLER_ACCEPTED_OUTCOME_REQUIRED"
    assert first["reconciliation_time_policy"] == (
        "OUTCOME_MUST_BE_RECONCILED_AND_AVAILABLE_BY_CURRENT_DECISION_CUTOFF"
    )


def test_signal_published_after_cutoff_cannot_change_decision() -> None:
    context_signal = load_context_signal()
    report = context_signal.generate_context_residual_forecasts(
        base_forecasts=[100, 100, 100, 100],
        actual_demand=[110, 120, 130, 140],
        context_keys=[
            "calendar:teaching",
            "calendar:teaching",
            "calendar:teaching",
            "calendar:teaching",
        ],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8), ts(4, 12)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10), ts(4, 10)],
        outcome_reconciled=reconciled(),
        outcome_reconciled_at=reconciled_times(),
        min_history=2,
        min_context_history=2,
        shrinkage_strength=1.0,
    )

    assert report["context_applied"][3] is False
    assert report["context_forecast"][3] == report["baseline_forecast"][3]
    assert "SIGNAL_NOT_AVAILABLE_AT_DECISION_TIME" in report["reason_codes"][3]


def test_sparse_context_falls_back_to_history_only_baseline() -> None:
    context_signal = load_context_signal()
    report = context_signal.generate_context_residual_forecasts(
        base_forecasts=[100, 100, 100, 100],
        actual_demand=[110, 120, 90, 95],
        context_keys=["menu:A", "menu:A", "menu:B", "menu:B"],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8), ts(4, 8)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10), ts(4, 10)],
        outcome_reconciled=reconciled(),
        outcome_reconciled_at=reconciled_times(),
        min_history=2,
        min_context_history=2,
        shrinkage_strength=2.0,
    )

    assert report["context_history_n"][3] == 1
    assert report["context_applied"][3] is False
    assert report["context_forecast"][3] == report["baseline_forecast"][3]
    assert "INSUFFICIENT_CONTEXT_HISTORY" in report["reason_codes"][3]


def test_unreconciled_historical_outlier_cannot_influence_later_forecast() -> None:
    context_signal = load_context_signal()
    report = context_signal.generate_context_residual_forecasts(
        base_forecasts=[100, 100, 100, 100],
        actual_demand=[100, 1000, 100, 100],
        context_keys=["menu:A", "menu:A", "menu:A", "menu:A"],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8), ts(4, 8)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10), ts(4, 10)],
        outcome_reconciled=[True, False, True, True],
        outcome_reconciled_at=[ts(1, 18), None, ts(3, 18), ts(4, 18)],
        min_history=2,
        min_context_history=2,
        shrinkage_strength=0.0,
    )

    assert report["history_n"] == [0, 1, 1, 2]
    assert report["context_history_n"] == [0, 1, 1, 2]
    assert report["baseline_forecast"][3] == 100.0
    assert report["context_forecast"][3] == 100.0
    assert report["context_applied"][3] is True
    assert "OUTCOME_NOT_RECONCILED_NOT_LEARNED" in report["reason_codes"][1]


def test_context_ablation_uses_identical_support_and_explicit_decision_loss() -> None:
    context_signal = load_context_signal()
    comparison = context_signal.compare_context_signal_forecasts(
        actual_demand=[100, 110, 90, None],
        baseline_forecast=[100, 100, 100, 100],
        context_forecast=[90, None, 95, 90],
        context_applied=[True, False, True, True],
        excess_cost=1.0,
        shortage_cost=3.0,
    )

    assert comparison["evaluation_indices"] == [0, 2]
    assert comparison["common_support_n"] == 2
    assert comparison["metrics"]["baseline"]["mae"] == 5.0
    assert comparison["metrics"]["context_signal"]["mae"] == 7.5
    assert comparison["metrics"]["baseline"]["mean_loss"] == 5.0
    assert comparison["metrics"]["context_signal"]["mean_loss"] == 17.5
    assert comparison["cost_provenance"] == "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"
    assert comparison["result_scope"] == "OFFLINE_CONTEXT_ABLATION_ONLY"


def test_median_residual_estimator_resists_single_historical_outlier() -> None:
    context_signal = load_context_signal()
    report = context_signal.generate_context_residual_forecasts(
        base_forecasts=[100, 100, 100, 100],
        actual_demand=[100, 100, 1000, 100],
        context_keys=["menu:A", "menu:A", "menu:A", "menu:A"],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8), ts(4, 8)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10), ts(4, 10)],
        outcome_reconciled=reconciled(),
        outcome_reconciled_at=reconciled_times(),
        min_history=3,
        min_context_history=3,
        shrinkage_strength=0.0,
        residual_statistic="MEDIAN",
    )

    assert report["baseline_forecast"][3] == 100.0
    assert report["context_forecast"][3] == 100.0
    assert report["context_applied"][3] is True
    assert report["residual_statistic"] == "MEDIAN"


def main() -> int:
    tests = [
        test_context_correction_is_strictly_past_only,
        test_signal_published_after_cutoff_cannot_change_decision,
        test_sparse_context_falls_back_to_history_only_baseline,
        test_unreconciled_historical_outlier_cannot_influence_later_forecast,
        test_context_ablation_uses_identical_support_and_explicit_decision_loss,
        test_median_residual_estimator_resists_single_historical_outlier,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
