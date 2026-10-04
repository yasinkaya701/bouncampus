import json
import os
from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter

from app.config import settings
from app.decision.menu_demand import apply_menu_adjustment, build_menu_demand_adjustment
from app.models.food_demand import FoodDemandPredictor
from app.optimizers.food_optimizer import FoodOptimizer
from app.schemas import FoodDemandForecast, MenuPopularity
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
f_pred = FoodDemandPredictor()
f_opt = FoodOptimizer()
real_service = RealDataService()


def _is_official_live_menu(menu: dict) -> bool:
    source = str(menu.get("source", "")).lower()
    return "resmi" in source and "canlı" in source and "fallback" not in source


def _is_live_weather(weather: dict) -> bool:
    source = str(weather.get("source", "")).lower()
    return "open-meteo live api" in source and "fallback" not in source


def _decision_signals(live_menu: dict, live_weather: dict) -> dict[str, bool]:
    course_cache = getattr(real_service, "_courses_cache", None)
    return {
        "schedule": bool(course_cache),
        "weather": _is_live_weather(live_weather),
        "menu": _is_official_live_menu(live_menu),
        # No verified academic-calendar source is wired into this Python route yet.
        "calendar": False,
    }


def _load_menu_popularity_catalog() -> list[dict]:
    path = os.path.join(settings.DATA_DIR, "menu_popularity.json")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []
    dishes = payload.get("dishes", []) if isinstance(payload, dict) else []
    return [dish for dish in dishes if isinstance(dish, dict)]


def _menu_items(live_menu: dict) -> List[MenuPopularity]:
    heuristic_popularity = live_menu.get("popularity_multiplier")
    return [
        MenuPopularity(
            name=str(live_menu.get("main_dish") or "Unavailable"),
            name_en="Main Dish",
            category="main",
            popularity_score=float(heuristic_popularity) if heuristic_popularity is not None else None,
            avg_rating=None,
            popularity_provenance="POLICY_HEURISTIC" if heuristic_popularity is not None else "UNAVAILABLE",
        ),
        MenuPopularity(
            name=str(live_menu.get("soup") or "Unavailable"),
            name_en="Daily Soup",
            category="soup",
            popularity_score=None,
            avg_rating=None,
            popularity_provenance="UNAVAILABLE",
        ),
        MenuPopularity(
            name=str(live_menu.get("vegan_dish") or "Unavailable"),
            name_en="Vegan Dish",
            category="vegan",
            popularity_score=None,
            avg_rating=None,
            popularity_provenance="UNAVAILABLE",
        ),
    ]


@router.get("/food", response_model=List[FoodDemandForecast])
def get_food_forecast(date_val: Optional[str] = None):
    target_date = date_val or (date.today() + timedelta(days=1)).isoformat()
    live_menu = real_service.fetch_live_cafeteria_menu()
    live_weather = real_service.fetch_live_weather()
    signal_availability = _decision_signals(live_menu, live_weather)
    menu_items = _menu_items(live_menu)
    menu_adjustment = build_menu_demand_adjustment(
        live_menu,
        _load_menu_popularity_catalog(),
        official_menu=signal_availability["menu"],
    )
    model_metadata = f_pred.metadata()
    method_eligibility = str(model_metadata.get("method_eligibility", "SANDBOX_ONLY"))

    forecasts: List[FoodDemandForecast] = []
    for cafeteria_id in ["B-SOUTH-GY", "B-NORTH-KY"]:
        for meal_type in ["lunch", "dinner"]:
            baseline_point_forecast, _legacy_compat = f_pred.predict(
                target_date,
                cafeteria_id,
                meal_type=meal_type,
            )
            menu_adjusted_forecast = apply_menu_adjustment(
                baseline_point_forecast,
                menu_adjustment["factor"],
            )
            decision = f_opt.optimize(
                target_date,
                cafeteria_id,
                menu_adjusted_forecast,
                menu_items,
                signal_availability=signal_availability,
                method_eligibility=method_eligibility,
            )
            forecasts.append(
                FoodDemandForecast(
                    date=target_date,
                    cafeteria_id=cafeteria_id,
                    meal_type=meal_type,
                    predicted_demand=decision["predicted_demand"],
                    planning_lower=decision["planning_lower"],
                    planning_candidate_production=menu_adjusted_forecast,
                    planning_candidate_semantics="ADVISORY_MODEL_ESTIMATE_NOT_AUTHORIZED_KITCHEN_ORDER",
                    recommended_production=decision["recommended_production"],
                    planning_upper=decision["planning_upper"],
                    menu_items=menu_items,
                    policy_version=decision["policy_version"],
                    model_id=decision["model_id"],
                    method_eligibility=decision["method_eligibility"],
                    forecast_provenance=decision["forecast_provenance"],
                    decision_provenance=decision["decision_provenance"],
                    band_semantics=decision["band_semantics"],
                    calibration_status=decision["calibration_status"],
                    signal_coverage_pct=decision["signal_coverage_pct"],
                    decision_readiness=decision["decision_readiness"],
                    abstained=decision["abstained"],
                    operator_approval_required=decision["operator_approval_required"],
                    automatic_kitchen_dispatch=decision["automatic_kitchen_dispatch"],
                    signals=decision["signals"],
                    reason_codes=decision["reason_codes"],
                    limitations=decision["limitations"],
                    model_metadata={
                        **model_metadata,
                        "meal_type": meal_type,
                        "decision_inputs": signal_availability,
                        "baseline_predicted_demand": baseline_point_forecast,
                        "menu_adjusted_predicted_demand": menu_adjusted_forecast,
                        "menu_adjustment": menu_adjustment,
                        "menu_adjustment_semantics": "BOUNDED_POLICY_HEURISTIC_NOT_MEASURED_ELASTICITY",
                    },
                )
            )
    return forecasts


@router.get("/food/live-menu")
def get_live_menu():
    """Return source-tagged menu context; callers must inspect source provenance."""
    return real_service.fetch_live_cafeteria_menu()


@router.get("/food/menu-popularity", response_model=List[MenuPopularity])
def get_menu_popularity():
    with open(os.path.join(settings.DATA_DIR, "menu_popularity.json"), "r", encoding="utf-8") as handle:
        dishes = json.load(handle)["dishes"]
    return [
        MenuPopularity(
            **dish,
            popularity_provenance="POLICY_HEURISTIC" if dish.get("popularity_score") is not None else "UNAVAILABLE",
        )
        for dish in dishes
    ]
