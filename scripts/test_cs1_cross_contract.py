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


def test_python_and_next_reachability_contract_match() -> None:
    python_policy = (ROOT / "backend/app/decision/food_policy.py").read_text(encoding="utf-8")
    next_reachability_path = ROOT / "frontend/src/lib/food-decision-reachability.ts"
    assert next_reachability_path.is_file(), "active Next reachability gate is missing"
    next_reachability = next_reachability_path.read_text(encoding="utf-8")
    route = (ROOT / "frontend/src/app/api/v1/food/route.ts").read_text(encoding="utf-8")

    python_match = re.search(
        r'REACHABILITY_POLICY_VERSION\s*=\s*"([^"]+)"',
        python_policy,
    )
    next_match = re.search(
        r"REACHABILITY_POLICY_VERSION\s*=\s*'([^']+)'",
        next_reachability,
    )
    assert python_match, "Python reachability policy version marker missing"
    assert next_match, "Next reachability policy version marker missing"
    assert python_match.group(1) == next_match.group(1), (
        "decision reachability policy drift: "
        f"Python={python_match.group(1)} Next={next_match.group(1)}"
    )

    for marker in (
        "DECISION_SURFACE_UNVERIFIED",
        "DECISION_AUTHORITY_DENIED",
        "DECISION_AUTHORITY_UNKNOWN",
        "DECISION_WINDOW_CLOSED",
        "DECISION_CHANGE_NOT_FEASIBLE_BEFORE_FREEZE",
        "DECISION_CHANGE_FEASIBILITY_UNKNOWN",
    ):
        assert marker in next_reachability, f"Next reachability gate missing {marker}"

    assert "applyDecisionReachability" in route, (
        "active Next /api/v1/food route must apply the reachability gate"
    )
    assert "reachabilityPolicyVersion" in route, (
        "active Next food API must expose the reachability policy version"
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
        test_python_and_next_reachability_contract_match,
        test_pilot_forecast_coverage_is_a_minimum_not_exact_target,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
