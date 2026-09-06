from fastapi import APIRouter
from app.schemas import ScenarioRequest, ScenarioResult, ScenarioComparison
from typing import List
from app.models.occupancy import OccupancyPredictor
from app.models.food_demand import FoodDemandPredictor
import pandas as pd

router = APIRouter(prefix="/api/v1")
occ_predictor = OccupancyPredictor()
food_predictor = FoodDemandPredictor()

@router.post("/scenarios/simulate", response_model=ScenarioResult)
def simulate_scenario(req: ScenarioRequest):
    custom_feats = {}
    if req.scenario_type == 'heatwave': custom_feats['temperature'] = 35.0
    elif req.scenario_type == 'exam_week': custom_feats['exam_week'] = 1
    elif req.scenario_type == 'event': custom_feats['event_count'] = 3
    elif req.scenario_type == 'rain': custom_feats['rain'] = 20.0
    elif req.scenario_type == 'building_closure': custom_feats['total_capacity'] = 0
    elif req.scenario_type == 'summer_school': custom_feats['semester_week'] = 20
    
    # baseline vs scenario
    baseline_occ = occ_predictor.predict_floor("2026-09-07", "B-NORTH-KB", 1)
    scenario_occ = occ_predictor.predict_floor("2026-09-07", "B-NORTH-KB", 1, custom_features=custom_feats)
    
    b_val = sum(x['occupancy_count'] for x in baseline_occ)
    s_val = sum(x['occupancy_count'] for x in scenario_occ)
    
    diff = s_val - b_val
    diff_percent = (diff / b_val) * 100 if b_val > 0 else 0
    
    comp = ScenarioComparison(metric="Daily Occupancy", baseline_value=b_val, scenario_value=s_val, diff=diff, diff_percent=diff_percent)
    
    return ScenarioResult(scenario_type=req.scenario_type, comparisons=[comp], insights=[f"Modified features: {custom_feats}"])
