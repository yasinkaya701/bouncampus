import { NextRequest, NextResponse } from 'next/server';
import { getShuttleNetworkSnapshot } from '@/lib/shuttle-network';
import {
  recommendShuttleItinerary,
  type ShuttleDecisionNetwork,
} from '@/lib/decision-intelligence/shuttle-policy';

export const dynamic = 'force-dynamic';

function parsePassengerTrips(raw: string | null): number | null {
  if (raw === null || raw.trim() === '') return null;
  const value = Number(raw);
  if (!Number.isFinite(value) || value < 0 || value > 100000) return Number.NaN;
  return Math.round(value);
}

export async function GET(request: NextRequest) {
  const origin = request.nextUrl.searchParams.get('origin')?.trim() ?? '';
  const destination = request.nextUrl.searchParams.get('destination')?.trim() ?? '';
  const passengerTrips = parsePassengerTrips(request.nextUrl.searchParams.get('passengerTrips'));

  if (!origin || !destination) {
    return NextResponse.json(
      { error: 'origin_and_destination_required' },
      { status: 400 },
    );
  }
  if (Number.isNaN(passengerTrips)) {
    return NextResponse.json(
      { error: 'invalid_passenger_trips', constraints: { min: 0, max: 100000 } },
      { status: 400 },
    );
  }

  const snapshot = getShuttleNetworkSnapshot();
  const network: ShuttleDecisionNetwork = {
    source: { url: snapshot.source.url },
    stops: snapshot.stops.map(stop => ({ id: stop.id })),
    routes: snapshot.routes.map(route => ({
      id: route.id,
      stopIds: route.stopIds,
      distanceKmEstimate: route.distanceKmEstimate,
      officialScheduleUrl: route.officialScheduleUrl,
      // Existing public route labels explicitly mark two-way services with ⇄.
      // Other services are treated forward-only so the policy fails closed.
      bidirectional: route.nameTr.includes('⇄') || route.nameEn.includes('⇄'),
    })),
  };

  const decision = recommendShuttleItinerary(network, origin, destination);
  let privateCarReplacementScenario = null;

  if (passengerTrips !== null && decision.recommendation) {
    const assumedCarOccupancy = snapshot.climateModel.assumedCarOccupancy;
    const emissionFactor = snapshot.climateModel.carEmissionKgCo2ePerVehicleKm;
    const avoidedVehicleKm = assumedCarOccupancy > 0
      ? (decision.recommendation.estimatedDistanceKm * passengerTrips) / assumedCarOccupancy
      : 0;
    privateCarReplacementScenario = {
      provenance: 'SCENARIO',
      passengerTrips,
      estimatedRouteDistanceKm: decision.recommendation.estimatedDistanceKm,
      assumedCarOccupancy,
      carEmissionKgCo2ePerVehicleKm: emissionFactor,
      avoidedVehicleKmEstimate: Number(avoidedVehicleKm.toFixed(2)),
      avoidedCarKgCo2eEstimate: Number((avoidedVehicleKm * emissionFactor).toFixed(2)),
      achievedImpact: false,
      note: snapshot.climateModel.noteEn,
    };
  }

  return NextResponse.json(
    {
      decision,
      privateCarReplacementScenario,
      truthBoundary: {
        source: snapshot.source,
        liveGpsConnected: false,
        liveOccupancyConnected: false,
        verifiedVehicleCapacityConnected: false,
        routeDirectionality: 'Derived conservatively from published route labels; official timetable remains authoritative.',
        departureTimes: 'CHECK_OFFICIAL_TIMETABLE',
      },
    },
    {
      headers: {
        'Cache-Control': 'no-store',
      },
    },
  );
}
