#!/usr/bin/env python3
"""Regression tests for service-level exportability in CS1 source admission."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.service_truth import validate_service_truth_source_contract  # noqa: E402
from test_cs1_service_truth_artifact_admission import source_contract  # noqa: E402


def test_verified_measured_sources_require_service_level_exportability() -> None:
    provenance = source_contract()

    result = validate_service_truth_source_contract(provenance)

    assert result["source_contract_complete"] is True
    assert result["source_contract_service_level_exportable"] is False
    assert result["source_contract_verified"] is False
    assert "actual_served" in result["non_service_level_source_contract_fields"]
    assert "actual_served" in result["unverified_exportability_source_contract_fields"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-source exportability regressions")
