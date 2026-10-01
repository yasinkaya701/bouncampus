#!/usr/bin/env python3
"""API contract tests for meal ranking and impression provenance."""

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


class MealRecommendationApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = FastAPI()
        app.include_router(operations.router)
        cls.client = TestClient(app)

    def test_meal_recommendation_endpoint(self):
        response = self.client.post(
            "/api/v1/decision/meals/recommend",
            json={
                "menu_items": [
                    {
                        "item_id": "a",
                        "name": "A",
                        "category": "main",
                        "tags": [],
                        "popularity_score": 0.8,
                        "avg_rating": 4.0,
                    },
                    {
                        "item_id": "b",
                        "name": "B",
                        "category": "main",
                        "tags": [],
                        "popularity_score": 0.5,
                        "avg_rating": 3.0,
                    },
                ]
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["ranked_items"][0]["item_id"], "a")
        self.assertFalse(payload["collaborative_model_used"])

    def test_impression_endpoint_preserves_decision_time_ranking(self):
        response = self.client.post(
            "/api/v1/decision/meals/impression",
            json={
                "request_id": "req-api-1",
                "ranking": {
                    "policy_version": "meal-recommendation-v1.0",
                    "method_scope": "TRANSPARENT_PERSONALIZATION_BASELINE",
                    "ranked_items": [{"item_id": "a"}, {"item_id": "b"}],
                },
                "context": {"meal_type": "lunch"},
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["ranked_item_ids"], ["a", "b"])
        self.assertFalse(payload["outcome_observed"])
        self.assertEqual(payload["request_id"], "req-api-1")


if __name__ == "__main__":
    unittest.main()
