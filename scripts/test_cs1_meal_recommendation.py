#!/usr/bin/env python3
"""Regression tests for the CS1 meal recommendation baseline and feedback contract."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.meal_recommendation import (  # noqa: E402
    build_recommendation_impression,
    rank_menu_items,
)


class MealRecommendationTests(unittest.TestCase):
    def test_dietary_exclusion_is_a_hard_filter(self):
        result = rank_menu_items({
            "menu_items": [
                {
                    "item_id": "meat",
                    "name": "Etli Yemek",
                    "category": "main",
                    "tags": ["meat"],
                    "popularity_score": 0.95,
                    "avg_rating": 4.8,
                },
                {
                    "item_id": "veg",
                    "name": "Sebze",
                    "category": "main",
                    "tags": ["vegetarian"],
                    "popularity_score": 0.60,
                    "avg_rating": 4.0,
                },
            ],
            "constraints": {"excluded_tags": ["meat"]},
        })
        self.assertEqual([row["item_id"] for row in result["ranked_items"]], ["veg"])
        self.assertEqual(result["excluded_item_ids"], ["meat"])

    def test_explicit_feedback_can_reorder_equal_population_priors(self):
        result = rank_menu_items({
            "menu_items": [
                {
                    "item_id": "a",
                    "name": "A",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.80,
                    "avg_rating": 4.0,
                },
                {
                    "item_id": "b",
                    "name": "B",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.80,
                    "avg_rating": 4.0,
                },
            ],
            "feedback": [
                {"item_id": "a", "category": "main", "rating": 5},
                {"item_id": "a", "category": "main", "rating": 5},
                {"item_id": "b", "category": "main", "rating": 1},
                {"item_id": "b", "category": "main", "rating": 1},
            ],
        })
        self.assertEqual(result["ranked_items"][0]["item_id"], "a")
        self.assertGreater(
            result["ranked_items"][0]["personalization_evidence_n"],
            0,
        )
        self.assertEqual(result["method_scope"], "TRANSPARENT_PERSONALIZATION_BASELINE")

    def test_cold_start_is_deterministic_population_prior(self):
        result = rank_menu_items({
            "menu_items": [
                {
                    "item_id": "popular",
                    "name": "Popular",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.90,
                    "avg_rating": 4.5,
                },
                {
                    "item_id": "less-popular",
                    "name": "Less Popular",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.50,
                    "avg_rating": 4.0,
                },
            ],
        })
        self.assertEqual(result["ranked_items"][0]["item_id"], "popular")
        self.assertEqual(result["feedback_rows_used"], 0)
        self.assertIn("COLD_START_POPULATION_PRIOR", result["reason_codes"])

    def test_malformed_feedback_is_ignored_and_counted(self):
        result = rank_menu_items({
            "menu_items": [
                {
                    "item_id": "a",
                    "name": "A",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.70,
                    "avg_rating": 4.0,
                }
            ],
            "feedback": [
                {"item_id": "a", "category": "main", "rating": 6},
                {"item_id": "a", "category": "main", "rating": "bad"},
                {"item_id": "a", "category": "main", "rating": 4},
            ],
        })
        self.assertEqual(result["feedback_rows_used"], 1)
        self.assertEqual(result["invalid_feedback_rows"], 2)
        self.assertIn("PARTIAL_INVALID_FEEDBACK", result["reason_codes"])

    def test_impression_keeps_policy_and_ranking_provenance(self):
        ranking = rank_menu_items({
            "menu_items": [
                {
                    "item_id": "a",
                    "name": "A",
                    "category": "main",
                    "tags": [],
                    "popularity_score": 0.7,
                    "avg_rating": 4.0,
                }
            ]
        })
        impression = build_recommendation_impression(
            ranking,
            request_id="req-1",
            context={"meal_type": "lunch", "cafeteria_id": "B-SOUTH-GY"},
        )
        self.assertEqual(impression["request_id"], "req-1")
        self.assertEqual(impression["ranked_item_ids"], ["a"])
        self.assertEqual(impression["policy_version"], ranking["policy_version"])
        self.assertFalse(impression["outcome_observed"])
        self.assertEqual(impression["event_scope"], "RECOMMENDATION_IMPRESSION")


if __name__ == "__main__":
    unittest.main()
