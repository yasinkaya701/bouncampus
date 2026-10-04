"""Past-only contextual residual correction and ablation for CS1.

This module does not assume that menu, academic-calendar, weather, or any other
context signal is useful. A signal may alter a forecast only when it was
available by the decision cutoff and sufficient prior reconciled rows exist for
the same context. Reconciled outcomes enter history only after their explicit
reconciliation timestamp is visible to the current decision cutoff.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import math
from statistics import median
from typing import Any, Sequence

SUPPORTED_RESIDUAL_STATISTICS = frozenset({"MEAN", "MEDIAN"})


def _non_negative_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def _context_key(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _aware_timestamp(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _aggregate_residual(values: Sequence[float], statistic: str) -> float:
    if statistic == "MEAN":
        return sum(values) / len(values)
    if statistic == "MEDIAN":
        return float(median(values))
    raise ValueError(f"unsupported residual statistic {statistic!r}")


def _validated_decision_cutoffs(values: Sequence[Any]) -> list[datetime]:
    cutoffs: list[datetime] = []
    for raw in values:
        cutoff = _aware_timestamp(raw)
        if cutoff is None:
            raise ValueError(
                "decision_cutoff_at must contain timezone-aware timestamps"
            )
        if cutoffs and cutoff < cutoffs[-1]:
            raise ValueError("decision_cutoff_at must be chronological")
        cutoffs.append(cutoff)
    return cutoffs


def _validated_reconciliation_times(
    *,
    outcome_reconciled: Sequence[bool],
    outcome_reconciled_at: Sequence[Any],
    decision_cutoffs: Sequence[datetime],
) -> list[datetime | None]:
    reconciled_times: list[datetime | None] = []
    for reconciled, raw_time, own_cutoff in zip(
        outcome_reconciled,
        outcome_reconciled_at,
        decision_cutoffs,
    ):
        reconciled_at = _aware_timestamp(raw_time)
        if reconciled:
            if reconciled_at is None:
                raise ValueError(
                    "reconciled outcome requires outcome_reconciled_at"
                )
            if reconciled_at <= own_cutoff:
                raise ValueError(
                    "outcome_reconciled_at must be after its own decision cutoff"
                )
        elif raw_time is not None and str(raw_time).strip():
            raise ValueError(
                "unreconciled outcome must not provide outcome_reconciled_at"
            )
        reconciled_times.append(reconciled_at if reconciled else None)
    return reconciled_times


def generate_context_residual_forecasts(
    *,
    base_forecasts: Sequence[float | int | None],
    actual_demand: Sequence[float | int | None],
    context_keys: Sequence[Any],
    signal_available_at: Sequence[Any],
    decision_cutoff_at: Sequence[Any],
    outcome_reconciled: Sequence[bool],
    outcome_reconciled_at: Sequence[Any],
    min_history: int,
    min_context_history: int,
    shrinkage_strength: float,
    residual_statistic: str = "MEAN",
) -> dict[str, object]:
    """Generate transparent context-corrected forecasts without truth leakage.

    For each row, the base forecast may be corrected from residual history built
    only from earlier rows whose accepted outcome was already reconciled by the
    current row's decision cutoff. A reconciled flag without an availability
    timestamp is rejected because it cannot prove historical observability.

    If the current context was known by decision cutoff and has enough accepted
    prior observations, its residual statistic is partially pooled toward the
    corresponding global residual statistic::

        weight = n_context / (n_context + shrinkage_strength)
        correction = weight * context_stat + (1 - weight) * global_stat

    ``decision_cutoff_at`` must be chronological. The current row is never learned
    before its own forecast, and its outcome timestamp must be after its own cutoff.
    """

    lengths = {
        len(base_forecasts),
        len(actual_demand),
        len(context_keys),
        len(signal_available_at),
        len(decision_cutoff_at),
        len(outcome_reconciled),
        len(outcome_reconciled_at),
    }
    if len(lengths) != 1:
        raise ValueError("context-signal inputs must have the same length")
    if min_history < 1:
        raise ValueError("min_history must be >= 1")
    if min_context_history < 1:
        raise ValueError("min_context_history must be >= 1")
    shrinkage = float(shrinkage_strength)
    if not math.isfinite(shrinkage) or shrinkage < 0:
        raise ValueError("shrinkage_strength must be finite and non-negative")
    statistic = str(residual_statistic or "").strip().upper()
    if statistic not in SUPPORTED_RESIDUAL_STATISTICS:
        raise ValueError(
            f"residual_statistic must be one of {tuple(sorted(SUPPORTED_RESIDUAL_STATISTICS))!r}"
        )
    if any(not isinstance(value, bool) for value in outcome_reconciled):
        raise ValueError("outcome_reconciled must contain explicit booleans")

    decision_cutoffs = _validated_decision_cutoffs(decision_cutoff_at)
    reconciliation_times = _validated_reconciliation_times(
        outcome_reconciled=outcome_reconciled,
        outcome_reconciled_at=outcome_reconciled_at,
        decision_cutoffs=decision_cutoffs,
    )

    global_residuals: list[float] = []
    context_residuals: dict[str, list[float]] = defaultdict(list)
    pending_residuals: list[tuple[datetime, float, str | None, bool]] = []

    baseline_forecast: list[float | None] = []
    context_forecast: list[float | None] = []
    context_applied: list[bool] = []
    history_n: list[int] = []
    context_history_n: list[int] = []
    reason_codes: list[list[str]] = []

    for index in range(len(base_forecasts)):
        cutoff = decision_cutoffs[index]

        # Promote only previously produced outcomes that were actually reconciled
        # by this decision cutoff. Later-reconciled truth remains pending.
        still_pending: list[tuple[datetime, float, str | None, bool]] = []
        for reconciled_at, residual, historical_key, historical_signal_usable in pending_residuals:
            if reconciled_at <= cutoff:
                global_residuals.append(residual)
                if historical_signal_usable and historical_key is not None:
                    context_residuals[historical_key].append(residual)
            else:
                still_pending.append(
                    (
                        reconciled_at,
                        residual,
                        historical_key,
                        historical_signal_usable,
                    )
                )
        pending_residuals = still_pending

        base = _non_negative_number(base_forecasts[index])
        actual = _non_negative_number(actual_demand[index])
        key = _context_key(context_keys[index])
        available = _aware_timestamp(signal_available_at[index])
        reconciled = outcome_reconciled[index]
        reconciled_at = reconciliation_times[index]
        signal_usable = (
            key is not None
            and available is not None
            and available <= cutoff
        )

        history_n.append(len(global_residuals))
        key_history = context_residuals.get(key, []) if key is not None else []
        context_history_n.append(len(key_history))
        reasons: list[str] = []

        if base is None:
            baseline = None
            contextual = None
            applied = False
            reasons.append("BASE_FORECAST_UNAVAILABLE")
        else:
            if len(global_residuals) >= min_history:
                global_stat = _aggregate_residual(global_residuals, statistic)
                baseline = max(base + global_stat, 0.0)
            else:
                global_stat = 0.0
                baseline = base
                reasons.append("INSUFFICIENT_GLOBAL_HISTORY_FOR_RESIDUAL_CORRECTION")

            contextual = baseline
            applied = False
            if key is None:
                reasons.append("CONTEXT_KEY_UNAVAILABLE")
            elif available is None:
                reasons.append("INVALID_SIGNAL_TIMING")
            elif available > cutoff:
                reasons.append("SIGNAL_NOT_AVAILABLE_AT_DECISION_TIME")
            elif len(global_residuals) < min_history:
                pass
            elif len(key_history) < min_context_history:
                reasons.append("INSUFFICIENT_CONTEXT_HISTORY")
            else:
                context_stat = _aggregate_residual(key_history, statistic)
                weight = (
                    1.0
                    if shrinkage == 0
                    else len(key_history) / (len(key_history) + shrinkage)
                )
                correction = weight * context_stat + (1.0 - weight) * global_stat
                contextual = max(base + correction, 0.0)
                applied = True
                reasons.append("CONTEXT_RESIDUAL_CORRECTION_APPLIED")

        baseline_forecast.append(baseline)
        context_forecast.append(contextual)
        context_applied.append(applied)

        # Current-row truth is queued only after prediction. It can influence a
        # later row only when its reconciliation timestamp is visible by that row.
        if not reconciled:
            reasons.append("OUTCOME_NOT_RECONCILED_NOT_LEARNED")
        elif base is None or actual is None:
            reasons.append("INVALID_RECONCILED_OUTCOME_NOT_LEARNED")
        else:
            assert reconciled_at is not None  # validated above
            pending_residuals.append(
                (reconciled_at, actual - base, key, signal_usable)
            )
            reasons.append("OUTCOME_RECONCILED_PENDING_AVAILABILITY")

        reason_codes.append(reasons)

    return {
        "baseline_forecast": baseline_forecast,
        "context_forecast": context_forecast,
        "context_applied": context_applied,
        "history_n": history_n,
        "context_history_n": context_history_n,
        "reason_codes": reason_codes,
        "min_history": min_history,
        "min_context_history": min_context_history,
        "shrinkage_strength": shrinkage,
        "residual_statistic": statistic,
        "leakage_policy": "PAST_RECONCILED_ROWS_VISIBLE_BY_CUTOFF_ONLY",
        "reconciliation_policy": "EXPLICIT_CALLER_ACCEPTED_OUTCOME_REQUIRED",
        "reconciliation_time_policy": (
            "OUTCOME_MUST_BE_RECONCILED_AND_AVAILABLE_BY_CURRENT_DECISION_CUTOFF"
        ),
        "availability_policy": "SIGNAL_MUST_BE_PUBLISHED_BY_DECISION_CUTOFF",
        "result_scope": "OFFLINE_CONTEXT_CORRECTION_ONLY",
        "claim_boundary": (
            "Context correction does not establish pilot readiness or achieved impact."
        ),
    }


def _forecast_metrics(
    actual: Sequence[float],
    forecast: Sequence[float],
    *,
    excess_cost: float,
    shortage_cost: float,
) -> dict[str, float | int | None]:
    if not actual:
        return {"n": 0, "mae": None, "mean_loss": None}
    absolute_errors = [
        abs(predicted - observed)
        for observed, predicted in zip(actual, forecast)
    ]
    losses = [
        excess_cost * max(predicted - observed, 0.0)
        + shortage_cost * max(observed - predicted, 0.0)
        for observed, predicted in zip(actual, forecast)
    ]
    return {
        "n": len(actual),
        "mae": sum(absolute_errors) / len(absolute_errors),
        "mean_loss": sum(losses) / len(losses),
    }


def compare_context_signal_forecasts(
    *,
    actual_demand: Sequence[float | int | None],
    baseline_forecast: Sequence[float | int | None],
    context_forecast: Sequence[float | int | None],
    context_applied: Sequence[bool],
    excess_cost: float,
    shortage_cost: float,
) -> dict[str, object]:
    """Compare baseline vs context correction on identical eligible support."""

    lengths = {
        len(actual_demand),
        len(baseline_forecast),
        len(context_forecast),
        len(context_applied),
    }
    if len(lengths) != 1:
        raise ValueError("context-ablation inputs must have the same length")

    excess = _non_negative_number(excess_cost)
    shortage = _non_negative_number(shortage_cost)
    if excess is None or shortage is None:
        raise ValueError("decision-loss costs must be finite and non-negative")

    evaluation_indices: list[int] = []
    actual_common: list[float] = []
    baseline_common: list[float] = []
    context_common: list[float] = []

    for index, applied in enumerate(context_applied):
        if not isinstance(applied, bool) or not applied:
            continue
        actual = _non_negative_number(actual_demand[index])
        baseline = _non_negative_number(baseline_forecast[index])
        contextual = _non_negative_number(context_forecast[index])
        if actual is None or baseline is None or contextual is None:
            continue
        evaluation_indices.append(index)
        actual_common.append(actual)
        baseline_common.append(baseline)
        context_common.append(contextual)

    return {
        "metrics": {
            "baseline": _forecast_metrics(
                actual_common,
                baseline_common,
                excess_cost=excess,
                shortage_cost=shortage,
            ),
            "context_signal": _forecast_metrics(
                actual_common,
                context_common,
                excess_cost=excess,
                shortage_cost=shortage,
            ),
        },
        "common_support_n": len(evaluation_indices),
        "evaluation_indices": evaluation_indices,
        "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
        "result_scope": "OFFLINE_CONTEXT_ABLATION_ONLY",
        "claim_boundary": (
            "Offline signal ablation does not establish operational impact."
        ),
    }
