#!/usr/bin/env python3
"""Regression tests for reservation-first CS1 decision intelligence."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_reservation_module():
    path = ROOT / "backend/app/decision/reservation.py"
    spec = importlib.util.spec_from_file_location("cs1_reservation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reservation_first_baseline_is_past_only() -> None:
    reservation = load_reservation_module()
    report = reservation.generate_reservation_baselines(
        [100, 100, 100, 100],
        [80, 90, 100, 0],
        [20, 30, 40, 1000],
        min_history=2,
    )
    assert report["raw_reservation"] == [100.0, 100.0, 100.0, 100.0]
    assert report["corrected_reservation"][:2] == [None, None]
    assert math.isclose(report["corrected_reservation"][2], 110.0)
    assert math.isclose(report["corrected_reservation"][3], 120.0)
    assert report["history_n"] == [0, 1, 2, 3]
    assert report["semantics"] == "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND"
    assert report["leakage_policy"] == "PAST_RECONCILED_SERVICES_ONLY"


def test_invalid_reconciliation_rows_are_not_learned_from() -> None:
    reservation = load_reservation_module()
    report = reservation.generate_reservation_baselines(
        [100, 100, 100, 100],
        [80, 120, 90, 95],
        [20, 10, 30, 25],
        min_history=2,
    )
    assert report["history_n"] == [0, 1, 1, 2]
    assert report["corrected_reservation"][2] is None
    assert math.isclose(report["corrected_reservation"][3], 110.0)


def test_reconciliation_diagnostics_explain_withhold_and_exclusions() -> None:
    reservation = load_reservation_module()
    report = reservation.generate_reservation_baselines(
        [100, 100, 100, 100],
        [80, 120, 90, 95],
        [20, 10, 30, 25],
        min_history=2,
    )
    assert report["reconciliation_status"] == [
        "RECONCILED",
        "EXCLUDED",
        "RECONCILED",
        "RECONCILED",
    ]
    assert (
        "RESERVED_SERVED_EXCEEDS_ACTIVE_RESERVATIONS"
        in report["reconciliation_reason_codes"][1]
    )
    assert report["reconciled_row_count"] == 3
    assert report["excluded_row_count"] == 1
    assert report["baseline_readiness"] == [
        "WITHHOLD",
        "WITHHOLD",
        "WITHHOLD",
        "BENCHMARK_READY",
    ]
    assert (
        "INSUFFICIENT_RECONCILED_HISTORY"
        in report["baseline_reason_codes"][2]
    )


def test_asymmetric_decision_loss_is_explicit_sensitivity_not_money() -> None:
    reservation = load_reservation_module()
    result = reservation.evaluate_decision_loss(
        [100, 100],
        [120, 80],
        excess_cost=1,
        shortage_cost=3,
    )
    assert result["n"] == 2
    assert result["surplus_units"] == 20.0
    assert result["shortage_units"] == 20.0
    assert result["total_loss"] == 80.0
    assert result["mean_loss"] == 40.0
    assert result["loss_unit"] == "RELATIVE_COST_UNITS"
    assert result["cost_provenance"] == "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"


def test_policy_comparison_uses_common_support_and_asymmetric_loss() -> None:
    reservation = load_reservation_module()
    report = reservation.compare_decision_policies(
        [100, 100, 100],
        {
            "conservative": [110, 110, None],
            "lean": [90, 90, 90],
        },
        excess_cost=1,
        shortage_cost=4,
    )
    assert report["evaluation_indices"] == [0, 1]
    assert report["ranking_by_mean_loss"] == ["conservative", "lean"]
    assert report["best_by_mean_loss"] == "conservative"
    assert report["common_support_n"] == 2
    assert report["result_scope"] == "OFFLINE_DECISION_BENCHMARK_ONLY"


def test_validation_rejects_bad_alignment_and_costs() -> None:
    reservation = load_reservation_module()
    try:
        reservation.generate_reservation_baselines([1], [1, 2], [0], min_history=1)
    except ValueError as exc:
        assert "same length" in str(exc)
    else:
        raise AssertionError("misaligned reservation inputs must be rejected")

    for bad_cost in (-1, float("nan"), float("inf")):
        try:
            reservation.evaluate_decision_loss(
                [10],
                [10],
                excess_cost=bad_cost,
                shortage_cost=1,
            )
        except ValueError as exc:
            assert "finite and non-negative" in str(exc)
        else:
            raise AssertionError("invalid decision-loss cost must be rejected")


def main() -> int:
    tests = [
        test_reservation_first_baseline_is_past_only,
        test_invalid_reconciliation_rows_are_not_learned_from,
        test_reconciliation_diagnostics_explain_withhold_and_exclusions,
        test_asymmetric_decision_loss_is_explicit_sensitivity_not_money,
        test_policy_comparison_uses_common_support_and_asymmetric_loss,
        test_validation_rejects_bad_alignment_and_costs,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
