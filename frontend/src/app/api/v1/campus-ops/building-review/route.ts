import { NextRequest, NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';
import courseSnapshotMeta from '@/data/course_snapshot_meta.json';
import { computeBuildingEnergy } from '@/lib/campus-calculations';
import { fetchBounWeather } from '@/lib/live-sources';
import { recommendBuildingReview } from '@/lib/decision-intelligence/building-review-policy';

export const dynamic = 'force-dynamic';

function parseDate(value: string | null): { dateVal: string; weekday: number } | null {
  const dateVal = value?.trim() || new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Istanbul',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
  const parsed = new Date(`${dateVal}T12:00:00+03:00`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateVal) || Number.isNaN(parsed.getTime())) return null;
  return { dateVal, weekday: (parsed.getDay() + 6) % 7 };
}

export async function GET(request: NextRequest) {
  const parsed = parseDate(request.nextUrl.searchParams.get('date'));
  if (!parsed) {
    return NextResponse.json({ error: 'invalid_date', expected: 'YYYY-MM-DD' }, { status: 400 });
  }

  const weather = await fetchBounWeather();
  const ambientTemperature = weather.temperature ?? 22;
  const scenarios = campusConfig.buildings.map(building =>
    computeBuildingEnergy(building.id, parsed.weekday, ambientTemperature)
  );
  const refreshDeadline = Date.parse(courseSnapshotMeta.refresh_required_after);
  const scheduleSnapshotStale = !Number.isFinite(refreshDeadline) || Date.now() > refreshDeadline;
  const weatherSource = `${weather.source.provenance}:${weather.source.label}${weather.source.ok ? '' : ':fallback'}`;

  const decision = recommendBuildingReview(scenarios, {
    scheduleSourceUrl: courseSnapshotMeta.source_url,
    weatherSource,
    scheduleSnapshotStale,
  });

  const rankedScenarioSummary = scenarios
    .filter(item => item.saving_kwh > 0)
    .sort((left, right) => right.saving_kwh - left.saving_kwh || left.building_id.localeCompare(right.building_id))
    .slice(0, 5)
    .map(item => ({
      buildingId: item.building_id,
      buildingName: item.building_name,
      modeledSavingPotentialKwh: item.saving_kwh,
      modeledSavingPercent: item.saving_percent,
    }));

  return NextResponse.json(
    {
      targetDate: parsed.dateVal,
      decision,
      rankedScenarioSummary,
      evidence: {
        courseSchedule: {
          sourceClass: courseSnapshotMeta.source_class,
          sourceUrl: courseSnapshotMeta.source_url,
          capturedAt: courseSnapshotMeta.captured_at,
          refreshRequiredAfter: courseSnapshotMeta.refresh_required_after,
          stale: scheduleSnapshotStale,
        },
        weather: weather.source,
        ambientTemperatureUsed: ambientTemperature,
        occupancyMethod: 'SCHEDULE_DERIVED_HEURISTIC',
        energyMethod: 'COUNTERFACTUAL_SCENARIO_MODEL',
      },
      truthBoundary: {
        liveOccupancySensorsConnected: false,
        buildingMetersConnected: false,
        bmsConnected: false,
        accessControlConnected: false,
        automaticHvacDispatch: false,
        automaticLightingDispatch: false,
        achievedSavingsClaimed: false,
      },
    },
    { headers: { 'Cache-Control': 'no-store' } },
  );
}
