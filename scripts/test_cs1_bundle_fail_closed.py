#!/usr/bin/env python3
"""Fail-closed regressions for the CS1 campus readiness bundle."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_bundle():
    path = ROOT / "backend/app/decision/campus_bundle.py"
    if not path.exists():
        raise AssertionError("canonical campus bundle module missing")
    spec = importlib.util.spec_from_file_location("cs1_campus_bundle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_empty_bundle_withholds() -> None:
    module = load_bundle()
    result = module.build_campus_ops_bundle({})
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["module_states"] == {}
    assert "NO_CAMPUS_OPS_MODULES" in result["reason_codes"]


def test_malformed_module_result_fails_closed_instead_of_crashing() -> None:
    module = load_bundle()
    result = module.build_campus_ops_bundle({"food": "not-a-result"})
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["module_states"] == {"food": "WITHHOLD"}
    assert "INVALID_MODULE_RESULT_food" in result["reason_codes"]


def test_unknown_readiness_fails_closed() -> None:
    module = load_bundle()
    result = module.build_campus_ops_bundle(
        {"energy": {"decision_readiness": "MAGIC_READY"}}
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["module_states"]["energy"] == "WITHHOLD"
    assert "UNKNOWN_READINESS_energy" in result["reason_codes"]


def test_most_conservative_readiness_wins() -> None:
    module = load_bundle()
    result = module.build_campus_ops_bundle(
        {
            "food": {"decision_readiness": "PILOT_READY"},
            "water": {"decision_readiness": "REVIEW_REQUIRED"},
            "state": {"decision_readiness": "WITHHOLD"},
        }
    )
    assert result["decision_readiness"] == "WITHHOLD"
    assert result["module_states"] == {
        "food": "PILOT_READY",
        "water": "REVIEW_REQUIRED",
        "state": "WITHHOLD",
    }


def test_api_and_orchestrator_route_to_canonical_bundle() -> None:
    router = (ROOT / "backend/app/routers/campus_ops.py").read_text(encoding="utf-8")
    orchestrator = (
        ROOT / "backend/app/decision/campus_orchestrator.py"
    ).read_text(encoding="utf-8")
    expected = "from app.decision.campus_bundle import build_campus_ops_bundle"
    assert expected in router
    assert expected in orchestrator


def main() -> int:
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
        print(f"PASS {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
