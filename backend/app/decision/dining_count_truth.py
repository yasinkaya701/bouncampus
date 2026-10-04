"""Fail-closed CS1 admission for EHB dining physical-count events.

This module consumes anonymous count events emitted by Production Count, Serving
Line, and Tray Return nodes. EHB remains the owner of sensing, firmware,
buffering/retry behavior, and physical performance. CS1 only validates the
supplied event contract and produces descriptive count totals.

Raw device counts are deliberately not promoted to reconciled service truth:
this module never emits ``actual_served``, surplus/waste, shortage, model
accuracy, or operational-impact claims. A serving-line tray count also remains
a tray count; CS1 does not assume one tray equals one produced/served portion.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
import hashlib
import json
from typing import Any

PHYSICAL_SOURCE = "PHYSICAL_MEASUREMENT"
VALID_QUALITY = "VALID"
MEASUREMENT_UNITS = {
    "PRODUCED_PORTION_DELTA": "PORTIONS",
    "SERVED_TRAY_DELTA": "TRAYS",
    "RETURNED_TRAY_DELTA": "TRAYS",
}

# The physical count contract is intentionally anonymous. These direct or
# account-linked identifiers are forbidden even when nested in metadata.
FORBIDDEN_PRIVACY_FIELDS = frozenset(
    {
        "studentid",
        "userid",
        "personid",
        "employeeid",
        "staffid",
        "reservationid",
        "email",
        "phone",
        "phonenumber",
        "fullname",
        "nationalid",
        "tckimlikno",
        "cardid",
        "carduid",
    }
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


def _positive_integer(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _normalized_key(value: Any) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum())


def _forbidden_privacy_fields(value: Any) -> set[str]:
    """Return forbidden identity-bearing keys found anywhere in JSON-like data."""

    found: set[str] = set()
    if isinstance(value, Mapping):
        for raw_key, nested in value.items():
            key = _normalized_key(raw_key)
            if key in FORBIDDEN_PRIVACY_FIELDS:
                found.add(key)
            found.update(_forbidden_privacy_fields(nested))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for nested in value:
            found.update(_forbidden_privacy_fields(nested))
    return found


def _event_fingerprint(
    *,
    event_id: str,
    device_id: str,
    station_id: str,
    timestamp: datetime,
    measurement_type: str,
    count_delta: int,
    unit: str,
    quality: str,
    source: str,
    firmware_version: str,
    schema_version: str,
) -> str:
    canonical = {
        "deviceId": device_id,
        "eventId": event_id,
        "firmwareVersion": firmware_version,
        "measurementType": measurement_type,
        "quality": quality,
        "schemaVersion": schema_version,
        "source": source,
        "stationId": station_id,
        "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
        "unit": unit,
        "value": count_delta,
    }
    payload = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_dining_count_event(event: Mapping[str, Any]) -> dict[str, object]:
    """Validate one EHB dining count event before CS1 aggregation.

    A stable anonymous ``eventId`` is mandatory so offline retries can be
    distinguished from new physical events. Structurally valid events with
    non-VALID quality or non-physical provenance remain explicit WITHHOLD
    observations rather than being silently counted. Identity-bearing fields
    are structural contract violations and are rejected even when nested.
    """

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")

    structural_reasons: list[str] = []
    withholding_reasons: list[str] = []

    event_id = _text(event.get("eventId"))
    device_id = _text(event.get("deviceId"))
    station_id = _text(event.get("stationId"))
    parsed_timestamp = _aware_timestamp(event.get("timestamp"))
    measurement_type = _text(event.get("measurementType"))
    count_delta = _positive_integer(event.get("value"))
    unit = _text(event.get("unit"))
    quality = _text(event.get("quality"))
    source = _text(event.get("source"))
    firmware_version = _text(event.get("firmwareVersion"))
    schema_version = _text(event.get("schemaVersion"))

    required_text = (
        (event_id, "EVENT_ID_REQUIRED"),
        (device_id, "DEVICE_ID_REQUIRED"),
        (station_id, "STATION_ID_REQUIRED"),
        (measurement_type, "MEASUREMENT_TYPE_REQUIRED"),
        (unit, "UNIT_REQUIRED"),
        (quality, "QUALITY_REQUIRED"),
        (source, "SOURCE_REQUIRED"),
        (firmware_version, "FIRMWARE_VERSION_REQUIRED"),
        (schema_version, "SCHEMA_VERSION_REQUIRED"),
    )
    for value, code in required_text:
        if value is None:
            _append_unique(structural_reasons, code)

    if parsed_timestamp is None:
        _append_unique(structural_reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
    if count_delta is None:
        _append_unique(structural_reasons, "VALUE_MUST_BE_POSITIVE_INTEGER")

    expected_unit = MEASUREMENT_UNITS.get(measurement_type or "")
    if measurement_type is not None and expected_unit is None:
        _append_unique(structural_reasons, "UNKNOWN_MEASUREMENT_TYPE")
    elif expected_unit is not None and unit is not None and unit != expected_unit:
        _append_unique(structural_reasons, "MEASUREMENT_UNIT_MISMATCH")

    for privacy_field in sorted(_forbidden_privacy_fields(event)):
        _append_unique(
            structural_reasons,
            f"PRIVACY_FIELD_NOT_ALLOWED_{privacy_field.upper()}",
        )

    if quality is not None and quality != VALID_QUALITY:
        _append_unique(withholding_reasons, "MEASUREMENT_QUALITY_NOT_VALID")
    if source is not None and source != PHYSICAL_SOURCE:
        _append_unique(withholding_reasons, "PHYSICAL_MEASUREMENT_REQUIRED")

    fingerprint: str | None = None
    if not structural_reasons:
        assert event_id is not None
        assert device_id is not None
        assert station_id is not None
        assert parsed_timestamp is not None
        assert measurement_type is not None
        assert count_delta is not None
        assert unit is not None
        assert quality is not None
        assert source is not None
        assert firmware_version is not None
        assert schema_version is not None
        fingerprint = _event_fingerprint(
            event_id=event_id,
            device_id=device_id,
            station_id=station_id,
            timestamp=parsed_timestamp,
            measurement_type=measurement_type,
            count_delta=count_delta,
            unit=unit,
            quality=quality,
            source=source,
            firmware_version=firmware_version,
            schema_version=schema_version,
        )

    if structural_reasons:
        status = "REJECTED"
        eligible = False
    elif withholding_reasons:
        status = "WITHHOLD"
        eligible = False
    else:
        status = "ACCEPTED_MEASURED"
        eligible = True

    reasons = structural_reasons + withholding_reasons
    return {
        "validation_status": status,
        "aggregation_eligible": eligible,
        "event_fingerprint_sha256": fingerprint,
        "event_id": event_id,
        "device_id": device_id,
        "station_id": station_id,
        "timestamp": parsed_timestamp.isoformat() if parsed_timestamp is not None else None,
        "measurement_type": measurement_type,
        "count_delta": count_delta,
        "unit": unit,
        "quality": quality,
        "source": source,
        "firmware_version": firmware_version,
        "schema_version": schema_version,
        "reason_codes": reasons,
        "reconciled_service_truth": False,
        "result_scope": "DINING_PHYSICAL_COUNT_EVENT_ADMISSION_ONLY",
        "claim_boundary": (
            "Admission validates anonymous physical count events only. It does not establish "
            "sensor field accuracy, tray-to-portion equivalence, reconciled actual served "
            "demand, surplus/waste, shortage, production effectiveness, or achieved savings."
        ),
    }


def aggregate_dining_count_events(
    events: Sequence[Mapping[str, Any]],
    *,
    expected_station_id: str,
    window_start: str,
    window_end: str,
) -> dict[str, object]:
    """Aggregate admitted count events for one station and one service window.

    Identical retries carrying the same ``eventId`` are idempotently deduplicated.
    Reusing an ``eventId`` with a changed payload, mixing stations, or supplying
    an explicit event outside the requested window rejects the complete aggregate.
    The outputs remain descriptive observed counts and are not a reconciled
    ``service_truth`` row.
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

    total_count = len(events)
    unique_event_count = 0
    idempotent_replay_count = 0
    hard_reasons: list[str] = []
    excluded_reason_counts: dict[str, int] = {}
    seen_event_payloads: dict[str, Mapping[str, Any]] = {}
    admitted: list[dict[str, object]] = []

    for raw_event in events:
        if not isinstance(raw_event, Mapping):
            unique_event_count += 1
            excluded_reason_counts["EVENT_MUST_BE_MAPPING"] = (
                excluded_reason_counts.get("EVENT_MUST_BE_MAPPING", 0) + 1
            )
            continue

        raw_event_id = _text(raw_event.get("eventId"))
        if raw_event_id is not None:
            previous = seen_event_payloads.get(raw_event_id)
            if previous is not None:
                if raw_event == previous:
                    idempotent_replay_count += 1
                    continue
                _append_unique(hard_reasons, "EVENT_ID_REPLAY_CONFLICT")
                continue
            seen_event_payloads[raw_event_id] = raw_event

        unique_event_count += 1

        raw_station_id = _text(raw_event.get("stationId"))
        if raw_station_id is not None and raw_station_id != station_id:
            _append_unique(hard_reasons, "STATION_ID_MISMATCH")

        raw_timestamp = _aware_timestamp(raw_event.get("timestamp"))
        if raw_timestamp is not None and not (start <= raw_timestamp < end):
            _append_unique(hard_reasons, "EVENT_OUTSIDE_WINDOW")

        validation = validate_dining_count_event(raw_event)
        if validation["validation_status"] == "ACCEPTED_MEASURED":
            admitted.append(validation)
            continue

        for code in validation["reason_codes"]:
            code_text = str(code)
            excluded_reason_counts[code_text] = excluded_reason_counts.get(code_text, 0) + 1

    if hard_reasons:
        return {
            "aggregation_status": "REJECTED",
            "descriptive_counts_available": False,
            "station_id": station_id,
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "total_event_count": total_count,
            "unique_event_count": unique_event_count,
            "idempotent_replay_count": idempotent_replay_count,
            "admitted_event_count": 0,
            "excluded_event_count": total_count,
            "produced_portions_observed": None,
            "served_trays_observed": None,
            "returned_trays_observed": None,
            "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
            "reason_codes": hard_reasons,
            "reconciled_service_truth": False,
            "result_scope": "DINING_PHYSICAL_COUNT_WINDOW_ONLY",
            "claim_boundary": (
                "A rejected count window exposes no descriptive totals and cannot be used as "
                "reconciled dining service truth."
            ),
        }

    totals = {
        "PRODUCED_PORTION_DELTA": 0,
        "SERVED_TRAY_DELTA": 0,
        "RETURNED_TRAY_DELTA": 0,
    }
    for event in admitted:
        measurement_type = str(event["measurement_type"])
        totals[measurement_type] += int(event["count_delta"])

    admitted_count = len(admitted)
    excluded_count = unique_event_count - admitted_count
    if admitted_count:
        status = "AGGREGATED"
        available = True
    else:
        status = "NO_ADMITTED_EVENTS"
        available = False

    return {
        "aggregation_status": status,
        "descriptive_counts_available": available,
        "station_id": station_id,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "total_event_count": total_count,
        "unique_event_count": unique_event_count,
        "idempotent_replay_count": idempotent_replay_count,
        "admitted_event_count": admitted_count,
        "excluded_event_count": excluded_count,
        "produced_portions_observed": totals["PRODUCED_PORTION_DELTA"],
        "served_trays_observed": totals["SERVED_TRAY_DELTA"],
        "returned_trays_observed": totals["RETURNED_TRAY_DELTA"],
        "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
        "reason_codes": [],
        "reconciled_service_truth": False,
        "result_scope": "DINING_PHYSICAL_COUNT_WINDOW_ONLY",
        "claim_boundary": (
            "The aggregate reports descriptive device-observed count deltas only. Serving-line "
            "tray counts remain trays and are not converted into portions or actual_served. It "
            "does not establish reconciled surplus/waste, shortage, physical field accuracy, "
            "causal impact, or achieved savings."
        ),
    }
