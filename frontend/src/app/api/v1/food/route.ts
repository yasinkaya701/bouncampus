import { NextResponse } from 'next/server';
import {
  buildProductionBand,
  CURRENT_RECOVERY_RATE_PCT,
  FOOD_WASTE_2025,
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  SKS_ACTIVITY_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
  type DemandSignalId,
} from '@/lib/food-waste';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const dateVal = requestUrl.searchParams.get('date_val');
  if (dateVal) dashboardUrl.searchParams.set('date_val', dateVal);

  let predictedMeals = 0;
  let dashboardAvailable = false;
  let signalAvailability: Partial<Record<DemandSignalId, boolean>> = {};

  try {
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (response.ok) {
      const dashboard = await response.json();
      predictedMeals = Number(dashboard.food_demand_meals ?? 0);
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
    // The official historical baseline remains usable even if the live/model dashboard is unavailable.
  }

  const preventionRatePct = Number(requestUrl.searchParams.get('prevention_rate_pct') ?? 15);
  const recoveryRatePct = Number(requestUrl.searchParams.get('recovery_rate_pct') ?? 85);
  const productionBand = buildProductionBand(predictedMeals, signalAvailability);

  return NextResponse.json({
    baseline: {
      ...FOOD_WASTE_BASELINE,
      currentRecoveryRatePct: Number(CURRENT_RECOVERY_RATE_PCT.toFixed(1)),
      yearOverYearReductionPct: Number(YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)),
      monthly2025: FOOD_WASTE_2025,
      source: FOOD_WASTE_SOURCE,
    },
    demandContext: {
      available: dashboardAvailable && Boolean(productionBand),
      productionBand,
      provenance: 'MODEL_ESTIMATE',
      note: 'Schedule/weather/menu/calendar-derived planning context; not cafeteria POS, production, or served-meal telemetry.',
    },
    decisionPolicy: {
      humanApprovalRequired: true,
      automaticKitchenDispatch: false,
      withholdRule: 'WITHHOLD when the course-schedule backbone is unavailable or contextual signal coverage is insufficient.',
      pilotRule: 'PILOT_READY means safe to test with operator review; it does not mean the forecast has been validated against cafeteria POS.',
    },
    pilotContract: FOOD_WASTE_PILOT_PROTOCOL,
    scenario: simulateFoodWasteScenario(preventionRatePct, recoveryRatePct),
    sources: [FOOD_WASTE_SOURCE, SKS_ACTIVITY_SOURCE],
    claimPolicy: {
      allowedNow: [
        'official historical food-waste baseline',
        'source health and provenance',
        'model-estimated next-service demand band',
        'scenario outputs explicitly labeled as scenarios',
        'pre-registered pilot targets and formulas',
      ],
      forbiddenUntilMeasured: [
        'food waste saved by BOUNCAMPUS',
        'CO2 or water saved by BOUNCAMPUS',
        'actual cafeteria production optimized',
        'actual student demand observed',
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
        'production planning band',
        'decision readiness based on source availability',
        'prevention/recovery scenario outcomes',
      ],
      unavailable: [
        'cafeteria POS transactions',
        'actual produced portions by service',
        'actual served portions by service',
        'plate-waste measurements by menu item',
      ],
    },
  });
}
