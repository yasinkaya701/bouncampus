'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import {
  Activity,
  ArrowRight,
  ArrowUpRight,
  BusFront,
  CalendarDays,
  CheckCircle2,
  Clock3,
  CloudSun,
  Database,
  ExternalLink,
  MapPin,
  ShieldAlert,
  Sparkles,
  Utensils,
} from 'lucide-react';
import KPICards from '@/components/Dashboard/KPICards';
import ActionCards from '@/components/Dashboard/ActionCards';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import type { SourceMeta } from '@/lib/live-sources';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

const provenanceLabel: Record<string, string> = {
  OFFICIAL_LIVE: 'OFFICIAL LIVE',
  OFFICIAL_SNAPSHOT: 'OFFICIAL SNAPSHOT',
  EXTERNAL_LIVE: 'EXTERNAL LIVE',
  MODEL_ESTIMATE: 'MODEL ESTIMATE',
  FALLBACK: 'UNAVAILABLE',
};

const provenanceTone: Record<string, string> = {
  OFFICIAL_LIVE: 'border-emerald-200 bg-emerald-50 text-emerald-700',
  OFFICIAL_SNAPSHOT: 'border-violet-200 bg-violet-50 text-violet-700',
  EXTERNAL_LIVE: 'border-blue-200 bg-blue-50 text-blue-700',
  MODEL_ESTIMATE: 'border-violet-200 bg-violet-50 text-violet-700',
  FALLBACK: 'border-amber-200 bg-amber-50 text-amber-700',
};

function fmt(value: number | null | undefined, suffix = '') {
  return value == null ? '—' : `${value}${suffix}`;
}

function SourcePill({ source }: { source?: SourceMeta }) {
  const type = source?.ok ? source.provenance : 'FALLBACK';
  return (
    <span className={`bc-chip ${provenanceTone[type] ?? provenanceTone.FALLBACK}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${source?.ok ? 'bg-current' : 'bg-amber-500'}`} />
      {provenanceLabel[type] ?? type}
    </span>
  );
}

