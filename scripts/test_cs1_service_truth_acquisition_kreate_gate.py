#!/usr/bin/env python3
"""Regression contract for wiring service-truth acquisition readiness into KREATE CI."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KREATE_CHECK = ROOT / "scripts/kreate_check.py"


def load_kreate_check():
    spec = importlib.util.spec_from_file_location("kreate_check", KREATE_CHECK)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {KREATE_CHECK}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_kreate_check_exposes_service_truth_acquisition_readiness_gate() -> None:
    contract = load_kreate_check()
    assert hasattr(contract, "check_service_truth_acquisition_readiness")

    errors: list[str] = []
    contract.check_service_truth_acquisition_readiness(errors)
    assert errors == []


def test_kreate_main_invokes_acquisition_readiness_gate() -> None:
    source = KREATE_CHECK.read_text(encoding="utf-8")
    assert "check_service_truth_acquisition_readiness(errors)" in source


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} KREATE acquisition-readiness gate tests")
