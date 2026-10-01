import type { CampusDecision, CampusDecisionReadiness, CampusProvenance } from './campus-contracts';

export type CourseSnapshotRecord = {
  code?: string;
  days?: string[];
  hours?: number[];
  rooms?: string[];
};

export type CourseSnapshot = Record<string, CourseSnapshotRecord>;

export type CourseSnapshotMeta = {
  captured_at?: string;
  refresh_required_after?: string;
  source_class?: string;
  source_url?: string;
  term?: string;
};

export type RoomScheduleIndex = {
  roomIds: string[];
  occupiedByRoomDay: Map<string, Set<number>>;
  scheduledLoadByRoomDay: Map<string, number>;
};

export type SpaceAllocationRequest = {
  requestId: string;
  day: string;
  startHour: number;
  durationHours: number;
  candidateRooms?: string[];
  requiredCapacity?: number;
};

export type SpaceAllocationRecommendation = {
  requestId: string;
  roomId: string;
  day: string;
  startHour: number;
  durationHours: number;
  occupiedHours: number[];
  capacityStatus: 'NOT_REQUIRED' | 'VERIFIED_SUFFICIENT' | 'UNVERIFIED';
  verifiedCapacity: number | null;
};

export type SpaceAllocationContext = {
  scheduleIndex: RoomScheduleIndex;
  snapshotMeta: CourseSnapshotMeta;
  roomCapacities?: Record<string, number>;
  nowIso?: string;
};

export type SpaceAllocationBatch = {
  decisions: Array<CampusDecision<SpaceAllocationRecommendation>>;
  assignedRequestIds: string[];
  unassignedRequestIds: string[];
};

const VALID_DAYS = new Set(['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']);

function roomDayKey(roomId: string, day: string): string {
  return `${roomId}\u0000${day}`;
}

function validHour(value: number): boolean {
  return Number.isInteger(value) && value >= 0 && value <= 23;
}

function occupiedHours(startHour: number, durationHours: number): number[] {
  return Array.from({ length: durationHours }, (_, offset) => startHour + offset);
}

export function buildRoomScheduleIndex(snapshot: CourseSnapshot): RoomScheduleIndex {
  const occupiedByRoomDay = new Map<string, Set<number>>();
  const roomIds = new Set<string>();

  for (const course of Object.values(snapshot)) {
    if (!Array.isArray(course.days) || !Array.isArray(course.hours) || !Array.isArray(course.rooms)) continue;
    const alignedLength = Math.min(course.days.length, course.hours.length, course.rooms.length);

    for (let index = 0; index < alignedLength; index += 1) {
      const day = course.days[index];
      const hour = course.hours[index];
      const roomId = course.rooms[index]?.trim();
      if (!roomId || !VALID_DAYS.has(day) || !validHour(hour)) continue;

      roomIds.add(roomId);
      const key = roomDayKey(roomId, day);
      const slots = occupiedByRoomDay.get(key) ?? new Set<number>();
      slots.add(hour);
      occupiedByRoomDay.set(key, slots);
    }
  }

  const scheduledLoadByRoomDay = new Map<string, number>();
  for (const [key, slots] of occupiedByRoomDay.entries()) {
    scheduledLoadByRoomDay.set(key, slots.size);
  }

  return {
    roomIds: Array.from(roomIds).sort((left, right) => left.localeCompare(right)),
    occupiedByRoomDay,
    scheduledLoadByRoomDay,
  };
}

function snapshotFreshness(meta: CourseSnapshotMeta, nowIso: string): {
  stale: boolean;
  unknown: boolean;
} {
  if (!meta.refresh_required_after) return { stale: false, unknown: true };
  const refreshAt = Date.parse(meta.refresh_required_after);
  const now = Date.parse(nowIso);
  if (!Number.isFinite(refreshAt) || !Number.isFinite(now)) return { stale: false, unknown: true };
  return { stale: now > refreshAt, unknown: false };
}

function validateRequest(request: SpaceAllocationRequest): string[] {
  const reasons: string[] = [];
  if (!request.requestId?.trim()) reasons.push('MISSING_REQUEST_ID');
  if (!VALID_DAYS.has(request.day)) reasons.push('INVALID_DAY');
  if (!validHour(request.startHour)) reasons.push('INVALID_START_HOUR');
  if (!Number.isInteger(request.durationHours) || request.durationHours <= 0) reasons.push('INVALID_DURATION');
  if (
    validHour(request.startHour)
    && Number.isInteger(request.durationHours)
    && request.durationHours > 0
    && request.startHour + request.durationHours - 1 > 23
  ) reasons.push('REQUEST_EXCEEDS_DAY_BOUNDARY');
  if (
    request.requiredCapacity !== undefined
    && (!Number.isFinite(request.requiredCapacity) || request.requiredCapacity <= 0)
  ) reasons.push('INVALID_REQUIRED_CAPACITY');
  return reasons;
}

