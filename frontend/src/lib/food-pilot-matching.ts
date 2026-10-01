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

export function validateMatchedPilotMeasurement(measurement: MatchedPilotServiceMeasurement) {
  const errors = validatePilotMeasurement(measurement);
  if (typeof measurement.pairId !== 'string' || !measurement.pairId.trim()) {
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
    const pairId = typeof measurement.pairId === 'string' ? measurement.pairId.trim() : '';
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
