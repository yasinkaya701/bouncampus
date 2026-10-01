from datetime import date, timedelta
from typing import List, Optional
import uuid

from fastapi import APIRouter

from app.models.food_demand import FoodDemandPredictor
from app.optimizers.food_optimizer import FoodOptimizer
from app.schemas import ActionItem
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
real_service = RealDataService()
food_predictor = FoodDemandPredictor()
food_optimizer = FoodOptimizer()


def _source_is_live(source: str, marker: str) -> bool:
    lowered = source.lower()
    return marker in lowered and "fallback" not in lowered and "klasik" not in lowered


@router.get("/actions", response_model=List[ActionItem])
def get_actions(date_val: Optional[str] = None):
    target_date = date_val or (date.today() + timedelta(days=1)).isoformat()
    menu = real_service.fetch_live_cafeteria_menu()
    weather = real_service.fetch_live_weather()
    temp = weather["temperature"]

    predicted_meals, _legacy_compat = food_predictor.predict(
        target_date,
        "B-NORTH-KY",
        meal_type="lunch",
    )
    signal_availability = {
        "schedule": bool(getattr(real_service, "_courses_cache", None)),
        "weather": _source_is_live(str(weather.get("source", "")), "open-meteo live api"),
        "menu": _source_is_live(str(menu.get("source", "")), "resmi canlı"),
        "calendar": False,
    }
    decision = food_optimizer.optimize(
        target_date,
        "B-NORTH-KY",
        predicted_meals,
        [],
        signal_availability=signal_availability,
    )

    if decision["abstained"]:
        food_action = ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="food",
            title=f"Hold Kuzey lunch recommendation: {menu['main_dish']}",
            time="11:00 - 14:00",
            location="Kuzey Yemekhanesi & Piramit",
            description=(
                f"MODEL_ESTIMATE demand is {predicted_meals} meals, but the decision policy returned "
                f"{decision['decision_readiness']} at {decision['signal_coverage_pct']}% configured signal coverage. "
                "No production target is issued. Resolve missing context and obtain operator review; no waste saving "
                "or operational outcome is claimed."
            ),
            impact_value=float(decision["signal_coverage_pct"]),
            impact_unit="% decision signal coverage",
            provenance="POLICY_HEURISTIC",
        )
    else:
        food_action = ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="food",
            title=f"Review Kuzey lunch plan: {menu['main_dish']}",
            time="11:00 - 14:00",
            location="Kuzey Yemekhanesi & Piramit",
            description=(
                f"MODEL_ESTIMATE demand is {predicted_meals} meals. The versioned POLICY_HEURISTIC planning range is "
                f"{decision['planning_lower']}–{decision['planning_upper']} and readiness is "
                f"{decision['decision_readiness']}. Human approval is mandatory; automatic kitchen dispatch is off. "
                "No achieved food-waste reduction is implied."
            ),
            impact_value=float(decision["recommended_production"] or 0),
            impact_unit="MODEL_ESTIMATE meals",
            provenance="MODEL_ESTIMATE",
        )

    return [
        food_action,
        ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="energy",
            title="Consolidate Kare Blok (KB) Evening Study Groups",
            time="18:00 - 22:00",
            location="Kare Blok",
            description=(
                f"Timetable-derived model context suggests low evening instructional load. Review consolidation before "
                f"changing HVAC state (outdoor temperature: {temp}°C)."
            ),
            impact_value=175.0,
            impact_unit="kWh model potential",
            provenance="MODEL_ESTIMATE",
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="MEDIUM",
            type="space",
            title="Review South Campus Lunch Overflow",
            time="12:15 - 13:15",
            location="Güney Yemekhanesi & Dodge Hall",
            description=(
                "Schedule/capacity context suggests potential lunch crowding. Treat the occupancy value as a model estimate "
                "and verify conditions before redirecting people."
            ),
            impact_value=75.0,
            impact_unit="MODEL_ESTIMATE students",
            provenance="MODEL_ESTIMATE",
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="MEDIUM",
            type="energy",
            title="New Hall (NH) Midday Lecture Hall Eco-Ventilation",
            time="12:00 - 13:00",
            location="Yeni Bina (NH)",
            description="Timetable-derived low-use estimate; field verification is required before changing ventilation.",
            impact_value=90.0,
            impact_unit="kWh model potential",
            provenance="MODEL_ESTIMATE",
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="LOW",
            type="energy",
            title="Aptullah Kuran Library Night HVAC Review",
            time="21:00 - 02:00",
            location="Aptullah Kuran Kütüphanesi",
            description="Review a timetable/occupancy-model based consolidation option; no automatic HVAC command is issued.",
            impact_value=45.0,
            impact_unit="kWh model potential",
            provenance="MODEL_ESTIMATE",
        ),
    ]
