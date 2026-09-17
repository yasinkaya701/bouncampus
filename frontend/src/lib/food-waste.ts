export type FoodWasteMonth = {
  month: string;
  monthTr: string;
  wasteKg: number;
  recoveredKg: number;
  wasteOilKg: number;
};

export type FoodWasteScenario = {
  preventionRatePct: number;
  recoveryRatePct: number;
  preventedKg: number;
  remainingWasteKg: number;
  recoveredKg: number;
  residualKg: number;
  residualReductionKg: number;
};

export type DemandSignalId = 'schedule' | 'weather' | 'menu' | 'calendar';

export type DemandSignal = {
  id: DemandSignalId;
  label: string;
  available: boolean;
  weightPct: number;
};

export type DecisionReadiness = 'PILOT_READY' | 'REVIEW_REQUIRED' | 'WITHHOLD';

export type ProductionDecisionBand = {
  predictedMeals: number;
  lowerBound: number;
  recommendedTarget: number;
  upperBound: number;
  signalCoveragePct: number;
  decisionReadiness: DecisionReadiness;
  operatorApprovalRequired: true;
  autoDispatchAllowed: false;
  provenance: 'MODEL_ESTIMATE';
  signals: DemandSignal[];
  reasonCodes: string[];
};

export type PilotServiceMeasurement = {
  date: string;
  serviceId: string;
  arm: 'CONTROL' | 'INTERVENTION';
  modelForecastMeals: number | null;
  producedPortions: number;
  servedPortions: number;
  edibleSurplusKg: number;
  wasteKg: number;
  earlySellout: boolean;
  operatorOverride: boolean;
  notes?: string;
};

export const FOOD_WASTE_SOURCE = {
  title: 'Boğaziçi University — Campus food waste tracking',
  url: 'https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310',
  provenance: 'OFFICIAL_PUBLIC' as const,
};

export const SKS_ACTIVITY_SOURCE = {
  title: 'Boğaziçi University SKS — Faaliyet Raporu',
  url: 'https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096',
  provenance: 'OFFICIAL_PUBLIC' as const,
};

export const FOOD_WASTE_2025: FoodWasteMonth[] = [
  { month: 'Jan', monthTr: 'Oca', wasteKg: 3992, recoveredKg: 2250, wasteOilKg: 475 },
  { month: 'Feb', monthTr: 'Şub', wasteKg: 7811, recoveredKg: 1555, wasteOilKg: 250 },
  { month: 'Mar', monthTr: 'Mar', wasteKg: 7004, recoveredKg: 2285, wasteOilKg: 900 },
  { month: 'Apr', monthTr: 'Nis', wasteKg: 4772, recoveredKg: 3090, wasteOilKg: 825 },
  { month: 'May', monthTr: 'May', wasteKg: 3832, recoveredKg: 2900, wasteOilKg: 450 },
  { month: 'Jun', monthTr: 'Haz', wasteKg: 2777, recoveredKg: 1450, wasteOilKg: 550 },
  { month: 'Jul', monthTr: 'Tem', wasteKg: 1923, recoveredKg: 1850, wasteOilKg: 150 },
  { month: 'Aug', monthTr: 'Ağu', wasteKg: 1502, recoveredKg: 3550, wasteOilKg: 350 },
  { month: 'Sep', monthTr: 'Eyl', wasteKg: 2072, recoveredKg: 1450, wasteOilKg: 830 },
  { month: 'Oct', monthTr: 'Eki', wasteKg: 1334, recoveredKg: 4850, wasteOilKg: 600 },
  { month: 'Nov', monthTr: 'Kas', wasteKg: 4784, recoveredKg: 3300, wasteOilKg: 550 },
  { month: 'Dec', monthTr: 'Ara', wasteKg: 6448, recoveredKg: 4900, wasteOilKg: 375 },
];

export const FOOD_WASTE_BASELINE = {
  year2024WasteKg: 50993,
  year2025WasteKg: 48251,
  year2025RecoveredKg: 33430,
  year2025WasteOilKg: 6305,
  communityStudents: 13000,
  communityStaff: 2000,
  diningHallCapacity: 1734,
  campusesWithDining: 6,
};

export const FOOD_WASTE_PILOT_PROTOCOL = {
  version: '1.0',
  durationDays: 14,
  design: 'MATCHED_CONTROL_INTERVENTION' as const,
  hypothesis: 'Operator-reviewed demand bands reduce normalized food waste without increasing early sell-out risk.',
  primaryMetric: {
    id: 'waste_kg_per_100_served',
    label: 'Waste kg / 100 served meals',
    formula: '(waste_kg / served_portions) * 100',
    rationale: 'Normalizes waste by service volume so a quiet day cannot look artificially better than a busy day.',
  },
  secondaryMetrics: [
    'waste kg / service',
    'overproduction rate',
    'edible surplus kg / 100 served meals',
    'forecast absolute percentage error',
    'operator override rate',
    'early-sellout incidence',
  ],
  measurementFields: [
    'date',
    'service_id',
    'arm',
    'model_forecast_meals',
    'produced_portions',
    'served_portions',
    'edible_surplus_kg',
    'waste_kg',
    'early_sellout',
    'operator_override',
    'notes',
  ],
  successGate: {
    minimumMeasuredServicesPerArm: 5,
    targetWasteReductionPct: 10,
    serviceGuardrail: 'No increase in early-sellout incidence versus the matched control arm.',
    safetyGuardrail: 'No food-safety process may be bypassed by a production recommendation.',
    interpretation: 'The 10% reduction is a pre-registered pilot target, not an achieved result.',
  },
  privacy: 'No personal or student-level data is required for the pilot.',
};

