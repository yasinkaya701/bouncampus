import assert from 'node:assert/strict';
import { validatePilotMeasurement, scoreFoodWastePilot } from '../src/lib/food-waste.ts';

const control = {
  date: '2026-10-08',
  serviceId: 'CALENDAR_CONTROL',
  arm: 'CONTROL',
  modelForecastMeals: null,
  producedPortions: 110,
  servedPortions: 100,
  edibleSurplusKg: 2,
  wasteKg: 5,
  earlySellout: false,
  operatorOverride: false,
};

for (const date of [
  '2026-02-30',
  '2025-02-29',
  '1900-02-29',
  '2026-04-31',
  '2026-13-01',
  '2026-00-01',
  '2026-10-00',
  '0000-01-01',
  '2026-1-08',
]) {
  const errors = validatePilotMeasurement({ ...control, date });
  assert.ok(errors.some(message => message.includes('valid YYYY-MM-DD calendar date')),
    `invalid calendar date ${date} must fail closed`);
}

for (const date of ['2024-02-29', '2000-02-29', '2026-10-08', '2026-12-31']) {
  assert.deepEqual(validatePilotMeasurement({ ...control, date }), [],
    `valid Gregorian date ${date} should be accepted`);
}

const bad = { ...control, date: '2026-02-30' };
const intervention = { ...control, serviceId: 'CALENDAR_INTERVENTION',
  arm: 'INTERVENTION', modelForecastMeals: 100 };
const scorecard = scoreFoodWastePilot([bad, intervention]);
assert.equal(scorecard.dataQuality.invalidMeasurementCount, 1);
assert.equal(scorecard.gates.dataQualityPassed, false);
assert.equal(scorecard.status, 'INSUFFICIENT_EVIDENCE');
console.log('pilot calendar date validity and fail-closed scoring tests passed');
