export type CampusDecisionDomain = 'FOOD' | 'SHUTTLE' | 'SPACE' | 'ENERGY' | 'OCCUPANCY';

export type CampusDecisionReadiness = 'READY' | 'REVIEW_REQUIRED' | 'WITHHOLD';

export type CampusProvenanceClass =
  | 'OFFICIAL_PUBLIC'
  | 'OFFICIAL_SNAPSHOT'
  | 'DERIVED_SNAPSHOT'
  | 'USER_SUPPLIED'
  | 'POLICY_HEURISTIC'
  | 'MODEL_ESTIMATE'
  | 'SCENARIO'
  | 'UNAVAILABLE';

export type CampusProvenance = {
  sourceClass: CampusProvenanceClass;
  sourceId: string;
  note?: string;
};

export type CampusDecision<TRecommendation> = {
  decisionId: string;
  domain: CampusDecisionDomain;
  generatedAt: string;
  readiness: CampusDecisionReadiness;
  abstained: boolean;
  operatorApprovalRequired: true;
  automaticDispatchAllowed: false;
  reasonCodes: string[];
  limitations: string[];
  provenance: CampusProvenance[];
  recommendation: TRecommendation | null;
};

export function withheldDecision<TRecommendation>(input: {
  decisionId: string;
  domain: CampusDecisionDomain;
  generatedAt?: string;
  reasonCodes: string[];
  limitations?: string[];
  provenance?: CampusProvenance[];
}): CampusDecision<TRecommendation> {
  return {
    decisionId: input.decisionId,
    domain: input.domain,
    generatedAt: input.generatedAt ?? new Date().toISOString(),
    readiness: 'WITHHOLD',
    abstained: true,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes: input.reasonCodes,
    limitations: input.limitations ?? [],
    provenance: input.provenance ?? [],
    recommendation: null,
  };
}
