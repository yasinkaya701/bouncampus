#!/usr/bin/env python3
"""Regression tests for aggregate shared-capacity allocation."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    path = ROOT / "backend/app/decision/shared_capacity_policy.py"
    if not path.exists():
        raise AssertionError("shared-capacity policy missing")
    spec = importlib.util.spec_from_file_location("cs1_shared_capacity_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def allocate(policy, **overrides):
    kwargs = {
        "total_capacity": 10,
        "capacity_provenance": "OFFICIAL_SNAPSHOT",
        "requests": [
            {"request_id": "study", "minimum": 2, "desired": 7, "priority_weight": 3},
            {"request_id": "charging", "minimum": 1, "desired": 5, "priority_weight": 1},
        ],
    }
    kwargs.update(overrides)
    return policy.allocate_shared_capacity(**kwargs)


def test_minimums_then_registered_priority_fill_verified_capacity() -> None:
    policy = load_policy()
    result = allocate(policy)
    allocations = {row["request_id"]: row["allocated"] for row in result["allocations"]}
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert sum(allocations.values()) == 10
    assert allocations["study"] == 7
    assert allocations["charging"] == 3
    assert result["capacity_provenance"] == "OFFICIAL_SNAPSHOT"
    assert result["capacity_semantics"] == "VERIFIED_AGGREGATE_RESOURCE_INVENTORY"
    assert result["automatic_execution_allowed"] is False


def test_unverified_capacity_fails_closed() -> None:
    policy = load_policy()
    for provenance in ("MODEL_ESTIMATE", "POLICY_HEURISTIC", "UNAVAILABLE"):
        result = allocate(policy, capacity_provenance=provenance)
        assert result["decision_readiness"] == "WITHHOLD"
        assert result["allocations"] == []
        assert result["capacity_provenance"] == provenance
        assert "UNVERIFIED_SHARED_CAPACITY" in result["reason_codes"]


def test_minimums_above_capacity_fail_closed() -> None:
    policy = load_policy()
    result = allocate(
        policy,
        total_capacity=4,
        requests=[
            {"request_id": "a", "minimum": 3, "desired": 3, "priority_weight": 1},
            {"request_id": "b", "minimum": 2, "desired": 2, "priority_weight": 1},
        ],
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["allocations"] == []
    assert "REQUEST_MINIMUMS_EXCEED_SHARED_CAPACITY" in result["reason_codes"]


def test_malformed_request_fails_closed() -> None:
    policy = load_policy()
    result = allocate(
        policy,
        requests=[{"request_id": "a", "minimum": 4, "desired": 2, "priority_weight": 1}],
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["allocations"] == []


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} shared-capacity policy tests")
