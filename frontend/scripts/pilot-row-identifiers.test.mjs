import assert from 'node:assert/strict';

const { nextPilotRowIdentifiers } =
  await import('../src/lib/pilot-row-identifiers.ts');

// Service identity is whitespace-normalized by the scorer. Allocation must use
// the same identity rule or a padded manual ID can be regenerated as a duplicate.
const rows = [
  { pairId: 'PAIR_01', serviceId: ' CONTROL-02 ', arm: 'CONTROL' },
  { pairId: 'PAIR_01', serviceId: 'INTERVENTION-01', arm: 'INTERVENTION' },
];

assert.deepEqual(
  nextPilotRowIdentifiers(rows, 'CONTROL'),
  { pairId: 'PAIR_02', serviceId: 'CONTROL-03' },
  'allocator must reserve trimmed service IDs and advance past their numeric suffix',
);

console.log('pilot row identifier normalization regression passed');
