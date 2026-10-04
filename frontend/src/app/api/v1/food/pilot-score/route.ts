import { NextResponse } from 'next/server';
import {
  FOOD_DECISION_POLICY,
  scoreFoodWastePilot,
} from '@/lib/food-waste';
import { summarizeMatchedPilotEffects } from '@/lib/food-pilot-pair-effects';
import {
  MATCHED_FOOD_WASTE_PILOT_PROTOCOL,
  analyzeMatchedPilotDesign,
  normalizeMatchedPilotMeasurement,
  validateMatchedPilotMeasurement,
  type MatchedPilotServiceMeasurement,
} from '@/lib/food-pilot-matching';

export async function GET() {
  return NextResponse.json({
    endpoint: 'POST /api/v1/food/pilot-score',
    protocol: MATCHED_FOOD_WASTE_PILOT_PROTOCOL,
    decisionPolicyVersion: FOOD_DECISION_POLICY.version,
    requestShape: {
      measurements: MATCHED_FOOD_WASTE_PILOT_PROTOCOL.measurementFields,
      acceptedNaming: ['snake_case', 'camelCase'],
    },
    evidencePromotion: {
      inputEvidenceClass: 'MEASURED_PILOT_DATA',
      outputEvidenceClass: 'PILOT_SCORECARD',
      generalizedImpactClaimAllowed: false,
      requiredChecks: [
        'row-level measurement validity',
        'pair_id present on every row',
        'exactly one CONTROL and one INTERVENTION service per pair_id',
        'no duplicate pair_id + arm combinations',
        'minimum matched pairs',
        'matched-pair normalized-waste effect summary',
        'duplicate service detection',
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

  const normalizedMeasurements = measurements.map(candidate => {
    if (!candidate || typeof candidate !== 'object' || Array.isArray(candidate)) return candidate;
    return normalizeMatchedPilotMeasurement(candidate as Record<string, unknown>);
  });

  const validationErrors = normalizedMeasurements.flatMap((candidate, index) => {
    if (!candidate || typeof candidate !== 'object' || Array.isArray(candidate)) {
      return [{ index, message: 'measurement must be an object' }];
    }
    return validateMatchedPilotMeasurement(candidate as MatchedPilotServiceMeasurement)
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

  const typed = normalizedMeasurements as MatchedPilotServiceMeasurement[];
  const matching = analyzeMatchedPilotDesign(typed);
  if (!matching.structurePassed) {
    return NextResponse.json(
      {
        error: 'INVALID_MATCHED_DESIGN',
        matching,
        detail: MATCHED_FOOD_WASTE_PILOT_PROTOCOL.matchingRule,
        evidencePromotionBlocked: true,
      },
      { status: 400 },
    );
  }

  const scorecard = scoreFoodWastePilot(typed);
  const pairedEffects = summarizeMatchedPilotEffects(typed);
  const minimumMatchedPairs = MATCHED_FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMatchedPairs;
  const enoughMatchedPairs = matching.matchedPairCount >= minimumMatchedPairs;
  const pairEffectsComplete = pairedEffects.matchedPairCount === matching.matchedPairCount;
  const promotableAsPilotResult =
    enoughMatchedPairs
    && pairEffectsComplete
    && scorecard.gates.dataQualityPassed
    && scorecard.gates.enoughEvidence
    && scorecard.status !== 'INSUFFICIENT_EVIDENCE';

  return NextResponse.json({
    scorecard,
    pairedEffects,
    matching: {
      ...matching,
      minimumMatchedPairs,
      enoughMatchedPairs,
      pairEffectsComplete,
    },
    protocolVersion: MATCHED_FOOD_WASTE_PILOT_PROTOCOL.version,
    decisionPolicyVersion: FOOD_DECISION_POLICY.version,
    evidencePromotion: {
      dataQualityPassed:
        scorecard.gates.dataQualityPassed && matching.structurePassed && pairEffectsComplete,
      enoughEvidence: scorecard.gates.enoughEvidence && enoughMatchedPairs,
      promotableAsPilotResult,
      promotableAsGeneralizedClimateImpact: false,
    },
    claimBoundary: MATCHED_FOOD_WASTE_PILOT_PROTOCOL.evidenceBoundary,
  });
}
