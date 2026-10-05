#!/usr/bin/env python3
"""Bridge admitted CS1 service-truth artifacts into the offline baseline benchmark.

This module intentionally re-runs the service-truth artifact admission in-process.
A caller-provided label or fingerprint is not enough to enter the measured benchmark.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.service_truth import validate_service_truth_artifact  # noqa: E402
from cs1_baseline_benchmark import build_report  # noqa: E402


def _require_mapping(value: object, *, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_rows(value: object) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError("artifact rows must be a sequence")
    rows: list[Mapping[str, Any]] = []
    for index, row in enumerate(value):
        if not isinstance(row, Mapping):
            raise ValueError(f"artifact row {index} must be a mapping")
        rows.append(row)
    return rows


def _series_key(row: Mapping[str, Any]) -> tuple[str, str]:
    campus_id = row.get("campus_id")
    meal_period = row.get("meal_period")
    if not isinstance(campus_id, str) or not campus_id.strip():
        raise ValueError("admitted row is missing campus_id")
    if not isinstance(meal_period, str) or not meal_period.strip():
        raise ValueError("admitted row is missing meal_period")
    return campus_id.strip(), meal_period.strip()


def _chronological_key(row: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(row.get("service_date", "")),
        str(row.get("decision_cutoff_at", "")),
        str(row.get("service_id", "")),
    )


def _csv_number(value: object, *, name: str) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric in admitted service truth")
    return str(value)


def build_admitted_benchmark_report(
    artifact: Mapping[str, Any],
    *,
    dataset_id: str,
    dataset_label: str,
    git_commit_sha: str,
    rolling_window: int,
    seasonal_lag: int,
    campus_id: str | None = None,
    meal_period: str | None = None,
    excess_cost: float = 1.0,
    shortage_cost: float = 1.0,
) -> dict[str, object]:
    """Validate and benchmark one admitted campus x meal-period service series."""

    artifact = _require_mapping(artifact, name="artifact")
    rows = _require_rows(artifact.get("rows"))
    field_provenance = _require_mapping(
        artifact.get("field_provenance"),
        name="artifact field_provenance",
    )

    if (campus_id is None) != (meal_period is None):
        raise ValueError("campus_id and meal_period must be provided together")

    available_series = {_series_key(row) for row in rows}
    if campus_id is None and meal_period is None:
        if len(available_series) != 1:
            raise ValueError(
                "multiple campus/meal series require explicit campus_id and meal_period"
            )
        selected_key = next(iter(available_series))
    else:
        assert campus_id is not None and meal_period is not None
        selected_key = (campus_id.strip(), meal_period.strip())
        if selected_key not in available_series:
            raise ValueError("requested campus_id and meal_period are absent from artifact")

    selected_rows = sorted(
        (row for row in rows if _series_key(row) == selected_key),
        key=_chronological_key,
    )
    if not selected_rows:
        raise ValueError("selected service-truth series is empty")

    # Admission must bind the exact rows that enter the benchmark. Validating a
    # larger multi-series container and then filtering would make the manifest
    # checksum describe data that the benchmark did not actually evaluate.
    admission = validate_service_truth_artifact(
        selected_rows,
        field_provenance=field_provenance,
    )
    if (
        admission.get("validation_status") != "ACCEPTED_FOR_OFFLINE_BENCHMARK"
        or admission.get("eligible_for_benchmark") is not True
    ):
        reasons = admission.get("reason_codes") or []
        raise ValueError(
            "selected service-truth series is not eligible for offline benchmark: "
            + ", ".join(str(reason) for reason in reasons)
        )

    benchmark_rows = [
        {
            "actual_served": _csv_number(
                row.get("actual_served"),
                name="actual_served",
            ),
            "operator_status_quo_quantity": _csv_number(
                row.get("operator_status_quo_quantity"),
                name="operator_status_quo_quantity",
            ),
        }
        for row in selected_rows
    ]

    first_date = str(selected_rows[0]["service_date"])
    last_date = str(selected_rows[-1]["service_date"])
    dataset_validation = _require_mapping(
        admission.get("dataset_validation"),
        name="admission dataset_validation",
    )
    dataset_checksum = dataset_validation.get("artifact_checksum_sha256")
    if not isinstance(dataset_checksum, str) or not dataset_checksum:
        raise ValueError("admission did not provide artifact checksum")

    report = build_report(
        benchmark_rows,
        dataset_label=dataset_label,
        dataset_id=dataset_id,
        dataset_provenance_class="MEASURED_OPERATIONAL",
        dataset_data_class="MEASURED",
        dataset_checksum_sha256=dataset_checksum,
        git_commit_sha=git_commit_sha,
        target_definition="actual_served per campus x meal_period x service_date",
        decision_time_cutoff_rule="SERVICE_TRUTH_DECISION_CUTOFF_AT_PER_ROW",
        evaluation_window=f"{first_date}..{last_date}",
        actual_column="actual_served",
        model_column=None,
        model_version=None,
        model_feature_ids=None,
        operator_column="operator_status_quo_quantity",
        rolling_window=rolling_window,
        seasonal_lag=seasonal_lag,
        excess_cost=excess_cost,
        shortage_cost=shortage_cost,
    )

    report["service_truth_admission"] = admission
    report["service_truth_series"] = {
        "campus_id": selected_key[0],
        "meal_period": selected_key[1],
        "service_count": len(selected_rows),
        "service_ids": [str(row["service_id"]) for row in selected_rows],
    }
    report["claim_boundary"] = (
        "This is an offline benchmark over a selected service-truth series admitted "
        "for structural, provenance, cutoff, and canonical-content integrity checks. "
        "Admission does not prove external-source accuracy, model value, pilot "
        "readiness, operational impact, savings, or automatic-action readiness."
    )
    return report
