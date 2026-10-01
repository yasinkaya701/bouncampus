"""Reservation-first demand baselines and decision-loss evaluation for CS1.

This module treats reservation counts as intent signals, never as served demand.
All corrected forecasts are learned from prior reconciled services only.
"""

from __future__ import annotations

import math
from typing import Mapping, Sequence


def _to_optional_non_negative_float(value):
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric < 0:
        return None
    return numeric


def generate_reservation_baselines(
    active_reservations_at_cutoff: Sequence[float | int | None],
    reserved_served_demand: Sequence[float | int | None],
    unreserved_demand: Sequence[float | int | None],
    *,
    min_history: int = 2,
) -> dict[str, object]:
    """Build raw and corrected reservation baselines from past reconciled services.

    The transparent correction is::

        current_reservations * historical_show_rate
        + historical_mean_unreserved_demand

    A historical row is learnable only when all three counts are finite and
    non-negative and reserved-served demand does not exceed active reservations.
    Current-service outcomes are appended only after its forecast is produced,
    preventing target leakage. Excluded rows and baseline WITHHOLD states are
    returned with explicit reason codes rather than being silently discarded.
    """

    if min_history < 1:
        raise ValueError("min_history must be >= 1")
    lengths = {
        len(active_reservations_at_cutoff),
        len(reserved_served_demand),
        len(unreserved_demand),
    }
    if len(lengths) != 1:
        raise ValueError("reservation reconciliation inputs must have the same length")

    reservations = [
        _to_optional_non_negative_float(value)
        for value in active_reservations_at_cutoff
    ]
    reserved_served = [
        _to_optional_non_negative_float(value)
        for value in reserved_served_demand
    ]
    unreserved = [
        _to_optional_non_negative_float(value)
        for value in unreserved_demand
    ]

    corrected: list[float | None] = []
    history_n: list[int] = []
    baseline_readiness: list[str] = []
    baseline_reason_codes: list[list[str]] = []
    reconciliation_status: list[str] = []
    reconciliation_reason_codes: list[list[str]] = []
    reconciled_history: list[tuple[float, float, float]] = []

    for index, current_reservations in enumerate(reservations):
        history_n.append(len(reconciled_history))
        readiness_reasons: list[str] = []
        if current_reservations is None:
            corrected.append(None)
            baseline_readiness.append("WITHHOLD")
            readiness_reasons.append("MISSING_OR_INVALID_CURRENT_RESERVATIONS")
        elif len(reconciled_history) < min_history:
            corrected.append(None)
            baseline_readiness.append("WITHHOLD")
            readiness_reasons.append("INSUFFICIENT_RECONCILED_HISTORY")
        else:
            historical_reservations = sum(row[0] for row in reconciled_history)
            if historical_reservations <= 0:
                corrected.append(None)
                baseline_readiness.append("WITHHOLD")
                readiness_reasons.append("ZERO_RESERVATION_HISTORY")
            else:
                historical_reserved_served = sum(row[1] for row in reconciled_history)
                show_rate = historical_reserved_served / historical_reservations
                expected_unreserved = sum(row[2] for row in reconciled_history) / len(
                    reconciled_history
                )
                corrected.append(current_reservations * show_rate + expected_unreserved)
                baseline_readiness.append("BENCHMARK_READY")
                readiness_reasons.append("CORRECTED_RESERVATION_BASELINE_AVAILABLE")
        baseline_reason_codes.append(readiness_reasons)

        reservation = reservations[index]
        served_from_reservation = reserved_served[index]
        served_without_reservation = unreserved[index]
        reconciliation_reasons: list[str] = []
        if reservation is None:
            reconciliation_reasons.append("MISSING_OR_INVALID_ACTIVE_RESERVATIONS")
        if served_from_reservation is None:
            reconciliation_reasons.append("MISSING_OR_INVALID_RESERVED_SERVED_DEMAND")
        if served_without_reservation is None:
            reconciliation_reasons.append("MISSING_OR_INVALID_UNRESERVED_DEMAND")
        if (
            reservation is not None
            and served_from_reservation is not None
            and served_from_reservation > reservation
        ):
            reconciliation_reasons.append(
                "RESERVED_SERVED_EXCEEDS_ACTIVE_RESERVATIONS"
            )

        if reconciliation_reasons:
            reconciliation_status.append("EXCLUDED")
        else:
            reconciliation_status.append("RECONCILED")
            reconciled_history.append(
                (reservation, served_from_reservation, served_without_reservation)
            )
        reconciliation_reason_codes.append(reconciliation_reasons)

    reconciled_row_count = reconciliation_status.count("RECONCILED")
    excluded_row_count = len(reconciliation_status) - reconciled_row_count

    return {
        "raw_reservation": list(reservations),
        "corrected_reservation": corrected,
        "history_n": history_n,
        "baseline_readiness": baseline_readiness,
        "baseline_reason_codes": baseline_reason_codes,
        "reconciliation_status": reconciliation_status,
        "reconciliation_reason_codes": reconciliation_reason_codes,
        "reconciled_row_count": reconciled_row_count,
        "excluded_row_count": excluded_row_count,
        "semantics": "RESERVATION_IS_INTENT_NOT_SERVED_DEMAND",
        "result_scope": "OFFLINE_BASELINE_ONLY",
        "leakage_policy": "PAST_RECONCILED_SERVICES_ONLY",
    }


