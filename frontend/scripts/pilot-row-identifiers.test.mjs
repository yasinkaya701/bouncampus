import assert from 'node:assert/strict';
import { nextPilotRowIdentifiers } from '../src/lib/pilot-row-identifiers.ts';

// Imported IDs may include accidental edge whitespace. The default allocator
// must use the same canonical service identity as pilot evidence deduplication.
const importedRows = [
  { pairId: 'PAIR_01', serviceId: ' CONTROL-02 ', arm: 'CONTROL' },
  { pairId: 'PAIR_01', serviceId: 'INTERVENTION-01', arm: 'INTERVENTION' },
];

const next = nextPilotRowIdentifiers(importedRows, 'CONTROL');
assert.equal(next.pairId, 'PAIR_02', 'a completed pair must not be reused');
assert.equal(next.serviceId, 'CONTROL-03',
  'padded imported identifiers must contribute to the next numeric ID');
assert.ok(!importedRows.some(row => row.serviceId.trim() === next.serviceId),
  'new default IDs must not alias existing physical services after trim');

const supplemented = [...importedRows, { ...next, arm: 'CONTROL' }];
const intervention = nextPilotRowIdentifiers(supplemented, 'INTERVENTION');
assert.equal(intervention.pairId, 'PAIR_02', 'opposite arm should complete the new pair');
assert.ok(!supplemented.some(row => row.serviceId.trim() === intervention.serviceId));

console.log('pilot row identifier whitespace-alias regression passed');
