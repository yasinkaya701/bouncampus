import { NextResponse } from 'next/server';
import type { DashboardData, ActionItem } from '@/lib/types';
import type { MissionBrief, MissionEvidence, MissionImpact } from '@/lib/mission-types';

function sourceValue(ok: boolean | undefined, value: string | null | undefined, fallback = 'unavailable') {
  if (!ok || value == null || value === '') return fallback;
  return value;
}

function confidenceFor(data: DashboardData) {
  const sources = data.sources ?? [];
  if (!sources.length) return { score: 20, label: 'LOW' as const };
  const healthy = sources.filter(source => source.ok).length;
  const ratio = healthy / sources.length;
  const score = Math.max(20, Math.min(95, Math.round(ratio * 100)));
  if (score >= 80) return { score, label: 'HIGH' as const };
  if (score >= 55) return { score, label: 'MEDIUM' as const };
  return { score, label: 'LOW' as const };
}

function missionTitle(action: ActionItem | undefined) {
  if (!action) return 'No action above the decision threshold';
  if (action.type === 'energy') return 'Open less space. Keep the same academic capacity.';
  if (action.type === 'food') return 'Match lunch production to the campus demand pulse.';
  return 'Redirect capacity before congestion becomes visible.';
}

function evidenceFrom(data: DashboardData, action: ActionItem | undefined): MissionEvidence[] {
  const weatherSource = data.live_weather?.provenance;
  const menuSource = data.live_menu?.provenance;
  const shuttleSource = data.live_shuttle?.provenance;
  const scheduleSource = data.sources?.find(source => source.id === 'boun-course-schedule');
  const evidence: MissionEvidence[] = [
    {
      id: 'schedule',
      label: 'Academic demand signal',
      value: `${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} course records`,
      interpretation: action?.type === 'energy'
        ? 'The timetable provides the demand shape used to identify low-use windows.'
        : 'The timetable provides the student-flow signal used by the model.',
      source: scheduleSource,
    },
    {
      id: 'weather',
      label: 'Bebek weather',
      value: sourceValue(weatherSource?.ok, data.live_weather?.temperature == null ? null : `${data.live_weather.temperature}°C`),
      interpretation: data.live_weather?.rain
        ? 'Rain raises indoor demand and cafeteria pressure in the demand model.'
        : 'Outdoor conditions are included in energy and food-demand assumptions.',
      source: weatherSource,
    },
    {
      id: 'menu',
      label: 'SKS menu',
      value: sourceValue(menuSource?.ok, data.live_menu?.main_dish),
      interpretation: 'The official menu is shown as operational context; demand volume remains modeled without POS data.',
      source: menuSource,
    },
    {
      id: 'shuttle',
      label: 'Mekik timetable',
      value: sourceValue(shuttleSource?.ok, data.live_shuttle?.next_departure),
      interpretation: 'Published departure timing adds mobility context; this is not live GPS.',
      source: shuttleSource,
    },
  ];
  return evidence;
}

function impactFrom(data: DashboardData, action: ActionItem | undefined): MissionImpact[] {
  const impact: MissionImpact[] = [];
  if (action) {
    impact.push({
      label: 'Primary modeled impact',
      value: action.impact_value,
      unit: action.impact_unit,
      note: 'Decision-support estimate; not a realized meter or POS outcome.',
    });
  }
  if (data.potential_saving_tl > 0) {
    impact.push({
      label: 'Daily cost potential',
      value: data.potential_saving_tl,
      unit: 'TL/day',
      note: 'Physics-lite energy model potential using repository assumptions.',
    });
  }
  if (data.co2_avoided_kg > 0) {
    impact.push({
      label: 'CO₂ potential',
      value: data.co2_avoided_kg,
      unit: 'kg CO₂e/day',
      note: 'Calculated from modeled energy reduction; not audited emissions data.',
    });
  }
  return impact.slice(0, 3);
}

export async function GET(request: Request) {
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const date = new URL(request.url).searchParams.get('date_val');
  if (date) dashboardUrl.searchParams.set('date_val', date);

  const response = await fetch(dashboardUrl, { cache: 'no-store' });
  if (!response.ok) {
    return NextResponse.json({ error: 'Dashboard unavailable' }, { status: 503 });
  }

  const data = await response.json() as DashboardData;
  const action = data.actions[0];
  const sources = data.sources ?? [];
  const passing = sources.filter(source => source.ok).length;
  const unavailable = sources.length - passing;
  const confidence = confidenceFor(data);
  const degraded = data.data_quality?.mode === 'DEGRADED';

  const brief: MissionBrief = {
    generated_at: new Date().toISOString(),
    date: data.date,
    status: degraded ? 'DEGRADED' : action ? 'READY' : 'WATCH',
    title: missionTitle(action),
    one_liner: action
      ? `${action.location} için ${action.time} penceresinde doğrulanabilir bir operasyon fırsatı bulundu.`
      : 'Kaynaklar izleniyor; model şu anda müdahale eşiğinin üzerinde bir aday üretmiyor.',
    why_now: action?.description ?? 'BOUNCAMPUS bir öneri uydurmak yerine eşik altında kalmayı seçti.',
    confidence: confidence.score,
    confidence_label: confidence.label,
    decision_id: action?.id ?? null,
    decision_type: action?.type ?? null,
    location: action?.location ?? 'Campus-wide',
    operating_window: action?.time ?? 'Continuous watch',
    recommendation: action?.title ?? 'Continue monitoring source and schedule signals',
    guardrail: 'No campus system is controlled automatically. A human must validate the field condition before any real-world action.',
    evidence: evidenceFrom(data, action),
    impact: impactFrom(data, action),
    source_health: {
      passing,
      total: sources.length,
      official_live: data.data_quality?.official_live_sources ?? 0,
      external_live: data.data_quality?.external_live_sources ?? 0,
      unavailable,
    },
    dashboard: data,
  };

  return NextResponse.json(brief);
}