function makeBaseProvenance(context: SpaceAllocationContext): CampusProvenance[] {
  const provenance: CampusProvenance[] = [
    {
      sourceClass: 'OFFICIAL_SNAPSHOT',
      sourceId: context.snapshotMeta.source_url ?? 'course-schedule-snapshot',
      note: `Course schedule snapshot${context.snapshotMeta.term ? ` for ${context.snapshotMeta.term}` : ''}; not live room occupancy.`,
    },
    {
      sourceClass: 'DERIVED_SNAPSHOT',
      sourceId: 'cs1-room-schedule-index-v1',
      note: 'Room conflicts are derived only from aligned day/hour/room schedule triples.',
    },
    {
      sourceClass: 'POLICY_HEURISTIC',
      sourceId: 'cs1-space-allocation-policy-v1',
      note: 'Ranks feasible rooms by scheduled load, adjacency, then deterministic room ID tie-break.',
    },
  ];
  if (context.roomCapacities) {
    provenance.push({
      sourceClass: 'USER_SUPPLIED',
      sourceId: 'request.roomCapacities',
      note: 'Capacity values are request-supplied and are not represented as live or university-verified telemetry.',
    });
  }
  return provenance;
}

function withholdSpaceDecision(
  request: SpaceAllocationRequest,
  context: SpaceAllocationContext,
  reasonCodes: string[],
): CampusDecision<SpaceAllocationRecommendation> {
  return {
    decisionId: `space:${request.requestId || 'unknown'}`,
    domain: 'SPACE',
    generatedAt: context.nowIso ?? new Date().toISOString(),
    readiness: 'WITHHOLD',
    abstained: true,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes,
    limitations: ['NO_LIVE_ROOM_OCCUPANCY', 'NO_ACCESS_CONTROL_INTEGRATION', 'SCHEDULE_SNAPSHOT_ONLY'],
    provenance: makeBaseProvenance(context),
    recommendation: null,
  };
}

type RankedRoom = {
  roomId: string;
  scheduledLoad: number;
  adjacentOccupied: number;
  capacityStatus: 'NOT_REQUIRED' | 'VERIFIED_SUFFICIENT' | 'UNVERIFIED';
  verifiedCapacity: number | null;
};

function isSlotFree(
  roomId: string,
  day: string,
  hours: number[],
  scheduleIndex: RoomScheduleIndex,
  reservedByRoomDay: Map<string, Set<number>>,
): boolean {
  const key = roomDayKey(roomId, day);
  const scheduled = scheduleIndex.occupiedByRoomDay.get(key);
  const reserved = reservedByRoomDay.get(key);
  return hours.every(hour => !scheduled?.has(hour) && !reserved?.has(hour));
}

function rankRoom(
  roomId: string,
  request: SpaceAllocationRequest,
  context: SpaceAllocationContext,
): RankedRoom | null {
  let capacityStatus: RankedRoom['capacityStatus'] = 'NOT_REQUIRED';
  let verifiedCapacity: number | null = null;

  if (request.requiredCapacity !== undefined) {
    const suppliedCapacity = context.roomCapacities?.[roomId];
    if (Number.isFinite(suppliedCapacity)) {
      verifiedCapacity = suppliedCapacity;
      if (suppliedCapacity < request.requiredCapacity) return null;
      capacityStatus = 'VERIFIED_SUFFICIENT';
    } else {
      capacityStatus = 'UNVERIFIED';
    }
  }

  const key = roomDayKey(roomId, request.day);
  const scheduled = context.scheduleIndex.occupiedByRoomDay.get(key);
  const lastHour = request.startHour + request.durationHours - 1;
  const adjacentOccupied = Number(Boolean(scheduled?.has(request.startHour - 1)))
    + Number(Boolean(scheduled?.has(lastHour + 1)));

  return {
    roomId,
    scheduledLoad: context.scheduleIndex.scheduledLoadByRoomDay.get(key) ?? 0,
    adjacentOccupied,
    capacityStatus,
    verifiedCapacity,
  };
}

function constrainedness(request: SpaceAllocationRequest, roomCount: number): number {
  const candidateCount = request.candidateRooms?.length ?? roomCount;
  return candidateCount * 100 - request.durationHours;
}

