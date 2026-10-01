from __future__ import annotations

import importlib.util
from collections.abc import Mapping
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
    "CROSS_DOMAIN_OUTPUT_IS_DECISION_SUPPORT_ONLY",
    "NO_AUTOMATIC_UNIVERSITY_OPERATION_EXECUTION",
    "NO_LIVE_TELEMETRY_CLAIM",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def _readiness(payload: Mapping[str, Any] | None) -> str | None:
    if payload is None:
        return None
    value = str(payload.get("decision_readiness", "")).upper()
    return value if value in CONTRACT.READINESS_STATES else None


def _campus_demand_context(campus_state: Mapping[str, Any]) -> dict[str, int]:
    totals = campus_state.get("campus_totals", {})
    if not isinstance(totals, Mapping):
        return {}
    output: dict[str, int] = {}
    for campus, raw in totals.items():
        if not isinstance(raw, Mapping):
            continue
        try:
            output[str(campus)] = int(round(float(raw.get("occupancy_estimate", 0))))
        except (TypeError, ValueError):
            continue
    return output


def _shuttle_shortfalls(payload: Mapping[str, Any] | None) -> list[str]:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return []
    rows = payload.get("routes", [])
    if not isinstance(rows, list):
        return []
    return [
        str(row.get("route_id", "")).strip()
        for row in rows
        if isinstance(row, Mapping)
        and row.get("capacity_feasible") is False
        and str(row.get("route_id", "")).strip()
    ]


def _unassigned_sessions(payload: Mapping[str, Any] | None) -> list[str]:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return []
    rows = payload.get("unassigned", [])
    if not isinstance(rows, list):
        return []
    return [
        str(row.get("session_id", "")).strip()
        for row in rows
        if isinstance(row, Mapping) and str(row.get("session_id", "")).strip()
    ]


def _building_attendance_targets(payload: Mapping[str, Any] | None) -> dict[str, int]:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return {}
    loads = payload.get("building_loads", {})
    if not isinstance(loads, Mapping):
        return {}
    output: dict[str, int] = {}
    for building_id, raw in loads.items():
        if not isinstance(raw, Mapping):
            continue
        try:
            output[str(building_id)] = int(round(float(raw.get("assigned_attendance", 0))))
        except (TypeError, ValueError):
            continue
    return output


def _food_target(payload: Mapping[str, Any] | None) -> int | None:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return None
    value = payload.get("recommended_production")
    if isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return int(numeric) if numeric >= 0 and numeric.is_integer() else None


def _energy_modes(payload: Mapping[str, Any] | None) -> dict[str, str]:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return {}
    rows = payload.get("zones", [])
    if not isinstance(rows, list):
        return {}
    output: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        zone_id = str(row.get("zone_id", "")).strip()
        mode = str(row.get("recommended_mode", "")).strip().upper()
        if zone_id and mode:
            output[zone_id] = mode
    return output


def _shared_allocations(payload: Mapping[str, Any] | None) -> dict[str, int]:
    if payload is None or _readiness(payload) == "WITHHOLD":
        return {}
    rows = payload.get("allocations", [])
    if not isinstance(rows, list):
        return {}
    output: dict[str, int] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        request_id = str(row.get("request_id", "")).strip()
        value = row.get("allocated")
        if not request_id or isinstance(value, bool):
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        if numeric >= 0 and numeric.is_integer():
            output[request_id] = int(numeric)
    return output


def build_campus_portfolio(
    *,
    campus_state: Mapping[str, Any],
    shuttle_plan: Mapping[str, Any] | None = None,
    classroom_plan: Mapping[str, Any] | None = None,
    food_decision: Mapping[str, Any] | None = None,
    energy_decision: Mapping[str, Any] | None = None,
    shared_capacity_decision: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    CONTRACT.validate_no_person_level_data(campus_state, path="campus_state")
    for name, payload in (
        ("shuttle_plan", shuttle_plan),
        ("classroom_plan", classroom_plan),
        ("food_decision", food_decision),
        ("energy_decision", energy_decision),
        ("shared_capacity_decision", shared_capacity_decision),
    ):
        if payload is not None:
            CONTRACT.validate_no_person_level_data(payload, path=name)

    core_readiness = _readiness(campus_state)
    if core_readiness is None:
        raise ValueError("campus_state must include a supported decision_readiness")
    if core_readiness == "WITHHOLD":
        return {
            "contract_version": CONTRACT_VERSION,
            "decision_provenance": "POLICY_HEURISTIC",
            "decision_readiness": "WITHHOLD",
            "abstained": True,
            "operator_approval_required": True,
            "automatic_execution_allowed": False,
            "cross_domain_signals": {},
            "domain_status": {"campus_state": "WITHHOLD"},
            "reason_codes": ["CORE_CAMPUS_STATE_WITHHELD"],
            "limitations": list(LIMITATIONS),
        }

    reason_codes = ["PRE_PILOT_OPERATOR_REVIEW_REQUIRED"]
    domain_status: dict[str, str] = {"campus_state": core_readiness}
    for label, payload in (
        ("shuttle", shuttle_plan),
        ("classroom", classroom_plan),
        ("food", food_decision),
        ("energy", energy_decision),
        ("shared_capacity", shared_capacity_decision),
    ):
        status = _readiness(payload)
        if status is None:
            if payload is not None:
                reason_codes.append(f"DOMAIN_STATUS_UNKNOWN_{label.upper()}")
            continue
        domain_status[label] = status
        if status == "WITHHOLD":
            reason_codes.append(f"DOMAIN_WITHHELD_{label.upper()}")

    shuttle_shortfalls = _shuttle_shortfalls(shuttle_plan)
    unassigned = _unassigned_sessions(classroom_plan)
    if shuttle_shortfalls or unassigned:
        reason_codes.append("CROSS_DOMAIN_CONFLICTS_REQUIRE_OPERATOR_REVIEW")

    campus_context = _campus_demand_context(campus_state)
    return {
        "contract_version": CONTRACT_VERSION,
        "decision_provenance": "POLICY_HEURISTIC",
        "decision_readiness": "REVIEW_REQUIRED",
        "abstained": False,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "cross_domain_signals": {
            "campus_demand_context": campus_context,
            "food_demand_context": dict(campus_context),
            "food_recommended_production": _food_target(food_decision),
            "energy_occupancy_context": dict(campus_context),
            "energy_zone_modes": _energy_modes(energy_decision),
            "shared_capacity_allocations": _shared_allocations(shared_capacity_decision),
            "shuttle_capacity_shortfall_routes": shuttle_shortfalls,
            "unassigned_sessions": unassigned,
            "building_attendance_targets": _building_attendance_targets(classroom_plan),
        },
        "domain_status": domain_status,
        "reason_codes": list(dict.fromkeys(reason_codes)),
        "limitations": list(LIMITATIONS),
    }
