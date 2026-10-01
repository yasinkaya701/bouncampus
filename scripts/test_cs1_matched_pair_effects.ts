#!/usr/bin/env node
import assert from 'node:assert/strict';
import { summarizeMatchedPilotEffects } from '../frontend/src/lib/food-pilot-pair-effects.ts';

const measurements = [
  { pairId: 'A', arm: 'CONTROL' as const, servedPortions: 100, wasteKg: 10, earlySellout: false },
  { pairId: 'A', arm: 'INTERVENTION' as const, servedPortions: 100, wasteKg: 2, earlySellout: false },
  { pairId: 'B', arm: 'CONTROL' as const, servedPortions: 100, wasteKg: 2, earlySellout: false },
  { pairId: 'B', arm: 'INTERVENTION' as const, servedPortions: 100, wasteKg: 6, earlySellout: true },
];

const summary = summarizeMatchedPilotEffects(measurements);
assert.equal(summary.matchedPairCount, 2);
assert.equal(summary.meanControlWasteKgPer100Served, 6);
assert.equal(summary.meanInterventionWasteKgPer100Served, 4);
assert.equal(summary.meanPairedWasteDeltaKgPer100Served, 2);
assert.equal(summary.normalizedWasteReductionPct, 33.33);
assert.equal(summary.improvedWastePairCount, 1);
assert.equal(summary.worsenedWastePairCount, 1);
assert.equal(summary.unchangedWastePairCount, 0);
assert.equal(summary.earlySelloutWorsenedPairCount, 1);
assert.deepEqual(
  summary.pairs.map(pair => [pair.pairId, pair.wasteDeltaKgPer100Served, pair.earlySelloutDirection]),
  [
    ['A', 8, 'UNCHANGED'],
    ['B', -4, 'WORSENED'],
  ],
);
assert.equal(summary.resultScope, 'MATCHED_PILOT_PAIR_EFFECTS_ONLY');
assert.equal(summary.generalizedImpactClaimAllowed, false);

// Same arm marginals, different pairing: pair heterogeneity must change even though
// the aggregate normalized reduction remains the same.
const rematched = summarizeMatchedPilotEffects([
  { pairId: 'A', arm: 'CONTROL' as const, servedPortions: 100, wasteKg: 10, earlySellout: false },
  { pairId: 'A', arm: 'INTERVENTION' as const, servedPortions: 100, wasteKg: 6, earlySellout: true },
  { pairId: 'B', arm: 'CONTROL' as const, servedPortions: 100, wasteKg: 2, earlySellout: false },
  { pairId: 'B', arm: 'INTERVENTION' as const, servedPortions: 100, wasteKg: 2, earlySellout: false },
]);
assert.equal(rematched.normalizedWasteReductionPct, 33.33);
assert.equal(rematched.improvedWastePairCount, 1);
assert.equal(rematched.worsenedWastePairCount, 0);
assert.equal(rematched.unchangedWastePairCount, 1);
assert.deepEqual(rematched.pairs.map(pair => pair.wasteDeltaKgPer100Served), [4, 0]);

console.log('PASS matched-pair effect semantics');
