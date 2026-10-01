#!/usr/bin/env python3
"""Regression tests for sparse occupancy-history prediction."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

import app.models.occupancy as occupancy_module  # noqa: E402
from app.models.occupancy import OccupancyPredictor  # noqa: E402


class FakeEncoder:
    def transform(self, values):
        return np.zeros(len(values), dtype=int)


class FakeModel:
    def predict(self, frame):
        return np.array([float(frame.iloc[0]["scheduled_students"])])


def sparse_history() -> pd.DataFrame:
    rows = []
    for hour, scheduled in ((9, 30), (10, 45)):
        rows.append(
            {
                "date": "2026-09-30",
                "hour": hour,
                "weekday": 2,
                "building_id": "B-TEST",
                "floor": 1,
                "scheduled_students": scheduled,
                "total_capacity": 100,
                "exam_week": 0,
                "event_count": 0,
                "temperature": 20.0,
                "rain": 0,
                "semester_week": 2,
                "prev_day_occupancy": 20,
                "prev_week_same_hour": 25,
                "occupancy_count": scheduled,
            }
        )
    return pd.DataFrame(rows)


def test_sparse_hour_history_does_not_raise_or_invent_missing_hours() -> None:
    predictor = OccupancyPredictor()
    predictor.model = FakeModel()
    predictor.le = FakeEncoder()

    original_read_csv = occupancy_module.pd.read_csv
    occupancy_module.pd.read_csv = lambda *_args, **_kwargs: sparse_history()
    try:
        result = predictor.predict_floor("2026-10-01", "B-TEST", 1)
    finally:
        occupancy_module.pd.read_csv = original_read_csv

    assert [row["hour"] for row in result] == [9, 10]
    assert [row["occupancy_count"] for row in result] == [30, 45]
    assert all(0 <= row["occupancy_ratio"] <= 1 for row in result)


def main() -> int:
    tests = [test_sparse_hour_history_does_not_raise_or_invent_missing_hours]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)}/{len(tests)} sparse occupancy-history tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