function formatDashboardDate(value: string) {
  try {
    return new Intl.DateTimeFormat('tr-TR', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'Europe/Istanbul' }).format(new Date(`${value}T12:00:00+03:00`));
  } catch {
    return value;
  }
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard().then(setData);
  }, []);

  if (!data) {
    return (
      <div className="grid min-h-[66vh] place-items-center">
        <div className="text-center">
          <div className="mx-auto h-9 w-9 animate-spin rounded-full border-2 border-slate-300 border-t-[#2f5cff]" />
          <p className="mt-4 text-xs font-bold text-slate-600">Campus intelligence is coming online</p>
          <p className="mt-1 font-mono text-[10px] text-slate-400">checking public sources · loading decision models</p>
        </div>
      </div>
    );
  }

  const degraded = data.data_quality?.mode === 'DEGRADED';
  const scheduleSource = data.sources?.find(source => source.id === 'boun-course-schedule');
  const calendarSource = data.sources?.find(source => source.id === 'boun-academic-calendar');
  const healthySources = data.sources?.filter(source => source.ok).length ?? 0;
  const totalSources = data.sources?.length ?? 0;
  const primaryAction = data.actions[0];
  const occupancyData = data.buildings
    .map(building => ({ name: building.name, occupancy: Math.round((building.occupancy_ratio ?? 0) * 100) }))
    .sort((a, b) => b.occupancy - a.occupancy)
    .slice(0, 9);

  return (
    <div className="space-y-4 md:space-y-5">
      <section className="bc-surface-dark relative overflow-hidden rounded-[30px] px-5 py-6 text-white sm:px-7 sm:py-7 lg:px-9 lg:py-8">
        <div className="pointer-events-none absolute -right-20 -top-32 h-80 w-80 rounded-full bg-blue-500/15 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-40 left-1/3 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />

        <div className="relative grid gap-8 xl:grid-cols-[1.55fr_0.8fr] xl:items-end">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="bc-chip border-white/10 bg-white/5 text-slate-300">BOUNCAMPUS / LIVE BRIEF</span>
              <span className={`bc-chip ${degraded ? 'border-amber-400/20 bg-amber-400/10 text-amber-300' : 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300'}`}>
                {degraded ? <ShieldAlert size={10} /> : <CheckCircle2 size={10} />}
                {degraded ? 'DEGRADED SOURCES' : 'SOURCE HEALTHY'}
              </span>
            </div>

            <h1 className="mt-7 max-w-4xl text-[38px] font-black leading-[0.98] tracking-[-0.06em] text-white sm:text-[48px] lg:text-[58px]">
              Kampüsü ölç, tahmin et,
              <span className="block text-blue-300">doğru anda harekete geç.</span>
            </h1>
            <p className="mt-5 max-w-2xl text-[13px] leading-relaxed text-slate-400 sm:text-sm">
              Boğaziçi&apos;nin public operasyon verilerini tek karar katmanında birleştiriyoruz. Canlı kaynaklar, resmî snapshot&apos;lar ve model tahminleri birbirine karıştırılmadan sunulur.
            </p>

            <div className="mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 text-[10px] font-bold text-slate-400">
              <span className="inline-flex items-center gap-1.5"><CalendarDays size={12} /> {formatDashboardDate(data.date)}</span>
              <span className="inline-flex items-center gap-1.5"><Database size={12} /> {healthySources}/{totalSources} source checks passing</span>
              <span className="inline-flex items-center gap-1.5"><Sparkles size={12} /> decision outputs explicitly labeled</span>
            </div>
          </div>

          <div className="rounded-[24px] border border-white/10 bg-white/[0.055] p-5 backdrop-blur-sm">
            <div className="flex items-center justify-between gap-4">
              <span className="text-[9px] font-black uppercase tracking-[0.18em] text-slate-500">Top decision candidate</span>
              <span className="rounded-full border border-violet-400/20 bg-violet-400/10 px-2 py-1 text-[8px] font-black tracking-[0.08em] text-violet-200">MODEL</span>
            </div>
            {primaryAction ? (
              <>
                <h2 className="mt-5 text-xl font-black leading-tight tracking-[-0.035em] text-white">{primaryAction.title}</h2>
                <p className="mt-3 line-clamp-3 text-[11px] leading-relaxed text-slate-400">{primaryAction.description}</p>
                <div className="mt-5 flex items-end justify-between gap-4 border-t border-white/10 pt-4">
                  <div>
                    <div className="text-[9px] font-bold uppercase tracking-[0.13em] text-slate-500">Modeled impact</div>
                    <div className="mt-1 font-mono text-2xl font-black tracking-[-0.04em] text-emerald-300">
                      {primaryAction.impact_value.toLocaleString('tr-TR')}
                      <span className="ml-1 text-[10px] font-bold text-slate-400">{primaryAction.impact_unit}</span>
                    </div>
                  </div>
                  <div className="text-right text-[9px] font-bold text-slate-500">
                    <div className="inline-flex items-center gap-1"><Clock3 size={10} /> {primaryAction.time}</div>
                    <div className="mt-1 inline-flex items-center gap-1"><MapPin size={10} /> {primaryAction.location}</div>
                  </div>
                </div>
              </>
            ) : (
              <p className="mt-5 text-xs text-slate-400">No decision candidate is currently above the model threshold.</p>
            )}
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between">
            <span className="bc-eyebrow">Bebek / weather</span>
            <CloudSun size={17} className="text-slate-400" />
          </div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{fmt(data.live_weather?.temperature, '°')}</div>
          <div className="mt-2 text-[11px] text-slate-500">Nem {fmt(data.live_weather?.humidity, '%')} · Rüzgâr {fmt(data.live_weather?.wind_speed, ' km/h')}</div>
          <div className="mt-5"><SourcePill source={data.live_weather?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between">
            <span className="bc-eyebrow">SKS / today</span>
            <Utensils size={16} className="text-slate-400" />
          </div>
          <div className="mt-6 line-clamp-2 min-h-[2.8rem] text-[15px] font-black leading-snug tracking-[-0.02em] text-[#0a1020]">
            {data.live_menu?.main_dish ?? 'Menü ayrıştırılamadı'}
          </div>
          <div className="mt-2 line-clamp-1 text-[11px] text-slate-500">{data.live_menu?.soup ?? '—'} {data.live_menu?.calories ? `· ${data.live_menu.calories} kcal` : ''}</div>
          <div className="mt-5"><SourcePill source={data.live_menu?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between">
            <span className="bc-eyebrow">Mekik / Güney → Kuzey</span>
            <BusFront size={17} className="text-slate-400" />
          </div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{data.live_shuttle?.next_departure ?? '—'}</div>
          <div className="mt-2 text-[11px] text-slate-500">Next published departure</div>
          <div className="mt-5"><SourcePill source={data.live_shuttle?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between">
            <span className="bc-eyebrow">BUIS / schedule</span>
            <Database size={16} className="text-slate-400" />
          </div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')}</div>
          <div className="mt-2 text-[11px] text-slate-500">Course records in the current snapshot</div>
          <div className="mt-5"><SourcePill source={scheduleSource} /></div>
        </article>
      </section>

      <KPICards data={data} />

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.8fr)_minmax(340px,0.72fr)]">
        <div className="bc-surface rounded-[28px] p-3 sm:p-4">
          <div className="flex flex-col gap-3 px-2 pb-4 pt-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <div className="bc-eyebrow">Spatial intelligence</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Campus operational map</h2>
              <p className="mt-1 text-[11px] text-slate-500">Building colors visualize schedule-derived utilization, not occupancy sensor measurements.</p>
            </div>
            <Link href="/buildings" className="bc-focus-ring inline-flex items-center gap-1.5 self-start rounded-full border border-slate-950/10 bg-[#f4f5f2] px-3 py-1.5 text-[10px] font-black text-slate-700 transition hover:bg-white sm:self-auto">
              Explore buildings <ArrowRight size={11} />
            </Link>
          </div>
          <CampusMap buildings={data.buildings} />
        </div>

        <aside className="bc-surface flex min-h-[620px] flex-col rounded-[28px] p-4 sm:p-5">
          <div className="flex items-start justify-between gap-3 border-b border-slate-900/8 pb-4">
            <div>
              <div className="bc-eyebrow">Decision queue</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">What should happen next?</h2>
              <p className="mt-1 text-[11px] leading-relaxed text-slate-500">Ranked decision candidates. Field validation is required before execution.</p>
            </div>
            <span className="grid h-9 w-9 shrink-0 place-items-center rounded-[13px] bg-[#0b1226] text-white"><Activity size={15} /></span>
          </div>
          <div className="mt-4 flex-1 overflow-y-auto pr-1">
            <ActionCards actions={data.actions} />
          </div>
        </aside>
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.45fr)_minmax(320px,0.55fr)]">
        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="mb-7 flex items-start justify-between gap-4">
            <div>
              <div className="bc-eyebrow">Schedule signal</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Where demand concentrates</h2>
              <p className="mt-1 text-[11px] text-slate-500">Top buildings by estimated utilization at the evaluation hour.</p>
            </div>
            <span className="bc-chip border-violet-200 bg-violet-50 text-violet-700"><Sparkles size={10} /> MODEL</span>
          </div>
          <div className="h-[310px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={occupancyData} layout="vertical" margin={{ top: 0, right: 22, left: 12, bottom: 0 }}>
                <CartesianGrid strokeDasharray="2 6" horizontal={false} stroke="rgba(15,23,42,0.08)" />
                <XAxis type="number" domain={[0, 100]} unit="%" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <YAxis dataKey="name" type="category" width={150} axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#475569', fontWeight: 600 }} />
                <Tooltip cursor={{ fill: 'rgba(47,92,255,0.04)' }} formatter={(value: number) => [`%${value}`, 'Estimated use']} contentStyle={{ borderRadius: '14px', borderColor: 'rgba(15,23,42,0.10)', boxShadow: '0 12px 34px rgba(10,16,32,0.10)', fontSize: '11px' }} />
                <Bar dataKey="occupancy" fill="#2f5cff" radius={[0, 8, 8, 0]} barSize={11} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="flex items-start justify-between">
            <div>
              <div className="bc-eyebrow">Academic context</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Calendar pulse</h2>
            </div>
            <CalendarDays size={18} className="text-slate-400" />
          </div>
          <div className="mt-6 space-y-1">
            {(data.academic_calendar?.length
              ? data.academic_calendar
              : [calendarSource?.ok ? 'Resmî takvim erişilebilir; yapılandırılmış başlık alınamadı.' : 'Akademik takvim kaynağı erişilemiyor.'])
              .slice(0, 5)
              .map((item, index) => (
                <div key={`${item}-${index}`} className="group flex gap-3 rounded-xl px-2 py-3 transition hover:bg-[#f4f5f2]">
                  <span className="mt-0.5 font-mono text-[9px] font-black text-slate-300">0{index + 1}</span>
                  <p className="text-[11px] font-semibold leading-relaxed text-slate-600">{item}</p>
                </div>
              ))}
          </div>
        </div>
      </section>

      <section id="sources" className="scroll-mt-28 rounded-[28px] border border-slate-950/10 bg-[#e9ece8]/70 p-5 sm:p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="bc-eyebrow">Data trust layer</div>
            <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Every signal has a provenance.</h2>
            <p className="mt-1 max-w-2xl text-[11px] leading-relaxed text-slate-500">Live public feed, dated official snapshot, external weather or model estimate: the product keeps the boundary visible instead of presenting everything as telemetry.</p>
          </div>
          <Link href="/api/v1/health" target="_blank" className="bc-focus-ring inline-flex items-center gap-1.5 self-start rounded-full bg-[#0b1226] px-3 py-2 text-[10px] font-black text-white shadow-sm lg:self-auto">
            Open health endpoint <ArrowUpRight size={11} />
          </Link>
        </div>

        <div className="mt-6 grid gap-2 md:grid-cols-2 xl:grid-cols-4">
          {(data.sources ?? []).map(source => (
            <a
              key={source.id}
              href={source.url}
              target={source.url.startsWith('http') ? '_blank' : undefined}
              rel={source.url.startsWith('http') ? 'noreferrer' : undefined}
              className="group rounded-[18px] border border-slate-950/8 bg-white/75 p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-sm"
            >
              <div className="flex items-start justify-between gap-3">
                <SourcePill source={source} />
                {source.url.startsWith('http') && <ExternalLink size={12} className="mt-1 text-slate-300 transition group-hover:text-slate-600" />}
              </div>
              <h3 className="mt-4 text-[12px] font-black leading-snug tracking-[-0.01em] text-[#0a1020]">{source.label}</h3>
              <p className="mt-2 line-clamp-3 text-[10px] leading-relaxed text-slate-500">{source.detail}</p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
