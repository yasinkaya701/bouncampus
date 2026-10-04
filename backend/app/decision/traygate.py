"""Fail-closed CS1 contract for TrayGate captures and inference results.

This module implements the software boundary documented in
``KREATE/HARDWARE/TRAYGATE_EHB_CS1_INTERFACE.md``. It validates payload shape,
identity, timing, capture quality, inference readiness, and bounded leftover
measurements. It does not establish hardware performance, model accuracy,
mass/gram calibration, field readiness, or achieved waste reduction.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import math
from typing import Any

CAPTURE_QUALITIES = frozenset(
    {
        "VALID",
        "BLURRED",
        "UNDEREXPOSED",
        "OVEREXPOSED",
        "PARTIAL_TRAY",
        "DEPTH_INVALID",
        "DEVICE_ERROR",
    }
)
RESULT_READINESS = frozenset({"READY", "REVIEW_REQUIRED", "WITHHOLD"})


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


def _bounded_number(value: Any, *, low: float, high: float) -> bool:
    if value is None or isinstance(value, bool):
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and low <= number <= high


def _append_unique(target: list[str], code: str) -> None:
    if code not in target:
        target.append(code)


def validate_traygate_capture(capture: Mapping[str, Any]) -> dict[str, object]:
    """Validate an EHB capture before CS1 inference.

    Structurally malformed payloads are rejected. Structurally valid captures
    that are not ``VALID`` quality, or do not contain a detected tray, are
    admitted only as explicit abstentions and require ``WITHHOLD`` downstream.
    """

    if not isinstance(capture, Mapping):
        raise ValueError("capture must be a mapping")

    reasons: list[str] = []
    capture_id = _text(capture.get("captureId"))

    required_text_fields = (
        ("deviceId", "DEVICE_ID_REQUIRED"),
        ("captureId", "CAPTURE_ID_REQUIRED"),
        ("rgbFrame", "RGB_FRAME_REQUIRED"),
        ("cameraCalibrationVersion", "CAMERA_CALIBRATION_VERSION_REQUIRED"),
        ("deviceSoftwareVersion", "DEVICE_SOFTWARE_VERSION_REQUIRED"),
    )
    for field, code in required_text_fields:
        if _text(capture.get(field)) is None:
            _append_unique(reasons, code)

    if _aware_timestamp(capture.get("timestamp")) is None:
        _append_unique(reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")

    tray_detected = capture.get("trayDetected")
    if not isinstance(tray_detected, bool):
        _append_unique(reasons, "TRAY_DETECTED_MUST_BE_BOOLEAN")

    quality = _text(capture.get("captureQuality"))
    if quality not in CAPTURE_QUALITIES:
        _append_unique(reasons, "UNKNOWN_CAPTURE_QUALITY")

    structural_errors = bool(reasons)
    if structural_errors:
        status = "REJECTED"
        eligible = False
        required_readiness = "WITHHOLD"
    elif quality != "VALID":
        status = "WITHHOLD"
        eligible = False
        required_readiness = "WITHHOLD"
        _append_unique(reasons, f"CAPTURE_QUALITY_{quality}")
    elif tray_detected is not True:
        status = "WITHHOLD"
        eligible = False
        required_readiness = "WITHHOLD"
        _append_unique(reasons, "TRAY_NOT_DETECTED")
    else:
        status = "ACCEPTED"
        eligible = True
        required_readiness = None

    return {
        "validation_status": status,
        "eligible_for_inference": eligible,
        "required_readiness": required_readiness,
        "capture_id": capture_id,
        "capture_quality": quality,
        "reason_codes": reasons,
        "result_scope": "TRAYGATE_CAPTURE_ADMISSION_ONLY",
        "claim_boundary": (
            "Capture admission validates payload structure and conservative quality semantics; "
            "it does not prove hardware reliability, model accuracy, or production readiness."
        ),
    }


def validate_traygate_result(
    result: Mapping[str, Any],
    *,
    expected_capture_id: str | None = None,
) -> dict[str, object]:
    """Validate a CS1 TrayGate inference result before waste analytics.

    Only structurally valid ``READY`` results are analytics-eligible. Review or
    abstention states remain explicit and cannot silently enter downstream
    aggregates. Percentages and confidences are contract values only; they are
    not converted to mass without a separately validated calibration layer.
    """

    if not isinstance(result, Mapping):
        raise ValueError("result must be a mapping")

    reasons: list[str] = []
    capture_id = _text(result.get("captureId"))

    required_text_fields = (
        ("captureId", "CAPTURE_ID_REQUIRED"),
        ("mealId", "MEAL_ID_REQUIRED"),
        ("trayId", "TRAY_ID_REQUIRED"),
        ("modelVersion", "MODEL_VERSION_REQUIRED"),
    )
    for field, code in required_text_fields:
        if _text(result.get(field)) is None:
            _append_unique(reasons, code)

    if expected_capture_id is not None:
        expected = _text(expected_capture_id)
        if expected is None:
            raise ValueError("expected_capture_id must be a non-empty string when provided")
        if capture_id != expected:
            _append_unique(reasons, "CAPTURE_ID_MISMATCH")

    readiness = _text(result.get("readiness"))
    if readiness not in RESULT_READINESS:
        _append_unique(reasons, "UNKNOWN_READINESS")

    items = result.get("items")
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        _append_unique(reasons, "ITEMS_MUST_BE_SEQUENCE")
        materialized_items: Sequence[Any] = ()
    else:
        materialized_items = items

    if readiness == "READY" and not materialized_items:
        _append_unique(reasons, "READY_RESULT_REQUIRES_ITEMS")

    for item in materialized_items:
        if not isinstance(item, Mapping):
            _append_unique(reasons, "ITEM_MUST_BE_MAPPING")
            continue
        if _text(item.get("food")) is None:
            _append_unique(reasons, "FOOD_LABEL_REQUIRED")
        if not _bounded_number(item.get("leftoverPercent"), low=0.0, high=100.0):
            _append_unique(reasons, "INVALID_LEFTOVER_PERCENT")
        if not _bounded_number(item.get("confidence"), low=0.0, high=1.0):
            _append_unique(reasons, "INVALID_CONFIDENCE")

    structural_errors = bool(reasons)
    if structural_errors:
        status = "REJECTED"
        analytics_eligible = False
    elif readiness == "WITHHOLD":
        status = "WITHHOLD"
        analytics_eligible = False
        _append_unique(reasons, "MODEL_WITHHELD")
    elif readiness == "REVIEW_REQUIRED":
        status = "REVIEW_REQUIRED"
        analytics_eligible = False
        _append_unique(reasons, "MODEL_REVIEW_REQUIRED")
    else:
        status = "ACCEPTED"
        analytics_eligible = True

    return {
        "validation_status": status,
        "analytics_eligible": analytics_eligible,
        "capture_id": capture_id,
        "readiness": readiness,
        "reason_codes": reasons,
        "result_scope": "TRAYGATE_RESULT_ADMISSION_ONLY",
        "claim_boundary": (
            "Result admission validates bounded inference outputs and abstention semantics; "
            "it does not establish model accuracy, gram-level calibration, field performance, "
            "or achieved waste reduction."
        ),
    }
