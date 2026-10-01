from datetime import date, timedelta, datetime
from typing import List, Optional
import json
import os
import uuid

from fastapi import APIRouter

from app.config import settings
from app.models.energy import EnergyModel
from app.models.food_demand import FoodDemandPredictor
from app.models.occupancy import OccupancyPredictor
from app.optimizers.action_engine import ActionEngine
from app.optimizers.energy_potential import estimate_energy_potential
from app.optimizers.food_optimizer import FoodOptimizer
from app.schemas import (
    ActionItem,
    Building,
    DashboardData,
    ImpactMetrics,
    LiveMenuInfo,
    LiveWeatherInfo,
    LiveWindTurbineInfo,
    RealCampusEvent,
)
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
o_pred = OccupancyPredictor()
e_model = EnergyModel()
f_pred = FoodDemandPredictor()
f_opt = FoodOptimizer()
action_engine = ActionEngine()
real_service = RealDataService()


def get_buildings_data():
    with open(os.path.join(settings.DATA_DIR, "campus_config.json"), "r", encoding="utf-8") as handle:
        return json.load(handle)["buildings"]


def _source_is_live(source: str, marker: str) -> bool:
    lowered = source.lower()
    return marker in lowered and "fallback" not in lowered and "klasik" not in lowered


@router.get("/buildings", response_model=List[Building])
def get_buildings():
    return [Building(**item) for item in get_buildings_data()]


