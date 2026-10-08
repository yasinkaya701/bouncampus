import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { parseIstanbulPlanningDate } from '../src/lib/decision-intelligence/istanbul-planning-date.ts';

const validCases = [
  ['2026-10-08', 3],
  ['2024-02-29', 3],
  ['2000-02-29', 1],
  ['2026-10-11', 6],
];
for (const [dateVal, weekday] of validCases) {
  assert.deepEqual(parseIstanbulPlanningDate(dateVal), { dateVal, weekday },
    'valid date and weekday must be interpreted without timezone drift');
}

for (const dateVal of [
  '2026-02-30',
  '2025-02-29',
  '1900-02-29',
  '2026-04-31',
  '2026-00-15',
  '2026-13-01',
  '2026-10-00',
  '2026-10-32',
  '0000-01-01',
  '2026-1-08',
  '2026-10-08T12:00:00',
]) {
  assert.equal(parseIstanbulPlanningDate(dateVal), null,
    'invalid planning date must be rejected: ' + dateVal);
}

// 23:30 UTC is already the next day in Istanbul. No locale separator assumptions.
assert.deepEqual(
  parseIstanbulPlanningDate(null, new Date('2026-10-07T22:30:00Z')),
  { dateVal: '2026-10-08', weekday: 3 },
);
assert.deepEqual(
  parseIstanbulPlanningDate('', new Date('2026-10-08T20:00:00Z')),
  { dateVal: '2026-10-08', weekday: 3 },
);

const route = readFileSync(
  fileURLToPath(new URL('../src/app/api/v1/campus-ops/building-review/route.ts', import.meta.url)),
  'utf8',
);
assert.match(route, /parseIstanbulPlanningDate\(request\.nextUrl\.searchParams\.get\('date'\)\)/);
assert.match(route, /error: 'invalid_date'/);

console.log('building energy review date parsing and timezone regression passed');
