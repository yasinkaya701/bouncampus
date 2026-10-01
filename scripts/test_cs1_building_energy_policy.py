#!/usr/bin/env python3
"""Regression tests for aggregate building-energy operating recommendations."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/building_energy_policy.py"
    if not path.exists():
        raise AssertionError("building-energy policy missing")
    spec = importlib.util.spec_from_file_location("cs1_building_energy_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zone_modes_follow_registered_utilization_thresholds() -> None:
    policy = load_policy()
    result = policy.plan_building_energy(
        zones=[
            {"zone_id": "Z-low", "capacity": 100, "occupancy_estimate": 10},
            {"zone_id": "Z-mid", "capacity": 100, "occupancy_estimate": 50},
            {"zone_id": "Z-high", "capacity": 100, "occupancy_estimate": 80},
        ],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
    )
    modes = {row["zone_id"]: row["recommended_mode"] for row in result["zones"]}
    assert modes == {
        "Z-low": "SETBACK_REVIEW",
        "Z-mid": "PARTIAL_LOAD_REVIEW",
        "Z-high": "NORMAL_SERVICE_REVIEW",
    }
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True


def test_occupancy_above_capacity_fails_closed() -> None:
    policy = load_policy()
    result = policy.plan_building_energy(
        zones=[{"zone_id": "Z1", "capacity": 100, "occupancy_estimate": 120}],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["zones"] == []
    assert "OCCUPANCY_EXCEEDS_ZONE_CAPACITY" in result["reason_codes"]


def test_upstream_withhold_propagates() -> None:
    policy = load_policy()
    result = policy.plan_building_energy(
        zones=[{"zone_id": "Z1", "capacity": 100, "occupancy_estimate": 20}],
        low_utilization_threshold=0.25,
        medium_utilization_threshold=0.60,
        upstream_readiness="WITHHOLD",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["zones"] == []
    assert "UPSTREAM_CAMPUS_STATE_WITHHELD" in result["reason_codes"]


def test_energy_policy_does_not_claim_achieved_savings() -> None:
    policy = load_policy()
    result = policy.plan_building_energy(
        zones=[{"zone_id": "Z1", "capacity": 100, "occupancy_estimate": 20}],
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
    print(f"ok: {len(tests)} building-energy policy tests")
