"""Fail-closed CS1 admission for Solar Validation Node observations.

This boundary validates downstream event structure and provenance only. It does
not choose sensors, calibration, uncertainty semantics, model-vs-measurement
acceptance thresholds, or prove solar-model accuracy, HVAC impact, or energy
savings. Those measurement semantics remain owned by EE; device/firmware/comms
implementation remains owned by EHB.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any

PHYSICAL_EVIDENCE_CLASS = "PHYSICAL_MEASUREMENT"
VALID_QUALITY = "VALID"


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
    return number if math.isfinite(number) else None


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def _fingerprint(event: Mapping[str, Any], timestamp: datetime, value: float) -> str:
    canonical = {
        "calibrationVersion": _text(event.get("calibrationVersion")),
        "deviceId": _text(event.get("deviceId")),
        "eventId": _text(event.get("eventId")),
        "evidenceClass": _text(event.get("evidenceClass")),
        "firmwareVersion": _text(event.get("firmwareVersion")),
        "measurementType": _text(event.get("measurementType")),
        "orientationAzimuthDeg": _finite_number(event.get("orientationAzimuthDeg")),
        "placement": _text(event.get("placement")),
        "quality": _text(event.get("quality")),
        "schemaVersion": _text(event.get("schemaVersion")),
        "stationId": _text(event.get("stationId")),
        "tiltDeg": _finite_number(event.get("tiltDeg")),
        "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
        "unit": _text(event.get("unit")),
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
    """Validate one physical solar observation without upgrading its claim level."""

    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")

    structural: list[str] = []
    withholding: list[str] = []

    event_id = _text(event.get("eventId"))
    device_id = _text(event.get("deviceId"))
    station_id = _text(event.get("stationId"))
    timestamp = _aware_timestamp(event.get("timestamp"))
    measurement_type = _text(event.get("measurementType"))
    value = _finite_number(event.get("value"))
    unit = _text(event.get("unit"))
    orientation = _finite_number(event.get("orientationAzimuthDeg"))
    tilt = _finite_number(event.get("tiltDeg"))
    placement = _text(event.get("placement"))
    quality = _text(event.get("quality"))
    calibration_version = _text(event.get("calibrationVersion"))
    evidence_class = _text(event.get("evidenceClass"))
    firmware_version = _text(event.get("firmwareVersion"))
    schema_version = _text(event.get("schemaVersion"))

    required_text = (
        (event_id, "EVENT_ID_REQUIRED"),
        (device_id, "DEVICE_ID_REQUIRED"),
        (station_id, "STATION_ID_REQUIRED"),
        (measurement_type, "MEASUREMENT_TYPE_REQUIRED"),
        (unit, "UNIT_REQUIRED"),
        (placement, "PLACEMENT_REQUIRED"),
        (quality, "QUALITY_REQUIRED"),
        (calibration_version, "CALIBRATION_VERSION_REQUIRED"),
        (evidence_class, "EVIDENCE_CLASS_REQUIRED"),
        (firmware_version, "FIRMWARE_VERSION_REQUIRED"),
        (schema_version, "SCHEMA_VERSION_REQUIRED"),
    )
    for candidate, code in required_text:
        if candidate is None:
            _append_unique(structural, code)

    if timestamp is None:
        _append_unique(structural, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")
    if value is None:
        _append_unique(structural, "MEASUREMENT_VALUE_MUST_BE_FINITE_NUMBER")
    if orientation is None or not 0.0 <= orientation <= 360.0:
        _append_unique(structural, "ORIENTATION_AZIMUTH_OUT_OF_RANGE")
    if tilt is None or not 0.0 <= tilt <= 180.0:
        _append_unique(structural, "TILT_OUT_OF_RANGE")

    fingerprint: str | None = None
    if not structural:
        assert timestamp is not None
        assert value is not None
        fingerprint = _fingerprint(event, timestamp, value)
        if quality != VALID_QUALITY:
            _append_unique(withholding, "MEASUREMENT_QUALITY_NOT_VALID")
        if evidence_class != PHYSICAL_EVIDENCE_CLASS:
            _append_unique(withholding, "PHYSICAL_MEASUREMENT_EVIDENCE_REQUIRED")

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
        "model_validation_claim_allowed": False,
        "impact_claim_allowed": False,
        "automatic_actuation": False,
        "event_fingerprint_sha256": fingerprint,
        "reason_codes": reasons,
        "result_scope": "SOLAR_VALIDATION_PHYSICAL_OBSERVATION_ONLY",
        "claim_boundary": (
            "A validated Solar Validation Node event is a descriptive physical observation only. "
            "It does not establish calibrated model accuracy, field-validation success, HVAC impact, "
            "energy savings, or permission for automatic actuation."
        ),
    }
