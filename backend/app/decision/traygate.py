"""Fail-closed CS1 contract for TrayGate capture and inference artifacts.

This module deliberately does *not* perform computer-vision inference. It
validates the EHB -> CS1 capture boundary, validates structured CS1 inference
results, and aggregates percentage-only READY results at one meal/service
boundary. Mass-equivalent waste requires separate measured calibration and is
therefore intentionally absent here.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import math
from typing import Any, Mapping, Sequence

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
INFERENCE_READINESS = frozenset({"READY", "REVIEW_REQUIRED", "WITHHOLD"})

# TrayGate is a tray-inspection measurement surface, not a person-tracking
# surface. Canonicalization catches common snake/camel/kebab variants.
_FORBIDDEN_PRIVACY_FIELDS = frozenset(
    {
        "studentid",
        "personid",
        "userid",
        "bucardid",
        "faceembedding",
        "biometricid",
        "identity",
        "studentidentity",
        "personidentity",
    }
)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _canonical_key(value: Any) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum())


def _reason_key(value: Any) -> str:
    return _canonical_key(value).upper()


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


def _append_unique(reasons: list[str], code: str) -> None:
    if code not in reasons:
        reasons.append(code)


def assess_capture(payload: Mapping[str, Any]) -> dict[str, object]:
    """Assess an EHB TrayGate capture before any CS1 model is invoked.

    The contract fails closed: malformed capture metadata, non-VALID capture
    quality, missing tray detection, or person-identifying fields produce
    ``WITHHOLD``. Passing this gate means only that the capture is admissible
    for inference; it is not evidence of model accuracy or operational impact.
    """

    reasons: list[str] = []
    if not isinstance(payload, Mapping):
        return {
            "accepted": False,
            "readiness": "WITHHOLD",
            "capture_id": None,
            "reason_codes": ["CAPTURE_PAYLOAD_MUST_BE_MAPPING"],
            "result_scope": "TRAYGATE_CAPTURE_ADMISSION_ONLY",
            "claim_boundary": (
                "Capture admission validates interface metadata only; it does not establish "
                "inference accuracy, measured waste, or operational savings."
            ),
        }

    required_text_fields = {
        "deviceId": "DEVICE_ID_REQUIRED",
        "captureId": "CAPTURE_ID_REQUIRED",
        "rgbFrame": "RGB_FRAME_REQUIRED",
        "cameraCalibrationVersion": "CAMERA_CALIBRATION_VERSION_REQUIRED",
        "deviceSoftwareVersion": "DEVICE_SOFTWARE_VERSION_REQUIRED",
    }
    for field, code in required_text_fields.items():
        if _text(payload.get(field)) is None:
            _append_unique(reasons, code)

    if _aware_timestamp(payload.get("timestamp")) is None:
        _append_unique(reasons, "TIMESTAMP_MUST_BE_TIMEZONE_AWARE")

    tray_detected = payload.get("trayDetected")
    if not isinstance(tray_detected, bool):
        _append_unique(reasons, "TRAY_DETECTED_MUST_BE_BOOLEAN")
    elif not tray_detected:
        _append_unique(reasons, "TRAY_NOT_DETECTED")

    capture_quality = _text(payload.get("captureQuality"))
    if capture_quality not in CAPTURE_QUALITIES:
        _append_unique(reasons, "UNKNOWN_CAPTURE_QUALITY")
    elif capture_quality != "VALID":
        _append_unique(reasons, f"CAPTURE_QUALITY_{capture_quality}")

    if "depthFrame" in payload and payload.get("depthFrame") is not None:
        if _text(payload.get("depthFrame")) is None:
            _append_unique(reasons, "DEPTH_FRAME_REFERENCE_INVALID")

    for field in payload:
        canonical_field = _canonical_key(field)
        if canonical_field in _FORBIDDEN_PRIVACY_FIELDS:
            _append_unique(
                reasons,
                f"PRIVACY_FIELD_NOT_ALLOWED_{_reason_key(field)}",
            )

    accepted = not reasons
    return {
        "accepted": accepted,
        "readiness": "READY_FOR_INFERENCE" if accepted else "WITHHOLD",
        "capture_id": _text(payload.get("captureId")),
        "reason_codes": reasons,
        "result_scope": "TRAYGATE_CAPTURE_ADMISSION_ONLY",
        "claim_boundary": (
            "Capture admission validates interface metadata only; it does not establish "
            "inference accuracy, measured waste, or operational savings."
        ),
    }


def validate_inference_result(result: Mapping[str, Any]) -> dict[str, object]:
    """Validate a structured CS1 TrayGate result without upgrading evidence."""

    reasons: list[str] = []
    if not isinstance(result, Mapping):
        return {
            "valid": False,
            "readiness": None,
            "capture_id": None,
            "meal_id": None,
            "reason_codes": ["INFERENCE_RESULT_MUST_BE_MAPPING"],
            "result_scope": "TRAYGATE_INFERENCE_RESULT_CONTRACT_ONLY",
        }

    required_text_fields = {
        "captureId": "CAPTURE_ID_REQUIRED",
        "mealId": "MEAL_ID_REQUIRED",
        "trayId": "TRAY_ID_REQUIRED",
        "modelVersion": "MODEL_VERSION_REQUIRED",
    }
    for field, code in required_text_fields.items():
        if _text(result.get(field)) is None:
            _append_unique(reasons, code)

    readiness = _text(result.get("readiness"))
    if readiness not in INFERENCE_READINESS:
        _append_unique(reasons, "UNKNOWN_INFERENCE_READINESS")

    items = result.get("items")
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        _append_unique(reasons, "ITEMS_MUST_BE_SEQUENCE")
        parsed_items: Sequence[Any] = ()
    else:
        parsed_items = items

    if readiness == "READY" and not parsed_items:
        _append_unique(reasons, "READY_ITEMS_REQUIRED")

    for item in parsed_items:
        if not isinstance(item, Mapping):
            _append_unique(reasons, "ITEM_MUST_BE_MAPPING")
            continue
        if _text(item.get("food")) is None:
            _append_unique(reasons, "FOOD_LABEL_REQUIRED")

        leftover_percent = _finite_number(item.get("leftoverPercent"))
        if leftover_percent is None or not 0.0 <= leftover_percent <= 100.0:
            _append_unique(reasons, "LEFTOVER_PERCENT_OUT_OF_RANGE")

        confidence = _finite_number(item.get("confidence"))
        if confidence is None or not 0.0 <= confidence <= 1.0:
            _append_unique(reasons, "CONFIDENCE_OUT_OF_RANGE")

    return {
        "valid": not reasons,
        "readiness": readiness,
        "capture_id": _text(result.get("captureId")),
        "meal_id": _text(result.get("mealId")),
        "reason_codes": reasons,
        "result_scope": "TRAYGATE_INFERENCE_RESULT_CONTRACT_ONLY",
        "claim_boundary": (
            "Contract validity does not establish CV accuracy, calibrated mass, field "
            "performance, or waste reduction."
        ),
    }


def aggregate_service_results(
    results: Sequence[Mapping[str, Any]],
    *,
    meal_id: str,
) -> dict[str, object]:
    """Aggregate READY percentage results for exactly one meal/service.

    ``REVIEW_REQUIRED`` and ``WITHHOLD`` remain visible in coverage counts but
    never contribute to food-leftover statistics. No percentage-to-mass
    conversion is performed because that requires measured calibration.
    """

    target_meal_id = _text(meal_id)
    if target_meal_id is None:
        raise ValueError("meal_id must be a non-empty string")
    if isinstance(results, (str, bytes)) or not isinstance(results, Sequence):
        raise ValueError("results must be a sequence of mappings")

    seen_capture_ids: set[str] = set()
    counts = {readiness: 0 for readiness in INFERENCE_READINESS}
    leftover_by_food: dict[str, list[float]] = defaultdict(list)
    model_versions: set[str] = set()

    for index, result in enumerate(results):
        validation = validate_inference_result(result)
        if not validation["valid"]:
            codes = ",".join(validation["reason_codes"])
            raise ValueError(f"invalid inference result at index {index}: {codes}")

        capture_id = str(validation["capture_id"])
        if capture_id in seen_capture_ids:
            raise ValueError(f"duplicate captureId: {capture_id}")
        seen_capture_ids.add(capture_id)

        result_meal_id = validation["meal_id"]
        if result_meal_id != target_meal_id:
            raise ValueError(
                f"mealId mismatch: expected {target_meal_id}, got {result_meal_id}"
            )

        readiness = str(validation["readiness"])
        counts[readiness] += 1
        model_version = _text(result.get("modelVersion"))
        if model_version is not None:
            model_versions.add(model_version)

        if readiness != "READY":
            continue

        for item in result.get("items", ()):
            food = str(_text(item.get("food")))
            leftover_percent = _finite_number(item.get("leftoverPercent"))
            # Validation above proves both values are present and in range.
            assert leftover_percent is not None
            leftover_by_food[food].append(leftover_percent)

    capture_count = len(results)
    ready_count = counts["READY"]
    food_leftover_percent: dict[str, dict[str, float | int]] = {}
    for food in sorted(leftover_by_food):
        values = leftover_by_food[food]
        food_leftover_percent[food] = {
            "mean": round(sum(values) / len(values), 6),
            "sample_count": len(values),
        }

    return {
        "meal_id": target_meal_id,
        "capture_count": capture_count,
        "ready_capture_count": ready_count,
        "review_required_capture_count": counts["REVIEW_REQUIRED"],
        "withheld_capture_count": counts["WITHHOLD"],
        "ready_coverage": ready_count / capture_count if capture_count else 0.0,
        "food_leftover_percent": food_leftover_percent,
        "model_versions": sorted(model_versions),
        "result_scope": "TRAYGATE_PERCENT_ONLY_NO_MASS_CALIBRATION",
        "claim_boundary": (
            "Only READY percentage estimates are aggregated. No kg, gram, energy, cost, "
            "or savings claim is derivable without separate measured calibration/evidence."
        ),
    }
