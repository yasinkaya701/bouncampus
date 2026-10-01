#!/usr/bin/env python3
"""API contract tests for recommendation outcomes and evaluation."""

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


class MealFeedbackApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = FastAPI()
        app.include_router(operations.router)
        cls.client = TestClient(app)

    def test_outcome_endpoint_links_selection_to_impression(self):
        response = self.client.post(
            "/api/v1/decision/meals/outcome",
            json={
                "impression": {
                    "event_scope": "RECOMMENDATION_IMPRESSION",
                    "request_id": "req-api-feedback",
                    "policy_version": "meal-recommendation-v1.0",
                    "method_scope": "TRANSPARENT_PERSONALIZATION_BASELINE",
                    "ranked_item_ids": ["a", "b"],
                    "outcome_observed": False,
                },
                "selected_item_id": "b",
                "rating": 4,
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["selected_rank"], 2)
        self.assertTrue(payload["outcome_observed"])

    def test_evaluation_endpoint_reports_ranking_metrics(self):
        response = self.client.post(
            "/api/v1/decision/meals/evaluate",
            json={
                "top_k": 2,
                "events": [
                    {
                        "event_scope": "RECOMMENDATION_OUTCOME",
                        "request_id": "r1",
                        "policy_version": "meal-recommendation-v1.0",
                        "method_scope": "TRANSPARENT_PERSONALIZATION_BASELINE",
                        "ranked_item_ids": ["a", "b"],
                        "selected_item_id": "a",
                        "selected_rank": 1,
                        "rating": 5,
                        "action": "SELECTED",
                        "outcome_observed": True,
                    }
                ],
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["n"], 1)
        self.assertEqual(payload["top1_hit_rate"], 1.0)
        self.assertEqual(payload["top_k_hit_rate"], 1.0)

    def test_outcome_rejects_unshown_selection(self):
        response = self.client.post(
            "/api/v1/decision/meals/outcome",
            json={
                "impression": {
                    "event_scope": "RECOMMENDATION_IMPRESSION",
                    "request_id": "req-bad",
                    "policy_version": "meal-recommendation-v1.0",
                    "method_scope": "TRANSPARENT_PERSONALIZATION_BASELINE",
                    "ranked_item_ids": ["a"],
                    "outcome_observed": False,
                },
                "selected_item_id": "x",
            },
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
