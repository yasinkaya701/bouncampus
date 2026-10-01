#!/usr/bin/env python3
"""Claim-firewall regression for dashboard action recommendations."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_ROUTE = ROOT / "backend" / "app" / "routers" / "dashboard.py"


def test_dashboard_does_not_publish_hard_coded_energy_actions() -> None:
    source = DASHBOARD_ROUTE.read_text(encoding="utf-8")
    forbidden_literals = {
        "Consolidate Kare Blok (KB) Evening Load",
        "New Hall (NH) Lecture Halls Idle Mode",
        "impact_value=165.0",
        "impact_value=85.0",
    }
    leaked = sorted(literal for literal in forbidden_literals if literal in source)
    assert not leaked, f"hard-coded dashboard actions leaked: {leaked}"


def test_dashboard_routes_non_food_actions_through_action_engine() -> None:
    source = DASHBOARD_ROUTE.read_text(encoding="utf-8")
    assert "ActionEngine" in source
    assert "action_engine.generate_actions" in source


def main() -> int:
    tests = [
        test_dashboard_does_not_publish_hard_coded_energy_actions,
        test_dashboard_routes_non_food_actions_through_action_engine,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} dashboard action claim-firewall tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
