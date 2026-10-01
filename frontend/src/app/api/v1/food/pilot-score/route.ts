import { NextResponse } from 'next/server';
import {
  FOOD_DECISION_POLICY,
  FOOD_WASTE_PILOT_PROTOCOL,
  scoreFoodWastePilot,
  validatePilotMeasurement,
  type PilotServiceMeasurement,
} from '@/lib/food-waste';

export async function GET() {
  return NextResponse.json({
    endpoint: 'POST /api/v1/food/pilot-score',
    protocol: FOOD_WASTE_PILOT_PROTOCOL,
    decisionPolicyVersion: FOOD_DECISION_POLICY.version,
    requestShape: {
      measurements: FOOD_WASTE_PILOT_PROTOCOL.measurementFields,
    },
    evidencePromotion: {
      inputEvidenceClass: 'MEASURED_PILOT_DATA',
      outputEvidenceClass: 'PILOT_SCORECARD',
      generalizedImpactClaimAllowed: false,
      requiredChecks: [
        'row-level measurement validity',
        'duplicate service detection',
        'minimum services per arm',
        '100% intervention forecast retention',
        'normalized waste-reduction target',
        'early-sellout guardrail',
        'manual food-safety review outside numeric scorecard',
      ],
    },
    note: 'Scores measured service outcomes only. It never creates or simulates pilot measurements.',
  });
}

export async function POST(request: Request) {
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: 'INVALID_JSON' }, { status: 400 });
  }

  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return NextResponse.json({ error: 'INVALID_BODY' }, { status: 400 });
  }

  const measurements = (payload as { measurements?: unknown }).measurements;
  if (!Array.isArray(measurements)) {
    return NextResponse.json(
      { error: 'MEASUREMENTS_REQUIRED', detail: 'Body must include a measurements array.' },
      { status: 400 },
    );
  }

  const validationErrors = measurements.flatMap((candidate, index) => {
    if (!candidate || typeof candidate !== 'object' || Array.isArray(candidate)) {
      return [{ index, message: 'measurement must be an object' }];
    }
    return validatePilotMeasurement(candidate as PilotServiceMeasurement)
      .map(message => ({ index, message }));
  });

  if (validationErrors.length) {
    return NextResponse.json(
      {
        error: 'INVALID_MEASUREMENTS',
        validationErrors,
        evidencePromotionBlocked: true,
      },
      { status: 400 },
    );
  }

  const typed = measurements as PilotServiceMeasurement[];
  const scorecard = scoreFoodWastePilot(typed);
  return NextResponse.json({
    scorecard,
    protocolVersion: FOOD_WASTE_PILOT_PROTOCOL.version,
    decisionPolicyVersion: FOOD_DECISION_POLICY.version,
    evidencePromotion: {
      dataQualityPassed: scorecard.gates.dataQualityPassed,
      enoughEvidence: scorecard.gates.enoughEvidence,
      promotableAsPilotResult: scorecard.status !== 'INSUFFICIENT_EVIDENCE',
      promotableAsGeneralizedClimateImpact: false,
    },
    claimBoundary: FOOD_WASTE_PILOT_PROTOCOL.evidenceBoundary,
  });
}
