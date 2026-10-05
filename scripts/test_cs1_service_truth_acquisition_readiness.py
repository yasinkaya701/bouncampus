#!/usr/bin/env python3
"""Regression contract for fail-closed service-truth acquisition readiness."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.service_truth_acquisition import (  # noqa: E402
    validate_service_truth_acquisition,
)
from kreate_check import check_service_truth_acquisition  # noqa: E402
from test_cs1_service_truth_artifact_admission import source_contract  # noqa: E402
from test_cs1_service_truth_contract import valid_rows  # noqa: E402


ACQUISITION_PATH = ROOT / "KREATE/EXPERIMENTS/SERVICE_TRUTH_ACQUISITION_V1.json"


def acquisition_template() -> dict:
    return json.loads(ACQUISITION_PATH.read_text())


def test_committed_acquisition_template_fails_closed_without_measured_rows_or_verified_sources() -> None:
    result = validate_service_truth_acquisition(acquisition_template())

    assert result["validation_status"] == "ACQUISITION_BLOCKED"
    assert result["ready_for_service_truth_validation"] is False
    assert result["benchmark_eligible"] is False
    assert result["pilot_evidence_eligible"] is False
    assert "MEASURED_ROWS_REQUIRED" in result["reason_codes"]
    assert "SOURCE_CONTRACT_UNVERIFIED" in result["reason_codes"]
    assert "actual_served" in result["source_contract_validation"][
        "unverified_source_contract_fields"
    ]


def test_declared_template_flags_cannot_self_promote_unverified_acquisition() -> None:
    artifact = acquisition_template()
    artifact["benchmark_eligible"] = True
    artifact["pilot_evidence_eligible"] = True

    result = validate_service_truth_acquisition(artifact)

    assert result["validation_status"] == "ACQUISITION_BLOCKED"
    assert result["benchmark_eligible"] is False
    assert result["pilot_evidence_eligible"] is False
    assert "DECLARED_ELIGIBILITY_NOT_TRUSTED" in result["reason_codes"]


def test_verified_measured_acquisition_only_becomes_ready_for_canonical_validation() -> None:
    artifact = deepcopy(acquisition_template())
    artifact["measured_rows"] = valid_rows()
    artifact["field_provenance"] = source_contract()
    artifact["benchmark_eligible"] = False
    artifact["pilot_evidence_eligible"] = False

    result = validate_service_truth_acquisition(artifact)

    assert result["validation_status"] == "READY_FOR_SERVICE_TRUTH_VALIDATION"
    assert result["ready_for_service_truth_validation"] is True
    assert result["reason_codes"] == []
    assert result["dataset_validation"]["validation_status"] == "ACCEPTED_MEASURED"
    assert result["source_contract_validation"]["source_contract_verified"] is True
    assert result["benchmark_eligible"] is False
    assert result["pilot_evidence_eligible"] is False
    assert "canonical service-truth admission" in result["claim_boundary"]


def test_kreate_guard_accepts_current_fail_closed_acquisition_template() -> None:
    errors: list[str] = []

    check_service_truth_acquisition(errors, artifact=acquisition_template())

    assert errors == []


def test_kreate_guard_rejects_self_declared_acquisition_eligibility() -> None:
    artifact = acquisition_template()
    artifact["benchmark_eligible"] = True
    artifact["pilot_evidence_eligible"] = True
    errors: list[str] = []

    check_service_truth_acquisition(errors, artifact=artifact)

    assert any("benchmark_eligible" in error for error in errors)
    assert any("pilot_evidence_eligible" in error for error in errors)


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth acquisition readiness tests")
