import {
  FOOD_WASTE_PILOT_PROTOCOL,
  validatePilotMeasurement,
  type PilotServiceMeasurement,
} from '@/lib/food-waste';

export type MatchedPilotServiceMeasurement = PilotServiceMeasurement & {
  pairId: string;
};

export type MatchedPilotDesignSummary = {
  matchedPairCount: number;
  pairCount: number;
  missingPairIdRows: number[];
  incompletePairIds: string[];
  duplicatePairArmKeys: string[];
  structurePassed: boolean;
};

export const MATCHED_FOOD_WASTE_PILOT_PROTOCOL = {
  ...FOOD_WASTE_PILOT_PROTOCOL,
  version: '1.2',
  measurementFields: [
    'pair_id',
    ...FOOD_WASTE_PILOT_PROTOCOL.measurementFields,
  ],
  successGate: {
    ...FOOD_WASTE_PILOT_PROTOCOL.successGate,
    minimumMatchedPairs: FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm,
  },
  matchingRule: 'Each pair_id must contain exactly one CONTROL service and one INTERVENTION service.',
  evidenceBoundary: `${FOOD_WASTE_PILOT_PROTOCOL.evidenceBoundary} Unmatched services cannot be promoted as matched-pilot evidence.`,
} as const;

function field(record: Record<string, unknown>, camelCase: string, snakeCase: string) {
  return record[camelCase] ?? record[snakeCase];
}

function stringField(record: Record<string, unknown>, camelCase: string, snakeCase: string) {
  const value = field(record, camelCase, snakeCase);
  return typeof value === 'string' ? value : '';
}

export function normalizeMatchedPilotMeasurement(candidate: Record<string, unknown>) {
  return {
    pairId: stringField(candidate, 'pairId', 'pair_id'),
    date: typeof candidate.date === 'string' ? candidate.date : '',
    serviceId: stringField(candidate, 'serviceId', 'service_id'),
    arm: candidate.arm,
    modelForecastMeals: field(candidate, 'modelForecastMeals', 'model_forecast_meals') ?? null,
    producedPortions: field(candidate, 'producedPortions', 'produced_portions'),
    servedPortions: field(candidate, 'servedPortions', 'served_portions'),
    edibleSurplusKg: field(candidate, 'edibleSurplusKg', 'edible_surplus_kg'),
    wasteKg: field(candidate, 'wasteKg', 'waste_kg'),
    earlySellout: field(candidate, 'earlySellout', 'early_sellout'),
    operatorOverride: field(candidate, 'operatorOverride', 'operator_override'),
    notes: candidate.notes,
  } as unknown as MatchedPilotServiceMeasurement;
}

export function validateMatchedPilotMeasurement(measurement: MatchedPilotServiceMeasurement) {
  const errors = validatePilotMeasurement(measurement);
  if (!measurement.pairId.trim()) {
    errors.push('pairId is required for matched-pilot evaluation');
  }
  return errors;
}

export function analyzeMatchedPilotDesign(
  measurements: MatchedPilotServiceMeasurement[],
): MatchedPilotDesignSummary {
  const missingPairIdRows: number[] = [];
  const pairArms = new Map<string, Set<'CONTROL' | 'INTERVENTION'>>();
  const seenPairArm = new Set<string>();
  const duplicatePairArmKeys = new Set<string>();

  measurements.forEach((measurement, index) => {
    const pairId = measurement.pairId.trim();
    if (!pairId) {
      missingPairIdRows.push(index);
      return;
    }
    if (measurement.arm !== 'CONTROL' && measurement.arm !== 'INTERVENTION') return;

    const pairArmKey = `${pairId}|${measurement.arm}`;
    if (seenPairArm.has(pairArmKey)) duplicatePairArmKeys.add(pairArmKey);
    seenPairArm.add(pairArmKey);

    const arms = pairArms.get(pairId) ?? new Set<'CONTROL' | 'INTERVENTION'>();
    arms.add(measurement.arm);
    pairArms.set(pairId, arms);
  });

  const incompletePairIds = [...pairArms.entries()]
    .filter(([, arms]) => !arms.has('CONTROL') || !arms.has('INTERVENTION'))
    .map(([pairId]) => pairId)
    .sort();
  const matchedPairCount = [...pairArms.values()]
    .filter(arms => arms.has('CONTROL') && arms.has('INTERVENTION'))
    .length;

  return {
    matchedPairCount,
    pairCount: pairArms.size,
    missingPairIdRows,
    incompletePairIds,
    duplicatePairArmKeys: [...duplicatePairArmKeys].sort(),
    structurePassed:
      missingPairIdRows.length === 0
      && incompletePairIds.length === 0
      && duplicatePairArmKeys.size === 0,
  };
}
