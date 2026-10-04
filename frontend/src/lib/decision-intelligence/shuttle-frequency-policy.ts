export type ShuttleFrequencyServiceType = 'campus_loop' | 'inter_campus';
export type ShuttlePressureBand = 'LOW' | 'MODERATE' | 'HIGH' | 'SURGE';
export type ScheduleCoverage = 'FULL' | 'PARTIAL' | 'NONE';
export type ShuttleDominantDirection = 'SOUTH_TO_NORTH' | 'NORTH_TO_SOUTH' | 'BALANCED' | 'UNRESOLVED';
export type ShuttleFleetFeasibilityStatus = 'UNVERIFIED' | 'USER_SUPPLIED_FEASIBLE' | 'USER_SUPPLIED_CONSTRAINED';

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
  availableVehicles?: number | null;
  roundTripMinutes?: number | null;
  vehicleCapacity?: number | null;
};

export type ShuttleFrequencyRecommendation = {
  routeId: string;
  day: string;
  hour: number;
  scheduleCoverage: ScheduleCoverage;
  scheduleAffectedSeatsEstimate: number;
  scheduleArrivalsEstimate: number;
  scheduleDeparturesEstimate: number;
  southToNorthProxySeatsEstimate: number | null;
  northToSouthProxySeatsEstimate: number | null;
  dominantDirection: ShuttleDominantDirection;
  pressureBasisSeatsEstimate: number;
  scenarioAdjustedPressureBasisSeatsEstimate: number;
  pressureBand: ShuttlePressureBand;
  targetHeadwayMinutes: number;
  targetDeparturesPerHour: number;
  operationalHeadwayMinutes: number;
  operationalDeparturesPerHour: number;
  availableVehicles: number | null;
  roundTripMinutes: number | null;
  vehicleCapacity: number | null;
  requiredVehiclesForTarget: number | null;
  fleetMinimumHeadwayMinutes: number | null;
  hourlySeatCapacityEstimate: number | null;
  currentPublishedHeadwayMinutes: number | null;
  publishedScheduleComparison: 'INCREASE_FREQUENCY_CANDIDATE' | 'MAINTAIN_OR_REVIEW' | 'DECREASE_FREQUENCY_CANDIDATE' | 'NO_COMPARABLE_PUBLISHED_HEADWAY';
  fleetFeasibilityStatus: ShuttleFleetFeasibilityStatus;
  automaticDispatch: false;
};

type Campus = 'south' | 'north';
type ProvenanceClass = 'OFFICIAL_SNAPSHOT' | 'USER_SUPPLIED' | 'POLICY_HEURISTIC' | 'EXTERNAL_LIVE' | 'SCENARIO' | 'UNAVAILABLE';
type Provenance = { sourceClass: ProvenanceClass; sourceId: string; note?: string };
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
type CampusPulse = { arrivals: number; departures: number };
type SchedulePulse = {
  arrivals: number;
  departures: number;
  affectedSeats: number;
  byCampus: Record<Campus, CampusPulse>;
};

const VALID_DAYS = new Set(['M', 'T', 'W', 'Th', 'F', 'St']);
const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };
const SOUTH_PREFIXES = new Set(['TB', 'İB', 'IB', 'M', 'ALH', 'GH', 'HH', 'OFB', 'ÖFB', 'NB', 'JF', 'GY']);
const NORTH_PREFIXES = new Set(['KB', 'NH', 'LIB', 'BM', 'EF', 'YD', 'ET', 'ETA', 'KP', 'SBU', 'KY', 'Y34']);
const ROUTE_SCOPE: Record<string, { campuses: Campus[]; coverage: ScheduleCoverage }> = {
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
const BANDS: ShuttlePressureBand[] = ['LOW', 'MODERATE', 'HIGH', 'SURGE'];
const LIMITATIONS = [
  'NO_LIVE_SHUTTLE_GPS',
  'NO_LIVE_SHUTTLE_OCCUPANCY',
  'NO_VERIFIED_FLEET_OR_TURNAROUND_FEASIBILITY',
  'USER_SUPPLIED_FLEET_CONTEXT_IS_NOT_TELEMETRY',
  'COURSE_SCHEDULE_ACTIVITY_IS_NOT_OBSERVED_RIDERSHIP',
  'DIRECTIONAL_VALUES_ARE_SCHEDULE_MOVEMENT_PROXIES_NOT_OBSERVED_OD_TRIPS',
  'NO_AUTOMATIC_TIMETABLE_MUTATION',
];

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
    limitations: LIMITATIONS,
    provenance,
    recommendation: null,
  };
}

