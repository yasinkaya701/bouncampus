import { NextResponse } from 'next/server';
import {
  buildProductionBand,
  CURRENT_RECOVERY_RATE_PCT,
  FOOD_DECISION_POLICY,
  FOOD_WASTE_2025,
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  SKS_ACTIVITY_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
  type DemandSignalId,
} from '@/lib/food-waste';
import { applyMethodEligibility } from '@/lib/food-decision-eligibility';

const PLANNING_CANDIDATE_SEMANTICS = 'ADVISORY_MODEL_ESTIMATE_NOT_AUTHORIZED_KITCHEN_ORDER' as const;

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const dateVal = requestUrl.searchParams.get('date_val');
  if (dateVal) dashboardUrl.searchParams.set('date_val', dateVal);

  let predictedMeals = 0;
  let baselinePredictedMeals = 0;
  let dashboardAvailable = false;
  let menuAdjustment: Record<string, unknown> | null = null;
  let signalAvailability: Partial<Record<DemandSignalId, boolean>> = {};

  try {
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (response.ok) {
      const dashboard = await response.json();
      predictedMeals = Number(dashboard.food_demand_meals ?? 0);
      baselinePredictedMeals = Number(dashboard.food_demand_baseline_meals ?? predictedMeals);
      menuAdjustment = dashboard.food_menu_adjustment && typeof dashboard.food_menu_adjustment === 'object'
        ? dashboard.food_menu_adjustment
        : null;
      dashboardAvailable = true;

      const sources = Array.isArray(dashboard.sources) ? dashboard.sources : [];
      signalAvailability = {
        schedule: Number(dashboard.real_courses_loaded ?? 0) > 0,
        weather: Boolean(dashboard.live_weather?.provenance?.ok),
        menu: Boolean(dashboard.live_menu?.provenance?.ok),
        calendar: sources.some(
          (source: { id?: string; ok?: boolean }) =>
            Boolean(source.ok) && String(source.id ?? '').toLowerCase().includes('calendar'),
        ),
      };
    }
  } catch {
    // Historical public-source context remains usable even if the model dashboard is unavailable.
  }

  const preventionRatePct = Number(requestUrl.searchParams.get('prevention_rate_pct') ?? 15);
  const recoveryRatePct = Number(requestUrl.searchParams.get('recovery_rate_pct') ?? 85);
  const sourceAssessment = buildProductionBand(predictedMeals, signalAvailability);
  const decisionAssessment = applyMethodEligibility(sourceAssessment, {
    methodEligibility: 'SANDBOX_ONLY',
  });
  const productionBand = decisionAssessment.abstained ? null : decisionAssessment;
  const planningCandidate = dashboardAvailable && sourceAssessment.predictedMeals > 0
    ? {
        portions: sourceAssessment.predictedMeals,
        baselinePortions: Math.max(0, Math.round(baselinePredictedMeals)),
        lowerBound: sourceAssessment.lowerBound,
        upperBound: sourceAssessment.upperBound,
        signalCoveragePct: sourceAssessment.signalCoveragePct,
        sourceReadiness: sourceAssessment.decisionReadiness,
        methodEligibility: decisionAssessment.methodEligibility,
        menuAdjustment,
        semantics: PLANNING_CANDIDATE_SEMANTICS,
        operatorApprovalRequired: true,
        automaticKitchenDispatch: false,
      }
    : null;

  return NextResponse.json({
    contractVersion: 'food-intelligence-v1.2',
    baseline: {
      ...FOOD_WASTE_BASELINE,
      currentRecoveryRatePct: Number(CURRENT_RECOVERY_RATE_PCT.toFixed(1)),
      yearOverYearReductionPct: Number(YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)),
      monthly2025: FOOD_WASTE_2025,
      source: FOOD_WASTE_SOURCE,
      evidenceClass: 'PUBLIC_SOURCE',
    },
    demandContext: {
      available: dashboardAvailable && decisionAssessment.predictedMeals > 0,
      actionable: dashboardAvailable && !decisionAssessment.abstained,
      planningCandidate,
      productionBand,
      decisionAssessment,
      provenance: FOOD_DECISION_POLICY.forecastProvenance,
      methodEligibility: decisionAssessment.methodEligibility,
      note: 'The planningCandidate is a menu-adjusted advisory model estimate and remains visible for diagnosis even when method eligibility withholds an actionable production recommendation. It is not cafeteria POS, production, served-meal telemetry, or an authorized kitchen order.',
    },
    decisionPolicy: {
      version: FOOD_DECISION_POLICY.version,
      provenance: FOOD_DECISION_POLICY.provenance,
      forecastProvenance: FOOD_DECISION_POLICY.forecastProvenance,
      bandSemantics: FOOD_DECISION_POLICY.bandSemantics,
      calibrationStatus: FOOD_DECISION_POLICY.calibrationStatus,
      signalWeightsPct: FOOD_DECISION_POLICY.signalWeightsPct,
      requiredSignals: FOOD_DECISION_POLICY.requiredSignals,
      reviewMinCoveragePct: FOOD_DECISION_POLICY.reviewMinCoveragePct,
      pilotReadyMinCoveragePct: FOOD_DECISION_POLICY.pilotReadyMinCoveragePct,
      humanApprovalRequired: FOOD_DECISION_POLICY.operatorApprovalRequired,
      automaticKitchenDispatch: FOOD_DECISION_POLICY.autoDispatchAllowed,
      limitations: FOOD_DECISION_POLICY.limitations,
      withholdRule: 'WITHHOLD when there is no positive demand estimate, a required source is unavailable, or the selected method is SANDBOX_ONLY/RETIRED.',
      pilotRule: 'PILOT_READY additionally requires a method explicitly promoted to PILOT_ELIGIBLE or PILOT_EVALUATED; source coverage alone can never promote a sandbox model.',
    },
    baselineEvaluation: {
      status: 'READY_FOR_MEASURED_DATA',
      currentMethodEligibility: decisionAssessment.methodEligibility,
      evidenceClass: 'TECH_TEST',
      candidates: [
        'previous comparable service',
        'expanding historical mean',
        'rolling historical mean',
        'same-cycle seasonal lag',
        'operator estimate when captured',
        'food-demand model point estimate',
      ],
      metrics: ['MAE', 'RMSE', 'WAPE', 'mean error'],
      leakageRule: 'Every baseline forecast must use only observations available before the target service.',
      comparisonRule: 'All candidates must be ranked on identical common-support service rows; missing hard cases cannot be silently dropped by one method.',
      claimBoundary: 'Offline forecast metrics do not demonstrate food-waste reduction or climate impact.',
    },
    pilotContract: FOOD_WASTE_PILOT_PROTOCOL,
    scenario: {
      ...simulateFoodWasteScenario(preventionRatePct, recoveryRatePct),
      evidenceClass: 'SCENARIO',
      achievedImpact: false,
      note: 'Counterfactual scenario only; values are not measured BOUNCAMPUS savings.',
    },
    sources: [FOOD_WASTE_SOURCE, SKS_ACTIVITY_SOURCE],
    claimPolicy: {
      allowedNow: [
        'official historical food-waste baseline',
        'source health and provenance',
        'sandbox model-estimated next-service demand for diagnostic use',
        'menu-adjusted advisory planning candidate explicitly marked as non-actionable',
        'POLICY_HEURISTIC planning range for diagnostic use',
        'decision readiness, method eligibility, and abstention state',
        'offline baseline/model evaluation explicitly labeled TECH_TEST',
        'scenario outputs explicitly labeled as scenarios',
        'pre-registered pilot targets and formulas',
      ],
      forbiddenUntilMeasured: [
        'food waste saved by BOUNCAMPUS',
        'cost saved by BOUNCAMPUS food decisions',
        'CO2 or water saved by BOUNCAMPUS',
        'actual cafeteria production optimized',
        'actual student demand observed',
        'calibrated confidence interval unless calibration is measured and documented',
        'PILOT_READY from a SANDBOX_ONLY or merely EVALUATED_OFFLINE method',
      ],
    },
    truthBoundary: {
      official: [
        '2024 and 2025 annual food-waste totals',
        '2025 monthly waste/recovery values',
        'campus dining-service scale and published dining-hall capacity',
      ],
      modeled: [
        'next-service meal demand',
        'menu-adjusted advisory planning candidate',
      ],
      policyHeuristic: [
        'menu popularity adjustment',
        'signal weights',
        'planning range width',
        'decision readiness thresholds',
      ],
      measuredPilot: [],
      unavailable: [
        'cafeteria POS transactions',
        'actual produced portions by service',
        'actual served portions by service',
        'plate-waste measurements by menu item',
        'calibrated forecast interval coverage',
      ],
    },
  });
}
