"""Canonical fail-closed readiness aggregation for CS1 campus operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

POLICY_VERSION = "campus-ops-v1.0"
OBJECTIVE_UNITS = "REGISTERED_RELATIVE_SENSITIVITY_UNITS"
POLICY_INPUT_PROVENANCE = "REGISTERED_POLICY_INPUT_NOT_OBSERVED_ECONOMICS"
READINESS_ORDER = {"PILOT_READY": 0, "REVIEW_REQUIRED": 1, "WITHHOLD": 2}


def _base() -> dict[str, Any]:
    return {
        "policy_version": POLICY_VERSION,
        "scope": "CAMPUS_OPERATIONS_BUNDLE",
        "objective_units": OBJECTIVE_UNITS,
        "policy_input_provenance": POLICY_INPUT_PROVENANCE,
        "operator_approval_required": True,
        "automatic_dispatch": False,
        "automatic_actuation": False,
        "impact_claim_allowed": False,
    }


def build_campus_ops_bundle(modules: Mapping[str, Any] | Any) -> dict[str, Any]:
    """Aggregate module readiness without trusting caller-provided result shapes.

    A bundle can never become more actionable than its most conservative module.
    Malformed module results, missing readiness, or unknown readiness labels are
    converted to ``WITHHOLD`` rather than raising or being silently ignored.
    """

    result = _base()
    if not isinstance(modules, Mapping):
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "module_states": {},
            "reason_codes": ["INVALID_CAMPUS_OPS_MODULES"],
        }
    if not modules:
        return {
            **result,
            "decision_readiness": "WITHHOLD",
            "module_states": {},
            "reason_codes": ["NO_CAMPUS_OPS_MODULES"],
        }

    module_states: dict[str, str] = {}
    reasons: list[str] = []
    for raw_module_id, module_result in modules.items():
        module_id = str(raw_module_id)
        if not isinstance(module_result, Mapping):
            module_states[module_id] = "WITHHOLD"
            reasons.append(f"INVALID_MODULE_RESULT_{module_id}")
            continue

        raw_state = module_result.get("decision_readiness")
        if raw_state is None or not str(raw_state).strip():
            module_states[module_id] = "WITHHOLD"
            reasons.append(f"MISSING_READINESS_{module_id}")
            continue

        state = str(raw_state).strip().upper()
        if state not in READINESS_ORDER:
            state = "WITHHOLD"
            reasons.append(f"UNKNOWN_READINESS_{module_id}")
        module_states[module_id] = state

    readiness = max(module_states.values(), key=lambda state: READINESS_ORDER[state])
    return {
        **result,
        "decision_readiness": readiness,
        "module_states": module_states,
        "reason_codes": reasons,
    }
