import assert from 'node:assert/strict';
import { recommendShuttleItinerary } from '../src/lib/decision-intelligence/shuttle-policy.ts';
import { buildRoomScheduleIndex, allocateRooms } from '../src/lib/decision-intelligence/space-allocation.ts';

const network = {
  source: { url: 'https://example.edu/shuttle' },
  stops: [{ id: 'a' }, { id: 'b' }, { id: 'c' }, { id: 'd' }],
  routes: [
    { id: 'r1', stopIds: ['a', 'b', 'c'], distanceKmEstimate: 4, bidirectional: false },
    { id: 'r2', stopIds: ['c', 'd'], distanceKmEstimate: 3, bidirectional: true },
    { id: 'r3', stopIds: ['a', 'd'], distanceKmEstimate: 12, bidirectional: true },
  ],
};

{
  const result = recommendShuttleItinerary(network, 'a', 'c');
  assert.equal(result.readiness, 'REVIEW_REQUIRED');
  assert.equal(result.recommendation?.routeIds[0], 'r1');
  assert.equal(result.recommendation?.transfers, 0);
  assert.ok(result.reasonCodes.includes('OFFICIAL_TIMETABLE_CHECK_REQUIRED'));
  assert.equal(result.automaticDispatchAllowed, false);
}

{
  const result = recommendShuttleItinerary(network, 'b', 'd', { transferPenaltyKm: 2 });
  assert.equal(result.recommendation?.routeIds.join(','), 'r1,r2');
  assert.deepEqual(result.recommendation?.transferStopIds, ['c']);
  assert.equal(result.recommendation?.transfers, 1);
}

{
  const directPreferred = recommendShuttleItinerary(network, 'a', 'd', { transferPenaltyKm: 0 });
  assert.equal(directPreferred.recommendation?.routeIds.join(','), 'r3');
  assert.equal(directPreferred.recommendation?.transfers, 0);
}

{
  const oneWayOnlyNetwork = { ...network, routes: [network.routes[0]] };
  const reversed = recommendShuttleItinerary(oneWayOnlyNetwork, 'c', 'a');
  assert.equal(reversed.readiness, 'WITHHOLD');
  assert.equal(reversed.recommendation, null);
  assert.ok(reversed.reasonCodes.includes('NO_FEASIBLE_SHUTTLE_PATH'));
}

{
  const invalid = recommendShuttleItinerary(network, 'missing', 'a');
  assert.equal(invalid.readiness, 'WITHHOLD');
  assert.ok(invalid.reasonCodes.includes('UNKNOWN_ORIGIN_STOP'));
}

const snapshot = {
  C1: { code: 'C1', days: ['M', 'M'], hours: [1, 2], rooms: ['R1', 'R1'] },
  C2: { code: 'C2', days: ['M'], hours: [3], rooms: ['R2'] },
};
const index = buildRoomScheduleIndex(snapshot);
const freshMeta = {
  captured_at: '2026-10-01T00:00:00Z',
  refresh_required_after: '2026-10-10T00:00:00Z',
  source_class: 'OFFICIAL_SNAPSHOT',
  source_url: 'https://example.edu/courses',
};

{
  const batch = allocateRooms(
    [
      { requestId: 'A', day: 'M', startHour: 1, durationHours: 1, candidateRooms: ['R1', 'R2'] },
      { requestId: 'B', day: 'M', startHour: 1, durationHours: 1, candidateRooms: ['R1', 'R2'] },
    ],
    { scheduleIndex: index, snapshotMeta: freshMeta, nowIso: '2026-10-01T12:00:00Z' },
  );
  assert.equal(batch.decisions[0].recommendation?.roomId, 'R2');
  assert.equal(batch.decisions[1].readiness, 'WITHHOLD');
  assert.ok(batch.decisions[1].reasonCodes.includes('NO_FEASIBLE_ROOM'));
  assert.deepEqual(batch.unassignedRequestIds, ['B']);
}

{
  const capacityUnknown = allocateRooms(
    [{ requestId: 'C', day: 'T', startHour: 4, durationHours: 1, candidateRooms: ['R1'], requiredCapacity: 30 }],
    { scheduleIndex: index, snapshotMeta: freshMeta, nowIso: '2026-10-01T12:00:00Z' },
  );
  assert.equal(capacityUnknown.decisions[0].readiness, 'REVIEW_REQUIRED');
  assert.ok(capacityUnknown.decisions[0].reasonCodes.includes('ROOM_CAPACITY_UNVERIFIED'));
}

{
  const capacityVerified = allocateRooms(
    [{ requestId: 'D', day: 'T', startHour: 4, durationHours: 1, candidateRooms: ['R1', 'R2'], requiredCapacity: 40 }],
    {
      scheduleIndex: index,
      snapshotMeta: freshMeta,
      roomCapacities: { R1: 20, R2: 50 },
      nowIso: '2026-10-01T12:00:00Z',
    },
  );
  assert.equal(capacityVerified.decisions[0].recommendation?.roomId, 'R2');
  assert.equal(capacityVerified.decisions[0].readiness, 'READY');
}

{
  const stale = allocateRooms(
    [{ requestId: 'E', day: 'T', startHour: 4, durationHours: 1, candidateRooms: ['R2'] }],
    {
      scheduleIndex: index,
      snapshotMeta: { ...freshMeta, refresh_required_after: '2026-09-30T23:59:59Z' },
      nowIso: '2026-10-01T12:00:00Z',
    },
  );
  assert.equal(stale.decisions[0].readiness, 'REVIEW_REQUIRED');
  assert.ok(stale.decisions[0].reasonCodes.includes('COURSE_SNAPSHOT_REFRESH_REQUIRED'));
}

console.log('campus operations policy tests passed');
