import { NextRequest, NextResponse } from 'next/server';
import courseSnapshot from '@/data/real_boun_courses.json';
import courseSnapshotMeta from '@/data/course_snapshot_meta.json';
import {
  allocateRooms,
  buildRoomScheduleIndex,
  type CourseSnapshot,
  type SpaceAllocationRequest,
} from '@/lib/decision-intelligence/space-allocation';

export const dynamic = 'force-dynamic';

const scheduleIndex = buildRoomScheduleIndex(courseSnapshot as CourseSnapshot);

const source = {
  term: courseSnapshotMeta.term,
  capturedAt: courseSnapshotMeta.captured_at,
  sourceUrl: courseSnapshotMeta.source_url,
  sourceClass: courseSnapshotMeta.source_class,
  refreshRequiredAfter: courseSnapshotMeta.refresh_required_after,
};

const truthBoundary = {
  liveRoomOccupancyConnected: false,
  accessControlConnected: false,
  bmsConnected: false,
  universityVerifiedRoomCapacityConnected: false,
  automaticRoomBooking: false,
  note: 'Recommendations check the official course-schedule snapshot and within-batch conflicts. They do not prove real-time room vacancy or booking authority.',
};

function parseSpaceRequest(value: unknown): SpaceAllocationRequest | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null;
  const item = value as Record<string, unknown>;
  if (typeof item.requestId !== 'string') return null;
  if (typeof item.day !== 'string') return null;
  if (typeof item.startHour !== 'number') return null;
  if (typeof item.durationHours !== 'number') return null;
  if (
    item.candidateRooms !== undefined
    && (!Array.isArray(item.candidateRooms) || !item.candidateRooms.every(room => typeof room === 'string'))
  ) return null;
  if (item.requiredCapacity !== undefined && typeof item.requiredCapacity !== 'number') return null;

  return {
    requestId: item.requestId,
    day: item.day,
    startHour: item.startHour,
    durationHours: item.durationHours,
    candidateRooms: item.candidateRooms as string[] | undefined,
    requiredCapacity: item.requiredCapacity as number | undefined,
  };
}

function parseRoomCapacities(value: unknown): Record<string, number> | undefined | null {
  if (value === undefined) return undefined;
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null;

  const output: Record<string, number> = {};
  for (const [roomId, capacity] of Object.entries(value)) {
    if (!roomId.trim() || typeof capacity !== 'number' || !Number.isFinite(capacity) || capacity <= 0) return null;
    output[roomId.trim()] = capacity;
  }
  return output;
}

export async function GET() {
  const now = Date.now();
  const refreshDeadline = Date.parse(courseSnapshotMeta.refresh_required_after);
  const stale = Number.isFinite(refreshDeadline) ? now > refreshDeadline : true;

  return NextResponse.json(
    {
      source,
      inventory: {
        roomsObservedInScheduleSnapshot: scheduleIndex.roomIds.length,
        roomIds: scheduleIndex.roomIds,
        roomCapacitySource: 'UNAVAILABLE',
      },
      readiness: stale ? 'REVIEW_REQUIRED' : 'READY',
      reasonCodes: stale ? ['COURSE_SNAPSHOT_REFRESH_REQUIRED'] : ['COURSE_SNAPSHOT_WITHIN_REFRESH_WINDOW'],
      truthBoundary,
    },
    {
      headers: {
        'Cache-Control': 'no-store',
      },
    },
  );
}

export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid_json' }, { status: 400 });
  }

  if (typeof body !== 'object' || body === null || Array.isArray(body)) {
    return NextResponse.json({ error: 'invalid_request_body' }, { status: 400 });
  }

  const payload = body as Record<string, unknown>;
  if (!Array.isArray(payload.requests) || payload.requests.length === 0 || payload.requests.length > 100) {
    return NextResponse.json(
      { error: 'requests_must_contain_1_to_100_items' },
      { status: 400 },
    );
  }

  const requests = payload.requests.map(parseSpaceRequest);
  if (requests.some(item => item === null)) {
    return NextResponse.json(
      {
        error: 'invalid_space_request_shape',
        required: ['requestId:string', 'day:string', 'startHour:number', 'durationHours:number'],
      },
      { status: 400 },
    );
  }

  const roomCapacities = parseRoomCapacities(payload.roomCapacities);
  if (roomCapacities === null) {
    return NextResponse.json(
      { error: 'room_capacities_must_be_positive_numeric_map' },
      { status: 400 },
    );
  }

  const batch = allocateRooms(requests as SpaceAllocationRequest[], {
    scheduleIndex,
    snapshotMeta: courseSnapshotMeta,
    roomCapacities,
  });

  return NextResponse.json(
    {
      ...batch,
      source,
      inventory: {
        roomsObservedInScheduleSnapshot: scheduleIndex.roomIds.length,
        roomCapacitySource: roomCapacities ? 'USER_SUPPLIED_REQUEST_DATA' : 'UNAVAILABLE',
      },
      truthBoundary,
    },
    {
      headers: {
        'Cache-Control': 'no-store',
      },
    },
  );
}
