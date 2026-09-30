#!/usr/bin/env python3
"""Benchmark CS1 food-demand forecasts against leakage-safe naive baselines.

This script never invents observations. It requires a measured or explicitly labeled
CSV dataset supplied by the caller and reports offline forecast metrics only.
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

    comparison = compare_forecasts(actual, forecasts)
    return {
        "schema_version": 1,
        "dataset_label": dataset_label,
        "row_count": len(rows),
        "actual_column": actual_column,
        "forecast_candidates": list(forecasts),
        "evaluation": comparison,
        "evidence_class": "TECH_TEST",
        "result_scope": "OFFLINE_BENCHMARK_ONLY",
        "leakage_policy": "Naive baselines use only observations before each target row.",
        "claim_boundary": (
            "Forecast benchmark metrics may support model-selection claims only. "
            "They do not demonstrate food-waste, cost, carbon, or water savings."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, type=Path, help="measured/labeled service-level CSV")
    parser.add_argument("--dataset-label", required=True, help="human-readable dataset provenance label")
    parser.add_argument("--actual-column", default="served_portions")
    parser.add_argument("--model-column", default="model_forecast_meals")
    parser.add_argument("--operator-column", default=None)
    parser.add_argument("--rolling-window", type=int, default=3)
    parser.add_argument("--seasonal-lag", type=int, default=7)
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
