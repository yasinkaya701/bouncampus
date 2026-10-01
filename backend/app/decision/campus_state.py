from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import math
from typing import Any

from app.decision.campus_contract import (
    CONTRACT_VERSION,
    PROVENANCE_STATES,
    decision_envelope,
    validate_no_person_level_data,
)

REQUIRED_SOURCES = ("schedule", "occupancy_model")


def _timestamp(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
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


def _nonnegative(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def build_campus_state(
    zones: Sequence[Mapping[str, Any]],
    sources: Mapping[str, Mapping[str, Any]],
    *,
    decision_time: str,
) -> dict[str, Any]:
    """Build one aggregate campus snapshot using only decision-time-available evidence."""

    validate_no_person_level_data(zones, path="zones")
    validate_no_person_level_data(sources, path="sources")
    cutoff = _timestamp(decision_time)
    if cutoff is None:
        raise ValueError("decision_time must be a timezone-aware ISO timestamp")

    source_status: dict[str, dict[str, Any]] = {}
    reasons: list[str] = []
    for source_id, raw in sources.items():
        if not isinstance(raw, Mapping):
            reasons.append(f"INVALID_SOURCE_{str(source_id).upper()}")
            continue
        available = raw.get("available") is True
        provenance = str(raw.get("provenance") or "").strip().upper()
        published = _timestamp(raw.get("published_at"))
        accepted = (
            available
            and provenance in PROVENANCE_STATES
            and published is not None
            and published <= cutoff
        )
        if available and published is not None and published > cutoff:
            reasons.append(f"SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_{str(source_id).upper()}")
        elif available and provenance not in PROVENANCE_STATES:
            reasons.append(f"UNSUPPORTED_SOURCE_PROVENANCE_{str(source_id).upper()}")
        elif available and published is None:
            reasons.append(f"INVALID_SOURCE_TIMESTAMP_{str(source_id).upper()}")
        source_status[str(source_id)] = {
            "available": available,
            "provenance": provenance or None,
            "published_at": raw.get("published_at"),
            "accepted_at_decision_time": accepted,
        }

    for required in REQUIRED_SOURCES:
        if not source_status.get(required, {}).get("accepted_at_decision_time", False):
            code = f"REQUIRED_SOURCE_UNAVAILABLE_{required.upper()}"
            if not any(required.upper() in existing for existing in reasons):
                reasons.append(code)

    normalized_zones: list[dict[str, Any]] = []
    seen: set[str] = set()
    zone_integrity_ok = True
    for raw in zones:
        if not isinstance(raw, Mapping):
            raise ValueError("zones must contain mappings")
        zone_id = str(raw.get("zone_id") or "").strip()
        campus = str(raw.get("campus") or "").strip().lower()
        capacity = _nonnegative(raw.get("capacity"))
        occupancy = _nonnegative(raw.get("occupancy_estimate"))
        scheduled = _nonnegative(raw.get("scheduled_load", 0))
        event = _nonnegative(raw.get("event_load", 0))
        if (
            not zone_id
            or zone_id in seen
            or not campus
            or capacity is None
            or capacity <= 0
            or occupancy is None
            or scheduled is None
            or event is None
        ):
            raise ValueError("invalid aggregate zone input")
        seen.add(zone_id)
        if occupancy > capacity:
            zone_integrity_ok = False
            reasons.append(f"OCCUPANCY_ESTIMATE_EXCEEDS_CAPACITY_{zone_id.upper()}")
        bounded_occupancy = min(occupancy, capacity)
        normalized_zones.append(
            {
                "zone_id": zone_id,
                "campus": campus,
                "capacity": int(round(capacity)),
                "occupancy_estimate": int(round(bounded_occupancy)),
                "scheduled_load": int(round(scheduled)),
                "event_load": int(round(event)),
                "utilization_pct": round((bounded_occupancy / capacity) * 100.0, 2),
            }
        )

    if not normalized_zones:
        reasons.append("NO_CAMPUS_ZONES")
        zone_integrity_ok = False

    required_ok = all(
        source_status.get(source, {}).get("accepted_at_decision_time", False)
        for source in REQUIRED_SOURCES
    )
    readiness = (
        "REVIEW_REQUIRED"
        if required_ok and normalized_zones and zone_integrity_ok
        else "WITHHOLD"
    )
    envelope = decision_envelope(
        readiness=readiness,
        reason_codes=reasons or ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"],
        scope="AGGREGATE_CAMPUS_STATE",
    )
    return {
        **envelope,
        "decision_time": decision_time,
        "zones": normalized_zones,
        "source_status": source_status,
        "truth_boundary": "AGGREGATE_DECISION_TIME_AVAILABLE_INPUTS_ONLY",
        "impact_claim_allowed": False,
    }
