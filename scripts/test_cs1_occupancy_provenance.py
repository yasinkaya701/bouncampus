#!/usr/bin/env python3
"""Regression: occupancy forecasts must not masquerade as measured/live occupancy."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.schemas import OccupancyForecast


def test_occupancy_forecast_declares_model_and_heuristic_provenance() -> None:
    forecast = OccupancyForecast(
        date="2026-10-05",
        building_id="B-NORTH-BM",
        total_hourly=[],
    )
    assert forecast.forecast_provenance == "MODEL_ESTIMATE"
    assert forecast.input_basis == "GENERATED_DATA_MODEL_PLUS_SCHEDULE_HEURISTICS"
    assert forecast.calibration_status == "NOT_CALIBRATED"
    assert forecast.measurement_status == "NO_LIVE_OCCUPANCY_MEASUREMENT"
    assert forecast.decision_eligible is False
    assert forecast.method_eligibility == "SANDBOX_ONLY"


def test_occupancy_forecast_limitations_disclose_generated_and_unmeasured_basis() -> None:
    forecast = OccupancyForecast(
        date="2026-10-05",
        building_id="B-NORTH-BM",
        total_hourly=[],
    )
    limitation_text = " ".join(forecast.limitations).lower()
    assert "generated" in limitation_text
    assert "schedule" in limitation_text
    assert "not measured" in limitation_text
    assert "roomnode" in limitation_text


def test_occupancy_router_source_does_not_label_estimate_as_real_schedule() -> None:
    source = (ROOT / "backend/app/routers/occupancy.py").read_text(encoding="utf-8")
    assert "Real BOUN Schedule" not in source
    assert "real_occ" not in source
    assert "schedule_estimate" in source
    assert "MODEL_ESTIMATE" in source


def test_predictor_source_explicitly_uses_generated_training_data() -> None:
    source = (ROOT / "backend/app/models/occupancy.py").read_text(encoding="utf-8")
    assert 'settings.GENERATED_DATA_DIR, "occupancy_history.csv"' in source


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} occupancy provenance regressions")
