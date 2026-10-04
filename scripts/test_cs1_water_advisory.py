#!/usr/bin/env python3
"""Focused regressions for aggregate campus water-use advisory planning."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/water_advisory.py"
    if not path.exists():
        raise AssertionError("water advisory policy missing")
    spec = importlib.util.spec_from_file_location("cs1_water_advisory", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_water_use_modes_follow_registered_ratio_thresholds() -> None:
    policy = load_policy()
    result = policy.plan_water_advisory(
        zones=[
            {"zone_id": "normal", "expected_liters": 1000, "observed_liters": 1050},
            {"zone_id": "elevated", "expected_liters": 1000, "observed_liters": 1300},
            {"zone_id": "critical", "expected_liters": 1000, "observed_liters": 1800},
        ],
        elevated_ratio_threshold=1.20,
        critical_ratio_threshold=1.50,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    modes = {row["zone_id"]: row["recommended_mode"] for row in result["zones"]}
    assert modes == {
        "normal": "NORMAL_USE_REVIEW",
        "elevated": "ELEVATED_USE_REVIEW",
        "critical": "LEAK_OR_OPERATIONAL_ANOMALY_REVIEW",
    }
    assert result["automatic_valve_actuation"] is False
    assert result["water_savings_claim_allowed"] is False


def test_invalid_or_zero_expected_baseline_fails_closed() -> None:
    policy = load_policy()
    result = policy.plan_water_advisory(
        zones=[{"zone_id": "bad", "expected_liters": 0, "observed_liters": 100}],
        elevated_ratio_threshold=1.20,
        critical_ratio_threshold=1.50,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["zones"] == []
    assert "INVALID_WATER_ZONE" in result["reason_codes"]


def test_threshold_order_must_be_explicit_and_valid() -> None:
    policy = load_policy()
    result = policy.plan_water_advisory(
        zones=[{"zone_id": "z", "expected_liters": 100, "observed_liters": 100}],
        elevated_ratio_threshold=1.60,
        critical_ratio_threshold=1.50,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert "INVALID_WATER_RATIO_THRESHOLDS" in result["reason_codes"]


def test_output_contains_no_achieved_water_savings_claim() -> None:
    policy = load_policy()
    result = policy.plan_water_advisory(
        zones=[{"zone_id": "z", "expected_liters": 100, "observed_liters": 140}],
        elevated_ratio_threshold=1.20,
        critical_ratio_threshold=1.50,
    )
    serialized = repr(result).lower()
    for forbidden in ("water_saved", "liters_saved", "cost_saved"):
        assert forbidden not in serialized
    assert "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM" in result["limitations"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} water-advisory tests")
