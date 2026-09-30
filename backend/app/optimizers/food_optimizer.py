from __future__ import annotations

from typing import Mapping

from app.decision.food_policy import build_food_decision


class FoodOptimizer:
    """Compatibility adapter over the versioned CS1 food decision policy."""

    def optimize(
        self,
        date,
        cafeteria_id,
        predicted_demand,
        menu,
        signal_availability: Mapping[str, bool] | None = None,
        *,
        method_eligibility: str = "SANDBOX_ONLY",
    ):
        del date, cafeteria_id, menu
        result = build_food_decision(
            predicted_demand,
            signal_availability,
            model_id="food-demand-xgboost",
            method_eligibility=method_eligibility,
        )

        # Preserve the old adapter keys for internal callers while the API contract
        # uses the explicit versioned names from build_food_decision.
        result["recommended"] = result["recommended_production"]
        result["policy_provenance"] = result["decision_provenance"]
        return result
