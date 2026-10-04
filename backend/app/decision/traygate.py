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
FORBIDDEN_CAPTURE_IDENTITY_FIELDS = frozenset(
    {
        "studentid",
        "personid",
        "userid",
        "bucardid",
        "faceembedding",
        "biometricid",
        "studentidentity",
        "personidentity",
    }
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _canonical_field_name(value: Any) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum())


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
    Person-identifying fields are rejected because TrayGate is an anonymous
    tray-measurement boundary rather than a person-tracking surface.
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

    for raw_field in capture:
        canonical_field = _canonical_field_name(raw_field)
        if canonical_field in FORBIDDEN_CAPTURE_IDENTITY_FIELDS:
            _append_unique(
                reasons,
                f"PRIVACY_FIELD_NOT_ALLOWED_{canonical_field.upper()}",
            )

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
            "Capture admission validates payload structure, anonymous-boundary semantics, "
            "and conservative quality handling; it does not prove hardware reliability, "
            "model accuracy, or production readiness."
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


def aggregate_traygate_service(
    results: Sequence[Mapping[str, Any]],
    *,
    expected_meal_id: str,
) -> dict[str, object]:
    """Aggregate contract-admitted TrayGate results for one meal/service.

    The aggregate is deliberately descriptive. Only valid ``READY`` results
    contribute per-food leftover percentages. Review, withheld, and malformed
    results are excluded and counted. Duplicate capture/tray identities or
    cross-meal input reject the entire aggregate to prevent silent double
    counting or service leakage.
    """

    if isinstance(results, (str, bytes)) or not isinstance(results, Sequence):
        raise ValueError("results must be a sequence of mappings")
    meal_id = _text(expected_meal_id)
    if meal_id is None:
        raise ValueError("expected_meal_id must be a non-empty string")

    hard_reasons: list[str] = []
    seen_capture_ids: set[str] = set()
    seen_tray_ids: set[str] = set()
    ready_rows: list[Mapping[str, Any]] = []
    excluded_reason_counts: dict[str, int] = {}

    for raw_result in results:
        if not isinstance(raw_result, Mapping):
            excluded_reason_counts["RESULT_MUST_BE_MAPPING"] = (
                excluded_reason_counts.get("RESULT_MUST_BE_MAPPING", 0) + 1
            )
            continue

        capture_id = _text(raw_result.get("captureId"))
        tray_id = _text(raw_result.get("trayId"))
        row_meal_id = _text(raw_result.get("mealId"))

        if capture_id is not None:
            if capture_id in seen_capture_ids:
                _append_unique(hard_reasons, "DUPLICATE_CAPTURE_ID")
            seen_capture_ids.add(capture_id)
        if tray_id is not None:
            if tray_id in seen_tray_ids:
                _append_unique(hard_reasons, "DUPLICATE_TRAY_ID")
            seen_tray_ids.add(tray_id)
        if row_meal_id is not None and row_meal_id != meal_id:
            _append_unique(hard_reasons, "MEAL_ID_MISMATCH")

        validation = validate_traygate_result(raw_result)
        if validation["validation_status"] == "ACCEPTED":
            ready_rows.append(raw_result)
            continue

        for code in validation["reason_codes"]:
            code_text = str(code)
            excluded_reason_counts[code_text] = excluded_reason_counts.get(code_text, 0) + 1

    total_count = len(results)

    if hard_reasons:
        return {
            "aggregation_status": "REJECTED",
            "descriptive_analytics_available": False,
            "meal_id": meal_id,
            "total_result_count": total_count,
            "ready_result_count": 0,
            "excluded_result_count": total_count,
            "ready_fraction": 0.0,
            "coverage_status": "NONE",
            "per_food": {},
            "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
            "reason_codes": hard_reasons,
            "result_scope": "TRAYGATE_SERVICE_DESCRIPTIVE_PERCENTAGES_ONLY",
            "claim_boundary": (
                "A rejected service aggregate exposes no leftover statistics. "
                "No mass, cost, climate, or savings estimate is produced."
            ),
        }

    per_food_values: dict[str, list[float]] = {}
    for row in ready_rows:
        items = row.get("items", ())
        for item in items:
            food = _text(item.get("food"))
            if food is None:
                continue
            per_food_values.setdefault(food, []).append(float(item["leftoverPercent"]))

    per_food: dict[str, dict[str, float | int]] = {}
    for food in sorted(per_food_values):
        values = per_food_values[food]
        per_food[food] = {
            "sample_count": len(values),
            "mean_leftover_percent": sum(values) / len(values),
            "min_leftover_percent": min(values),
            "max_leftover_percent": max(values),
        }

    ready_count = len(ready_rows)
    excluded_count = total_count - ready_count
    ready_fraction = ready_count / total_count if total_count else 0.0
    if ready_count == 0:
        coverage_status = "NONE"
        aggregation_status = "NO_READY_RESULTS"
        descriptive_available = False
    elif ready_count == total_count:
        coverage_status = "FULL"
        aggregation_status = "AGGREGATED"
        descriptive_available = True
    else:
        coverage_status = "PARTIAL"
        aggregation_status = "AGGREGATED"
        descriptive_available = True

    return {
        "aggregation_status": aggregation_status,
        "descriptive_analytics_available": descriptive_available,
        "meal_id": meal_id,
        "total_result_count": total_count,
        "ready_result_count": ready_count,
        "excluded_result_count": excluded_count,
        "ready_fraction": ready_fraction,
        "coverage_status": coverage_status,
        "per_food": per_food,
        "excluded_reason_counts": dict(sorted(excluded_reason_counts.items())),
        "reason_codes": [],
        "result_scope": "TRAYGATE_SERVICE_DESCRIPTIVE_PERCENTAGES_ONLY",
        "claim_boundary": (
            "Service aggregation reports unweighted descriptive leftover percentages from "
            "contract-admitted READY results only. It does not estimate grams, kilograms, "
            "cost, carbon, water, causal impact, or achieved savings."
        ),
    }
