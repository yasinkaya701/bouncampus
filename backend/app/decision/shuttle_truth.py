"""Fail-closed admission for EE shuttle passenger-count measurements.

CS1 consumes the minimum measurement contract defined by the EE shuttle-counter
workstream. EE remains the owner of sensor geometry, calibration, uncertainty,
field accuracy, and the minimum acceptable confidence threshold. This module
only validates supplied events and produces descriptive IN/OUT count deltas.
It never upgrades a window delta into absolute vehicle occupancy.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any

PHYSICAL_EVIDENCE_CLASS = "PHYSICAL_MEASUREMENT"
VALID_QUALITY = "VALID"
VALID_DIRECTIONS = frozenset({"IN", "OUT"})
_IDENTITY_FIELD_NAMES = frozenset(
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


def _normalized_field_name(value: Any) -> str:
    return "".join(character for character in str(value).casefold() if character.isalnum())


def _contains_identity_field(value: Any, *, _seen: set[int] | None = None) -> bool:
    """Return whether a JSON-like payload contains person/card identity fields.

    Device, vehicle, station, door and firmware identifiers are operational
    identifiers and remain allowed. The guard is intentionally key-based so
    ordinary free-form sensor-health values are not misclassified as identity.
    """

    seen = _seen if _seen is not None else set()
    if isinstance(value, Mapping):
        object_id = id(value)
        if object_id in seen:
            return False
        seen.add(object_id)
        for key, nested in value.items():
            if _normalized_field_name(key) in _IDENTITY_FIELD_NAMES:
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


def _bounded_number(value: Any, *, low: float, high: float) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or not low <= number <= high:
        return None
    return number


def _confidence_threshold(value: Any) -> float:
    number = _bounded_number(value, low=0.0, high=1.0)
    if number is None:
        raise ValueError("min_measurement_confidence must be a finite number in [0, 1]")
    return number


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _event_fingerprint(
    *,
    device_id: str,
    vehicle_id: str,
    timestamp: datetime,
    direction: str,
    count_delta: int,
    quality: str,
    measurement_confidence: float,
    evidence_class: str,
) -> str:
    canonical = {
        "countDelta": count_delta,
        "deviceId": device_id,
        "direction": direction,
        "evidenceClass": evidence_class,
        "measurementConfidence": measurement_confidence,
        "quality": quality,
        "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
        "vehicleId": vehicle_id,
    }
    payload = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_shuttle_count_event(
    event: Mapping[str, Any],
    *,
    min_measurement_confidence: float,
) -> dict[str, object]:
    """Validate one EE shuttle count event before CS1 decision use.

    The caller must pass the minimum confidence already approved by the EE
    measurement owner. CS1 deliberately does not define that threshold.
    Structurally valid events with non-VALID quality, insufficient confidence,
    or non-physical provenance are retained as explicit WITHHOLD observations.
    Identity-bearing payload fields are structural privacy failures and are
    rejected before an event fingerprint can be emitted.
    """

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")
    threshold = _confidence_threshold(min_measurement_confidence)

    reasons: list[str] = []
    device_id = _text(event.get("deviceId"))
    vehicle_id = _text(event.get("vehicleId"))
    parsed_timestamp = _aware_timestamp(event.get("timestamp"))
    direction = _text(event.get("direction"))
    quality = _text(event.get("quality"))
    evidence_class = _text(event.get("evidenceClass"))
    measurement_confidence = _bounded_number(
        event.get("measurementConfidence"), low=0.0, high=1.0
    )
    raw_count_delta = event.get("countDelta")
    count_delta = (
        raw_count_delta
        if isinstance(raw_count_delta, int)
        and not isinstance(raw_count_delta, bool)
        and raw_count_delta > 0
        else None
    )

    if device_id is None:
        _append_unique(reasons, "DEVICE_ID_REQUIRED")
    if vehicle_id is None:
        _append_unique(reasons, "VEHICLE_ID_REQUIRED")
    if parsed_timestamp is None:
        _append_unique(reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
    if direction not in VALID_DIRECTIONS:
        _append_unique(reasons, "INVALID_DIRECTION")
    if count_delta is None:
        _append_unique(reasons, "COUNT_DELTA_MUST_BE_POSITIVE_INTEGER")
    if quality is None:
        _append_unique(reasons, "QUALITY_REQUIRED")
    if measurement_confidence is None:
        _append_unique(reasons, "INVALID_MEASUREMENT_CONFIDENCE")
    if evidence_class is None:
        _append_unique(reasons, "EVIDENCE_CLASS_REQUIRED")
    if _contains_identity_field(event):
        _append_unique(reasons, "IDENTITY_BEARING_PAYLOAD_FORBIDDEN")

    structural_error = bool(reasons)
    fingerprint: str | None = None
    if not structural_error:
        assert device_id is not None
        assert vehicle_id is not None
        assert parsed_timestamp is not None
        assert direction is not None
        assert count_delta is not None
        assert quality is not None
        assert measurement_confidence is not None
        assert evidence_class is not None
        fingerprint = _event_fingerprint(
            device_id=device_id,
            vehicle_id=vehicle_id,
            timestamp=parsed_timestamp,
            direction=direction,
            count_delta=count_delta,
            quality=quality,
            measurement_confidence=measurement_confidence,
            evidence_class=evidence_class,
        )

        if quality != VALID_QUALITY:
            _append_unique(reasons, "MEASUREMENT_QUALITY_NOT_VALID")
        if measurement_confidence < threshold:
            _append_unique(reasons, "MEASUREMENT_CONFIDENCE_BELOW_THRESHOLD")
        if evidence_class != PHYSICAL_EVIDENCE_CLASS:
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
        "decision_eligible": eligible,
        "event_fingerprint_sha256": fingerprint,
        "device_id": device_id,
        "vehicle_id": vehicle_id,
        "timestamp": parsed_timestamp.isoformat() if parsed_timestamp is not None else None,
        "direction": direction,
        "count_delta": count_delta,
        "measurement_confidence": measurement_confidence,
        "minimum_confidence_threshold": threshold,
        "quality": quality,
        "evidence_class": evidence_class,
        "reason_codes": reasons,
        "result_scope": "SHUTTLE_PASSENGER_COUNT_ADMISSION_ONLY",
        "claim_boundary": (
            "Admission validates supplied passenger-count events only. It does not establish "
            "sensor field accuracy, absolute occupancy, dispatch readiness, or operational impact."
        ),
    }


def aggregate_shuttle_count_events(
    events: Sequence[Mapping[str, Any]],
    *,
    expected_vehicle_id: str,
    window_start: str,
    window_end: str,
    min_measurement_confidence: float,
) -> dict[str, object]:
    """Aggregate admitted physical count events for one vehicle/time window.

    The returned ``net_count_delta`` is ``IN - OUT`` over the requested window.
    It is not absolute occupancy because no opening occupancy is established by
    this contract. Duplicate replay, cross-vehicle mixing, and explicit
    out-of-window events reject the complete aggregate.
    """

    if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
        raise ValueError("events must be a sequence of mappings")
    vehicle_id = _text(expected_vehicle_id)
    if vehicle_id is None:
        raise ValueError("expected_vehicle_id must be a non-empty string")
    start = _aware_timestamp(window_start)
    end = _aware_timestamp(window_end)
    if start is None or end is None:
        raise ValueError("window_start and window_end must be timezone-aware timestamps")
    if start >= end:
        raise ValueError("window_start must be earlier than window_end")
    threshold = _confidence_threshold(min_measurement_confidence)

    hard_reasons: list[str] = []
    excluded_reason_counts: dict[str, int] = {}
    seen_fingerprints: set[str] = set()
    admitted: list[dict[str, object]] = []

    for raw_event in events:
        if not isinstance(raw_event, Mapping):
            excluded_reason_counts["EVENT_MUST_BE_MAPPING"] = (
                excluded_reason_counts.get("EVENT_MUST_BE_MAPPING", 0) + 1
            )
            continue

        raw_vehicle_id = _text(raw_event.get("vehicleId"))
        if raw_vehicle_id is not None and raw_vehicle_id != vehicle_id:
            _append_unique(hard_reasons, "VEHICLE_ID_MISMATCH")

        raw_timestamp = _aware_timestamp(raw_event.get("timestamp"))
        if raw_timestamp is not None and not (start <= raw_timestamp < end):
            _append_unique(hard_reasons, "EVENT_OUTSIDE_WINDOW")

        validation = validate_shuttle_count_event(
            raw_event,
            min_measurement_confidence=threshold,
        )
        fingerprint = validation["event_fingerprint_sha256"]
        if isinstance(fingerprint, str):
            if fingerprint in seen_fingerprints:
                _append_unique(hard_reasons, "DUPLICATE_EVENT_FINGERPRINT")
            seen_fingerprints.add(fingerprint)

        if validation["decision_eligible"] is True:
            admitted.append(validation)
        else:
            for code in validation["reason_codes"]:
                reason = str(code)
                excluded_reason_counts[reason] = excluded_reason_counts.get(reason, 0) + 1

    total_count = len(events)

    if hard_reasons:
        return {
            "aggregation_status": "REJECTED",
            "descriptive_counts_available": False,
            "vehicle_id": vehicle_id,
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "total_event_count": total_count,
            "admitted_event_count": 0,
            "excluded_event_count": total_count,
            "admitted_fraction": 0.0,
            "coverage_status": "NONE",
            "in_count": None,
            "out_count": None,
            "net_count_delta": None,
            "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
            "reason_codes": hard_reasons,
            "result_scope": "SHUTTLE_PASSENGER_COUNT_WINDOW_DELTA_ONLY",
            "claim_boundary": (
                "Rejected scope exposes no count aggregate. No absolute occupancy, "
                "automatic dispatch, field-accuracy, or impact claim is produced."
            ),
        }

    in_count = sum(
        int(row["count_delta"])
        for row in admitted
        if row["direction"] == "IN"
    )
    out_count = sum(
        int(row["count_delta"])
        for row in admitted
        if row["direction"] == "OUT"
    )
    admitted_count = len(admitted)
    excluded_count = total_count - admitted_count
    admitted_fraction = admitted_count / total_count if total_count else 0.0

    if admitted_count == 0:
        status = "NO_ADMITTED_MEASUREMENTS"
        descriptive_available = False
        coverage = "NONE"
    elif admitted_count == total_count:
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
        "vehicle_id": vehicle_id,
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
        "total_event_count": total_count,
        "admitted_event_count": admitted_count,
        "excluded_event_count": excluded_count,
        "admitted_fraction": admitted_fraction,
        "coverage_status": coverage,
        "in_count": in_count,
        "out_count": out_count,
        "net_count_delta": in_count - out_count,
        "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
        "reason_codes": [],
        "result_scope": "SHUTTLE_PASSENGER_COUNT_WINDOW_DELTA_ONLY",
        "claim_boundary": (
            "This aggregate is a descriptive IN/OUT delta over one vehicle/time window. "
            "Without independently reconciled opening occupancy it is not absolute occupancy, "
            "and it does not establish field accuracy, dispatch readiness, or achieved impact."
        ),
    }
