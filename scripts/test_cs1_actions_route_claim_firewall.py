#!/usr/bin/env python3
"""Claim-firewall regression for the public actions API route."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIONS_ROUTE = ROOT / "backend" / "app" / "routers" / "actions.py"


def test_actions_route_does_not_publish_hard_coded_operational_claims() -> None:
    source = ACTIONS_ROUTE.read_text(encoding="utf-8")
    forbidden_literals = {
        "Consolidate Kare Blok (KB) Evening Study Groups",
        "Review South Campus Lunch Overflow",
        "New Hall (NH) Midday Lecture Hall Eco-Ventilation",
        "Aptullah Kuran Library Night HVAC Review",
        "175.0",
        "90.0",
        "45.0",
        "75.0",
    }
    leaked = sorted(literal for literal in forbidden_literals if literal in source)
    assert not leaked, f"hard-coded operational claims leaked from actions route: {leaked}"


def test_actions_route_uses_evidence_gated_action_engine_for_non_food_actions() -> None:
    source = ACTIONS_ROUTE.read_text(encoding="utf-8")
    assert "ActionEngine" in source
    assert "action_engine.generate_actions" in source


def main() -> int:
    tests = [
        test_actions_route_does_not_publish_hard_coded_operational_claims,
        test_actions_route_uses_evidence_gated_action_engine_for_non_food_actions,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} actions-route claim-firewall tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
