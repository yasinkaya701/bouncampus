from __future__ import annotations

import importlib.util
import math
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def _load_contract():
    try:
        from app.decision import campus_contract as contract  # type: ignore

        return contract
    except ModuleNotFoundError:
        path = Path(__file__).with_name("campus_contract.py")
        spec = importlib.util.spec_from_file_location("campus_contract_fallback", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load campus contract from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


CONTRACT = _load_contract()
CONTRACT_VERSION = CONTRACT.CONTRACT_VERSION

LIMITATIONS = (
    "NO_LIVE_REGISTRAR_INTEGRATION_CLAIM",
    "NO_UNVERIFIED_ROOM_CAPACITY_CLAIM",
    "NO_UNVERIFIED_ENROLLMENT_CLAIM",
    "NO_STUDENT_LEVEL_TIMETABLE_TRACKING",
    "GREEDY_HEURISTIC_NOT_GLOBAL_OPTIMUM",
    "OPERATOR_APPROVAL_REQUIRED_BEFORE_ROOM_CHANGE",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _finite(value: Any, *, field: str, minimum: float | None = None) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{field} must be finite")
    if minimum is not None and numeric < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return numeric


def _positive(value: Any, *, field: str) -> float:
    numeric = _finite(value, field=field, minimum=0.0)
    if numeric <= 0:
        raise ValueError(f"{field} must be greater than zero")
    return numeric


def _strict_bool(value: Any, *, field: str, default: bool = False) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _normalize_equipment(value: Any, *, field: str) -> set[str]:
    if value is None:
        return set()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError(f"{field} must be a list")
    normalized: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field} entries must be non-empty strings")
        normalized.add(item.strip().lower())
    return normalized


def _normalize_room(room: Mapping[str, Any]) -> dict[str, Any]:
    room_id = str(room.get("room_id", "")).strip()
    building_id = str(room.get("building_id", "")).strip()
    campus = str(room.get("campus", "")).strip().lower()
    if not room_id:
        raise ValueError("room_id is required")
    if not building_id:
        raise ValueError(f"building_id is required for room {room_id}")
    if not campus:
        raise ValueError(f"campus is required for room {room_id}")

    capacity = _positive(room.get("capacity"), field=f"room {room_id} capacity")
    energy_score = _finite(
        room.get("energy_cost_score", 0.0),
        field=f"room {room_id} energy_cost_score",
        minimum=0.0,
    )
    return {
        "room_id": room_id,
        "building_id": building_id,
        "campus": campus,
        "capacity": int(round(capacity)),
        "accessible": _strict_bool(
            room.get("accessible", False), field=f"room {room_id} accessible"
        ),
        "equipment": _normalize_equipment(
            room.get("equipment", []), field=f"room {room_id} equipment"
        ),
        "energy_cost_score": energy_score,
    }


def _normalize_session(session: Mapping[str, Any]) -> dict[str, Any]:
    session_id = str(session.get("session_id", "")).strip()
    campus = str(session.get("campus", "")).strip().lower()
    if not session_id:
        raise ValueError("session_id is required")
    if not campus:
        raise ValueError(f"campus is required for session {session_id}")

    start = _finite(
        session.get("start_minute"), field=f"session {session_id} start time", minimum=0.0
    )
    end = _finite(
        session.get("end_minute"), field=f"session {session_id} end time", minimum=0.0
    )
    if start >= end:
        raise ValueError(f"session {session_id} time window must have start < end")
    if end > 24 * 60:
        raise ValueError(f"session {session_id} time window must fit within one day")

    attendance = _positive(
        session.get("expected_attendance"),
        field=f"session {session_id} expected_attendance",
    )
    return {
        "session_id": session_id,
        "campus": campus,
        "start_minute": int(round(start)),
        "end_minute": int(round(end)),
        "expected_attendance": int(round(attendance)),
        "accessibility_required": _strict_bool(
            session.get("accessibility_required", False),
            field=f"session {session_id} accessibility_required",
        ),
        "equipment_required": _normalize_equipment(
            session.get("equipment_required", []),
            field=f"session {session_id} equipment_required",
        ),
    }


def _overlaps(start: int, end: int, existing: tuple[int, int]) -> bool:
    existing_start, existing_end = existing
    return start < existing_end and existing_start < end


def _feasible(
    session: Mapping[str, Any],
    room: Mapping[str, Any],
    bookings: Mapping[str, list[tuple[int, int]]],
) -> bool:
    if session["campus"] != room["campus"]:
        return False
    if session["expected_attendance"] > room["capacity"]:
        return False
    if session["accessibility_required"] and not room["accessible"]:
        return False
    if not session["equipment_required"].issubset(room["equipment"]):
        return False
    return not any(
        _overlaps(session["start_minute"], session["end_minute"], interval)
        for interval in bookings.get(room["room_id"], [])
    )


def _withhold(
    reason_code: str,
    *,
    room_inventory_provenance: str,
    attendance_provenance: str,
) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "WITHHOLD",
        "abstained": True,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "room_inventory_provenance": room_inventory_provenance,
        "attendance_provenance": attendance_provenance,
        "assignments": [],
        "unassigned": [],
        "building_loads": {},
        "reason_codes": [reason_code],
        "limitations": list(LIMITATIONS),
    }


