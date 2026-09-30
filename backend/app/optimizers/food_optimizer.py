from __future__ import annotations

from typing import Mapping


class FoodOptimizer:
    """Transparent operator-reviewed planning policy for food production.

    This policy intentionally does not estimate achieved waste or cost savings.
    Its planning band is a policy heuristic for a pilot workflow, not a
    statistically calibrated confidence interval.
    """

    def optimize(
        self,
        date,
        cafeteria_id,
        predicted_demand,
        menu,
        signal_availability: Mapping[str, bool] | None = None,
    ):
        del date, cafeteria_id, menu  # Reserved for later evidence-backed policy inputs.

        demand = max(0, int(round(predicted_demand)))
        planning_lower = max(0, int(round(demand * 0.95)))
        heuristic_target = max(0, int(round(demand * 1.05)))
        planning_upper = max(0, int(round(demand * 1.10)))

        availability = dict(signal_availability or {})
        schedule_available = bool(availability.get("schedule"))
        menu_available = bool(availability.get("menu"))

        reason_codes = ["HEURISTIC_BAND_NOT_CALIBRATED"]
        if not schedule_available:
            decision_readiness = "WITHHOLD"
            recommended = None
            reason_codes.insert(0, "MISSING_SCHEDULE_BACKBONE")
        elif not menu_available:
            decision_readiness = "REVIEW_REQUIRED"
            recommended = heuristic_target
            reason_codes.insert(0, "MISSING_MENU_CONTEXT")
        else:
            decision_readiness = "PILOT_READY"
            recommended = heuristic_target

        return {
            "planning_lower": planning_lower,
            "recommended": recommended,
            "planning_upper": planning_upper,
            "decision_readiness": decision_readiness,
            "policy_provenance": "POLICY_HEURISTIC",
            "operator_approval_required": True,
            "automatic_kitchen_dispatch": False,
            "reason_codes": reason_codes,
        }
