import snapshot from '@/data/food_waste_2025.json';

export const FAO_GLOBAL_FOOD_WASTE_FACTORS = {
  co2e_kg_per_kg_food_waste: 3.3 / 1.3,
  blue_water_l_per_kg_food_waste: (250 * 1_000_000_000_000) / (1.3 * 1_000_000_000_000),
  source_label: 'FAO Food Wastage Footprint: Impacts on Natural Resources',
  source_url: 'https://www.fao.org/4/i3347e/i3347e.pdf',
  note: 'Global-average proxy only; not a Boğaziçi menu-specific life-cycle assessment.',
} as const;

type MenuSummary = {
  main_dish?: string | null;
  vegan_dish?: string | null;
  soup?: string | null;
  popularity_multiplier?: number | null;
};

type WeatherSummary = {
  rain?: boolean | null;
  temperature?: number | null;
};

export type FoodOperationsModel = {
  date: string;
  mode: 'MODEL_SANDBOX';
  cafeteria: {
    id: string;
    name: string;
    scope_note: string;
  };
  demand: {
    predicted_meals: number;
    model_note: string;
    current_plan_scenario_portions: number;
    recommended_production_portions: number;
    recommended_safety_buffer_pct: number;
    scenario_planning_buffer_pct: number;
    avoidable_overproduction_portions: number;
  };
  risk: {
    level: 'LOW' | 'MEDIUM' | 'HIGH';
    score: number;
    drivers: string[];
  };
  historical_baseline: {
    source_year: 2025;
    month: number;
    month_label_tr: string;
    month_label_en: string;
    monthly_food_waste_kg: number;
    historical_daily_average_kg: number;
    annual_food_waste_kg: number;
    annual_sent_to_istac_for_recycling_kg: number;
    service_population_approx: number;
  };
  pilot_target: {
    reduction_target_pct: number;
    target_avoided_food_waste_kg_per_day: number;
    carbon_proxy_kg_co2e_per_day: number;
    blue_water_proxy_l_per_day: number;
    methodology_note: string;
  };
  menu: MenuSummary | null;
  weather: WeatherSummary | null;
  evidence: Array<{
    label: string;
    url: string;
    provenance: 'OFFICIAL_SNAPSHOT' | 'MODEL_ESTIMATE' | 'EXTERNAL_REFERENCE';
    note: string;
  }>;
  decision: {
    title_tr: string;
    title_en: string;
    action_tr: string;
    action_en: string;
    approval_required: true;
    learn_signal_tr: string;
    learn_signal_en: string;
  };
};

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function round(value: number, digits = 1) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function daysInMonth(year: number, month: number) {
  return new Date(year, month, 0).getDate();
}

