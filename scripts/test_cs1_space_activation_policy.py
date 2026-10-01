#!/usr/bin/env python3
"""Regression tests for aggregate CS1 space/zone activation planning."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/space_activation_policy.py"
    if not path.exists():
        raise AssertionError("space activation policy missing")
    spec = importlib.util.spec_from_file_location("cs1_space_activation_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scenarios():
    return [
        {"demand": 60, "weight": 0.25},
        {"demand": 80, "weight": 0.50},
        {"demand": 100, "weight": 0.25},
    ]


def zones():
    return [
        {"zone_id": "L1", "capacity": 60, "activation_weight": 2.0},
        {"zone_id": "L2", "capacity": 50, "activation_weight": 1.0},
        {"zone_id": "L3", "capacity": 40, "activation_weight": 0.5},
    ]


def test_selects_low_registered_loss_zone_bundle_without_energy_savings_claim() -> None:
    policy = load_policy()
    result = policy.plan_space_activation(
        occupancy_scenarios=scenarios(),
        zones=zones(),
        idle_capacity_weight=0.5,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
        zone_inventory_provenance="OFFICIAL_SNAPSHOT",
        occupancy_provenance="MODEL_ESTIMATE",
        upstream_readiness="REVIEW_REQUIRED",
    )
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["selected_zone_ids"] == ["L1", "L3"]
    assert result["selected_capacity"] == 100
    assert result["zone_inventory_provenance"] == "OFFICIAL_SNAPSHOT"
    assert result["occupancy_provenance"] == "MODEL_ESTIMATE"
    assert result["energy_savings_claim_allowed"] is False
    assert result["automatic_execution_allowed"] is False
    assert result["operator_approval_required"] is True


def test_withholds_unverified_zone_capacity() -> None:
    policy = load_policy()
    result = policy.plan_space_activation(
        occupancy_scenarios=scenarios(),
        zones=zones(),
        idle_capacity_weight=0.5,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
        zone_inventory_provenance="MODEL_ESTIMATE",
        occupancy_provenance="MODEL_ESTIMATE",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["selected_zone_ids"] == []
    assert "UNVERIFIED_ZONE_INVENTORY" in result["reason_codes"]


def test_withholds_when_full_capacity_cannot_meet_registered_service_floor() -> None:
    policy = load_policy()
    result = policy.plan_space_activation(
        occupancy_scenarios=[{"demand": 120, "weight": 1.0}],
        zones=[{"zone_id": "L1", "capacity": 80, "activation_weight": 1.0}],
        idle_capacity_weight=1.0,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
        zone_inventory_provenance="OFFICIAL_SNAPSHOT",
        occupancy_provenance="MODEL_ESTIMATE",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["selected_zone_ids"] == []
    assert result["selected_capacity"] == 80
    assert "SPACE_CAPACITY_BELOW_REGISTERED_SERVICE_FLOOR" in result["reason_codes"]


def test_withholds_sandbox_or_unavailable_occupancy_evidence() -> None:
    policy = load_policy()
    for provenance in ("GENERATED_SANDBOX", "UNAVAILABLE"):
        result = policy.plan_space_activation(
            occupancy_scenarios=scenarios(),
            zones=zones(),
            idle_capacity_weight=0.5,
            shortage_weight=4.0,
            min_point_service_ratio=0.9,
            zone_inventory_provenance="OFFICIAL_SNAPSHOT",
            occupancy_provenance=provenance,
        )
        assert result["decision_readiness"] == "WITHHOLD"
        assert result["selected_zone_ids"] == []
        assert "OCCUPANCY_EVIDENCE_NOT_ACTIONABLE" in result["reason_codes"]


def test_upstream_withhold_propagates_without_zone_recommendation() -> None:
    policy = load_policy()
    result = policy.plan_space_activation(
        occupancy_scenarios=scenarios(),
        zones=zones(),
        idle_capacity_weight=0.5,
        shortage_weight=4.0,
        min_point_service_ratio=0.9,
        zone_inventory_provenance="OFFICIAL_SNAPSHOT",
        occupancy_provenance="MODEL_ESTIMATE",
        upstream_readiness="WITHHOLD",
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["selected_zone_ids"] == []
    assert "UPSTREAM_CAMPUS_STATE_WITHHELD" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} space-activation policy tests")
