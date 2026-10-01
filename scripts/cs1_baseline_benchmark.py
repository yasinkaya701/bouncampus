#!/usr/bin/env python3
"""Benchmark CS1 food-demand candidates against leakage-safe baselines.

This script never invents observations. It requires a measured or explicitly labeled
CSV dataset supplied by the caller and reports offline forecast/decision metrics only.
Reservation counts are treated as intent signals, never as served demand.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.baselines import compare_forecasts, generate_naive_baselines  # noqa: E402
from app.decision.reservation import (  # noqa: E402
    compare_decision_policies,
    generate_reservation_baselines,
)

DATASET_PROVENANCE_CLASSES = (
    "OFFICIAL_PUBLIC",
    "MEASURED_OPERATIONAL",
    "GENERATED_SANDBOX",
)
DATASET_DATA_CLASSES = ("MEASURED", "GENERATED", "MIXED")


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


def _require_text(value: str, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _validate_hex(value: str, *, name: str, lengths: set[int]) -> str:
    normalized = _require_text(value, name=name).lower()
    if len(normalized) not in lengths or any(
        character not in "0123456789abcdef" for character in normalized
    ):
        lengths_text = "/".join(str(length) for length in sorted(lengths))
        raise ValueError(f"{name} must be a {lengths_text}-character hexadecimal value")
    return normalized


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_git_commit_sha(explicit: str | None = None) -> str | None:
    candidates = [explicit, os.environ.get("GITHUB_SHA")]
    for candidate in candidates:
        if candidate:
            try:
                return _validate_hex(candidate, name="git_commit_sha", lengths={40, 64})
            except ValueError:
                continue

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    candidate = result.stdout.strip()
    try:
        return _validate_hex(candidate, name="git_commit_sha", lengths={40, 64})
    except ValueError:
        return None


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        return list(reader)


def _normalized_feature_ids(values: Sequence[str] | None) -> list[str] | None:
    if values is None:
        return None
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _require_text(value, name="model_feature_id")
        if text not in seen:
            normalized.append(text)
            seen.add(text)
    return normalized or None


def build_reproducibility_manifest(
    *,
    dataset_label: str,
    dataset_id: str,
    dataset_provenance_class: str,
    dataset_data_class: str,
    dataset_checksum_sha256: str,
    git_commit_sha: str,
    target_definition: str,
    decision_time_cutoff_rule: str,
    evaluation_window: str,
    forecasts: dict[str, list[float | None]],
    comparison: dict[str, object],
    actual_column: str,
    model_column: str | None,
    model_version: str | None,
    model_feature_ids: Sequence[str] | None,
    operator_column: str | None,
    reservation_column: str | None,
    reserved_served_column: str | None,
    unreserved_column: str | None,
) -> dict[str, object]:
    dataset_label = _require_text(dataset_label, name="dataset_label")
    dataset_id = _require_text(dataset_id, name="dataset_id")
    target_definition = _require_text(target_definition, name="target_definition")
    decision_time_cutoff_rule = _require_text(
        decision_time_cutoff_rule,
        name="decision_time_cutoff_rule",
    )
    evaluation_window = _require_text(evaluation_window, name="evaluation_window")
    dataset_checksum_sha256 = _validate_hex(
        dataset_checksum_sha256,
        name="dataset_checksum_sha256",
        lengths={64},
    )
    git_commit_sha = _validate_hex(
        git_commit_sha,
        name="git_commit_sha",
        lengths={40, 64},
    )
    if dataset_provenance_class not in DATASET_PROVENANCE_CLASSES:
        raise ValueError(
            "dataset_provenance_class must be one of "
            f"{DATASET_PROVENANCE_CLASSES!r}"
        )
    if dataset_data_class not in DATASET_DATA_CLASSES:
        raise ValueError(f"dataset_data_class must be one of {DATASET_DATA_CLASSES!r}")
    if (
        dataset_provenance_class == "GENERATED_SANDBOX"
        and dataset_data_class != "GENERATED"
    ):
        raise ValueError("GENERATED_SANDBOX provenance requires GENERATED data class")
    if (
        dataset_data_class == "GENERATED"
        and dataset_provenance_class != "GENERATED_SANDBOX"
    ):
        raise ValueError("GENERATED data must use GENERATED_SANDBOX provenance")

    normalized_model_features = _normalized_feature_ids(model_feature_ids)
    method_versions: dict[str, str | None] = {}
    feature_ids_by_method: dict[str, list[str] | None] = {}
    reason_codes: list[str] = []

    for method_id in forecasts:
        if method_id == "model":
            version = model_version.strip() if model_version and model_version.strip() else None
            method_versions[method_id] = version
            feature_ids_by_method[method_id] = normalized_model_features
            if version is None:
                reason_codes.append("MODEL_VERSION_UNAVAILABLE")
            if normalized_model_features is None:
                reason_codes.append("MODEL_FEATURE_IDS_UNAVAILABLE")
        elif method_id == "operator":
            method_versions[method_id] = "OPERATOR_ESTIMATE_INPUT_V1"
            feature_ids_by_method[method_id] = ["OPERATOR_JUDGMENT"]
        elif method_id in {"raw_reservation", "corrected_reservation"}:
            method_versions[method_id] = "CS1_RESERVATION_BASELINES_V1"
            feature_ids_by_method[method_id] = (
                ["active_reservations_at_cutoff"]
                if method_id == "raw_reservation"
                else [
                    "active_reservations_at_cutoff",
                    "historical_reserved_show_rate",
                    "historical_unreserved_demand",
                ]
            )
        else:
            method_versions[method_id] = "CS1_NAIVE_BASELINES_V1"
            feature_ids_by_method[method_id] = ["historical_actual"]

    metrics_mapping = comparison.get("metrics")
    metric_names: list[str] = []
    if isinstance(metrics_mapping, dict):
        names: set[str] = set()
        for metric_result in metrics_mapping.values():
            if isinstance(metric_result, dict):
                names.update(str(name) for name in metric_result)
        metric_names = sorted(names)

    status = "COMPLETE" if not reason_codes else "INCOMPLETE"
    if dataset_data_class == "GENERATED":
        eligibility_conclusion = "SANDBOX_ONLY"
    elif reason_codes:
        eligibility_conclusion = "REVIEW_ONLY_REPRODUCIBILITY_INCOMPLETE"
    else:
        eligibility_conclusion = "OFFLINE_EVALUATION_ONLY"

    return {
        "status": status,
        "reason_codes": reason_codes,
        "git_commit_sha": git_commit_sha,
        "dataset": {
            "id": dataset_id,
            "label": dataset_label,
            "provenance_class": dataset_provenance_class,
            "data_class": dataset_data_class,
            "sha256": dataset_checksum_sha256,
        },
        "target_definition": target_definition,
        "actual_column": actual_column,
        "decision_time_cutoff_rule": decision_time_cutoff_rule,
        "split_definition": "PAST_ONLY_COMMON_SUPPORT_SEQUENCE",
        "evaluation_window": evaluation_window,
        "method_ids": list(forecasts),
        "method_versions": method_versions,
        "feature_ids_by_method": feature_ids_by_method,
        "baseline_ids": [
            method_id for method_id in forecasts if method_id not in {"model", "operator"}
        ],
        "evaluation_metric_fields": metric_names,
        "input_columns": {
            "actual": actual_column,
            "model_forecast": model_column,
            "operator_forecast": operator_column,
            "active_reservations_at_cutoff": reservation_column,
            "reserved_served_demand": reserved_served_column,
            "unreserved_demand": unreserved_column,
        },
        "exclusions_and_missingness": {
            "common_support_n": comparison.get("common_support_n"),
            "common_support_pct": comparison.get("common_support_pct"),
            "evaluation_indices": comparison.get("evaluation_indices"),
            "available_n_by_method": comparison.get("available_n_by_method"),
        },
        "eligibility_conclusion": eligibility_conclusion,
        "claim_boundary": (
            "This manifest supports reproducibility and offline evaluation only; "
            "it does not establish pilot eligibility or achieved impact."
        ),
    }


def build_report(
    rows: list[dict[str, str]],
    *,
    dataset_label: str,
    dataset_id: str,
    dataset_provenance_class: str,
    dataset_data_class: str,
    dataset_checksum_sha256: str,
    git_commit_sha: str,
    target_definition: str,
    decision_time_cutoff_rule: str,
    evaluation_window: str,
    actual_column: str,
    model_column: str | None,
    model_version: str | None,
    model_feature_ids: Sequence[str] | None,
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
    reproducibility = build_reproducibility_manifest(
        dataset_label=dataset_label,
        dataset_id=dataset_id,
        dataset_provenance_class=dataset_provenance_class,
        dataset_data_class=dataset_data_class,
        dataset_checksum_sha256=dataset_checksum_sha256,
        git_commit_sha=git_commit_sha,
        target_definition=target_definition,
        decision_time_cutoff_rule=decision_time_cutoff_rule,
        evaluation_window=evaluation_window,
        forecasts=forecasts,
        comparison=comparison,
        actual_column=actual_column,
        model_column=model_column,
        model_version=model_version,
        model_feature_ids=model_feature_ids,
        operator_column=operator_column,
        reservation_column=reservation_column,
        reserved_served_column=reserved_served_column,
        unreserved_column=unreserved_column,
    )

    return {
        "schema_version": 3,
        "dataset_label": dataset_label,
        "row_count": len(rows),
        "actual_column": actual_column,
        "forecast_candidates": list(forecasts),
        "evaluation": comparison,
        "decision_evaluation": decision_evaluation,
        "reservation_reconciliation": reservation_reconciliation,
        "reproducibility": reproducibility,
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
    parser.add_argument("--dataset-id", required=True, help="stable dataset/artifact identifier")
    parser.add_argument(
        "--dataset-provenance-class",
        required=True,
        choices=DATASET_PROVENANCE_CLASSES,
    )
    parser.add_argument(
        "--dataset-data-class",
        required=True,
        choices=DATASET_DATA_CLASSES,
        help="MEASURED, GENERATED, or MIXED",
    )
    parser.add_argument(
        "--target-definition",
        required=True,
        help="semantic target definition, not merely a column name",
    )
    parser.add_argument(
        "--decision-time-cutoff-rule",
        required=True,
        help="rule defining what information is allowed before the decision",
    )
    parser.add_argument(
        "--evaluation-window",
        required=True,
        help="human-readable chronological evaluation window",
    )
    parser.add_argument(
        "--git-commit-sha",
        default=None,
        help="optional explicit git SHA; otherwise GITHUB_SHA/git rev-parse is used",
    )
    parser.add_argument("--actual-column", default="served_portions")
    parser.add_argument("--model-column", default="model_forecast_meals")
    parser.add_argument("--model-version", default=None)
    parser.add_argument(
        "--model-feature-id",
        action="append",
        dest="model_feature_ids",
        default=None,
        help="repeat for every feature used by the precomputed model forecast",
    )
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

    git_commit_sha = resolve_git_commit_sha(args.git_commit_sha)
    if git_commit_sha is None:
        print(
            "ERROR: git commit SHA unavailable; pass --git-commit-sha explicitly",
            file=sys.stderr,
        )
        return 2

    try:
        report = build_report(
            load_rows(args.csv),
            dataset_label=args.dataset_label,
            dataset_id=args.dataset_id,
            dataset_provenance_class=args.dataset_provenance_class,
            dataset_data_class=args.dataset_data_class,
            dataset_checksum_sha256=sha256_file(args.csv),
            git_commit_sha=git_commit_sha,
            target_definition=args.target_definition,
            decision_time_cutoff_rule=args.decision_time_cutoff_rule,
            evaluation_window=args.evaluation_window,
            actual_column=args.actual_column,
            model_column=args.model_column,
            model_version=args.model_version,
            model_feature_ids=args.model_feature_ids,
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
