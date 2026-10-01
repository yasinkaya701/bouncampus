from __future__ import annotations

import importlib.util
import math
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any


def _load_contract():
    try:
        from app.decision import campus_contract as contract  # type: ignore

        return contract
    except ModuleNotFoundError:
        path = Path(__file__).with_name("campus_contract.py")
        spec = importlib.util.spec_from_file_location("campus_contract_fallback", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load campus contract from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


CONTRACT = _load_contract()
CONTRACT_VERSION = CONTRACT.CONTRACT_VERSION
REQUIRED_SOURCES = ("schedule", "occupancy_model")
OPTIONAL_SOURCES = ("events", "weather")
SOURCE_NAMES = (*REQUIRED_SOURCES, *OPTIONAL_SOURCES)

LIMITATIONS = (
    "NO_LIVE_TELEMETRY_CLAIM",
    "NO_LIVE_BMS_CLAIM",
    "NO_LIVE_TURNSTILE_OR_WIFI_OCCUPANCY_CLAIM",
    "AGGREGATE_DECISION_SUPPORT_ONLY",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _finite_nonnegative(value: Any, *, field: str) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(numeric) or numeric < 0:
        raise ValueError(f"{field} must be finite and non-negative")
    return numeric


def _positive(value: Any, *, field: str) -> float:
    numeric = _finite_nonnegative(value, field=field)
    if numeric <= 0:
        raise ValueError(f"{field} must be greater than zero")
    return numeric


def _parse_timestamp(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be an ISO-8601 timestamp with timezone")
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone information")
    return parsed


def _normalize_source(
    source_name: str,
    payload: Mapping[str, Any] | None,
    *,
    decision_time: datetime,
    reason_codes: list[str],
) -> dict[str, Any]:
    item = dict(payload or {})
    available = bool(item.get("available", False))
    provenance = str(item.get("provenance", "")).upper()
    published_at_raw = item.get("published_at")
    accepted = False

    if available:
        if provenance not in CONTRACT.PROVENANCE_STATES:
            reason_codes.append(f"INVALID_SOURCE_PROVENANCE_{source_name.upper()}")
        elif published_at_raw is None:
            reason_codes.append(f"MISSING_SOURCE_TIMESTAMP_{source_name.upper()}")
        else:
            published_at = _parse_timestamp(
                published_at_raw, field=f"sources.{source_name}.published_at"
            )
            if published_at > decision_time:
                reason_codes.append(
                    f"SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_{source_name.upper()}"
                )
            else:
                accepted = True
    else:
        reason_codes.append(f"MISSING_SOURCE_{source_name.upper()}")

    return {
        "available": available,
        "accepted_at_decision_time": accepted,
        "provenance": provenance or None,
        "published_at": published_at_raw,
    }


def _normalize_zone(zone: Mapping[str, Any], reason_codes: list[str]) -> dict[str, Any]:
    zone_id = str(zone.get("zone_id", "")).strip()
    campus = str(zone.get("campus", "")).strip().lower()
    if not zone_id:
        raise ValueError("zone_id is required")
    if not campus:
        raise ValueError(f"campus is required for zone {zone_id}")

    capacity = _positive(zone.get("capacity"), field=f"zone {zone_id} capacity")
    occupancy = _finite_nonnegative(
        zone.get("occupancy_estimate", 0), field=f"zone {zone_id} occupancy_estimate"
    )
    scheduled = _finite_nonnegative(
        zone.get("scheduled_load", 0), field=f"zone {zone_id} scheduled_load"
    )
    event_load = _finite_nonnegative(
        zone.get("event_load", 0), field=f"zone {zone_id} event_load"
    )

    bounded_occupancy = occupancy
    if occupancy > capacity:
        bounded_occupancy = capacity
        reason_codes.append(f"OCCUPANCY_EXCEEDS_CAPACITY_{zone_id.upper()}")
    if scheduled + event_load > capacity:
        reason_codes.append(f"SCHEDULED_LOAD_EXCEEDS_CAPACITY_{zone_id.upper()}")

    return {
        "zone_id": zone_id,
        "campus": campus,
        "capacity": int(round(capacity)),
        "occupancy_estimate": int(round(bounded_occupancy)),
        "scheduled_load": int(round(scheduled)),
        "event_load": int(round(event_load)),
        "utilization_pct": round((bounded_occupancy / capacity) * 100.0, 2),
        "state_provenance": "MODEL_ESTIMATE",
    }


def build_campus_state(
    zones: Sequence[Mapping[str, Any]],
    sources: Mapping[str, Mapping[str, Any]] | None,
    *,
    decision_time: str,
) -> dict[str, Any]:
    """Build a decision-time-safe aggregate campus state snapshot.

    The state engine accepts only aggregate zone records. Required sources must have
    been available by the decision cutoff; future information is never silently used.
    Even with complete context, the pre-pilot engine remains REVIEW_REQUIRED rather
    than claiming operational readiness from synthetic/model-only data.
    """

    CONTRACT.validate_no_person_level_data(zones, path="zones")
    CONTRACT.validate_no_person_level_data(sources or {}, path="sources")

    cutoff = _parse_timestamp(decision_time, field="decision_time")
    reason_codes: list[str] = []

    source_status = {
        name: _normalize_source(
            name,
            (sources or {}).get(name),
            decision_time=cutoff,
            reason_codes=reason_codes,
        )
        for name in SOURCE_NAMES
        if name in REQUIRED_SOURCES or name in (sources or {})
    }

    normalized_zones: list[dict[str, Any]] = []
    seen_zone_ids: set[str] = set()
    for raw_zone in zones:
        zone = _normalize_zone(raw_zone, reason_codes)
        if zone["zone_id"] in seen_zone_ids:
            raise ValueError(f"duplicate zone_id: {zone['zone_id']}")
        seen_zone_ids.add(zone["zone_id"])
        normalized_zones.append(zone)

    campus_totals: dict[str, dict[str, Any]] = {}
    for zone in normalized_zones:
        campus = zone["campus"]
        bucket = campus_totals.setdefault(
            campus,
            {"capacity": 0, "occupancy_estimate": 0, "scheduled_load": 0, "event_load": 0},
        )
        bucket["capacity"] += zone["capacity"]
        bucket["occupancy_estimate"] += zone["occupancy_estimate"]
        bucket["scheduled_load"] += zone["scheduled_load"]
        bucket["event_load"] += zone["event_load"]

    for bucket in campus_totals.values():
        capacity = bucket["capacity"]
        bucket["utilization_pct"] = (
            round((bucket["occupancy_estimate"] / capacity) * 100.0, 2)
            if capacity > 0
            else 0.0
        )

    required_unusable = [
        name
        for name in REQUIRED_SOURCES
        if not source_status.get(name, {}).get("accepted_at_decision_time", False)
    ]
    if not normalized_zones:
        readiness = "WITHHOLD"
        reason_codes.insert(0, "NO_ZONE_STATE")
    elif required_unusable:
        readiness = "WITHHOLD"
        for name in required_unusable:
            missing_code = f"MISSING_REQUIRED_SOURCE_{name.upper()}"
            if missing_code not in reason_codes:
                reason_codes.insert(0, missing_code)
    else:
        readiness = "REVIEW_REQUIRED"
        reason_codes.insert(0, "PRE_PILOT_OPERATOR_REVIEW_REQUIRED")

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_time": decision_time,
        "state_provenance": "MODEL_ESTIMATE",
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": readiness,
        "abstained": readiness == "WITHHOLD",
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "source_status": source_status,
        "zones": normalized_zones,
        "campus_totals": campus_totals,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "limitations": list(LIMITATIONS),
    }
