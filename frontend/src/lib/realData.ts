import { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioResult } from './types';
import campusConfig from '@/data/campus_config.json';
import { computeBuildingOccupancy, computeBuildingEnergy } from './campus-calculations';

// Determine current weekday (0=Mon ... 6=Sun)
const now = new Date();
const currentDayIdx = (now.getDay() + 6) % 7; // Monday = 0
const currentHour = now.getHours();

// 1. Schedule-derived Boğaziçi building occupancy estimates.
export const realBuildings: Building[] = campusConfig.buildings.map(b => {
  const occData = computeBuildingOccupancy(b.id, currentDayIdx);
  const hourState = occData.total_hourly[currentHour] || occData.total_hourly[12];
  const occCount = hourState.occupancy_count;
  const occRatio = hourState.occupancy_ratio;

  return {
    id: b.id,
    name: b.name,
    code: b.code,
    campus: b.campus as 'south' | 'north',
    coords: b.coords as [number, number],
    floors: b.floors,
    total_capacity: b.total_capacity,
    type: b.type,
    current_occupancy: occCount,
    occupancy_ratio: occRatio,
    energy_profile: b.energy_profile
  };
});

// 2. Schedule-derived hourly occupancy forecasts (06:00 - 22:00).
export const realOccupancy: OccupancyForecast[] = campusConfig.buildings.map(b => {
  const occData = computeBuildingOccupancy(b.id, currentDayIdx);
  return {
    building_id: b.id,
    building_name: b.name,
    hourly: occData.total_hourly
      .filter(h => h.hour >= 6 && h.hour <= 22)
      .map(h => ({
        hour: h.hour,
        occupancy_ratio: h.occupancy_ratio,
        occupancy_count: h.occupancy_count,
      }))
  };
});

// 3. Energy model outputs. These are estimates, not measured savings.
export const realEnergy: EnergyForecast[] = campusConfig.buildings.map(b => {
  const nrg = computeBuildingEnergy(b.id, currentDayIdx);
  return {
    building_id: b.id,
    building_name: b.name,
    baseline_kwh: nrg.baseline_kwh,
    optimized_kwh: nrg.optimized_kwh,
    saving_kwh: nrg.saving_kwh,
    saving_percent: nrg.saving_percent,
    recommendations: nrg.recommendations
  };
});

const FALLBACK_POLICY_VERSION = 'food-decision-v1.0';
const FALLBACK_SIGNAL_COVERAGE_PCT = 50;

function fallbackFoodForecast(cafeteriaId: string, predictedDemand: number): FoodForecast {
  return {
    date: now.toISOString().split('T')[0],
    cafeteria_id: cafeteriaId,
    meal_type: 'lunch',
    predicted_demand: predictedDemand,
    planning_lower: Math.round(predictedDemand * 0.9),
    recommended_production: predictedDemand,
    planning_upper: Math.round(predictedDemand * 1.13),
    menu_items: [],
    policy_version: FALLBACK_POLICY_VERSION,
    model_id: 'repository-fallback-demand-estimate',
    forecast_provenance: 'MODEL_ESTIMATE',
    decision_provenance: 'POLICY_HEURISTIC',
    band_semantics: 'PLANNING_RANGE_NOT_CALIBRATED_INTERVAL',
    calibration_status: 'NOT_CALIBRATED',
    signal_coverage_pct: FALLBACK_SIGNAL_COVERAGE_PCT,
    decision_readiness: 'REVIEW_REQUIRED',
    abstained: false,
    operator_approval_required: true,
    automatic_kitchen_dispatch: false,
    signals: [
      { id: 'schedule', available: true, policy_weight_pct: 50, weight_basis: 'POLICY_HEURISTIC' },
      { id: 'weather', available: false, policy_weight_pct: 20, weight_basis: 'POLICY_HEURISTIC' },
      { id: 'menu', available: false, policy_weight_pct: 20, weight_basis: 'POLICY_HEURISTIC' },
      { id: 'calendar', available: false, policy_weight_pct: 10, weight_basis: 'POLICY_HEURISTIC' },
    ],
    reason_codes: [
      'CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED',
      'HEURISTIC_BAND_NOT_CALIBRATED',
      'MISSING_WEATHER',
      'MISSING_MENU',
      'MISSING_CALENDAR',
    ],
    limitations: [
      'STATIC_REPOSITORY_FALLBACK_NOT_LIVE',
      'NO_CAFETERIA_POS_OR_SERVED_MEAL_TELEMETRY',
      'HEURISTIC_BAND_NOT_CALIBRATED',
      'PILOT_OUTCOMES_NOT_YET_MEASURED',
    ],
    model_metadata: {
      source: 'REPOSITORY_FALLBACK',
      result_scope: 'MODEL_SANDBOX',
      impact_validation_status: 'NOT_PILOT_VALIDATED',
    },
  };
}

// 4. Fallback cafeteria demand estimates. They are never treated as measured demand
// or as evidence of achieved food-waste reduction.
export const realFood: FoodForecast[] = [
  fallbackFoodForecast('B-NORTH-KY', 3240),
  fallbackFoodForecast('B-SOUTH-GY', 820),
];

const fallbackFoodDemandMeals = realFood.reduce((sum, item) => sum + item.predicted_demand, 0);