export function allocateRooms(
  requests: SpaceAllocationRequest[],
  context: SpaceAllocationContext,
): SpaceAllocationBatch {
  const nowIso = context.nowIso ?? new Date().toISOString();
  const executionContext = { ...context, nowIso };
  const freshness = snapshotFreshness(context.snapshotMeta, nowIso);
  const knownRooms = new Set(context.scheduleIndex.roomIds);
  const reservedByRoomDay = new Map<string, Set<number>>();
  const decisionByOriginalIndex = new Map<number, CampusDecision<SpaceAllocationRecommendation>>();

  const queue = requests
    .map((request, originalIndex) => ({ request, originalIndex }))
    .sort((left, right) =>
      constrainedness(left.request, context.scheduleIndex.roomIds.length)
      - constrainedness(right.request, context.scheduleIndex.roomIds.length)
      || left.originalIndex - right.originalIndex
    );

  for (const { request, originalIndex } of queue) {
    const validationReasons = validateRequest(request);
    if (validationReasons.length > 0) {
      decisionByOriginalIndex.set(originalIndex, withholdSpaceDecision(request, executionContext, validationReasons));
      continue;
    }

    const requestedCandidates = request.candidateRooms?.length
      ? Array.from(new Set(request.candidateRooms.map(room => room.trim()).filter(Boolean)))
      : context.scheduleIndex.roomIds;
    const candidates = requestedCandidates.filter(roomId => knownRooms.has(roomId));
    if (candidates.length === 0) {
      decisionByOriginalIndex.set(
        originalIndex,
        withholdSpaceDecision(request, executionContext, ['NO_KNOWN_CANDIDATE_ROOM']),
      );
      continue;
    }

    const hours = occupiedHours(request.startHour, request.durationHours);
    const scheduleFreeRooms = candidates.filter(roomId =>
      isSlotFree(roomId, request.day, hours, context.scheduleIndex, reservedByRoomDay)
    );
    if (scheduleFreeRooms.length === 0) {
      decisionByOriginalIndex.set(
        originalIndex,
        withholdSpaceDecision(request, executionContext, ['NO_FEASIBLE_ROOM']),
      );
      continue;
    }

    const rankedRooms = scheduleFreeRooms
      .map(roomId => rankRoom(roomId, request, executionContext))
      .filter((room): room is RankedRoom => room !== null)
      .sort((left, right) => {
        const leftCapacityRank = left.capacityStatus === 'VERIFIED_SUFFICIENT' || left.capacityStatus === 'NOT_REQUIRED' ? 0 : 1;
        const rightCapacityRank = right.capacityStatus === 'VERIFIED_SUFFICIENT' || right.capacityStatus === 'NOT_REQUIRED' ? 0 : 1;
        return leftCapacityRank - rightCapacityRank
          || left.scheduledLoad - right.scheduledLoad
          || left.adjacentOccupied - right.adjacentOccupied
          || left.roomId.localeCompare(right.roomId);
      });

    const selected = rankedRooms[0];
    if (!selected) {
      decisionByOriginalIndex.set(
        originalIndex,
        withholdSpaceDecision(request, executionContext, ['NO_ROOM_MEETS_REQUIRED_CAPACITY']),
      );
      continue;
    }

    const key = roomDayKey(selected.roomId, request.day);
    const reserved = reservedByRoomDay.get(key) ?? new Set<number>();
    for (const hour of hours) reserved.add(hour);
    reservedByRoomDay.set(key, reserved);

    const reasonCodes: string[] = ['SCHEDULE_CONFLICT_CHECK_PASSED'];
    let readiness: CampusDecisionReadiness = 'READY';
    if (selected.capacityStatus === 'UNVERIFIED') {
      readiness = 'REVIEW_REQUIRED';
      reasonCodes.push('ROOM_CAPACITY_UNVERIFIED');
    }
    if (freshness.stale) {
      readiness = 'REVIEW_REQUIRED';
      reasonCodes.push('COURSE_SNAPSHOT_REFRESH_REQUIRED');
    } else if (freshness.unknown) {
      readiness = 'REVIEW_REQUIRED';
      reasonCodes.push('COURSE_SNAPSHOT_FRESHNESS_UNKNOWN');
    }

    decisionByOriginalIndex.set(originalIndex, {
      decisionId: `space:${request.requestId}`,
      domain: 'SPACE',
      generatedAt: nowIso,
      readiness,
      abstained: false,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes,
      limitations: [
        'NO_LIVE_ROOM_OCCUPANCY',
        'NO_ACCESS_CONTROL_INTEGRATION',
        'SCHEDULE_SNAPSHOT_ONLY',
        ...(selected.capacityStatus === 'UNVERIFIED' ? ['ROOM_CAPACITY_NOT_VERIFIED'] : []),
      ],
      provenance: makeBaseProvenance(executionContext),
      recommendation: {
        requestId: request.requestId,
        roomId: selected.roomId,
        day: request.day,
        startHour: request.startHour,
        durationHours: request.durationHours,
        occupiedHours: hours,
        capacityStatus: selected.capacityStatus,
        verifiedCapacity: selected.verifiedCapacity,
      },
    });
  }

  const decisions = requests.map((request, index) =>
    decisionByOriginalIndex.get(index)
    ?? withholdSpaceDecision(request, executionContext, ['INTERNAL_ALLOCATION_GAP'])
  );

  return {
    decisions,
    assignedRequestIds: decisions
      .filter(decision => decision.recommendation !== null)
      .map(decision => decision.recommendation!.requestId),
    unassignedRequestIds: decisions
      .map((decision, index) => ({ decision, requestId: requests[index]?.requestId ?? decision.decisionId }))
      .filter(({ decision }) => decision.recommendation === null)
      .map(({ requestId }) => requestId),
  };
}
