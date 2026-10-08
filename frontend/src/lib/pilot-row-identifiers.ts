export type PilotRowArm = 'CONTROL' | 'INTERVENTION';

export type PilotRowIdentity = {
  arm: PilotRowArm;
  pairId: string;
  serviceId: string;
};

/**
 * Allocate usable default identities even after rows have been removed, reordered,
 * or imported. A pair gets one service from each arm; a new row first repairs an
 * incomplete pair with the opposite arm instead of silently duplicating a pair.
 */
export function nextPilotRowIdentifiers(
  rows: readonly PilotRowIdentity[],
  arm: PilotRowArm,
): { pairId: string; serviceId: string } {
  const pairArmCounts = new Map<string, { CONTROL: number; INTERVENTION: number }>();
  const usedPairIds = new Set<string>();
  const usedServiceIds = new Set<string>();

  for (const row of rows) {
    const pairId = row.pairId.trim();
    if (pairId) {
      usedPairIds.add(pairId);
      const counts = pairArmCounts.get(pairId) ?? { CONTROL: 0, INTERVENTION: 0 };
      counts[row.arm] += 1;
      pairArmCounts.set(pairId, counts);
    }
    // Scoring compares trimmed service identities; reserve the same canonical key.
    usedServiceIds.add(row.serviceId.trim());
  }

  // Prefer a single unmatched opposite-arm service; never attach another
  // same-arm service to a pair that already contains the requested arm.
  const openPairId = rows.find(row => {
    const pairId = row.pairId.trim();
    const counts = pairArmCounts.get(pairId);
    return pairId && row.arm !== arm && counts?.[arm] === 0 && counts?.[row.arm] === 1;
  })?.pairId.trim();

  const maxPairIndex = rows.reduce((max, row) => {
    const match = /^PAIR_(\d+)$/.exec(row.pairId.trim());
    return match ? Math.max(max, Number(match[1])) : max;
  }, 0);
  let nextPairIndex = maxPairIndex + 1;
  let pairId = `PAIR_${String(nextPairIndex).padStart(2, '0')}`;
  while (usedPairIds.has(pairId)) {
    nextPairIndex += 1;
    pairId = `PAIR_${String(nextPairIndex).padStart(2, '0')}`;
  }

  const maxServiceIndex = rows.reduce((max, row) => {
    const match = /^(?:CONTROL|INTERVENTION)-(\d+)$/.exec(row.serviceId.trim());
    return match ? Math.max(max, Number(match[1])) : max;
  }, 0);
  let nextServiceIndex = maxServiceIndex + 1;
  let serviceId = `${arm}-${String(nextServiceIndex).padStart(2, '0')}`;
  while (usedServiceIds.has(serviceId)) {
    nextServiceIndex += 1;
    serviceId = `${arm}-${String(nextServiceIndex).padStart(2, '0')}`;
  }

  return { pairId: openPairId ?? pairId, serviceId };
}