// 5. Prioritized campus actions derived from repository models/policy. Every action
// is review-only; this fallback module cannot dispatch changes to physical systems.
export const realActions: ActionItem[] = [
  {
    id: 'ACT-01',
    priority: 'HIGH',
    type: 'energy',
    title: 'New Hall (NH) 5. ve 6. Kat Konsolidasyonu',
    time: '17:00 - 21:00',
    location: 'Kuzey Kampüs New Hall',
    description: 'Schedule-derived occupancy estimates suggest reviewing evening floor consolidation before any HVAC or lighting action.',
    impact_value: 148,
    impact_unit: 'kWh model potential',
    icon: 'Zap',
    provenance: 'MODEL_ESTIMATE',
  },
  {
    id: 'ACT-02',
    priority: 'HIGH',
    type: 'food',
    title: 'Kuzey Yemekhane Üretim Planını Gözden Geçir',
    time: '16:30',
    location: 'Kuzey Yemekhanesi',
    description: 'Fallback demand is MODEL_ESTIMATE and the planning range is POLICY_HEURISTIC. Decision state is REVIEW_REQUIRED; operator approval is mandatory, automatic kitchen dispatch is disabled, and no food-waste saving is claimed.',
    impact_value: FALLBACK_SIGNAL_COVERAGE_PCT,
    impact_unit: '% decision signal coverage',
    icon: 'Utensils',
    provenance: 'POLICY_HEURISTIC',
  },
  {
    id: 'ACT-03',
    priority: 'MEDIUM',
    type: 'space',
    title: 'Perkins Hall (M) 1. Kat Derslik Birleştirme',
    time: '14:00 - 17:00',
    location: 'Güney Kampüs M-1100 Amfisi',
    description: 'Schedule-derived occupancy estimates suggest a consolidation option; verify room use before any operational change.',
    impact_value: 82,
    impact_unit: 'kWh model potential',
    icon: 'Building2',
    provenance: 'MODEL_ESTIMATE',
  },
  {
    id: 'ACT-04',
    priority: 'MEDIUM',
    type: 'energy',
    title: 'Kare Blok (KB) AHU-2 Eko Mod İncelemesi',
    time: '13:30',
    location: 'Kare Blok Bodrum Katı',
    description: 'Review the modeled ventilation opportunity with real building telemetry before changing AHU state.',
    impact_value: 65,
    impact_unit: 'kWh model potential',
    icon: 'Zap',
    provenance: 'MODEL_ESTIMATE',
  },
  {
    id: 'ACT-05',
    priority: 'LOW',
    type: 'space',
    title: 'Aptullah Kuran Kütüphanesi Kat 3 Isıtma İncelemesi',
    time: '20:00 - 02:00',
    location: 'Kütüphane 3. Kat',
    description: 'Review the modeled nighttime HVAC opportunity against real occupancy and temperature telemetry before action.',
    impact_value: 38,
    impact_unit: 'kWh model potential',
    icon: 'Building2',
    provenance: 'MODEL_ESTIMATE',
  }
];

// 6. Aggregate dashboard model metrics. Food impact is intentionally excluded until
// measured pilot evidence exists.
const totalBaselineEnergy = realEnergy.reduce((acc, e) => acc + e.baseline_kwh, 0);
const totalOptimizedEnergy = realEnergy.reduce((acc, e) => acc + e.optimized_kwh, 0);
const totalEnergySavedKwh = totalBaselineEnergy - totalOptimizedEnergy;
const modeledEnergySavingTl = Math.round(totalEnergySavedKwh * 2.85);
const modeledEnergyCo2Kg = Math.round(totalEnergySavedKwh * 0.47);

const campusTotalStudents = realBuildings.reduce((acc, b) => acc + (b.current_occupancy || 0), 0);
const campusTotalCapacity = realBuildings.reduce((acc, b) => acc + b.total_capacity, 0);
const campusOccupancyRatio = Math.round((campusTotalStudents / campusTotalCapacity) * 100) / 100;

export const realDashboardData: DashboardData = {
  date: now.toISOString().split('T')[0],
  campus_occupancy: campusOccupancyRatio,
  predicted_energy_mwh: Math.round((totalBaselineEnergy / 1000) * 10) / 10,
  food_demand_meals: fallbackFoodDemandMeals,
  potential_saving_tl: modeledEnergySavingTl,
  co2_avoided_kg: modeledEnergyCo2Kg,
  buildings: realBuildings,
  actions: realActions,
  occupancy_forecasts: realOccupancy,
  energy_forecasts: realEnergy,
  food_forecasts: realFood,
  data_quality: {
    mode: 'MODEL_SANDBOX',
    official_live_sources: 0,
    external_live_sources: 0,
    model_estimates: ['building occupancy', 'energy', 'food demand'],
    unavailable_sources: ['cafeteria POS', 'produced portions', 'served portions', 'measured service waste', 'live building telemetry'],
    note: 'Repository fallback only. Food demand and energy values are model estimates; no achieved food-waste or climate impact is claimed.',
  },
};

// 7. Scenario Simulation Engine. Changes are counterfactual scenario outputs, not
// measured impact.
export const realScenarioResult: ScenarioResult = {
  original: realDashboardData,
  modified: {
    ...realDashboardData,
    campus_occupancy: Math.min(1.0, campusOccupancyRatio * 1.25),
    predicted_energy_mwh: Math.round(realDashboardData.predicted_energy_mwh * 1.18 * 10) / 10,
    food_demand_meals: Math.round(realDashboardData.food_demand_meals * 1.22),
    potential_saving_tl: Math.round(realDashboardData.potential_saving_tl * 1.3),
    co2_avoided_kg: Math.round(realDashboardData.co2_avoided_kg * 1.24),
  },
  changes: {
    energy_change_percent: 18.2,
    food_change_percent: 22.0,
    co2_change_percent: 24.1,
    cost_change_tl: Math.round(modeledEnergySavingTl * 0.3),
  }
};
