import assert from 'node:assert/strict';
import { estimatePublishedHeadwayMinutes, recommendShuttleFrequency } from '../src/lib/decision-intelligence/shuttle-frequency-policy.ts';

const courses = {
  A: { code: 'CMPE 150.01', days: ['Th', 'Th'], hours: [6, 7], rooms: ['NH 101', 'NH 101'] },
  B: { code: 'MATH 101.01', days: ['Th', 'Th'], hours: [8, 9], rooms: ['M 1100', 'M 1100'] },
  C: { code: 'ECON 101.01', days: ['Th'], hours: [8], rooms: ['NH 201'] },
  D: { code: 'CHEM 105.01', days: ['Th'], hours: [8], rooms: ['M 2100'] },
  E: { code: 'PHYS 121.01', days: ['Th'], hours: [8], rooms: ['ALH 1'] },
};
const staleMeta = {
  captured_at: '2026-09-06T23:44:48.000Z',
  refresh_required_after: '2026-09-30T23:59:59+03:00',
  source_class: 'OFFICIAL_SNAPSHOT',
  source_url: 'https://registration.bogazici.edu.tr/BUIS/General/schedule.aspx',
};

const dry = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'Th', hour: 16, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T15:40:00+03:00', rain: false });
const wetEvent = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'Th', hour: 16, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T15:40:00+03:00', rain: true, eventMultiplier: 1.5 });
assert.equal(dry.readiness, 'REVIEW_REQUIRED');
assert.equal(wetEvent.readiness, 'REVIEW_REQUIRED');
assert.equal(dry.recommendation?.dominantDirection, 'NORTH_TO_SOUTH');
assert.equal(dry.recommendation?.southToNorthProxySeatsEstimate, 132);
assert.equal(dry.recommendation?.northToSouthProxySeatsEstimate, 608);
assert.equal(dry.recommendation?.pressureBasisSeatsEstimate, 608);
assert.ok(dry.reasonCodes.includes('DIRECTIONAL_SCHEDULE_PRESSURE_APPLIED'));
assert.ok((wetEvent.recommendation?.targetHeadwayMinutes ?? 99) < (dry.recommendation?.targetHeadwayMinutes ?? 0));
assert.ok(wetEvent.reasonCodes.includes('COURSE_SNAPSHOT_REFRESH_REQUIRED'));
assert.ok(wetEvent.reasonCodes.includes('RAIN_PRESSURE_APPLIED'));
assert.ok(wetEvent.reasonCodes.includes('EVENT_SCENARIO_PRESSURE_APPLIED'));
assert.equal(wetEvent.automaticDispatchAllowed, false);
assert.equal(wetEvent.recommendation?.fleetFeasibilityStatus, 'UNVERIFIED');

const noPulseBase = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'Th', hour: 12, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T11:40:00+03:00' });
const noPulseEvent = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'Th', hour: 12, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T11:40:00+03:00', eventMultiplier: 3 });
assert.equal(noPulseEvent.recommendation?.targetHeadwayMinutes, noPulseBase.recommendation?.targetHeadwayMinutes);
assert.ok(noPulseEvent.reasonCodes.includes('EVENT_SCENARIO_MULTIPLIER_NO_BASELINE_ACTIVITY'));

const published = ['14:00', '14:20', '14:40', '15:00', '15:20', '15:40', '16:00', '16:20'];
assert.equal(estimatePublishedHeadwayMinutes(published, 15), 20);
const publishedComparison = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'Th', hour: 16, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T15:40:00+03:00', officialDepartureTimes: published });
assert.equal(publishedComparison.recommendation?.currentPublishedHeadwayMinutes, 20);
assert.equal(publishedComparison.recommendation?.publishedScheduleComparison, 'INCREASE_FREQUENCY_CANDIDATE');

const noCoverage = recommendShuttleFrequency({ routeId: 'etiler-kilyos', serviceType: 'inter_campus', day: 'Th', hour: 16, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T15:40:00+03:00' });
assert.equal(noCoverage.readiness, 'WITHHOLD');
assert.ok(noCoverage.reasonCodes.includes('NO_ROUTE_SCHEDULE_COVERAGE'));

const queueOverride = recommendShuttleFrequency({ routeId: 'etiler-kilyos', serviceType: 'inter_campus', day: 'Th', hour: 16, courses, snapshotMeta: staleMeta, nowIso: '2026-10-01T15:40:00+03:00', operatorQueuePassengers: 55 });
assert.equal(queueOverride.readiness, 'REVIEW_REQUIRED');
assert.ok(queueOverride.reasonCodes.includes('USER_SUPPLIED_QUEUE_SIGNAL'));
assert.equal(queueOverride.recommendation?.dominantDirection, 'UNRESOLVED');

const invalid = recommendShuttleFrequency({ routeId: 'south-north-loop', serviceType: 'campus_loop', day: 'X', hour: 99, courses, snapshotMeta: staleMeta });
assert.equal(invalid.readiness, 'WITHHOLD');
assert.ok(invalid.reasonCodes.includes('INVALID_PLANNING_WINDOW'));

console.log('shuttle frequency policy tests passed');
