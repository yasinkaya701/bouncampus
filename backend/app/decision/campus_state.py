"""Aggregate, fail-closed campus state for CS1 decision intelligence."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import importlib.util
import math
from pathlib import Path
from typing import Any

CONTRACT_VERSION = "campus-ops-v1.0"
REQUIRED_SOURCES = ("schedule", "occupancy_model")
PERSON_LEVEL_FIELDS = frozenset(
    {
        "student_id",
        "person_id",
        "email",
        "device_id",
        "wifi_client_id",
        "payment_id",
        "card_id",
    }
)


def _load_source_health():
    path = Path(__file__).with_name("source_health.py")
    spec = importlib.util.spec_from_file_location("_campus_ops_source_health", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load source-health module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _required_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _number(
    value: Any,
    *,
    field: str,
    minimum: float = 0.0,
    strictly_positive: bool = False,
) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a finite number") from exc
    if not math.isfinite(number):
        raise ValueError(f"{field} must be a finite number")
    if strictly_positive:
        if number <= 0:
            raise ValueError(f"{field} must be greater than zero")
    elif number < minimum:
        raise ValueError(f"{field} must be at least {minimum:g}")
    return number


def _normalized_zone(zone: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(zone, Mapping):
        raise ValueError("each zone must be a mapping")
    disallowed = PERSON_LEVEL_FIELDS.intersection(zone.keys())
    if disallowed:
        fields = ", ".join(sorted(disallowed))
        raise ValueError(f"person-level identifiers are not allowed in campus state: {fields}")

    zone_id = _required_text(zone.get("zone_id"), field="zone_id")
    campus = _required_text(zone.get("campus"), field=f"{zone_id}.campus")
    capacity = _number(
        zone.get("capacity"),
        field=f"{zone_id}.capacity",
        strictly_positive=True,
    )
    occupancy = _number(
        zone.get("occupancy_estimate"),
        field=f"{zone_id}.occupancy_estimate",
    )
    scheduled = _number(
        zone.get("scheduled_load"),
        field=f"{zone_id}.scheduled_load",
    )
    event = _number(
        zone.get("event_load", 0),
        field=f"{zone_id}.event_load",
    )

    return {
        "zone_id": zone_id,
        "campus": campus,
        "capacity": capacity,
        "occupancy_estimate": occupancy,
        "scheduled_load": scheduled,
        "event_load": event,
        "utilization_pct": round((occupancy / capacity) * 100.0, 2),
    }


def _compact_number(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


def build_campus_state(
    zones: Sequence[Mapping[str, Any]],
    sources: Mapping[str, Mapping[str, Any]],
    decision_time: str,
) -> dict[str, Any]:
    """Build an aggregate state using only information available at decision time."""

    if isinstance(zones, (str, bytes)) or not isinstance(zones, Sequence) or not zones:
        raise ValueError("zones must be a non-empty sequence of mappings")
    if not isinstance(sources, Mapping):
        raise ValueError("sources must be a mapping")

    normalized_zones: list[dict[str, Any]] = []
    seen_zone_ids: set[str] = set()
    for raw_zone in zones:
        zone = _normalized_zone(raw_zone)
        if zone["zone_id"] in seen_zone_ids:
            raise ValueError(f"duplicate zone_id: {zone['zone_id']}")
        seen_zone_ids.add(zone["zone_id"])
        normalized_zones.append(zone)

    source_health_module = _load_source_health()
    normalized_sources = source_health_module.normalize_sources(
        sources,
        decision_time,
        domain="campus",
    )
    by_id = {item["source_id"]: item for item in normalized_sources}

    reason_codes: list[str] = []
    withheld = False
    for required in REQUIRED_SOURCES:
        health = by_id.get(required)
        if health is None or health["status"] == "UNAVAILABLE":
            reason_codes.append(f"MISSING_REQUIRED_SOURCE_{required.upper()}")
            withheld = True
            continue
        if health["status"] == "NOT_AVAILABLE_AT_DECISION_TIME":
            reason_codes.extend(health["reason_codes"])
            withheld = True
            continue
        if health["status"] in {"STALE", "PARTIAL"} or not health["eligible_at_decision_time"]:
            reason_codes.extend(
                health["reason_codes"]
                or [f"REQUIRED_SOURCE_NOT_VERIFIED_{required.upper()}"]
            )
            withheld = True

    campus_totals: dict[str, dict[str, int | float]] = {}
    for zone in normalized_zones:
        campus = zone["campus"]
        totals = campus_totals.setdefault(
            campus,
            {
                "capacity": 0.0,
                "occupancy_estimate": 0.0,
                "scheduled_load": 0.0,
                "event_load": 0.0,
            },
        )
        for field in ("capacity", "occupancy_estimate", "scheduled_load", "event_load"):
            totals[field] += zone[field]

    for totals in campus_totals.values():
        totals["utilization_pct"] = round(
            totals["occupancy_estimate"] / totals["capacity"] * 100.0,
            2,
        )
        for field in ("capacity", "occupancy_estimate", "scheduled_load", "event_load"):
            totals[field] = _compact_number(float(totals[field]))

    readiness = "WITHHOLD" if withheld else "REVIEW_REQUIRED"
    if not reason_codes:
        reason_codes = ["OPERATOR_REVIEW_REQUIRED"]

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_time": decision_time,
        "decision_readiness": readiness,
        "abstained": withheld,
        "campus_totals": campus_totals,
        "zone_states": normalized_zones,
        "source_health": normalized_sources,
        "reason_codes": reason_codes,
        "limitations": [
            "NO_LIVE_TELEMETRY_CLAIM",
            "OCCUPANCY_IS_AGGREGATE_MODEL_ESTIMATE",
        ],
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
    }
