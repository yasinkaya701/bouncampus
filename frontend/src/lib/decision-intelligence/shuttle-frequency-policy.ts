export type ShuttleFrequencyServiceType = 'campus_loop' | 'inter_campus';
export type ShuttlePressureBand = 'LOW' | 'MODERATE' | 'HIGH' | 'SURGE';
export type ScheduleCoverage = 'FULL' | 'PARTIAL' | 'NONE';

export type ShuttleCourseRecord = {
  code?: string;
  days?: string[];
  hours?: Array<number | string>;
  rooms?: string[];
};

export type ShuttleCourseSnapshotMeta = {
  captured_at?: string;
  refresh_required_after?: string;
  source_class?: string;
  source_url?: string;
};

export type ShuttleFrequencyInput = {
  routeId: string;
  serviceType: ShuttleFrequencyServiceType;
  day: string;
  hour: number;
  courses: Record<string, ShuttleCourseRecord>;
  snapshotMeta: ShuttleCourseSnapshotMeta;
  nowIso?: string;
  rain?: boolean | null;
  weatherSourceId?: string | null;
  eventMultiplier?: number;
  operatorQueuePassengers?: number | null;
  officialDepartureTimes?: string[];
};

export type ShuttleFrequencyRecommendation = {
  routeId: string;
  day: string;
  hour: number;
  scheduleCoverage: ScheduleCoverage;
  scheduleAffectedSeatsEstimate: number;
  scheduleArrivalsEstimate: number;
  scheduleDeparturesEstimate: number;
  pressureBand: ShuttlePressureBand;
  targetHeadwayMinutes: number;
  targetDeparturesPerHour: number;
  currentPublishedHeadwayMinutes: number | null;
  publishedScheduleComparison: 'INCREASE_FREQUENCY_CANDIDATE' | 'MAINTAIN_OR_REVIEW' | 'DECREASE_FREQUENCY_CANDIDATE' | 'NO_COMPARABLE_PUBLISHED_HEADWAY';
  fleetFeasibilityStatus: 'UNVERIFIED';
  automaticDispatch: false;
};

type Provenance = {
  sourceClass: 'OFFICIAL_SNAPSHOT' | 'USER_SUPPLIED' | 'POLICY_HEURISTIC' | 'EXTERNAL_LIVE' | 'SCENARIO' | 'UNAVAILABLE';
  sourceId: string;
  note?: string;
};

type FrequencyDecision = {
  decisionId: string;
  domain: 'SHUTTLE';
  generatedAt: string;
  readiness: 'REVIEW_REQUIRED' | 'WITHHOLD';
  abstained: boolean;
  operatorApprovalRequired: true;
  automaticDispatchAllowed: false;
  reasonCodes: string[];
  limitations: string[];
  provenance: Provenance[];
  recommendation: ShuttleFrequencyRecommendation | null;
};

const VALID_DAYS = new Set(['M', 'T', 'W', 'Th', 'F', 'St']);
const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };

const SOUTH_PREFIXES = new Set(['TB', 'İB', 'IB', 'M', 'ALH', 'GH', 'HH', 'OFB', 'ÖFB', 'NB', 'JF', 'GY']);
const NORTH_PREFIXES = new Set(['KB', 'NH', 'LIB', 'BM', 'EF', 'YD', 'ET', 'ETA', 'KP', 'SBU', 'KY', 'Y34']);

const ROUTE_SCHEDULE_SCOPE: Record<string, { campuses: Array<'south' | 'north'>; coverage: ScheduleCoverage }> = {
  'south-north-loop': { campuses: ['south', 'north'], coverage: 'FULL' },
  'south-etiler-ring': { campuses: ['south'], coverage: 'PARTIAL' },
  'south-hisar': { campuses: ['south'], coverage: 'PARTIAL' },
  'etiler-anadolu-kandilli': { campuses: [], coverage: 'NONE' },
  'etiler-kilyos': { campuses: [], coverage: 'NONE' },
  'anadolu-kilyos': { campuses: [], coverage: 'NONE' },
  'kilyos-zekeriyakoy': { campuses: [], coverage: 'NONE' },
};

const HEADWAYS: Record<ShuttleFrequencyServiceType, number[]> = {
  campus_loop: [20, 15, 10, 5],
  inter_campus: [60, 45, 30, 20],
};

