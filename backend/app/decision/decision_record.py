from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import math
from typing import Any, Mapping, Sequence

DECISION_STAGES = ("SHADOW", "ADVISORY", "BOUNDED_INTERVENTION")
RECORD_SCOPE = "PROSPECTIVE_DECISION_AUDIT_ONLY"


def _require_text(name: str, value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{name} must be a non-empty string")
    return text


def _parse_aware_datetime(name: str, value: Any) -> datetime:
    text = _require_text(name, value)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{name} must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{name} must include a timezone offset")
    return parsed


def _optional_non_negative_number(name: str, value: Any) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric or null")
    if not math.isfinite(float(value)):
        raise ValueError(f"{name} must be finite")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _validate_action(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise ValueError(f"{name} must be a non-empty mapping")
    action_type = str(value.get("type") or "").strip()
    if not action_type:
        raise ValueError(f"{name}.type must be non-empty")
    return dict(value)


def _validate_planning_band(value: Any) -> list[float | int] | None:
    if value is None:
        return None
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 2:
        raise ValueError("planning_band must contain [lower, upper]")
    lower = _optional_non_negative_number("planning_band lower", value[0])
    upper = _optional_non_negative_number("planning_band upper", value[1])
    if lower is None or upper is None or lower > upper:
        raise ValueError("planning_band lower must be <= upper")
    return [lower, upper]


def create_decision_record(
    *,
    decision_id: str,
    service_id: str,
    created_at: str,
    information_cutoff_at: str,
    input_snapshot_ids: Sequence[str],
    strategy_version: str,
    stage: str,
    recommended_action: Mapping[str, Any],
    raw_reservation_count: float | int | None = None,
    simple_baseline: float | int | None = None,
    model_estimate_if_any: float | int | None = None,
    planning_band: Sequence[float | int] | None = None,
) -> dict[str, Any]:
    """Create an auditable pre-outcome decision record.

    The record deliberately separates pre-freeze information, recommendation,
    human action, and later measured outcome. It is not itself pilot evidence or
    an impact claim.
    """

    normalized_stage = str(stage or "").upper()
    if normalized_stage not in DECISION_STAGES:
        raise ValueError(f"stage must be one of {DECISION_STAGES}")

    created = _parse_aware_datetime("created_at", created_at)
    cutoff = _parse_aware_datetime("information_cutoff_at", information_cutoff_at)
    if cutoff > created:
        raise ValueError("information_cutoff_at cannot be after created_at")

    if not isinstance(input_snapshot_ids, Sequence) or isinstance(input_snapshot_ids, (str, bytes)):
        raise ValueError("input_snapshot_ids must be a sequence")
    normalized_snapshots = [_require_text("input_snapshot_id", item) for item in input_snapshot_ids]
    if not normalized_snapshots:
        raise ValueError("input_snapshot_ids must not be empty")
    if len(set(normalized_snapshots)) != len(normalized_snapshots):
        raise ValueError("input_snapshot_ids must be unique")

    action = _validate_action("recommended_action", recommended_action)

    return {
        "record_scope": RECORD_SCOPE,
        "decision_id": _require_text("decision_id", decision_id),
        "service_id": _require_text("service_id", service_id),
        "created_at": created_at,
        "information_cutoff_at": information_cutoff_at,
        "input_snapshot_ids": normalized_snapshots,
        "strategy_version": _require_text("strategy_version", strategy_version),
        "decision_stage": normalized_stage,
        "raw_reservation_count": _optional_non_negative_number(
            "raw_reservation_count", raw_reservation_count
        ),
        "simple_baseline": _optional_non_negative_number("simple_baseline", simple_baseline),
        "model_estimate_if_any": _optional_non_negative_number(
            "model_estimate_if_any", model_estimate_if_any
        ),
        "planning_band": _validate_planning_band(planning_band),
        "recommended_action": action,
        "operator_action": None,
        "operator_override": None,
        "operator_override_reason": None,
        "actual_served": None,
        "actual_surplus": None,
        "shortage_event": None,
        "accepted_service_record": None,
        "verification_state": "PENDING",
        "outcome_evidence_class": None,
        "operator_approval_required": normalized_stage != "SHADOW",
        "automatic_kitchen_dispatch": False,
        "generalized_impact_claim_allowed": False,
    }


def record_operator_action(
    record: Mapping[str, Any],
    operator_action: Mapping[str, Any],
    *,
    operator_override: bool,
    operator_override_reason: str | None = None,
) -> dict[str, Any]:
    if record.get("decision_stage") == "SHADOW":
        raise ValueError("shadow mode must not record operator action")
    if not isinstance(operator_override, bool):
        raise ValueError("operator_override must be boolean")
    if record.get("operator_action") is not None:
        raise ValueError("operator action is already recorded")

    action = _validate_action("operator_action", operator_action)
    recommended = record.get("recommended_action")
    if operator_override:
        reason = str(operator_override_reason or "").strip()
        if not reason:
            raise ValueError("operator override reason is required")
    else:
        if action != recommended:
            raise ValueError("non-override operator action must match recommended_action")
        reason = None

    updated = deepcopy(dict(record))
    updated["operator_action"] = action
    updated["operator_override"] = bool(operator_override)
    updated["operator_override_reason"] = reason
    return updated


def attach_service_outcome(
    record: Mapping[str, Any],
    *,
    actual_served: float | int,
    actual_surplus: float | int,
    shortage_event: bool,
    accepted_service_record: str | None,
) -> dict[str, Any]:
    if record.get("actual_served") is not None or record.get("verification_state") != "PENDING":
        raise ValueError("service outcome is already attached")

    served = _optional_non_negative_number("actual_served", actual_served)
    surplus = _optional_non_negative_number("actual_surplus", actual_surplus)
    if served is None or surplus is None:
        raise ValueError("actual_served and actual_surplus are required")
    if not isinstance(shortage_event, bool):
        raise ValueError("shortage_event must be boolean")

    accepted = str(accepted_service_record or "").strip() or None
    updated = deepcopy(dict(record))
    updated["actual_served"] = served
    updated["actual_surplus"] = surplus
    updated["shortage_event"] = shortage_event
    updated["accepted_service_record"] = accepted
    if accepted is None:
        updated["verification_state"] = "RECONCILIATION_REQUIRED"
        updated["outcome_evidence_class"] = "UNVERIFIED_SERVICE_OUTCOME"
    else:
        updated["verification_state"] = "VERIFIED"
        updated["outcome_evidence_class"] = "MEASURED_SERVICE_OUTCOME"
    updated["generalized_impact_claim_allowed"] = False
    return updated
