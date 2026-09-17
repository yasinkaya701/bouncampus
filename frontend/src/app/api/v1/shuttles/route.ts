import { NextRequest, NextResponse } from 'next/server';
import { getShuttleNetworkSnapshot, type ShuttleServiceType } from '@/lib/shuttle-network';

export const dynamic = 'force-dynamic';

const VALID_TYPES = new Set<ShuttleServiceType>(['campus_loop', 'inter_campus']);

export async function GET(request: NextRequest) {
  const snapshot = getShuttleNetworkSnapshot();
  const requestedType = request.nextUrl.searchParams.get('type') as ShuttleServiceType | null;

  if (requestedType && !VALID_TYPES.has(requestedType)) {
    return NextResponse.json(
      {
        error: 'invalid_shuttle_type',
        allowed: Array.from(VALID_TYPES),
      },
      { status: 400 },
    );
  }

  const routes = requestedType
    ? snapshot.routes.filter(route => route.serviceType === requestedType)
    : snapshot.routes;

  return NextResponse.json(
    {
      ...snapshot,
      routes,
      filters: {
        serviceType: requestedType ?? 'all',
      },
    },
    {
      headers: {
        'Cache-Control': 'public, max-age=300, stale-while-revalidate=1800',
      },
    },
  );
}
