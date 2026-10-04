"""Fail-closed intake contract for CS1 dining service-level truth.

This module does not provide measured campus data.  It only decides whether an
incoming service row is structurally suitable for offline benchmarking and
freezes deterministic intake manifests.  Generated/sandbox evidence is never
promoted to benchmark truth.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
import hashlib
import json
import math
from typing import Any

MEASURED_EVIDENCE_CLASS = "MEASURED_SERVICE_TRUTH"
SANDBOX_EVIDENCE_CLASS = "GENERATED_SANDBOX"
ALLOWED_EVIDENCE_CLASSES = frozenset({MEASURED_EVIDENCE_CLASS, SANDBOX_EVIDENCE_CLASS})

REQUIRED_CONTEXT_SOURCES = ("menu", "academic_calendar", "weather_forecast")
REQUIRED_SOURCE_CONTRACT_FIELDS = (
    "actual_served",
    "produced_portions",
    "surplus_or_waste",
    "shortage_or_early_sellout",
    "operator_estimate",
    "menu",
    "academic_calendar",
    "weather_forecast",
)

TRUTH_BOUNDARY = "REAL_RECONCILED_SERVICE_LEVEL_MEASUREMENTS_ONLY"
RESERVATION_SEMANTICS = "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND"
PROMOTION_SCOPE = "OFFLINE_BENCHMARK_INPUT_ONLY_AFTER_REAL_MEASURED_DATA"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonnegative_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number >= 0.0


def _parse_timestamp(value: Any) -> datetime | None:
    if not _text(value) or "T" not in value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _valid_service_date(value: Any) -> bool:
    if not _text(value):
        return False
    try:
        date.fromisoformat(value.strip())
    except ValueError:
        return False
    return True


def _append_once(items: list[str], code: str) -> None:
    if code not in items:
        items.append(code)


def _validate_snapshot(
    snapshot: Any,
    *,
    label: str,
    cutoff: datetime | None,
    contract_reasons: list[str],
    known_snapshot_ids: set[str],
    require_value: bool = False,
) -> None:
    token = label.upper()
    if not isinstance(snapshot, Mapping):
        _append_once(contract_reasons, f"MISSING_OR_INVALID_SNAPSHOT_{token}")
        return

    snapshot_id = snapshot.get("snapshot_id")
    if not _text(snapshot_id):
        _append_once(contract_reasons, f"MISSING_SNAPSHOT_ID_{token}")

    available_at = _parse_timestamp(snapshot.get("available_at"))
    cutoff_safe = False
    if available_at is None:
        _append_once(contract_reasons, f"INVALID_SNAPSHOT_TIMESTAMP_{token}")
    elif cutoff is None:
        cutoff_safe = False
    elif available_at > cutoff:
        if label in REQUIRED_CONTEXT_SOURCES or label == "reservation":
            _append_once(contract_reasons, f"CONTEXT_AFTER_DECISION_CUTOFF_{token}")
        else:
            _append_once(contract_reasons, f"INPUT_AFTER_DECISION_CUTOFF_{token}")
    else:
        cutoff_safe = True

    # Only evidence that is provably available by the decision cutoff may
    # satisfy decision-audit provenance. A future snapshot can have a valid ID
    # while still being hindsight information, so it must not enter this set.
    if _text(snapshot_id) and cutoff_safe:
        known_snapshot_ids.add(snapshot_id.strip())

    if require_value and not _nonnegative_number(snapshot.get("value")):
        _append_once(contract_reasons, f"MISSING_OR_INVALID_VALUE_{token}")


def _validate_outcome(
    outcome: Any,
    *,
    contract_reasons: list[str],
) -> None:
    if not isinstance(outcome, Mapping):
        _append_once(contract_reasons, "MISSING_OR_INVALID_OUTCOME")
        return

    actual_served = outcome.get("actual_served")
    if not _nonnegative_number(actual_served):
        _append_once(contract_reasons, "MISSING_OR_INVALID_ACTUAL_SERVED")

    if not _nonnegative_number(outcome.get("produced_portions")):
        _append_once(contract_reasons, "MISSING_OR_INVALID_PRODUCED_PORTIONS")

    surplus_valid = _nonnegative_number(outcome.get("actual_surplus_portions"))
    waste_valid = _nonnegative_number(outcome.get("waste_kg"))
    if not (surplus_valid or waste_valid):
        _append_once(contract_reasons, "SURPLUS_OR_WASTE_MEASUREMENT_REQUIRED")

    if not isinstance(outcome.get("shortage_or_early_sellout"), bool):
        _append_once(contract_reasons, "MISSING_OR_INVALID_SHORTAGE_STATUS")

    if outcome.get("reconciled") is not True:
        _append_once(contract_reasons, "OUTCOME_NOT_RECONCILED")

    if not _text(outcome.get("source_record_id")):
        _append_once(contract_reasons, "OUTCOME_SOURCE_RECORD_ID_REQUIRED")

    reserved_present = "reservation_served" in outcome
    unreserved_present = "unreserved_served" in outcome
    if reserved_present or unreserved_present:
        reserved = outcome.get("reservation_served")
        unreserved = outcome.get("unreserved_served")
        if not (_nonnegative_number(reserved) and _nonnegative_number(unreserved)):
            _append_once(contract_reasons, "INVALID_SERVED_DEMAND_DECOMPOSITION")
        elif _nonnegative_number(actual_served):
            if not math.isclose(
                float(reserved) + float(unreserved),
                float(actual_served),
                rel_tol=0.0,
                abs_tol=1e-9,
            ):
                _append_once(contract_reasons, "SERVED_DEMAND_DECOMPOSITION_MISMATCH")


def _validate_reservation_context(
    reservation: Any,
    *,
    cutoff: datetime | None,
    contract_reasons: list[str],
    known_snapshot_ids: set[str],
) -> None:
    _validate_snapshot(
        reservation,
        label="reservation",
        cutoff=cutoff,
        contract_reasons=contract_reasons,
        known_snapshot_ids=known_snapshot_ids,
    )
    if not isinstance(reservation, Mapping):
        return
    if not _nonnegative_number(reservation.get("active_at_cutoff")):
        _append_once(contract_reasons, "MISSING_OR_INVALID_ACTIVE_RESERVATIONS")
    if not _text(reservation.get("coverage_scope")):
        _append_once(contract_reasons, "RESERVATION_COVERAGE_SCOPE_REQUIRED")


def _validate_decision_audit(
    audit: Any,
    *,
    known_snapshot_ids: set[str],
) -> list[str]:
    reasons: list[str] = []
    if not isinstance(audit, Mapping):
        return ["DECISION_AUDIT_MISSING"]

    if not _text(audit.get("baseline_version")):
        reasons.append("DECISION_AUDIT_BASELINE_VERSION_REQUIRED")
    if not _text(audit.get("method_version")):
        reasons.append("DECISION_AUDIT_METHOD_VERSION_REQUIRED")

    quantity_valid = _nonnegative_number(audit.get("recommended_quantity"))
    band = audit.get("recommended_band")
    band_valid = False
    if isinstance(band, Mapping):
        low = band.get("low")
        high = band.get("high")
        band_valid = (
            _nonnegative_number(low)
            and _nonnegative_number(high)
            and float(low) <= float(high)
        )
    elif isinstance(band, Sequence) and not isinstance(band, (str, bytes)) and len(band) == 2:
        low, high = band
        band_valid = (
            _nonnegative_number(low)
            and _nonnegative_number(high)
            and float(low) <= float(high)
        )
    if not (quantity_valid or band_valid):
        reasons.append("DECISION_AUDIT_RECOMMENDATION_REQUIRED")

    action = audit.get("operator_action")
    if not _text(action):
        reasons.append("DECISION_AUDIT_OPERATOR_ACTION_REQUIRED")
    elif action.strip().upper() == "OVERRIDE" and not _text(audit.get("override_reason")):
        reasons.append("DECISION_AUDIT_OVERRIDE_REASON_REQUIRED")

    input_ids = audit.get("input_snapshot_ids")
    if not isinstance(input_ids, Sequence) or isinstance(input_ids, (str, bytes)) or not input_ids:
        reasons.append("DECISION_AUDIT_INPUT_SNAPSHOTS_REQUIRED")
    else:
        normalized: list[str] = []
        for snapshot_id in input_ids:
            if not _text(snapshot_id):
                reasons.append("DECISION_AUDIT_INVALID_INPUT_SNAPSHOT_ID")
                continue
            normalized.append(snapshot_id.strip())
        if any(snapshot_id not in known_snapshot_ids for snapshot_id in normalized):
            reasons.append("DECISION_AUDIT_UNKNOWN_INPUT_SNAPSHOT")

    return list(dict.fromkeys(reasons))


def assess_service_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """Assess one service row without converting weak evidence into truth.

    ``contract_complete`` means the service-level fields and cutoff semantics are
    structurally sufficient, including a complete decision audit. It does *not*
    mean the row is measured. A row is ``benchmark_eligible`` only when the
    contract is complete and its evidence class is explicitly
    ``MEASURED_SERVICE_TRUTH``.
    """

    if not isinstance(row, Mapping):
        raise ValueError("service row must be a mapping")

    contract_reasons: list[str] = []
    evidence_reasons: list[str] = []
    known_snapshot_ids: set[str] = set()

    service_id = row.get("service_id")
    if not _text(service_id):
        contract_reasons.append("SERVICE_ID_REQUIRED")
    if not _valid_service_date(row.get("service_date")):
        contract_reasons.append("SERVICE_DATE_REQUIRED")
    if not _text(row.get("campus_id")):
        contract_reasons.append("CAMPUS_ID_REQUIRED")
    if not _text(row.get("meal_period")):
        contract_reasons.append("MEAL_PERIOD_REQUIRED")

    cutoff = _parse_timestamp(row.get("decision_cutoff_at"))
    if cutoff is None:
        contract_reasons.append("DECISION_CUTOFF_TIMESTAMP_REQUIRED")

    evidence_class = row.get("evidence_class")
    if evidence_class not in ALLOWED_EVIDENCE_CLASSES:
        contract_reasons.append("UNSUPPORTED_EVIDENCE_CLASS")
    elif evidence_class == SANDBOX_EVIDENCE_CLASS:
        evidence_reasons.append("GENERATED_SANDBOX_NOT_BENCHMARK_TRUTH")

    _validate_outcome(row.get("outcome"), contract_reasons=contract_reasons)

    _validate_snapshot(
        row.get("operator_estimate"),
        label="operator_estimate",
        cutoff=cutoff,
        contract_reasons=contract_reasons,
        known_snapshot_ids=known_snapshot_ids,
        require_value=True,
    )

    context = row.get("context")
    if not isinstance(context, Mapping):
        contract_reasons.append("MISSING_OR_INVALID_CONTEXT")
    else:
        for source_name in REQUIRED_CONTEXT_SOURCES:
            _validate_snapshot(
                context.get(source_name),
                label=source_name,
                cutoff=cutoff,
                contract_reasons=contract_reasons,
                known_snapshot_ids=known_snapshot_ids,
            )
        if "reservation" in context and context.get("reservation") is not None:
            _validate_reservation_context(
                context.get("reservation"),
                cutoff=cutoff,
                contract_reasons=contract_reasons,
                known_snapshot_ids=known_snapshot_ids,
            )

    audit_reasons = _validate_decision_audit(
        row.get("decision_audit"),
        known_snapshot_ids=known_snapshot_ids,
    )

    contract_reasons = list(dict.fromkeys(contract_reasons))
    reason_codes = list(dict.fromkeys(contract_reasons + evidence_reasons + audit_reasons))
    contract_complete = not contract_reasons and not audit_reasons
    benchmark_eligible = contract_complete and evidence_class == MEASURED_EVIDENCE_CLASS

    return {
        "service_id": service_id.strip() if _text(service_id) else None,
        "contract_complete": contract_complete,
        "benchmark_eligible": benchmark_eligible,
        "decision_audit_complete": not audit_reasons,
        "evidence_class": evidence_class,
        "reason_codes": reason_codes,
        "contract_reason_codes": contract_reasons,
        "decision_audit_reason_codes": audit_reasons,
        "truth_boundary": TRUTH_BOUNDARY,
        "reservation_semantics": RESERVATION_SEMANTICS,
    }


def _canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("dataset content must be canonical JSON-compatible data") from exc
    return hashlib.sha256(payload).hexdigest()


def _source_contract_status(field_provenance: Any) -> tuple[list[str], list[str]]:
    if not isinstance(field_provenance, Mapping):
        return list(REQUIRED_SOURCE_CONTRACT_FIELDS), list(REQUIRED_SOURCE_CONTRACT_FIELDS)

    missing: list[str] = []
    unverified: list[str] = []
    for field in REQUIRED_SOURCE_CONTRACT_FIELDS:
        entry = field_provenance.get(field)
        if not isinstance(entry, Mapping) or not all(
            _text(entry.get(key))
            for key in ("owner", "source_system", "availability_semantics")
        ):
            missing.append(field)
            unverified.append(field)
            continue
        if str(entry.get("verification_status", "")).strip().upper() != "VERIFIED":
            unverified.append(field)
    return missing, unverified


def freeze_dataset(
    rows: Sequence[Mapping[str, Any]],
    *,
    dataset_id: str,
    field_provenance: Mapping[str, Any],
) -> dict[str, Any]:
    """Freeze a deterministic intake manifest without asserting pilot readiness.

    Row order is canonicalized by ``service_id`` so the same row set yields the
    same data hash.  The manifest reports evidence/readiness counts; it never
    invents a minimum sample size or upgrades sandbox rows to real truth.
    """

    if not _text(dataset_id):
        raise ValueError("dataset_id must be a non-empty string")
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise ValueError("rows must be a sequence of service-row mappings")
    if not rows:
        raise ValueError("cannot freeze an empty dining truth dataset")

    materialized: list[Mapping[str, Any]] = []
    service_ids: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("each dataset row must be a mapping")
        service_id = row.get("service_id")
        if not _text(service_id):
            raise ValueError("all rows require a non-empty service_id before freeze")
        normalized_id = service_id.strip()
        if normalized_id in service_ids:
            raise ValueError(f"duplicate service_id: {normalized_id}")
        service_ids.append(normalized_id)
        materialized.append(row)

    canonical_rows = sorted(materialized, key=lambda row: row["service_id"].strip())
    assessments = [assess_service_row(row) for row in canonical_rows]

    missing_contract_fields, unverified_contract_fields = _source_contract_status(field_provenance)
    source_contract_complete = not missing_contract_fields
    source_contract_verified = source_contract_complete and not unverified_contract_fields

    return {
        "dataset_id": dataset_id.strip(),
        "row_count": len(canonical_rows),
        "contract_complete_row_count": sum(
            1 for item in assessments if item["contract_complete"]
        ),
        "benchmark_eligible_row_count": sum(
            1 for item in assessments if item["benchmark_eligible"]
        ),
        "generated_sandbox_row_count": sum(
            1 for item in assessments if item["evidence_class"] == SANDBOX_EVIDENCE_CLASS
        ),
        "data_sha256": _canonical_sha256(canonical_rows),
        "source_contract_sha256": _canonical_sha256(field_provenance),
        "source_contract_complete": source_contract_complete,
        "source_contract_verified": source_contract_verified,
        "missing_source_contract_fields": missing_contract_fields,
        "unverified_source_contract_fields": unverified_contract_fields,
        "row_assessments": assessments,
        "truth_boundary": TRUTH_BOUNDARY,
        "promotion_scope": PROMOTION_SCOPE,
    }
