#!/usr/bin/env python3
"""Integration tests for reservation-aware CS1 offline benchmarking."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_benchmark_module():
    path = ROOT / "scripts/cs1_baseline_benchmark.py"
    spec = importlib.util.spec_from_file_location("cs1_baseline_benchmark", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_rows() -> list[dict[str, str]]:
    return [
        {
            "served": "100",
            "reservations": "100",
            "reserved_served": "80",
            "unreserved": "20",
        },
        {
            "served": "120",
            "reservations": "100",
            "reserved_served": "90",
            "unreserved": "30",
        },
        {
            "served": "110",
            "reservations": "100",
            "reserved_served": "85",
            "unreserved": "25",
        },
        {
            "served": "130",
            "reservations": "110",
            "reserved_served": "95",
            "unreserved": "35",
        },
    ]


def reproducibility_kwargs() -> dict[str, object]:
    return {
        "dataset_id": "reservation-fixture-v1",
        "dataset_provenance_class": "MEASURED_OPERATIONAL",
        "dataset_data_class": "MEASURED",
        "dataset_checksum_sha256": "b" * 64,
        "git_commit_sha": "0123456789abcdef0123456789abcdef01234567",
        "target_definition": "served portions per service",
        "decision_time_cutoff_rule": "reservations frozen before production decision",
        "evaluation_window": "fixture rows 1-4 in chronological order",
        "model_version": None,
        "model_feature_ids": None,
    }


def test_reservation_candidates_join_forecast_and_decision_benchmarks() -> None:
    benchmark = load_benchmark_module()
    report = benchmark.build_report(
        fixture_rows(),
        dataset_label="fixture",
        actual_column="served",
        model_column=None,
        operator_column=None,
        rolling_window=2,
        seasonal_lag=2,
        reservation_column="reservations",
        reserved_served_column="reserved_served",
        unreserved_column="unreserved",
        excess_cost=1.0,
        shortage_cost=3.0,
        **reproducibility_kwargs(),
    )

    assert "raw_reservation" in report["forecast_candidates"]
    assert "corrected_reservation" in report["forecast_candidates"]
    assert (
        report["reservation_reconciliation"]["semantics"]
        == "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND"
    )
    assert report["reservation_reconciliation"]["corrected_reservation"][:2] == [
        None,
        None,
    ]
    assert (
        report["decision_evaluation"]["cost_provenance"]
        == "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"
    )
    assert report["decision_evaluation"]["common_support_n"] > 0
    assert report["reproducibility"]["status"] == "COMPLETE"
    assert report["reproducibility"]["eligibility_conclusion"] == "OFFLINE_EVALUATION_ONLY"
    assert "savings" in report["claim_boundary"].lower()


def test_partial_reservation_contract_is_rejected() -> None:
    benchmark = load_benchmark_module()
    try:
        benchmark.build_report(
            fixture_rows(),
            dataset_label="fixture",
            actual_column="served",
            model_column=None,
            operator_column=None,
            rolling_window=2,
            seasonal_lag=2,
            reservation_column="reservations",
            reserved_served_column=None,
            unreserved_column=None,
            excess_cost=1.0,
            shortage_cost=1.0,
            **reproducibility_kwargs(),
        )
    except ValueError as exc:
        assert "reservation reconciliation requires" in str(exc)
    else:
        raise AssertionError("partial reservation configuration must be rejected")


def main() -> int:
    tests = [
        test_reservation_candidates_join_forecast_and_decision_benchmarks,
        test_partial_reservation_contract_is_rejected,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
