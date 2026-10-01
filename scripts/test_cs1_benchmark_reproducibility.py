#!/usr/bin/env python3
"""Regression tests for CS1 benchmark reproducibility metadata."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_benchmark_module():
    path = ROOT / "scripts/cs1_baseline_benchmark.py"
    spec = importlib.util.spec_from_file_location("cs1_baseline_benchmark_repro", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows() -> list[dict[str, str]]:
    return [
        {"served": "100", "model": "102"},
        {"served": "110", "model": "108"},
        {"served": "120", "model": "119"},
        {"served": "130", "model": "131"},
    ]


def build(benchmark, *, model_version: str | None):
    return benchmark.build_report(
        rows(),
        dataset_label="fixture measured services",
        dataset_id="fixture-services-v1",
        dataset_provenance_class="MEASURED_OPERATIONAL",
        dataset_data_class="MEASURED",
        dataset_checksum_sha256="a" * 64,
        git_commit_sha="0123456789abcdef0123456789abcdef01234567",
        target_definition="served portions per service",
        decision_time_cutoff_rule="all features frozen before kitchen production decision",
        evaluation_window="fixture rows 1-4 in chronological order",
        actual_column="served",
        model_column="model",
        model_version=model_version,
        model_feature_ids=("schedule", "menu"),
        operator_column=None,
        rolling_window=2,
        seasonal_lag=2,
        excess_cost=1.0,
        shortage_cost=1.0,
    )


def test_complete_manifest_exposes_reproducibility_contract() -> None:
    benchmark = load_benchmark_module()
    report = build(benchmark, model_version="fixture-model-v1")
    manifest = report["reproducibility"]

    assert manifest["status"] == "COMPLETE"
    assert manifest["git_commit_sha"] == "0123456789abcdef0123456789abcdef01234567"
    assert manifest["dataset"]["id"] == "fixture-services-v1"
    assert manifest["dataset"]["sha256"] == "a" * 64
    assert manifest["dataset"]["data_class"] == "MEASURED"
    assert manifest["target_definition"] == "served portions per service"
    assert manifest["decision_time_cutoff_rule"].startswith("all features frozen")
    assert manifest["split_definition"] == "PAST_ONLY_COMMON_SUPPORT_SEQUENCE"
    assert manifest["method_versions"]["model"] == "fixture-model-v1"
    assert manifest["feature_ids_by_method"]["model"] == ["schedule", "menu"]
    assert manifest["eligibility_conclusion"] == "OFFLINE_EVALUATION_ONLY"


def test_unversioned_model_marks_manifest_incomplete_and_blocks_promotion() -> None:
    benchmark = load_benchmark_module()
    report = build(benchmark, model_version=None)
    manifest = report["reproducibility"]

    assert manifest["status"] == "INCOMPLETE"
    assert "MODEL_VERSION_UNAVAILABLE" in manifest["reason_codes"]
    assert manifest["method_versions"]["model"] is None
    assert manifest["eligibility_conclusion"] == "REVIEW_ONLY_REPRODUCIBILITY_INCOMPLETE"


def main() -> int:
    tests = [
        test_complete_manifest_exposes_reproducibility_contract,
        test_unversioned_model_marks_manifest_incomplete_and_blocks_promotion,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
