"""Fail-closed prospective decision-record validation for CS1.

This module implements the audit contract described by the reservation/service
reconciliation research without claiming that a pilot has run. It deliberately
keeps the recommended/operator action payload opaque so a control surface is not
hard-coded before PMR verifies the reachable decision.
"""

from __future__ import annotations

from datetime import datetime
import math
from typing import Any, Mapping, Sequence

ALLOWED_MODES = frozenset({"SHADOW", "ADVISORY", "BOUNDED_INTERVENTION"})
ALLOWED_VERIFICATION_STATES = frozenset({"PENDING", "VERIFIED", "RECONCILIATION_REQUIRED"})
CLAIM_SCOPE = "PROSPECTIVE_AUDIT_CONTRACT_ONLY"


def _nonempty_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _non_negative_number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def _parse_timestamp(value: Any) -> datetime | None:
    text = _nonempty_text(value)
    if text is None:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _validate_optional_number(record: Mapping[str, Any], field: str, reasons: list[str]) -> None:
    value = record.get(field)
    if value is not None and _non_negative_number(value) is None:
        reasons.append(f"INVALID_{field.upper()}")


def _validate_planning_band(value: Any, reasons: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, Mapping):
        reasons.append("INVALID_PLANNING_BAND")
        return
    lower = _non_negative_number(value.get("lower"))
    upper = _non_negative_number(value.get("upper"))
    if lower is None or upper is None:
        reasons.append("INVALID_PLANNING_BAND")
    elif lower > upper:
        reasons.append("PLANNING_BAND_LOWER_EXCEEDS_UPPER")


def validate_decision_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one prospective shadow/advisory/intervention audit record.

    The validator is intentionally claim-conservative: even a fully reconciled
    record is an audit artifact, not proof of impact. It checks chronology,
    traceability, operator override semantics and minimum outcome reconciliation.
    """

    reasons: list[str] = []

    decision_id = _nonempty_text(record.get("decision_id"))
    service_id = _nonempty_text(record.get("service_id"))
    strategy_version = _nonempty_text(record.get("strategy_version"))
    if decision_id is None:
        reasons.append("DECISION_ID_REQUIRED")
    if service_id is None:
        reasons.append("SERVICE_ID_REQUIRED")
    if strategy_version is None:
        reasons.append("STRATEGY_VERSION_REQUIRED")

    mode = str(record.get("mode") or "").strip().upper()
    if mode not in ALLOWED_MODES:
        reasons.append("UNSUPPORTED_DECISION_MODE")

    cutoff = _parse_timestamp(record.get("information_cutoff_at"))
    created = _parse_timestamp(record.get("created_at"))
    freeze = _parse_timestamp(record.get("decision_freeze_at"))
    if cutoff is None:
        reasons.append("VALID_INFORMATION_CUTOFF_REQUIRED")
    if created is None:
        reasons.append("VALID_CREATED_AT_REQUIRED")
    if freeze is None:
        reasons.append("VALID_DECISION_FREEZE_REQUIRED")
    if cutoff is not None and created is not None and cutoff > created:
        reasons.append("INFORMATION_CUTOFF_AFTER_DECISION_CREATED")
    if created is not None and freeze is not None and created > freeze:
        reasons.append("DECISION_CREATED_AFTER_FREEZE")

    snapshots = record.get("input_snapshot_ids")
    if not isinstance(snapshots, Sequence) or isinstance(snapshots, (str, bytes)):
        reasons.append("INPUT_SNAPSHOT_IDS_REQUIRED")
    else:
        normalized_snapshots = [_nonempty_text(item) for item in snapshots]
        if not normalized_snapshots or any(item is None for item in normalized_snapshots):
            reasons.append("INPUT_SNAPSHOT_IDS_REQUIRED")
        elif len(set(normalized_snapshots)) != len(normalized_snapshots):
            reasons.append("DUPLICATE_INPUT_SNAPSHOT_ID")

    for field in (
        "raw_reservation_count",
        "simple_baseline",
        "model_estimate_if_any",
        "actual_served",
        "actual_surplus",
    ):
        _validate_optional_number(record, field, reasons)
    _validate_planning_band(record.get("planning_band"), reasons)

    recommended_action = record.get("recommended_action")
    if not isinstance(recommended_action, Mapping) or not recommended_action:
        reasons.append("RECOMMENDED_ACTION_REQUIRED")

    operator_action_required = mode in {"ADVISORY", "BOUNDED_INTERVENTION"}
    operator_action = record.get("operator_action")
    if operator_action_required and (
        not isinstance(operator_action, Mapping) or not operator_action
    ):
        reasons.append("OPERATOR_ACTION_REQUIRED")

    operator_override_raw = record.get("operator_override", False)
    if not isinstance(operator_override_raw, bool):
        reasons.append("OPERATOR_OVERRIDE_MUST_BE_BOOLEAN")
        operator_override = False
    else:
        operator_override = operator_override_raw
    override_reason = _nonempty_text(record.get("operator_override_reason"))
    if operator_override and override_reason is None:
        reasons.append("OVERRIDE_REASON_REQUIRED")
    if mode == "SHADOW" and operator_override:
        reasons.append("SHADOW_MODE_CANNOT_RECORD_OPERATOR_OVERRIDE")

    verification_state = str(record.get("verification_state") or "PENDING").strip().upper()
    if verification_state not in ALLOWED_VERIFICATION_STATES:
        reasons.append("UNSUPPORTED_VERIFICATION_STATE")
    elif verification_state == "RECONCILIATION_REQUIRED":
        reasons.append("OUTCOME_RECONCILIATION_REQUIRED")
    elif verification_state == "VERIFIED":
        if _non_negative_number(record.get("actual_served")) is None:
            reasons.append("VERIFIED_OUTCOME_REQUIRES_ACTUAL_SERVED")
        if _non_negative_number(record.get("actual_surplus")) is None:
            reasons.append("VERIFIED_OUTCOME_REQUIRES_ACTUAL_SURPLUS")
        if not isinstance(record.get("shortage_event"), bool):
            reasons.append("VERIFIED_OUTCOME_REQUIRES_SHORTAGE_EVENT")
        if _nonempty_text(record.get("accepted_service_record")) is None:
            reasons.append("VERIFIED_OUTCOME_REQUIRES_ACCEPTED_SERVICE_RECORD")

    record_status = "AUDIT_READY" if not reasons else "RECONCILIATION_REQUIRED"

    return {
        "record_status": record_status,
        "reason_codes": reasons,
        "decision_id": decision_id,
        "service_id": service_id,
        "mode": mode,
        "verification_state": verification_state,
        "operator_action_required": operator_action_required,
        "operator_approval_required": mode in {"ADVISORY", "BOUNDED_INTERVENTION"},
        "claim_scope": CLAIM_SCOPE,
        "impact_claim_allowed": False,
        "autonomous_dispatch_allowed": False,
        "semantics": {
            "reservation": "INTENT_SIGNAL_NOT_SERVED_DEMAND",
            "actions": "OPERATOR_DEFINED_UNTIL_PMR_VERIFIES_CONTROL_SURFACE",
            "timestamps": "TIMEZONE_AWARE_SERVICE_LEVEL_AUDIT",
            "verified_outcome": "REQUIRES_ACCEPTED_SERVICE_RECORD",
        },
    }
