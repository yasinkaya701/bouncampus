#!/usr/bin/env python3
"""Regression tests for CS1 policy-sensitivity gating."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_high_target_span_requires_review() -> None:
    sensitivity = load_module(
        "policy_sensitivity",
        "backend/app/decision/policy_sensitivity.py",
    )
    report = sensitivity.assess_policy_sensitivity(
        1000,
        [
            {
                "scenario_id": "balanced",
                "target": 1000,
                "shortage_weight": 1.0,
                "excess_weight": 1.0,
                "buffer_pct": 0.0,
            },
            {
                "scenario_id": "shortage-averse",
                "target": 1120,
                "shortage_weight": 2.0,
                "excess_weight": 1.0,
                "buffer_pct": 12.0,
            },
            {
                "scenario_id": "excess-averse",
                "target": 930,
                "shortage_weight": 1.0,
                "excess_weight": 2.0,
                "buffer_pct": -7.0,
            },
        ],
        max_relative_target_span_pct=10.0,
        policy_version="food-policy-v1",
    )

    assert report["sensitivity_state"] == "HIGH"
    assert report["readiness_effect"] == "REVIEW_REQUIRED"
    assert math.isclose(report["relative_target_span_pct"], 19.0, rel_tol=1e-9)
    assert report["parameter_provenance"] == "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS"
    assert report["selected_operational_target"] is None
    assert "POLICY_SENSITIVITY_HIGH" in report["reason_codes"]


def test_invalid_scenario_fails_closed() -> None:
    sensitivity = load_module(
        "policy_sensitivity_invalid",
        "backend/app/decision/policy_sensitivity.py",
    )
    report = sensitivity.assess_policy_sensitivity(
        1000,
        [
            {
                "scenario_id": "balanced",
                "target": 1000,
                "shortage_weight": 1.0,
                "excess_weight": 1.0,
                "buffer_pct": 0.0,
            },
            {
                "scenario_id": "broken",
                "target": float("nan"),
                "shortage_weight": 1.0,
                "excess_weight": 1.0,
                "buffer_pct": 0.0,
            },
        ],
        max_relative_target_span_pct=10.0,
        policy_version="food-policy-v1",
    )

    assert report["sensitivity_state"] == "WITHHOLD"
    assert report["readiness_effect"] == "WITHHOLD"
    assert report["selected_operational_target"] is None
    assert report["relative_target_span_pct"] is None
    assert "INVALID_POLICY_SENSITIVITY_SCENARIO" in report["reason_codes"]


def main() -> int:
    tests = [
        test_high_target_span_requires_review,
        test_invalid_scenario_fails_closed,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
