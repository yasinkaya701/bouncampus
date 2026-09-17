import type {
  FoodBatchPlan,
  FoodCafeteriaSummary,
  FoodDataSource,
  FoodDecisionDriver,
  FoodForecast,
  FoodIntelligenceResponse,
  FoodMealType,
  FoodProvenance,
  FoodReforecastRequest,
  FoodWasteBaseline,
} from './types';

const OFFICIAL_WASTE_URL = 'https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310';
const OFFICIAL_SKS_REPORT_URL = 'https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096';
const OFFICIAL_SERVICE_URL = 'https://yemekhane.bogazici.edu.tr/yemek-servislerimiz';
const OFFICIAL_MENU_URL = 'https://yemekhane.bogazici.edu.tr/';

export const OFFICIAL_WASTE_2025: FoodWasteBaseline = {
  year: 2025,
  total_food_waste_kg: 48251,
  recycled_food_waste_kg: 33430,
  waste_oil_kg: 6305,
  provenance: 'OFFICIAL_PUBLIC_HISTORICAL',
  source_url: OFFICIAL_WASTE_URL,
  months: [
    { month: 1, food_waste_kg: 3992, recycled_food_waste_kg: 2250 },
    { month: 2, food_waste_kg: 7811, recycled_food_waste_kg: 1555 },
    { month: 3, food_waste_kg: 7004, recycled_food_waste_kg: 2285 },
    { month: 4, food_waste_kg: 4772, recycled_food_waste_kg: 3090 },
    { month: 5, food_waste_kg: 3832, recycled_food_waste_kg: 2900 },
    { month: 6, food_waste_kg: 2777, recycled_food_waste_kg: 1450 },
    { month: 7, food_waste_kg: 1923, recycled_food_waste_kg: 1850 },
    { month: 8, food_waste_kg: 1502, recycled_food_waste_kg: 3550 },
    { month: 9, food_waste_kg: 2072, recycled_food_waste_kg: 1450 },
    { month: 10, food_waste_kg: 1334, recycled_food_waste_kg: 4850 },
    { month: 11, food_waste_kg: 4784, recycled_food_waste_kg: 3300 },
    { month: 12, food_waste_kg: 6448, recycled_food_waste_kg: 4900 },
  ],
};

type ServiceTable = Record<FoodMealType, string | null>;

type CafeteriaConfig = FoodCafeteriaSummary & {
  weekday: ServiceTable;
  weekend: ServiceTable;
};

const CAFETERIAS: CafeteriaConfig[] = [
  {
    id: 'B-NORTH-KY',
    name_tr: 'Kuzey Kampüs Yemekhanesi',
    name_en: 'North Campus Dining Hall',
    campus: 'north',
    seating_capacity: 692,
    weekday: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
    weekend: { breakfast: '08:30-10:00', lunch: '12:00-13:45', dinner: '17:30-19:30' },
    service: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
  },
  {
    id: 'B-SOUTH-GY',
    name_tr: 'Güney Kampüs Yemekhanesi',
    name_en: 'South Campus Dining Hall',
    campus: 'south',
    seating_capacity: 114,
    weekday: { breakfast: '07:30-09:30', lunch: '12:15-14:30', dinner: '17:00-19:15' },
    weekend: { breakfast: '08:30-10:00', lunch: '12:00-13:45', dinner: '17:30-19:30' },
    service: { breakfast: '07:30-09:30', lunch: '12:15-14:30', dinner: '17:00-19:15' },
  },
  {
    id: 'B-HISAR-YM',
    name_tr: 'Hisar Kampüs Yemekhanesi',
    name_en: 'Hisar Campus Dining Hall',
    campus: 'hisar',
    seating_capacity: 118,
    weekday: { breakfast: null, lunch: '11:30-14:30', dinner: null },
    weekend: { breakfast: null, lunch: null, dinner: null },
    service: { breakfast: null, lunch: '11:30-14:30', dinner: null },
  },
  {
    id: 'B-KANDILLI-YM',
    name_tr: 'Kandilli Kampüs Yemekhanesi',
    name_en: 'Kandilli Campus Dining Hall',
    campus: 'kandilli',
    seating_capacity: 120,
    weekday: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
    weekend: { breakfast: '08:30-10:00', lunch: '12:00-13:45', dinner: '17:30-19:30' },
    service: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
  },
  {
    id: 'B-ANADOLU-YM',
    name_tr: 'Anadolu Hisarı Kampüs Yemekhanesi',
    name_en: 'Anadolu Hisarı Campus Dining Hall',
    campus: 'anadolu-hisari',
    seating_capacity: 486,
    weekday: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
    weekend: { breakfast: '08:30-10:00', lunch: '12:00-13:45', dinner: '17:30-19:30' },
    service: { breakfast: '07:30-09:30', lunch: '11:30-14:30', dinner: '17:00-19:15' },
  },
  {
    id: 'B-KILYOS-YM',
    name_tr: 'Kilyos / Sarıtepe Kampüs Yemekhanesi',
    name_en: 'Kilyos / Sarıtepe Campus Dining Hall',
    campus: 'kilyos-saritepe',
    seating_capacity: 122,
    weekday: { breakfast: '07:30-10:00', lunch: '12:00-15:00', dinner: '17:00-19:15' },
    weekend: { breakfast: '08:30-10:00', lunch: '12:00-13:45', dinner: '17:30-19:30' },
    service: { breakfast: '07:30-10:00', lunch: '12:00-15:00', dinner: '17:00-19:15' },
  },
];

