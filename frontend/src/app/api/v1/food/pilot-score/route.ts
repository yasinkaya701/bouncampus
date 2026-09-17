import { NextResponse } from 'next/server';
import {
  FOOD_WASTE_PILOT_PROTOCOL,
  scoreFoodWastePilot,
  validatePilotMeasurement,
  type PilotServiceMeasurement,
} from '@/lib/food-waste';

export async function GET() {
  return NextResponse.json({
    endpoint: 'POST /api/v1/food/pilot-score',
    protocol: FOOD_WASTE_PILOT_PROTOCOL,
    requestShape: {
      measurements: FOOD_WASTE_PILOT_PROTOCOL.measurementFields,
    },
    note: 'Scores measured aggregate service outcomes only. It does not create or simulate pilot measurements.',
  });
}

export async function POST(request: Request) {
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: 'INVALID_JSON' }, { status: 400 });
  }

  const measurements = (payload as { measurements?: unknown })?.measurements;
  if (!Array.isArray(measurements)) {
    return NextResponse.json(
      { error: 'MEASUREMENTS_REQUIRED', detail: 'Body must include a measurements array.' },
      { status: 400 },
    );
  }

  const typed = measurements as PilotServiceMeasurement[];
  const validationErrors = typed.flatMap((measurement, index) =>
    validatePilotMeasurement(measurement).map(message => ({ index, message })),
  );

  if (validationErrors.length) {
    return NextResponse.json(
      { error: 'INVALID_MEASUREMENTS', validationErrors },
      { status: 400 },
    );
  }

  return NextResponse.json({
    scorecard: scoreFoodWastePilot(typed),
    protocolVersion: FOOD_WASTE_PILOT_PROTOCOL.version,
    claimBoundary: 'PROMISING is a pilot classification, not a generalized climate-impact claim.',
  });
}
