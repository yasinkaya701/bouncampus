#!/usr/bin/env python3
"""Focused regressions for aggregate building-energy advisory planning."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/energy_advisory.py"
    if not path.exists():
        raise AssertionError("energy advisory policy missing")
    spec = importlib.util.spec_from_file_location("cs1_energy_advisory", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zone_modes_follow_registered_utilization_thresholds() -> None:
    policy = load_policy()
    result = policy.plan_energy_advisory(
        zones=[
            {"zone_id": "low", "capacity": 100, "occupancy_estimate": 10},
            {"zone_id": "mid", "capacity": 100, "occupancy_estimate": 50},
            {"zone_id": "high", "capacity": 100, "occupancy_estimate": 80},
        ],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    modes = {row["zone_id"]: row["recommended_mode"] for row in result["zones"]}
    assert modes == {
        "low": "SETBACK_REVIEW",
        "mid": "PARTIAL_LOAD_REVIEW",
        "high": "NORMAL_SERVICE_REVIEW",
    }
    assert result["operator_approval_required"] is True
    assert result["automatic_actuation"] is False
    assert result["energy_savings_claim_allowed"] is False


def test_impossible_zone_state_fails_closed() -> None:
    policy = load_policy()
    result = policy.plan_energy_advisory(
        zones=[{"zone_id": "bad", "capacity": 100, "occupancy_estimate": 101}],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["zones"] == []
    assert "OCCUPANCY_EXCEEDS_ZONE_CAPACITY" in result["reason_codes"]


def test_bad_thresholds_fail_closed() -> None:
    policy = load_policy()
    result = policy.plan_energy_advisory(
        zones=[{"zone_id": "z", "capacity": 100, "occupancy_estimate": 20}],
        low_utilization_threshold=0.70,
        medium_utilization_threshold=0.60,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert "INVALID_UTILIZATION_THRESHOLDS" in result["reason_codes"]


def test_output_contains_no_achieved_savings_fields() -> None:
    policy = load_policy()
    result = policy.plan_energy_advisory(
        zones=[{"zone_id": "z", "capacity": 100, "occupancy_estimate": 20}],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
    )
    serialized = repr(result).lower()
    for forbidden in ("energy_saved_kwh", "cost_saved", "co2_saved", "carbon_saved"):
        assert forbidden not in serialized
    assert "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM" in result["limitations"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} energy-advisory tests")
