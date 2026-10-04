"""Fail-closed admission contract for measured dining service truth.

This module validates whether a campus × meal-period × service-date artifact is
safe to hand to CS1 benchmark/ablation code. It never fabricates operational
rows and never upgrades generated sandbox data into measured evidence.
"""

from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

CONTRACT_VERSION = "SERVICE_TRUTH_V1"
SERVICE_LEVEL_GRANULARITY = "CAMPUS_MEAL_SERVICE"
MEASURED_EVIDENCE_CLASSES = frozenset(
    {
        "OFFICIAL_OPERATIONAL_EXPORT",
        "OPERATOR_MEASUREMENT",
        "PHYSICAL_MEASUREMENT",
    }
)
SANDBOX_EVIDENCE_CLASS = "GENERATED_SANDBOX"
ALLOWED_ROW_EVIDENCE_CLASSES = MEASURED_EVIDENCE_CLASSES | {SANDBOX_EVIDENCE_CLASS}
ALLOWED_INPUT_EVIDENCE_CLASSES = frozenset(
    {
        "OFFICIAL_PUBLIC",
        "OFFICIAL_OPERATIONAL_EXPORT",
        "OPERATOR_MEASUREMENT",
        "PHYSICAL_MEASUREMENT",
        "EXTERNAL_LIVE",
        "OFFICIAL_LIVE",
        "OFFICIAL_SNAPSHOT",
        "MODEL_ESTIMATE",
        "GENERATED_SANDBOX",
    }
)
REQUIRED_DECISION_INPUTS = frozenset({"menu", "academic_calendar"})
REQUIRED_SOURCE_CONTRACT_FIELDS = frozenset(
    {
        "actual_served",
        "produced_portions",
        "surplus_or_waste",
        "shortage_or_early_sellout",
        "operator_status_quo_quantity",
        "menu",
        "academic_calendar",
    }
)
SOURCE_CONTRACT_ENTRY_FIELDS = (
    "owner",
    "source_system",
    "availability_semantics",
)
PRIVACY_FIELD_NAMES = frozenset(
    {
        "studentid",
        "studentnumber",
        "studentno",
        "studentname",
        "personid",
        "personname",
        "passengerid",
        "passengername",
        "userid",
        "username",
        "fullname",
        "cardid",
        "carduid",
        "bucardid",
        "campuscardid",
        "nationalid",
        "identitynumber",
        "tckn",
        "tcidentitynumber",
        "email",
        "emailaddress",
        "phone",
        "phonenumber",
        "faceid",
        "faceembedding",
        "biometricid",
    }
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalized_field_name(value: Any) -> str:
    return "".join(character for character in str(value).casefold() if character.isalnum())


def _privacy_reason_codes(value: Any, *, _seen: set[int] | None = None) -> list[str]:
    """Return explicit reason codes for identity-bearing keys in JSON-like data.

    The guard is key-based rather than value-based so ordinary operational text,
    source labels, snapshot identifiers, and audit notes are not misclassified as
    personal data. Device/source/business metadata remains allowed unless its key
    explicitly represents a person, account, card/contact, or biometric identity.
    """

    seen = _seen if _seen is not None else set()
    reasons: list[str] = []

    if isinstance(value, Mapping):
        object_id = id(value)
        if object_id in seen:
            return reasons
        seen.add(object_id)
        for key, nested in value.items():
            normalized = _normalized_field_name(key)
            if normalized in PRIVACY_FIELD_NAMES:
                _append_unique(
                    reasons,
                    f"PRIVACY_FIELD_NOT_ALLOWED_{normalized.upper()}",
                )
            for reason in _privacy_reason_codes(nested, _seen=seen):
                _append_unique(reasons, reason)
        return reasons

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        object_id = id(value)
        if object_id in seen:
            return reasons
        seen.add(object_id)
        for item in value:
            for reason in _privacy_reason_codes(item, _seen=seen):
                _append_unique(reasons, reason)

    return reasons


def _aware_timestamp(value: Any) -> datetime | None:
    text = _text(value)
    if text is None:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _service_date(value: Any) -> date | None:
    text = _text(value)
    if text is None:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def _nonnegative_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _canonical_checksum(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(
        rows,
        key=lambda row: (
            str(row.get("service_date", "")),
            str(row.get("decision_cutoff_at", "")),
            str(row.get("service_id", "")),
        ),
    )
    payload = json.dumps(
        ordered,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _canonical_json_sha256(value: Any) -> str:
    try:
        payload = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("source contract must be canonical JSON-compatible data") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_service_truth_source_contract(
    field_provenance: Mapping[str, Any],
) -> dict[str, object]:
    """Validate ownership/availability metadata without upgrading it to evidence.

    Structural completeness is intentionally independent from source verification:
    an explicitly owned source can be complete while still marked ``UNVERIFIED``.
    Optional source entries are not globally required, but any optional entry that
    is declared must satisfy the same structural contract as required entries.
    """

    if not isinstance(field_provenance, Mapping):
        raise ValueError("field_provenance must be a mapping")

    declared_fields = {str(field) for field in field_provenance}
    missing = sorted(REQUIRED_SOURCE_CONTRACT_FIELDS - declared_fields)
    incomplete: list[str] = []
    unverified: list[str] = list(missing)

    for raw_field, entry in field_provenance.items():
        field = str(raw_field)
        structurally_complete = isinstance(entry, Mapping) and all(
            _text(entry.get(key)) is not None for key in SOURCE_CONTRACT_ENTRY_FIELDS
        )
        if not structurally_complete:
            incomplete.append(field)

        verification_status = (
            _text(entry.get("verification_status")) if isinstance(entry, Mapping) else None
        )
        if verification_status != "VERIFIED" and field not in unverified:
            unverified.append(field)

    incomplete.sort()
    unverified.sort()
    source_contract_complete = not missing and not incomplete
    source_contract_verified = source_contract_complete and not unverified

    return {
        "source_contract_complete": source_contract_complete,
        "source_contract_verified": source_contract_verified,
        "source_contract_sha256": _canonical_json_sha256(field_provenance),
        "required_source_contract_fields": sorted(REQUIRED_SOURCE_CONTRACT_FIELDS),
        "missing_source_contract_fields": missing,
        "incomplete_source_contract_fields": incomplete,
        "unverified_source_contract_fields": unverified,
        "result_scope": "SERVICE_TRUTH_SOURCE_CONTRACT_ONLY",
        "claim_boundary": (
            "Source ownership and availability metadata do not prove measured-data "
            "availability, benchmark eligibility, pilot readiness, or savings."
        ),
    }


def validate_service_truth_dataset(
    rows: Sequence[Mapping[str, Any]],
    *,
    require_measured: bool = True,
    min_services: int = 3,
) -> dict[str, object]:
    """Validate a service-level truth artifact before benchmark admission.

    `require_measured=True` is the production/offline-evidence path. Generated
    rows may be validated structurally only by setting it to False, and remain
    `SANDBOX_ONLY` with `eligible_for_benchmark=False`.
    """

    if isinstance(rows, (str, bytes)) or not isinstance(rows, Sequence):
        raise ValueError("rows must be a sequence of mappings")
    if isinstance(min_services, bool) or not isinstance(min_services, int) or min_services < 1:
        raise ValueError("min_services must be a positive integer")
    if not isinstance(require_measured, bool):
        raise ValueError("require_measured must be boolean")

    reasons: list[str] = []
    row_errors: dict[str, list[str]] = {}
    parsed_rows: list[tuple[date, datetime, str]] = []
    seen_service_ids: set[str] = set()
    saw_sandbox = False

    for index, raw_row in enumerate(rows):
        label = f"row:{index}"
        errors: list[str] = []
        if not isinstance(raw_row, Mapping):
            _append_unique(errors, "ROW_MUST_BE_MAPPING")
            row_errors[label] = errors
            for code in errors:
                _append_unique(reasons, code)
            continue

        for privacy_reason in _privacy_reason_codes(raw_row):
            _append_unique(errors, privacy_reason)

        service_id = _text(raw_row.get("service_id"))
        if service_id is None:
            _append_unique(errors, "SERVICE_ID_REQUIRED")
        else:
            label = service_id
            if service_id in seen_service_ids:
                _append_unique(errors, "DUPLICATE_SERVICE_ID")
            seen_service_ids.add(service_id)

        if raw_row.get("granularity") != SERVICE_LEVEL_GRANULARITY:
            _append_unique(errors, "SERVICE_LEVEL_GRANULARITY_REQUIRED")

        parsed_date = _service_date(raw_row.get("service_date"))
        if parsed_date is None:
            _append_unique(errors, "INVALID_SERVICE_DATE")

        if _text(raw_row.get("campus_id")) is None:
            _append_unique(errors, "CAMPUS_ID_REQUIRED")
        if _text(raw_row.get("meal_period")) is None:
            _append_unique(errors, "MEAL_PERIOD_REQUIRED")

        cutoff = _aware_timestamp(raw_row.get("decision_cutoff_at"))
        if cutoff is None:
            _append_unique(errors, "DECISION_CUTOFF_MUST_BE_TIMEZONE_AWARE")

        actual_served = _nonnegative_number(raw_row.get("actual_served"))
        if actual_served is None:
            _append_unique(errors, "INVALID_ACTUAL_SERVED")
        if _nonnegative_number(raw_row.get("produced_portions")) is None:
            _append_unique(errors, "INVALID_PRODUCED_PORTIONS")

        surplus = raw_row.get("actual_surplus_portions")
        waste = raw_row.get("waste_kg")
        valid_surplus = _nonnegative_number(surplus) if surplus is not None else None
        valid_waste = _nonnegative_number(waste) if waste is not None else None
        if surplus is not None and valid_surplus is None:
            _append_unique(errors, "INVALID_ACTUAL_SURPLUS_PORTIONS")
        if waste is not None and valid_waste is None:
            _append_unique(errors, "INVALID_WASTE_KG")
        if valid_surplus is None and valid_waste is None:
            _append_unique(errors, "SURPLUS_OR_WASTE_MEASUREMENT_REQUIRED")

        if not isinstance(raw_row.get("shortage_or_early_sellout"), bool):
            _append_unique(errors, "SHORTAGE_OR_EARLY_SELLOUT_MUST_BE_BOOLEAN")

        reconciled = raw_row.get("outcome_reconciled")
        if reconciled is not True:
            _append_unique(errors, "UNRECONCILED_OUTCOME")
        if _text(raw_row.get("outcome_source_record_id")) is None:
            _append_unique(errors, "OUTCOME_SOURCE_RECORD_ID_REQUIRED")

        reservation_served_present = "reservation_served" in raw_row
        unreserved_served_present = "unreserved_served" in raw_row
        if reservation_served_present or unreserved_served_present:
            if not (reservation_served_present and unreserved_served_present):
                _append_unique(errors, "SERVED_DEMAND_DECOMPOSITION_INCOMPLETE")
            else:
                reservation_served = _nonnegative_number(raw_row.get("reservation_served"))
                unreserved_served = _nonnegative_number(raw_row.get("unreserved_served"))
                if reservation_served is None or unreserved_served is None:
                    _append_unique(errors, "INVALID_SERVED_DEMAND_DECOMPOSITION")
                elif actual_served is not None and not math.isclose(
                    reservation_served + unreserved_served,
                    actual_served,
                    rel_tol=0.0,
                    abs_tol=1e-9,
                ):
                    _append_unique(errors, "SERVED_DEMAND_DECOMPOSITION_MISMATCH")

        if _nonnegative_number(raw_row.get("operator_status_quo_quantity")) is None:
            _append_unique(errors, "OPERATOR_STATUS_QUO_QUANTITY_REQUIRED")

        workflow_active = raw_row.get("reservation_workflow_active")
        if not isinstance(workflow_active, bool):
            _append_unique(errors, "RESERVATION_WORKFLOW_ACTIVE_MUST_BE_BOOLEAN")
        elif workflow_active and _nonnegative_number(
            raw_row.get("active_reservations_at_cutoff")
        ) is None:
            _append_unique(errors, "ACTIVE_RESERVATIONS_REQUIRED_FOR_ACTIVE_WORKFLOW")

        evidence_class = _text(raw_row.get("evidence_class"))
        if evidence_class not in ALLOWED_ROW_EVIDENCE_CLASSES:
            _append_unique(errors, "UNKNOWN_ROW_EVIDENCE_CLASS")
        elif evidence_class == SANDBOX_EVIDENCE_CLASS:
            saw_sandbox = True
            if require_measured:
                _append_unique(errors, "MEASURED_EVIDENCE_REQUIRED")
        elif evidence_class not in MEASURED_EVIDENCE_CLASSES:
            _append_unique(errors, "MEASURED_EVIDENCE_REQUIRED")

        decision_inputs = raw_row.get("decision_inputs")
        observed_fields: set[str] = set()
        cutoff_safe_snapshot_ids: set[str] = set()
        if not isinstance(decision_inputs, Sequence) or isinstance(
            decision_inputs, (str, bytes)
        ):
            _append_unique(errors, "DECISION_INPUTS_MUST_BE_SEQUENCE")
        else:
            for source in decision_inputs:
                if not isinstance(source, Mapping):
                    _append_unique(errors, "DECISION_INPUT_MUST_BE_MAPPING")
                    continue
                field = _text(source.get("field"))
                if field is None:
                    _append_unique(errors, "DECISION_INPUT_FIELD_REQUIRED")
                else:
                    observed_fields.add(field)
                snapshot_id = _text(source.get("snapshot_id"))
                if snapshot_id is None:
                    _append_unique(errors, "DECISION_INPUT_SNAPSHOT_ID_REQUIRED")
                available_at = _aware_timestamp(source.get("available_at"))
                if available_at is None:
                    _append_unique(errors, "DECISION_INPUT_AVAILABLE_AT_MUST_BE_TIMEZONE_AWARE")
                elif cutoff is not None and available_at > cutoff:
                    _append_unique(errors, "DECISION_INPUT_NOT_AVAILABLE_AT_CUTOFF")
                input_evidence = _text(source.get("evidence_class"))
                if input_evidence not in ALLOWED_INPUT_EVIDENCE_CLASSES:
                    _append_unique(errors, "UNKNOWN_DECISION_INPUT_EVIDENCE_CLASS")
                if (
                    snapshot_id is not None
                    and available_at is not None
                    and cutoff is not None
                    and available_at <= cutoff
                    and input_evidence in ALLOWED_INPUT_EVIDENCE_CLASSES
                ):
                    cutoff_safe_snapshot_ids.add(snapshot_id)

        for required_field in sorted(REQUIRED_DECISION_INPUTS - observed_fields):
            _append_unique(
                errors,
                f"REQUIRED_DECISION_INPUT_MISSING_{required_field.upper()}",
            )

        if workflow_active is True and "reservation" not in observed_fields:
            _append_unique(errors, "RESERVATION_DECISION_INPUT_REQUIRED")

        decision_audit = raw_row.get("decision_audit")
        if decision_audit is None:
            _append_unique(errors, "DECISION_AUDIT_REQUIRED")
        elif not isinstance(decision_audit, Mapping):
            _append_unique(errors, "DECISION_AUDIT_MUST_BE_MAPPING")
        else:
            if _text(decision_audit.get("method_version")) is None:
                _append_unique(errors, "DECISION_AUDIT_METHOD_VERSION_REQUIRED")

            has_quantity = "recommended_quantity" in decision_audit
            has_band = "recommended_quantity_band" in decision_audit
            if has_quantity and has_band:
                _append_unique(errors, "DECISION_AUDIT_AMBIGUOUS_RECOMMENDATION")
            elif not has_quantity and not has_band:
                _append_unique(errors, "DECISION_AUDIT_RECOMMENDATION_REQUIRED")
            if has_quantity and _nonnegative_number(
                decision_audit.get("recommended_quantity")
            ) is None:
                _append_unique(errors, "DECISION_AUDIT_INVALID_RECOMMENDED_QUANTITY")
            if has_band:
                band = decision_audit.get("recommended_quantity_band")
                if not isinstance(band, Mapping):
                    _append_unique(errors, "DECISION_AUDIT_INVALID_RECOMMENDED_QUANTITY_BAND")
                else:
                    lower = _nonnegative_number(band.get("lower"))
                    upper = _nonnegative_number(band.get("upper"))
                    if lower is None or upper is None or lower > upper:
                        _append_unique(
                            errors,
                            "DECISION_AUDIT_INVALID_RECOMMENDED_QUANTITY_BAND",
                        )

            operator_action = _text(decision_audit.get("operator_action"))
            if operator_action is None:
                _append_unique(errors, "DECISION_AUDIT_OPERATOR_ACTION_REQUIRED")
            elif operator_action.upper() == "OVERRIDE" and _text(
                decision_audit.get("override_reason")
            ) is None:
                _append_unique(errors, "DECISION_AUDIT_OVERRIDE_REASON_REQUIRED")

            audit_snapshot_ids = decision_audit.get("input_snapshot_ids")
            if not isinstance(audit_snapshot_ids, Sequence) or isinstance(
                audit_snapshot_ids, (str, bytes)
            ) or not audit_snapshot_ids:
                _append_unique(errors, "DECISION_AUDIT_INPUT_SNAPSHOTS_REQUIRED")
            else:
                for raw_snapshot_id in audit_snapshot_ids:
                    audit_snapshot_id = _text(raw_snapshot_id)
                    if audit_snapshot_id is None:
                        _append_unique(errors, "DECISION_AUDIT_INVALID_INPUT_SNAPSHOT_ID")
                    elif audit_snapshot_id not in cutoff_safe_snapshot_ids:
                        _append_unique(errors, "DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT")

        if parsed_date is not None and cutoff is not None and service_id is not None:
            parsed_rows.append((parsed_date, cutoff, service_id))

        if errors:
            row_errors[label] = errors
            for code in errors:
                _append_unique(reasons, code)

    if len(rows) < min_services:
        _append_unique(reasons, "INSUFFICIENT_CHRONOLOGICAL_SERVICES")

    chronological = [
        service_id
        for _, _, service_id in sorted(
            parsed_rows,
            key=lambda item: (item[0], item[1], item[2]),
        )
    ]

    mapping_rows = [row for row in rows if isinstance(row, Mapping)]
    checksum = _canonical_checksum(mapping_rows)

    if reasons:
        status = "REJECTED"
        eligible = False
    elif saw_sandbox:
        status = "SANDBOX_ONLY"
        eligible = False
        _append_unique(reasons, "GENERATED_SANDBOX_NOT_BENCHMARK_TRUTH")
    else:
        status = "ACCEPTED_MEASURED"
        eligible = True

    return {
        "validation_status": status,
        "eligible_for_benchmark": eligible,
        "contract_version": CONTRACT_VERSION,
        "service_count": len(rows),
        "chronological_service_ids": chronological,
        "artifact_checksum_sha256": checksum,
        "reason_codes": reasons,
        "row_errors": row_errors,
        "required_granularity": SERVICE_LEVEL_GRANULARITY,
        "required_decision_inputs": sorted(REQUIRED_DECISION_INPUTS),
        "result_scope": "SERVICE_TRUTH_ADMISSION_ONLY",
        "claim_boundary": (
            "Contract acceptance validates structure, provenance and decision-time availability; "
            "it does not prove forecast value, operational impact, or savings."
        ),
    }


def validate_service_truth_artifact(
    rows: Sequence[Mapping[str, Any]],
    *,
    field_provenance: Mapping[str, Any],
    require_measured: bool = True,
    min_services: int = 3,
) -> dict[str, object]:
    """Bind dataset admission and source ownership into one fail-closed decision.

    This function composes the canonical dataset and source-contract validators.
    It adds no new evidence semantics: benchmark eligibility requires both an
    ``ACCEPTED_MEASURED`` dataset and a fully verified source contract.
    """

    dataset_validation = validate_service_truth_dataset(
        rows,
        require_measured=require_measured,
        min_services=min_services,
    )
    source_contract_validation = validate_service_truth_source_contract(field_provenance)

    fingerprint_payload = {
        "contract_version": CONTRACT_VERSION,
        "dataset_checksum_sha256": dataset_validation["artifact_checksum_sha256"],
        "source_contract_checksum_sha256": source_contract_validation[
            "source_contract_sha256"
        ],
    }
    fingerprint = _canonical_json_sha256(fingerprint_payload)

    dataset_status = dataset_validation["validation_status"]
    source_complete = bool(source_contract_validation["source_contract_complete"])
    source_verified = bool(source_contract_validation["source_contract_verified"])
    reasons: list[str] = []

    if dataset_status == "SANDBOX_ONLY":
        status = "SANDBOX_ONLY"
        eligible = False
        for code in dataset_validation.get("reason_codes", []):
            _append_unique(reasons, str(code))
    elif dataset_status != "ACCEPTED_MEASURED":
        status = "DATASET_REJECTED"
        eligible = False
        _append_unique(reasons, "DATASET_NOT_ACCEPTED_MEASURED")
        for code in dataset_validation.get("reason_codes", []):
            _append_unique(reasons, str(code))
    elif not source_complete:
        status = "SOURCE_CONTRACT_INCOMPLETE"
        eligible = False
        _append_unique(reasons, "SOURCE_CONTRACT_INCOMPLETE")
    elif not source_verified:
        status = "SOURCE_CONTRACT_UNVERIFIED"
        eligible = False
        _append_unique(reasons, "SOURCE_CONTRACT_UNVERIFIED")
    else:
        status = "ACCEPTED_FOR_OFFLINE_BENCHMARK"
        eligible = True

    return {
        "validation_status": status,
        "eligible_for_benchmark": eligible,
        "contract_version": CONTRACT_VERSION,
        "dataset_validation": dataset_validation,
        "source_contract_validation": source_contract_validation,
        "artifact_admission_fingerprint_sha256": fingerprint,
        "reason_codes": reasons,
        "result_scope": "SERVICE_TRUTH_ARTIFACT_ADMISSION_ONLY",
        "claim_boundary": (
            "Artifact admission proves only structural and declared-source provenance "
            "eligibility for offline benchmark input; it does not prove data accuracy, "
            "model value, pilot readiness, operational impact, or savings."
        ),
    }
