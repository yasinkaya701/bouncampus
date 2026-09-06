from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal
from datetime import date

class Building(BaseModel):
    id: str
    name: str
    code: str
    campus: str
    coords: List[float]
    floors: int
    total_capacity: int
    type: str
    occupancy_ratio: Optional[float] = None
    floor_capacities: Optional[List[int]] = None

class BuildingInfo(Building): pass

class OccupancyByHour(BaseModel):
    hour: int
    occupancy_count: int
    occupancy_ratio: float

class OccupancyByFloor(BaseModel):
    floor: int
    hourly_occupancy: List[OccupancyByHour]

class OccupancyForecast(BaseModel):
    date: str
    building_id: str
    total_hourly: List[OccupancyByHour]
    by_floor: Optional[List[OccupancyByFloor]] = None

class FloorEnergyDetail(BaseModel):
    floor: int
    energy_kwh: float
    hvac_kwh: float
    lighting_kwh: float
    is_active: bool

class HourlyEnergyForecast(BaseModel):
    hour: int
    total_kwh: float
    floor_details: List[FloorEnergyDetail]

class EnergySaving(BaseModel):
    kwh_saved: float
    cost_saved_tl: float
    co2_avoided_kg: float

class EnergyForecast(BaseModel):
    date: str
    building_id: str
    baseline_kwh: float
    optimized_kwh: float
    savings: EnergySaving
    hourly_forecast: List[HourlyEnergyForecast]

class MenuPopularity(BaseModel):
    name: str
    name_en: str
    category: str
    popularity_score: float
    avg_rating: float

class FoodDemandForecast(BaseModel):
    date: str
    cafeteria_id: str
    meal_type: str
    predicted_demand: int
    recommended_production: int
    menu_items: List[MenuPopularity]
    potential_waste_saved_kg: float
    cost_saved_tl: float

class ActionItem(BaseModel):
    id: str
    priority: str
    type: str
    title: str
    time: str
    location: str
    description: str
    impact_value: float
    impact_unit: str

class ScenarioRequest(BaseModel):
    scenario_type: str
    params: Dict[str, Any]

class ScenarioComparison(BaseModel):
    metric: str
    baseline_value: float
    scenario_value: float
    diff: float
    diff_percent: float

class ScenarioResult(BaseModel):
    scenario_type: str
    comparisons: List[ScenarioComparison]
    insights: List[str]

class ImpactMetrics(BaseModel):
    kwh_saved: float
    co2_avoided_kg: float
    food_waste_avoided_kg: float
    cost_saved_tl: float

class LiveWeatherInfo(BaseModel):
    source: str
    temperature: float
    humidity: int
    rain: bool
    wind_speed: float

class LiveMenuInfo(BaseModel):
    source: str
    date: str
    soup: str
    main_dish: str
    calories: int
    vegan_dish: str
    sides: List[str]
    options: List[str]
    popularity_multiplier: float

class LiveWindTurbineInfo(BaseModel):
    source: str
    wind_speed_kmh: float
    current_power_kw: float
    daily_clean_mwh: float
    co2_offset_kg: float
    campus_electricity_coverage_percent: float

class RealCampusEvent(BaseModel):
    name: str
    building_id: str
    location: str
    time: str
    expected_attendance: int
    category: str
    impact: str

class DashboardData(BaseModel):
    date: str
    campus_occupancy: int
    predicted_energy_mwh: float
    food_demand_meals: int
    potential_saving_tl: float
    co2_avoided_kg: float
    buildings: List[Building]
    actions: List[ActionItem]
    live_weather: Optional[LiveWeatherInfo] = None
    live_menu: Optional[LiveMenuInfo] = None
    live_wind: Optional[LiveWindTurbineInfo] = None
    today_events: Optional[List[RealCampusEvent]] = None
    real_courses_loaded: Optional[int] = None