def evaluate_decision_loss(
    actual_demand: Sequence[float | int | None],
    recommended_quantity: Sequence[float | int | None],
    *,
    excess_cost: float = 1.0,
    shortage_cost: float = 1.0,
) -> dict[str, float | int | str | None]:
    """Evaluate surplus/shortage loss in relative sensitivity units, not currency."""

    excess_cost_number = _to_optional_non_negative_float(excess_cost)
    shortage_cost_number = _to_optional_non_negative_float(shortage_cost)
    if excess_cost_number is None or shortage_cost_number is None:
        raise ValueError("decision-loss costs must be finite and non-negative")
    if len(actual_demand) != len(recommended_quantity):
        raise ValueError("actual demand and recommended quantity must have the same length")

    pairs: list[tuple[float, float]] = []
    for actual_value, recommended_value in zip(actual_demand, recommended_quantity):
        actual_number = _to_optional_non_negative_float(actual_value)
        recommended_number = _to_optional_non_negative_float(recommended_value)
        if actual_number is None or recommended_number is None:
            continue
        pairs.append((actual_number, recommended_number))

    if not pairs:
        return {
            "n": 0,
            "surplus_units": 0.0,
            "shortage_units": 0.0,
            "total_loss": None,
            "mean_loss": None,
            "loss_unit": "RELATIVE_COST_UNITS",
            "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
        }

    surplus_units = sum(max(recommended - actual, 0.0) for actual, recommended in pairs)
    shortage_units = sum(max(actual - recommended, 0.0) for actual, recommended in pairs)
    total_loss = excess_cost_number * surplus_units + shortage_cost_number * shortage_units

    return {
        "n": len(pairs),
        "surplus_units": surplus_units,
        "shortage_units": shortage_units,
        "total_loss": total_loss,
        "mean_loss": total_loss / len(pairs),
        "loss_unit": "RELATIVE_COST_UNITS",
        "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
    }


def compare_decision_policies(
    actual_demand: Sequence[float | int | None],
    policies: Mapping[str, Sequence[float | int | None]],
    *,
    excess_cost: float = 1.0,
    shortage_cost: float = 1.0,
) -> dict[str, object]:
    """Rank policies by asymmetric decision loss on identical finite support."""

    actual_values = list(actual_demand)
    for name, recommended in policies.items():
        if len(recommended) != len(actual_values):
            raise ValueError(
                f"actual demand and recommended quantity must have the same length for policy {name!r}"
            )

    if not policies:
        return {
            "metrics": {},
            "ranking_by_mean_loss": [],
            "best_by_mean_loss": None,
            "common_support_n": 0,
            "evaluation_indices": [],
            "result_scope": "OFFLINE_DECISION_BENCHMARK_ONLY",
            "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
        }

    normalized_actual = [
        _to_optional_non_negative_float(value) for value in actual_values
    ]
    normalized_policies = {
        name: [_to_optional_non_negative_float(value) for value in recommended]
        for name, recommended in policies.items()
    }
    evaluation_indices = [
        index
        for index, actual_value in enumerate(normalized_actual)
        if actual_value is not None
        and all(values[index] is not None for values in normalized_policies.values())
    ]

    actual_common = [normalized_actual[index] for index in evaluation_indices]
    metrics = {
        name: evaluate_decision_loss(
            actual_common,
            [values[index] for index in evaluation_indices],
            excess_cost=excess_cost,
            shortage_cost=shortage_cost,
        )
        for name, values in normalized_policies.items()
    }
    ranking = [
        name
        for name, result in sorted(
            metrics.items(),
            key=lambda item: (
                math.inf if item[1]["mean_loss"] is None else float(item[1]["mean_loss"]),
                item[0],
            ),
        )
        if result["mean_loss"] is not None
    ]

    return {
        "metrics": metrics,
        "ranking_by_mean_loss": ranking,
        "best_by_mean_loss": ranking[0] if ranking else None,
        "common_support_n": len(evaluation_indices),
        "evaluation_indices": evaluation_indices,
        "result_scope": "OFFLINE_DECISION_BENCHMARK_ONLY",
        "cost_provenance": "SENSITIVITY_PARAMETER_NOT_OBSERVED_ECONOMICS",
    }
