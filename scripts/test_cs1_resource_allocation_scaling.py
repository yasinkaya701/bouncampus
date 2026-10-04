#!/usr/bin/env python3
"""Regression gates for the scalable CS1 shared-capacity allocator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_allocator():
    path = ROOT / "backend/app/decision/resource_allocation.py"
    spec = importlib.util.spec_from_file_location("cs1_resource_allocation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def legacy_allocate(total_capacity: int, requests: list[dict]) -> tuple[dict[str, int], int]:
    rows = [{**row, "allocated": row["minimum"]} for row in requests]
    remaining = total_capacity - sum(row["minimum"] for row in rows)
    while remaining > 0:
        eligible = [row for row in rows if row["allocated"] < row["desired"]]
        if not eligible:
            break
        eligible.sort(
            key=lambda row: (
                -row["priority_weight"],
                -(row["desired"] - row["allocated"]),
                row["request_id"],
            )
        )
        eligible[0]["allocated"] += 1
        remaining -= 1
    return {row["request_id"]: row["allocated"] for row in rows}, remaining


def test_batched_allocator_matches_legacy_policy_on_small_cases() -> None:
    allocator = load_allocator()
    cases = [
        (
            10,
            [
                {"request_id": "study", "minimum": 2, "desired": 7, "priority_weight": 3},
                {"request_id": "charging", "minimum": 1, "desired": 5, "priority_weight": 1},
            ],
        ),
        (
            10,
            [
                {"request_id": "b", "minimum": 0, "desired": 5, "priority_weight": 1},
                {"request_id": "a", "minimum": 0, "desired": 5, "priority_weight": 1},
            ],
        ),
        (
            9,
            [
                {"request_id": "b", "minimum": 0, "desired": 5, "priority_weight": 1},
                {"request_id": "a", "minimum": 0, "desired": 4, "priority_weight": 1},
            ],
        ),
        (
            12,
            [
                {"request_id": "a", "minimum": 1, "desired": 8, "priority_weight": 2},
                {"request_id": "b", "minimum": 2, "desired": 9, "priority_weight": 2},
                {"request_id": "c", "minimum": 1, "desired": 4, "priority_weight": 1},
            ],
        ),
    ]
    for capacity, requests in cases:
        expected, expected_remaining = legacy_allocate(capacity, requests)
        result = allocator.allocate_shared_capacity(
            total_capacity=capacity,
            requests=requests,
        )
        actual = {row["request_id"]: row["allocated"] for row in result["allocations"]}
        assert actual == expected
        assert result["unallocated_capacity"] == expected_remaining


def test_billion_unit_capacity_is_allocated_without_unit_iteration() -> None:
    allocator = load_allocator()
    result = allocator.allocate_shared_capacity(
        total_capacity=1_000_000_000,
        requests=[
            {"request_id": "a", "minimum": 0, "desired": 400_000_000, "priority_weight": 2},
            {"request_id": "b", "minimum": 0, "desired": 400_000_000, "priority_weight": 2},
            {"request_id": "c", "minimum": 0, "desired": 400_000_000, "priority_weight": 1},
        ],
    )
    actual = {row["request_id"]: row["allocated"] for row in result["allocations"]}
    assert actual == {"a": 400_000_000, "b": 400_000_000, "c": 200_000_000}
    assert result["unallocated_capacity"] == 0
    assert result["allocation_semantics"] == "PRIORITY_FIRST_LARGEST_UNMET_GAP_BATCHED"


def test_invalid_minimums_fail_closed() -> None:
    allocator = load_allocator()
    result = allocator.allocate_shared_capacity(
        total_capacity=4,
        requests=[
            {"request_id": "a", "minimum": 3, "desired": 3, "priority_weight": 1},
            {"request_id": "b", "minimum": 2, "desired": 2, "priority_weight": 1},
        ],
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["allocations"] == []
    assert "REGISTERED_MINIMUMS_EXCEED_AVAILABLE_CAPACITY" in result["reason_codes"]


def test_api_and_orchestrator_route_to_scalable_allocator() -> None:
    router = (ROOT / "backend/app/routers/campus_ops.py").read_text(encoding="utf-8")
    orchestrator = (ROOT / "backend/app/decision/campus_orchestrator.py").read_text(encoding="utf-8")
    expected = "from app.decision.resource_allocation import allocate_shared_capacity"
    assert expected in router
    assert expected in orchestrator


def main() -> int:
    tests = [
        test_batched_allocator_matches_legacy_policy_on_small_cases,
        test_billion_unit_capacity_is_allocated_without_unit_iteration,
        test_invalid_minimums_fail_closed,
        test_api_and_orchestrator_route_to_scalable_allocator,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
