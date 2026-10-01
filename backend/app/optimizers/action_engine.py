from __future__ import annotations

import math
import uuid
from typing import Any, Iterable, Mapping

from app.schemas import ActionItem


class ActionEngine:
    """Adapt evidence-bearing decision candidates into operator action items.

    The engine is intentionally fail-closed: it never invents an operational
    action when upstream decision evidence is absent or not reviewable.
    """

    _ALLOWED_PROVENANCE = {
        "MODEL_ESTIMATE",
        "POLICY_HEURISTIC",
        "OFFICIAL_LIVE",
        "OFFICIAL_SNAPSHOT",
    }
    _REVIEWABLE_READINESS = {
        "PILOT_READY",
        "READY_FOR_REVIEW",
        "REVIEW_REQUIRED",
    }
    _REQUIRED_TEXT_FIELDS = (
        "priority",
        "title",
        "time",
        "location",
        "description",
        "impact_unit",
    )

    def generate_actions(self, date, energy_recs, food_recs):
        actions: list[ActionItem] = []
        actions.extend(self._adapt_candidates(energy_recs, action_type="energy"))
        actions.extend(self._adapt_candidates(food_recs, action_type="food"))
        return actions

    def _adapt_candidates(
        self,
        candidates: Iterable[Mapping[str, Any]] | None,
        *,
        action_type: str,
    ) -> list[ActionItem]:
        if not candidates:
            return []

        adapted: list[ActionItem] = []
        for candidate in candidates:
            if not isinstance(candidate, Mapping):
                continue
            if candidate.get("decision_readiness") not in self._REVIEWABLE_READINESS:
                continue
            if candidate.get("operator_approval_required") is not True:
                continue
            if candidate.get("auto_dispatch_allowed") is not False:
                continue

            provenance = candidate.get("provenance")
            if provenance not in self._ALLOWED_PROVENANCE:
                continue

            if any(
                not isinstance(candidate.get(field), str)
                or not candidate[field].strip()
                for field in self._REQUIRED_TEXT_FIELDS
            ):
                continue

            impact_value = candidate.get("impact_value")
            if isinstance(impact_value, bool):
                continue
            try:
                numeric_impact = float(impact_value)
            except (TypeError, ValueError):
                continue
            if not math.isfinite(numeric_impact):
                continue

            adapted.append(
                ActionItem(
                    id=str(uuid.uuid4()),
                    priority=candidate["priority"].strip(),
                    type=action_type,
                    title=candidate["title"].strip(),
                    time=candidate["time"].strip(),
                    location=candidate["location"].strip(),
                    description=candidate["description"].strip(),
                    impact_value=numeric_impact,
                    impact_unit=candidate["impact_unit"].strip(),
                    provenance=provenance,
                )
            )

        return adapted