def allocate_classrooms(
    sessions: Sequence[Mapping[str, Any]],
    rooms: Sequence[Mapping[str, Any]],
    *,
    upstream_readiness: str = "REVIEW_REQUIRED",
    room_inventory_provenance: str = "UNAVAILABLE",
    attendance_provenance: str = "UNAVAILABLE",
) -> dict[str, Any]:
    """Allocate sessions to rooms using verified inputs and hard constraints first.

    This v1 allocator is intentionally transparent and greedy. Capacity-sensitive
    assignments are emitted only when both room inventory and attendance/enrollment
    inputs have verified operational provenance. The result always requires human
    approval and never writes a registrar booking automatically.
    """

    CONTRACT.validate_no_person_level_data(sessions, path="sessions")
    CONTRACT.validate_no_person_level_data(rooms, path="rooms")

    normalized_upstream = str(upstream_readiness).upper()
    if normalized_upstream not in CONTRACT.READINESS_STATES:
        raise ValueError(f"unsupported upstream_readiness: {upstream_readiness}")

    room_provenance = CONTRACT.normalize_provenance(
        room_inventory_provenance, field="room_inventory_provenance"
    )
    attendance_source = CONTRACT.normalize_provenance(
        attendance_provenance, field="attendance_provenance"
    )

    if normalized_upstream == "WITHHOLD":
        return _withhold(
            "UPSTREAM_CAMPUS_STATE_WITHHELD",
            room_inventory_provenance=room_provenance,
            attendance_provenance=attendance_source,
        )
    if not sessions or not rooms:
        return _withhold(
            "NO_SESSIONS_OR_ROOMS_SUPPLIED",
            room_inventory_provenance=room_provenance,
            attendance_provenance=attendance_source,
        )
    if room_provenance not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        return _withhold(
            "UNVERIFIED_ROOM_INVENTORY",
            room_inventory_provenance=room_provenance,
            attendance_provenance=attendance_source,
        )
    if attendance_source not in CONTRACT.VERIFIED_CAPACITY_PROVENANCE:
        return _withhold(
            "UNVERIFIED_ATTENDANCE_INPUT",
            room_inventory_provenance=room_provenance,
            attendance_provenance=attendance_source,
        )

    normalized_rooms = [_normalize_room(room) for room in rooms]
    room_ids = [room["room_id"] for room in normalized_rooms]
    if len(room_ids) != len(set(room_ids)):
        raise ValueError("duplicate room_id values are not allowed")

    normalized_sessions = [_normalize_session(session) for session in sessions]
    session_ids = [session["session_id"] for session in normalized_sessions]
    if len(session_ids) != len(set(session_ids)):
        raise ValueError("duplicate session_id values are not allowed")

    ordered_sessions = sorted(
        normalized_sessions,
        key=lambda item: (item["start_minute"], -item["expected_attendance"], item["session_id"]),
    )
    bookings: dict[str, list[tuple[int, int]]] = {}
    assignments: list[dict[str, Any]] = []
    unassigned: list[dict[str, Any]] = []
    building_loads: dict[str, dict[str, int]] = {}
    reason_codes = ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"]

    for session in ordered_sessions:
        candidates = [
            room
            for room in normalized_rooms
            if _feasible(session, room, bookings)
        ]
        if not candidates:
            unassigned.append(
                {
                    "session_id": session["session_id"],
                    "reason": "NO_FEASIBLE_ROOM",
                }
            )
            reason_codes.append(f"NO_FEASIBLE_ROOM_{session['session_id'].upper()}")
            continue

        def score(room: Mapping[str, Any]) -> tuple[float, int, str]:
            spare_seats = room["capacity"] - session["expected_attendance"]
            combined = spare_seats + (room["energy_cost_score"] * 10.0)
            return (combined, room["capacity"], room["room_id"])

        chosen = min(candidates, key=score)
        bookings.setdefault(chosen["room_id"], []).append(
            (session["start_minute"], session["end_minute"])
        )
        assignments.append(
            {
                "session_id": session["session_id"],
                "room_id": chosen["room_id"],
                "building_id": chosen["building_id"],
                "campus": chosen["campus"],
                "start_minute": session["start_minute"],
                "end_minute": session["end_minute"],
                "expected_attendance": session["expected_attendance"],
                "room_capacity": chosen["capacity"],
                "utilization_pct": round(
                    (session["expected_attendance"] / chosen["capacity"]) * 100.0, 2
                ),
                "room_inventory_provenance": room_provenance,
                "attendance_provenance": attendance_source,
                "assignment_provenance": "POLICY_HEURISTIC",
            }
        )
        bucket = building_loads.setdefault(
            chosen["building_id"],
            {
                "assigned_sessions": 0,
                "assigned_attendance": 0,
                "assigned_room_capacity": 0,
            },
        )
        bucket["assigned_sessions"] += 1
        bucket["assigned_attendance"] += session["expected_attendance"]
        bucket["assigned_room_capacity"] += chosen["capacity"]

    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "demand_provenance": attendance_source,
        "room_inventory_provenance": room_provenance,
        "attendance_provenance": attendance_source,
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "assignments": assignments,
        "unassigned": unassigned,
        "building_loads": building_loads,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "limitations": list(LIMITATIONS),
    }
