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
    """Return comparable offline metrics and a deterministic MAE ranking."""

    metrics = {
        name: evaluate_predictions(actual, predicted)
        for name, predicted in forecasts.items()
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
    return {
        "metrics": metrics,
        "ranking_by_mae": ranking,
        "best_by_mae": ranking[0] if ranking else None,
        "result_scope": "OFFLINE_BENCHMARK_ONLY",
    }
