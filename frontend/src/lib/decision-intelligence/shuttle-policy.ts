import type { CampusDecision } from './campus-contracts';

export type ShuttleDecisionStop = {
  id: string;
};

export type ShuttleDecisionRoute = {
  id: string;
  stopIds: string[];
  distanceKmEstimate: number;
  bidirectional?: boolean;
  officialScheduleUrl?: string;
};

export type ShuttleDecisionNetwork = {
  source?: { url?: string };
  stops: ShuttleDecisionStop[];
  routes: ShuttleDecisionRoute[];
};

export type ShuttlePolicyOptions = {
  transferPenaltyKm?: number;
  maxTransfers?: 0 | 1;
  nowIso?: string;
};

export type ShuttleItineraryRecommendation = {
  originStopId: string;
  destinationStopId: string;
  routeIds: string[];
  transferStopIds: string[];
  transfers: number;
  estimatedDistanceKm: number;
  policyScore: number;
  officialScheduleUrl: string | null;
  timingStatus: 'OFFICIAL_TIMETABLE_LOOKUP_REQUIRED';
  telemetryStatus: 'NOT_CONNECTED';
};

type Candidate = {
  routeIds: string[];
  transferStopIds: string[];
  transfers: number;
  estimatedDistanceKm: number;
  policyScore: number;
  officialScheduleUrl: string | null;
};

function segmentDistanceKm(route: ShuttleDecisionRoute, fromStopId: string, toStopId: string): number | null {
  const fromIndex = route.stopIds.indexOf(fromStopId);
  const toIndex = route.stopIds.indexOf(toStopId);
  if (fromIndex < 0 || toIndex < 0 || fromIndex === toIndex) return null;
  if (fromIndex > toIndex && !route.bidirectional) return null;

  const edgeCount = Math.max(1, route.stopIds.length - 1);
  const traversedEdges = Math.abs(toIndex - fromIndex);
  const routeDistance = Number.isFinite(route.distanceKmEstimate) && route.distanceKmEstimate >= 0
    ? route.distanceKmEstimate
    : 0;
  return routeDistance * (traversedEdges / edgeCount);
}

function directCandidates(
  network: ShuttleDecisionNetwork,
  originStopId: string,
  destinationStopId: string,
): Candidate[] {
  return network.routes.flatMap(route => {
    const distance = segmentDistanceKm(route, originStopId, destinationStopId);
    if (distance === null) return [];
    return [{
      routeIds: [route.id],
      transferStopIds: [],
      transfers: 0,
      estimatedDistanceKm: distance,
      policyScore: distance,
      officialScheduleUrl: route.officialScheduleUrl ?? network.source?.url ?? null,
    }];
  });
}

function transferCandidates(
  network: ShuttleDecisionNetwork,
  originStopId: string,
  destinationStopId: string,
  transferPenaltyKm: number,
): Candidate[] {
  const candidates: Candidate[] = [];

  for (const firstRoute of network.routes) {
    for (const secondRoute of network.routes) {
      if (firstRoute.id === secondRoute.id) continue;

      for (const transferStopId of firstRoute.stopIds) {
        if (transferStopId === originStopId || transferStopId === destinationStopId) continue;
        if (!secondRoute.stopIds.includes(transferStopId)) continue;

        const firstDistance = segmentDistanceKm(firstRoute, originStopId, transferStopId);
        const secondDistance = segmentDistanceKm(secondRoute, transferStopId, destinationStopId);
        if (firstDistance === null || secondDistance === null) continue;

        const estimatedDistanceKm = firstDistance + secondDistance;
        candidates.push({
          routeIds: [firstRoute.id, secondRoute.id],
          transferStopIds: [transferStopId],
          transfers: 1,
          estimatedDistanceKm,
          policyScore: estimatedDistanceKm + transferPenaltyKm,
          officialScheduleUrl:
            firstRoute.officialScheduleUrl
            ?? secondRoute.officialScheduleUrl
            ?? network.source?.url
            ?? null,
        });
      }
    }
  }

  return candidates;
}

function candidateKey(candidate: Candidate): string {
  return `${candidate.routeIds.join('>')}|${candidate.transferStopIds.join('>')}`;
}

