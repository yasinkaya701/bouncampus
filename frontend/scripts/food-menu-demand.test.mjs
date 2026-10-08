import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import {
  applyMenuDemandAdjustment,
  buildMenuDemandAdjustment,
} from '../src/lib/decision-intelligence/food-menu-demand.ts';

const here = dirname(fileURLToPath(import.meta.url));
const frontendRoot = resolve(here, '..');
const repoRoot = resolve(frontendRoot, '..');

const popular = buildMenuDemandAdjustment(
  {
    mainDish: 'Köfte',
    soup: 'Mercimek Çorbası',
    veganDish: 'Nohut',
  },
  true,
);
const lowerAppeal = buildMenuDemandAdjustment(
  {
    mainDish: 'Kuru Fasulye',
    soup: 'Bamya Çorbası',
    veganDish: 'Nohut',
  },
  true,
);
const unverified = buildMenuDemandAdjustment(
  {
    mainDish: 'Köfte',
    soup: 'Mercimek Çorbası',
    veganDish: 'Nohut',
  },
  false,
);

assert.ok(popular.factor > 1, `popular menu factor should exceed 1, got ${popular.factor}`);
assert.ok(lowerAppeal.factor < popular.factor, 'lower-appeal menu must produce less demand than popular menu');
assert.equal(unverified.factor, 1, 'unverified menu must not change demand');
assert.equal(unverified.provenance, 'UNAVAILABLE');
assert.ok(applyMenuDemandAdjustment(1000, popular.factor) > 1000);
assert.ok(applyMenuDemandAdjustment(1000, lowerAppeal.factor) < applyMenuDemandAdjustment(1000, popular.factor));
assert.ok(popular.matchedItems.includes('Köfte'));
assert.ok(popular.matchedItems.includes('Mercimek Çorbası'));

const backendCatalog = JSON.parse(
  readFileSync(resolve(repoRoot, 'backend/app/data/menu_popularity.json'), 'utf8'),
);
const frontendCatalog = JSON.parse(
  readFileSync(resolve(frontendRoot, 'src/data/menu_popularity.json'), 'utf8'),
);
assert.deepEqual(frontendCatalog, backendCatalog, 'frontend menu popularity catalog must stay in sync with backend policy data');

const dashboardRoute = readFileSync(resolve(frontendRoot, 'src/app/api/v1/dashboard/route.ts'), 'utf8');
assert.match(dashboardRoute, /buildMenuDemandAdjustment/);
assert.match(dashboardRoute, /food_demand_baseline_meals/);
assert.match(dashboardRoute, /food_menu_adjustment/);

import { parseFoodScenarioRate } from '../src/lib/food-scenario-query.ts';

assert.equal(parseFoodScenarioRate(null, 15), 15, 'omitted prevention rate uses the documented default');
assert.equal(parseFoodScenarioRate(null, 85), 85, 'omitted recovery rate uses the documented default');
assert.equal(parseFoodScenarioRate('0', 15), 0, 'explicit zero remains valid');
assert.equal(parseFoodScenarioRate('  22.5  ', 15), 22.5, 'finite fractional rates stay valid');
assert.equal(parseFoodScenarioRate('-10', 15), -10, 'existing scenario clamp still handles out-of-range finite inputs');
for (const invalid of ['', '   ', 'not-a-number', 'NaN', 'Infinity', '-Infinity', '1e309']) {
  assert.equal(parseFoodScenarioRate(invalid, 15), null,
    `invalid scenario query value ${JSON.stringify(invalid)} must be rejected`);
}

const foodRoute = readFileSync(resolve(frontendRoot, 'src/app/api/v1/food/route.ts'), 'utf8');
assert.match(foodRoute, /parseFoodScenarioRate/);
assert.match(foodRoute, /INVALID_SCENARIO_RATE/);
assert.match(foodRoute, /planningCandidate/);
assert.match(foodRoute, /diagnosticProductionBand/);
assert.match(foodRoute, /recommendedTarget:\s*sourceAssessment\.predictedMeals/);
assert.match(foodRoute, /ADVISORY_MODEL_ESTIMATE_NOT_AUTHORIZED_KITCHEN_ORDER/);

// The operator surface must keep a diagnostic portion candidate visible while
// preserving the non-actionable WITHHOLD/approval boundary for sandbox methods.
const page = readFileSync(resolve(frontendRoot, 'src/app/food-waste/page.tsx'), 'utf8');
assert.match(page, /planningCandidate/);
assert.match(page, /Planlama adayı/);
assert.match(page, /advisoryOnly/);
assert.match(page, /demandContext\.actionable/);
assert.match(page, /decisionReadiness/);

console.log('food menu-demand product wiring tests passed');
