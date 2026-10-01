import type { EligibilityAwareProductionDecision } from './food-decision-eligibility';

export const REACHABILITY_POLICY_VERSION = 'decision-reachability-v1.1' as const;

export type DecisionReachabilityStatus = 'REACHABLE' | 'UNVERIFIED' | 'UNREACHABLE';

export type DecisionReachabilityEvidence = {
  decisionSurface?: string | null;
  decisionSurfaceVerified?: boolean | null;
  operatorAuthorityConfirmed?: boolean | null;
  minutesBeforeFreeze?: number | null;
  changeFeasibleBeforeFreeze?: boolean | null;
};

export type ReachabilityAwareProductionDecision = EligibilityAwareProductionDecision & {
  reachabilityPolicyVersion: typeof REACHABILITY_POLICY_VERSION;
  decisionReachabilityStatus: DecisionReachabilityStatus;
  decisionSurface: string | null;
  decisionSurfaceVerified: boolean | null;
  operatorAuthorityConfirmed: boolean | null;
  minutesBeforeFreeze: number | null;
  changeFeasibleBeforeFreeze: boolean | null;
};

function normalizeOptionalBoolean(value: unknown): boolean | null {
  return typeof value === 'boolean' ? value : null;
}

function normalizeMinutes(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

function normalizeSurface(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  const normalized = value.trim().toUpperCase();
  return normalized || null;
}

function appendReasons(existing: string[], additions: string[]) {
  const next = [...existing];
  additions.forEach(code => {
    if (!next.includes(code)) next.push(code);
  });
  return next;
}

export function applyDecisionReachability(
  decision: EligibilityAwareProductionDecision,
  evidence?: DecisionReachabilityEvidence | null,
): ReachabilityAwareProductionDecision {
  if (evidence == null) {
    const decisionReadiness = decision.decisionReadiness === 'PILOT_READY'
      ? 'REVIEW_REQUIRED'
      : decision.decisionReadiness;

    return {
      ...decision,
      reachabilityPolicyVersion: REACHABILITY_POLICY_VERSION,
      decisionReachabilityStatus: 'UNVERIFIED',
      decisionSurface: null,
      decisionSurfaceVerified: null,
      operatorAuthorityConfirmed: null,
      minutesBeforeFreeze: null,
      changeFeasibleBeforeFreeze: null,
      decisionReadiness,
      abstained: decisionReadiness === 'WITHHOLD',
      recommendedTarget: decisionReadiness === 'WITHHOLD' ? null : decision.recommendedTarget,
      reasonCodes: appendReasons(decision.reasonCodes, ['DECISION_REACHABILITY_UNVERIFIED']),
    };
  }

  const decisionSurface = normalizeSurface(evidence.decisionSurface);
  const decisionSurfaceVerified = normalizeOptionalBoolean(evidence.decisionSurfaceVerified);
  const operatorAuthorityConfirmed = normalizeOptionalBoolean(evidence.operatorAuthorityConfirmed);
  const minutesBeforeFreeze = normalizeMinutes(evidence.minutesBeforeFreeze);
  const changeFeasibleBeforeFreeze = normalizeOptionalBoolean(
    evidence.changeFeasibleBeforeFreeze,
  );

  const reasons: string[] = [];
  let hardBlock = false;

  if (decisionSurface == null) reasons.push('DECISION_SURFACE_UNSPECIFIED');
  if (decisionSurfaceVerified !== true) reasons.push('DECISION_SURFACE_UNVERIFIED');

  if (operatorAuthorityConfirmed === false) {
    reasons.push('DECISION_AUTHORITY_DENIED');
    hardBlock = true;
  } else if (operatorAuthorityConfirmed == null) {
    reasons.push('DECISION_AUTHORITY_UNKNOWN');
  }

  if (minutesBeforeFreeze == null) {
    reasons.push('DECISION_FREEZE_TIME_UNKNOWN');
  } else if (minutesBeforeFreeze <= 0) {
    reasons.push('DECISION_WINDOW_CLOSED');
    hardBlock = true;
  }

  if (changeFeasibleBeforeFreeze === false) {
    reasons.push('DECISION_CHANGE_NOT_FEASIBLE_BEFORE_FREEZE');
    hardBlock = true;
  } else if (changeFeasibleBeforeFreeze == null) {
    reasons.push('DECISION_CHANGE_FEASIBILITY_UNKNOWN');
  }

  let decisionReachabilityStatus: DecisionReachabilityStatus;
  if (hardBlock) decisionReachabilityStatus = 'UNREACHABLE';
  else if (reasons.length > 0) decisionReachabilityStatus = 'UNVERIFIED';
  else {
    decisionReachabilityStatus = 'REACHABLE';
    reasons.push('DECISION_REACHABLE_BEFORE_FREEZE');
  }

  let decisionReadiness = decision.decisionReadiness;
  if (decisionReachabilityStatus === 'UNREACHABLE') decisionReadiness = 'WITHHOLD';
  else if (
    decisionReachabilityStatus === 'UNVERIFIED'
    && decisionReadiness === 'PILOT_READY'
  ) decisionReadiness = 'REVIEW_REQUIRED';

  const abstained = decisionReadiness === 'WITHHOLD';

  return {
    ...decision,
    reachabilityPolicyVersion: REACHABILITY_POLICY_VERSION,
    decisionReachabilityStatus,
    decisionSurface,
    decisionSurfaceVerified,
    operatorAuthorityConfirmed,
    minutesBeforeFreeze,
    changeFeasibleBeforeFreeze,
    decisionReadiness,
    abstained,
    recommendedTarget: abstained ? null : decision.recommendedTarget,
    reasonCodes: appendReasons(decision.reasonCodes, reasons),
  };
}
