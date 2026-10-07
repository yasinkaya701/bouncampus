import assert from 'node:assert/strict';
import { scoreFoodWastePilot } from '../src/lib/food-waste.ts';

// These are deterministic synthetic regression fixtures, not observed pilot results.
function matchedFixture(controlWasteKg, interventionWasteKg) {
  return Array.from({ length: 5 }, (_, index) => {
    const base = {
      date: '2026-10-08',
      serviceId: `CONTROL_${index}`,
      arm: 'CONTROL',
      modelForecastMeals: null,
      producedPortions: 110,
      servedPortions: 100,
      edibleSurplusKg: 0,
      wasteKg: controlWasteKg,
      earlySellout: false,
      operatorOverride: false,
    };
    return [
      base,
      {
        ...base,
        serviceId: `INTERVENTION_${index}`,
        arm: 'INTERVENTION',
        modelForecastMeals: 100,
        wasteKg: interventionWasteKg,
      },
    ];
  }).flat();
}

// The former code rounded mean rates to 1.00 and 0.90 BEFORE comparing,
// thereby promoting a true 9.96% reduction as if it had met the 10% gate.
const belowTarget = scoreFoodWastePilot(matchedFixture(1.004, 0.904));
assert.equal(belowTarget.gates.enoughEvidence, true);
assert.equal(belowTarget.gates.dataQualityPassed, true);
assert.equal(belowTarget.gates.wasteReductionTargetMet, false);
assert.equal(belowTarget.status, 'FAILED');
assert.equal(belowTarget.normalizedWasteReductionPct, 9.96);

// Near-zero waste creates the opposite error: rounding both arms to 0.01
// previously produced zero reduction despite a real 16.67% reduction.
const aboveTarget = scoreFoodWastePilot(matchedFixture(0.006, 0.005));
assert.equal(aboveTarget.gates.wasteReductionTargetMet, true);
assert.equal(aboveTarget.status, 'PROMISING');
assert.equal(aboveTarget.normalizedWasteReductionPct, 16.67);

// Exact boundary must still count as meeting the preregistered target.
const exactTarget = scoreFoodWastePilot(matchedFixture(1, 0.9));
assert.equal(exactTarget.gates.wasteReductionTargetMet, true);
assert.equal(exactTarget.status, 'PROMISING');

// Do not interpret a genuine sub-threshold value as machine roundoff.
const justBelowTarget = scoreFoodWastePilot(matchedFixture(1, 0.9000000001));
assert.equal(justBelowTarget.gates.wasteReductionTargetMet, false);
assert.equal(justBelowTarget.status, 'FAILED');

console.log('pilot waste-reduction full-precision threshold regression passed');
