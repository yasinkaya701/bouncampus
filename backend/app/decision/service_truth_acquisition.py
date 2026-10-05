"""Fail-closed readiness gate for the CS1 service-truth acquisition handoff.

This layer does not admit benchmark truth. It only checks whether an acquisition
artifact has enough measured-looking structure and verified source metadata to be
handed to the canonical SERVICE_TRUTH_V1 validation path.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .service_truth import (
    validate_service_truth_dataset,
    validate_service_truth_source_contract,
)


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def validate_service_truth_acquisition(artifact: Mapping[str, Any]) -> dict[str, object]:
    """Validate acquisition readiness without self-promoting benchmark eligibility."""

    if not isinstance(artifact, Mapping):
        raise ValueError("artifact must be a mapping")

    raw_rows = artifact.get("measured_rows")
    rows_valid_type = isinstance(raw_rows, Sequence) and not isinstance(
        raw_rows, (str, bytes, bytearray)
    )
    rows = raw_rows if rows_valid_type else []

    raw_provenance = artifact.get("field_provenance")
    provenance = raw_provenance if isinstance(raw_provenance, Mapping) else {}

    dataset_validation = validate_service_truth_dataset(rows, require_measured=True)
    source_contract_validation = validate_service_truth_source_contract(provenance)

    reasons: list[str] = []
    if not rows_valid_type or not rows:
        _append_unique(reasons, "MEASURED_ROWS_REQUIRED")
    elif dataset_validation["validation_status"] != "ACCEPTED_MEASURED":
        _append_unique(reasons, "DATASET_NOT_ACCEPTED_MEASURED")
        for code in dataset_validation.get("reason_codes", []):
            _append_unique(reasons, str(code))

    if not source_contract_validation["source_contract_complete"]:
        _append_unique(reasons, "SOURCE_CONTRACT_INCOMPLETE")
    if not source_contract_validation["source_contract_verified"]:
        _append_unique(reasons, "SOURCE_CONTRACT_UNVERIFIED")

    declared_benchmark = artifact.get("benchmark_eligible") is True
    declared_pilot = artifact.get("pilot_evidence_eligible") is True
    if declared_benchmark or declared_pilot:
        _append_unique(reasons, "DECLARED_ELIGIBILITY_NOT_TRUSTED")

    ready = (
        dataset_validation["validation_status"] == "ACCEPTED_MEASURED"
        and bool(source_contract_validation["source_contract_verified"])
        and not declared_benchmark
        and not declared_pilot
    )
    status = "READY_FOR_SERVICE_TRUTH_VALIDATION" if ready else "ACQUISITION_BLOCKED"

    return {
        "validation_status": status,
        "ready_for_service_truth_validation": ready,
        "benchmark_eligible": False,
        "pilot_evidence_eligible": False,
        "dataset_validation": dataset_validation,
        "source_contract_validation": source_contract_validation,
        "reason_codes": [] if ready else reasons,
        "result_scope": "SERVICE_TRUTH_ACQUISITION_READINESS_ONLY",
        "claim_boundary": (
            "Readiness only permits handoff to canonical service-truth admission; it does "
            "not itself establish benchmark eligibility, pilot evidence, source accuracy, "
            "operational impact, savings, or live integration."
        ),
    }