export function buildFoodOperationsModel(input: {
  date: string;
  predictedDemand: number;
  planningBufferPct?: number;
  targetReductionPct?: number;
  menu?: MenuSummary | null;
  weather?: WeatherSummary | null;
}): FoodOperationsModel {
  const parsedDate = new Date(`${input.date}T12:00:00+03:00`);
  const month = Number.isNaN(parsedDate.getTime()) ? 1 : parsedDate.getMonth() + 1;
  const monthRow = snapshot.months.find(item => item.month === month) ?? snapshot.months[0];
  const planningBufferPct = clamp(Number(input.planningBufferPct ?? 12), 0, 30);
  const targetReductionPct = clamp(Number(input.targetReductionPct ?? 10), 1, 30);
  const recommendedSafetyBufferPct = 5;
  const predictedDemand = Math.max(0, Math.round(Number(input.predictedDemand) || 0));
  const currentPlan = Math.ceil(predictedDemand * (1 + planningBufferPct / 100));
  const recommended = Math.ceil(predictedDemand * (1 + recommendedSafetyBufferPct / 100));
  const avoidableOverproduction = Math.max(0, currentPlan - recommended);

  const historicalDailyAverage = monthRow.food_waste_kg / daysInMonth(2025, monthRow.month);
  const targetAvoidedKg = historicalDailyAverage * (targetReductionPct / 100);
  const carbonProxy = targetAvoidedKg * FAO_GLOBAL_FOOD_WASTE_FACTORS.co2e_kg_per_kg_food_waste;
  const waterProxy = targetAvoidedKg * FAO_GLOBAL_FOOD_WASTE_FACTORS.blue_water_l_per_kg_food_waste;

  const menuFactor = clamp(Number(input.menu?.popularity_multiplier ?? 1), 0.7, 1.3);
  const rainPenalty = input.weather?.rain === true ? 7 : 0;
  const bufferPenalty = Math.max(0, planningBufferPct - recommendedSafetyBufferPct) * 2.2;
  const menuPenalty = Math.abs(menuFactor - 1) * 40;
  const riskScore = Math.round(clamp(28 + rainPenalty + bufferPenalty + menuPenalty, 0, 100));
  const riskLevel = riskScore >= 65 ? 'HIGH' : riskScore >= 40 ? 'MEDIUM' : 'LOW';

  const drivers = [
    `Demand model: ${predictedDemand.toLocaleString('en-US')} meals from timetable flow + weather`,
    `Scenario planning buffer: ${round(planningBufferPct, 0)}% vs ${recommendedSafetyBufferPct}% pilot buffer`,
    input.weather?.rain === true ? 'Rain signal raises demand uncertainty' : 'No rain uplift in the current weather signal',
    input.menu?.main_dish ? `Official menu signal available: ${input.menu.main_dish}` : 'Official menu item unavailable; no menu-specific demand adjustment claimed',
  ];

  return {
    date: input.date,
    mode: 'MODEL_SANDBOX',
    cafeteria: {
      id: 'BOUN-DINING-COMBINED',
      name: 'Boğaziçi dining operations',
      scope_note: 'Decision-support layer; no cafeteria POS, kitchen ERP, scale, or production-control integration is claimed.',
    },
    demand: {
      predicted_meals: predictedDemand,
      model_note: 'Prediction is derived from the existing BOUNCAMPUS timetable-flow model and weather signal; it is not a POS measurement.',
      current_plan_scenario_portions: currentPlan,
      recommended_production_portions: recommended,
      recommended_safety_buffer_pct: recommendedSafetyBufferPct,
      scenario_planning_buffer_pct: planningBufferPct,
      avoidable_overproduction_portions: avoidableOverproduction,
    },
    risk: {
      level: riskLevel,
      score: riskScore,
      drivers,
    },
    historical_baseline: {
      source_year: 2025,
      month: monthRow.month,
      month_label_tr: monthRow.label_tr,
      month_label_en: monthRow.label_en,
      monthly_food_waste_kg: monthRow.food_waste_kg,
      historical_daily_average_kg: round(historicalDailyAverage, 1),
      annual_food_waste_kg: snapshot.totals.food_waste_kg,
      annual_sent_to_istac_for_recycling_kg: snapshot.totals.sent_to_istac_for_recycling_kg,
      service_population_approx: snapshot.service_population.students + snapshot.service_population.staff,
    },
    pilot_target: {
      reduction_target_pct: targetReductionPct,
      target_avoided_food_waste_kg_per_day: round(targetAvoidedKg, 1),
      carbon_proxy_kg_co2e_per_day: round(carbonProxy, 1),
      blue_water_proxy_l_per_day: round(waterProxy, 0),
      methodology_note: 'Avoided-waste target is applied to the same-month 2025 official daily-average baseline. CO₂e and blue-water values use FAO global-average food-wastage ratios, so they are directional proxies rather than menu-specific LCA results.',
    },
    menu: input.menu ?? null,
    weather: input.weather ?? null,
    evidence: [
      {
        label: snapshot.source.label,
        url: snapshot.source.url,
        provenance: 'OFFICIAL_SNAPSHOT',
        note: `2025 official total: ${snapshot.totals.food_waste_kg.toLocaleString('en-US')} kg food waste; ${snapshot.totals.sent_to_istac_for_recycling_kg.toLocaleString('en-US')} kg reported as sent to ISTAC for recycling.`,
      },
      {
        label: 'BOUNCAMPUS cafeteria demand model',
        url: '/api/v1/dashboard',
        provenance: 'MODEL_ESTIMATE',
        note: 'Timetable-flow + weather model. Must be calibrated against real meal/POS counts before operational deployment.',
      },
      {
        label: FAO_GLOBAL_FOOD_WASTE_FACTORS.source_label,
        url: FAO_GLOBAL_FOOD_WASTE_FACTORS.source_url,
        provenance: 'EXTERNAL_REFERENCE',
        note: FAO_GLOBAL_FOOD_WASTE_FACTORS.note,
      },
    ],
    decision: {
      title_tr: 'Üretimi talep tahmini etrafında kontrollü daralt',
      title_en: 'Tighten production around the demand forecast',
      action_tr: `Pilot için ${recommended.toLocaleString('tr-TR')} porsiyon üretim bandını mutfak sorumlusuna öner; servis sonunda üretilen, tüketilen ve kalan porsiyonları kaydet.`,
      action_en: `Propose a ${recommended.toLocaleString('en-US')}-portion pilot band to the kitchen lead; record produced, served, and leftover portions after service.`,
      approval_required: true,
      learn_signal_tr: 'Ertesi gün gerçek üretim/tüketim/kalan sayılarıyla tahmin hatasını ve güvenlik tamponunu güncelle.',
      learn_signal_en: 'Next day, update forecast error and the safety buffer using actual produced/served/leftover counts.',
    },
  };
}
