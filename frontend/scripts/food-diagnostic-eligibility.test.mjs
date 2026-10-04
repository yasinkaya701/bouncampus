import assert from 'node:assert/strict';
import { buildProductionBand } from '../src/lib/food-waste.ts';
import { applyMethodEligibility } from '../src/lib/food-decision-eligibility.ts';

const diagnostic = buildProductionBand(1000, {
  schedule: false,
  weather: true,
  menu: true,
  calendar: false,
});

assert.equal(diagnostic.decisionReadiness, 'WITHHOLD');
assert.equal(diagnostic.abstained, true);
assert.equal(
  diagnostic.recommendedTarget,
  1000,
  'source-level diagnostic band should preserve the model point estimate even when source readiness withholds action',
);

const sandbox = applyMethodEligibility(
  buildProductionBand(1000, {
    schedule: true,
    weather: true,
    menu: true,
    calendar: true,
  }),
  { methodEligibility: 'SANDBOX_ONLY' },
);

assert.equal(sandbox.decisionReadiness, 'WITHHOLD');
assert.equal(sandbox.abstained, true);
assert.equal(
  sandbox.recommendedTarget,
  null,
  'method-level SANDBOX_ONLY gate must still remove the actionable recommendation',
);
assert.ok(sandbox.reasonCodes.includes('METHOD_SANDBOX_ONLY'));

console.log('food diagnostic/eligibility boundary tests passed');
