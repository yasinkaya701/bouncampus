from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

CONTRACT_VERSION = "campus-ops-v1.0"
READINESS_STATES = frozenset({"PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD"})
PROVENANCE_STATES = frozenset({"PUBLIC_SOURCE", "MODEL_ESTIMATE", "POLICY_HEURISTIC", "MEASURED_PILOT"})

PERSON_LEVEL_KEYS = frozenset(
    {
        "student_id",
        "studentid",
        "bucard_id",
        "bucardid",
        "user_id",
        "userid",
        "person_id",
        "personid",
        "national_id",
        "tc_kimlik",
        "email",
        "phone",
        "scholarship_status",
        "individual_trace",
        "device_mac",
        "mac_address",
    }
)


def _normalized_key(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_")


def validate_no_person_level_data(value: Any, *, path: str = "payload") -> None:
    """Reject person-level identifiers anywhere in a campus-ops payload."""

    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = _normalized_key(key)
            if normalized in PERSON_LEVEL_KEYS:
                raise ValueError(
                    f"person-level data is not allowed in campus operations: {path}.{key}"
                )
            validate_no_person_level_data(nested, path=f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, nested in enumerate(value):
            validate_no_person_level_data(nested, path=f"{path}[{index}]")


def decision_envelope(
    *,
    readiness: str,
    reason_codes: Sequence[str],
    scope: str,
) -> dict[str, Any]:
    state = str(readiness).upper()
    if state not in READINESS_STATES:
        raise ValueError(f"unsupported readiness state: {readiness}")
    return {
        "contract_version": CONTRACT_VERSION,
        "scope": scope,
        "decision_readiness": state,
        "abstained": state == "WITHHOLD",
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "reason_codes": list(dict.fromkeys(str(code) for code in reason_codes if str(code))),
    }
