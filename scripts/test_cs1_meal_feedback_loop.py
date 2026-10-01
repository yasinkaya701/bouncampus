#!/usr/bin/env python3
"""Tests for recommendation outcome capture and offline ranking evaluation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.decision.meal_feedback import (  # noqa: E402
    build_recommendation_outcome,
    evaluate_recommendation_outcomes,
)


class MealFeedbackLoopTests(unittest.TestCase):
    def setUp(self):
        self.impression = {
            "event_scope": "RECOMMENDATION_IMPRESSION",
            "request_id": "req-1",
            "policy_version": "meal-recommendation-v1.0",
            "method_scope": "TRANSPARENT_PERSONALIZATION_BASELINE",
            "ranked_item_ids": ["a", "b", "c"],
            "outcome_observed": False,
        }

    def test_outcome_must_reference_a_shown_item(self):
        with self.assertRaises(ValueError):
            build_recommendation_outcome(
                self.impression,
                selected_item_id="not-shown",
                rating=5,
            )

    def test_outcome_preserves_impression_policy_and_request(self):
        outcome = build_recommendation_outcome(
            self.impression,
            selected_item_id="b",
            rating=4,
        )
        self.assertEqual(outcome["event_scope"], "RECOMMENDATION_OUTCOME")
        self.assertEqual(outcome["request_id"], "req-1")
        self.assertEqual(outcome["policy_version"], "meal-recommendation-v1.0")
        self.assertEqual(outcome["selected_item_id"], "b")
        self.assertEqual(outcome["selected_rank"], 2)
        self.assertTrue(outcome["outcome_observed"])

    def test_invalid_rating_fails_closed(self):
        with self.assertRaises(ValueError):
            build_recommendation_outcome(
                self.impression,
                selected_item_id="a",
                rating=6,
            )

    def test_offline_metrics_use_only_valid_observed_outcomes(self):
        events = [
            build_recommendation_outcome(self.impression, selected_item_id="a", rating=5),
            build_recommendation_outcome(
                {**self.impression, "request_id": "req-2"},
                selected_item_id="c",
                rating=3,
            ),
            {"event_scope": "BROKEN"},
        ]
        report = evaluate_recommendation_outcomes(events, top_k=2)
        self.assertEqual(report["n"], 2)
        self.assertEqual(report["invalid_rows"], 1)
        self.assertAlmostEqual(report["top1_hit_rate"], 0.5)
        self.assertAlmostEqual(report["top_k_hit_rate"], 0.5)
        self.assertAlmostEqual(report["mean_reciprocal_rank"], (1.0 + 1.0 / 3.0) / 2.0)
        self.assertAlmostEqual(report["mean_selected_rank"], 2.0)
        self.assertEqual(report["evaluation_scope"], "OFFLINE_OBSERVED_OUTCOMES_ONLY")


if __name__ == "__main__":
    unittest.main()
