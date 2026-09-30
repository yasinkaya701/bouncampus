from __future__ import annotations

import math
from typing import Mapping, Sequence


def _to_optional_float(value):
    if value is None:
        return None
    numeric = float(value)
    if not math.isfinite(numeric):
        return None
    return numeric


def evaluate_predictions(
    actual: Sequence[float | int | None],
    predicted: Sequence[float | int | None],
) -> dict[str, float | int | None]:
    """Evaluate aligned forecasts while ignoring explicit missing pairs."""

    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")

    pairs: list[tuple[float, float]] = []
    for actual_value, predicted_value in zip(actual, predicted):
        actual_number = _to_optional_float(actual_value)
        predicted_number = _to_optional_float(predicted_value)
        if actual_number is None or predicted_number is None:
            continue
        pairs.append((actual_number, predicted_number))

    if not pairs:
        return {
            "n": 0,
            "mae": None,
            "rmse": None,
            "wape_pct": None,
            "mean_error": None,
            "mean_error_pct": None,
        }

    errors = [predicted_value - actual_value for actual_value, predicted_value in pairs]
    abs_errors = [abs(error) for error in errors]
    squared_errors = [error * error for error in errors]
    actual_sum = sum(abs(actual_value) for actual_value, _ in pairs)
    actual_mean = sum(actual_value for actual_value, _ in pairs) / len(pairs)
    mean_error = sum(errors) / len(errors)

    return {
        "n": len(pairs),
        "mae": sum(abs_errors) / len(abs_errors),
        "rmse": math.sqrt(sum(squared_errors) / len(squared_errors)),
        "wape_pct": None if actual_sum == 0 else (sum(abs_errors) / actual_sum) * 100,
        "mean_error": mean_error,
        "mean_error_pct": None if actual_mean == 0 else (mean_error / actual_mean) * 100,
    }


def generate_naive_baselines(
    actual: Sequence[float | int],
    *,
    rolling_window: int = 3,
    seasonal_lag: int = 7,
) -> dict[str, list[float | None]]:
    """Generate past-only baselines so future observations never leak into forecasts."""

    if rolling_window < 1:
        raise ValueError("rolling_window must be >= 1")
    if seasonal_lag < 1:
        raise ValueError("seasonal_lag must be >= 1")

    values = [float(value) for value in actual]
    previous_service: list[float | None] = []
    expanding_mean: list[float | None] = []
    rolling_mean: list[float | None] = []
    seasonal: list[float | None] = []

    for index in range(len(values)):
        history = values[:index]
        previous_service.append(history[-1] if history else None)
        expanding_mean.append(sum(history) / len(history) if history else None)
        recent = history[-rolling_window:]
        rolling_mean.append(sum(recent) / len(recent) if recent else None)
        seasonal.append(values[index - seasonal_lag] if index >= seasonal_lag else None)

    return {
        "previous_service": previous_service,
        "expanding_mean": expanding_mean,
        f"rolling_mean_{rolling_window}": rolling_mean,
        f"seasonal_lag_{seasonal_lag}": seasonal,
    }


def compare_forecasts(
    actual: Sequence[float | int | None],
    forecasts: Mapping[str, Sequence[float | int | None]],
) -> dict[str, object]:
    """Compare every candidate on one identical finite evaluation support.

    Ranking methods on different subsets is invalid because a sparse method could
    omit difficult services and appear artificially strong. This function therefore
    intersects the available rows across the target and every candidate before any
    metric or ranking is computed.
    """

    actual_values = list(actual)
    for name, predicted in forecasts.items():
        if len(predicted) != len(actual_values):
            raise ValueError(
                f"actual and predicted must have the same length for forecast {name!r}"
            )

    if not forecasts:
        return {
            "metrics": {},
            "ranking_by_mae": [],
            "best_by_mae": None,
            "common_support_n": 0,
            "common_support_pct": 0.0,
            "evaluation_indices": [],
            "available_n_by_method": {},
            "result_scope": "OFFLINE_BENCHMARK_ONLY",
        }

    normalized_actual = [_to_optional_float(value) for value in actual_values]
    normalized_forecasts = {
        name: [_to_optional_float(value) for value in predicted]
        for name, predicted in forecasts.items()
    }

    valid_actual_indices = [
        index for index, value in enumerate(normalized_actual) if value is not None
    ]
    evaluation_indices = [
        index
        for index in valid_actual_indices
        if all(values[index] is not None for values in normalized_forecasts.values())
    ]

    actual_common = [normalized_actual[index] for index in evaluation_indices]
    metrics = {
        name: evaluate_predictions(
            actual_common,
            [values[index] for index in evaluation_indices],
        )
        for name, values in normalized_forecasts.items()
    }
    available_n_by_method = {
        name: sum(
            1
            for index in valid_actual_indices
            if values[index] is not None
        )
        for name, values in normalized_forecasts.items()
    }

    eligible = [
        (name, result)
        for name, result in metrics.items()
        if result["mae"] is not None
    ]
    ranking = [
        name
        for name, _ in sorted(
            eligible,
            key=lambda item: (
                float(item[1]["mae"]),
                float(item[1]["rmse"]) if item[1]["rmse"] is not None else math.inf,
                item[0],
            ),
        )
    ]
    valid_actual_n = len(valid_actual_indices)
    common_support_n = len(evaluation_indices)
    common_support_pct = (
        0.0
        if valid_actual_n == 0
        else round((common_support_n / valid_actual_n) * 100, 6)
    )

    return {
        "metrics": metrics,
        "ranking_by_mae": ranking,
        "best_by_mae": ranking[0] if ranking else None,
        "common_support_n": common_support_n,
        "common_support_pct": common_support_pct,
        "evaluation_indices": evaluation_indices,
        "available_n_by_method": available_n_by_method,
        "result_scope": "OFFLINE_BENCHMARK_ONLY",
    }
