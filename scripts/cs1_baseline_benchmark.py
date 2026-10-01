#!/usr/bin/env python3
"""Benchmark CS1 food-demand candidates against leakage-safe baselines.

This script never invents observations. It requires a measured or explicitly labeled
CSV dataset supplied by the caller and reports offline forecast/decision metrics only.
Reservation counts are treated as intent signals, never as served demand.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.baselines import compare_forecasts, generate_naive_baselines  # noqa: E402
from app.decision.reservation import (  # noqa: E402
    compare_decision_policies,
    generate_reservation_baselines,
)


def parse_optional_number(value: str | None):
    if value is None:
        return None
    stripped = value.strip()
    if stripped == "":
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise ValueError(f"expected numeric value, found {value!r}") from exc


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        return list(reader)


def build_report(
    rows: list[dict[str, str]],
    *,
    dataset_label: str,
    actual_column: str,
    model_column: str | None,
    operator_column: str | None,
    rolling_window: int,
    seasonal_lag: int,
    reservation_column: str | None = None,
    reserved_served_column: str | None = None,
    unreserved_column: str | None = None,
    excess_cost: float = 1.0,
    shortage_cost: float = 1.0,
) -> dict[str, object]:
    if not rows:
        raise ValueError("CSV contains no data rows")
    if actual_column not in rows[0]:
        raise ValueError(f"missing actual column {actual_column!r}")

    actual = []
    for index, row in enumerate(rows, start=2):
        value = parse_optional_number(row.get(actual_column))
        if value is None:
            raise ValueError(f"row {index}: actual column {actual_column!r} is required")
        if value < 0:
            raise ValueError(f"row {index}: actual value cannot be negative")
        actual.append(value)

    forecasts: dict[str, list[float | None]] = generate_naive_baselines(
        actual,
        rolling_window=rolling_window,
        seasonal_lag=seasonal_lag,
    )

    def add_optional_forecast(name: str, column: str | None) -> None:
        if not column:
            return
        if column not in rows[0]:
            raise ValueError(f"missing forecast column {column!r}")
        forecasts[name] = [parse_optional_number(row.get(column)) for row in rows]

    add_optional_forecast("model", model_column)
    add_optional_forecast("operator", operator_column)

    reservation_columns = (
        reservation_column,
        reserved_served_column,
        unreserved_column,
    )
    reservation_reconciliation: dict[str, object] | None = None
    if any(reservation_columns):
        if not all(reservation_columns):
            raise ValueError(
                "reservation reconciliation requires reservation, reserved-served, "
                "and unreserved columns together"
            )

        assert reservation_column is not None
        assert reserved_served_column is not None
        assert unreserved_column is not None
        for column in reservation_columns:
            if column not in rows[0]:
                raise ValueError(
                    f"missing reservation reconciliation column {column!r}"
                )

        reservation_reconciliation = generate_reservation_baselines(
            [parse_optional_number(row.get(reservation_column)) for row in rows],
            [parse_optional_number(row.get(reserved_served_column)) for row in rows],
            [parse_optional_number(row.get(unreserved_column)) for row in rows],
        )
        forecasts["raw_reservation"] = list(
            reservation_reconciliation["raw_reservation"]
        )
        forecasts["corrected_reservation"] = list(
            reservation_reconciliation["corrected_reservation"]
        )

    comparison = compare_forecasts(actual, forecasts)
    decision_evaluation = compare_decision_policies(
        actual,
        forecasts,
        excess_cost=excess_cost,
        shortage_cost=shortage_cost,
    )

    return {
        "schema_version": 2,
        "dataset_label": dataset_label,
        "row_count": len(rows),
        "actual_column": actual_column,
        "forecast_candidates": list(forecasts),
        "evaluation": comparison,
        "decision_evaluation": decision_evaluation,
        "reservation_reconciliation": reservation_reconciliation,
        "evidence_class": "TECH_TEST",
        "result_scope": "OFFLINE_BENCHMARK_ONLY",
        "leakage_policy": (
            "Naive and corrected reservation baselines use only observations "
            "before each target row."
        ),
        "reservation_semantics": "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND",
        "decision_loss_semantics": (
            "Forecast candidates are evaluated as direct quantity targets under "
            "relative excess/shortage sensitivity weights."
        ),
        "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
        "claim_boundary": (
            "Forecast and relative decision-loss benchmarks may support "
            "model-selection claims only. They do not demonstrate food-waste, "
            "cost, carbon, or water savings."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv", required=True, type=Path, help="measured/labeled service-level CSV"
    )
    parser.add_argument(
        "--dataset-label", required=True, help="human-readable dataset provenance label"
    )
    parser.add_argument("--actual-column", default="served_portions")
    parser.add_argument("--model-column", default="model_forecast_meals")
    parser.add_argument("--operator-column", default=None)
    parser.add_argument("--rolling-window", type=int, default=3)
    parser.add_argument("--seasonal-lag", type=int, default=7)
    parser.add_argument(
        "--reservation-column",
        default=None,
        help="active reservations at decision cutoff; requires reconciliation columns",
    )
    parser.add_argument(
        "--reserved-served-column",
        default=None,
        help="served demand attributable to cutoff reservations",
    )
    parser.add_argument(
        "--unreserved-column",
        default=None,
        help="served demand not attributable to cutoff reservations",
    )
    parser.add_argument(
        "--excess-cost",
        type=float,
        default=1.0,
        help="relative surplus sensitivity weight; not currency",
    )
    parser.add_argument(
        "--shortage-cost",
        type=float,
        default=1.0,
        help="relative shortage sensitivity weight; not currency",
    )
    parser.add_argument("--output", type=Path, default=None, help="optional JSON output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr)
        return 2
    if args.rolling_window < 1 or args.seasonal_lag < 1:
        print("ERROR: rolling-window and seasonal-lag must be >= 1", file=sys.stderr)
        return 2

    try:
        report = build_report(
            load_rows(args.csv),
            dataset_label=args.dataset_label,
            actual_column=args.actual_column,
            model_column=args.model_column,
            operator_column=args.operator_column,
            rolling_window=args.rolling_window,
            seasonal_lag=args.seasonal_lag,
            reservation_column=args.reservation_column,
            reserved_served_column=args.reserved_served_column,
            unreserved_column=args.unreserved_column,
            excess_cost=args.excess_cost,
            shortage_cost=args.shortage_cost,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
