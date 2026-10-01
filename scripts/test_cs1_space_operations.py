#!/usr/bin/env python3
"""Regression tests for CS1 flexible-space consolidation planning."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.campus_operations import (  # noqa: E402
    READINESS_PILOT,
    READINESS_REVIEW,
    READINESS_WITHHOLD,
    plan_space_service,
)


class SpaceOperationsTests(unittest.TestCase):
    def test_activates_low_energy_capacity_after_must_open_space(self):
        result = plan_space_service({
            "predicted_demand": 120,
            "reserve_ratio": 0.10,
            "spaces": [
                {
                    "space_id": "LIB-A",
                    "capacity": 60,
                    "relative_energy_cost": 8,
                    "must_open": True,
                    "available": True,
                },
                {
                    "space_id": "LIB-B",
                    "capacity": 80,
                    "relative_energy_cost": 4,
                    "available": True,
                },
                {
                    "space_id": "LIB-C",
                    "capacity": 100,
                    "relative_energy_cost": 12,
                    "available": True,
                },
            ],
        })
        self.assertEqual(result["readiness"], READINESS_PILOT)
        self.assertEqual(result["required_capacity"], 132)
        self.assertEqual(result["active_space_ids"], ["LIB-A", "LIB-B"])
        self.assertGreaterEqual(result["active_capacity"], result["required_capacity"])
        self.assertEqual(result["capacity_shortfall"], 0)

    def test_insufficient_capacity_withholds_closure_recommendation(self):
        result = plan_space_service({
            "predicted_demand": 100,
            "reserve_ratio": 0.20,
            "spaces": [
                {
                    "space_id": "S1",
                    "capacity": 50,
                    "relative_energy_cost": 2,
                    "available": True,
                },
                {
                    "space_id": "S2",
                    "capacity": 40,
                    "relative_energy_cost": 3,
                    "available": True,
                },
            ],
        })
        self.assertEqual(result["readiness"], READINESS_WITHHOLD)
        self.assertEqual(result["capacity_shortfall"], 30)
        self.assertEqual(set(result["active_space_ids"]), {"S1", "S2"})
        self.assertIn("INSUFFICIENT_AVAILABLE_CAPACITY", result["reason_codes"])

    def test_invalid_space_rows_force_review_when_capacity_is_otherwise_feasible(self):
        result = plan_space_service({
            "predicted_demand": 40,
            "spaces": [
                {
                    "space_id": "S1",
                    "capacity": 80,
                    "relative_energy_cost": 5,
                    "available": True,
                },
                {
                    "space_id": "BROKEN",
                    "capacity": "unknown",
                    "relative_energy_cost": 1,
                    "available": True,
                },
            ],
        })
        self.assertEqual(result["readiness"], READINESS_REVIEW)
        self.assertIn("PARTIAL_INVALID_SPACE_INPUTS", result["reason_codes"])
        self.assertEqual(result["active_space_ids"], ["S1"])


if __name__ == "__main__":
    unittest.main()
