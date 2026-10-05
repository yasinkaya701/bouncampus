#!/usr/bin/env python3
"""Regression guard for KREATE service-truth acquisition claims."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kreate_check import check_service_truth_acquisition  # noqa: E402


ACQUISITION_PATH = ROOT / "KREATE/EXPERIMENTS/SERVICE_TRUTH_ACQUISITION_V1.json"


def acquisition_template() -> dict:
    return json.loads(ACQUISITION_PATH.read_text(encoding="utf-8"))


def test_current_blocked_acquisition_template_is_valid_ci_state() -> None:
    errors: list[str] = []

    check_service_truth_acquisition(errors, artifact=acquisition_template())

    assert errors == []


def test_raw_benchmark_flag_cannot_self_promote_acquisition_artifact() -> None:
    artifact = deepcopy(acquisition_template())
    artifact["benchmark_eligible"] = True
    errors: list[str] = []

    check_service_truth_acquisition(errors, artifact=artifact)

    assert any("benchmark_eligible" in error for error in errors)


def test_raw_pilot_flag_cannot_self_promote_acquisition_artifact() -> None:
    artifact = deepcopy(acquisition_template())
    artifact["pilot_evidence_eligible"] = True
    errors: list[str] = []

    check_service_truth_acquisition(errors, artifact=artifact)

    assert any("pilot_evidence_eligible" in error for error in errors)


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} KREATE acquisition guard tests")
