"""Source-health normalization for CS1 campus-operations decisions.

The module is deliberately policy-light: it validates provenance and information
availability at the decision cutoff, but it does not invent freshness thresholds.
Callers may provide ``max_age_seconds`` when a source contract defines one.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
import math
from typing import Any

CANONICAL_PROVENANCE = frozenset(
    {
        "OFFICIAL_PUBLIC",
        "OFFICIAL_LIVE",
        "OFFICIAL_SNAPSHOT",
        "EXTERNAL_LIVE",
        "MODEL_ESTIMATE",
        "OPERATOR_MEASUREMENT",
    }
)

PROVENANCE_ALIASES = {
    "PUBLIC_SOURCE": "OFFICIAL_PUBLIC",
}


def _source_token(source_id: str) -> str:
    token = source_id.strip().upper().replace("-", "_").replace(" ", "_")
    if not token:
        raise ValueError("source_id must be a non-empty string")
    return token


def _parse_timestamp(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip() or "T" not in value:
        raise ValueError(f"{field} timestamp must be an offset-aware ISO-8601 timestamp")
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError as exc:
        raise ValueError(f"{field} timestamp must be an offset-aware ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} timestamp must include a timezone offset")
    return parsed


def _optional_fraction(value: Any, *, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a finite number between 0 and 1")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a finite number between 0 and 1") from exc
    if not math.isfinite(number) or not 0.0 <= number <= 1.0:
        raise ValueError(f"{field} must be a finite number between 0 and 1")
    return number


def _optional_nonnegative_number(value: Any, *, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a finite non-negative number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a finite non-negative number") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field} must be a finite non-negative number")
    return number


def normalize_source(
    source_id: str,
    source: Mapping[str, Any],
    decision_time: str,
    *,
    domain: str = "campus",
) -> dict[str, Any]:
    """Normalize one source into the campus-ops source-health contract."""

    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("source_id must be a non-empty string")
    if not isinstance(source, Mapping):
        raise ValueError(f"source {source_id!r} must be a mapping")
    if not isinstance(domain, str) or not domain.strip():
        raise ValueError("domain must be a non-empty string")

    token = _source_token(source_id)
    cutoff = _parse_timestamp(decision_time, field="decision_time")

    available = source.get("available")
    if not isinstance(available, bool):
        raise ValueError(f"source {source_id!r} available must be boolean")

    provenance_raw = source.get("provenance")
    if not isinstance(provenance_raw, str) or not provenance_raw.strip():
        raise ValueError(f"source {source_id!r} provenance is required")
    provenance = PROVENANCE_ALIASES.get(provenance_raw.strip().upper(), provenance_raw.strip().upper())
    if provenance not in CANONICAL_PROVENANCE:
        raise ValueError(f"source {source_id!r} provenance {provenance_raw!r} is not recognized")

    published_raw = source.get("published_at")
    published = None
    if published_raw is not None:
        published = _parse_timestamp(published_raw, field=f"{source_id}.published_at")

    fetched_raw = source.get("fetched_at")
    if fetched_raw is not None:
        _parse_timestamp(fetched_raw, field=f"{source_id}.fetched_at")

    coverage = _optional_fraction(source.get("coverage"), field=f"{source_id}.coverage")
    max_age_seconds = _optional_nonnegative_number(
        source.get("max_age_seconds"),
        field=f"{source_id}.max_age_seconds",
    )

    reason_codes: list[str] = []
    freshness_seconds: int | None = None

    if not available:
        status = "UNAVAILABLE"
        eligible = False
        reason_codes.append(f"SOURCE_UNAVAILABLE_{token}")
    elif published is None:
        status = "PARTIAL"
        eligible = False
        reason_codes.append(f"SOURCE_TIMESTAMP_MISSING_{token}")
    elif published > cutoff:
        status = "NOT_AVAILABLE_AT_DECISION_TIME"
        eligible = False
        reason_codes.append(f"SOURCE_NOT_AVAILABLE_AT_DECISION_TIME_{token}")
    else:
        freshness_seconds = max(0, int((cutoff - published).total_seconds()))
        if max_age_seconds is not None and freshness_seconds > max_age_seconds:
            status = "STALE"
            eligible = False
            reason_codes.append(f"SOURCE_STALE_{token}")
        elif coverage is not None and coverage < 1.0:
            status = "PARTIAL"
            eligible = True
            reason_codes.append(f"SOURCE_PARTIAL_COVERAGE_{token}")
        else:
            status = "VERIFIED"
            eligible = True

    return {
        "source_id": source_id.strip(),
        "domain": domain.strip(),
        "provenance": provenance,
        "available": available,
        "published_at": published_raw,
        "fetched_at": fetched_raw,
        "decision_cutoff": decision_time,
        "freshness_seconds": freshness_seconds,
        "coverage": coverage,
        "status": status,
        "eligible_at_decision_time": eligible,
        "reason_codes": reason_codes,
    }


def normalize_sources(
    sources: Mapping[str, Mapping[str, Any]],
    decision_time: str,
    *,
    domain: str = "campus",
) -> list[dict[str, Any]]:
    """Normalize a mapping of source-id -> source contract in insertion order."""

    if not isinstance(sources, Mapping):
        raise ValueError("sources must be a mapping")
    normalized: list[dict[str, Any]] = []
    for source_id, source in sources.items():
        if not isinstance(source, Mapping):
            raise ValueError(f"source {source_id!r} must be a mapping")
        normalized.append(
            normalize_source(source_id, source, decision_time, domain=domain)
        )
    return normalized
