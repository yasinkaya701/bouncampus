#!/usr/bin/env python3
"""Regression tests for privacy-safe source provenance in CS1 service truth."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"
for path in (BACKEND, SCRIPTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.decision.service_truth import (  # noqa: E402
    validate_service_truth_artifact,
    validate_service_truth_source_contract,
)
from test_cs1_service_truth_artifact_admission import (  # noqa: E402
    measured_row,
    source_contract,
)


def test_verified_source_contract_rejects_nested_identity_contact_metadata() -> None:
    provenance = source_contract()
    provenance["actual_served"]["support"] = {
        "email": "synthetic-ops-contact@example.invalid",
    }

    result = validate_service_truth_source_contract(provenance)

    assert result["source_contract_complete"] is True
    assert result["source_contract_privacy_safe"] is False
    assert result["source_contract_verified"] is False
    assert "PRIVACY_FIELD_NOT_ALLOWED_EMAIL" in result["privacy_reason_codes"]


def test_identity_bearing_source_metadata_is_rejected_before_benchmark_admission() -> None:
    provenance = source_contract()
    provenance["menu"]["support"] = {
        "email": "synthetic-menu-contact@example.invalid",
    }

    result = validate_service_truth_artifact(
        [measured_row(0), measured_row(1), measured_row(2)],
        field_provenance=provenance,
    )

    assert result["dataset_validation"]["validation_status"] == "ACCEPTED_MEASURED"
    assert result["source_contract_validation"]["source_contract_complete"] is True
    assert result["source_contract_validation"]["source_contract_privacy_safe"] is False
    assert result["source_contract_validation"]["source_contract_verified"] is False
    assert result["validation_status"] == "SOURCE_CONTRACT_PRIVACY_REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "SOURCE_CONTRACT_PRIVACY_REJECTED" in result["reason_codes"]
    assert "PRIVACY_FIELD_NOT_ALLOWED_EMAIL" in result["reason_codes"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} source-provenance privacy tests")
