"""Fail-closed readiness gate for service-truth acquisition artifacts.

This module is deliberately narrower than canonical service-truth admission. It
answers only whether an acquisition handoff has enough measured rows and verified
source metadata to be submitted to the canonical validators next. It never grants
benchmark or pilot evidence eligibility by itself.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .service_truth import (
    _conditionally_required_source_fields,
    validate_service_truth_dataset,
    validate_service_truth_source_contract,
)


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def validate_service_truth_acquisition(artifact: Mapping[str, Any]) -> dict[str, object]:
    """Validate whether an acquisition handoff is ready for canonical admission.

    Readiness requires measured service-level rows that pass the existing dataset
    validator plus a fully verified, privacy-safe source contract. Optional source
    fields such as weather remain conditionally required when the measured rows
    actually declare them as decision inputs.

    The acquisition artifact's own benchmark/pilot flags are never trusted as
    evidence. Even a ready artifact must still pass canonical service-truth
    admission before any downstream benchmark use can be considered.
    """

    if not isinstance(artifact, Mapping):
        raise ValueError("artifact must be a mapping")

    measured_rows = artifact.get("measured_rows", [])
    if isinstance(measured_rows, (str, bytes)) or not isinstance(measured_rows, Sequence):
        raise ValueError("measured_rows must be a sequence")

    field_provenance = artifact.get("field_provenance", {})
    if not isinstance(field_provenance, Mapping):
        raise ValueError("field_provenance must be a mapping")

    dataset_validation = validate_service_truth_dataset(
        measured_rows,
        require_measured=True,
    )
    conditional_source_fields = _conditionally_required_source_fields(measured_rows)
    source_contract_validation = validate_service_truth_source_contract(
        field_provenance,
        additional_required_fields=sorted(conditional_source_fields),
    )

    reasons: list[str] = []
    if not measured_rows:
        _append_unique(reasons, "MEASURED_ROWS_REQUIRED")
    elif dataset_validation["validation_status"] != "ACCEPTED_MEASURED":
        _append_unique(reasons, "MEASURED_DATASET_NOT_ACCEPTED")

    if source_contract_validation["source_contract_verified"] is not True:
        _append_unique(reasons, "SOURCE_CONTRACT_UNVERIFIED")

    if artifact.get("benchmark_eligible") is True or artifact.get("pilot_evidence_eligible") is True:
        _append_unique(reasons, "DECLARED_ELIGIBILITY_NOT_TRUSTED")

    ready = not reasons
    validation_status = (
        "READY_FOR_SERVICE_TRUTH_VALIDATION" if ready else "ACQUISITION_BLOCKED"
    )

    return {
        "validation_status": validation_status,
        "ready_for_service_truth_validation": ready,
        "benchmark_eligible": False,
        "pilot_evidence_eligible": False,
        "reason_codes": reasons,
        "dataset_validation": dataset_validation,
        "source_contract_validation": source_contract_validation,
        "result_scope": "SERVICE_TRUTH_ACQUISITION_READINESS_ONLY",
        "claim_boundary": (
            "Acquisition readiness only permits the artifact to proceed to canonical "
            "service-truth admission. It does not establish benchmark eligibility, pilot "
            "evidence, source accuracy, operational impact, savings, or automatic action."
        ),
    }
