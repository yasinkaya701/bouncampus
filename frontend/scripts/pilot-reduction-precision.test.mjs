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

// A physical dining service cannot simultaneously be a CONTROL and an
// INTERVENTION observation on the same date. Reusing its identity must
// invalidate evidence even if the arm labels differ.
const uniqueServices = matchedFixture(2, 1);
assert.equal(scoreFoodWastePilot(uniqueServices).gates.dataQualityPassed, true);

const reusedService = uniqueServices.map((item, index) => index === 1
  ? { ...item, serviceId: uniqueServices[0].serviceId }
  : item);
const repeated = scoreFoodWastePilot(reusedService);
assert.equal(repeated.dataQuality.invalidMeasurementCount, 0,
  'both individual rows are otherwise structurally valid');
assert.equal(repeated.gates.dataQualityPassed, false,
  'same-day service identity shared across arms must fail closed');
assert.equal(repeated.gates.enoughEvidence, false);
assert.equal(repeated.status, 'INSUFFICIENT_EVIDENCE');
assert.ok(repeated.dataQuality.duplicateServiceKeys.includes('2026-10-08|CONTROL_0'));

// Whitespace is not a distinct physical service identity. An operator
// accidentally padding an identifier must not bypass cross-arm deduplication.
const paddedService = uniqueServices.map((item, index) => index === 1
  ? { ...item, serviceId: `  ${uniqueServices[0].serviceId}  ` }
  : item);
const paddedScore = scoreFoodWastePilot(paddedService);
assert.equal(paddedScore.gates.dataQualityPassed, false);
assert.equal(paddedScore.status, 'INSUFFICIENT_EVIDENCE');
assert.ok(paddedScore.dataQuality.duplicateServiceKeys.includes('2026-10-08|CONTROL_0'));

// Preserve historical allowance for local service IDs reused on
// *different* dates: identity consists of the date and service ID.
const otherDate = uniqueServices.map((item, index) => index === 1
  ? { ...item, serviceId: uniqueServices[0].serviceId, date: '2026-10-09' }
  : item);
assert.equal(scoreFoodWastePilot(otherDate).gates.dataQualityPassed, true);

// The sell-out guardrail is a strict incidence comparison. Rounding both
// displayed arm percentages to 0.10% must not hide a real increase.
const lowSelloutControl = Array.from({ length: 1001 }, (_, index) => ({
  date: '2026-10-08',
  serviceId: `SELL_CTRL_${index}`,
  arm: 'CONTROL',
  modelForecastMeals: null,
  producedPortions: 110,
  servedPortions: 100,
  edibleSurplusKg: 0,
  wasteKg: 2,
  earlySellout: index === 0,
  operatorOverride: false,
}));
const higherSelloutIntervention = Array.from({ length: 1000 }, (_, index) => ({
  ...lowSelloutControl[0],
  serviceId: `SELL_TEST_${index}`,
  arm: 'INTERVENTION',
  modelForecastMeals: 100,
  wasteKg: 1,
  earlySellout: index === 0,
}));
const guardedScore = scoreFoodWastePilot([...lowSelloutControl, ...higherSelloutIntervention]);
assert.equal(guardedScore.gates.enoughEvidence, true);
assert.equal(guardedScore.gates.wasteReductionTargetMet, true);
assert.equal(guardedScore.control.earlySelloutRatePct, 0.1);
assert.equal(guardedScore.intervention.earlySelloutRatePct, 0.1);
assert.equal(guardedScore.gates.earlySelloutGuardrailPassed, false,
  'a real increased incidence cannot pass through display rounding');
assert.equal(guardedScore.status, 'FAILED');

console.log('pilot waste-reduction full-precision threshold regression passed');
