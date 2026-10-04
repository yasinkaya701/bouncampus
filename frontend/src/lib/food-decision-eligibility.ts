import type { ProductionDecisionBand } from './food-waste';

export type MethodEligibility =
  | 'SANDBOX_ONLY'
  | 'EVALUATED_OFFLINE'
  | 'PILOT_ELIGIBLE'
  | 'PILOT_EVALUATED'
  | 'RETIRED';

export type EligibilityAwareProductionDecision = Omit<ProductionDecisionBand, 'recommendedTarget'> & {
  recommendedTarget: number | null;
  methodEligibility: MethodEligibility;
};

export type MethodEligibilityOptions = {
  methodEligibility: MethodEligibility;
};

function withReason(reasonCodes: string[], code: string) {
  return reasonCodes.includes(code) ? reasonCodes : [code, ...reasonCodes];
}

export function applyMethodEligibility(
  band: ProductionDecisionBand,
  { methodEligibility }: MethodEligibilityOptions,
): EligibilityAwareProductionDecision {
  const base: EligibilityAwareProductionDecision = {
    ...band,
    methodEligibility,
  };

  if (methodEligibility === 'SANDBOX_ONLY') {
    return {
      ...base,
      decisionReadiness: 'WITHHOLD',
      abstained: true,
      recommendedTarget: null,
      reasonCodes: withReason(base.reasonCodes, 'METHOD_SANDBOX_ONLY'),
    };
  }

  if (methodEligibility === 'RETIRED') {
    return {
      ...base,
      decisionReadiness: 'WITHHOLD',
      abstained: true,
      recommendedTarget: null,
      reasonCodes: withReason(base.reasonCodes, 'METHOD_RETIRED'),
    };
  }

  if (methodEligibility === 'EVALUATED_OFFLINE' && base.decisionReadiness !== 'WITHHOLD') {
    return {
      ...base,
      decisionReadiness: 'REVIEW_REQUIRED',
      abstained: false,
      reasonCodes: withReason(base.reasonCodes, 'METHOD_NOT_YET_PILOT_ELIGIBLE'),
    };
  }

  return base;
}
