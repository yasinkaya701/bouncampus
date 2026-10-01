import type { CampusDecision } from './campus-contracts';

export type BuildingEnergyScenario = {
  building_id: string;
  building_name?: string;
  baseline_kwh: number;
  optimized_kwh: number;
  saving_kwh: number;
  saving_percent?: number;
  savings?: {
    kwh_saved?: number;
    cost_saved_tl?: number;
    co2_avoided_kg?: number;
  };
};

export type BuildingReviewContext = {
  scheduleSourceUrl: string;
  weatherSource: string;
  scheduleSnapshotStale?: boolean;
  nowIso?: string;
};

export type BuildingReviewRecommendation = {
  buildingId: string;
  buildingName: string;
  mode: 'FIELD_VERIFICATION_ONLY';
  modeledBaselineKwh: number;
  modeledOptimizedKwh: number;
  modeledSavingPotentialKwh: number;
  modeledSavingPercent: number;
  nextChecks: string[];
  prohibitedAutomaticActions: string[];
};

function finiteNonNegative(value: number): boolean {
  return Number.isFinite(value) && value >= 0;
}

function validScenario(item: BuildingEnergyScenario): boolean {
  return Boolean(item.building_id?.trim())
    && finiteNonNegative(item.baseline_kwh)
    && finiteNonNegative(item.optimized_kwh)
    && finiteNonNegative(item.saving_kwh)
    && item.optimized_kwh <= item.baseline_kwh + 0.0001;
}

function stableCompare(left: BuildingEnergyScenario, right: BuildingEnergyScenario): number {
  if (right.saving_kwh !== left.saving_kwh) return right.saving_kwh - left.saving_kwh;
  const leftPct = left.baseline_kwh > 0 ? left.saving_kwh / left.baseline_kwh : 0;
  const rightPct = right.baseline_kwh > 0 ? right.saving_kwh / right.baseline_kwh : 0;
  if (rightPct !== leftPct) return rightPct - leftPct;
  return left.building_id < right.building_id ? -1 : left.building_id > right.building_id ? 1 : 0;
}

export function recommendBuildingReview(
  scenarios: BuildingEnergyScenario[],
  context: BuildingReviewContext,
): CampusDecision<BuildingReviewRecommendation> {
  const generatedAt = context.nowIso ?? new Date().toISOString();
  const limitations = [
    'NO_BUILDING_METER_CALIBRATION',
    'NO_LIVE_ROOM_OCCUPANCY',
    'NO_BMS_CONTROL_CONNECTION',
    'NO_AUTOMATIC_HVAC_OR_LIGHTING_ACTUATION',
    'SCHEDULE_DERIVED_OCCUPANCY_ESTIMATE',
  ];
  const provenance = [
    {
      sourceClass: 'OFFICIAL_SNAPSHOT' as const,
      sourceId: context.scheduleSourceUrl || 'course-schedule-snapshot',
      note: 'Instructional schedule is used as context; it does not measure physical occupancy.',
    },
    {
      sourceClass: 'MODEL_ESTIMATE' as const,
      sourceId: 'campus-calculations.computeBuildingOccupancy',
      note: 'Student counts and room capacities include deterministic heuristics rather than access-control or sensor counts.',
    },
    {
      sourceClass: 'SCENARIO' as const,
      sourceId: 'campus-calculations.computeBuildingEnergy',
      note: 'Energy values are modeled counterfactuals, not meter-verified consumption or achieved savings.',
    },
    {
      sourceClass: context.weatherSource.toLowerCase().includes('fallback') ? 'SCENARIO' as const : 'OFFICIAL_PUBLIC' as const,
      sourceId: context.weatherSource || 'weather-source-unknown',
      note: 'Weather affects modeled HVAC load only; it does not validate building controls.',
    },
  ];

  const candidates = scenarios.filter(validScenario).sort(stableCompare);
  const selected = candidates.find(item => item.saving_kwh > 0);
  if (!selected) {
    return {
      decisionId: 'energy:building-review:none',
      domain: 'ENERGY',
      generatedAt,
      readiness: 'WITHHOLD',
      abstained: true,
      operatorApprovalRequired: true,
      automaticDispatchAllowed: false,
      reasonCodes: ['NO_BUILDING_ENERGY_SCENARIO'],
      limitations,
      provenance,
      recommendation: null,
    };
  }

  const modeledSavingPercent = selected.baseline_kwh > 0
    ? Math.round((selected.saving_kwh / selected.baseline_kwh) * 1000) / 10
    : 0;
  const reasonCodes = [
    'MODEL_SCENARIO_NOT_METERED_SAVINGS',
    'FIELD_VERIFICATION_REQUIRED',
    'HUMAN_APPROVAL_REQUIRED',
  ];
  if (context.scheduleSnapshotStale) reasonCodes.push('COURSE_SNAPSHOT_REFRESH_REQUIRED');
  if (context.weatherSource.toLowerCase().includes('fallback')) reasonCodes.push('WEATHER_FALLBACK_ASSUMPTION');

  return {
    decisionId: `energy:building-review:${selected.building_id}`,
    domain: 'ENERGY',
    generatedAt,
    readiness: 'REVIEW_REQUIRED',
    abstained: false,
    operatorApprovalRequired: true,
    automaticDispatchAllowed: false,
    reasonCodes,
    limitations,
    provenance,
    recommendation: {
      buildingId: selected.building_id,
      buildingName: selected.building_name ?? selected.building_id,
      mode: 'FIELD_VERIFICATION_ONLY',
      modeledBaselineKwh: selected.baseline_kwh,
      modeledOptimizedKwh: selected.optimized_kwh,
      modeledSavingPotentialKwh: selected.saving_kwh,
      modeledSavingPercent,
      nextChecks: [
        'Verify actual room use and critical activities with facilities staff.',
        'Compare the candidate period against sub-meter or BMS data if available.',
        'Confirm comfort, ventilation, accessibility and equipment constraints before any operational change.',
        'Record measured baseline and post-intervention energy before claiming savings.',
      ],
      prohibitedAutomaticActions: [
        'Do not close floors automatically.',
        'Do not change HVAC setpoints automatically.',
        'Do not switch lighting or ventilation automatically.',
        'Do not report modeled saving potential as achieved impact.',
      ],
    },
  };
}
