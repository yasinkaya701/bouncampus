'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { CloudRain, Gauge, Loader2, RefreshCw } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import { shuttleRoutes } from '@/lib/shuttle-network';

type Recommendation = {
  routeId: string;
  scheduleCoverage: 'FULL' | 'PARTIAL' | 'NONE';
  scheduleAffectedSeatsEstimate: number;
  scheduleArrivalsEstimate: number;
  scheduleDeparturesEstimate: number;
  southToNorthProxySeatsEstimate: number | null;
  northToSouthProxySeatsEstimate: number | null;
  dominantDirection: 'SOUTH_TO_NORTH' | 'NORTH_TO_SOUTH' | 'BALANCED' | 'UNRESOLVED';
  pressureBasisSeatsEstimate: number;
  scenarioAdjustedPressureBasisSeatsEstimate: number;
  pressureBand: 'LOW' | 'MODERATE' | 'HIGH' | 'SURGE';
  targetHeadwayMinutes: number;
  targetDeparturesPerHour: number;
  currentPublishedHeadwayMinutes: number | null;
  publishedScheduleComparison: string;
  fleetFeasibilityStatus: 'UNVERIFIED';
};

type FrequencyResponse = {
  decision: {
    readiness: 'REVIEW_REQUIRED' | 'WITHHOLD';
    reasonCodes: string[];
    recommendation: Recommendation | null;
  };
  hourlyPlan: Array<{ hour: number; readiness: string; recommendation: Recommendation | null }>;
  context: {
    courseSnapshot: { term: string; refreshRequiredAfter: string };
    weather: { rain: boolean | null; source: { provenance: string } };
  };
};

const DAYS = [
  ['M', 'Pzt', 'Mon'], ['T', 'Sal', 'Tue'], ['W', 'Çar', 'Wed'], ['Th', 'Per', 'Thu'], ['F', 'Cum', 'Fri'],
] as const;
const DAY_MAP: Record<string, string> = { Mon: 'M', Tue: 'T', Wed: 'W', Thu: 'Th', Fri: 'F', Sat: 'M', Sun: 'M' };

