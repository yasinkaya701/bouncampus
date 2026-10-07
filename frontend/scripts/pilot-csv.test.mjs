import assert from 'node:assert/strict';
import { registerHooks } from 'node:module';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Node's native TypeScript stripping does not resolve Next.js @/lib aliases.
// Keep this test dependency-free and load the real application modules.
const frontendRoot = fileURLToPath(new URL('../', import.meta.url));
registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier.startsWith('@/lib/')) {
      const file = resolve(frontendRoot, 'src', specifier.slice(2) + '.ts');
      return nextResolve(pathToFileURL(file).href, context);
    }
    return nextResolve(specifier, context);
  },
});

const { parsePilotCsv, serializePilotCsv, PILOT_CSV_HEADERS } =
  await import('../src/lib/pilot-csv.ts');
const { analyzeMatchedPilotDesign } =
  await import('../src/lib/food-pilot-matching.ts');

const control = {
  pairId: 'PAIR_01',
  date: '2026-10-07',
  serviceId: 'CONTROL_01',
  arm: 'CONTROL',
  modelForecastMeals: null,
  producedPortions: 110,
  servedPortions: 100,
  edibleSurplusKg: 2,
  wasteKg: 6,
  earlySellout: false,
  operatorOverride: false,
  notes: 'Cook said "no"\nand noted leftovers',
};
const intervention = {
  ...control,
  serviceId: 'INTERVENTION_01',
  arm: 'INTERVENTION',
  modelForecastMeals: 104,
  wasteKg: 4,
  notes: '',
};
const pair = [control, intervention];

const csv = serializePilotCsv(pair);
assert.ok(csv.startsWith('pair_id,date,'));
const parsed = parsePilotCsv('\uFEFF' + csv);
assert.deepEqual(parsed.errors, [], 'valid matched pilot CSV should import cleanly');
assert.deepEqual(parsed.measurements, pair, 'import/export must preserve pair ID and escaped notes');
assert.equal(analyzeMatchedPilotDesign(parsed.measurements).structurePassed, true);
assert.deepEqual(parsePilotCsv(serializePilotCsv(parsed.measurements)).measurements, pair);
const crlf = serializePilotCsv([{ ...control, notes: '' }, intervention]).replaceAll('\n', '\r\n');
assert.equal(parsePilotCsv(crlf).measurements.length, 2, 'CRLF input should parse');

const fields = {
  pair_id: 'PAIR_01',
  date: '2026-10-07',
  service_id: 'CONTROL_01',
  arm: 'CONTROL',
  model_forecast_meals: '',
  produced_portions: '110',
  served_portions: '100',
  edible_surplus_kg: '2',
  waste_kg: '6',
  early_sellout: 'false',
  operator_override: 'false',
  notes: '',
};
const asCsv = (values, names = PILOT_CSV_HEADERS) =>
  names.join(',') + '\n' + names.map(name => values[name] ?? '').join(',') + '\n';

{
  const result = parsePilotCsv(asCsv({ ...fields, pair_id: '' }));
  assert.match(result.errors.join(' '), /pairId is required/);
  assert.equal(result.measurements.length, 0);
}
{
  const result = parsePilotCsv(asCsv(fields, PILOT_CSV_HEADERS.filter(name => name !== 'pair_id')));
  assert.match(result.errors.join(' '), /Missing required CSV headers: pair_id/);
}
{
  const result = parsePilotCsv(asCsv({ ...fields, early_sellout: '' }));
  assert.match(result.errors.join(' '), /boolean fields must/);
}
{
  const result = parsePilotCsv(asCsv({ ...fields, waste_kg: '' }));
  assert.match(result.errors.join(' '), /wasteKg must be >= 0/);
}
{
  const result = parsePilotCsv(asCsv({ ...fields, produced_portions: '' }));
  assert.match(result.errors.join(' '), /producedPortions must be >= 0/);
}
{
  const result = parsePilotCsv(asCsv({ ...fields, operator_override: '' }));
  assert.match(result.errors.join(' '), /boolean fields must/);
}
{
  const headers = [...PILOT_CSV_HEADERS, 'pair_id'];
  const result = parsePilotCsv(asCsv(fields, headers));
  assert.match(result.errors.join(' '), /Duplicate CSV headers: pair_id/);
}
{
  const result = parsePilotCsv(asCsv({ ...fields, arm: 'INTERVENTION' }));
  assert.match(result.errors.join(' '), /INTERVENTION requires modelForecastMeals/);
}


{
  const malformed = parsePilotCsv(asCsv({ ...fields, notes: '"unterminated' }));
  assert.match(malformed.errors.join(' '), /Unterminated quoted CSV field/);
  assert.equal(malformed.measurements.length, 0, 'broken quoted records must not enter evidence');
}
{
  const malformed = parsePilotCsv(asCsv({ ...fields, notes: 'stray"quote' }));
  assert.match(malformed.errors.join(' '), /Invalid CSV quote/);
  assert.equal(malformed.measurements.length, 0);
}
{
  const malformed = parsePilotCsv(asCsv({ ...fields, notes: '"closed"trailing' }));
  assert.match(malformed.errors.join(' '), /Unexpected text after CSV closing quote/);
  assert.equal(malformed.measurements.length, 0);
}
{
  const tooMany = parsePilotCsv(asCsv({ ...fields, notes: 'fine' }).trimEnd() + ',extra' + String.fromCharCode(10));
  assert.match(tooMany.errors.join(' '), /expected 12 columns, received 13/);
  assert.equal(tooMany.measurements.length, 0);
}
{
  const tooFew = parsePilotCsv(asCsv(fields).trimEnd().slice(0, -1) + String.fromCharCode(10));
  assert.match(tooFew.errors.join(' '), /expected 12 columns, received 11/);
  assert.equal(tooFew.measurements.length, 0);
}

console.log('pilot CSV matched-pair round-trip and fail-closed validation passed');
