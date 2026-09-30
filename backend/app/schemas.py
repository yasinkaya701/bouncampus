from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal


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


class BuildingInfo(Building):
    pass


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
    popularity_score: Optional[float] = None
    avg_rating: Optional[float] = None
    popularity_provenance: Literal["POLICY_HEURISTIC", "UNAVAILABLE"] = "UNAVAILABLE"


class DecisionSignal(BaseModel):
    id: str
    available: bool
    policy_weight_pct: int
    weight_basis: Literal["POLICY_HEURISTIC"]


class FoodDemandForecast(BaseModel):
    date: str
    cafeteria_id: str
    meal_type: str
    predicted_demand: int
    planning_lower: int
    recommended_production: Optional[int]
    planning_upper: int
    menu_items: List[MenuPopularity]
    policy_version: str
    model_id: str
    forecast_provenance: Literal["MODEL_ESTIMATE"]
    decision_provenance: Literal["POLICY_HEURISTIC"]
    band_semantics: Literal["PLANNING_RANGE_NOT_CALIBRATED_INTERVAL"]
    calibration_status: Literal["NOT_CALIBRATED"]
    signal_coverage_pct: int
    decision_readiness: Literal["PILOT_READY", "REVIEW_REQUIRED", "WITHHOLD"]
    abstained: bool
    operator_approval_required: bool
    automatic_kitchen_dispatch: bool
    signals: List[DecisionSignal]
    reason_codes: List[str]
    limitations: List[str]
    model_metadata: Dict[str, Any]


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
    provenance: Optional[
        Literal["MODEL_ESTIMATE", "POLICY_HEURISTIC", "OFFICIAL_LIVE", "OFFICIAL_SNAPSHOT"]
    ] = None


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
    food_waste_avoided_kg: Optional[float] = None
    cost_saved_tl: float
    energy_provenance: Literal["MODEL_ESTIMATE"] = "MODEL_ESTIMATE"
    food_waste_impact_status: Literal["UNMEASURED"] = "UNMEASURED"
    note: str = (
        "Energy values are model estimates. Food-waste impact remains unmeasured until a valid pilot exists."
    )


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
