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

export type PilotArmSummary = {
  measuredServices: number;
  meanWasteKgPer100Served: number | null;
  meanWasteKgPerService: number | null;
  meanOverproductionRatePct: number | null;
  meanEdibleSurplusKgPer100Served: number | null;
  meanForecastApePct: number | null;
  earlySelloutRatePct: number | null;
  operatorOverrideRatePct: number | null;
};

export type PilotScorecardStatus = 'INSUFFICIENT_EVIDENCE' | 'PROMISING' | 'FAILED';

export type PilotScorecard = {
  status: PilotScorecardStatus;
  control: PilotArmSummary;
  intervention: PilotArmSummary;
  normalizedWasteReductionPct: number | null;
  gates: {
    enoughEvidence: boolean;
    wasteReductionTargetMet: boolean | null;
    earlySelloutGuardrailPassed: boolean | null;
    foodSafetyManualReviewRequired: true;
  };
  notes: string[];
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

function mean(values: Array<number | null>) {
  const usable = values.filter((value): value is number => value != null && Number.isFinite(value));
  if (!usable.length) return null;
  return usable.reduce((sum, value) => sum + value, 0) / usable.length;
}

function roundMetric(value: number | null, digits = 2) {
  if (value == null) return null;
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
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

export function validatePilotMeasurement(measurement: PilotServiceMeasurement) {
  const errors: string[] = [];
  if (!measurement.date) errors.push('date is required');
  if (!measurement.serviceId) errors.push('serviceId is required');
  if (measurement.arm !== 'CONTROL' && measurement.arm !== 'INTERVENTION') errors.push('arm must be CONTROL or INTERVENTION');
  if (!Number.isFinite(measurement.producedPortions) || measurement.producedPortions < 0) errors.push('producedPortions must be >= 0');
  if (!Number.isFinite(measurement.servedPortions) || measurement.servedPortions <= 0) errors.push('servedPortions must be > 0');
  if (!Number.isFinite(measurement.edibleSurplusKg) || measurement.edibleSurplusKg < 0) errors.push('edibleSurplusKg must be >= 0');
  if (!Number.isFinite(measurement.wasteKg) || measurement.wasteKg < 0) errors.push('wasteKg must be >= 0');
  if (measurement.modelForecastMeals != null && (!Number.isFinite(measurement.modelForecastMeals) || measurement.modelForecastMeals < 0)) errors.push('modelForecastMeals must be null or >= 0');
  return errors;
}

function summarizePilotArm(measurements: PilotServiceMeasurement[]): PilotArmSummary {
  const wastePer100 = measurements.map(item => wasteKgPer100Served(item.wasteKg, item.servedPortions));
  const overproduction = measurements.map(item => overproductionRatePct(item.producedPortions, item.servedPortions));
  const surplusPer100 = measurements.map(item => item.servedPortions > 0 ? (item.edibleSurplusKg / item.servedPortions) * 100 : null);
  const forecastApe = measurements.map(item => {
    if (item.modelForecastMeals == null || item.servedPortions <= 0) return null;
    return (Math.abs(item.modelForecastMeals - item.servedPortions) / item.servedPortions) * 100;
  });
  const earlySelloutRate = measurements.length
    ? (measurements.filter(item => item.earlySellout).length / measurements.length) * 100
    : null;
  const overrideRate = measurements.length
    ? (measurements.filter(item => item.operatorOverride).length / measurements.length) * 100
    : null;

  return {
    measuredServices: measurements.length,
    meanWasteKgPer100Served: roundMetric(mean(wastePer100)),
    meanWasteKgPerService: roundMetric(mean(measurements.map(item => item.wasteKg))),
    meanOverproductionRatePct: roundMetric(mean(overproduction)),
    meanEdibleSurplusKgPer100Served: roundMetric(mean(surplusPer100)),
    meanForecastApePct: roundMetric(mean(forecastApe)),
    earlySelloutRatePct: roundMetric(earlySelloutRate),
    operatorOverrideRatePct: roundMetric(overrideRate),
  };
}

export function scoreFoodWastePilot(measurements: PilotServiceMeasurement[]): PilotScorecard {
  const controlMeasurements = measurements.filter(item => item.arm === 'CONTROL');
  const interventionMeasurements = measurements.filter(item => item.arm === 'INTERVENTION');
  const control = summarizePilotArm(controlMeasurements);
  const intervention = summarizePilotArm(interventionMeasurements);
  const minimum = FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm;
  const enoughEvidence = control.measuredServices >= minimum && intervention.measuredServices >= minimum;

  const reduction = control.meanWasteKgPer100Served != null && intervention.meanWasteKgPer100Served != null
    ? pilotWasteReductionPct(control.meanWasteKgPer100Served, intervention.meanWasteKgPer100Served)
    : null;
  const normalizedWasteReductionPct = roundMetric(reduction);
  const wasteReductionTargetMet = normalizedWasteReductionPct == null
    ? null
    : normalizedWasteReductionPct >= FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct;
  const earlySelloutGuardrailPassed = control.earlySelloutRatePct == null || intervention.earlySelloutRatePct == null
    ? null
    : intervention.earlySelloutRatePct <= control.earlySelloutRatePct;

  const notes: string[] = [];
  if (!enoughEvidence) notes.push(`Need at least ${minimum} measured services in both CONTROL and INTERVENTION arms.`);
  if (wasteReductionTargetMet === false) notes.push('Pre-registered normalized waste-reduction target was not met.');
  if (earlySelloutGuardrailPassed === false) notes.push('Early-sellout incidence increased in the intervention arm.');
  notes.push('Food-safety compliance requires manual operational review and cannot be inferred from service-level numeric fields alone.');

  let status: PilotScorecardStatus = 'INSUFFICIENT_EVIDENCE';
  if (enoughEvidence) {
    status = wasteReductionTargetMet === true && earlySelloutGuardrailPassed === true ? 'PROMISING' : 'FAILED';
  }

  return {
    status,
    control,
    intervention,
    normalizedWasteReductionPct,
    gates: {
      enoughEvidence,
      wasteReductionTargetMet,
      earlySelloutGuardrailPassed,
      foodSafetyManualReviewRequired: true,
    },
    notes,
  };
}
