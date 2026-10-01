#!/usr/bin/env python3
"""Regression tests for CS1 decision reachability / freeze-time gating."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.optimizers.food_optimizer import FoodOptimizer  # noqa: E402


FULL_SIGNALS = {
    "schedule": True,
    "weather": True,
    "menu": True,
    "calendar": True,
}


def optimize(*, decision_reachability=None, include_reachability: bool = True):
    kwargs = {
        "signal_availability": FULL_SIGNALS,
        "method_eligibility": "PILOT_ELIGIBLE",
    }
    if include_reachability:
        kwargs["decision_reachability"] = decision_reachability
    return FoodOptimizer().optimize(
        "2026-10-01",
        "B-SOUTH-GY",
        1000,
        [],
        **kwargs,
    )


def verified_reachability(**overrides):
    value = {
        "decision_surface": "PRODUCTION_QUANTITY",
        "decision_surface_verified": True,
        "operator_authority_confirmed": True,
        "minutes_before_freeze": 90,
        "change_feasible_before_freeze": True,
    }
    value.update(overrides)
    return value


def test_unverified_reachability_blocks_pilot_ready_but_keeps_review_path() -> None:
    result = optimize(include_reachability=False)
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1000
    assert "DECISION_REACHABILITY_UNVERIFIED" in result["reason_codes"]
    assert result["operator_approval_required"] is True
    assert result["automatic_kitchen_dispatch"] is False


def test_verified_reachability_can_preserve_pilot_ready() -> None:
    result = optimize(decision_reachability=verified_reachability())
    assert result["decision_reachability_status"] == "REACHABLE"
    assert result["decision_surface"] == "PRODUCTION_QUANTITY"
    assert result["decision_surface_verified"] is True
    assert result["minutes_before_freeze"] == 90.0
    assert result["change_feasible_before_freeze"] is True
    assert result["decision_readiness"] == "PILOT_READY"
    assert result["recommended"] == 1000
    assert "DECISION_REACHABLE_BEFORE_FREEZE" in result["reason_codes"]


def test_named_but_unverified_surface_cannot_unlock_pilot_ready() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            decision_surface="SOME_UNVERIFIED_CONTROL",
            decision_surface_verified=False,
        )
    )
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1000
    assert "DECISION_SURFACE_UNVERIFIED" in result["reason_codes"]


def test_non_string_surface_is_not_silently_coerced() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            decision_surface=123,
        )
    )
    assert result["decision_surface"] is None
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert "DECISION_SURFACE_UNSPECIFIED" in result["reason_codes"]


def test_denied_authority_withholds_actionable_recommendation() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            operator_authority_confirmed=False,
        )
    )
    assert result["decision_reachability_status"] == "UNREACHABLE"
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended"] is None
    assert "DECISION_AUTHORITY_DENIED" in result["reason_codes"]


def test_unknown_authority_blocks_pilot_ready_without_claiming_denial() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            operator_authority_confirmed=None,
        )
    )
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1000
    assert "DECISION_AUTHORITY_UNKNOWN" in result["reason_codes"]
    assert "DECISION_AUTHORITY_DENIED" not in result["reason_codes"]


def test_closed_decision_window_withholds_actionable_recommendation() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            minutes_before_freeze=0,
        )
    )
    assert result["decision_reachability_status"] == "UNREACHABLE"
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended"] is None
    assert "DECISION_WINDOW_CLOSED" in result["reason_codes"]


def test_unknown_freeze_time_blocks_pilot_ready_without_inventing_timing() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            minutes_before_freeze=None,
        )
    )
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1000
    assert "DECISION_FREEZE_TIME_UNKNOWN" in result["reason_codes"]


def test_string_freeze_time_is_not_silently_coerced() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            minutes_before_freeze="90",
        )
    )
    assert result["minutes_before_freeze"] is None
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert "DECISION_FREEZE_TIME_UNKNOWN" in result["reason_codes"]


def test_known_infeasible_change_before_freeze_withholds() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            change_feasible_before_freeze=False,
        )
    )
    assert result["decision_reachability_status"] == "UNREACHABLE"
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["recommended"] is None
    assert "DECISION_CHANGE_NOT_FEASIBLE_BEFORE_FREEZE" in result["reason_codes"]


def test_unknown_change_feasibility_blocks_pilot_ready() -> None:
    result = optimize(
        decision_reachability=verified_reachability(
            change_feasible_before_freeze=None,
        )
    )
    assert result["decision_reachability_status"] == "UNVERIFIED"
    assert result["decision_readiness"] == "REVIEW_REQUIRED"
    assert result["recommended"] == 1000
    assert "DECISION_CHANGE_FEASIBILITY_UNKNOWN" in result["reason_codes"]


def main() -> int:
    tests = [
        test_unverified_reachability_blocks_pilot_ready_but_keeps_review_path,
        test_verified_reachability_can_preserve_pilot_ready,
        test_named_but_unverified_surface_cannot_unlock_pilot_ready,
        test_non_string_surface_is_not_silently_coerced,
        test_denied_authority_withholds_actionable_recommendation,
        test_unknown_authority_blocks_pilot_ready_without_claiming_denial,
        test_closed_decision_window_withholds_actionable_recommendation,
        test_unknown_freeze_time_blocks_pilot_ready_without_inventing_timing,
        test_string_freeze_time_is_not_silently_coerced,
        test_known_infeasible_change_before_freeze_withholds,
        test_unknown_change_feasibility_blocks_pilot_ready,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
