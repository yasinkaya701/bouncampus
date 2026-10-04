"""Explainable solar exposure and site-orientation planning for CS1 campus operations.

Uses the compact NOAA solar-position approximation with timezone-aware timestamps.
Outputs are advisory geometry indices, not calibrated daylight, thermal-load, energy,
or comfort predictions.
"""
from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

POLICY_VERSION = "solar-site-planning-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
LIMITATIONS = (
    "NO_3D_RAY_TRACING_OR_CAD_OCCLUSION_MODEL",
    "NO_CALIBRATED_DAYLIGHT_OR_THERMAL_MODEL",
    "NO_GLAZING_SHGC_OR_HVAC_CALIBRATION",
    "SOLAR_POSITION_USES_NOAA_APPROXIMATION",
    "OBSTRUCTION_HORIZON_IS_CALLER_SUPPLIED_GEOMETRY",
    "NO_ACHIEVED_ENERGY_OR_COMFORT_CLAIM",
)


def _number(value: Any, *, minimum: float | None = None, maximum: float | None = None) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    if minimum is not None and numeric < minimum:
        return None
    if maximum is not None and numeric > maximum:
        return None
    return numeric


def _aware_datetime(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _base(scope: str) -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": scope,
        "objective_units": OBJECTIVE_UNITS,
        "decision_readiness": "REVIEW_REQUIRED",
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
        "limitations": list(LIMITATIONS),
    }


def _withhold(scope: str, reason: str) -> dict[str, Any]:
    return {
        **_base(scope),
        "decision_readiness": "WITHHOLD",
        "reason_codes": [reason],
    }


def solar_position(latitude_deg: Any, longitude_deg: Any, timestamp: Any) -> dict[str, float]:
    """Return approximate solar azimuth/elevation for a timezone-aware timestamp.

    Longitude follows the conventional geographic sign: east positive, west negative.
    Azimuth is degrees clockwise from north; elevation is degrees above the horizon.
    """
    latitude = _number(latitude_deg, minimum=-90.0, maximum=90.0)
    longitude = _number(longitude_deg, minimum=-180.0, maximum=180.0)
    instant = _aware_datetime(timestamp)
    if latitude is None or longitude is None or instant is None:
        raise ValueError("INVALID_SOLAR_GEOMETRY_INPUT")

    days_in_year = 366 if (instant.year % 4 == 0 and (instant.year % 100 != 0 or instant.year % 400 == 0)) else 365
    day_of_year = instant.timetuple().tm_yday
    local_hour = instant.hour + instant.minute / 60.0 + instant.second / 3600.0
    gamma = 2.0 * math.pi / days_in_year * (day_of_year - 1 + (local_hour - 12.0) / 24.0)

    eqtime = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )
    decl = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )

    timezone_hours = instant.utcoffset().total_seconds() / 3600.0
    time_offset = eqtime + 4.0 * longitude - 60.0 * timezone_hours
    true_solar_minutes = local_hour * 60.0 + time_offset
    hour_angle_deg = true_solar_minutes / 4.0 - 180.0
    while hour_angle_deg < -180.0:
        hour_angle_deg += 360.0
    while hour_angle_deg > 180.0:
        hour_angle_deg -= 360.0

    lat = math.radians(latitude)
    ha = math.radians(hour_angle_deg)
    cos_zenith = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(ha)
    cos_zenith = max(-1.0, min(1.0, cos_zenith))
    zenith = math.acos(cos_zenith)
    elevation = 90.0 - math.degrees(zenith)

    azimuth = (
        math.degrees(
            math.atan2(
                math.sin(ha),
                math.cos(ha) * math.sin(lat) - math.tan(decl) * math.cos(lat),
            )
        )
        + 180.0
    ) % 360.0
    return {
        "azimuth_deg": round(azimuth, 4),
        "elevation_deg": round(elevation, 4),
    }


