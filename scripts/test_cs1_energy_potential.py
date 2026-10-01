#!/usr/bin/env python3
"""Regression tests for transparent energy-potential scenario calculations."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.optimizers.energy_potential import estimate_energy_potential  # noqa: E402


def test_neutral_temperature_uses_registered_scenario_assumptions() -> None:
    result = estimate_energy_potential(22.0)
    assert result["predicted_energy_mwh"] == 11.2
    assert result["kwh_saved"] == 1568.0
    assert result["cost_saved_tl"] == 4390.4
    assert result["co2_avoided_kg"] == 737.0
    assert result["provenance"] == "MODEL_ESTIMATE"
    assert result["claim_scope"] == "SCENARIO_POTENTIAL_NOT_MEASURED_SAVINGS"


def test_temperature_distance_changes_scenario_consistently() -> None:
    result = estimate_energy_potential(32.0)
    assert result["predicted_energy_mwh"] == 15.7
    assert result["kwh_saved"] == 2198.0
    assert result["cost_saved_tl"] == 6154.4
    assert result["co2_avoided_kg"] == 1033.1


def test_invalid_assumptions_fail_closed() -> None:
    invalid_calls = [
        lambda: estimate_energy_potential(math.nan),
        lambda: estimate_energy_potential(True),
        lambda: estimate_energy_potential(22.0, optimization_fraction=1.1),
        lambda: estimate_energy_potential(22.0, base_energy_mwh=-1),
        lambda: estimate_energy_potential(22.0, cost_tl_per_kwh=math.inf),
    ]
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            continue
        raise AssertionError("invalid energy-potential input must raise ValueError")


def main() -> int:
    tests = [
        test_neutral_temperature_uses_registered_scenario_assumptions,
        test_temperature_distance_changes_scenario_consistently,
        test_invalid_assumptions_fail_closed,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} energy-potential tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
