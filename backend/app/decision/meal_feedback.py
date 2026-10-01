from __future__ import annotations

import math
from statistics import mean
from typing import Any, Mapping, Sequence

EVALUATION_SCOPE = "OFFLINE_OBSERVED_OUTCOMES_ONLY"
CLAIM_BOUNDARY = (
    "Recommendation outcome metrics describe observed choice/rating behavior for logged "
    "impressions only. They do not establish causal impact, nutrition quality, or waste reduction."
)


def _rating(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("rating must be a number from 1 to 5")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("rating must be a number from 1 to 5") from exc
    if not math.isfinite(number) or number < 1.0 or number > 5.0:
        raise ValueError("rating must be a number from 1 to 5")
    return number


def build_recommendation_outcome(
    impression: Mapping[str, Any],
    *,
    selected_item_id: str,
    rating: Any = None,
    action: str = "SELECTED",
) -> dict[str, Any]:
    """Attach an observed choice/rating to a previously logged impression."""

    if impression.get("event_scope") != "RECOMMENDATION_IMPRESSION":
        raise ValueError("a RECOMMENDATION_IMPRESSION event is required")
    request_id = str(impression.get("request_id") or "").strip()
    if not request_id:
        raise ValueError("impression request_id is required")
    raw_ranked = impression.get("ranked_item_ids")
    if not isinstance(raw_ranked, Sequence) or isinstance(raw_ranked, (str, bytes)):
        raise ValueError("impression ranked_item_ids are required")
    ranked_item_ids = [str(item_id) for item_id in raw_ranked]
    selected = str(selected_item_id or "").strip()
    if not selected or selected not in ranked_item_ids:
        raise ValueError("selected_item_id must reference an item shown in the impression")
    normalized_rating = _rating(rating)
    normalized_action = str(action or "SELECTED").strip().upper()
    if normalized_action not in {"SELECTED", "RATED", "DISMISSED_AFTER_SELECTION"}:
        raise ValueError("unsupported recommendation outcome action")

    return {
        "event_scope": "RECOMMENDATION_OUTCOME",
        "request_id": request_id,
        "policy_version": str(impression.get("policy_version") or "UNKNOWN"),
        "method_scope": str(impression.get("method_scope") or "UNKNOWN"),
        "ranked_item_ids": ranked_item_ids,
        "selected_item_id": selected,
        "selected_rank": ranked_item_ids.index(selected) + 1,
        "rating": normalized_rating,
        "action": normalized_action,
        "outcome_observed": True,
        "claim_boundary": (
            "Outcome is linked to one logged recommendation impression; it is not causal evidence."
        ),
    }


def evaluate_recommendation_outcomes(
    events: Sequence[Any],
    *,
    top_k: int = 3,
) -> dict[str, Any]:
    """Compute transparent ranking metrics from valid observed outcome events."""

    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer")
    if not isinstance(events, Sequence) or isinstance(events, (str, bytes)):
        raise ValueError("events must be a sequence")

    ranks: list[int] = []
    ratings: list[float] = []
    invalid_rows = 0
    policy_versions: set[str] = set()

    for event in events:
        if not isinstance(event, Mapping):
            invalid_rows += 1
            continue
        rank = event.get("selected_rank")
        try:
            rank_int = int(rank)
        except (TypeError, ValueError):
            invalid_rows += 1
            continue
        if (
            event.get("event_scope") != "RECOMMENDATION_OUTCOME"
            or event.get("outcome_observed") is not True
            or rank_int < 1
        ):
            invalid_rows += 1
            continue
        ranked = event.get("ranked_item_ids")
        selected = str(event.get("selected_item_id") or "")
        if (
            not isinstance(ranked, Sequence)
            or isinstance(ranked, (str, bytes))
            or selected not in [str(item_id) for item_id in ranked]
            or rank_int != [str(item_id) for item_id in ranked].index(selected) + 1
        ):
            invalid_rows += 1
            continue
        ranks.append(rank_int)
        policy_versions.add(str(event.get("policy_version") or "UNKNOWN"))
        try:
            valid_rating = _rating(event.get("rating"))
        except ValueError:
            invalid_rows += 1
            ranks.pop()
            continue
        if valid_rating is not None:
            ratings.append(valid_rating)

    if not ranks:
        return {
            "evaluation_scope": EVALUATION_SCOPE,
            "n": 0,
            "invalid_rows": invalid_rows,
            "top_k": top_k,
            "top1_hit_rate": None,
            "top_k_hit_rate": None,
            "mean_reciprocal_rank": None,
            "mean_selected_rank": None,
            "mean_rating": None,
            "policy_versions": sorted(policy_versions),
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return {
        "evaluation_scope": EVALUATION_SCOPE,
        "n": len(ranks),
        "invalid_rows": invalid_rows,
        "top_k": top_k,
        "top1_hit_rate": sum(rank == 1 for rank in ranks) / len(ranks),
        "top_k_hit_rate": sum(rank <= top_k for rank in ranks) / len(ranks),
        "mean_reciprocal_rank": mean(1.0 / rank for rank in ranks),
        "mean_selected_rank": mean(ranks),
        "mean_rating": mean(ratings) if ratings else None,
        "policy_versions": sorted(policy_versions),
        "claim_boundary": CLAIM_BOUNDARY,
    }
