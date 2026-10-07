import assert from 'node:assert/strict';
import { validatePilotMeasurement } from '../src/lib/food-waste.ts';

const valid = {
  date: '2024-02-29',
  serviceId: 'LEAP_YEAR_CONTROL',
  arm: 'CONTROL',
  modelForecastMeals: null,
  producedPortions: 110,
  servedPortions: 100,
  edibleSurplusKg: 2,
  wasteKg: 6,
  earlySellout: false,
  operatorOverride: false,
  notes: '',
};

assert.deepEqual(validatePilotMeasurement(valid), [], 'valid leap day must be accepted');

for (const date of [
  '2025-02-29',
  '2026-02-30',
  '2026-04-31',
  '2026-00-10',
  '2026-13-10',
  '2026-10-00',
  '2026-10-32',
  '2026-1-08',
]) {
  const errors = validatePilotMeasurement({ ...valid, date });
  assert.ok(errors.some(message => message.includes('date must be a real YYYY-MM-DD calendar date')),
    `invalid calendar date ${date} must be rejected`);
}

assert.deepEqual(validatePilotMeasurement({ ...valid, date: '2028-02-29' }), [],
  'subsequent leap day must remain valid');
assert.ok(validatePilotMeasurement({ ...valid, date: '2100-02-29' }).length > 0,
  'century years not divisible by 400 are not leap years');
assert.deepEqual(validatePilotMeasurement({ ...valid, date: '2000-02-29' }), [],
  'century years divisible by 400 are leap years');

console.log('pilot service calendar-date validation passed');
