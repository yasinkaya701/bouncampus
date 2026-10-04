"""Fail-closed CS1 admission for anonymous RoomNode physical measurements.

The module validates downstream event semantics and emits descriptive summaries.
It does not establish sensor calibration, field accuracy, calibrated occupancy
truth, energy savings, or permission for automatic actuation. EE remains owner
of measurement/calibration/uncertainty semantics; EHB remains owner of device,
firmware, communications, buffering and retry implementation.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any

PHYSICAL_SOURCE = "PHYSICAL_MEASUREMENT"
VALID_QUALITY = "VALID"
MEASUREMENT_UNITS = {
    "OCCUPANCY_COUNT": "PEOPLE",
    "CO2_PPM": "PPM",
    "AIR_TEMPERATURE_C": "CELSIUS",
    "RELATIVE_HUMIDITY_PERCENT": "PERCENT",
}
IDENTITY_FIELD_NAMES = frozenset(
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


def _finite_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _normalized_key(value: Any) -> str:
    return "".join(character for character in str(value).casefold() if character.isalnum())


def _contains_identity_field(value: Any, *, _seen: set[int] | None = None) -> bool:
    seen = _seen if _seen is not None else set()
    if isinstance(value, Mapping):
        object_id = id(value)
        if object_id in seen:
            return False
        seen.add(object_id)
        for key, nested in value.items():
            if _normalized_key(key) in IDENTITY_FIELD_NAMES:
                return True
            if _contains_identity_field(nested, _seen=seen):
                return True
        return False
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        object_id = id(value)
        if object_id in seen:
            return False
        seen.add(object_id)
        return any(_contains_identity_field(item, _seen=seen) for item in value)
    return False


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _normalized_value(measurement_type: str | None, raw_value: Any, reasons: list[str]) -> float | None:
    if measurement_type == "OCCUPANCY_COUNT":
        if (
            isinstance(raw_value, bool)
            or not isinstance(raw_value, int)
            or raw_value < 0
        ):
            _append_unique(reasons, "OCCUPANCY_COUNT_MUST_BE_NONNEGATIVE_INTEGER")
            return None
        return float(raw_value)

    number = _finite_number(raw_value)
    if number is None:
        _append_unique(reasons, "MEASUREMENT_VALUE_MUST_BE_FINITE_NUMBER")
        return None
    if measurement_type == "CO2_PPM" and number < 0:
        _append_unique(reasons, "CO2_PPM_MUST_BE_NONNEGATIVE")
        return None
    if measurement_type == "RELATIVE_HUMIDITY_PERCENT" and not 0.0 <= number <= 100.0:
        _append_unique(reasons, "RELATIVE_HUMIDITY_OUT_OF_RANGE")
        return None
    return number


def _fingerprint(
    *,
    event_id: str,
    device_id: str,
    station_id: str,
    timestamp: datetime,
    measurement_type: str,
    value: float,
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
        "value": value,
    }
    payload = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_roomnode_event(event: Mapping[str, Any]) -> dict[str, object]:
    """Validate one RoomNode observation without upgrading its claim level."""

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")

    structural: list[str] = []
    withholding: list[str] = []

    event_id = _text(event.get("eventId"))
    device_id = _text(event.get("deviceId"))
    station_id = _text(event.get("stationId"))
    timestamp = _aware_timestamp(event.get("timestamp"))
    measurement_type = _text(event.get("measurementType"))
    unit = _text(event.get("unit"))
    quality = _text(event.get("quality"))
    source = _text(event.get("source"))
    firmware_version = _text(event.get("firmwareVersion"))
    schema_version = _text(event.get("schemaVersion"))

    if event_id is None:
        _append_unique(structural, "EVENT_ID_REQUIRED")
    if device_id is None:
        _append_unique(structural, "DEVICE_ID_REQUIRED")
    if station_id is None:
        _append_unique(structural, "STATION_ID_REQUIRED")
    if timestamp is None:
        _append_unique(structural, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
    if measurement_type not in MEASUREMENT_UNITS:
        _append_unique(structural, "UNSUPPORTED_MEASUREMENT_TYPE")
    expected_unit = MEASUREMENT_UNITS.get(measurement_type or "")
    if unit is None:
        _append_unique(structural, "UNIT_REQUIRED")
    elif expected_unit is not None and unit != expected_unit:
        _append_unique(structural, "MEASUREMENT_UNIT_MISMATCH")
    if quality is None:
        _append_unique(structural, "QUALITY_REQUIRED")
    if source is None:
        _append_unique(structural, "SOURCE_REQUIRED")
    if firmware_version is None:
        _append_unique(structural, "FIRMWARE_VERSION_REQUIRED")
    if schema_version is None:
        _append_unique(structural, "SCHEMA_VERSION_REQUIRED")
    if _contains_identity_field(event):
        _append_unique(structural, "IDENTITY_BEARING_PAYLOAD_FORBIDDEN")

    value = _normalized_value(measurement_type, event.get("value"), structural)

    fingerprint: str | None = None
    if not structural:
        assert event_id is not None
        assert device_id is not None
        assert station_id is not None
        assert timestamp is not None
        assert measurement_type is not None
        assert value is not None
        assert unit is not None
        assert quality is not None
        assert source is not None
        assert firmware_version is not None
        assert schema_version is not None
        fingerprint = _fingerprint(
            event_id=event_id,
            device_id=device_id,
            station_id=station_id,
            timestamp=timestamp,
            measurement_type=measurement_type,
            value=value,
            unit=unit,
            quality=quality,
            source=source,
            firmware_version=firmware_version,
            schema_version=schema_version,
        )
        if quality != VALID_QUALITY:
            _append_unique(withholding, "MEASUREMENT_QUALITY_NOT_VALID")
        if source != PHYSICAL_SOURCE:
            _append_unique(withholding, "PHYSICAL_MEASUREMENT_SOURCE_REQUIRED")

    if structural:
        status = "REJECTED"
        reasons = structural
    elif withholding:
        status = "WITHHOLD"
        reasons = withholding
    else:
        status = "ACCEPTED_MEASURED"
        reasons = []

    return {
        "validation_status": status,
        "measurement_eligible": status == "ACCEPTED_MEASURED",
        "decision_eligible": False,
        "event_fingerprint_sha256": fingerprint,
        "reason_codes": reasons,
        "result_scope": "ROOMNODE_PHYSICAL_OBSERVATION_ONLY",
        "impact_claim_allowed": False,
        "automatic_actuation": False,
        "claim_boundary": (
            "A validated RoomNode event is an anonymous descriptive physical observation only. "
            "It does not establish calibrated occupancy truth, sensor field accuracy, energy "
            "savings, or permission for automatic space/HVAC actuation."
        ),
    }


def summarize_roomnode_window(
    events: Sequence[Mapping[str, Any]],
    *,
    station_id: str,
    window_start: str,
    window_end: str,
) -> dict[str, object]:
    """Deduplicate and summarize one station/time window descriptively."""

    if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
        raise ValueError("events must be a sequence")
    expected_station = _text(station_id)
    start = _aware_timestamp(window_start)
    end = _aware_timestamp(window_end)
    if expected_station is None:
        raise ValueError("station_id is required")
    if start is None or end is None or start >= end:
        raise ValueError("window_start/window_end must be timezone-aware and increasing")

    hard_reasons: list[str] = []
    excluded_reason_counts: dict[str, int] = {}
    seen_event_payloads: dict[str, Mapping[str, Any]] = {}
    accepted: list[tuple[str, float, str]] = []
    unique_event_count = 0
    idempotent_replay_count = 0

    for raw_event in events:
        if not isinstance(raw_event, Mapping):
            unique_event_count += 1
            _append_unique(hard_reasons, "EVENT_MUST_BE_MAPPING")
            continue

        event_id = _text(raw_event.get("eventId"))
        if event_id is not None:
            previous = seen_event_payloads.get(event_id)
            if previous is not None:
                if raw_event == previous:
                    idempotent_replay_count += 1
                    continue
                _append_unique(hard_reasons, "EVENT_ID_REPLAY_CONFLICT")
                continue
            seen_event_payloads[event_id] = raw_event

        unique_event_count += 1
        row_station = _text(raw_event.get("stationId"))
        if row_station != expected_station:
            _append_unique(hard_reasons, "STATION_ID_MISMATCH")

        timestamp = _aware_timestamp(raw_event.get("timestamp"))
        if timestamp is not None and not (start <= timestamp < end):
            _append_unique(hard_reasons, "EVENT_OUTSIDE_WINDOW")

        validation = validate_roomnode_event(raw_event)
        status = validation["validation_status"]
        if status == "REJECTED":
            for code in validation["reason_codes"]:
                _append_unique(hard_reasons, str(code))
            continue
        if status == "WITHHOLD":
            for code in validation["reason_codes"]:
                code_text = str(code)
                excluded_reason_counts[code_text] = excluded_reason_counts.get(code_text, 0) + 1
            continue

        measurement_type = _text(raw_event.get("measurementType"))
        unit = _text(raw_event.get("unit"))
        value_reasons: list[str] = []
        value = _normalized_value(measurement_type, raw_event.get("value"), value_reasons)
        if measurement_type is not None and unit is not None and value is not None:
            accepted.append((measurement_type, value, unit))

    base = {
        "station_id": expected_station,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "total_event_count": len(events),
        "unique_event_count": unique_event_count,
        "idempotent_replay_count": idempotent_replay_count,
        "decision_eligible": False,
        "impact_claim_allowed": False,
        "automatic_actuation": False,
        "result_scope": "ROOMNODE_WINDOW_DESCRIPTIVE_ONLY",
        "claim_boundary": (
            "Window summaries are descriptive sensor observations only. Occupancy counts remain "
            "uncalibrated measurement outputs until EE-owned validation/uncertainty evidence exists; "
            "no energy savings or automatic actuation claim is produced."
        ),
    }

    if hard_reasons:
        return {
            **base,
            "aggregation_status": "REJECTED",
            "accepted_event_count": 0,
            "excluded_event_count": len(events),
            "per_measurement": {},
            "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
            "reason_codes": hard_reasons,
        }

    grouped: dict[str, dict[str, object]] = {}
    by_type: dict[str, list[tuple[float, str]]] = {}
    for measurement_type, value, unit in accepted:
        by_type.setdefault(measurement_type, []).append((value, unit))
    for measurement_type in sorted(by_type):
        values = [item[0] for item in by_type[measurement_type]]
        unit = by_type[measurement_type][0][1]
        grouped[measurement_type] = {
            "unit": unit,
            "sample_count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    accepted_count = len(accepted)
    return {
        **base,
        "aggregation_status": "DESCRIPTIVE_ONLY" if accepted_count else "WITHHOLD",
        "accepted_event_count": accepted_count,
        "excluded_event_count": unique_event_count - accepted_count,
        "per_measurement": grouped,
        "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
        "reason_codes": [] if accepted_count else ["NO_VALID_PHYSICAL_MEASUREMENTS"],
    }
