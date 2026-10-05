"""Fail-closed admission for EE Solar Validation Node observations.

EE owns sensor selection, placement design, calibration/reference methods,
uncertainty/error budgets, model-vs-measurement acceptance criteria, and field
validation. CS1 validates only the caller-supplied event/provenance contract and
keeps admitted observations descriptive; admission does not validate the solar
model or authorize a campus decision.
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

_IDENTITY_FIELD_NAMES = frozenset(
    {
        "studentid",
        "studentnumber",
        "studentno",
        "studentname",
        "personid",
        "personname",
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
    """Detect direct/account identity keys anywhere in a JSON-like payload."""

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


def _finite_number(
    value: Any,
    *,
    low: float | None = None,
    high: float | None = None,
) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    if low is not None and number < low:
        return None
    if high is not None and number > high:
        return None
    return number


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _event_fingerprint(
    *,
    event_id: str,
    device_id: str,
    station_id: str,
    timestamp: datetime,
    measurement_type: str,
    value: float,
    unit: str,
    orientation_deg: float,
    tilt_deg: float,
    placement: Mapping[str, Any],
    quality: str,
    calibration_version: str,
    firmware_version: str,
    schema_version: str,
    evidence_class: str,
) -> str:
    canonical = {
        "calibrationVersion": calibration_version,
        "deviceId": device_id,
        "eventId": event_id,
        "evidenceClass": evidence_class,
        "firmwareVersion": firmware_version,
        "measurementType": measurement_type,
        "orientationDeg": orientation_deg,
        "placement": placement,
        "quality": quality,
        "schemaVersion": schema_version,
        "stationId": station_id,
        "tiltDeg": tilt_deg,
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


def validate_solar_validation_event(event: Mapping[str, Any]) -> dict[str, object]:
    """Validate one solar-node event without promoting it to model truth."""

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")

    reasons: list[str] = []
    event_id = _text(event.get("eventId"))
    device_id = _text(event.get("deviceId"))
    station_id = _text(event.get("stationId"))
    timestamp = _aware_timestamp(event.get("timestamp"))
    measurement_type = _text(event.get("measurementType"))
    value = _finite_number(event.get("value"))
    unit = _text(event.get("unit"))
    orientation_deg = _finite_number(event.get("orientationDeg"), low=0.0, high=360.0)
    tilt_deg = _finite_number(event.get("tiltDeg"), low=0.0, high=90.0)
    raw_placement = event.get("placement")
    placement = raw_placement if isinstance(raw_placement, Mapping) and raw_placement else None
    quality = _text(event.get("quality"))
    calibration_version = _text(event.get("calibrationVersion"))
    firmware_version = _text(event.get("firmwareVersion"))
    schema_version = _text(event.get("schemaVersion"))
    evidence_class = _text(event.get("evidenceClass"))

    required_text = (
        (event_id, "EVENT_ID_REQUIRED"),
        (device_id, "DEVICE_ID_REQUIRED"),
        (station_id, "STATION_ID_REQUIRED"),
        (measurement_type, "MEASUREMENT_TYPE_REQUIRED"),
        (unit, "UNIT_REQUIRED"),
        (quality, "QUALITY_REQUIRED"),
        (calibration_version, "CALIBRATION_VERSION_REQUIRED"),
        (firmware_version, "FIRMWARE_VERSION_REQUIRED"),
        (schema_version, "SCHEMA_VERSION_REQUIRED"),
        (evidence_class, "EVIDENCE_CLASS_REQUIRED"),
    )
    for candidate, reason in required_text:
        if candidate is None:
            _append_unique(reasons, reason)

    if timestamp is None:
        _append_unique(reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
    if value is None:
        _append_unique(reasons, "INVALID_MEASUREMENT_VALUE")
    if orientation_deg is None:
        _append_unique(
            reasons,
            "INVALID_ORIENTATION_DEG" if "orientationDeg" in event else "ORIENTATION_REQUIRED",
        )
    if tilt_deg is None:
        _append_unique(reasons, "INVALID_TILT_DEG" if "tiltDeg" in event else "TILT_REQUIRED")
    if placement is None:
        _append_unique(reasons, "PLACEMENT_REQUIRED")
    if _contains_identity_field(event):
        _append_unique(reasons, "IDENTITY_BEARING_PAYLOAD_FORBIDDEN")

    structural_error = bool(reasons)
    fingerprint: str | None = None

    if not structural_error:
        assert event_id is not None
        assert device_id is not None
        assert station_id is not None
        assert timestamp is not None
        assert measurement_type is not None
        assert value is not None
        assert unit is not None
        assert orientation_deg is not None
        assert tilt_deg is not None
        assert placement is not None
        assert quality is not None
        assert calibration_version is not None
        assert firmware_version is not None
        assert schema_version is not None
        assert evidence_class is not None

        orientation_deg = 0.0 if orientation_deg == 360.0 else orientation_deg
        try:
            fingerprint = _event_fingerprint(
                event_id=event_id,
                device_id=device_id,
                station_id=station_id,
                timestamp=timestamp,
                measurement_type=measurement_type,
                value=value,
                unit=unit,
                orientation_deg=orientation_deg,
                tilt_deg=tilt_deg,
                placement=placement,
                quality=quality,
                calibration_version=calibration_version,
                firmware_version=firmware_version,
                schema_version=schema_version,
                evidence_class=evidence_class,
            )
        except (TypeError, ValueError):
            _append_unique(reasons, "PLACEMENT_MUST_BE_JSON_SERIALIZABLE")
            structural_error = True
            fingerprint = None

        if not structural_error:
            if quality != VALID_QUALITY:
                _append_unique(reasons, "MEASUREMENT_QUALITY_NOT_VALID")
            if evidence_class != PHYSICAL_EVIDENCE_CLASS:
                _append_unique(reasons, "PHYSICAL_MEASUREMENT_REQUIRED")

    if structural_error:
        status = "REJECTED"
        measurement_eligible = False
    elif reasons:
        status = "WITHHOLD"
        measurement_eligible = False
    else:
        status = "ACCEPTED_MEASURED"
        measurement_eligible = True

    safe_placement = None if status == "REJECTED" else dict(placement) if placement is not None else None

    return {
        "validation_status": status,
        "measurement_eligible": measurement_eligible,
        "decision_eligible": False,
        "model_validation_eligible": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
        "event_fingerprint_sha256": fingerprint,
        "event_id": event_id,
        "device_id": device_id,
        "station_id": station_id,
        "timestamp": timestamp.astimezone(timezone.utc).isoformat() if timestamp is not None else None,
        "measurement_type": measurement_type,
        "value": value,
        "unit": unit,
        "orientation_deg": orientation_deg,
        "tilt_deg": tilt_deg,
        "placement": safe_placement,
        "quality": quality,
        "calibration_version": calibration_version,
        "firmware_version": firmware_version,
        "schema_version": schema_version,
        "evidence_class": evidence_class,
        "reason_codes": reasons,
        "result_scope": "SOLAR_VALIDATION_PHYSICAL_OBSERVATION_ONLY",
        "claim_boundary": (
            "This is a descriptive physical measurement admission only. It does not validate "
            "the solar model, establish field accuracy, or prove HVAC, energy, comfort, or "
            "savings impact. A separately registered EE-owned model-comparison protocol is "
            "required before model validation or decision use."
        ),
    }
