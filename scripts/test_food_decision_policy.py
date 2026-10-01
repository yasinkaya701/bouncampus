#!/usr/bin/env python3
"""Focused regression tests for the CS1 food decision policy."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.optimizers.food_optimizer import FoodOptimizer  # noqa: E402


def assert_claim_firewall(result: dict) -> None:
    forbidden = {"waste_reduction", "potential_waste_saved_kg", "cost_saved_tl"}
    leaked = forbidden.intersection(result)
    assert not leaked, f"pre-pilot impact fields leaked from decision policy: {sorted(leaked)}"
    assert result["policy_provenance"] == "POLICY_HEURISTIC"
    assert result["forecast_provenance"] == "MODEL_ESTIMATE"
    assert result["band_semantics"] == "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"
    assert result["calibration_status"] == "NOT_CALIBRATED"
    assert result["operator_approval_required"] is True
    assert result["automatic_kitchen_dispatch"] is False
    assert "HEURISTIC_BAND_NOT_CALIBRATED" in result["reason_codes"]


def pilot_eligible_optimize(*, demand: int, signals: dict[str, bool]):
    return FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        demand,
        [],
        signal_availability=signals,
        method_eligibility="PILOT_ELIGIBLE",
    )


def test_withholds_without_schedule_backbone() -> None:
    result = pilot_eligible_optimize(
        demand=1000,
        signals={"schedule": False, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["abstained"] is True
    assert result["recommended"] is None
    assert result["planning_lower"] == 900
    assert result["planning_upper"] == 1130
    assert "MISSING_REQUIRED_SCHEDULE" in result["reason_codes"]


def test_requires_review_when_context_is_partial() -> None:
    result = pilot_eligible_optimize(
        demand=1000,
        signals={"schedule": True, "menu": False},
    )
    assert_claim_firewall(result)
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["signal_coverage_pct"] == 50
    assert result["recommended"] == 1000
    assert result["planning_lower"] == 900
    assert result["planning_upper"] == 1130
    assert "CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED" in result["reason_codes"]


def test_marks_pilot_eligible_core_context_ready_but_keeps_human_gate() -> None:
    result = pilot_eligible_optimize(
        demand=1000,
        signals={"schedule": True, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["method_eligibility"] == "PILOT_ELIGIBLE"
    assert result["decision_readiness"] == "PILOT_READY"
    assert result["signal_coverage_pct"] == 70
    assert result["recommended"] == 1000
    assert result["planning_lower"] == 930
    assert result["planning_upper"] == 1090


def test_optimizer_defaults_to_sandbox_and_abstains() -> None:
    result = FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        1000,
        [],
        signal_availability={"schedule": True, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["method_eligibility"] == "SANDBOX_ONLY"
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended"] is None
    assert "METHOD_SANDBOX_ONLY" in result["reason_codes"]


def test_non_positive_demand_abstains() -> None:
    result = pilot_eligible_optimize(
        demand=-25,
        signals={"schedule": True, "menu": True},
    )
    assert_claim_firewall(result)
    assert result["planning_lower"] == 0
    assert result["recommended"] is None
    assert result["planning_upper"] == 0
    assert result["decision_readiness"] == "WITHHOLD"
    assert "NO_POSITIVE_DEMAND_ESTIMATE" in result["reason_codes"]


def main() -> int:
    tests = [
        test_withholds_without_schedule_backbone,
        test_requires_review_when_context_is_partial,
        test_marks_pilot_eligible_core_context_ready_but_keeps_human_gate,
        test_optimizer_defaults_to_sandbox_and_abstains,
        test_non_positive_demand_abstains,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
