#!/usr/bin/env python3
"""Focused regression tests for the CS1 food decision policy."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "backend/app/optimizers/food_optimizer.py"

spec = importlib.util.spec_from_file_location("food_optimizer", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"could not load {MODULE_PATH}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FoodOptimizer = module.FoodOptimizer


def assert_claim_firewall(result: dict) -> None:
    forbidden = {"waste_reduction", "potential_waste_saved_kg", "cost_saved_tl"}
    leaked = forbidden.intersection(result)
    assert not leaked, f"pre-pilot impact fields leaked from decision policy: {sorted(leaked)}"
    assert result["policy_provenance"] == "POLICY_HEURISTIC"
    assert result["operator_approval_required"] is True
    assert result["automatic_kitchen_dispatch"] is False
    assert "HEURISTIC_BAND_NOT_CALIBRATED" in result["reason_codes"]


def test_withholds_without_schedule_backbone() -> None:
    result = FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        1000,
        [],
        signal_availability={"schedule": False, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended"] is None
    assert "MISSING_SCHEDULE_BACKBONE" in result["reason_codes"]


def test_requires_review_when_menu_context_is_missing() -> None:
    result = FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        1000,
        [],
        signal_availability={"schedule": True, "menu": False},
    )
    assert_claim_firewall(result)
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1050
    assert result["planning_lower"] == 950
    assert result["planning_upper"] == 1100
    assert "MISSING_MENU_CONTEXT" in result["reason_codes"]


def test_marks_core_context_pilot_ready_but_keeps_human_gate() -> None:
    result = FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        1000,
        [],
        signal_availability={"schedule": True, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["decision_readiness"] == "PILOT_READY"
    assert result["recommended"] == 1050
    assert result["planning_lower"] == 950
    assert result["planning_upper"] == 1100


def test_negative_demand_is_clamped_to_zero() -> None:
    result = FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        -25,
        [],
        signal_availability={"schedule": True, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["planning_lower"] == 0
    assert result["recommended"] == 0
    assert result["planning_upper"] == 0


def main() -> int:
    tests = [
        test_withholds_without_schedule_backbone,
        test_requires_review_when_menu_context_is_missing,
        test_marks_core_context_pilot_ready_but_keeps_human_gate,
        test_negative_demand_is_clamped_to_zero,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
