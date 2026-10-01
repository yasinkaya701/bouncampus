#!/usr/bin/env python3
"""Focused regression tests for the CS1 campus operations decision layer."""

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
    allocate_classrooms,
    build_operations_snapshot,
    plan_food_service,
    plan_shuttle_service,
)


class CampusOperationsTests(unittest.TestCase):
    def test_food_abstains_without_schedule(self):
        result = plan_food_service({
            "historical_served": [100, 105, 95, 110, 98],
            "signals": {"menu": True, "calendar": True},
        })
        self.assertEqual(result["readiness"], READINESS_WITHHOLD)
        self.assertIsNone(result["recommended_production"])
        self.assertIn("SCHEDULE_SIGNAL_REQUIRED", result["reason_codes"])

    def test_food_uses_asymmetric_shortage_weight(self):
        result = plan_food_service({
            "historical_served": [100, 102, 98, 105, 95, 101],
            "signals": {"schedule": True, "menu": True, "calendar": True},
            "context_multipliers": {"menu": 1.05},
            "shortage_weight": 3,
            "surplus_weight": 1,
        })
        self.assertEqual(result["readiness"], READINESS_PILOT)
        midpoint = (result["planning_lower"] + result["planning_upper"]) / 2
        self.assertGreater(result["recommended_production"], midpoint)
        self.assertEqual(result["cost_target_quantile"], 0.75)

    def test_shuttle_adds_capacity_for_peak(self):
        result = plan_shuttle_service({
            "vehicle_capacity": 40,
            "departures": [
                {
                    "departure_id": "08:00",
                    "predicted_demand": 76,
                    "waiting_queue": 4,
                    "scheduled_vehicles": 1,
                }
            ],
        })
        self.assertEqual(result["readiness"], READINESS_PILOT)
        self.assertEqual(result["plan"][0]["recommended_vehicles"], 3)
        self.assertEqual(result["projected_overflow"], 0)

    def test_shuttle_partial_bad_input_requires_review(self):
        result = plan_shuttle_service({
            "vehicle_capacity": 50,
            "departures": [
                {"departure_id": "A", "predicted_demand": 25},
                {"departure_id": "B", "predicted_demand": "bad"},
            ],
        })
        self.assertEqual(result["readiness"], READINESS_REVIEW)

    def test_room_allocation_respects_capacity_and_conflict(self):
        result = allocate_classrooms({
            "rooms": [
                {
                    "room_id": "R1",
                    "capacity": 40,
                    "building_id": "B1",
                    "energy_cost": 3,
                    "available_slots": ["MON-09"],
                },
                {
                    "room_id": "R2",
                    "capacity": 80,
                    "building_id": "B1",
                    "energy_cost": 5,
                    "available_slots": ["MON-09"],
                },
            ],
            "sessions": [
                {"session_id": "S1", "slot": "MON-09", "expected_attendance": 70},
                {"session_id": "S2", "slot": "MON-09", "expected_attendance": 35},
            ],
        })
        by_session = {row["session_id"]: row["room_id"] for row in result["assignments"]}
        self.assertEqual(by_session["S1"], "R2")
        self.assertEqual(by_session["S2"], "R1")
        self.assertEqual(result["readiness"], READINESS_PILOT)

    def test_room_unassigned_is_withhold(self):
        result = allocate_classrooms({
            "rooms": [
                {
                    "room_id": "R1",
                    "capacity": 30,
                    "building_id": "B1",
                    "energy_cost": 2,
                    "available_slots": ["MON-09"],
                },
            ],
            "sessions": [
                {"session_id": "S1", "slot": "MON-09", "expected_attendance": 60},
            ],
        })
        self.assertEqual(result["readiness"], READINESS_WITHHOLD)
        self.assertEqual(result["unassigned_count"], 1)

    def test_snapshot_fails_closed_to_worst_domain(self):
        result = build_operations_snapshot({
            "food": {
                "historical_served": [100, 100, 100],
                "signals": {"schedule": True, "menu": True, "calendar": True},
            },
            "shuttle": {
                "vehicle_capacity": 40,
                "departures": [{"predicted_demand": 20}],
            },
            "classroom": {"rooms": [], "sessions": []},
        })
        self.assertEqual(result["overall_readiness"], READINESS_WITHHOLD)


if __name__ == "__main__":
    unittest.main()
