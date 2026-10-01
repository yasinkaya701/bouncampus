from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

CONTRACT_VERSION = "campus-ops-v1.0"
READINESS_STATES = ("PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD")
PROVENANCE_STATES = (
    "OFFICIAL_PUBLIC",
    "OFFICIAL_LIVE",
    "OFFICIAL_SNAPSHOT",
    "EXTERNAL_LIVE",
    "MODEL_ESTIMATE",
    "OPERATOR_MEASUREMENT",
    "POLICY_HEURISTIC",
    "SCENARIO",
    "GENERATED_SANDBOX",
    "UNAVAILABLE",
)
PROVENANCE_ALIASES = {
    "PUBLIC_SOURCE": "OFFICIAL_PUBLIC",
    "MEASURED_PILOT": "OPERATOR_MEASUREMENT",
}
VERIFIED_CAPACITY_PROVENANCE = frozenset(
    {
        "OFFICIAL_PUBLIC",
        "OFFICIAL_LIVE",
        "OFFICIAL_SNAPSHOT",
        "OPERATOR_MEASUREMENT",
    }
)

FORBIDDEN_PERSON_LEVEL_KEYS = {
    "student_id",
    "studentid",
    "bucard_id",
    "bucardid",
    "user_id",
    "userid",
    "person_id",
    "personid",
    "email",
    "phone",
    "scholarship",
    "scholarship_status",
    "national_id",
    "tc_kimlik",
    "device_id",
    "deviceid",
    "wifi_client_id",
    "wifi_clientid",
}

TRUTH_BOUNDARY_LIMITATIONS = (
    "NO_LIVE_BMS_CLAIM",
    "NO_LIVE_TURNSTILE_OR_WIFI_OCCUPANCY_CLAIM",
    "NO_LIVE_SHUTTLE_GPS_CLAIM",
    "NO_LIVE_CAFETERIA_POS_CLAIM",
    "NO_LIVE_REGISTRAR_INTEGRATION_CLAIM",
    "UNMEASURED_IMPACT_NO_SAVINGS_CLAIM",
)


def normalize_provenance(value: Any, *, field: str = "provenance") -> str:
    """Return the canonical provenance label, accepting only documented aliases."""

    candidate = str(value or "").strip().upper()
    candidate = PROVENANCE_ALIASES.get(candidate, candidate)
    if candidate not in PROVENANCE_STATES:
        raise ValueError(f"unsupported {field}: {value}")
    return candidate


def is_verified_capacity_provenance(value: Any) -> bool:
    try:
        return normalize_provenance(value) in VERIFIED_CAPACITY_PROVENANCE
    except ValueError:
        return False


def validate_no_person_level_data(value: Any, *, path: str = "root") -> None:
    """Reject person-level identifiers anywhere in an aggregate CS1 payload."""

    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_").replace(" ", "_")
            if normalized in FORBIDDEN_PERSON_LEVEL_KEYS:
                raise ValueError(
                    f"person-level data is not accepted by campus operations: {path}.{key}"
                )
            validate_no_person_level_data(child, path=f"{path}.{key}")
        return

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            validate_no_person_level_data(child, path=f"{path}[{index}]")


def build_decision_envelope(
    *,
    domain: str,
    readiness: str,
    recommendation: Any,
    reason_codes: Sequence[str] = (),
    limitations: Sequence[str] = (),
    provenance: str = "POLICY_HEURISTIC",
) -> dict[str, Any]:
    readiness_value = str(readiness).upper()
    if readiness_value not in READINESS_STATES:
        raise ValueError(f"unsupported readiness: {readiness}")
    provenance_value = normalize_provenance(provenance)

    abstained = readiness_value == "WITHHOLD"
    return {
        "contract_version": CONTRACT_VERSION,
        "domain": str(domain),
        "decision_readiness": readiness_value,
        "abstained": abstained,
        "recommendation": None if abstained else recommendation,
        "decision_provenance": provenance_value,
        "operator_approval_required": True,
        "automatic_execution_allowed": False,
        "reason_codes": list(dict.fromkeys(str(code) for code in reason_codes)),
        "limitations": list(
            dict.fromkeys(
                [*(str(item) for item in limitations), *TRUTH_BOUNDARY_LIMITATIONS]
            )
        ),
    }
