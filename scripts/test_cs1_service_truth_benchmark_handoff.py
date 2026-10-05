#!/usr/bin/env python3
"""Regression contract for service-truth -> CS1 benchmark handoff."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

HANDOFF_PATH = SCRIPTS / "cs1_service_truth_benchmark.py"


def snapshot_sha256(content: object) -> str:
    payload = json.dumps(
        content,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def measured_row(index: int) -> dict:
    day = index + 1
    service_date = f"2026-10-{day:02d}"
    menu_snapshot = f"menu-{service_date}-lunch"
    calendar_snapshot = "calendar-2026-fall-v1"
    weather_snapshot = f"weather-forecast-{service_date}-0700"
    menu_content = {
        "service_date": service_date,
        "meal_period": "lunch",
        "items": ["lentil_soup", "rice", "seasonal_main"],
    }
    calendar_content = {"term": "2026-fall", "instructional_day": True}
    weather_content = {
        "forecast_for": f"{service_date}T12:00:00+03:00",
        "issued_at": f"{service_date}T07:00:00+03:00",
        "temperature_c": 18 + index,
        "precipitation_probability": 0.1,
    }
    return {
        "service_id": f"north-lunch-{service_date}",
        "granularity": "CAMPUS_MEAL_SERVICE",
        "service_date": service_date,
        "campus_id": "north",
        "meal_period": "lunch",
        "decision_cutoff_at": f"{service_date}T08:00:00+03:00",
        "actual_served": 100 + index,
        "produced_portions": 110 + index,
        "actual_surplus_portions": 10,
        "shortage_or_early_sellout": False,
        "outcome_reconciled": True,
        "outcome_source_record_id": f"ops-record-{index}",
        "operator_status_quo_quantity": 108 + index,
        "reservation_workflow_active": False,
        "evidence_class": "OFFICIAL_OPERATIONAL_EXPORT",
        "decision_inputs": [
            {
                "field": "menu",
                "snapshot_id": menu_snapshot,
                "snapshot_content": menu_content,
                "snapshot_sha256": snapshot_sha256(menu_content),
                "available_at": f"{service_date}T07:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
            {
                "field": "academic_calendar",
                "snapshot_id": calendar_snapshot,
                "snapshot_content": calendar_content,
                "snapshot_sha256": snapshot_sha256(calendar_content),
                "available_at": "2026-09-01T00:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
            {
                "field": "weather_forecast",
                "snapshot_id": weather_snapshot,
                "snapshot_content": weather_content,
                "snapshot_sha256": snapshot_sha256(weather_content),
                "available_at": f"{service_date}T07:00:00+03:00",
                "evidence_class": "OFFICIAL_SNAPSHOT",
            },
        ],
        "decision_audit": {
            "method_version": "operator-status-quo-v1",
            "recommended_quantity": 108 + index,
            "operator_action": "ACCEPT_RECOMMENDATION",
            "input_snapshot_ids": [menu_snapshot, calendar_snapshot, weather_snapshot],
        },
    }


def source_contract() -> dict:
    def entry(source_system: str, availability_semantics: str) -> dict:
        return {
            "owner": "DINING_OPERATIONS",
            "source_system": source_system,
            "availability_semantics": availability_semantics,
            "verification_status": "VERIFIED",
        }

    return {
        "actual_served": entry("SERVICE_EXPORT", "POST_SERVICE_RECONCILED"),
        "produced_portions": entry("PRODUCTION_LOG", "POST_PRODUCTION_RECORDED"),
        "surplus_or_waste": entry("SURPLUS_LOG", "POST_SERVICE_MEASURED"),
        "shortage_or_early_sellout": entry("SERVICE_STATUS", "POST_SERVICE_RECORDED"),
        "operator_status_quo_quantity": entry(
            "PRODUCTION_PLAN", "MUST_EXIST_BY_DECISION_CUTOFF"
        ),
        "menu": entry("OFFICIAL_MENU", "MUST_EXIST_BY_DECISION_CUTOFF"),
        "academic_calendar": {
            "owner": "UNIVERSITY",
            "source_system": "OFFICIAL_ACADEMIC_CALENDAR",
            "availability_semantics": "MUST_EXIST_BY_DECISION_CUTOFF",
            "verification_status": "VERIFIED",
        },
        "weather_forecast": {
            "owner": "ARCHIVED_FORECAST_PROVIDER",
            "source_system": "HISTORICAL_FORECAST_SNAPSHOT",
            "availability_semantics": "FORECAST_MUST_HAVE_BEEN_AVAILABLE_BY_DECISION_CUTOFF",
            "verification_status": "VERIFIED",
        },
    }


def load_handoff():
    assert HANDOFF_PATH.exists(), (
        "service-truth benchmark handoff module is required before measured "
        "artifacts can reach the baseline benchmark"
    )
    spec = importlib.util.spec_from_file_location("cs1_service_truth_benchmark", HANDOFF_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {HANDOFF_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_accepted_artifact_is_validated_sorted_and_checksum_bound() -> None:
    handoff = load_handoff()
    artifact = {
        "rows": [measured_row(2), measured_row(0), measured_row(1)],
        "field_provenance": source_contract(),
    }
    report = handoff.build_admitted_benchmark_report(
        artifact,
        dataset_id="north-lunch-measured-v1",
        dataset_label="North lunch measured services",
        git_commit_sha="a" * 40,
        rolling_window=2,
        seasonal_lag=1,
    )
    admission = report["service_truth_admission"]
    assert admission["validation_status"] == "ACCEPTED_FOR_OFFLINE_BENCHMARK"
    assert admission["eligible_for_benchmark"] is True
    assert report["reproducibility"]["dataset"]["sha256"] == admission[
        "dataset_validation"
    ]["artifact_checksum_sha256"]
    assert report["service_truth_series"]["service_ids"] == [
        "north-lunch-2026-10-01",
        "north-lunch-2026-10-02",
        "north-lunch-2026-10-03",
    ]
    assert report["result_scope"] == "OFFLINE_BENCHMARK_ONLY"
    assert "external-source accuracy" in report["claim_boundary"]


def test_explicit_series_selection_revalidates_only_selected_rows() -> None:
    handoff = load_handoff()
    north_rows = [measured_row(index) for index in range(3)]
    south_rows = []
    for index in range(3):
        row = json.loads(json.dumps(measured_row(index)))
        row["campus_id"] = "south"
        row["service_id"] = row["service_id"].replace("north-", "south-", 1)
        row["outcome_source_record_id"] = f"south-ops-record-{index}"
        south_rows.append(row)

    report = handoff.build_admitted_benchmark_report(
        {
            "rows": [
                south_rows[2], north_rows[1], south_rows[0],
                north_rows[2], north_rows[0], south_rows[1],
            ],
            "field_provenance": source_contract(),
        },
        dataset_id="north-lunch-selected-v1",
        dataset_label="North lunch selected series",
        git_commit_sha="b" * 40,
        rolling_window=2,
        seasonal_lag=1,
        campus_id="north",
        meal_period="lunch",
    )
    admission = report["service_truth_admission"]
    assert admission["dataset_validation"]["service_count"] == 3
    assert report["reproducibility"]["dataset"]["sha256"] == admission[
        "dataset_validation"
    ]["artifact_checksum_sha256"]


def test_unverified_source_contract_cannot_reach_measured_benchmark() -> None:
    handoff = load_handoff()
    provenance = source_contract()
    provenance["actual_served"]["verification_status"] = "UNVERIFIED"
    try:
        handoff.build_admitted_benchmark_report(
            {
                "rows": [measured_row(0), measured_row(1), measured_row(2)],
                "field_provenance": provenance,
            },
            dataset_id="unverified-source-v1",
            dataset_label="Unverified source must fail",
            git_commit_sha="c" * 40,
            rolling_window=2,
            seasonal_lag=1,
        )
    except ValueError as exc:
        assert "not eligible for offline benchmark" in str(exc)
    else:
        raise AssertionError("unverified source provenance reached measured benchmark")


def test_post_cutoff_snapshot_cannot_reach_measured_benchmark() -> None:
    handoff = load_handoff()
    rows = [measured_row(0), measured_row(1), measured_row(2)]
    rows[0]["decision_inputs"][0]["available_at"] = "2026-10-01T09:00:00+03:00"
    try:
        handoff.build_admitted_benchmark_report(
            {"rows": rows, "field_provenance": source_contract()},
            dataset_id="post-cutoff-v1",
            dataset_label="Post cutoff must fail",
            git_commit_sha="d" * 40,
            rolling_window=2,
            seasonal_lag=1,
        )
    except ValueError as exc:
        assert "not eligible for offline benchmark" in str(exc)
    else:
        raise AssertionError("post-cutoff snapshot reached measured benchmark")


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth benchmark handoff tests")
