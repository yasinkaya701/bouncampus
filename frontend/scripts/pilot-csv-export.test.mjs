import assert from 'node:assert/strict';
import { registerHooks } from 'node:module';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Keep this separate from the active core pilot-csv regression owners.
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
const { preparePilotCsvExport, parsePilotCsv, serializePilotCsv } =
  await import('../src/lib/pilot-csv.ts');

const control = {
  pairId: 'PAIR_01',
  date: '2026-10-08',
  serviceId: 'CONTROL-01',
  arm: 'CONTROL',
  modelForecastMeals: null,
  producedPortions: 110,
  servedPortions: 100,
  edibleSurplusKg: 2,
  wasteKg: 6,
  earlySellout: false,
  operatorOverride: false,
  notes: 'Inspector noted "leftover"\nand checked it.',
};
const intervention = {
  ...control,
  serviceId: 'INTERVENTION-02',
  arm: 'INTERVENTION',
  modelForecastMeals: 105,
  notes: '',
};

// A valid export must be identical to the existing format and reimport cleanly.
const pair = [control, intervention];
const exportResult = preparePilotCsvExport(pair);
assert.deepEqual(exportResult.errors, []);
assert.equal(exportResult.csv, serializePilotCsv(pair));
assert.deepEqual(parsePilotCsv(exportResult.csv).measurements, pair);

function mustBlock(label, measurements, expected) {
  const result = preparePilotCsvExport(measurements);
  assert.equal(result.csv, null, label + ': no unusable download');
  assert.match(result.errors.join(' '), expected, label);
}

// The original UI let users download a file that would fail its own import.
mustBlock('blank required amount', [{ ...control, producedPortions: Number.NaN }, intervention],
  /producedPortions must be >= 0/);
mustBlock('blank intervention forecast', [control, { ...intervention, modelForecastMeals: null }],
  /INTERVENTION requires modelForecastMeals/);
mustBlock('impossible date', [{ ...control, date: '2026-02-30' }, intervention],
  /valid YYYY-MM-DD calendar date/);
mustBlock('unconfirmed operator flag', [{ ...control, operatorOverride: null }, intervention],
  /operatorOverride must be boolean/);
mustBlock('invalid served amount', [{ ...control, servedPortions: 0 }, intervention],
  /servedPortions must be > 0/);
mustBlock('empty data set', [], /No measurement rows/);

// Partial pairs are valid CSV drafts; matching is checked separately for scoring.
const partialPair = preparePilotCsvExport([control]);
assert.ok(partialPair.csv);
assert.deepEqual(partialPair.errors, []);
assert.deepEqual(parsePilotCsv(partialPair.csv).measurements, [control]);

console.log('pilot CSV export preflight and reimport regression passed');