export function recommendShuttleItinerary(
  network: ShuttleDecisionNetwork,
  originStopId: string,
  destinationStopId: string,
  options: ShuttlePolicyOptions = {},
): CampusDecision<ShuttleItineraryRecommendation> {
  const generatedAt = options.nowIso ?? new Date().toISOString();
  const decisionId = `shuttle:${originStopId || 'unknown'}:${destinationStopId || 'unknown'}`;
  const stopIds = new Set(network.stops.map(stop => stop.id));
  const provenance = [{
    sourceClass: 'OFFICIAL_PUBLIC' as const,
    sourceId: network.source?.url ?? 'shuttle-network-snapshot',
    note: 'Route topology only; departure timing remains authoritative at the official timetable.',
  }];
  const limitations = [
    'NO_LIVE_SHUTTLE_GPS',
    'NO_LIVE_SHUTTLE_OCCUPANCY',
    'NO_VERIFIED_REAL_TIME_ETA',
  ];

  if (!stopIds.has(originStopId)) {
    return {
      decisionId,
      domain: 'SHUTTLE',
      generatedAt,
      readiness: 'WITHHOLD',
      abstained: true,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes: ['UNKNOWN_ORIGIN_STOP'],
      limitations,
      provenance,
      recommendation: null,
    };
  }

  if (!stopIds.has(destinationStopId)) {
    return {
      decisionId,
      domain: 'SHUTTLE',
      generatedAt,
      readiness: 'WITHHOLD',
      abstained: true,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes: ['UNKNOWN_DESTINATION_STOP'],
      limitations,
      provenance,
      recommendation: null,
    };
  }

  if (originStopId === destinationStopId) {
    return {
      decisionId,
      domain: 'SHUTTLE',
      generatedAt,
      readiness: 'WITHHOLD',
      abstained: true,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes: ['NO_TRIP_REQUIRED'],
      limitations,
      provenance,
      recommendation: null,
    };
  }

  const transferPenaltyKm = Number.isFinite(options.transferPenaltyKm)
    ? Math.max(0, options.transferPenaltyKm ?? 3)
    : 3;
  const maxTransfers = options.maxTransfers ?? 1;
  const candidates = directCandidates(network, originStopId, destinationStopId);
  if (maxTransfers === 1) {
    candidates.push(...transferCandidates(network, originStopId, destinationStopId, transferPenaltyKm));
  }

  candidates.sort((left, right) =>
    left.policyScore - right.policyScore
    || left.transfers - right.transfers
    || candidateKey(left).localeCompare(candidateKey(right))
  );

  const selected = candidates[0];
  if (!selected) {
    return {
      decisionId,
      domain: 'SHUTTLE',
      generatedAt,
      readiness: 'WITHHOLD',
      abstained: true,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes: ['NO_FEASIBLE_SHUTTLE_PATH'],
      limitations,
      provenance,
      recommendation: null,
    };
  }

  return {
    decisionId,
    domain: 'SHUTTLE',
    generatedAt,
    readiness: 'REVIEW_REQUIRED',
    abstained: false,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes: ['OFFICIAL_TIMETABLE_CHECK_REQUIRED', 'ROUTE_TOPOLOGY_RECOMMENDATION_ONLY'],
    limitations,
    provenance: [
      ...provenance,
      {
        sourceClass: 'POLICY_HEURISTIC',
        sourceId: 'cs1-shuttle-topology-policy-v1',
        note: `Transfer penalty ${transferPenaltyKm} km-equivalent; not learned from rider outcomes.`,
      },
    ],
    recommendation: {
      originStopId,
      destinationStopId,
      routeIds: selected.routeIds,
      transferStopIds: selected.transferStopIds,
      transfers: selected.transfers,
      estimatedDistanceKm: Number(selected.estimatedDistanceKm.toFixed(2)),
      policyScore: Number(selected.policyScore.toFixed(2)),
      officialScheduleUrl: selected.officialScheduleUrl,
      timingStatus: 'OFFICIAL_TIMETABLE_LOOKUP_REQUIRED',
      telemetryStatus: 'NOT_CONNECTED',
    },
  };
}
