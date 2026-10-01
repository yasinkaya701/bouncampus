export type MatchedPairEffectMeasurement = {
  pairId: string;
  arm: 'CONTROL' | 'INTERVENTION';
  servedPortions: number;
  wasteKg: number;
  earlySellout: boolean;
};

export type MatchedPairWasteEffect = {
  pairId: string;
  controlWasteKgPer100Served: number;
  interventionWasteKgPer100Served: number;
  wasteDeltaKgPer100Served: number;
  wasteDirection: 'IMPROVED' | 'WORSENED' | 'UNCHANGED';
  earlySelloutDirection: 'IMPROVED' | 'WORSENED' | 'UNCHANGED';
};

export type MatchedPilotEffectSummary = {
  matchedPairCount: number;
  meanControlWasteKgPer100Served: number | null;
  meanInterventionWasteKgPer100Served: number | null;
  meanPairedWasteDeltaKgPer100Served: number | null;
  medianPairedWasteDeltaKgPer100Served: number | null;
  normalizedWasteReductionPct: number | null;
  improvedWastePairCount: number;
  worsenedWastePairCount: number;
  unchangedWastePairCount: number;
  improvedWastePairPct: number | null;
  earlySelloutImprovedPairCount: number;
  earlySelloutWorsenedPairCount: number;
  pairs: MatchedPairWasteEffect[];
  resultScope: 'MATCHED_PILOT_PAIR_EFFECTS_ONLY';
  generalizedImpactClaimAllowed: false;
};

function roundMetric(value: number, digits = 2) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function mean(values: number[]) {
  if (!values.length) return null;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function median(values: number[]) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  if (sorted.length % 2) return sorted[middle];
  return (sorted[middle - 1] + sorted[middle]) / 2;
}

function wasteKgPer100Served(measurement: MatchedPairEffectMeasurement) {
  if (!Number.isFinite(measurement.servedPortions) || measurement.servedPortions <= 0) {
    throw new Error(`pair ${measurement.pairId}: servedPortions must be > 0`);
  }
  if (!Number.isFinite(measurement.wasteKg) || measurement.wasteKg < 0) {
    throw new Error(`pair ${measurement.pairId}: wasteKg must be finite and >= 0`);
  }
  return (measurement.wasteKg / measurement.servedPortions) * 100;
}

export function summarizeMatchedPilotEffects(
  measurements: MatchedPairEffectMeasurement[],
): MatchedPilotEffectSummary {
  const pairsById = new Map<
    string,
    Partial<Record<'CONTROL' | 'INTERVENTION', MatchedPairEffectMeasurement>>
  >();

  for (const measurement of measurements) {
    const pairId = measurement.pairId.trim();
    if (!pairId) throw new Error('pairId is required for matched-pair effect calculation');
    if (measurement.arm !== 'CONTROL' && measurement.arm !== 'INTERVENTION') {
      throw new Error(`pair ${pairId}: unsupported arm`);
    }
    if (typeof measurement.earlySellout !== 'boolean') {
      throw new Error(`pair ${pairId}: earlySellout must be boolean`);
    }
    // Validate numeric fields before inserting so malformed rows cannot enter a pair.
    wasteKgPer100Served({ ...measurement, pairId });

    const pair = pairsById.get(pairId) ?? {};
    if (pair[measurement.arm]) {
      throw new Error(`pair ${pairId}: duplicate ${measurement.arm} row`);
    }
    pair[measurement.arm] = { ...measurement, pairId };
    pairsById.set(pairId, pair);
  }

  const pairs: MatchedPairWasteEffect[] = [];
  const rawControlValues: number[] = [];
  const rawInterventionValues: number[] = [];
  const rawDeltas: number[] = [];

  for (const pairId of [...pairsById.keys()].sort()) {
    const pair = pairsById.get(pairId)!;
    const control = pair.CONTROL;
    const intervention = pair.INTERVENTION;
    if (!control || !intervention) {
      throw new Error(`pair ${pairId}: exactly one CONTROL and one INTERVENTION row are required`);
    }

    const controlWaste = wasteKgPer100Served(control);
    const interventionWaste = wasteKgPer100Served(intervention);
    const delta = controlWaste - interventionWaste;
    rawControlValues.push(controlWaste);
    rawInterventionValues.push(interventionWaste);
    rawDeltas.push(delta);

    const wasteDirection = delta > 0 ? 'IMPROVED' : delta < 0 ? 'WORSENED' : 'UNCHANGED';
    const earlySelloutDirection =
      control.earlySellout === intervention.earlySellout
        ? 'UNCHANGED'
        : control.earlySellout && !intervention.earlySellout
          ? 'IMPROVED'
          : 'WORSENED';

    pairs.push({
      pairId,
      controlWasteKgPer100Served: roundMetric(controlWaste),
      interventionWasteKgPer100Served: roundMetric(interventionWaste),
      wasteDeltaKgPer100Served: roundMetric(delta),
      wasteDirection,
      earlySelloutDirection,
    });
  }

  const controlMean = mean(rawControlValues);
  const interventionMean = mean(rawInterventionValues);
  const deltaMean = mean(rawDeltas);
  const deltaMedian = median(rawDeltas);
  const normalizedReduction =
    controlMean != null && controlMean > 0 && interventionMean != null
      ? ((controlMean - interventionMean) / controlMean) * 100
      : null;
  const improvedWastePairCount = pairs.filter(pair => pair.wasteDirection === 'IMPROVED').length;
  const worsenedWastePairCount = pairs.filter(pair => pair.wasteDirection === 'WORSENED').length;
  const unchangedWastePairCount = pairs.length - improvedWastePairCount - worsenedWastePairCount;

  return {
    matchedPairCount: pairs.length,
    meanControlWasteKgPer100Served: controlMean == null ? null : roundMetric(controlMean),
    meanInterventionWasteKgPer100Served:
      interventionMean == null ? null : roundMetric(interventionMean),
    meanPairedWasteDeltaKgPer100Served: deltaMean == null ? null : roundMetric(deltaMean),
    medianPairedWasteDeltaKgPer100Served: deltaMedian == null ? null : roundMetric(deltaMedian),
    normalizedWasteReductionPct:
      normalizedReduction == null ? null : roundMetric(normalizedReduction),
    improvedWastePairCount,
    worsenedWastePairCount,
    unchangedWastePairCount,
    improvedWastePairPct:
      pairs.length ? roundMetric((improvedWastePairCount / pairs.length) * 100) : null,
    earlySelloutImprovedPairCount: pairs.filter(
      pair => pair.earlySelloutDirection === 'IMPROVED',
    ).length,
    earlySelloutWorsenedPairCount: pairs.filter(
      pair => pair.earlySelloutDirection === 'WORSENED',
    ).length,
    pairs,
    resultScope: 'MATCHED_PILOT_PAIR_EFFECTS_ONLY',
    generalizedImpactClaimAllowed: false,
  };
}
