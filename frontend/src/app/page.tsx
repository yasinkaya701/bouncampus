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
  CloudSun,
  Database,
  ExternalLink,
  Sparkles,
  Utensils,
} from 'lucide-react';
import MissionSpotlight from '@/components/Dashboard/MissionSpotlight';
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
          <p className="mt-4 text-xs font-bold text-slate-600">Building today&apos;s campus mission</p>
          <p className="mt-1 font-mono text-[10px] text-slate-400">checking sources · calculating opportunities · preserving provenance</p>
        </div>
      </div>
    );
  }

  const scheduleSource = data.sources?.find(source => source.id === 'boun-course-schedule');
  const calendarSource = data.sources?.find(source => source.id === 'boun-academic-calendar');
  const occupancyData = data.buildings
    .map(building => ({ name: building.name, occupancy: Math.round((building.occupancy_ratio ?? 0) * 100) }))
    .sort((a, b) => b.occupancy - a.occupancy)
    .slice(0, 9);

  return (
    <div className="space-y-4 md:space-y-5">
      <MissionSpotlight />

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between"><span className="bc-eyebrow">Bebek / weather</span><CloudSun size={17} className="text-slate-400" /></div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{fmt(data.live_weather?.temperature, '°')}</div>
          <div className="mt-2 text-[11px] text-slate-500">Nem {fmt(data.live_weather?.humidity, '%')} · Rüzgâr {fmt(data.live_weather?.wind_speed, ' km/h')}</div>
          <div className="mt-5"><SourcePill source={data.live_weather?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between"><span className="bc-eyebrow">SKS / menu</span><Utensils size={16} className="text-slate-400" /></div>
          <div className="mt-6 line-clamp-2 min-h-[2.8rem] text-[15px] font-black leading-snug tracking-[-0.02em] text-[#0a1020]">{data.live_menu?.main_dish ?? 'Menü ayrıştırılamadı'}</div>
          <div className="mt-2 line-clamp-1 text-[11px] text-slate-500">{data.live_menu?.soup ?? '—'} {data.live_menu?.calories ? `· ${data.live_menu.calories} kcal` : ''}</div>
          <div className="mt-5"><SourcePill source={data.live_menu?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between"><span className="bc-eyebrow">Mekik / Güney → Kuzey</span><BusFront size={17} className="text-slate-400" /></div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{data.live_shuttle?.next_departure ?? '—'}</div>
          <div className="mt-2 text-[11px] text-slate-500">Next published departure</div>
          <div className="mt-5"><SourcePill source={data.live_shuttle?.provenance} /></div>
        </article>

        <article className="bc-surface rounded-[24px] p-5">
          <div className="flex items-center justify-between"><span className="bc-eyebrow">BUIS / schedule</span><Database size={16} className="text-slate-400" /></div>
          <div className="mt-6 font-mono text-[32px] font-black leading-none tracking-[-0.05em] text-[#0a1020]">{(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')}</div>
          <div className="mt-2 text-[11px] text-slate-500">Course records in the current snapshot</div>
          <div className="mt-5"><SourcePill source={scheduleSource} /></div>
        </article>
      </section>

      <KPICards data={data} />

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.75fr)_minmax(350px,0.75fr)]">
        <div className="bc-surface rounded-[28px] p-3 sm:p-4">
          <div className="flex flex-col gap-3 px-2 pb-4 pt-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <div className="bc-eyebrow">Spatial intelligence</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Where the mission is happening</h2>
              <p className="mt-1 text-[11px] text-slate-500">Building colors visualize schedule-derived utilization, not live occupancy sensors.</p>
            </div>
            <Link href="/buildings" className="bc-focus-ring inline-flex items-center gap-1.5 self-start rounded-full border border-slate-950/10 bg-[#f4f5f2] px-3 py-1.5 text-[10px] font-black text-slate-700 transition hover:bg-white sm:self-auto">Open campus twin <ArrowRight size={11} /></Link>
          </div>
          <CampusMap buildings={data.buildings} />
        </div>

        <aside className="bc-surface flex min-h-[620px] flex-col rounded-[28px] p-4 sm:p-5">
          <div className="flex items-start justify-between gap-3 border-b border-slate-900/8 pb-4">
            <div>
              <div className="bc-eyebrow">Human decision queue</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">What deserves review?</h2>
              <p className="mt-1 text-[11px] leading-relaxed text-slate-500">Ranked model candidates. Nothing is dispatched automatically.</p>
            </div>
            <span className="grid h-9 w-9 shrink-0 place-items-center rounded-[13px] bg-[#0b1226] text-white"><Activity size={15} /></span>
          </div>
          <div className="mt-4 flex-1 overflow-y-auto pr-1"><ActionCards actions={data.actions} /></div>
          <Link href="/decisions" className="bc-focus-ring mt-4 flex items-center justify-center gap-2 rounded-[14px] bg-[#0b1226] px-4 py-3 text-[10px] font-black text-white">Open approval ledger <ArrowRight size={12} /></Link>
        </aside>
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.45fr)_minmax(320px,0.55fr)]">
        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="mb-7 flex items-start justify-between gap-4">
            <div><div className="bc-eyebrow">Schedule signal</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Where demand concentrates</h2><p className="mt-1 text-[11px] text-slate-500">Top buildings by estimated utilization at the current evaluation hour.</p></div>
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
          <div className="flex items-start justify-between"><div><div className="bc-eyebrow">Academic context</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Calendar pulse</h2></div><CalendarDays size={18} className="text-slate-400" /></div>
          <div className="mt-6 space-y-1">
            {(data.academic_calendar?.length ? data.academic_calendar : [calendarSource?.ok ? 'Resmî takvim erişilebilir; yapılandırılmış başlık alınamadı.' : 'Akademik takvim kaynağı canlı doğrulanamadı.'])
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
          <div><div className="bc-eyebrow">Data trust layer</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Every claim is auditable.</h2><p className="mt-1 max-w-2xl text-[11px] leading-relaxed text-slate-500">Live feed, official snapshot, external weather or model estimate: BOUNCAMPUS keeps the boundary visible and degrades instead of fabricating telemetry.</p></div>
          <div className="flex flex-wrap gap-2">
            <Link href="/data" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-full border border-slate-950/10 bg-white px-3 py-2 text-[10px] font-black text-slate-700">Open Data Trust <ArrowRight size={11} /></Link>
            <Link href="/api/v1/brief" target="_blank" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-full bg-[#0b1226] px-3 py-2 text-[10px] font-black text-white">Mission JSON <ArrowUpRight size={11} /></Link>
          </div>
        </div>

        <div className="mt-6 grid gap-2 md:grid-cols-2 xl:grid-cols-4">
          {(data.sources ?? []).map(source => (
            <a key={source.id} href={source.url} target={source.url.startsWith('http') ? '_blank' : undefined} rel={source.url.startsWith('http') ? 'noreferrer' : undefined} className="group rounded-[18px] border border-slate-950/8 bg-white/75 p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-sm">
              <div className="flex items-start justify-between gap-3"><SourcePill source={source} />{source.url.startsWith('http') && <ExternalLink size={12} className="mt-1 text-slate-300 transition group-hover:text-slate-600" />}</div>
              <h3 className="mt-4 text-[12px] font-black leading-snug tracking-[-0.01em] text-[#0a1020]">{source.label}</h3>
              <p className="mt-2 line-clamp-3 text-[10px] leading-relaxed text-slate-500">{source.detail}</p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
