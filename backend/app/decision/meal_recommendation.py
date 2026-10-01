from __future__ import annotations

import math
from statistics import mean
from typing import Any, Mapping, Sequence

POLICY_VERSION = "meal-recommendation-v1.0"
METHOD_SCOPE = "TRANSPARENT_PERSONALIZATION_BASELINE"
CLAIM_BOUNDARY = (
    "Ranking scores are decision-support preferences, not probabilities, health advice, "
    "or evidence of food-waste reduction. The collaborative ALS prototype is not used "
    "by this baseline until its generated-data provenance is validated offline."
)


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _unit_interval(value: Any) -> float | None:
    number = _number(value)
    if number is None:
        return None
    return min(max(number, 0.0), 1.0)


def _rating(value: Any) -> float | None:
    number = _number(value)
    if number is None or number < 1.0 or number > 5.0:
        return None
    return number


def _clean_tags(value: Any) -> set[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return set()
    return {str(tag).strip().lower() for tag in value if str(tag).strip()}


def _population_prior(item: Mapping[str, Any]) -> float:
    popularity = _unit_interval(item.get("popularity_score"))
    avg_rating = _rating(item.get("avg_rating"))
    rating_score = None if avg_rating is None else (avg_rating - 1.0) / 4.0
    components = [value for value in (popularity, rating_score) if value is not None]
    return mean(components) if components else 0.5


def _shrunken_preference(
    ratings: Sequence[float],
    *,
    prior: float,
    shrinkage: float,
) -> float:
    if not ratings:
        return prior
    raw = (mean(ratings) - 1.0) / 4.0
    weight = len(ratings) / (len(ratings) + shrinkage)
    return weight * raw + (1.0 - weight) * prior


def rank_menu_items(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Rank current menu items using population priors and explicit feedback only.

    The function is deliberately dependency-free and auditable. Dietary exclusions are
    hard filters. Personalization is learned only from valid 1..5 explicit feedback;
    missing feedback falls back to a deterministic population prior. This is intended as
    the benchmark that any collaborative or contextual model must beat on held-out data.
    """

    raw_items = payload.get("menu_items")
    raw_items = (
        raw_items
        if isinstance(raw_items, Sequence) and not isinstance(raw_items, (str, bytes))
        else []
    )
    raw_feedback = payload.get("feedback")
    raw_feedback = (
        raw_feedback
        if isinstance(raw_feedback, Sequence) and not isinstance(raw_feedback, (str, bytes))
        else []
    )
    constraints = payload.get("constraints")
    constraints = constraints if isinstance(constraints, Mapping) else {}
    excluded_tags = _clean_tags(constraints.get("excluded_tags"))

    item_ratings: dict[str, list[float]] = {}
    category_ratings: dict[str, list[float]] = {}
    valid_feedback_rows = 0
    invalid_feedback_rows = 0

    for row in raw_feedback:
        if not isinstance(row, Mapping):
            invalid_feedback_rows += 1
            continue
        item_id = str(row.get("item_id") or "").strip()
        category = str(row.get("category") or "").strip().lower()
        rating = _rating(row.get("rating"))
        if not item_id or rating is None:
            invalid_feedback_rows += 1
            continue
        valid_feedback_rows += 1
        item_ratings.setdefault(item_id, []).append(rating)
        if category:
            category_ratings.setdefault(category, []).append(rating)

    ranked: list[dict[str, Any]] = []
    excluded_item_ids: list[str] = []
    invalid_item_rows = 0

    for row in raw_items:
        if not isinstance(row, Mapping):
            invalid_item_rows += 1
            continue
        item_id = str(row.get("item_id") or row.get("name") or "").strip()
        name = str(row.get("name") or item_id).strip()
        category = str(row.get("category") or "unknown").strip().lower() or "unknown"
        if not item_id or not name:
            invalid_item_rows += 1
            continue
        tags = _clean_tags(row.get("tags"))
        if excluded_tags.intersection(tags):
            excluded_item_ids.append(item_id)
            continue

        prior = _population_prior(row)
        item_history = item_ratings.get(item_id, [])
        category_history = category_ratings.get(category, [])
        components = [prior]
        evidence_n = 0
        reasons = ["POPULATION_PRIOR"]

        if item_history:
            components.append(
                _shrunken_preference(item_history, prior=prior, shrinkage=2.0)
            )
            evidence_n += len(item_history)
            reasons.append("EXPLICIT_ITEM_FEEDBACK")
        if category_history:
            components.append(
                _shrunken_preference(category_history, prior=prior, shrinkage=4.0)
            )
            evidence_n += len(category_history)
            reasons.append("EXPLICIT_CATEGORY_FEEDBACK")

        score = mean(components)
        ranked.append(
            {
                "item_id": item_id,
                "name": name,
                "category": category,
                "tags": sorted(tags),
                "score": round(score, 6),
                "population_prior": round(prior, 6),
                "personalization_evidence_n": evidence_n,
                "reason_codes": reasons,
            }
        )

    ranked.sort(
        key=lambda item: (
            -item["score"],
            -item["population_prior"],
            item["item_id"],
        )
    )

    reason_codes: list[str] = []
    if valid_feedback_rows == 0:
        reason_codes.append("COLD_START_POPULATION_PRIOR")
    if invalid_feedback_rows:
        reason_codes.append("PARTIAL_INVALID_FEEDBACK")
    if invalid_item_rows:
        reason_codes.append("PARTIAL_INVALID_MENU_ITEMS")
    if excluded_item_ids:
        reason_codes.append("DIETARY_HARD_FILTER_APPLIED")
    if not ranked:
        reason_codes.insert(0, "NO_ELIGIBLE_MENU_ITEMS")

    return {
        "policy_version": POLICY_VERSION,
        "method_scope": METHOD_SCOPE,
        "ranked_items": ranked,
        "excluded_item_ids": excluded_item_ids,
        "feedback_rows_used": valid_feedback_rows,
        "invalid_feedback_rows": invalid_feedback_rows,
        "invalid_item_rows": invalid_item_rows,
        "collaborative_model_used": False,
        "reason_codes": reason_codes,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_recommendation_impression(
    ranking: Mapping[str, Any],
    *,
    request_id: str,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create the audit record needed to evaluate recommendation quality later.

    Outcomes are intentionally absent at impression time. A downstream feedback event
    should reference this request_id and the selected/rated item so offline evaluation
    can preserve the decision-time information boundary.
    """

    clean_request_id = str(request_id or "").strip()
    if not clean_request_id:
        raise ValueError("request_id is required for recommendation provenance")
    ranked_items = ranking.get("ranked_items")
    if not isinstance(ranked_items, Sequence) or isinstance(ranked_items, (str, bytes)):
        ranked_items = []
    ranked_item_ids = [
        str(item.get("item_id"))
        for item in ranked_items
        if isinstance(item, Mapping) and item.get("item_id") is not None
    ]
    clean_context = dict(context) if isinstance(context, Mapping) else {}

    return {
        "event_scope": "RECOMMENDATION_IMPRESSION",
        "request_id": clean_request_id,
        "policy_version": str(ranking.get("policy_version") or POLICY_VERSION),
        "method_scope": str(ranking.get("method_scope") or METHOD_SCOPE),
        "ranked_item_ids": ranked_item_ids,
        "context": clean_context,
        "outcome_observed": False,
        "selected_item_id": None,
        "rating": None,
        "claim_boundary": (
            "Impression logging records what was shown at decision time; it is not an outcome."
        ),
    }
