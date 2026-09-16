import type { SourceMeta } from './live-sources';

export interface Building {
  id: string;
  name: string;
  code: string;
  campus: 'south' | 'north';
  coords: [number, number];
  floors: number;
  total_capacity: number;
  type: string;
  current_occupancy?: number;
  occupancy_ratio?: number;
  energy_profile?: {
    base_load_kw: number;
    hvac_coefficient: number;
    lighting_max_kw: number;
    t_target: number;
  };
  floor_capacities?: number[];
}

export interface OccupancyByHour {
  hour: number;
  occupancy_count: number;
  occupancy_ratio: number;
}

export interface OccupancyByFloor {
  floor: number;
  hourly_occupancy: OccupancyByHour[];
}

export interface OccupancyForecast {
  date?: string;
  building_id: string;
  building_name?: string;
  hourly?: OccupancyByHour[];
  total_hourly?: OccupancyByHour[];
  by_floor?: OccupancyByFloor[];
}

export interface FloorEnergyDetail {
  floor: number;
  energy_kwh: number;
  hvac_kwh: number;
  lighting_kwh: number;
  is_active: boolean;
}

export interface HourlyEnergyForecast {
  hour: number;
  total_kwh: number;
  floor_details: FloorEnergyDetail[];
}

export interface EnergySaving {
  kwh_saved: number;
  cost_saved_tl: number;
  co2_avoided_kg: number;
}

export interface EnergyForecast {
  date?: string;
  building_id: string;
  building_name?: string;
  baseline_kwh: number;
  optimized_kwh: number;
  saving_kwh?: number;
  saving_percent?: number;
  savings?: EnergySaving;
  hourly_forecast?: HourlyEnergyForecast[];
  recommendations?: string[];
}

export interface FoodForecast {
  cafeteria_id: string;
  cafeteria_name: string;
  baseline_portions: number;
  predicted_demand: number;
  recommended_production: number;
  avoided_waste_portions: number;
  avoided_waste_kg: number;
  menu_popularity_factor: number;
}

export interface ActionItem {
  id: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  type: 'energy' | 'food' | 'space';
  title: string;
  time: string;
  location: string;
  description: string;
  impact_value: number;
  impact_unit: string;
  icon: string;
  provenance?: 'MODEL_ESTIMATE' | 'OFFICIAL_LIVE' | 'OFFICIAL_SNAPSHOT';
}

export interface LiveWeatherInfo {
  source: string;
  temperature: number | null;
  humidity: number | null;
  rain: boolean | null;
  wind_speed: number | null;
  provenance?: SourceMeta;
}

export interface LiveMenuInfo {
  source: string;
  date: string;
  soup: string | null;
  main_dish: string | null;
  calories: number | null;
  vegan_dish: string | null;
  sides: string[];
  options: string[];
  popularity_multiplier: number;
  provenance?: SourceMeta;
}

export interface LiveWindTurbineInfo {
  source: string;
  wind_speed_kmh: number | null;
  current_power_kw: number | null;
  daily_clean_mwh: number | null;
  co2_offset_kg: number | null;
  campus_electricity_coverage_percent: number | null;
  provenance?: SourceMeta;
}

export interface LiveShuttleInfo {
  route: string;
  departure_times: string[];
  next_departure: string | null;
  provenance: SourceMeta;
}

export interface RealCampusEvent {
  name: string;
  building_id: string;
  location: string;
  time: string;
  expected_attendance: number;
  category: string;
  impact: string;
}

export interface DataQualitySummary {
  mode: 'LIVE_WITH_MODELS' | 'DEGRADED';
  official_live_sources: number;
  external_live_sources: number;
  model_estimates: string[];
  unavailable_sources: string[];
  note: string;
}

export interface DashboardData {
  date: string;
  campus_occupancy: number;
  predicted_energy_mwh: number;
  food_demand_meals: number;
  potential_saving_tl: number;
  co2_avoided_kg: number;
  buildings: Building[];
  actions: ActionItem[];
  occupancy_forecasts?: OccupancyForecast[];
  energy_forecasts?: EnergyForecast[];
  food_forecasts?: FoodForecast[];
  live_weather?: LiveWeatherInfo;
  live_menu?: LiveMenuInfo;
  live_wind?: LiveWindTurbineInfo;
  live_shuttle?: LiveShuttleInfo;
  today_events?: RealCampusEvent[];
  academic_calendar?: string[];
  real_courses_loaded?: number;
  sources?: SourceMeta[];
  data_quality?: DataQualitySummary;
}

export interface ScenarioRequest {
  scenario_type: 'heatwave' | 'exam_week' | 'event' | 'rain' | 'building_closure' | 'summer_school';
  params: Record<string, any>;
}

export interface ScenarioResult {
  original: DashboardData;
  modified: DashboardData;
  changes: {
    energy_change_percent: number;
    food_change_percent: number;
    co2_change_percent: number;
    cost_change_tl: number;
  };
}
