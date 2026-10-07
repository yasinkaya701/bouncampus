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
export type DecisionReadiness = 'PILOT_READY' | 'REVIEW_REQUIRED' | 'WITHHOLD';

export type DemandSignal = {
  id: DemandSignalId;
  label: string;
  available: boolean;
  weightPct: number;
  weightBasis: 'POLICY_HEURISTIC';
};

export type ProductionDecisionBand = {
  policyVersion: string;
  predictedMeals: number;
  lowerBound: number;
  recommendedTarget: number | null;
  upperBound: number;
  signalCoveragePct: number;
  decisionReadiness: DecisionReadiness;
  abstained: boolean;
  operatorApprovalRequired: true;
  autoDispatchAllowed: false;
  provenance: 'MODEL_ESTIMATE';
  decisionProvenance: 'POLICY_HEURISTIC';
  bandSemantics: 'PLANNING_RANGE_NOT_CALIBRATED_INTERVAL';
  calibrationStatus: 'NOT_CALIBRATED';
  signals: DemandSignal[];
  reasonCodes: string[];
  limitations: string[];
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
    dataQualityPassed: boolean;
    wasteReductionTargetMet: boolean | null;
    earlySelloutGuardrailPassed: boolean | null;
    foodSafetyManualReviewRequired: true;
  };
  dataQuality: {
    invalidMeasurementCount: number;
    duplicateServiceKeys: string[];
    interventionForecastCoveragePct: number | null;
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

export const FOOD_DECISION_POLICY = {
  version: 'food-decision-v1.1',
  provenance: 'POLICY_HEURISTIC' as const,
  forecastProvenance: 'MODEL_ESTIMATE' as const,
  bandSemantics: 'PLANNING_RANGE_NOT_CALIBRATED_INTERVAL' as const,
  calibrationStatus: 'NOT_CALIBRATED' as const,
  signalWeightsPct: {
    schedule: 50,
    weather: 20,
    menu: 20,
    calendar: 10,
  } satisfies Record<DemandSignalId, number>,
  requiredSignals: ['schedule'] as const,
  reviewMinCoveragePct: 50,
  pilotReadyMinCoveragePct: 70,
  operatorApprovalRequired: true as const,
  autoDispatchAllowed: false as const,
  limitations: [
    'NO_CAFETERIA_POS_OR_SERVED_MEAL_TELEMETRY',
    'HEURISTIC_BAND_NOT_CALIBRATED',
    'PILOT_OUTCOMES_NOT_YET_MEASURED',
  ],
};

export const FOOD_WASTE_PILOT_PROTOCOL = {
  version: '1.1',
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
    minimumInterventionForecastCoveragePct: 100,
    serviceGuardrail: 'No increase in early-sellout incidence versus the matched control arm.',
    safetyGuardrail: 'No food-safety process may be bypassed by a production recommendation.',
    interpretation: 'The 10% reduction is a pre-registered pilot target, not an achieved result.',
  },
  evidenceBoundary: 'PROMISING is pilot evidence only; it is not a generalized climate-impact or savings claim.',
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

function planningFactors(signalCoveragePct: number) {
  if (signalCoveragePct >= 80) return { lower: 0.96, upper: 1.06 };
  if (signalCoveragePct >= 60) return { lower: 0.93, upper: 1.09 };
  return { lower: 0.9, upper: 1.13 };
}

export function buildProductionBand(
  predictedMeals: number,
  availability: Partial<Record<DemandSignalId, boolean>> = {},
): ProductionDecisionBand {
  const demand = Number.isFinite(predictedMeals) && predictedMeals > 0
    ? Math.max(0, Math.round(predictedMeals))
    : 0;

  const labels: Record<DemandSignalId, string> = {
    schedule: 'Course schedule',
    weather: 'Weather',
    menu: 'Menu context',
    calendar: 'Academic calendar',
  };
  const signals = (Object.keys(FOOD_DECISION_POLICY.signalWeightsPct) as DemandSignalId[]).map(id => ({
    id,
    label: labels[id],
    available: Boolean(availability[id]),
    weightPct: FOOD_DECISION_POLICY.signalWeightsPct[id],
    weightBasis: FOOD_DECISION_POLICY.provenance,
  }));

  const signalCoveragePct = signals.reduce(
    (total, signal) => total + (signal.available ? signal.weightPct : 0),
    0,
  );
  const scheduleAvailable = signals.find(signal => signal.id === 'schedule')?.available ?? false;

  let decisionReadiness: DecisionReadiness = 'WITHHOLD';
  if (demand <= 0) decisionReadiness = 'WITHHOLD';
  else if (!scheduleAvailable) decisionReadiness = 'WITHHOLD';
  else if (signalCoveragePct >= FOOD_DECISION_POLICY.pilotReadyMinCoveragePct) decisionReadiness = 'PILOT_READY';
  else if (signalCoveragePct >= FOOD_DECISION_POLICY.reviewMinCoveragePct) decisionReadiness = 'REVIEW_REQUIRED';

  const factors = planningFactors(signalCoveragePct);
  const reasonCodes = ['HEURISTIC_BAND_NOT_CALIBRATED'];
  reasonCodes.push(
    ...signals
      .filter(signal => !signal.available)
      .map(signal => `MISSING_${signal.id.toUpperCase()}`),
  );
  if (demand <= 0) reasonCodes.unshift('NO_POSITIVE_DEMAND_ESTIMATE');
  else if (!scheduleAvailable) reasonCodes.unshift('MISSING_REQUIRED_SCHEDULE');
  else if (decisionReadiness === 'REVIEW_REQUIRED') reasonCodes.unshift('CONTEXT_PARTIAL_OPERATOR_REVIEW_REQUIRED');
  else if (decisionReadiness === 'WITHHOLD') reasonCodes.unshift('INSUFFICIENT_DECISION_CONTEXT');

  const abstained = decisionReadiness === 'WITHHOLD';

  return {
    policyVersion: FOOD_DECISION_POLICY.version,
    predictedMeals: demand,
    lowerBound: Math.max(0, Math.round(demand * factors.lower)),
    recommendedTarget: abstained ? null : demand,
    upperBound: Math.max(0, Math.round(demand * factors.upper)),
    signalCoveragePct,
    decisionReadiness,
    abstained,
    operatorApprovalRequired: true,
    autoDispatchAllowed: false,
    provenance: FOOD_DECISION_POLICY.forecastProvenance,
    decisionProvenance: FOOD_DECISION_POLICY.provenance,
    bandSemantics: FOOD_DECISION_POLICY.bandSemantics,
    calibrationStatus: FOOD_DECISION_POLICY.calibrationStatus,
    signals,
    reasonCodes,
    limitations: [...FOOD_DECISION_POLICY.limitations],
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

function isValidPilotCalendarDate(value: unknown): boolean {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const year = Number(value.slice(0, 4));
  const month = Number(value.slice(5, 7));
  const day = Number(value.slice(8, 10));
  if (year < 1 || month < 1 || month > 12 || day < 1) return false;
  const leapYear = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const daysInMonth = [31, leapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return day <= daysInMonth[month - 1];
}

export function validatePilotMeasurement(measurement: PilotServiceMeasurement) {
  const errors: string[] = [];
  if (!isValidPilotCalendarDate(measurement.date)) errors.push('date must be a valid YYYY-MM-DD calendar date');
  if (!measurement.serviceId.trim()) errors.push('serviceId is required');
  if (measurement.arm !== 'CONTROL' && measurement.arm !== 'INTERVENTION') errors.push('arm must be CONTROL or INTERVENTION');
  if (!Number.isFinite(measurement.producedPortions) || measurement.producedPortions < 0) errors.push('producedPortions must be >= 0');
  if (!Number.isFinite(measurement.servedPortions) || measurement.servedPortions <= 0) errors.push('servedPortions must be > 0');
  if (
    Number.isFinite(measurement.producedPortions)
    && Number.isFinite(measurement.servedPortions)
    && measurement.servedPortions > measurement.producedPortions
  ) errors.push('servedPortions cannot exceed producedPortions');
  if (!Number.isFinite(measurement.edibleSurplusKg) || measurement.edibleSurplusKg < 0) errors.push('edibleSurplusKg must be >= 0');
  if (!Number.isFinite(measurement.wasteKg) || measurement.wasteKg < 0) errors.push('wasteKg must be >= 0');
  if (
    measurement.modelForecastMeals != null
    && (!Number.isFinite(measurement.modelForecastMeals) || measurement.modelForecastMeals < 0)
  ) errors.push('modelForecastMeals must be null or >= 0');
  if (measurement.arm === 'INTERVENTION' && measurement.modelForecastMeals == null) {
    errors.push('INTERVENTION requires modelForecastMeals for decision-support evaluation');
  }
  if (typeof measurement.earlySellout !== 'boolean') errors.push('earlySellout must be boolean');
  if (typeof measurement.operatorOverride !== 'boolean') errors.push('operatorOverride must be boolean');
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
  const invalidMeasurementCount = measurements.filter(item => validatePilotMeasurement(item).length > 0).length;
  const seen = new Set<string>();
  const duplicates = new Set<string>();
  measurements.forEach(item => {
    // A service has one observed arm; arm is not part of its unique identity.
    // Reusing the same dated service in both arms must not create two observations.
    const key = `${item.date}|${item.serviceId}`;
    if (seen.has(key)) duplicates.add(key);
    seen.add(key);
  });

  const controlMeasurements = measurements.filter(item => item.arm === 'CONTROL');
  const interventionMeasurements = measurements.filter(item => item.arm === 'INTERVENTION');
  const control = summarizePilotArm(controlMeasurements);
  const intervention = summarizePilotArm(interventionMeasurements);
  const interventionWithForecast = interventionMeasurements.filter(item => item.modelForecastMeals != null).length;
  const interventionForecastCoveragePct = interventionMeasurements.length
    ? (interventionWithForecast / interventionMeasurements.length) * 100
    : null;
  const minimumForecastCoveragePct = FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumInterventionForecastCoveragePct;

  const dataQualityPassed = invalidMeasurementCount === 0
    && duplicates.size === 0
    && interventionForecastCoveragePct != null
    && interventionForecastCoveragePct >= FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumInterventionForecastCoveragePct;

  const minimum = FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm;
  const enoughEvidence = dataQualityPassed
    && control.measuredServices >= minimum
    && intervention.measuredServices >= minimum;

  // Display summaries are rounded to two decimals. Never use them as inputs
  // to a pre-registered evidence-promotion gate: near-threshold pilots can
  // otherwise be promoted (or rejected) solely because of presentation rounding.
  const controlWastePer100 = mean(controlMeasurements.map(item =>
    wasteKgPer100Served(item.wasteKg, item.servedPortions)));
  const interventionWastePer100 = mean(interventionMeasurements.map(item =>
    wasteKgPer100Served(item.wasteKg, item.servedPortions)));
  const reduction = controlWastePer100 != null && interventionWastePer100 != null
    ? pilotWasteReductionPct(controlWastePer100, interventionWastePer100)
    : null;
  const normalizedWasteReductionPct = roundMetric(reduction);
  // Compare raw means directly. A few floating-point ULPs are needed for
  // mathematically exact thresholds (e.g. an average of 0.9 can be stored as
  // 0.9000000000000001); this is NOT a policy or display-rounding tolerance.
  const targetWastePer100 = controlWastePer100 == null
    ? null
    : controlWastePer100 * (1 - FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct / 100);
  const machineTolerance = targetWastePer100 == null || interventionWastePer100 == null
    ? 0
    : 8 * Number.EPSILON * Math.max(Math.abs(targetWastePer100), Math.abs(interventionWastePer100));
  const wasteReductionTargetMet = reduction == null || targetWastePer100 == null || interventionWastePer100 == null
    ? null
    : interventionWastePer100 <= targetWastePer100 + machineTolerance;
  const earlySelloutGuardrailPassed = control.earlySelloutRatePct == null || intervention.earlySelloutRatePct == null
    ? null
    : intervention.earlySelloutRatePct <= control.earlySelloutRatePct;

  const notes: string[] = [];
  if (invalidMeasurementCount) notes.push(`${invalidMeasurementCount} measurement row(s) fail the pilot measurement contract.`);
  if (duplicates.size) notes.push('Duplicate service rows must be resolved before evidence promotion.');
  if (interventionForecastCoveragePct == null || interventionForecastCoveragePct < minimumForecastCoveragePct) {
    notes.push(`Intervention forecast coverage must be at least ${minimumForecastCoveragePct}% for evidence promotion.`);
  }
  if (!enoughEvidence) notes.push(`Need at least ${minimum} valid measured services in both CONTROL and INTERVENTION arms.`);
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
      dataQualityPassed,
      wasteReductionTargetMet,
      earlySelloutGuardrailPassed,
      foodSafetyManualReviewRequired: true,
    },
    dataQuality: {
      invalidMeasurementCount,
      duplicateServiceKeys: [...duplicates].sort(),
      interventionForecastCoveragePct: roundMetric(interventionForecastCoveragePct),
    },
    notes,
  };
}
