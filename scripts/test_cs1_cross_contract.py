#!/usr/bin/env python3
"""Cross-language regression gates for the CS1 food decision contract."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_python_and_next_policy_versions_match() -> None:
    python_policy = (ROOT / "backend/app/decision/food_policy.py").read_text(encoding="utf-8")
    next_policy = (ROOT / "frontend/src/lib/food-waste.ts").read_text(encoding="utf-8")

    python_match = re.search(r'POLICY_VERSION\s*=\s*"([^"]+)"', python_policy)
    next_match = re.search(r"version:\s*'([^']+)'", next_policy)
    assert python_match, "Python food policy version marker missing"
    assert next_match, "Next food policy version marker missing"
    assert python_match.group(1) == next_match.group(1), (
        f"food decision policy drift: Python={python_match.group(1)} Next={next_match.group(1)}"
    )


def test_pilot_forecast_coverage_is_a_minimum_not_exact_target() -> None:
    next_policy = (ROOT / "frontend/src/lib/food-waste.ts").read_text(encoding="utf-8")
    expected = (
        "interventionForecastCoveragePct >= "
        "FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumInterventionForecastCoveragePct"
    )
    assert expected in next_policy, (
        "pilot forecast-coverage gate must accept coverage at or above the configured minimum"
    )


def main() -> int:
    tests = [
        test_python_and_next_policy_versions_match,
        test_pilot_forecast_coverage_is_a_minimum_not_exact_target,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