@router.get("/dashboard", response_model=DashboardData)
def get_dashboard(date_val: Optional[str] = None):
    target_date = date_val or (date.today() + timedelta(days=1)).isoformat()
    dt = datetime.fromisoformat(target_date)
    weekday = dt.weekday()

    # Source-tagged weather/menu context. Fallback data remain usable for display but
    # do not count as healthy live decision signals.
    live_weather = real_service.fetch_live_weather()
    weather_info = LiveWeatherInfo(
        source=live_weather["source"],
        temperature=live_weather["temperature"],
        humidity=live_weather["humidity"],
        rain=live_weather["rain"],
        wind_speed=live_weather["wind_speed"],
    )

    live_menu_data = real_service.fetch_live_cafeteria_menu()
    menu_info = LiveMenuInfo(
        source=live_menu_data["source"],
        date=live_menu_data["date"],
        soup=live_menu_data["soup"],
        main_dish=live_menu_data["main_dish"],
        calories=live_menu_data["calories"],
        vegan_dish=live_menu_data["vegan_dish"],
        sides=live_menu_data["sides"],
        options=live_menu_data["options"],
        popularity_multiplier=live_menu_data["popularity_multiplier"],
    )

    # Schedule-derived occupancy is an estimate, not access-control telemetry.
    real_campus_occ = real_service.get_hourly_campus_occupancy(weekday)
    current_hour = datetime.now().hour
    eval_hour = current_hour if 8 <= current_hour <= 21 else 12

    building_data = get_buildings_data()
    total_occ = 0
    buildings_res = []
    for building in building_data:
        building_id = building["id"]
        real_occ_hourly = real_campus_occ.get(building_id, {})
        hour_occ = real_occ_hourly.get(eval_hour, 0)
        capacity = max(1, building["total_capacity"])
        occupancy_ratio = min(1.0, round(hour_occ / capacity, 3))
        total_occ += hour_occ

        building_result = Building(**building)
        building_result.occupancy_ratio = occupancy_ratio
        buildings_res.append(building_result)

    # Keep forecasting separate from the decision policy. The model produces a point
    # estimate; the policy decides whether it is actionable and exposes abstention.
    food_point_forecasts = []
    for cafeteria_id in ("B-SOUTH-GY", "B-NORTH-KY"):
        point_forecast, _legacy_compat = f_pred.predict(
            target_date,
            cafeteria_id,
            meal_type="lunch",
        )
        food_point_forecasts.append(point_forecast)
    food_demand_meals = sum(food_point_forecasts)

    food_signal_availability = {
        "schedule": bool(getattr(real_service, "_courses_cache", None)),
        "weather": _source_is_live(str(live_weather.get("source", "")), "open-meteo live api"),
        "menu": _source_is_live(str(live_menu_data.get("source", "")), "resmi canlı"),
        "calendar": False,
    }
    food_decision = f_opt.optimize(
        target_date,
        "ALL_DINING_HALLS",
        food_demand_meals,
        [],
        signal_availability=food_signal_availability,
    )

    # Energy outputs are scenario estimates from explicit registered assumptions.
    # The shared calculator prevents dashboard and impact endpoints from drifting to
    # unrelated hard-coded numbers.
    energy_potential = estimate_energy_potential(live_weather["temperature"])
    predicted_energy_mwh = energy_potential["predicted_energy_mwh"]
    kwh_saved = energy_potential["kwh_saved"]
    co2_avoided_kg = energy_potential["co2_avoided_kg"]
    potential_saving_tl = energy_potential["cost_saved_tl"]

    if food_decision["abstained"]:
        food_action = ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="food",
            title="Hold lunch production recommendation",
            time="10:30 - 14:00",
            location="Kuzey + Güney Yemekhaneleri",
            description=(
                f"Food-demand model point estimate is {food_demand_meals} meals, but decision state is "
                f"{food_decision['decision_readiness']} with {food_decision['signal_coverage_pct']}% configured "
                "signal coverage. No production target is issued; operator review and missing-context resolution "
                "are required. No food-waste saving is claimed."
            ),
            impact_value=float(food_decision["signal_coverage_pct"]),
            impact_unit="% decision signal coverage",
            provenance="POLICY_HEURISTIC",
        )
    else:
        food_action = ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="food",
            title=f"Review lunch production plan: {menu_info.main_dish}",
            time="10:30 - 14:00",
            location="Kuzey + Güney Yemekhaneleri",
            description=(
                f"MODEL_ESTIMATE demand is {food_demand_meals} meals. The POLICY_HEURISTIC planning range is "
                f"{food_decision['planning_lower']}–{food_decision['planning_upper']} with state "
                f"{food_decision['decision_readiness']}. Human approval is required and automatic kitchen dispatch "
                "is disabled. This is not measured waste reduction."
            ),
            impact_value=float(food_decision["recommended_production"] or 0),
            impact_unit="MODEL_ESTIMATE meals",
            provenance="MODEL_ESTIMATE",
        )

    # Keep dashboard actions evidence-gated. Non-food recommendations must come
    # from a domain policy with explicit readiness/provenance instead of static
    # pseudo-operational numbers embedded in the route.
    non_food_actions = action_engine.generate_actions(
        target_date,
        energy_recs=[],
        food_recs=[],
    )
    actions = [food_action, *non_food_actions]

    wind_data = real_service.fetch_kilyos_wind_generation()
    wind_info = LiveWindTurbineInfo(**wind_data)

    raw_events = real_service.get_real_campus_events(target_date)
    events_info = [RealCampusEvent(**event) for event in raw_events]

    return DashboardData(
        date=target_date,
        campus_occupancy=total_occ,
        predicted_energy_mwh=predicted_energy_mwh,
        food_demand_meals=food_demand_meals,
        potential_saving_tl=potential_saving_tl,
        co2_avoided_kg=co2_avoided_kg,
        buildings=buildings_res,
        actions=actions,
        live_weather=weather_info,
        live_menu=menu_info,
        live_wind=wind_info,
        today_events=events_info,
        real_courses_loaded=len(real_service._courses_cache),
    )


@router.get("/metrics/impact", response_model=ImpactMetrics)
def get_impact_metrics(date_val: Optional[str] = None):
    del date_val
    live_weather = real_service.fetch_live_weather()
    energy_potential = estimate_energy_potential(live_weather["temperature"])
    return ImpactMetrics(
        kwh_saved=energy_potential["kwh_saved"],
        co2_avoided_kg=energy_potential["co2_avoided_kg"],
        food_waste_avoided_kg=None,
        cost_saved_tl=energy_potential["cost_saved_tl"],
        energy_provenance="MODEL_ESTIMATE",
        food_waste_impact_status="UNMEASURED",
        note=(
            "Energy values are scenario potential from configured assumptions and current weather context; "
            "they are not measured savings. Food-waste impact remains UNMEASURED until a valid matched pilot "
            "is completed."
        ),
    )
