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

const { parsePilotCsv, serializePilotCsv, preparePilotCsvExport, PILOT_CSV_HEADERS } =
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

// The UI must never offer a CSV that its own importer will reject.
assert.deepEqual(preparePilotCsvExport(pair), { csv: serializePilotCsv(pair), errors: [] },
  'valid measured rows remain exportable without modifying notes or identifiers');
{
  const invalidDraft = preparePilotCsvExport([{ ...control, producedPortions: Number.NaN }, intervention]);
  assert.equal(invalidDraft.csv, null, 'blank required numeric fields must block CSV export');
  assert.match(invalidDraft.errors.join(' '), /producedPortions must be >= 0/);
}
{
  const missingForecast = preparePilotCsvExport([control, { ...intervention, modelForecastMeals: null }]);
  assert.equal(missingForecast.csv, null, 'intervention without forecast must not be exported as valid data');
  assert.match(missingForecast.errors.join(' '), /INTERVENTION requires modelForecastMeals/);
}
{
  const empty = preparePilotCsvExport([]);
  assert.equal(empty.csv, null, 'header-only exports cannot be reimported');
  assert.match(empty.errors.join(' '), /No measurement rows/);
}
{
  const unfinishedPair = preparePilotCsvExport([control]);
  assert.ok(unfinishedPair.csv, 'complete individual measurement rows may be saved before pairing');
  assert.deepEqual(unfinishedPair.errors, []);
}

const csv = serializePilotCsv(pair);
assert.ok(csv.startsWith('pair_id,date,'));
const parsed = parsePilotCsv('\uFEFF' + csv);
assert.deepEqual(parsed.errors, [], 'valid matched pilot CSV should import cleanly');
assert.deepEqual(parsed.measurements, pair, 'import/export must preserve pair ID and escaped notes');
assert.equal(analyzeMatchedPilotDesign(parsed.measurements).structurePassed, true);
assert.deepEqual(parsePilotCsv(serializePilotCsv(parsed.measurements)).measurements, pair);
const whitespaceNote = '  Inspector note, recorded verbatim.  \r\n  Follow-up\t ';
const annotatedPair = [{ ...control, notes: whitespaceNote }, intervention];
const annotatedImport = parsePilotCsv(serializePilotCsv(annotatedPair));
assert.deepEqual(annotatedImport.errors, [], 'CSV should accept annotated notes with whitespace');
assert.deepEqual(annotatedImport.measurements, annotatedPair,
  'CSV import/export must not strip spaces, tabs, or CRLF from evidence notes');

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

// Malformed records must fail closed rather than silently truncating measurements.
const validCsv = asCsv(fields);
const validDataRow = validCsv.trimEnd().split('\n')[1];
const csvHeader = PILOT_CSV_HEADERS.join(',');

{
  const result = parsePilotCsv(`${csvHeader}\n${validDataRow},unexpected\n`);
  assert.match(result.errors.join(' '), /expected 12 CSV columns, received 13/);
  assert.equal(result.measurements.length, 0, 'extra columns must not be silently discarded');
}
{
  const result = parsePilotCsv(`${csvHeader}\n${validDataRow.slice(0, -1)}\n`);
  assert.match(result.errors.join(' '), /expected 12 CSV columns, received 11/);
  assert.equal(result.measurements.length, 0, 'short rows must not be silently padded');
}
{
  const result = parsePilotCsv(`${csvHeader}\n${validDataRow}"unterminated\n`);
  assert.match(result.errors.join(' '), /unterminated quoted field/);
  assert.equal(result.measurements.length, 0);
}
{
  const result = parsePilotCsv(`${csvHeader}\n${validDataRow}"closed"trailing\n`);
  assert.match(result.errors.join(' '), /unexpected characters after closing quote/);
  assert.equal(result.measurements.length, 0);
}
{
  const result = parsePilotCsv(`${csvHeader}\n${validDataRow}unescaped"quote\n`);
  assert.match(result.errors.join(' '), /unexpected quote/);
  assert.equal(result.measurements.length, 0);
}
{
  const result = parsePilotCsv(validCsv + validDataRow + ',unexpected\n');
  assert.equal(result.errors.length, 1);
  assert.equal(result.measurements.length, 0, 'one bad row invalidates the whole import');
}

{
  const { hasConfirmedPilotFlags } = await import('../src/lib/pilot-flag-confirmation.ts');
  assert.equal(hasConfirmedPilotFlags([{ earlySellout: null, operatorOverride: false }]), false,
    'unanswered sell-out must not be counted as a measured no');
  assert.equal(hasConfirmedPilotFlags([{ earlySellout: false, operatorOverride: null }]), false,
    'unanswered operator override must not be counted as a measured no');
  assert.equal(hasConfirmedPilotFlags([{ earlySellout: false, operatorOverride: false }]), true,
    'explicit no/no is valid evidence');
  assert.equal(hasConfirmedPilotFlags([{ earlySellout: true, operatorOverride: false }]), true,
    'explicit yes/no is valid evidence');
  assert.equal(hasConfirmedPilotFlags([
    { earlySellout: true, operatorOverride: true },
    { earlySellout: null, operatorOverride: false },
  ]), false, 'one unanswered service must prevent scoring or export for the whole form');
}

const { nextPilotRowIdentifiers } = await import('../src/lib/pilot-row-identifiers.ts');

const firstPair = [
  { pairId: 'PAIR_01', serviceId: 'CONTROL-01', arm: 'CONTROL' },
  { pairId: 'PAIR_01', serviceId: 'INTERVENTION-02', arm: 'INTERVENTION' },
];
const nextControlIdentity = nextPilotRowIdentifiers(firstPair, 'CONTROL');
assert.deepEqual(nextControlIdentity, { pairId: 'PAIR_02', serviceId: 'CONTROL-03' },
  'new control service must get its own pair and a unique service ID');
const incompleteRows = [...firstPair, { ...nextControlIdentity, arm: 'CONTROL' }];
const nextInterventionIdentity = nextPilotRowIdentifiers(incompleteRows, 'INTERVENTION');
assert.deepEqual(nextInterventionIdentity, { pairId: 'PAIR_02', serviceId: 'INTERVENTION-04' },
  'new intervention service must complete the existing unmatched pair');
const matchedRows = [...incompleteRows, { ...nextInterventionIdentity, arm: 'INTERVENTION' }];
const afterRemoval = matchedRows.filter(row => row.serviceId !== 'INTERVENTION-02');
assert.deepEqual(nextPilotRowIdentifiers(afterRemoval, 'INTERVENTION'),
  { pairId: 'PAIR_01', serviceId: 'INTERVENTION-05' },
  're-adding after deletion must fill orphan pair without recycling a live service ID');
const repeatedControl = nextPilotRowIdentifiers(matchedRows, 'CONTROL');
assert.deepEqual(repeatedControl, { pairId: 'PAIR_03', serviceId: 'CONTROL-05' },
  'consecutive same-arm additions cannot double-book an existing pair');
assert.equal(new Set(matchedRows.map(row => row.serviceId)).size, matchedRows.length,
  'generated service IDs must stay unique');

console.log('pilot CSV matched-pair round-trip and fail-closed validation passed');
