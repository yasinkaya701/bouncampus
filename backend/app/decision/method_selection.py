"""Fail-closed method-selection gate for CS1 baseline-first evaluation."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

SUPPORTED_LOWER_IS_BETTER_METRICS = ("mae", "rmse", "wape_pct", "mean_loss")
STAGE_ELIGIBILITY = {
    "OFFLINE_EVALUATION": frozenset(
        {"EVALUATED_OFFLINE", "PILOT_ELIGIBLE", "PILOT_EVALUATED"}
    ),
    "PILOT": frozenset({"PILOT_ELIGIBLE", "PILOT_EVALUATED"}),
}


def _metric_value(value):
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def _integer_support_count(value: object) -> int:
    """Parse a non-negative integer count without silently truncating evidence."""

    if isinstance(value, bool):
        raise ValueError("comparison common_support_n must be an integer")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("comparison common_support_n must be an integer") from exc
    if not math.isfinite(numeric) or numeric < 0 or not numeric.is_integer():
        raise ValueError("comparison common_support_n must be an integer")
    return int(numeric)


def _withhold(
    *,
    baseline_id: str,
    stage: str,
    primary_metric: str,
    common_support_n: int,
    min_common_support_n: int,
    min_relative_improvement_pct: float,
    reason_codes: Sequence[str],
) -> dict[str, object]:
    return {
        "selection_status": "WITHHOLD",
        "selected_method": None,
        "selected_method_eligibility": None,
        "selection_rule": "NO_DEFENSIBLE_SELECTION",
        "baseline_id": baseline_id,
        "primary_metric": primary_metric,
        "baseline_metric": None,
        "selected_metric": None,
        "relative_improvement_pct_vs_baseline": None,
        "common_support_n": common_support_n,
        "min_common_support_n": min_common_support_n,
        "min_relative_improvement_pct": min_relative_improvement_pct,
        "stage": stage,
        "candidate_assessments": {},
        "reason_codes": list(reason_codes),
        "result_scope": "METHOD_SELECTION_GATE_ONLY",
        "claim_boundary": (
            "Method selection does not establish operational readiness or achieved impact."
        ),
    }


def select_method(
    comparison: Mapping[str, object],
    *,
    baseline_id: str,
    method_eligibility: Mapping[str, str],
    stage: str,
    primary_metric: str,
    min_common_support_n: int,
    min_relative_improvement_pct: float,
    candidate_method_ids: Sequence[str] | None = None,
) -> dict[str, object]:
    """Select a method only when it defensibly beats a designated baseline.

    Thresholds are caller-supplied registered policy inputs. This function does not
    invent promotion thresholds, economic weights, or pilot-readiness claims.
    Malformed measured metrics fail closed as unavailable evidence.
    """

    if stage not in STAGE_ELIGIBILITY:
        raise ValueError(f"unsupported selection stage {stage!r}")
    if primary_metric not in SUPPORTED_LOWER_IS_BETTER_METRICS:
        raise ValueError(
            f"primary_metric must be one of {SUPPORTED_LOWER_IS_BETTER_METRICS!r}"
        )
    if min_common_support_n < 1:
        raise ValueError("min_common_support_n must be >= 1")
    min_improvement = float(min_relative_improvement_pct)
    if not math.isfinite(min_improvement) or min_improvement < 0:
        raise ValueError("min_relative_improvement_pct must be finite and non-negative")

    metrics = comparison.get("metrics")
    if not isinstance(metrics, Mapping):
        raise ValueError("comparison must contain a metrics mapping")

    common_support_n = _integer_support_count(comparison.get("common_support_n", 0))
    if common_support_n < min_common_support_n:
        return _withhold(
            baseline_id=baseline_id,
            stage=stage,
            primary_metric=primary_metric,
            common_support_n=common_support_n,
            min_common_support_n=min_common_support_n,
            min_relative_improvement_pct=min_improvement,
            reason_codes=["INSUFFICIENT_COMMON_SUPPORT"],
        )

    baseline_metrics = metrics.get(baseline_id)
    if not isinstance(baseline_metrics, Mapping):
        return _withhold(
            baseline_id=baseline_id,
            stage=stage,
            primary_metric=primary_metric,
            common_support_n=common_support_n,
            min_common_support_n=min_common_support_n,
            min_relative_improvement_pct=min_improvement,
            reason_codes=["DESIGNATED_BASELINE_MISSING"],
        )

    baseline_metric = _metric_value(baseline_metrics.get(primary_metric))
    if baseline_metric is None:
        return _withhold(
            baseline_id=baseline_id,
            stage=stage,
            primary_metric=primary_metric,
            common_support_n=common_support_n,
            min_common_support_n=min_common_support_n,
            min_relative_improvement_pct=min_improvement,
            reason_codes=["DESIGNATED_BASELINE_METRIC_UNAVAILABLE"],
        )

    allowed_states = STAGE_ELIGIBILITY[stage]
    baseline_eligibility = method_eligibility.get(baseline_id, "SANDBOX_ONLY")
    if baseline_eligibility not in allowed_states:
        result = _withhold(
            baseline_id=baseline_id,
            stage=stage,
            primary_metric=primary_metric,
            common_support_n=common_support_n,
            min_common_support_n=min_common_support_n,
            min_relative_improvement_pct=min_improvement,
            reason_codes=["BASELINE_NOT_ELIGIBLE_FOR_STAGE"],
        )
        result["baseline_metric"] = baseline_metric
        return result

    if candidate_method_ids is None:
        candidate_ids = [name for name in metrics if name != baseline_id]
    else:
        candidate_ids = []
        seen: set[str] = set()
        for name in candidate_method_ids:
            if name != baseline_id and name not in seen:
                candidate_ids.append(name)
                seen.add(name)

    candidate_assessments: dict[str, dict[str, object]] = {}
    eligible_candidates: list[tuple[str, float, float | None]] = []

    for method_id in candidate_ids:
        eligibility = method_eligibility.get(method_id, "SANDBOX_ONLY")
        eligible_for_stage = eligibility in allowed_states
        reasons: list[str] = []
        method_metrics = metrics.get(method_id)
        metric = (
            _metric_value(method_metrics.get(primary_metric))
            if isinstance(method_metrics, Mapping)
            else None
        )
        if not eligible_for_stage:
            reasons.append("METHOD_NOT_ELIGIBLE_FOR_STAGE")
        if metric is None:
            reasons.append("METRIC_UNAVAILABLE")

        improvement_pct: float | None = None
        beats_baseline = False
        if metric is not None and baseline_metric > 0:
            improvement_pct = ((baseline_metric - metric) / baseline_metric) * 100
            beats_baseline = (
                metric < baseline_metric and improvement_pct >= min_improvement
            )
        elif metric is not None and baseline_metric == 0:
            reasons.append("ZERO_BASELINE_METRIC_NO_RELATIVE_IMPROVEMENT")

        if (
            eligible_for_stage
            and metric is not None
            and metric < baseline_metric
            and not beats_baseline
        ):
            reasons.append("CANDIDATE_IMPROVEMENT_BELOW_REGISTERED_GATE")

        candidate_assessments[method_id] = {
            "eligibility": eligibility,
            "eligible_for_stage": eligible_for_stage,
            "metric": metric,
            "relative_improvement_pct_vs_baseline": improvement_pct,
            "beats_baseline": beats_baseline,
            "reason_codes": reasons,
        }
        if eligible_for_stage and metric is not None:
            eligible_candidates.append((method_id, metric, improvement_pct))

    passing_candidates = [
        item
        for item in eligible_candidates
        if candidate_assessments[item[0]]["beats_baseline"] is True
    ]

    if passing_candidates:
        selected_method, selected_metric, improvement_pct = min(
            passing_candidates,
            key=lambda item: (item[1], item[0]),
        )
        reason_codes = ["REGISTERED_PROMOTION_GATE_CLEARED"]
        selection_rule = "CANDIDATE_BEATS_BASELINE"
    else:
        selected_method = baseline_id
        selected_metric = baseline_metric
        improvement_pct = 0.0
        selection_rule = "BASELINE_RETAINED_COMPLEXITY_NOT_JUSTIFIED"
        if any(
            "CANDIDATE_IMPROVEMENT_BELOW_REGISTERED_GATE"
            in assessment["reason_codes"]
            for assessment in candidate_assessments.values()
        ):
            reason_codes = ["CANDIDATE_IMPROVEMENT_BELOW_REGISTERED_GATE"]
        elif not eligible_candidates:
            reason_codes = ["NO_ELIGIBLE_CANDIDATE"]
        else:
            reason_codes = ["NO_ELIGIBLE_CANDIDATE_BEATS_BASELINE"]

    return {
        "selection_status": "SELECTED",
        "selected_method": selected_method,
        "selected_method_eligibility": method_eligibility.get(
            selected_method, "SANDBOX_ONLY"
        ),
        "selection_rule": selection_rule,
        "baseline_id": baseline_id,
        "primary_metric": primary_metric,
        "baseline_metric": baseline_metric,
        "selected_metric": selected_metric,
        "relative_improvement_pct_vs_baseline": improvement_pct,
        "common_support_n": common_support_n,
        "min_common_support_n": min_common_support_n,
        "min_relative_improvement_pct": min_improvement,
        "stage": stage,
        "candidate_assessments": candidate_assessments,
        "reason_codes": reason_codes,
        "result_scope": "METHOD_SELECTION_GATE_ONLY",
        "claim_boundary": (
            "Method selection does not establish operational readiness or achieved impact."
        ),
    }
