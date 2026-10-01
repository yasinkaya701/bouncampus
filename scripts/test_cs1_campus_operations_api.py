#!/usr/bin/env python3
"""API smoke coverage for the CS1 campus operations router."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from app.routers import operations  # noqa: E402


class CampusOperationsApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = FastAPI()
        app.include_router(operations.router)
        cls.client = TestClient(app)

    def test_capabilities(self):
        response = self.client.get("/api/v1/decision/capabilities")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["policy_version"], "campus-operations-v1.0")
        self.assertIn("food", payload["domains"])
        self.assertIn("shuttle", payload["domains"])
        self.assertIn("classroom", payload["domains"])
        self.assertIn("space", payload["domains"])

    def test_shuttle_plan(self):
        response = self.client.post(
            "/api/v1/decision/shuttle/plan",
            json={
                "vehicle_capacity": 40,
                "departures": [{"departure_id": "08:00", "predicted_demand": 60}],
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["domain"], "SHUTTLE")
        self.assertEqual(payload["plan"][0]["recommended_vehicles"], 2)

    def test_space_plan(self):
        response = self.client.post(
            "/api/v1/decision/spaces/plan",
            json={
                "predicted_demand": 50,
                "spaces": [
                    {
                        "space_id": "LIB-A",
                        "capacity": 80,
                        "relative_energy_cost": 5,
                        "available": True,
                    }
                ],
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["domain"], "SPACE")
        self.assertEqual(payload["active_space_ids"], ["LIB-A"])
        self.assertFalse(payload["automatic_building_control"])

    def test_snapshot_fails_closed(self):
        response = self.client.post(
            "/api/v1/decision/snapshot",
            json={
                "food": {
                    "historical_served": [100, 105, 98],
                    "signals": {"schedule": True, "menu": True, "calendar": True},
                },
                "shuttle": {
                    "vehicle_capacity": 40,
                    "departures": [{"predicted_demand": 20}],
                },
                "classroom": {"rooms": [], "sessions": []},
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["overall_readiness"], "WITHHOLD")


if __name__ == "__main__":
    unittest.main()
