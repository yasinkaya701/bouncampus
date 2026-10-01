#!/usr/bin/env python3
"""Regression tests for dashboard/impact energy scenario consistency."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_ROUTE = ROOT / "backend" / "app" / "routers" / "dashboard.py"


def test_dashboard_uses_shared_energy_potential_calculator() -> None:
    source = DASHBOARD_ROUTE.read_text(encoding="utf-8")
    assert "from app.optimizers.energy_potential import estimate_energy_potential" in source
    assert "estimate_energy_potential(" in source
    assert "predicted_energy_mwh = energy_potential[\"predicted_energy_mwh\"]" in source


def test_impact_endpoint_does_not_publish_unrelated_fixed_savings() -> None:
    source = DASHBOARD_ROUTE.read_text(encoding="utf-8")
    forbidden_literals = {
        "kwh_saved=300.0",
        "co2_avoided_kg=141.0",
        "cost_saved_tl=840.0",
    }
    leaked = sorted(literal for literal in forbidden_literals if literal in source)
    assert not leaked, f"fixed impact values leaked: {leaked}"
    assert "kwh_saved=energy_potential[\"kwh_saved\"]" in source
    assert "cost_saved_tl=energy_potential[\"cost_saved_tl\"]" in source
    assert "co2_avoided_kg=energy_potential[\"co2_avoided_kg\"]" in source


def main() -> int:
    tests = [
        test_dashboard_uses_shared_energy_potential_calculator,
        test_impact_endpoint_does_not_publish_unrelated_fixed_savings,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} dashboard energy-contract tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
