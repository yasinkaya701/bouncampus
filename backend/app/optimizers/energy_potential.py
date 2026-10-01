from __future__ import annotations

import math
from typing import Any


def _finite_non_negative(value: Any, *, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite non-negative number")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite non-negative number") from exc
    if not math.isfinite(numeric) or numeric < 0:
        raise ValueError(f"{name} must be a finite non-negative number")
    return numeric


def estimate_energy_potential(
    temperature: Any,
    *,
    base_energy_mwh: Any = 11.2,
    optimization_fraction: Any = 0.14,
    cost_tl_per_kwh: Any = 2.8,
    co2_kg_per_kwh: Any = 0.47,
) -> dict[str, float | str | dict[str, float]]:
    """Return a transparent scenario estimate, never measured savings.

    The defaults preserve the existing dashboard assumptions while centralizing
    them in one validated calculation. Callers may override assumptions only
    explicitly, so API surfaces cannot drift to unrelated hard-coded numbers.
    """

    temp = _finite_non_negative(temperature, name="temperature")
    base_mwh = _finite_non_negative(base_energy_mwh, name="base_energy_mwh")
    optimization = _finite_non_negative(
        optimization_fraction,
        name="optimization_fraction",
    )
    if optimization > 1:
        raise ValueError("optimization_fraction must be between 0 and 1")
    cost_rate = _finite_non_negative(cost_tl_per_kwh, name="cost_tl_per_kwh")
    co2_rate = _finite_non_negative(co2_kg_per_kwh, name="co2_kg_per_kwh")

    hvac_factor = 1.0 + max(0.0, abs(temp - 22.0) * 0.04)
    predicted_energy_mwh = round(base_mwh * hvac_factor, 1)
    kwh_saved = max(0.0, round(predicted_energy_mwh * optimization * 1000.0, 0))
    cost_saved_tl = round(kwh_saved * cost_rate, 1)
    co2_avoided_kg = round(kwh_saved * co2_rate, 1)

    return {
        "predicted_energy_mwh": predicted_energy_mwh,
        "kwh_saved": kwh_saved,
        "cost_saved_tl": cost_saved_tl,
        "co2_avoided_kg": co2_avoided_kg,
        "provenance": "MODEL_ESTIMATE",
        "claim_scope": "SCENARIO_POTENTIAL_NOT_MEASURED_SAVINGS",
        "assumptions": {
            "base_energy_mwh": base_mwh,
            "optimization_fraction": optimization,
            "cost_tl_per_kwh": cost_rate,
            "co2_kg_per_kwh": co2_rate,
        },
    }