export const CURRENT_RECOVERY_RATE_PCT =
  (FOOD_WASTE_BASELINE.year2025RecoveredKg / FOOD_WASTE_BASELINE.year2025WasteKg) * 100;

export const YEAR_OVER_YEAR_REDUCTION_PCT =
  ((FOOD_WASTE_BASELINE.year2024WasteKg - FOOD_WASTE_BASELINE.year2025WasteKg) /
    FOOD_WASTE_BASELINE.year2024WasteKg) *
  100;

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

export function simulateFoodWasteScenario(
  preventionRatePct: number,
  recoveryRatePct: number,
): FoodWasteScenario {
  const prevention = clamp(preventionRatePct, 0, 60);
  const recovery = clamp(recoveryRatePct, 0, 100);
  const baseline = FOOD_WASTE_BASELINE.year2025WasteKg;
  const preventedKg = baseline * (prevention / 100);
  const remainingWasteKg = Math.max(0, baseline - preventedKg);
  const recoveredKg = remainingWasteKg * (recovery / 100);
  const residualKg = Math.max(0, remainingWasteKg - recoveredKg);
  const baselineResidual = baseline - FOOD_WASTE_BASELINE.year2025RecoveredKg;

  return {
    preventionRatePct: prevention,
    recoveryRatePct: recovery,
    preventedKg: Math.round(preventedKg),
    remainingWasteKg: Math.round(remainingWasteKg),
    recoveredKg: Math.round(recoveredKg),
    residualKg: Math.round(residualKg),
    residualReductionKg: Math.round(Math.max(0, baselineResidual - residualKg)),
  };
}

export function buildProductionBand(
  predictedMeals: number,
  availability: Partial<Record<DemandSignalId, boolean>> = {},
): ProductionDecisionBand | null {
  const demand = Math.max(0, Math.round(predictedMeals));
  if (!demand) return null;

  const signals: DemandSignal[] = [
    { id: 'schedule', label: 'Course schedule', available: Boolean(availability.schedule), weightPct: 50 },
    { id: 'weather', label: 'Weather', available: Boolean(availability.weather), weightPct: 20 },
    { id: 'menu', label: 'Menu context', available: Boolean(availability.menu), weightPct: 20 },
    { id: 'calendar', label: 'Academic calendar', available: Boolean(availability.calendar), weightPct: 10 },
  ];

  const signalCoveragePct = signals.reduce(
    (total, signal) => total + (signal.available ? signal.weightPct : 0),
    0,
  );
  const scheduleAvailable = signals.find(signal => signal.id === 'schedule')?.available ?? false;

  let decisionReadiness: DecisionReadiness = 'WITHHOLD';
  if (scheduleAvailable && signalCoveragePct >= 70) decisionReadiness = 'PILOT_READY';
  else if (scheduleAvailable && signalCoveragePct >= 50) decisionReadiness = 'REVIEW_REQUIRED';

  // Uncertainty expands when contextual signals are missing. The band remains decision support,
  // never measured cafeteria demand, and can never bypass the human operator gate.
  const lowerFactor = signalCoveragePct >= 80 ? 0.96 : signalCoveragePct >= 60 ? 0.93 : 0.9;
  const upperFactor = signalCoveragePct >= 80 ? 1.06 : signalCoveragePct >= 60 ? 1.09 : 1.13;
  const reasonCodes = signals.filter(signal => !signal.available).map(signal => `MISSING_${signal.id.toUpperCase()}`);
  if (decisionReadiness === 'WITHHOLD') reasonCodes.unshift('INSUFFICIENT_DECISION_CONTEXT');
  if (decisionReadiness === 'REVIEW_REQUIRED') reasonCodes.unshift('CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED');

  return {
    predictedMeals: demand,
    lowerBound: Math.max(0, Math.round(demand * lowerFactor)),
    recommendedTarget: demand,
    upperBound: Math.round(demand * upperFactor),
    signalCoveragePct,
    decisionReadiness,
    operatorApprovalRequired: true,
    autoDispatchAllowed: false,
    provenance: 'MODEL_ESTIMATE',
    signals,
    reasonCodes,
  };
}

export function wasteKgPer100Served(wasteKg: number, servedPortions: number) {
  if (servedPortions <= 0) return null;
  return (Math.max(0, wasteKg) / servedPortions) * 100;
}

export function overproductionRatePct(producedPortions: number, servedPortions: number) {
  if (producedPortions <= 0) return null;
  return (Math.max(0, producedPortions - servedPortions) / producedPortions) * 100;
}

export function pilotWasteReductionPct(controlWastePer100: number, interventionWastePer100: number) {
  if (controlWastePer100 <= 0) return null;
  return ((controlWastePer100 - interventionWastePer100) / controlWastePer100) * 100;
}
