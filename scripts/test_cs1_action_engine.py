#!/usr/bin/env python3
"""Regression tests for evidence-gated campus action generation."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.optimizers.action_engine import ActionEngine  # noqa: E402


def valid_candidate(**overrides):
    candidate = {
        "priority": "HIGH",
        "title": "Review verified campus recommendation",
        "time": "18:00 - 20:00",
        "location": "Kare Blok",
        "description": "Operator review is required before any operational change.",
        "impact_value": 42.0,
        "impact_unit": "MODEL_ESTIMATE kWh potential",
        "provenance": "MODEL_ESTIMATE",
        "decision_readiness": "REVIEW_REQUIRED",
        "operator_approval_required": True,
        "auto_dispatch_allowed": False,
    }
    candidate.update(overrides)
    return candidate


def test_empty_inputs_generate_no_actions() -> None:
    actions = ActionEngine().generate_actions("2026-10-01", [], [])
    assert actions == [], "empty evidence must never synthesize a hard-coded action"


def test_unreviewable_or_auto_dispatch_candidates_are_rejected() -> None:
    engine = ActionEngine()
    candidates = [
        valid_candidate(decision_readiness="WITHHOLD"),
        valid_candidate(operator_approval_required=False),
        valid_candidate(auto_dispatch_allowed=True),
        valid_candidate(provenance="UNVERIFIED"),
        valid_candidate(impact_value=math.nan),
    ]
    actions = engine.generate_actions("2026-10-01", candidates, [])
    assert actions == []


def test_explicit_reviewable_candidate_is_adapted_without_changing_evidence() -> None:
    actions = ActionEngine().generate_actions(
        "2026-10-01",
        [valid_candidate()],
        [],
    )
    assert len(actions) == 1
    action = actions[0]
    assert action.type == "energy"
    assert action.title == "Review verified campus recommendation"
    assert action.impact_value == 42.0
    assert action.impact_unit == "MODEL_ESTIMATE kWh potential"
    assert action.provenance == "MODEL_ESTIMATE"
    assert "Operator review" in action.description


def main() -> int:
    tests = [
        test_empty_inputs_generate_no_actions,
        test_unreviewable_or_auto_dispatch_candidates_are_rejected,
        test_explicit_reviewable_candidate_is_adapted_without_changing_evidence,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} CS1 action-engine tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
