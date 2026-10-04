from __future__ import annotations

import math
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

NEUTRAL_POPULARITY_SCORE = 0.80
MIN_MENU_FACTOR = 0.90
MAX_MENU_FACTOR = 1.12
POPULARITY_TO_FACTOR_SLOPE = 0.80

_COMPONENT_WEIGHTS = {
    "main_dish": 0.60,
    "soup": 0.15,
    "vegan_dish": 0.10,
    "sides": 0.10,
    "options": 0.05,
}

_TURKISH_ASCII = str.maketrans(
    {
        "ı": "i",
        "ş": "s",
        "ğ": "g",
        "ç": "c",
        "ö": "o",
        "ü": "u",
    }
)


def _normalize_name(value: Any) -> str:
    text = str(value or "").strip().casefold().translate(_TURKISH_ASCII)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _finite_float(value: Any) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    return numeric


def _catalog_entries(catalog: Iterable[Mapping[str, Any]]) -> list[tuple[str, float]]:
    entries: list[tuple[str, float]] = []
    for row in catalog:
        name = _normalize_name(row.get("name"))
        score = _finite_float(row.get("popularity_score"))
        if not name or score is None:
            continue
        entries.append((name, min(1.0, max(0.0, score))))
    return entries


def _match_score(name: Any, entries: Sequence[tuple[str, float]]) -> float | None:
    needle = _normalize_name(name)
    if not needle or needle == "unavailable":
        return None

    exact = [score for candidate, score in entries if candidate == needle]
    if exact:
        return exact[0]

    candidates = [
        (len(candidate), score)
        for candidate, score in entries
        if len(candidate) >= 4 and (candidate in needle or needle in candidate)
    ]
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def _component_items(live_menu: Mapping[str, Any]) -> list[tuple[str, float]]:
    items: list[tuple[str, float]] = []
    for key in ("main_dish", "soup", "vegan_dish"):
        value = live_menu.get(key)
        if value:
            items.append((str(value), _COMPONENT_WEIGHTS[key]))

    for key in ("sides", "options"):
        raw = live_menu.get(key) or []
        values = [str(value) for value in raw if value]
        if not values:
            continue
        share = _COMPONENT_WEIGHTS[key] / len(values)
        items.extend((value, share) for value in values)
    return items


def build_menu_demand_adjustment(
    live_menu: Mapping[str, Any],
    catalog: Iterable[Mapping[str, Any]],
    *,
    official_menu: bool,
) -> dict[str, Any]:
    """Build a bounded menu-driven demand adjustment from heuristic popularity data.

    This is deliberately a policy heuristic, not a measured elasticity estimate. An
    unverified/fallback menu source is forced to a neutral factor so stale menu data
    cannot change the production forecast.
    """

    if not official_menu:
        return {
            "factor": 1.0,
            "popularity_score": None,
            "matched_weight": 0.0,
            "matched_items": [],
            "unmatched_items": [],
            "provenance": "UNAVAILABLE",
            "reason_codes": ["MENU_SOURCE_NOT_VERIFIED_LIVE"],
        }

    entries = _catalog_entries(catalog)
    weighted_score = 0.0
    matched_weight = 0.0
    matched_items: list[str] = []
    unmatched_items: list[str] = []
    total_present_weight = 0.0

    for item_name, weight in _component_items(live_menu):
        total_present_weight += weight
        score = _match_score(item_name, entries)
        if score is None:
            weighted_score += NEUTRAL_POPULARITY_SCORE * weight
            unmatched_items.append(item_name)
            continue
        weighted_score += score * weight
        matched_weight += weight
        matched_items.append(item_name)

    missing_weight = max(0.0, 1.0 - total_present_weight)
    weighted_score += NEUTRAL_POPULARITY_SCORE * missing_weight

    if matched_weight > 0:
        factor = 1.0 + (weighted_score - NEUTRAL_POPULARITY_SCORE) * POPULARITY_TO_FACTOR_SLOPE
        factor = min(MAX_MENU_FACTOR, max(MIN_MENU_FACTOR, factor))
        return {
            "factor": round(factor, 4),
            "popularity_score": round(weighted_score, 4),
            "matched_weight": round(matched_weight, 4),
            "matched_items": matched_items,
            "unmatched_items": unmatched_items,
            "provenance": "POLICY_HEURISTIC_CATALOG",
            "reason_codes": ["MENU_POPULARITY_HEURISTIC_APPLIED"],
        }

    source_factor = _finite_float(live_menu.get("popularity_multiplier"))
    if source_factor is not None:
        bounded = min(MAX_MENU_FACTOR, max(MIN_MENU_FACTOR, source_factor))
        return {
            "factor": round(bounded, 4),
            "popularity_score": None,
            "matched_weight": 0.0,
            "matched_items": [],
            "unmatched_items": unmatched_items,
            "provenance": "POLICY_HEURISTIC_SOURCE",
            "reason_codes": ["SOURCE_MULTIPLIER_FALLBACK"],
        }

    return {
        "factor": 1.0,
        "popularity_score": None,
        "matched_weight": 0.0,
        "matched_items": [],
        "unmatched_items": unmatched_items,
        "provenance": "POLICY_HEURISTIC_NEUTRAL",
        "reason_codes": ["NO_MATCHED_MENU_POPULARITY_SIGNAL"],
    }


def apply_menu_adjustment(predicted_demand: Any, factor: Any) -> int:
    demand = _finite_float(predicted_demand)
    adjustment = _finite_float(factor)
    if demand is None or demand <= 0:
        return 0
    if adjustment is None:
        adjustment = 1.0
    adjustment = min(MAX_MENU_FACTOR, max(MIN_MENU_FACTOR, adjustment))
    return max(0, int(round(demand * adjustment)))
