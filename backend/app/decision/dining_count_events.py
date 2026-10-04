"""Fail-closed admission for EHB dining count-node events.

CS1 consumes anonymous Production Count, Serving Line, and Tray Return events.
EHB remains the owner of sensor choice, embedded implementation, firmware,
buffering, retry, reconnect, and delivery semantics. This module validates raw
physical events and exposes descriptive counts only. It never promotes those
counts into reconciled service truth, benchmark truth, waste/surplus truth,
shortage status, or an operator baseline.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import json
from typing import Any

PHYSICAL_SOURCE = "PHYSICAL_MEASUREMENT"
VALID_QUALITY = "VALID"
COUNT_UNIT = "count"
VALID_MEASUREMENT_TYPES = frozenset(
    {
        "PRODUCED_PORTIONS",
        "SERVED_PORTIONS",
        "RETURNED_TRAYS",
    }
)
_REQUIRED_TEXT_FIELDS = (
    ("eventId", "EVENT_ID_REQUIRED"),
    ("deviceId", "DEVICE_ID_REQUIRED"),
    ("stationId", "STATION_ID_REQUIRED"),
    ("firmwareVersion", "FIRMWARE_VERSION_REQUIRED"),
    ("schemaVersion", "SCHEMA_VERSION_REQUIRED"),
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


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


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _positive_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def _canonical_payload(event: Mapping[str, Any]) -> str | None:
    """Return a stable JSON representation for replay comparison."""

    try:
        return json.dumps(
            dict(event),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError):
        return None


def validate_dining_count_event(event: Mapping[str, Any]) -> dict[str, object]:
    """Validate one physical dining count event for descriptive CS1 use."""

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")

    reasons: list[str] = []
    text_values: dict[str, str | None] = {}
    for field, code in _REQUIRED_TEXT_FIELDS:
        value = _text(event.get(field))
        text_values[field] = value
        if value is None:
            _append_unique(reasons, code)

    parsed_timestamp = _aware_timestamp(event.get("timestamp"))
    if parsed_timestamp is None:
        _append_unique(reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")

    measurement_type = _text(event.get("measurementType"))
    if measurement_type not in VALID_MEASUREMENT_TYPES:
        _append_unique(reasons, "UNSUPPORTED_MEASUREMENT_TYPE")

    count_value = _positive_int(event.get("value"))
    if count_value is None:
        _append_unique(reasons, "COUNT_VALUE_MUST_BE_POSITIVE_INTEGER")

    unit = _text(event.get("unit"))
    if unit != COUNT_UNIT:
        _append_unique(reasons, "COUNT_UNIT_REQUIRED")

    quality = _text(event.get("quality"))
    if quality is None:
        _append_unique(reasons, "QUALITY_REQUIRED")

    source = _text(event.get("source"))
    if source is None:
        _append_unique(reasons, "SOURCE_REQUIRED")

    canonical_payload = _canonical_payload(event)
    if canonical_payload is None:
        _append_unique(reasons, "EVENT_MUST_BE_JSON_SERIALIZABLE")

    structural_error = bool(reasons)
    if not structural_error:
        assert quality is not None
        assert source is not None
        if quality != VALID_QUALITY:
            _append_unique(reasons, "MEASUREMENT_QUALITY_NOT_VALID")
        if source != PHYSICAL_SOURCE:
            _append_unique(reasons, "PHYSICAL_MEASUREMENT_REQUIRED")

    if structural_error:
        status = "REJECTED"
        eligible = False
    elif reasons:
        status = "WITHHOLD"
        eligible = False
    else:
        status = "ACCEPTED_MEASURED"
        eligible = True

    return {
        "validation_status": status,
        "descriptive_eligible": eligible,
        "benchmark_truth_eligible": False,
        "event_id": text_values["eventId"],
        "device_id": text_values["deviceId"],
        "station_id": text_values["stationId"],
        "timestamp": parsed_timestamp.isoformat() if parsed_timestamp is not None else None,
        "measurement_type": measurement_type,
        "value": count_value,
        "unit": unit,
        "quality": quality,
        "source": source,
        "firmware_version": text_values["firmwareVersion"],
        "schema_version": text_values["schemaVersion"],
        "canonical_payload": canonical_payload,
        "reason_codes": reasons,
        "result_scope": "DINING_COUNT_EVENT_ADMISSION_ONLY",
        "claim_boundary": (
            "Accepted events are anonymous descriptive physical-count evidence only. "
            "They are not reconciled actual_served, surplus/waste, shortage/sellout, "
            "operator baseline, benchmark truth, pilot evidence, or impact evidence."
        ),
    }


def aggregate_dining_count_events(
    events: Sequence[Mapping[str, Any]],
    *,
    expected_station_id: str,
    window_start: str,
    window_end: str,
) -> dict[str, object]:
    """Aggregate unique admitted count events for one station/time window.

    Identical same-eventId transport retries are deduplicated. Reusing an
    eventId with a changed JSON payload rejects the complete window because CS1
    cannot distinguish transport mutation from conflicting physical evidence.
    """

    if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
        raise ValueError("events must be a sequence of mappings")
    station_id = _text(expected_station_id)
    if station_id is None:
        raise ValueError("expected_station_id must be a non-empty string")
    start = _aware_timestamp(window_start)
    end = _aware_timestamp(window_end)
    if start is None or end is None:
        raise ValueError("window_start and window_end must be timezone-aware timestamps")
    if start >= end:
        raise ValueError("window_start must be earlier than window_end")

    hard_reasons: list[str] = []
    excluded_reason_counts: dict[str, int] = {}
    seen_event_payloads: dict[str, str] = {}
    admitted: list[dict[str, object]] = []
    idempotent_replay_count = 0

    for raw_event in events:
        if not isinstance(raw_event, Mapping):
            excluded_reason_counts["EVENT_MUST_BE_MAPPING"] = (
                excluded_reason_counts.get("EVENT_MUST_BE_MAPPING", 0) + 1
            )
            continue

        raw_event_id = _text(raw_event.get("eventId"))
        canonical_payload = _canonical_payload(raw_event)
        if raw_event_id is not None and canonical_payload is not None:
            previous = seen_event_payloads.get(raw_event_id)
            if previous is not None:
                if previous == canonical_payload:
                    idempotent_replay_count += 1
                    continue
                _append_unique(hard_reasons, "EVENT_ID_REPLAY_CONFLICT")
                continue
            seen_event_payloads[raw_event_id] = canonical_payload

        raw_station_id = _text(raw_event.get("stationId"))
        if raw_station_id is not None and raw_station_id != station_id:
            _append_unique(hard_reasons, "STATION_ID_MISMATCH")

        raw_timestamp = _aware_timestamp(raw_event.get("timestamp"))
        if raw_timestamp is not None and not (start <= raw_timestamp < end):
            _append_unique(hard_reasons, "EVENT_OUTSIDE_WINDOW")

        validation = validate_dining_count_event(raw_event)
        if validation["descriptive_eligible"] is True:
            admitted.append(validation)
        else:
            for code in validation["reason_codes"]:
                reason = str(code)
                excluded_reason_counts[reason] = excluded_reason_counts.get(reason, 0) + 1

    total_count = len(events)
    unique_count = total_count - idempotent_replay_count

    if hard_reasons:
        return {
            "aggregation_status": "REJECTED",
            "descriptive_counts_available": False,
            "benchmark_truth_eligible": False,
            "station_id": station_id,
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "total_event_count": total_count,
            "unique_event_count": unique_count,
            "idempotent_replay_count": idempotent_replay_count,
            "admitted_event_count": 0,
            "excluded_event_count": unique_count,
            "coverage_status": "NONE",
            "produced_portion_count": None,
            "served_portion_count": None,
            "returned_tray_count": None,
            "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
            "reason_codes": hard_reasons,
            "result_scope": "DINING_COUNT_EVENT_WINDOW_DESCRIPTIVE_ONLY",
            "claim_boundary": (
                "Rejected scope exposes no count aggregate and establishes no service truth, "
                "hardware performance, benchmark eligibility, or operational impact."
            ),
        }

    produced_count = sum(
        int(row["value"])
        for row in admitted
        if row["measurement_type"] == "PRODUCED_PORTIONS"
    )
    served_count = sum(
        int(row["value"])
        for row in admitted
        if row["measurement_type"] == "SERVED_PORTIONS"
    )
    returned_count = sum(
        int(row["value"])
        for row in admitted
        if row["measurement_type"] == "RETURNED_TRAYS"
    )
    admitted_count = len(admitted)
    excluded_count = max(0, unique_count - admitted_count)

    if admitted_count == 0:
        status = "NO_ADMITTED_MEASUREMENTS"
        descriptive_available = False
        coverage = "NONE"
    elif admitted_count == unique_count:
        status = "AGGREGATED"
        descriptive_available = True
        coverage = "FULL"
    else:
        status = "AGGREGATED"
        descriptive_available = True
        coverage = "PARTIAL"

    return {
        "aggregation_status": status,
        "descriptive_counts_available": descriptive_available,
        "benchmark_truth_eligible": False,
        "station_id": station_id,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "total_event_count": total_count,
        "unique_event_count": unique_count,
        "idempotent_replay_count": idempotent_replay_count,
        "admitted_event_count": admitted_count,
        "excluded_event_count": excluded_count,
        "coverage_status": coverage,
        "produced_portion_count": produced_count,
        "served_portion_count": served_count,
        "returned_tray_count": returned_count,
        "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
        "reason_codes": [],
        "result_scope": "DINING_COUNT_EVENT_WINDOW_DESCRIPTIVE_ONLY",
        "claim_boundary": (
            "These are descriptive raw count-node totals only. They do not become reconciled "
            "actual_served, surplus/waste, shortage/sellout, operator baseline, benchmark truth, "
            "pilot evidence, or achieved impact without the separate SERVICE_TRUTH_V1 process."
        ),
    }