const BAND_BY_INDEX: ShuttlePressureBand[] = ['LOW', 'MODERATE', 'HIGH', 'SURGE'];

function withhold(input: ShuttleFrequencyInput, generatedAt: string, reasonCodes: string[], provenance: Provenance[] = []): FrequencyDecision {
  return {
    decisionId: `shuttle-frequency:${input.routeId || 'unknown'}:${input.day || 'unknown'}:${String(input.hour)}`,
    domain: 'SHUTTLE',
    generatedAt,
    readiness: 'WITHHOLD',
    abstained: true,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes,
    limitations: [
      'NO_LIVE_SHUTTLE_GPS',
      'NO_LIVE_SHUTTLE_OCCUPANCY',
      'NO_VERIFIED_FLEET_OR_TURNAROUND_FEASIBILITY',
      'COURSE_SCHEDULE_ACTIVITY_IS_NOT_OBSERVED_RIDERSHIP',
    ],
    provenance,
    recommendation: null,
  };
}

function roomCampus(room: string): 'south' | 'north' | null {
  const prefix = room.trim().match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
  if (!prefix) return null;
  if (SOUTH_PREFIXES.has(prefix)) return 'south';
  if (NORTH_PREFIXES.has(prefix)) return 'north';
  return null;
}

function estimatedStudents(courseCode: string, room: string): number {
  const normalized = room.toUpperCase();
  let capacity = 45;
  if (/NH\s*(101|201|301|401)/.test(normalized)) capacity = 150;
  else if (/M\s*(1100|2100|2150)/.test(normalized)) capacity = 120;
  else if (/KB\s*(001|002)/.test(normalized)) capacity = 100;
  else if (/ALH/.test(normalized)) capacity = 300;
  else if (/TB\s*130|TB\s*240|İB\s*[12]0[12]|IB\s*[12]0[12]/.test(normalized)) capacity = 75;

  const level = Number(courseCode.match(/\b([1-6])\d{2}\b/)?.[1] ?? 3);
  const fill = level === 1 ? 0.88 : level === 2 ? 0.78 : level <= 4 ? 0.65 : 0.45;
  return Math.max(8, Math.round(capacity * fill));
}

function toClockHour(raw: number | string): number | null {
  const numeric = Number(raw);
  if (!Number.isInteger(numeric)) return null;
  const hour = SLOT_TO_HOUR[numeric] ?? numeric;
  return hour >= 0 && hour <= 23 ? hour : null;
}

function schedulePulse(
  courses: Record<string, ShuttleCourseRecord>,
  day: string,
  planningHour: number,
  campuses: Array<'south' | 'north'>,
) {
  let arrivals = 0;
  let departures = 0;
  let sessions = 0;
  const campusSet = new Set(campuses);

  for (const course of Object.values(courses ?? {})) {
    const days = Array.isArray(course.days) ? course.days : [];
    const hours = Array.isArray(course.hours) ? course.hours : [];
    const rooms = Array.isArray(course.rooms) ? course.rooms : [];
    const entries: Array<{ hour: number; room: string; campus: 'south' | 'north'; students: number }> = [];

    for (let index = 0; index < Math.min(days.length, hours.length, rooms.length); index += 1) {
      if (days[index] !== day) continue;
      const hour = toClockHour(hours[index]);
      const room = String(rooms[index] ?? '').trim();
      const campus = roomCampus(room);
      if (hour === null || !campus || !campusSet.has(campus)) continue;
      entries.push({
        hour,
        room,
        campus,
        students: estimatedStudents(String(course.code ?? ''), room),
      });
    }

    entries.sort((left, right) => left.hour - right.hour || left.room.localeCompare(right.room));
    let group: typeof entries = [];
    const flush = () => {
      if (!group.length) return;
      const start = group[0].hour;
      const endExclusive = group[group.length - 1].hour + 1;
      const students = Math.max(...group.map(item => item.students));
      if (start === planningHour) arrivals += students;
      if (endExclusive === planningHour) departures += students;
      if (start === planningHour || endExclusive === planningHour) sessions += 1;
      group = [];
    };

    for (const entry of entries) {
      const previous = group[group.length - 1];
      if (previous && (entry.hour !== previous.hour + 1 || entry.room !== previous.room)) flush();
      group.push(entry);
    }
    flush();
  }

  return { arrivals, departures, affectedSeats: arrivals + departures, sessions };
}

