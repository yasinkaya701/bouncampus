from fastapi import APIRouter
from app.schemas import FoodDemandForecast, MenuPopularity
from datetime import date, timedelta
from typing import List, Optional
from app.models.food_demand import FoodDemandPredictor
from app.optimizers.food_optimizer import FoodOptimizer
from app.utils.real_data_service import RealDataService
import json, os
from app.config import settings

router = APIRouter(prefix="/api/v1")
f_pred = FoodDemandPredictor()
f_opt = FoodOptimizer()
real_service = RealDataService()

@router.get("/food", response_model=List[FoodDemandForecast])
def get_food_forecast(date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    live_menu = real_service.fetch_live_cafeteria_menu()
    
    # Map live menu into MenuPopularity
    live_items = [
        MenuPopularity(name=live_menu["main_dish"], name_en="Main Dish", category="meat", popularity_score=live_menu["popularity_multiplier"], avg_rating=4.5),
        MenuPopularity(name=live_menu["soup"], name_en="Daily Soup", category="soup", popularity_score=0.85, avg_rating=4.2),
        MenuPopularity(name=live_menu["vegan_dish"], name_en="Vegan Dish", category="vegan", popularity_score=0.75, avg_rating=4.0)
    ]
    
    res = []
    for c in ['B-SOUTH-GY', 'B-NORTH-KY']:
        for m in ['lunch', 'dinner']:
            d_val, _ = f_pred.predict(d, c)
            # Adjust with live popularity multiplier
            adjusted_demand = int(d_val * live_menu["popularity_multiplier"])
            opt = f_opt.optimize(d, c, adjusted_demand, [])
            res.append(FoodDemandForecast(
                date=d, cafeteria_id=c, meal_type=m, predicted_demand=adjusted_demand,
                recommended_production=opt['recommended'], menu_items=live_items,
                potential_waste_saved_kg=round(opt['waste_reduction'] * 0.4, 1),
                cost_saved_tl=round(opt['waste_reduction'] * 22.0, 1)
            ))
    return res

@router.get("/food/live-menu")
def get_live_menu():
    """Returns the official real-time menu from yemekhane.bogazici.edu.tr"""
    return real_service.fetch_live_cafeteria_menu()

@router.get("/food/menu-popularity", response_model=List[MenuPopularity])
def get_menu_popularity():
    with open(os.path.join(settings.DATA_DIR, 'menu_popularity.json'), 'r') as f:
        dishes = json.load(f)['dishes']
    return [MenuPopularity(**x) for x in dishes]