const OFFICIAL_DAILY_MEALS = 6000;
const OFFICIAL_PACKAGE_MEALS = 2000;
const MEAL_SHARE: Record<FoodMealType, number> = { breakfast: 0.18, lunch: 0.5, dinner: 0.32 };
const SCENARIO_PROBABILITIES = { low: 0.2, mean: 0.6, high: 0.2 };

export interface FoodIntelligenceInput {
  date: string;
  northSouthLunchSignal?: number | null;
  rain?: boolean | null;
  temperature?: number | null;
  menu?: {
    main_dish?: string | null;
    soup?: string | null;
    vegan_dish?: string | null;
    source?: string | null;
    provenance?: { provenance?: string; ok?: boolean } | null;
  } | null;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function roundTo(value: number, step: number) {
  return Math.max(0, Math.round(value / step) * step);
}

function isWeekend(date: string) {
  const day = new Date(`${date}T12:00:00+03:00`).getDay();
  return day === 0 || day === 6;
}

function serviceFor(cafeteria: CafeteriaConfig, date: string): ServiceTable {
  return isWeekend(date) ? cafeteria.weekend : cafeteria.weekday;
}

function mealCapacity(date: string, meal: FoodMealType) {
  return CAFETERIAS.reduce((sum, cafeteria) => {
    return sum + (serviceFor(cafeteria, date)[meal] ? cafeteria.seating_capacity : 0);
  }, 0);
}

function baseDemandFor(date: string, cafeteria: CafeteriaConfig, meal: FoodMealType) {
  const service = serviceFor(cafeteria, date)[meal];
  if (!service) return 0;
  const activeCapacity = mealCapacity(date, meal);
  const dayScale = isWeekend(date) ? 0.55 : 1;
  const mealTotal = OFFICIAL_DAILY_MEALS * MEAL_SHARE[meal] * dayScale;
  return activeCapacity > 0 ? mealTotal * cafeteria.seating_capacity / activeCapacity : 0;
}

function publicProxyScale(input: FoodIntelligenceInput) {
  const north = CAFETERIAS.find(item => item.id === 'B-NORTH-KY')!;
  const south = CAFETERIAS.find(item => item.id === 'B-SOUTH-GY')!;
  const publicNorthSouthLunch = baseDemandFor(input.date, north, 'lunch') + baseDemandFor(input.date, south, 'lunch');
  if (!input.northSouthLunchSignal || publicNorthSouthLunch <= 0) return 1;
  return clamp(input.northSouthLunchSignal / publicNorthSouthLunch, 0.62, 1.38);
}

function scenarioWaste(production: number, demand: number) {
  return Math.max(0, production - demand);
}

function scenarioShortage(production: number, demand: number) {
  return Math.max(0, demand - production);
}

function expectedWasteForAdaptivePlan(low: number, mean: number, high: number, initial: number, second: number, reserve: number) {
  const lowProduction = initial + Math.round(second * 0.25);
  const meanProduction = initial + second;
  const highProduction = initial + second + reserve;
  return (
    SCENARIO_PROBABILITIES.low * scenarioWaste(lowProduction, low)
    + SCENARIO_PROBABILITIES.mean * scenarioWaste(meanProduction, mean)
    + SCENARIO_PROBABILITIES.high * scenarioWaste(highProduction, high)
  );
}

function optimizeBatchPlan(low: number, mean: number, high: number) {
  const step = mean >= 800 ? 10 : 5;
  const minInitial = roundTo(Math.max(low * 0.68, mean * 0.52), step);
  const maxInitial = roundTo(mean * 0.9, step);
  const maxSecond = roundTo(mean * 0.4, step);
  const maxReserve = roundTo(mean * 0.22, step);

  let best = {
    cost: Number.POSITIVE_INFINITY,
    initial: roundTo(mean * 0.72, step),
    second: roundTo(mean * 0.18, step),
    reserve: roundTo(Math.max(0, high - mean * 0.9), step),
  };

  for (let initial = minInitial; initial <= maxInitial; initial += step) {
    for (let second = 0; second <= maxSecond; second += step) {
      const reserve = Math.min(maxReserve, roundTo(Math.max(0, high - initial - second), step));
      const lowProduction = initial + Math.round(second * 0.25);
      const meanProduction = initial + second;
      const highProduction = initial + second + reserve;
      const scenarioLoss = (
        SCENARIO_PROBABILITIES.low * (scenarioWaste(lowProduction, low) * 1.1 + scenarioShortage(lowProduction, low) * 5.5)
        + SCENARIO_PROBABILITIES.mean * (scenarioWaste(meanProduction, mean) * 1.1 + scenarioShortage(meanProduction, mean) * 5.5)
        + SCENARIO_PROBABILITIES.high * (scenarioWaste(highProduction, high) * 1.1 + scenarioShortage(highProduction, high) * 5.5)
      );
      const operationalChangeCost = second * 0.045 + reserve * 0.075;
      const cost = scenarioLoss + operationalChangeCost;
      if (cost < best.cost) best = { cost, initial, second, reserve };
    }
  }

  const initial = best.initial;
  const second = best.second;
  const reserve = best.reserve;
  const adaptiveWaste = expectedWasteForAdaptivePlan(low, mean, high, initial, second, reserve);
  const singleBatchReference = roundTo(high, step);
  const referenceWaste = (
    SCENARIO_PROBABILITIES.low * scenarioWaste(singleBatchReference, low)
    + SCENARIO_PROBABILITIES.mean * scenarioWaste(singleBatchReference, mean)
    + SCENARIO_PROBABILITIES.high * scenarioWaste(singleBatchReference, high)
  );

  const plan: FoodBatchPlan[] = [
    { id: 'initial', label: 'Initial batch', portions: initial, release_offset_minutes: -90, mode: 'COMMIT' },
    { id: 'second', label: 'T−45 batch', portions: second, release_offset_minutes: -45, mode: 'CONDITIONAL' },
    { id: 'reserve', label: 'Prep-ready reserve', portions: reserve, release_offset_minutes: -15, mode: 'RESERVE' },
  ];

  return {
    plan,
    recommended: initial + second,
    maximum: initial + second + reserve,
    baseline: singleBatchReference,
    avoidedWastePortions: Math.max(0, Math.round(referenceWaste - adaptiveWaste)),
  };
}

function normalizeMenuProvenance(input: FoodIntelligenceInput): FoodProvenance {
  const value = input.menu?.provenance?.provenance;
  if (value === 'OFFICIAL_LIVE' && input.menu?.provenance?.ok !== false) return 'OFFICIAL_LIVE';
  if (value === 'OFFICIAL_SNAPSHOT') return 'OFFICIAL_SNAPSHOT';
  return 'NOT_CONNECTED';
}

function forecastFor(
  cafeteria: CafeteriaConfig,
  meal: FoodMealType,
  input: FoodIntelligenceInput,
  scale: number,
): FoodForecast | null {
  const service = serviceFor(cafeteria, input.date)[meal];
  if (!service) return null;

  const base = baseDemandFor(input.date, cafeteria, meal);
  const predicted = Math.max(1, Math.round(base * scale));
  const uncertainty = meal === 'lunch' ? 0.14 : 0.17;
  const low = Math.max(0, Math.round(predicted * (1 - uncertainty)));
  const high = Math.max(predicted, Math.round(predicted * (1 + uncertainty)));
  const optimized = optimizeBatchPlan(low, predicted, high);
  const drivers: FoodDecisionDriver[] = [
    {
      id: 'official-operational-scale',
      label: 'Official daily meal scale',
      value: `${OFFICIAL_DAILY_MEALS.toLocaleString('tr-TR')} meals/day`,
      effect: 'NEUTRAL',
      provenance: 'OFFICIAL_SNAPSHOT',
    },
    {
      id: 'timetable-weather-proxy',
      label: 'Timetable + weather demand proxy',
      value: `${scale.toFixed(2)}×`,
      effect: scale > 1.03 ? 'UP' : scale < 0.97 ? 'DOWN' : 'NEUTRAL',
      provenance: 'MODEL_ESTIMATE',
    },
    {
      id: 'weather',
      label: 'Weather context',
      value: input.rain === true ? 'Rain' : input.rain === false ? 'No rain' : 'Unavailable',
      effect: input.rain === true ? 'UP' : 'NEUTRAL',
      provenance: input.rain == null ? 'NOT_CONNECTED' : 'EXTERNAL_FORECAST',
    },
    {
      id: 'menu-feedback',
      label: 'Menu vote / rating',
      value: 'Not connected — neutral factor',
      effect: 'NEUTRAL',
      provenance: 'NOT_CONNECTED',
    },
  ];

  return {
    date: input.date,
    cafeteria_id: cafeteria.id,
    cafeteria_name: cafeteria.name_tr,
    campus: cafeteria.campus,
    seating_capacity: cafeteria.seating_capacity,
    meal_type: meal,
    service_window: service,
    baseline_portions: optimized.baseline,
    predicted_demand: predicted,
    demand_low: low,
    demand_high: high,
    confidence_level: 0.8,
    recommended_production: optimized.recommended,
    max_production: optimized.maximum,
    avoided_waste_portions: optimized.avoidedWastePortions,
    avoided_waste_kg: null,
    water_avoided_liters: null,
    co2_avoided_kg: null,
    menu_popularity_factor: null,
    menu_popularity_status: 'NOT_CONNECTED',
    batch_plan: optimized.plan,
    drivers,
    provenance: 'MODEL_ESTIMATE',
    model_status: 'PUBLIC_PROXY_UNCALIBRATED',
    comparison_basis: 'Modeled adaptive batching vs. a risk-averse single batch sized to the 80% upper demand bound; this is not measured waste prevention.',
  };
}

export function buildFoodIntelligence(input: FoodIntelligenceInput): FoodIntelligenceResponse {
  const scale = publicProxyScale(input);
  const meals: FoodMealType[] = ['breakfast', 'lunch', 'dinner'];
  const forecasts = CAFETERIAS.flatMap(cafeteria => meals
    .map(meal => forecastFor(cafeteria, meal, input, scale))
    .filter((forecast): forecast is FoodForecast => forecast !== null));

  const menuProvenance = normalizeMenuProvenance(input);
  const sources: FoodDataSource[] = [
    {
      id: 'food-waste-2025',
      label: 'Boğaziçi Campus Food Waste Tracking — 2025',
      provenance: 'OFFICIAL_PUBLIC_HISTORICAL',
      status: 'CONNECTED',
      url: OFFICIAL_WASTE_URL,
      detail: '48,251 kg annual food-waste outcome with monthly values; used as the campus baseline, not as cafeteria-level labels.',
    },
    {
      id: 'sks-operational-scale',
      label: 'SKS 2025 activity report',
      provenance: 'OFFICIAL_SNAPSHOT',
      status: 'PUBLIC_AGGREGATE',
      url: OFFICIAL_SKS_REPORT_URL,
      detail: '6 dining halls, approximately 6,000 daily meals and 2,000 package meals. Aggregate operational scale only.',
    },
    {
      id: 'cafeteria-service-hours',
      label: 'Official dining service hours',
      provenance: 'OFFICIAL_LIVE',
      status: 'CONNECTED',
      url: OFFICIAL_SERVICE_URL,
      detail: 'Meal availability and service windows by campus are used by the batch scheduler.',
    },
    {
      id: 'official-menu',
      label: 'Official SKS menu',
      provenance: menuProvenance,
      status: menuProvenance === 'OFFICIAL_LIVE' ? 'CONNECTED' : 'NOT_CONNECTED',
      url: OFFICIAL_MENU_URL,
      detail: menuProvenance === 'OFFICIAL_LIVE' ? 'Current menu is connected.' : 'Current menu fetch is unavailable; no fallback dish is treated as real.',
    },
    {
      id: 'bucard-production-leftover',
      label: 'BUCard + production + served + leftover feed',
      provenance: 'AUTHORIZED_PRIVATE',
      status: 'NOT_CONNECTED',
      detail: 'Required for pilot calibration, 30-minute live reforecasting and measured waste-prevention claims. No personal identity is required.',
    },
    {
      id: 'menu-rating',
      label: 'BUCampus menu vote / daily rating',
      provenance: 'AUTHORIZED_PRIVATE',
      status: 'NOT_CONNECTED',
      detail: 'Public demo keeps the factor neutral. Synthetic popularity scores are never presented as student feedback.',
    },
    {
      id: 'lca-coefficients',
      label: 'Menu-level water and carbon coefficients',
      provenance: 'EXTERNAL_COEFFICIENT',
      status: 'NOT_CONNECTED',
      detail: 'Water and CO₂ avoided remain null until ingredient/portion mapping and coefficient provenance are available.',
    },
  ];

  return {
    date: input.date,
    mode: 'PUBLIC_PROXY',
    official_baseline: OFFICIAL_WASTE_2025,
    operational_scale: {
      daily_meals: OFFICIAL_DAILY_MEALS,
      package_meals: OFFICIAL_PACKAGE_MEALS,
      provenance: 'OFFICIAL_SNAPSHOT',
    },
    menu: {
      main_dish: input.menu?.main_dish ?? null,
      soup: input.menu?.soup ?? null,
      vegan_dish: input.menu?.vegan_dish ?? null,
      source: input.menu?.source ?? 'Official SKS menu unavailable',
      provenance: menuProvenance,
    },
    cafeterias: CAFETERIAS.map(cafeteria => ({
      id: cafeteria.id,
      name_tr: cafeteria.name_tr,
      name_en: cafeteria.name_en,
      campus: cafeteria.campus,
      seating_capacity: cafeteria.seating_capacity,
      service: serviceFor(cafeteria, input.date),
    })),
    forecasts,
    sources,
    limitations: [
      'Public data does not expose cafeteria-level transactions, production quantities or leftovers, so demand remains a model estimate until an authorized pilot feed is connected.',
      'The 2025 48,251 kg figure is a real campus-level historical baseline; it is not attributed to a specific cafeteria, meal or menu item.',
      'Avoided portions compare two modeled production policies. Avoided kg, virtual water and CO₂e are intentionally not calculated without sourced portion/LCA coefficients.',
      'Menu popularity is neutral in public mode; no synthetic rating is treated as real student feedback.',
    ],
    reforecast_contract: {
      endpoint: '/api/v1/food',
      cadence_minutes: 30,
      required_private_fields: ['served_so_far', 'production_committed', 'timestamp', 'cafeteria_id', 'meal_type'],
      manual_operator_input_supported: true,
    },
  };
}

export function reforecastFoodDecision(prior: FoodForecast, request: FoodReforecastRequest): FoodForecast {
  const elapsed = clamp(request.elapsed_fraction, 0.05, 0.95);
  const queue = Math.max(0, request.queue_count ?? 0);
  const paceProjection = request.served_so_far / elapsed + queue * 0.35;
  const updatedMean = Math.max(request.served_so_far, Math.round(prior.predicted_demand * 0.45 + paceProjection * 0.55));
  const low = Math.max(request.served_so_far, Math.round(updatedMean * 0.92));
  const high = Math.max(updatedMean, Math.round(updatedMean * 1.08));
  const optimized = optimizeBatchPlan(low, updatedMean, high);

  return {
    ...prior,
    predicted_demand: updatedMean,
    demand_low: low,
    demand_high: high,
    confidence_level: 0.8,
    baseline_portions: optimized.baseline,
    recommended_production: optimized.recommended,
    max_production: optimized.maximum,
    avoided_waste_portions: optimized.avoidedWastePortions,
    batch_plan: optimized.plan,
    model_status: 'LIVE_REFORECAST',
    drivers: [
      {
        id: 'operator-served-so-far',
        label: 'Served so far',
        value: `${Math.max(0, request.served_so_far)} portions @ ${(elapsed * 100).toFixed(0)}% service elapsed`,
        effect: paceProjection > prior.predicted_demand ? 'UP' : paceProjection < prior.predicted_demand ? 'DOWN' : 'NEUTRAL',
        provenance: 'USER_INPUT',
      },
      ...prior.drivers.filter(driver => driver.id !== 'operator-served-so-far'),
    ],
    comparison_basis: 'Live reforecast uses operator-observed serving pace plus the public prior. With an authorized BUCard/POS feed the same contract can run automatically every 30 minutes.',
  };
}
