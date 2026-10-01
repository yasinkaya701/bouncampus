'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { BusFront, CloudRain, Gauge, Loader2, RefreshCw, UsersRound } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import { shuttleRoutes } from '@/lib/shuttle-network';

type Readiness = 'REVIEW_REQUIRED' | 'WITHHOLD';

type FrequencyRecommendation = {
  routeId: string;
  day: string;
  hour: number;
  scheduleCoverage: 'FULL' | 'PARTIAL' | 'NONE';
  scheduleAffectedSeatsEstimate: number;
  scheduleArrivalsEstimate: number;
  scheduleDeparturesEstimate: number;
  pressureBand: 'LOW' | 'MODERATE' | 'HIGH' | 'SURGE';
  targetHeadwayMinutes: number;
  targetDeparturesPerHour: number;
  currentPublishedHeadwayMinutes: number | null;
  publishedScheduleComparison: string;
  fleetFeasibilityStatus: 'UNVERIFIED';
};

type FrequencyResponse = {
  decision: {
    readiness: Readiness;
    reasonCodes: string[];
    limitations: string[];
    automaticDispatchAllowed: false;
    recommendation: FrequencyRecommendation | null;
  };
  hourlyPlan: Array<{
    hour: number;
    readiness: Readiness;
    reasonCodes: string[];
    recommendation: FrequencyRecommendation | null;
  }>;
  context: {
    planningWindow: { day: string; hour: number; timezone: string };
    courseSnapshot: {
      term: string;
      capturedAt: string;
      refreshRequiredAfter: string;
      sourceClass: string;
      sourceUrl: string;
    };
    weather: {
      rain: boolean | null;
      temperature: number | null;
      windSpeedKmh: number | null;
      source: { provenance: string; ok: boolean; label: string };
    };
    publishedSchedule: {
      nextDeparture: string | null;
      source: { provenance: string; ok: boolean };
    } | null;
    scenarioInputs: {
      eventMultiplier: number;
      operatorQueuePassengers: number | null;
    };
  };
  truthBoundary: {
    recommendationType: string;
    scheduleActivityIsObservedRidership: false;
    liveGpsConnected: false;
    liveOccupancyConnected: false;
    verifiedFleetCapacityConnected: false;
    verifiedTurnaroundConnected: false;
    automaticDispatch: false;
    officialTimetableRemainsAuthoritative: true;
  };
};

const DAYS = [
  { id: 'M', tr: 'Pzt', en: 'Mon' },
  { id: 'T', tr: 'Sal', en: 'Tue' },
  { id: 'W', tr: 'Çar', en: 'Wed' },
  { id: 'Th', tr: 'Per', en: 'Thu' },
  { id: 'F', tr: 'Cum', en: 'Fri' },
];

const DAY_FROM_WEEKDAY: Record<string, string> = {
  Mon: 'M', Tue: 'T', Wed: 'W', Thu: 'Th', Fri: 'F', Sat: 'St', Sun: 'Su',
};