function roomCampus(room: string): Campus | null {
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

function clockHour(raw: number | string): number | null {
  const numeric = Number(raw);
  if (!Number.isInteger(numeric)) return null;
  const hour = SLOT_TO_HOUR[numeric] ?? numeric;
  return hour >= 0 && hour <= 23 ? hour : null;
}

function emptyPulse(): SchedulePulse {
  return {
    arrivals: 0,
    departures: 0,
    affectedSeats: 0,
    byCampus: { south: { arrivals: 0, departures: 0 }, north: { arrivals: 0, departures: 0 } },
  };
}

function schedulePulse(courses: Record<string, ShuttleCourseRecord>, day: string, planningHour: number, campuses: Campus[]): SchedulePulse {
  const pulse = emptyPulse();
  const allowed = new Set(campuses);

  for (const course of Object.values(courses ?? {})) {
    const days = Array.isArray(course.days) ? course.days : [];
    const hours = Array.isArray(course.hours) ? course.hours : [];
    const rooms = Array.isArray(course.rooms) ? course.rooms : [];
    const entries: Array<{ hour: number; room: string; campus: Campus; students: number }> = [];

    for (let i = 0; i < Math.min(days.length, hours.length, rooms.length); i += 1) {
      if (days[i] !== day) continue;
      const hour = clockHour(hours[i]);
      const room = String(rooms[i] ?? '').trim();
      const campus = roomCampus(room);
      if (hour === null || !campus || !allowed.has(campus)) continue;
      entries.push({ hour, room, campus, students: estimatedStudents(String(course.code ?? ''), room) });
    }

    entries.sort((a, b) => a.hour - b.hour || a.room.localeCompare(b.room));
    let group: typeof entries = [];
    const flush = () => {
      if (!group.length) return;
      const start = group[0].hour;
      const endExclusive = group[group.length - 1].hour + 1;
      const campus = group[0].campus;
      const students = Math.max(...group.map(item => item.students));
      if (start === planningHour) {
        pulse.arrivals += students;
        pulse.byCampus[campus].arrivals += students;
      }
      if (endExclusive === planningHour) {
        pulse.departures += students;
        pulse.byCampus[campus].departures += students;
      }
      group = [];
    };

    for (const entry of entries) {
      const prev = group[group.length - 1];
      if (prev && (entry.hour !== prev.hour + 1 || entry.room !== prev.room || entry.campus !== prev.campus)) flush();
      group.push(entry);
    }
    flush();
  }

  pulse.affectedSeats = pulse.arrivals + pulse.departures;
  return pulse;
}

function directionalPressure(pulse: SchedulePulse, coverage: ScheduleCoverage) {
  if (coverage !== 'FULL') {
    return {
      southToNorth: null as number | null,
      northToSouth: null as number | null,
      dominantDirection: 'UNRESOLVED' as ShuttleDominantDirection,
      pressureBasisSeats: pulse.affectedSeats,
    };
  }

  const southToNorth = pulse.byCampus.north.arrivals + pulse.byCampus.south.departures;
  const northToSouth = pulse.byCampus.south.arrivals + pulse.byCampus.north.departures;
  const total = southToNorth + northToSouth;
  const diff = Math.abs(southToNorth - northToSouth);
  const directional = total > 0 && diff >= 30 && diff / total >= 0.15;
  const dominantDirection: ShuttleDominantDirection = directional
    ? (southToNorth > northToSouth ? 'SOUTH_TO_NORTH' : 'NORTH_TO_SOUTH')
    : 'BALANCED';

  return {
    southToNorth,
    northToSouth,
    dominantDirection,
    pressureBasisSeats: Math.max(southToNorth, northToSouth),
  };
}

function bandIndex(seats: number): number {
  if (seats >= 1000) return 3;
  if (seats >= 350) return 2;
  if (seats >= 120) return 1;
  return 0;
}

function validRange(value: number | undefined | null, min: number, max: number): boolean {
  return value === undefined || value === null || (Number.isFinite(value) && value >= min && value <= max);
}

function validIntegerRange(value: number | undefined | null, min: number, max: number): boolean {
  return value === undefined || value === null || (Number.isInteger(value) && Number(value) >= min && Number(value) <= max);
}

function clockMinutes(value: string): number | null {
  const match = value.trim().match(/^(\d{1,2}):(\d{2})$/);
  if (!match) return null;
  const hour = Number(match[1]);
  const minute = Number(match[2]);
  if (!Number.isInteger(hour) || !Number.isInteger(minute) || hour < 0 || hour > 23 || minute < 0 || minute > 59) return null;
  return hour * 60 + minute;
}

export function estimatePublishedHeadwayMinutes(times: string[] | undefined, planningHour: number): number | null {
  const minutes = (times ?? []).map(clockMinutes).filter((value): value is number => value !== null).sort((a, b) => a - b);
  if (minutes.length < 2) return null;
  const center = planningHour * 60;
  const nearby = minutes.filter(value => Math.abs(value - center) <= 120);
  const source = nearby.length >= 2 ? nearby : minutes;
  const gaps = source.slice(1).map((value, index) => value - source[index]).filter(gap => gap > 0 && gap <= 180).sort((a, b) => a - b);
  if (!gaps.length) return null;
  const middle = Math.floor(gaps.length / 2);
  return gaps.length % 2 ? gaps[middle] : Math.round((gaps[middle - 1] + gaps[middle]) / 2);
}

export function recommendShuttleFrequency(input: ShuttleFrequencyInput): FrequencyDecision {
  const generatedAt = input.nowIso ?? new Date().toISOString();
  const provenance: Provenance[] = [];

  if (!input.routeId || !['campus_loop', 'inter_campus'].includes(input.serviceType) || !VALID_DAYS.has(input.day) || !Number.isInteger(input.hour) || input.hour < 0 || input.hour > 23) {
    return withhold(input, generatedAt, ['INVALID_PLANNING_WINDOW']);
  }
  if (!validRange(input.eventMultiplier, 1, 3) || !validRange(input.operatorQueuePassengers, 0, 10000)) {
    return withhold(input, generatedAt, ['INVALID_CONTEXT_FACTOR']);
  }

  const hasFleetContext = input.availableVehicles !== undefined && input.availableVehicles !== null
    || input.roundTripMinutes !== undefined && input.roundTripMinutes !== null
    || input.vehicleCapacity !== undefined && input.vehicleCapacity !== null;
  const hasFleetCore = input.availableVehicles !== undefined && input.availableVehicles !== null
    && input.roundTripMinutes !== undefined && input.roundTripMinutes !== null;
  if (hasFleetContext && !hasFleetCore) {
    return withhold(input, generatedAt, ['INCOMPLETE_FLEET_CONTEXT']);
  }
  if (
    !validIntegerRange(input.availableVehicles, 1, 100)
    || !validRange(input.roundTripMinutes, 1, 600)
    || !validIntegerRange(input.vehicleCapacity, 1, 500)
  ) {
    return withhold(input, generatedAt, ['INVALID_FLEET_CONTEXT']);
  }

  const scope = ROUTE_SCOPE[input.routeId] ?? { campuses: [], coverage: 'NONE' as const };
  const queue = input.operatorQueuePassengers ?? null;
  if (scope.coverage === 'NONE' && queue === null) {
    provenance.push({ sourceClass: 'UNAVAILABLE', sourceId: `schedule-coverage:${input.routeId}`, note: 'Stored course snapshot has no route-relevant campus mapping for this service.' });
    return withhold(input, generatedAt, ['NO_ROUTE_SCHEDULE_COVERAGE'], provenance);
  }

  const reasons = ['OPERATOR_REVIEW_REQUIRED', 'FREQUENCY_POLICY_HEURISTIC_ONLY'];
  const pulse = scope.coverage === 'NONE' ? emptyPulse() : schedulePulse(input.courses, input.day, input.hour, scope.campuses);
  const directional = directionalPressure(pulse, scope.coverage);

  if (scope.coverage !== 'NONE') {
    provenance.push({ sourceClass: 'OFFICIAL_SNAPSHOT', sourceId: input.snapshotMeta.source_url ?? 'course-schedule-snapshot', note: 'Aggregate class start/end activity only; not rider-level demand.' });
  }
  if (scope.coverage === 'FULL') reasons.push('DIRECTIONAL_SCHEDULE_PRESSURE_APPLIED');
  if (scope.coverage === 'PARTIAL') reasons.push('PARTIAL_ROUTE_SCHEDULE_COVERAGE');

  const refreshAfter = input.snapshotMeta.refresh_required_after ? Date.parse(input.snapshotMeta.refresh_required_after) : Number.NaN;
  const nowMs = Date.parse(generatedAt);
  if (Number.isFinite(refreshAfter) && Number.isFinite(nowMs) && nowMs > refreshAfter) reasons.push('COURSE_SNAPSHOT_REFRESH_REQUIRED');

  const eventMultiplier = input.eventMultiplier ?? 1;
  const scenarioAdjustedPressureBasisSeatsEstimate = Math.round(directional.pressureBasisSeats * eventMultiplier);
  let pressureIndex = bandIndex(scenarioAdjustedPressureBasisSeatsEstimate);

  if (eventMultiplier > 1) {
    reasons.push(directional.pressureBasisSeats > 0 ? 'EVENT_SCENARIO_PRESSURE_APPLIED' : 'EVENT_SCENARIO_MULTIPLIER_NO_BASELINE_ACTIVITY');
    provenance.push({ sourceClass: 'SCENARIO', sourceId: 'operator-event-multiplier', note: `Caller-supplied multiplier ${eventMultiplier.toFixed(2)} applied to the schedule pressure basis only.` });
  }
  if (input.rain === true) {
    pressureIndex += 1;
    reasons.push('RAIN_PRESSURE_APPLIED');
    provenance.push({ sourceClass: input.weatherSourceId ? 'EXTERNAL_LIVE' : 'USER_SUPPLIED', sourceId: input.weatherSourceId ?? 'rain-context' });
  } else if (input.rain === false && input.weatherSourceId) {
    provenance.push({ sourceClass: 'EXTERNAL_LIVE', sourceId: input.weatherSourceId });
  }
  if (queue !== null) {
    if (queue >= 40) pressureIndex += 2;
    else if (queue >= 15) pressureIndex += 1;
    reasons.push('USER_SUPPLIED_QUEUE_SIGNAL');
    provenance.push({ sourceClass: 'USER_SUPPLIED', sourceId: 'operator-queue-observation', note: 'Aggregate queue observation; no person-level identifiers.' });
  }

  pressureIndex = Math.max(0, Math.min(3, pressureIndex));
  const targetHeadway = HEADWAYS[input.serviceType][pressureIndex];
  const targetDeparturesPerHour = Number((60 / targetHeadway).toFixed(2));

  let fleetFeasibilityStatus: ShuttleFleetFeasibilityStatus = 'UNVERIFIED';
  let requiredVehiclesForTarget: number | null = null;
  let fleetMinimumHeadwayMinutes: number | null = null;
  let operationalHeadwayMinutes = targetHeadway;
  let operationalDeparturesPerHour = targetDeparturesPerHour;
  let hourlySeatCapacityEstimate: number | null = null;

  if (hasFleetCore) {
    const availableVehicles = Number(input.availableVehicles);
    const roundTripMinutes = Number(input.roundTripMinutes);
    requiredVehiclesForTarget = Math.ceil(roundTripMinutes / targetHeadway);
    fleetMinimumHeadwayMinutes = Math.ceil(roundTripMinutes / availableVehicles);
    operationalHeadwayMinutes = Math.max(targetHeadway, fleetMinimumHeadwayMinutes);
    operationalDeparturesPerHour = Number((60 / operationalHeadwayMinutes).toFixed(2));
    fleetFeasibilityStatus = operationalHeadwayMinutes > targetHeadway
      ? 'USER_SUPPLIED_CONSTRAINED'
      : 'USER_SUPPLIED_FEASIBLE';

    reasons.push('USER_SUPPLIED_FLEET_CONTEXT');
    if (fleetFeasibilityStatus === 'USER_SUPPLIED_CONSTRAINED') reasons.push('FLEET_CONSTRAINS_DEMAND_TARGET');
    if (input.vehicleCapacity !== undefined && input.vehicleCapacity !== null) {
      hourlySeatCapacityEstimate = Number((operationalDeparturesPerHour * input.vehicleCapacity).toFixed(1));
      reasons.push('USER_SUPPLIED_VEHICLE_CAPACITY');
    }
    provenance.push({
      sourceClass: 'USER_SUPPLIED',
      sourceId: 'operator-fleet-context',
      note: `${availableVehicles} vehicles; ${roundTripMinutes} min round trip${input.vehicleCapacity ? `; ${input.vehicleCapacity} seats/vehicle` : ''}. Not verified telemetry.`,
    });
  }

  const publishedHeadway = estimatePublishedHeadwayMinutes(input.officialDepartureTimes, input.hour);
  let comparison: ShuttleFrequencyRecommendation['publishedScheduleComparison'] = 'NO_COMPARABLE_PUBLISHED_HEADWAY';
  if (publishedHeadway !== null) {
    comparison = operationalHeadwayMinutes < publishedHeadway - 1
      ? 'INCREASE_FREQUENCY_CANDIDATE'
      : operationalHeadwayMinutes > publishedHeadway + 1
        ? 'DECREASE_FREQUENCY_CANDIDATE'
        : 'MAINTAIN_OR_REVIEW';
  }

  provenance.push({
    sourceClass: 'POLICY_HEURISTIC',
    sourceId: 'cs1-shuttle-frequency-policy-v3',
    note: 'Directional values are movement proxies from aggregate class start/end activity. User-supplied fleet context constrains the advisory headway but does not authorize dispatch.',
  });

  return {
    decisionId: `shuttle-frequency:${input.routeId}:${input.day}:${input.hour}`,
    domain: 'SHUTTLE',
    generatedAt,
    readiness: 'REVIEW_REQUIRED',
    abstained: false,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes: reasons,
    limitations: LIMITATIONS,
    provenance,
    recommendation: {
      routeId: input.routeId,
      day: input.day,
      hour: input.hour,
      scheduleCoverage: scope.coverage,
      scheduleAffectedSeatsEstimate: pulse.affectedSeats,
      scheduleArrivalsEstimate: pulse.arrivals,
      scheduleDeparturesEstimate: pulse.departures,
      southToNorthProxySeatsEstimate: directional.southToNorth,
      northToSouthProxySeatsEstimate: directional.northToSouth,
      dominantDirection: directional.dominantDirection,
      pressureBasisSeatsEstimate: directional.pressureBasisSeats,
      scenarioAdjustedPressureBasisSeatsEstimate,
      pressureBand: BANDS[pressureIndex],
      targetHeadwayMinutes: targetHeadway,
      targetDeparturesPerHour,
      operationalHeadwayMinutes,
      operationalDeparturesPerHour,
      availableVehicles: hasFleetCore ? Number(input.availableVehicles) : null,
      roundTripMinutes: hasFleetCore ? Number(input.roundTripMinutes) : null,
      vehicleCapacity: input.vehicleCapacity ?? null,
      requiredVehiclesForTarget,
      fleetMinimumHeadwayMinutes,
      hourlySeatCapacityEstimate,
      currentPublishedHeadwayMinutes: publishedHeadway,
      publishedScheduleComparison: comparison,
      fleetFeasibilityStatus,
      automaticDispatch: false,
    },
  };
}