function currentWindow() {
  const now = new Date();
  const weekday = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Istanbul', weekday: 'short' }).format(now);
  const hour = Number(new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', hour: '2-digit', hour12: false }).format(now));
  return { day: DAY_MAP[weekday] ?? 'M', hour };
}

export default function ShuttleFrequencyPlanner() {
  const { locale, t } = useLocale();
  const initial = useMemo(currentWindow, []);
  const [routeId, setRouteId] = useState('south-north-loop');
  const [day, setDay] = useState(initial.day);
  const [hour, setHour] = useState(String(initial.hour));
  const [eventMultiplier, setEventMultiplier] = useState('1');
  const [queuePassengers, setQueuePassengers] = useState('');
  const [result, setResult] = useState<FrequencyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ routeId, day, hour, eventMultiplier });
      if (queuePassengers.trim()) params.set('queuePassengers', queuePassengers.trim());
      const response = await fetch(`/api/v1/shuttles/frequency?${params.toString()}`, { cache: 'no-store' });
      const body = await response.json() as FrequencyResponse | { error?: string };
      if (!response.ok) throw new Error('error' in body && body.error ? body.error : 'frequency_plan_failed');
      setResult(body as FrequencyResponse);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : 'frequency_plan_failed');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
    // One bootstrap request; later changes require an explicit operator action.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function submit(event: FormEvent) {
    event.preventDefault();
    void load();
  }

  const rec = result?.decision.recommendation ?? null;
  const dominantDirectionLabel = rec?.dominantDirection === 'SOUTH_TO_NORTH'
    ? t('Güney → Kuzey', 'South → North')
    : rec?.dominantDirection === 'NORTH_TO_SOUTH'
      ? t('Kuzey → Güney', 'North → South')
      : rec?.dominantDirection === 'BALANCED'
        ? t('Dengeli', 'Balanced')
        : t('Çözümlenemedi', 'Unresolved');

  return (
    <section className="rounded-[28px] border border-slate-900/[0.08] bg-white p-5 shadow-[0_16px_45px_rgba(15,23,42,.045)] sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#173f67]"><Gauge size={12} /> {t('Mekik sıklık planlayıcı', 'Shuttle frequency planner')}</div>
          <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('Ders dalgasını headway önerisine çevir', 'Turn class waves into a headway recommendation')}</h2>
          <p className="mt-2 max-w-3xl text-[10px] leading-5 text-slate-500">{t('Ders başlangıç/bitiş aktivitesini yönsel hareket proxy’sine çevirir; haricî yağmur verisi, operatör senaryosu ve kuyruk gözlemiyle birlikte değerlendirir. Filo/şoför/tur süresi doğrulanmadan resmî tarifeyi değiştirmez.', 'Transforms class start/end activity into a directional movement proxy, then combines it with external rain data, operator scenarios and aggregate queue observations. It never changes the official timetable without verified fleet, driver and turnaround feasibility.')}</p>
        </div>
        <div className="flex items-center gap-2">
          {result?.context.weather.rain === true ? <span className="inline-flex items-center gap-1 rounded-full border border-sky-200 bg-sky-50 px-2.5 py-1 text-[9px] font-black text-sky-800"><CloudRain size={10} /> RAIN</span> : null}
          <span className={`rounded-full border px-2.5 py-1 font-mono text-[9px] font-black ${result?.decision.readiness === 'WITHHOLD' ? 'border-rose-200 bg-rose-50 text-rose-800' : 'border-amber-200 bg-amber-50 text-amber-800'}`}>{result?.decision.readiness ?? 'LOADING'}</span>
        </div>
      </div>

      <form onSubmit={submit} className="mt-5 grid gap-3 md:grid-cols-6">
        <Field label={t('Hat', 'Route')} wide>
          <select value={routeId} onChange={e => setRouteId(e.target.value)} className="input-shell">
            {shuttleRoutes.map(route => <option key={route.id} value={route.id}>{locale === 'tr' ? route.nameTr : route.nameEn}</option>)}
          </select>
        </Field>
        <Field label={t('Gün', 'Day')}>
          <select value={day} onChange={e => setDay(e.target.value)} className="input-shell">
            {DAYS.map(([id, tr, en]) => <option key={id} value={id}>{locale === 'tr' ? tr : en}</option>)}
          </select>
        </Field>
        <Field label={t('Saat', 'Hour')}>
          <input value={hour} onChange={e => setHour(e.target.value)} type="number" min="0" max="23" className="input-shell" />
        </Field>
        <Field label={t('Etkinlik çarpanı', 'Event multiplier')}>
          <input value={eventMultiplier} onChange={e => setEventMultiplier(e.target.value)} type="number" min="1" max="3" step="0.25" className="input-shell" />
        </Field>
        <Field label={t('Kuyruk · opsiyonel', 'Queue · optional')}>
          <input value={queuePassengers} onChange={e => setQueuePassengers(e.target.value)} type="number" min="0" max="10000" placeholder="0" className="input-shell" />
        </Field>
        <div className="flex items-end">
          <button type="submit" disabled={loading} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-xl bg-[#071c33] px-4 py-2.5 text-[10px] font-black text-white disabled:opacity-50">{loading ? <Loader2 className="animate-spin" size={13} /> : <RefreshCw size={13} />} {t('Hesapla', 'Compute')}</button>
        </div>
      </form>

      {error ? <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 font-mono text-[9px] text-rose-800">{error}</div> : null}

      {rec ? (
        <div className="mt-5 grid gap-3 lg:grid-cols-[.8fr_1.2fr]">
          <div className="rounded-2xl bg-[#071c33] p-5 text-white">
            <div className="text-[9px] font-black uppercase tracking-[0.12em] text-white/50">{t('Önerilen sefer aralığı', 'Recommended headway')}</div>
            <div className="mt-3 flex items-end gap-2"><span className="text-[52px] font-black leading-none tracking-[-0.08em]">{rec.targetHeadwayMinutes}</span><span className="pb-1 text-[11px] font-black text-white/55">{t('dk', 'min')}</span></div>
            <div className="mt-2 text-[10px] text-white/55">{rec.targetDeparturesPerHour} {t('sefer/saat adayı', 'departures/hour candidate')} · {rec.pressureBand}</div>
            <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.05] p-3">
              <div className="text-[8px] font-black uppercase tracking-[0.1em] text-white/40">{t('Baskın yön', 'Dominant direction')}</div>
              <div className="mt-1 text-[16px] font-black">{dominantDirectionLabel}</div>
            </div>
          </div>
          <div className="rounded-2xl border border-slate-900/[0.07] bg-[#f7f9f6] p-4">
            <div className="grid gap-2 sm:grid-cols-3 lg:grid-cols-6">
              <Metric label={t('Program etkisi', 'Schedule seats')} value={String(rec.scheduleAffectedSeatsEstimate)} />
              <Metric label={t('Baskı bazı', 'Pressure basis')} value={String(rec.pressureBasisSeatsEstimate)} />
              <Metric label={t('Güney → Kuzey', 'South → North')} value={rec.southToNorthProxySeatsEstimate === null ? '—' : String(rec.southToNorthProxySeatsEstimate)} />
              <Metric label={t('Kuzey → Güney', 'North → South')} value={rec.northToSouthProxySeatsEstimate === null ? '—' : String(rec.northToSouthProxySeatsEstimate)} />
              <Metric label={t('Senaryo sonrası', 'Scenario-adjusted')} value={String(rec.scenarioAdjustedPressureBasisSeatsEstimate)} />
              <Metric label={t('Yayınlı headway', 'Published headway')} value={rec.currentPublishedHeadwayMinutes === null ? '—' : `${rec.currentPublishedHeadwayMinutes}m`} />
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">{result?.decision.reasonCodes.map(code => <span key={code} className="rounded-md border border-slate-200 bg-white px-2 py-1 font-mono text-[8px] font-bold text-slate-500">{code}</span>)}</div>
            <p className="mt-3 text-[9px] leading-4 text-slate-500">{t('Yön değerleri gerçek origin-destination yolculukları değil, program başlangıç/bitişlerinden türetilmiş hareket proxy’leridir. Filo uygunluğu UNVERIFIED ve otomatik dispatch kapalıdır.', 'Directional values are not observed origin-destination trips; they are movement proxies derived from class starts/ends. Fleet feasibility is UNVERIFIED and automatic dispatch is disabled.')}</p>
          </div>
        </div>
      ) : null}

      {result?.hourlyPlan.length ? (
        <div className="mt-5">
          <div className="mb-2 text-[9px] font-black uppercase tracking-[0.1em] text-slate-400">{t('Program bazlı günlük plan · 09–21', 'Schedule-only daily plan · 09–21')}</div>
          <div className="grid grid-cols-4 gap-2 sm:grid-cols-7 lg:grid-cols-13">
            {result.hourlyPlan.map(item => <div key={item.hour} className="rounded-xl border border-slate-200 bg-white p-2 text-center"><div className="font-mono text-[8px] text-slate-400">{item.hour}:00</div><div className="mt-1 text-[12px] font-black">{item.recommendation ? `${item.recommendation.targetHeadwayMinutes}m` : '—'}</div><div className="text-[7px] font-black text-slate-400">{item.recommendation?.pressureBand ?? 'WITHHOLD'}</div></div>)}
          </div>
        </div>
      ) : null}

      {result ? <div className="mt-4 border-t border-slate-900/[0.06] pt-3 text-[8px] font-bold text-slate-400">{result.context.courseSnapshot.term} · weather: {result.context.weather.source.provenance} · fleet feasibility: UNVERIFIED · official timetable authoritative</div> : null}
      <style jsx>{` .input-shell { width: 100%; margin-top: .375rem; border-radius: .75rem; border: 1px solid rgb(226 232 240); background: white; padding: .625rem .75rem; font-size: 11px; font-weight: 700; color: rgb(30 41 59); } `}</style>
    </section>
  );
}

function Field({ label, wide = false, children }: { label: string; wide?: boolean; children: React.ReactNode }) {
  return <label className={`text-[9px] font-black uppercase tracking-[0.08em] text-slate-500 ${wide ? 'md:col-span-2' : ''}`}>{label}{children}</label>;
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-slate-900/[0.06] bg-white p-3"><div className="text-[7px] font-black uppercase tracking-[0.07em] text-slate-400">{label}</div><div className="mt-1 text-[12px] font-black text-slate-800">{value}</div></div>;
}
