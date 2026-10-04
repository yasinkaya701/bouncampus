#!/usr/bin/env python3
"""Regression tests for reconciliation-time and chronology leakage guards."""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_context_signal():
    path = ROOT / "backend/app/decision/context_signal.py"
    spec = importlib.util.spec_from_file_location("cs1_context_signal_temporal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ts(day: int, hour: int) -> str:
    return f"2026-10-{day:02d}T{hour:02d}:00:00+03:00"


def test_api_requires_reconciliation_timestamp_semantics() -> None:
    context_signal = load_context_signal()
    parameters = inspect.signature(
        context_signal.generate_context_residual_forecasts
    ).parameters
    assert "outcome_reconciled_at" in parameters, (
        "past-only correction cannot prove an outcome was known by a future cutoff "
        "without an explicit reconciliation timestamp"
    )


def test_outcome_enters_history_only_after_reconciliation_time() -> None:
    context_signal = load_context_signal()
    report = context_signal.generate_context_residual_forecasts(
        base_forecasts=[100, 100, 100],
        actual_demand=[150, 100, 100],
        context_keys=["menu:A", "menu:A", "menu:A"],
        signal_available_at=[ts(1, 8), ts(2, 8), ts(3, 8)],
        decision_cutoff_at=[ts(1, 10), ts(2, 10), ts(3, 10)],
        outcome_reconciled=[True, False, False],
        outcome_reconciled_at=[ts(3, 9), None, None],
        min_history=1,
        min_context_history=1,
        shrinkage_strength=0.0,
    )

    assert report["history_n"] == [0, 0, 1]
    assert report["context_history_n"] == [0, 0, 1]
    assert report["baseline_forecast"] == [100.0, 100.0, 150.0]
    assert report["context_forecast"] == [100.0, 100.0, 150.0]
    assert report["reconciliation_time_policy"] == (
        "OUTCOME_MUST_BE_RECONCILED_AND_AVAILABLE_BY_CURRENT_DECISION_CUTOFF"
    )


def test_out_of_order_decision_cutoffs_fail_closed() -> None:
    context_signal = load_context_signal()
    try:
        context_signal.generate_context_residual_forecasts(
            base_forecasts=[100, 100],
            actual_demand=[100, 100],
            context_keys=["menu:A", "menu:A"],
            signal_available_at=[ts(2, 8), ts(1, 8)],
            decision_cutoff_at=[ts(2, 10), ts(1, 10)],
            outcome_reconciled=[False, False],
            outcome_reconciled_at=[None, None],
            min_history=1,
            min_context_history=1,
            shrinkage_strength=0.0,
        )
    except ValueError as exc:
        assert "decision_cutoff_at must be chronological" in str(exc)
    else:
        raise AssertionError("out-of-order decision cutoffs must fail closed")


def test_reconciled_outcome_without_timestamp_fails_closed() -> None:
    context_signal = load_context_signal()
    try:
        context_signal.generate_context_residual_forecasts(
            base_forecasts=[100],
            actual_demand=[110],
            context_keys=["menu:A"],
            signal_available_at=[ts(1, 8)],
            decision_cutoff_at=[ts(1, 10)],
            outcome_reconciled=[True],
            outcome_reconciled_at=[None],
            min_history=1,
            min_context_history=1,
            shrinkage_strength=0.0,
        )
    except ValueError as exc:
        assert "reconciled outcome requires outcome_reconciled_at" in str(exc)
    else:
        raise AssertionError("timestamp-less reconciled truth must fail closed")


def test_reconciliation_cannot_predate_its_own_decision_cutoff() -> None:
    context_signal = load_context_signal()
    try:
        context_signal.generate_context_residual_forecasts(
            base_forecasts=[100],
            actual_demand=[110],
            context_keys=["menu:A"],
            signal_available_at=[ts(1, 8)],
            decision_cutoff_at=[ts(1, 10)],
            outcome_reconciled=[True],
            outcome_reconciled_at=[ts(1, 9)],
            min_history=1,
            min_context_history=1,
            shrinkage_strength=0.0,
        )
    except ValueError as exc:
        assert "outcome_reconciled_at must be after its own decision cutoff" in str(exc)
    else:
        raise AssertionError("pre-cutoff outcome truth must fail closed")


def main() -> int:
    tests = [
        test_api_requires_reconciliation_timestamp_semantics,
        test_outcome_enters_history_only_after_reconciliation_time,
        test_out_of_order_decision_cutoffs_fail_closed,
        test_reconciled_outcome_without_timestamp_fails_closed,
        test_reconciliation_cannot_predate_its_own_decision_cutoff,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
