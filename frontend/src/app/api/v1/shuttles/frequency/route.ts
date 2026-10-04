import { NextRequest, NextResponse } from 'next/server';
import realCourses from '@/data/real_boun_courses.json';
import courseSnapshotMeta from '@/data/course_snapshot_meta.json';
import { getShuttleNetworkSnapshot } from '@/lib/shuttle-network';
import { fetchBounShuttle, fetchBounWeather } from '@/lib/live-sources';
import { recommendShuttleFrequency, type ShuttleCourseRecord } from '@/lib/decision-intelligence/shuttle-frequency-policy';

export const dynamic = 'force-dynamic';

const DAY_BY_SHORT_NAME: Record<string, string> = { Mon: 'M', Tue: 'T', Wed: 'W', Thu: 'Th', Fri: 'F', Sat: 'St', Sun: 'Su' };

function istanbulPlanningWindow(now: Date) {
  const weekday = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Istanbul', weekday: 'short' }).format(now);
  const hour = Number(new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', hour: '2-digit', hour12: false }).format(now));
  return { day: DAY_BY_SHORT_NAME[weekday] ?? 'M', hour };
}

function optionalFinite(raw: string | null): number | undefined {
  if (raw === null || raw.trim() === '') return undefined;
  const value = Number(raw);
  return Number.isFinite(value) ? value : Number.NaN;
}

function isInvalidOptional(value: number | undefined) {
  return value !== undefined && Number.isNaN(value);
}

export async function GET(request: NextRequest) {
  const now = new Date();
  const defaults = istanbulPlanningWindow(now);
  const routeId = request.nextUrl.searchParams.get('routeId')?.trim() || 'south-north-loop';
  const day = request.nextUrl.searchParams.get('day')?.trim() || defaults.day;
  const hourRaw = request.nextUrl.searchParams.get('hour');
  const hour = hourRaw === null || hourRaw.trim() === '' ? defaults.hour : Number(hourRaw);
  const eventMultiplier = optionalFinite(request.nextUrl.searchParams.get('eventMultiplier')) ?? 1;
  const queuePassengers = optionalFinite(request.nextUrl.searchParams.get('queuePassengers'));
  const availableVehicles = optionalFinite(request.nextUrl.searchParams.get('availableVehicles'));
  const roundTripMinutes = optionalFinite(request.nextUrl.searchParams.get('roundTripMinutes'));
  const vehicleCapacity = optionalFinite(request.nextUrl.searchParams.get('vehicleCapacity'));

  if (
    !Number.isInteger(hour)
    || hour < 0
    || hour > 23
    || Number.isNaN(eventMultiplier)
    || isInvalidOptional(queuePassengers)
    || isInvalidOptional(availableVehicles)
    || isInvalidOptional(roundTripMinutes)
    || isInvalidOptional(vehicleCapacity)
  ) {
    return NextResponse.json({ error: 'invalid_frequency_context' }, { status: 400 });
  }

  const snapshot = getShuttleNetworkSnapshot();
  const route = snapshot.routes.find(item => item.id === routeId);
  if (!route) {
    return NextResponse.json({ error: 'unknown_shuttle_route', allowedRouteIds: snapshot.routes.map(item => item.id) }, { status: 404 });
  }

  const [weather, shuttleFeed] = await Promise.all([
    fetchBounWeather(),
    routeId === 'south-north-loop' ? fetchBounShuttle() : Promise.resolve(null),
  ]);
  const courses = realCourses as Record<string, ShuttleCourseRecord>;
  const nowIso = now.toISOString();
  const common = {
    routeId,
    serviceType: route.serviceType,
    day,
    courses,
    snapshotMeta: courseSnapshotMeta,
    nowIso,
    officialDepartureTimes: shuttleFeed?.departure_times,
  };

  const decision = recommendShuttleFrequency({
    ...common,
    hour,
    rain: weather.rain,
    weatherSourceId: weather.source.ok ? weather.source.url : null,
    eventMultiplier,
    operatorQueuePassengers: queuePassengers ?? null,
    availableVehicles: availableVehicles ?? null,
    roundTripMinutes: roundTripMinutes ?? null,
    vehicleCapacity: vehicleCapacity ?? null,
  });

  // Keep this baseline schedule-only. Fleet and queue/event scenario inputs affect the
  // selected planning window, not the reference day curve shown to the operator.
  const hourlyPlan = Array.from({ length: 13 }, (_, index) => 9 + index).map(planningHour => {
    const scheduleOnly = recommendShuttleFrequency({ ...common, hour: planningHour });
    return { hour: planningHour, readiness: scheduleOnly.readiness, reasonCodes: scheduleOnly.reasonCodes, recommendation: scheduleOnly.recommendation };
  });

  const fleetInputPresent = availableVehicles !== undefined || roundTripMinutes !== undefined || vehicleCapacity !== undefined;

  return NextResponse.json({
    decision,
    hourlyPlan,
    context: {
      route: { id: route.id, nameTr: route.nameTr, nameEn: route.nameEn, serviceType: route.serviceType },
      planningWindow: { day, hour, timezone: 'Europe/Istanbul' },
      courseSnapshot: {
        term: courseSnapshotMeta.term,
        capturedAt: courseSnapshotMeta.captured_at,
        refreshRequiredAfter: courseSnapshotMeta.refresh_required_after,
        sourceClass: courseSnapshotMeta.source_class,
        sourceUrl: courseSnapshotMeta.source_url,
      },
      weather: {
        rain: weather.rain,
        temperature: weather.temperature,
        windSpeedKmh: weather.wind_speed_kmh,
        source: weather.source,
      },
      publishedSchedule: shuttleFeed ? {
        route: shuttleFeed.route,
        departureTimes: shuttleFeed.departure_times,
        nextDeparture: shuttleFeed.next_departure,
        source: shuttleFeed.source,
      } : null,
      scenarioInputs: {
        eventMultiplier,
        operatorQueuePassengers: queuePassengers ?? null,
        fleet: {
          availableVehicles: availableVehicles ?? null,
          roundTripMinutes: roundTripMinutes ?? null,
          vehicleCapacity: vehicleCapacity ?? null,
          provenance: fleetInputPresent ? 'USER_SUPPLIED' : 'UNAVAILABLE',
          verifiedTelemetry: false,
        },
      },
    },
    truthBoundary: {
      recommendationType: 'ADVISORY_FREQUENCY_POLICY_HEURISTIC',
      scheduleActivityIsObservedRidership: false,
      liveGpsConnected: false,
      liveOccupancyConnected: false,
      verifiedFleetCapacityConnected: false,
      verifiedTurnaroundConnected: false,
      userSuppliedFleetContextVerified: false,
      automaticDispatch: false,
      officialTimetableRemainsAuthoritative: true,
    },
  }, { headers: { 'Cache-Control': 'no-store' } });
}
