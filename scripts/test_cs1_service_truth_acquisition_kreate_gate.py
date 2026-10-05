#!/usr/bin/env python3
"""Regression contract for wiring service-truth acquisition readiness into KREATE CI."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KREATE_CHECK = ROOT / "scripts/kreate_check.py"
ACQUISITION_PATH = ROOT / "KREATE/EXPERIMENTS/SERVICE_TRUTH_ACQUISITION_V1.json"


def load_kreate_check():
    spec = importlib.util.spec_from_file_location("kreate_check", KREATE_CHECK)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {KREATE_CHECK}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def acquisition_template() -> dict:
    return json.loads(ACQUISITION_PATH.read_text(encoding="utf-8"))


def test_current_blocked_acquisition_is_valid_kreate_ci_state() -> None:
    contract = load_kreate_check()
    assert hasattr(contract, "check_service_truth_acquisition_readiness")

    errors: list[str] = []
    contract.check_service_truth_acquisition_readiness(
        errors,
        artifact=acquisition_template(),
    )
    assert errors == []


def test_kreate_guard_rejects_raw_benchmark_self_promotion() -> None:
    contract = load_kreate_check()
    artifact = deepcopy(acquisition_template())
    artifact["benchmark_eligible"] = True
    errors: list[str] = []

    contract.check_service_truth_acquisition_readiness(errors, artifact=artifact)

    assert any("benchmark_eligible" in error for error in errors)


def test_kreate_guard_rejects_raw_pilot_self_promotion() -> None:
    contract = load_kreate_check()
    artifact = deepcopy(acquisition_template())
    artifact["pilot_evidence_eligible"] = True
    errors: list[str] = []

    contract.check_service_truth_acquisition_readiness(errors, artifact=artifact)

    assert any("pilot_evidence_eligible" in error for error in errors)


def test_kreate_main_invokes_acquisition_readiness_gate() -> None:
    source = KREATE_CHECK.read_text(encoding="utf-8")
    assert "check_service_truth_acquisition_readiness(errors)" in source


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} KREATE acquisition-readiness gate tests")
