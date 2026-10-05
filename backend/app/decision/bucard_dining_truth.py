"""Fail-closed admission for privacy-preserving BUCard dining aggregate reports.

This validates caller-supplied campus/meal aggregates. Raw report counts are not
promoted to ``actual_served`` unless reconciliation, semantic mapping, and
correction handling are explicitly recorded.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
import hashlib
import json
from typing import Any

SERVICE_LEVEL_GRANULARITY = "CAMPUS_MEAL_SERVICE"
OFFICIAL_EXPORT_EVIDENCE = "OFFICIAL_OPERATIONAL_EXPORT"
RECONCILED_STATUS = "RECONCILED_BY_SKS"
VERIFIED_MAPPING_STATUS = "SKS_VERIFIED"

_ALLOWED_COUNT_SEMANTICS = frozenset(
    {"PASSAGE_COUNT", "MEAL_TRANSACTION_COUNT", "REPORTED_SERVED_COUNT"}
)
_ALLOWED_RECONCILIATION_STATUSES = frozenset({"UNRECONCILED", RECONCILED_STATUS})
_ALLOWED_MAPPING_STATUSES = frozenset({"UNVERIFIED", VERIFIED_MAPPING_STATUS})
_FORBIDDEN_PRIVACY_FIELDS = frozenset(
    {
        "card",
        "cardid",
        "carduid",
        "cardnumber",
        "cardtoken",
        "bucard",
        "bucardid",
        "bucarduid",
        "student",
        "studentid",
        "studentnumber",
        "studentidentity",
        "person",
        "personid",
        "personidentity",
        "user",
        "userid",
        "email",
        "emailaddress",
        "phone",
        "phonenumber",
        "identity",
        "identityid",
        "biometric",
        "biometricid",
        "face",
        "faceid",
        "faceembedding",
        "transactionid",
    }
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalized_field_name(value: Any) -> str:
    return "".join(character for character in str(value).casefold() if character.isalnum())


def _privacy_fields(value: Any, *, _seen: set[int] | None = None) -> set[str]:
    seen = _seen if _seen is not None else set()
    found: set[str] = set()
    if isinstance(value, Mapping):
        object_id = id(value)
        if object_id in seen:
            return found
        seen.add(object_id)
        for key, nested in value.items():
            normalized = _normalized_field_name(key)
            if normalized in _FORBIDDEN_PRIVACY_FIELDS:
                found.add(normalized)
            found.update(_privacy_fields(nested, _seen=seen))
        return found
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        object_id = id(value)
        if object_id in seen:
            return found
        seen.add(object_id)
        for nested in value:
            found.update(_privacy_fields(nested, _seen=seen))
    return found


def _service_date(value: Any) -> date | None:
    text = _text(value)
    if text is None:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


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


def _nonnegative_integer(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _canonical_artifact_checksum(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(
        (dict(row) for row in rows),
        key=lambda row: str(row.get("service_id", "")),
    )
    payload = json.dumps(
        ordered,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_bucard_dining_export(
    rows: Sequence[Mapping[str, Any]],
    *,
    min_services: int = 3,
) -> dict[str, object]:
    """Validate aggregate report structure and explicit reconciliation evidence."""

    if isinstance(rows, (str, bytes, bytearray)) or not isinstance(rows, Sequence):
        raise ValueError("rows must be a sequence of mappings")
    if isinstance(min_services, bool) or not isinstance(min_services, int) or min_services <= 0:
        raise ValueError("min_services must be a positive integer")

    structural_reasons: list[str] = []
    hold_reasons: list[str] = []
    row_errors: dict[str, list[str]] = {}
    seen_service_ids: set[str] = set()
    parsed_rows: list[Mapping[str, Any]] = []
    privacy_safe = True

    if len(rows) < min_services:
        _append_unique(structural_reasons, "INSUFFICIENT_SERVICE_ROWS")

    for index, raw_row in enumerate(rows):
        row_key = f"row:{index}"
        errors: list[str] = []
        if not isinstance(raw_row, Mapping):
            _append_unique(errors, "ROW_MUST_BE_MAPPING")
            row_errors[row_key] = errors
            _append_unique(structural_reasons, "ROW_MUST_BE_MAPPING")
            continue

        parsed_rows.append(raw_row)
        for field in sorted(_privacy_fields(raw_row)):
            code = f"PRIVACY_FIELD_NOT_ALLOWED_{field.upper()}"
            _append_unique(errors, code)
            _append_unique(structural_reasons, code)
            privacy_safe = False

        service_id = _text(raw_row.get("service_id"))
        if service_id is None:
            _append_unique(errors, "SERVICE_ID_REQUIRED")
        elif service_id in seen_service_ids:
            _append_unique(errors, "DUPLICATE_SERVICE_ID")
        else:
            seen_service_ids.add(service_id)
            row_key = service_id

        if raw_row.get("granularity") != SERVICE_LEVEL_GRANULARITY:
            _append_unique(errors, "GRANULARITY_MUST_BE_CAMPUS_MEAL_SERVICE")
        if _service_date(raw_row.get("service_date")) is None:
            _append_unique(errors, "SERVICE_DATE_MUST_BE_ISO_DATE")
        if _text(raw_row.get("campus_id")) is None:
            _append_unique(errors, "CAMPUS_ID_REQUIRED")
        if _text(raw_row.get("meal_period")) is None:
            _append_unique(errors, "MEAL_PERIOD_REQUIRED")
        if _nonnegative_integer(raw_row.get("count_value")) is None:
            _append_unique(errors, "COUNT_VALUE_MUST_BE_NONNEGATIVE_INTEGER")

        count_semantics = _text(raw_row.get("count_semantics"))
        if count_semantics is None:
            _append_unique(errors, "COUNT_SEMANTICS_REQUIRED")
        elif count_semantics not in _ALLOWED_COUNT_SEMANTICS:
            _append_unique(errors, "UNKNOWN_COUNT_SEMANTICS")

        if "package_meal_count" in raw_row and raw_row.get("package_meal_count") is not None:
            if _nonnegative_integer(raw_row.get("package_meal_count")) is None:
                _append_unique(errors, "PACKAGE_MEAL_COUNT_MUST_BE_NONNEGATIVE_INTEGER")

        if _aware_timestamp(raw_row.get("report_generated_at")) is None:
            _append_unique(errors, "REPORT_GENERATED_AT_MUST_BE_TIMEZONE_AWARE")
        if _text(raw_row.get("source_report_id")) is None:
            _append_unique(errors, "SOURCE_REPORT_ID_REQUIRED")
        if raw_row.get("evidence_class") != OFFICIAL_EXPORT_EVIDENCE:
            _append_unique(errors, "OFFICIAL_OPERATIONAL_EXPORT_REQUIRED")

        reconciliation_status = _text(raw_row.get("reconciliation_status"))
        if reconciliation_status not in _ALLOWED_RECONCILIATION_STATUSES:
            _append_unique(errors, "UNKNOWN_RECONCILIATION_STATUS")
        elif reconciliation_status != RECONCILED_STATUS:
            _append_unique(hold_reasons, "RECONCILIATION_REQUIRED_FOR_ACTUAL_SERVED")
        elif _text(raw_row.get("reconciliation_record_id")) is None:
            _append_unique(hold_reasons, "RECONCILIATION_RECORD_ID_REQUIRED")

        mapping_status = _text(raw_row.get("semantic_mapping_status"))
        if mapping_status not in _ALLOWED_MAPPING_STATUSES:
            _append_unique(errors, "UNKNOWN_SEMANTIC_MAPPING_STATUS")
        elif mapping_status != VERIFIED_MAPPING_STATUS:
            _append_unique(hold_reasons, "SEMANTIC_MAPPING_REQUIRED_FOR_ACTUAL_SERVED")
        elif _text(raw_row.get("semantic_mapping_version")) is None:
            _append_unique(hold_reasons, "SEMANTIC_MAPPING_VERSION_REQUIRED")

        correction_flag = raw_row.get("duplicate_reversal_rules_applied")
        if not isinstance(correction_flag, bool):
            _append_unique(errors, "DUPLICATE_REVERSAL_RULES_FLAG_REQUIRED")
        elif correction_flag is not True:
            _append_unique(hold_reasons, "DUPLICATE_REVERSAL_RULES_REQUIRED")

        try:
            json.dumps(raw_row, sort_keys=True, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError):
            _append_unique(errors, "ROW_MUST_BE_JSON_SERIALIZABLE")

        if errors:
            row_errors[row_key] = errors
            for error in errors:
                _append_unique(structural_reasons, error)

    artifact_checksum: str | None = None
    if not structural_reasons and len(parsed_rows) == len(rows):
        try:
            artifact_checksum = _canonical_artifact_checksum(parsed_rows)
        except (TypeError, ValueError):
            _append_unique(structural_reasons, "ARTIFACT_MUST_BE_JSON_SERIALIZABLE")

    reason_codes = list(structural_reasons)
    for reason in hold_reasons:
        _append_unique(reason_codes, reason)

    if structural_reasons:
        status = "REJECTED"
        eligible = False
    elif hold_reasons:
        status = "WITHHOLD_UNRECONCILED"
        eligible = False
    else:
        status = "ACCEPTED_RECONCILED_OUTCOME"
        eligible = True

    return {
        "validation_status": status,
        "eligible_as_actual_served": eligible,
        "benchmark_eligible": False,
        "decision_input_eligible": False,
        "automatic_action": False,
        "privacy_safe": privacy_safe,
        "service_count": len(rows),
        "artifact_checksum_sha256": artifact_checksum,
        "reason_codes": reason_codes,
        "row_errors": row_errors,
        "required_granularity": SERVICE_LEVEL_GRANULARITY,
        "source_system": "BUCARD_DINING_REPORT",
        "result_scope": "BUCARD_AGGREGATE_OUTCOME_ADMISSION_ONLY",
        "claim_boundary": (
            "Admission validates only caller-supplied aggregate structure and declared "
            "reconciliation, mapping, and evidence labels. Caller-supplied reconciliation, "
            "mapping, and evidence labels do not prove authenticity. Benchmark use still "
            "requires canonical validate_service_truth_artifact admission with a verified "
            "source contract and content-bound source snapshots. This adapter does not prove "
            "live access, external-source accuracy, forecast value, operational impact, "
            "savings, or authorization for automatic action."
        ),
    }


def project_reconciled_actual_served_observations(
    rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, object]]:
    """Project only reconciled aggregates into minimal service-truth observations."""

    validation = validate_bucard_dining_export(rows)
    if validation["eligible_as_actual_served"] is not True:
        raise ValueError("BUCard aggregate export is not eligible as actual_served")

    projected: list[dict[str, object]] = []
    for row in sorted(
        rows,
        key=lambda item: (
            str(item.get("service_date", "")),
            str(item.get("campus_id", "")),
            str(item.get("meal_period", "")),
            str(item.get("service_id", "")),
        ),
    ):
        projected.append(
            {
                "service_id": str(row["service_id"]),
                "service_date": str(row["service_date"]),
                "campus_id": str(row["campus_id"]),
                "meal_period": str(row["meal_period"]),
                "actual_served": int(row["count_value"]),
                "outcome_reconciled": True,
                "outcome_source_record_id": str(row["reconciliation_record_id"]),
                "evidence_class": OFFICIAL_EXPORT_EVIDENCE,
            }
        )
    return projected