function currentIstanbulWindow() {
  const now = new Date();
  const weekday = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Istanbul', weekday: 'short' }).format(now);
  const hour = Number(new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', hour: '2-digit', hour12: false }).format(now));
  return { day: DAY_FROM_WEEKDAY[weekday] ?? 'M', hour };
}

function bandClass(band: FrequencyRecommendation['pressureBand']) {
  if (band === 'SURGE') return 'border-rose-200 bg-rose-50 text-rose-800';
  if (band === 'HIGH') return 'border-amber-200 bg-amber-50 text-amber-800';
  if (band === 'MODERATE') return 'border-sky-200 bg-sky-50 text-sky-800';
  return 'border-slate-200 bg-slate-50 text-slate-700';
}

export default function ShuttleFrequencyPlanner() {
  const { locale, t } = useLocale();
  const initial = useMemo(() => currentIstanbulWindow(), []);
  const [routeId, setRouteId] = useState('south-north-loop');
  const [day, setDay] = useState(initial.day === 'Su' || initial.day === 'St' ? 'M' : initial.day);
  const [hour, setHour] = useState(String(initial.hour));
  const [eventMultiplier, setEventMultiplier] = useState('1');
  const [queuePassengers, setQueuePassengers] = useState('');
  const [result, setResult] = useState<FrequencyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadFrequency() {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ routeId, day, hour, eventMultiplier });
      if (queuePassengers.trim()) params.set('queuePassengers', queuePassengers.trim());
      const response = await fetch(`/api/v1/shuttles/frequency?${params.toString()}`, { cache: 'no-store' });
      const body = await response.json() as FrequencyResponse | { error?: string };
      if (!response.ok) throw new Error('error' in body && body.error ? body.error : 'frequency_plan_failed');
      setResult(body as FrequencyResponse);
    } catch (loadError) {
      setResult(null);
      setError(loadError instanceof Error ? loadError.message : 'frequency_plan_failed');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadFrequency();
    // Initial snapshot for the default route/window only. Subsequent changes are explicit operator actions.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function submit(event: FormEvent) {
    event.preventDefault();
    void loadFrequency();
  }

  const recommendation = result?.decision.recommendation ?? null;

  return (
    <article className="rounded-[28px] border border-slate-900/[0.08] bg-white p-5 shadow-[0_16px_45px_rgba(15,23,42,.045)] sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#173f67]"><Gauge size={12} /> {t('Mekik sıklık planlayıcı', 'Shuttle frequency planner')}</div>
          <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('Ders dalgasını sefer aralığına çevir', 'Turn class waves into a headway recommendation')}</h2>
          <p className="mt-2 max-w-3xl text-[10px] leading-5 text-slate-500">
            {t(
              'Ders başlangıç/bitiş yoğunluğu, canlı haricî yağmur sinyali ve operatör senaryo girdilerini birleştirir. Çıktı öneridir; filo, şoför ve tur süresi doğrulanmadan resmî tarifeyi değiştirmez.',
              'Combines class start/end activity, live external rain context and operator scenario inputs. The output is advisory; it never changes the official timetable without verified fleet, driver and turnaround feasibility.',
            )}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {result?.context.weather.rain === true ? (
            <span className="inline-flex items-center gap-1 rounded-full border border-sky-200 bg-sky-50 px-2.5 py-1 text-[9px] font-black text-sky-800"><CloudRain size={10} /> {t('Yağmur baskısı', 'Rain pressure')}</span>
          ) : null}
          <span className={`rounded-full border px-2.5 py-1 font-mono text-[9px] font-black ${result?.decision.readiness === 'WITHHOLD' ? 'border-rose-200 bg-rose-50 text-rose-800' : 'border-amber-200 bg-amber-50 text-amber-800'}`}>
            {result?.decision.readiness ?? 'LOADING'}
          </span>
        </div>
      </div>

      <form onSubmit={submit} className="mt-5 grid gap-3 md:grid-cols-5">
        <label className="text-[9px] font-black uppercase tracking-[0.08em] text-slate-500 md:col-span-2">
          {t('Hat', 'Route')}
          <select value={routeId} onChange={event => setRouteId(event.target.value)} className="bc-focus-ring mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold normal-case tracking-normal text-slate-800">
            {shuttleRoutes.map(route => <option key={route.id} value={route.id}>{locale === 'tr' ? route.nameTr : route.nameEn}</option>)}
          </select>
        </label>
        <label className="text-[9px] font-black uppercase tracking-[0.08em] text-slate-500">
          {t('Gün', 'Day')}
          <select value={day} onChange={event => setDay(event.target.value)} className="bc-focus-ring mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold normal-case tracking-normal text-slate-800">
            {DAYS.map(item => <option key={item.id} value={item.id}>{locale === 'tr' ? item.tr : item.en}</option>)}
          </select>
        </label>
        <label className="text-[9px] font-black uppercase tracking-[0.08em] text-slate-500">
          {t('Saat', 'Hour')}
          <input value={hour} onChange={event => setHour(event.target.value)} type="number" min="0" max="23" className="bc-focus-ring mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold normal-case tracking-normal text-slate-800" />
        </label>
        <div className="flex items-end">
          <button type="submit" disabled={loading} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-xl bg-[#071c33] px-4 py-2.5 text-[10px] font-black text-white disabled:opacity-50">
            {loading ? <Loader2 className="animate-spin" size={13} /> : <RefreshCw size={13} />} {t('Planı hesapla', 'Compute plan')}
          </button>
        </div>
        <label className="text-[9px] font-black uppercase tracking-[0.08em] text-slate-500 md:col-span-2">
          {t('Etkinlik çarpanı · senaryo', 'Event multiplier · scenario')}
          <input value={eventMultiplier} onChange={event => setEventMultiplier(event.target.value)} type="number" min="1" max="3" step="0.25" className="bc-focus-ring mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold normal-case tracking-normal text-slate-800" />
        </label>
        <label className="text-[9px] font-black uppercase tracking-[0.08em] text-slate-500 md:col-span-2">
          {t('Kuyruk gözlemi · opsiyonel', 'Observed queue · optional')}
          <div className="relative mt-1.5">
            <UsersRound className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-300" size={13} />
            <input value={queuePassengers} onChange={event => setQueuePassengers(event.target.value)} type="number" min="0" max="10000" placeholder="0" className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-9 pr-3 text-[11px] font-bold normal-case tracking-normal text-slate-800" />
          </div>
        </label>
      </form>

      {error ? <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 font-mono text-[9px] text-rose-800">{error}</div> : null}

      {recommendation ? (
        <div className="mt-5 grid gap-3 lg:grid-cols-[1fr_1.4fr]">
          <div className="rounded-2xl bg-[#071c33] p-5 text-white">
            <div className="flex items-center justify-between gap-3">
              <div className="text-[9px] font-black uppercase tracking-[0.12em] text-white/50">{t('Hedef sefer aralığı', 'Target headway')}</div>
              <span className={`rounded-full border px-2 py-1 font-mono text-[8px] font-black ${bandClass(recommendation.pressureBand)}`}>{recommendation.pressureBand}</span>
            </div>
            <div className="mt-3 flex items-end gap-2"><span className="text-[48px] font-black leading-none tracking-[-0.08em]">{recommendation.targetHeadwayMinutes}</span><span className="pb-1 text-[11px] font-black text-white/55">{t('dk', 'min')}</span></div>
            <div className="mt-3 text-[10px] text-white/55">{recommendation.targetDeparturesPerHour} {t('sefer/saat adayı', 'departures/hour candidate')}</div>
            <div className="mt-4 grid grid-cols-3 gap-2">
              <MiniMetric label={t('Program etkisi', 'Schedule seats')} value={String(recommendation.scheduleAffectedSeatsEstimate)} />
              <MiniMetric label={t('Başlayan', 'Starting')} value={String(recommendation.scheduleArrivalsEstimate)} />
              <MiniMetric label={t('Biten', 'Ending')} value={String(recommendation.scheduleDeparturesEstimate)} />
            </div>
          </div>
          <div className="rounded-2xl border border-slate-900/[0.07] bg-[#f7f9f6] p-4">
            <div className="grid gap-2 sm:grid-cols-3">
              <InfoMetric label={t('Program kapsaması', 'Schedule coverage')} value={recommendation.scheduleCoverage} />
              <InfoMetric label={t('Yayınlı headway', 'Published headway')} value={recommendation.currentPublishedHeadwayMinutes === null ? '—' : `${recommendation.currentPublishedHeadwayMinutes} min`} />
              <InfoMetric label={t('Tarife karşılaştırması', 'Timetable comparison')} value={recommendation.publishedScheduleComparison.replaceAll('_', ' ')} />
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {result?.decision.reasonCodes.map(code => <span key={code} className="rounded-md border border-slate-200 bg-white px-2 py-1 font-mono text-[8px] font-bold text-slate-500">{code}</span>)}
            </div>
            <p className="mt-3 text-[9px] leading-4 text-slate-500">
              {t('Programdaki koltuk tahmini yolcu sayısı değildir. Filo kapasitesi ve tur süresi doğrulanmadığı için çıktı operatör incelemesi ister ve otomatik dispatch yapmaz.', 'Schedule-seat activity is not a rider count. Fleet capacity and turnaround are unverified, so the result requires operator review and never dispatches automatically.')}
            </p>
          </div>
        </div>
      ) : null}

      {result?.hourlyPlan?.length ? (
        <div className="mt-5">
          <div className="mb-2 text-[9px] font-black uppercase tracking-[0.1em] text-slate-400">{t('Ders programına göre günlük baz plan · 09–21', 'Schedule-only daily baseline · 09–21')}</div>
          <div className="grid grid-cols-4 gap-2 sm:grid-cols-7 lg:grid-cols-13">
            {result.hourlyPlan.map(item => (
              <div key={item.hour} className={`rounded-xl border p-2 text-center ${item.recommendation ? 'border-slate-200 bg-white' : 'border-rose-100 bg-rose-50'}`}>
                <div className="font-mono text-[8px] font-bold text-slate-400">{String(item.hour).padStart(2, '0')}:00</div>
                <div className="mt-1 text-[12px] font-black text-slate-900">{item.recommendation ? `${item.recommendation.targetHeadwayMinutes}m` : '—'}</div>
                <div className="mt-0.5 text-[7px] font-black text-slate-400">{item.recommendation?.pressureBand ?? 'WITHHOLD'}</div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {result ? (
        <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-slate-900/[0.06] pt-4 text-[8px] font-bold text-slate-400">
          <span>{t('Ders snapshot', 'Course snapshot')}: {result.context.courseSnapshot.term}</span>
          <span>·</span>
          <span>{t('Hava', 'Weather')}: {result.context.weather.source.provenance}</span>
          <span>·</span>
          <span>{t('Filo uygunluğu', 'Fleet feasibility')}: UNVERIFIED</span>
          <span>·</span>
          <span>{t('Resmî tarife otorite', 'Official timetable authoritative')}</span>
        </div>
      ) : null}
    </article>
  );
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl bg-white/[0.07] p-2"><div className="text-[7px] font-black uppercase tracking-[0.06em] text-white/35">{label}</div><div className="mt-1 font-mono text-[13px] font-black text-white">{value}</div></div>;
}

function InfoMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-slate-900/[0.06] bg-white p-3"><div className="text-[7px] font-black uppercase tracking-[0.07em] text-slate-400">{label}</div><div className="mt-1 break-words text-[10px] font-black text-slate-800">{value}</div></div>;
}