function scheduleBandIndex(affectedSeats: number): number {
  if (affectedSeats >= 1000) return 3;
  if (affectedSeats >= 350) return 2;
  if (affectedSeats >= 120) return 1;
  return 0;
}

function validFiniteRange(value: number | undefined | null, min: number, max: number): boolean {
  return value === undefined || value === null || (Number.isFinite(value) && value >= min && value <= max);
}

function minutesFromClock(value: string): number | null {
  const match = value.trim().match(/^(\d{1,2}):(\d{2})$/);
  if (!match) return null;
  const h = Number(match[1]);
  const m = Number(match[2]);
  if (!Number.isInteger(h) || !Number.isInteger(m) || h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

export function estimatePublishedHeadwayMinutes(times: string[] | undefined, planningHour: number): number | null {
  const minutes = (times ?? [])
    .map(minutesFromClock)
    .filter((value): value is number => value !== null)
    .sort((a, b) => a - b);
  if (minutes.length < 2) return null;
  const center = planningHour * 60;
  const nearby = minutes.filter(value => Math.abs(value - center) <= 120);
  const source = nearby.length >= 2 ? nearby : minutes;
  const gaps = source.slice(1).map((value, index) => value - source[index]).filter(gap => gap > 0 && gap <= 180);
  if (!gaps.length) return null;
  gaps.sort((a, b) => a - b);
  const middle = Math.floor(gaps.length / 2);
  return gaps.length % 2 === 1 ? gaps[middle] : Math.round((gaps[middle - 1] + gaps[middle]) / 2);
}

export function recommendShuttleFrequency(input: ShuttleFrequencyInput): FrequencyDecision {
  const generatedAt = input.nowIso ?? new Date().toISOString();
  const provenance: Provenance[] = [];

  if (!input.routeId || !['campus_loop', 'inter_campus'].includes(input.serviceType) || !VALID_DAYS.has(input.day) || !Number.isInteger(input.hour) || input.hour < 0 || input.hour > 23) {
    return withhold(input, generatedAt, ['INVALID_PLANNING_WINDOW']);
  }
  if (!validFiniteRange(input.eventMultiplier, 1, 3) || !validFiniteRange(input.operatorQueuePassengers, 0, 10000)) {
    return withhold(input, generatedAt, ['INVALID_CONTEXT_FACTOR']);
  }

  const scope = ROUTE_SCHEDULE_SCOPE[input.routeId] ?? { campuses: [], coverage: 'NONE' as const };
  const queue = input.operatorQueuePassengers ?? null;
  if (scope.coverage === 'NONE' && queue === null) {
    provenance.push({ sourceClass: 'UNAVAILABLE', sourceId: `schedule-coverage:${input.routeId}`, note: 'Stored course snapshot has no route-relevant campus mapping for this service.' });
    return withhold(input, generatedAt, ['NO_ROUTE_SCHEDULE_COVERAGE'], provenance);
  }

  const reasonCodes = ['OPERATOR_REVIEW_REQUIRED', 'FREQUENCY_POLICY_HEURISTIC_ONLY'];
  const pulse = scope.coverage === 'NONE'
    ? { arrivals: 0, departures: 0, affectedSeats: 0, sessions: 0 }
    : schedulePulse(input.courses, input.day, input.hour, scope.campuses);

  if (scope.coverage !== 'NONE') {
    provenance.push({
      sourceClass: 'OFFICIAL_SNAPSHOT',
      sourceId: input.snapshotMeta.source_url ?? 'course-schedule-snapshot',
      note: 'Used only to estimate aggregate class-start/end activity; it is not rider-level demand.',
    });
  }

  const refreshAfter = input.snapshotMeta.refresh_required_after ? Date.parse(input.snapshotMeta.refresh_required_after) : Number.NaN;
  const nowMs = Date.parse(generatedAt);
  if (Number.isFinite(refreshAfter) && Number.isFinite(nowMs) && nowMs > refreshAfter) {
    reasonCodes.push('COURSE_SNAPSHOT_REFRESH_REQUIRED');
  }
  if (scope.coverage === 'PARTIAL') reasonCodes.push('PARTIAL_ROUTE_SCHEDULE_COVERAGE');

  let pressureIndex = scheduleBandIndex(pulse.affectedSeats);
  if (input.rain === true) {
    pressureIndex += 1;
    reasonCodes.push('RAIN_PRESSURE_APPLIED');
    provenance.push({ sourceClass: input.weatherSourceId ? 'EXTERNAL_LIVE' : 'USER_SUPPLIED', sourceId: input.weatherSourceId ?? 'rain-context', note: 'Rain bumps the discrete service-pressure band by one level.' });
  } else if (input.rain === false && input.weatherSourceId) {
    provenance.push({ sourceClass: 'EXTERNAL_LIVE', sourceId: input.weatherSourceId, note: 'No rain pressure applied.' });
  }

  const eventMultiplier = input.eventMultiplier ?? 1;
  if (eventMultiplier >= 1.75) pressureIndex += 2;
  else if (eventMultiplier >= 1.25) pressureIndex += 1;
  if (eventMultiplier > 1) {
    reasonCodes.push('EVENT_SCENARIO_PRESSURE_APPLIED');
    provenance.push({ sourceClass: 'SCENARIO', sourceId: 'operator-event-multiplier', note: `Caller-supplied event multiplier ${eventMultiplier.toFixed(2)}; not learned from observed ridership.` });
  }

  if (queue !== null) {
    if (queue >= 40) pressureIndex += 2;
    else if (queue >= 15) pressureIndex += 1;
    reasonCodes.push('USER_SUPPLIED_QUEUE_SIGNAL');
    provenance.push({ sourceClass: 'USER_SUPPLIED', sourceId: 'operator-queue-observation', note: 'Aggregate queue observation supplied by an operator; no person-level identifiers are accepted.' });
  }

  pressureIndex = Math.max(0, Math.min(3, pressureIndex));
  const headway = HEADWAYS[input.serviceType][pressureIndex];
  const publishedHeadway = estimatePublishedHeadwayMinutes(input.officialDepartureTimes, input.hour);
  let comparison: ShuttleFrequencyRecommendation['publishedScheduleComparison'] = 'NO_COMPARABLE_PUBLISHED_HEADWAY';
  if (publishedHeadway !== null) {
    if (headway < publishedHeadway - 1) comparison = 'INCREASE_FREQUENCY_CANDIDATE';
    else if (headway > publishedHeadway + 1) comparison = 'DECREASE_FREQUENCY_CANDIDATE';
    else comparison = 'MAINTAIN_OR_REVIEW';
  }

  provenance.push({
    sourceClass: 'POLICY_HEURISTIC',
    sourceId: 'cs1-shuttle-frequency-policy-v1',
    note: 'Discrete headway bands are planning heuristics; fleet/driver/turnaround feasibility must be verified before any timetable change.',
  });

  return {
    decisionId: `shuttle-frequency:${input.routeId}:${input.day}:${input.hour}`,
    domain: 'SHUTTLE',
    generatedAt,
    readiness: 'REVIEW_REQUIRED',
    abstained: false,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes,
    limitations: [
      'NO_LIVE_SHUTTLE_GPS',
      'NO_LIVE_SHUTTLE_OCCUPANCY',
      'NO_VERIFIED_FLEET_OR_TURNAROUND_FEASIBILITY',
      'COURSE_SCHEDULE_ACTIVITY_IS_NOT_OBSERVED_RIDERSHIP',
      'NO_AUTOMATIC_TIMETABLE_MUTATION',
    ],
    provenance,
    recommendation: {
      routeId: input.routeId,
      day: input.day,
      hour: input.hour,
      scheduleCoverage: scope.coverage,
      scheduleAffectedSeatsEstimate: pulse.affectedSeats,
      scheduleArrivalsEstimate: pulse.arrivals,
      scheduleDeparturesEstimate: pulse.departures,
      pressureBand: BAND_BY_INDEX[pressureIndex],
      targetHeadwayMinutes: headway,
      targetDeparturesPerHour: Number((60 / headway).toFixed(2)),
      currentPublishedHeadwayMinutes: publishedHeadway,
      publishedScheduleComparison: comparison,
      fleetFeasibilityStatus: 'UNVERIFIED',
      automaticDispatch: false,
    },
  };
}