def _angular_difference_deg(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def _vertical_facade_exposure(
    sun_azimuth: float,
    sun_elevation: float,
    facade_azimuth: float,
    obstruction_elevation: float,
) -> float:
    if sun_elevation <= 0.0 or sun_elevation <= obstruction_elevation:
        return 0.0
    diff = math.radians(_angular_difference_deg(sun_azimuth, facade_azimuth))
    incidence = math.cos(math.radians(sun_elevation)) * math.cos(diff)
    return max(0.0, min(1.0, incidence))


def analyze_room_solar_exposure(
    *,
    latitude_deg: Any,
    longitude_deg: Any,
    timestamps: Sequence[Any],
    rooms: Sequence[Mapping[str, Any]],
    class_sessions: Sequence[Mapping[str, Any]],
    affected_threshold: Any = 0.25,
) -> dict[str, Any]:
    scope = "ROOM_SOLAR_EXPOSURE_REVIEW"
    latitude = _number(latitude_deg, minimum=-90.0, maximum=90.0)
    longitude = _number(longitude_deg, minimum=-180.0, maximum=180.0)
    threshold = _number(affected_threshold, minimum=0.0, maximum=1.0)
    if (
        latitude is None
        or longitude is None
        or threshold is None
        or not isinstance(timestamps, Sequence)
        or isinstance(timestamps, (str, bytes))
        or not timestamps
        or not isinstance(rooms, Sequence)
        or isinstance(rooms, (str, bytes))
        or not rooms
        or not isinstance(class_sessions, Sequence)
        or isinstance(class_sessions, (str, bytes))
    ):
        result = _withhold(scope, "INVALID_SOLAR_GEOMETRY_INPUT")
        result.update({"room_exposure": [], "affected_classes": []})
        return result

    positions: dict[str, dict[str, float]] = {}
    for raw_timestamp in timestamps:
        instant = _aware_datetime(raw_timestamp)
        if instant is None:
            result = _withhold(scope, "INVALID_SOLAR_GEOMETRY_INPUT")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        key = instant.isoformat()
        try:
            positions[key] = solar_position(latitude, longitude, key)
        except ValueError:
            result = _withhold(scope, "INVALID_SOLAR_GEOMETRY_INPUT")
            result.update({"room_exposure": [], "affected_classes": []})
            return result

    normalized_rooms: dict[str, dict[str, Any]] = {}
    room_exposure: list[dict[str, Any]] = []
    exposure_lookup: dict[tuple[str, str], float] = {}
    for raw_room in rooms:
        if not isinstance(raw_room, Mapping):
            result = _withhold(scope, "INVALID_ROOM_SOLAR_GEOMETRY")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        room_id = str(raw_room.get("room_id") or "").strip()
        building_id = str(raw_room.get("building_id") or "").strip()
        facade = _number(raw_room.get("facade_azimuth_deg"), minimum=0.0, maximum=360.0)
        window_area = _number(raw_room.get("window_area_m2"), minimum=0.0)
        obstruction = _number(raw_room.get("obstruction_elevation_deg", 0.0), minimum=0.0, maximum=90.0)
        transmittance = _number(raw_room.get("solar_transmittance", 1.0), minimum=0.0, maximum=1.0)
        if (
            not room_id
            or room_id in normalized_rooms
            or not building_id
            or facade is None
            or window_area is None
            or obstruction is None
            or transmittance is None
        ):
            result = _withhold(scope, "INVALID_ROOM_SOLAR_GEOMETRY")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        if facade == 360.0:
            facade = 0.0
        normalized_rooms[room_id] = {"building_id": building_id}
        samples: list[dict[str, Any]] = []
        values: list[float] = []
        for timestamp, pos in positions.items():
            base_exposure = _vertical_facade_exposure(
                pos["azimuth_deg"],
                pos["elevation_deg"],
                facade,
                obstruction,
            )
            exposure = base_exposure * transmittance
            exposure = max(0.0, min(1.0, exposure))
            exposure_lookup[(room_id, timestamp)] = exposure
            values.append(exposure)
            samples.append(
                {
                    "timestamp": timestamp,
                    "sun_azimuth_deg": pos["azimuth_deg"],
                    "sun_elevation_deg": pos["elevation_deg"],
                    "direct_exposure_index": round(exposure, 4),
                }
            )
        mean_exposure = sum(values) / len(values)
        room_exposure.append(
            {
                "room_id": room_id,
                "building_id": building_id,
                "facade_azimuth_deg": facade,
                "window_area_m2": window_area,
                "mean_direct_exposure_index": round(mean_exposure, 4),
                "direct_gain_area_index": round(mean_exposure * window_area, 4),
                "samples": samples,
            }
        )

    affected_classes: list[dict[str, Any]] = []
    for raw_session in class_sessions:
        if not isinstance(raw_session, Mapping):
            result = _withhold(scope, "INVALID_CLASS_SOLAR_SESSION")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        class_id = str(raw_session.get("class_id") or "").strip()
        room_id = str(raw_session.get("room_id") or "").strip()
        instant = _aware_datetime(raw_session.get("timestamp"))
        if not class_id or room_id not in normalized_rooms or instant is None:
            result = _withhold(scope, "INVALID_CLASS_SOLAR_SESSION")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        key = instant.isoformat()
        exposure = exposure_lookup.get((room_id, key))
        if exposure is None:
            result = _withhold(scope, "CLASS_SESSION_OUTSIDE_SOLAR_SAMPLES")
            result.update({"room_exposure": [], "affected_classes": []})
            return result
        if exposure + 1e-12 >= threshold:
            affected_classes.append(
                {
                    "class_id": class_id,
                    "room_id": room_id,
                    "building_id": normalized_rooms[room_id]["building_id"],
                    "timestamp": key,
                    "direct_exposure_index": round(exposure, 4),
                }
            )

    room_exposure.sort(key=lambda row: row["room_id"])
    affected_classes.sort(key=lambda row: (row["timestamp"], row["class_id"], row["room_id"]))
    return {
        **_base(scope),
        "affected_threshold": threshold,
        "room_exposure": room_exposure,
        "affected_classes": affected_classes,
        "reason_codes": ["ADVISORY_SOLAR_GEOMETRY_REVIEW", "FIELD_GEOMETRY_VALIDATION_REQUIRED"],
        "method_semantics": "NOAA_SOLAR_POSITION_PLUS_VERTICAL_FACADE_INCIDENCE",
    }


def rank_new_building_orientations(
    *,
    latitude_deg: Any,
    longitude_deg: Any,
    timestamps: Sequence[Any],
    facade_program: Sequence[Mapping[str, Any]],
    candidate_orientations_deg: Sequence[Any],
) -> dict[str, Any]:
    scope = "NEW_BUILDING_ORIENTATION_REVIEW"
    latitude = _number(latitude_deg, minimum=-90.0, maximum=90.0)
    longitude = _number(longitude_deg, minimum=-180.0, maximum=180.0)
    if (
        latitude is None
        or longitude is None
        or not isinstance(timestamps, Sequence)
        or isinstance(timestamps, (str, bytes))
        or not timestamps
        or not isinstance(facade_program, Sequence)
        or isinstance(facade_program, (str, bytes))
        or not facade_program
        or not isinstance(candidate_orientations_deg, Sequence)
        or isinstance(candidate_orientations_deg, (str, bytes))
        or not candidate_orientations_deg
    ):
        result = _withhold(scope, "INVALID_SITE_PLANNING_INPUT")
        result.update({"candidates": [], "automatic_design_selection": False})
        return result

    positions: list[dict[str, float]] = []
    for value in timestamps:
        try:
            positions.append(solar_position(latitude, longitude, value))
        except ValueError:
            result = _withhold(scope, "INVALID_SITE_PLANNING_INPUT")
            result.update({"candidates": [], "automatic_design_selection": False})
            return result

    facades: list[dict[str, float | str]] = []
    seen_facades: set[str] = set()
    for raw in facade_program:
        if not isinstance(raw, Mapping):
            result = _withhold(scope, "INVALID_FACADE_PROGRAM")
            result.update({"candidates": [], "automatic_design_selection": False})
            return result
        facade_id = str(raw.get("facade_id") or "").strip()
        relative = _number(raw.get("relative_azimuth_deg"), minimum=0.0, maximum=360.0)
        daylight_weight = _number(raw.get("daylight_weight"), minimum=0.0)
        heat_weight = _number(raw.get("heat_weight"), minimum=0.0)
        if (
            not facade_id
            or facade_id in seen_facades
            or relative is None
            or daylight_weight is None
            or heat_weight is None
        ):
            result = _withhold(scope, "INVALID_FACADE_PROGRAM")
            result.update({"candidates": [], "automatic_design_selection": False})
            return result
        seen_facades.add(facade_id)
        facades.append(
            {
                "facade_id": facade_id,
                "relative_azimuth_deg": 0.0 if relative == 360.0 else relative,
                "daylight_weight": daylight_weight,
                "heat_weight": heat_weight,
            }
        )

    candidates: list[dict[str, Any]] = []
    seen_orientations: set[float] = set()
    for raw_orientation in candidate_orientations_deg:
        orientation = _number(raw_orientation, minimum=0.0, maximum=360.0)
        if orientation is None:
            result = _withhold(scope, "INVALID_SITE_PLANNING_INPUT")
            result.update({"candidates": [], "automatic_design_selection": False})
            return result
        orientation = 0.0 if orientation == 360.0 else orientation
        if orientation in seen_orientations:
            continue
        seen_orientations.add(orientation)
        total_loss = 0.0
        components: list[dict[str, Any]] = []
        for facade in facades:
            absolute = (orientation + float(facade["relative_azimuth_deg"])) % 360.0
            exposures = [
                _vertical_facade_exposure(
                    pos["azimuth_deg"],
                    pos["elevation_deg"],
                    absolute,
                    0.0,
                )
                for pos in positions
            ]
            mean_exposure = sum(exposures) / len(exposures)
            daylight_loss = float(facade["daylight_weight"]) * (1.0 - mean_exposure)
            heat_loss = float(facade["heat_weight"]) * mean_exposure
            facade_loss = daylight_loss + heat_loss
            total_loss += facade_loss
            components.append(
                {
                    "facade_id": facade["facade_id"],
                    "absolute_azimuth_deg": round(absolute, 4),
                    "mean_direct_exposure_index": round(mean_exposure, 4),
                    "registered_loss": round(facade_loss, 6),
                }
            )
        candidates.append(
            {
                "orientation_deg": orientation,
                "registered_loss": round(total_loss, 6),
                "facades": components,
            }
        )

    candidates.sort(key=lambda row: (row["registered_loss"], row["orientation_deg"]))
    return {
        **_base(scope),
        "automatic_design_selection": False,
        "candidates": candidates,
        "recommended_orientation_deg": candidates[0]["orientation_deg"] if candidates else None,
        "recommendation_semantics": "ADVISORY_ORIENTATION_CANDIDATE_REQUIRES_ARCHITECTURAL_AND_FIELD_REVIEW",
        "reason_codes": ["REGISTERED_WEIGHTS_NOT_CALIBRATED_ENERGY_MODEL", "ARCHITECTURAL_REVIEW_REQUIRED"],
    }
