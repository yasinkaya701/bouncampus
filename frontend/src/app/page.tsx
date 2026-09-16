'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, BookOpen, BusFront, CloudSun, ExternalLink, MapPin, ShieldCheck, Utensils } from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import type { SourceMeta } from '@/lib/live-sources';
import { useLocale } from '@/lib/i18n';
import { presentBuilding } from '@/lib/campus-directory';
import { actionTitle } from '@/lib/action-copy';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

function SourceState({ source }: { source?: SourceMeta }) {
  const { t } = useLocale();
  if (!source) return <span className="text-[9px] font-bold text-slate-400">{t('Kaynak yok', 'No source')}</span>;
  const live = source.ok && (source.provenance === 'OFFICIAL_LIVE' || source.provenance === 'EXTERNAL_LIVE');
  const label = live ? t('canlı', 'live') : source.provenance === 'OFFICIAL_SNAPSHOT' ? t('resmî snapshot', 'official snapshot') : t('kullanılamıyor', 'unavailable');
  return <span className={`text-[9px] font-bold ${live ? 'text-emerald-700' : source.provenance === 'OFFICIAL_SNAPSHOT' ? 'text-slate-500' : 'text-amber-700'}`}>{label}</span>;
}

export default function DashboardPage() {
  const { locale, t } = useLocale();
  const [data, setData] = useState<DashboardData | null>(null);
  useEffect(() => { getDashboard().then(setData); }, []);

  const utilization = useMemo(() => (data?.buildings ?? []).map(building => ({ ...building, pct: Math.round((building.occupancy_ratio ?? 0) * 100) })).sort((a, b) => b.pct - a.pct).slice(0, 7), [data]);
  if (!data) return <div className="grid min-h-[58vh] place-items-center text-sm font-semibold text-slate-400">{t('Kampüs verileri yükleniyor…', 'Loading campus data…')}</div>;

  const scheduleSource = data.sources?.find(source => source.id === 'boun-course-schedule');
  const qualityGood = data.data_quality?.mode !== 'DEGRADED';
  const facts = [
    { icon: CloudSun, label: t('Bebek hava', 'Bebek weather'), value: data.live_weather?.temperature == null ? '—' : `${data.live_weather.temperature}°C`, detail: data.live_weather?.humidity == null ? '' : `${t('Nem', 'Humidity')} ${data.live_weather.humidity}%`, source: data.live_weather?.provenance },
    { icon: BusFront, label: t('Sonraki mekik', 'Next shuttle'), value: data.live_shuttle?.next_departure ?? '—', detail: t('Yayınlanmış tarife', 'Published timetable'), source: data.live_shuttle?.provenance },
    { icon: Utensils, label: t('SKS menü', 'SKS menu'), value: data.live_menu?.main_dish ?? '—', detail: data.live_menu?.soup ?? '', source: data.live_menu?.provenance },
    { icon: BookOpen, label: t('Ders kaydı', 'Course records'), value: (data.real_courses_loaded ?? 0).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US'), detail: t('Mevcut snapshot', 'Current snapshot'), source: scheduleSource },
  ];

  return <div className="space-y-8">
    <section className="grid gap-7 border-b border-slate-900/10 pb-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-end"><div><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('Boğaziçi kampüs görünümü', 'Boğaziçi campus view')}</div><h1 className="mt-3 max-w-4xl text-[40px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950 sm:text-[52px]">{t('Kampüste bugün ne oluyor?', 'What is happening on campus today?')}</h1><p className="mt-4 max-w-2xl text-[13px] leading-6 text-slate-500">{t('Ders programı, resmî kampüs kaynakları, mekik, menü ve hava verisini tek görünümde toplar. Tahmin ile ölçümü birbirine karıştırmaz.', 'Brings schedules, official campus sources, shuttle, menu and weather into one view without mixing estimates with measured data.')}</p></div><div className="border-l border-slate-900/10 pl-5"><div className="flex items-center gap-2 text-[11px] font-black text-slate-950"><ShieldCheck size={14} /> {qualityGood ? t('Kaynak katmanı çalışıyor', 'Source layer available') : t('Kısıtlı veri modu', 'Degraded data mode')}</div><p className="mt-2 text-[10px] leading-5 text-slate-500">{data.data_quality?.note ?? t('Her kaynak kendi provenans bilgisiyle gösterilir.', 'Each source is shown with its own provenance.')}</p><div className="mt-3 font-mono text-[9px] text-slate-400">{data.date}</div></div></section>

    <section className="grid overflow-hidden rounded-xl border border-slate-900/10 bg-white sm:grid-cols-2 xl:grid-cols-4">{facts.map((fact, index) => { const Icon = fact.icon; return <article key={fact.label} className={`p-4 ${index > 0 ? 'border-t border-slate-900/10 sm:border-l sm:border-t-0' : ''} ${index === 2 ? 'sm:border-l-0 xl:border-l' : ''}`}><div className="flex items-center justify-between gap-3"><span className="text-[10px] font-black uppercase tracking-[0.11em] text-slate-400">{fact.label}</span><Icon size={14} className="text-slate-400" /></div><div className="mt-4 line-clamp-2 min-h-[2rem] text-xl font-black tracking-[-0.035em] text-slate-950">{fact.value}</div><div className="mt-1 min-h-[1rem] truncate text-[10px] text-slate-500">{fact.detail}</div><div className="mt-3"><SourceState source={fact.source} /></div></article>; })}</section>

    <section className="rounded-2xl border border-slate-900/10 bg-white p-3 sm:p-4"><div className="flex flex-col gap-3 px-1 pb-4 sm:flex-row sm:items-end sm:justify-between"><div><h2 className="text-xl font-black tracking-[-0.035em] text-slate-950">{t('Kampüs haritası', 'Campus map')}</h2><p className="mt-1 text-[11px] leading-5 text-slate-500">{t('Bina konumları mümkün olduğunda OpenStreetMap üzerinden eşleştirilir. Eşleşmeyen kayıtlar yedek konum olarak açıkça işaretlenir.', 'Building positions are matched from OpenStreetMap when possible. Unmatched records are explicitly marked as fallback positions.')}</p></div><Link href="/buildings" className="inline-flex items-center gap-1.5 text-[11px] font-bold text-[#173f67]">{t('Bina dizinini aç', 'Open building directory')} <ArrowRight size={12} /></Link></div><CampusMap buildings={data.buildings} /></section>

    <section className="grid gap-7 lg:grid-cols-2"><div className="border-t border-slate-900/10 pt-5"><div className="flex items-end justify-between gap-4"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Program tabanlı model', 'Schedule-derived model')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('Tahmini bina kullanımı', 'Estimated building use')}</h2></div><span className="text-[9px] font-bold text-slate-400">{t('canlı sensör değil', 'not a live sensor')}</span></div><div className="mt-5 divide-y divide-slate-900/8">{utilization.map(building => { const display = presentBuilding(building, locale); return <div key={building.id} className="grid grid-cols-[minmax(0,1fr)_120px_38px] items-center gap-3 py-3"><div className="min-w-0"><div className="truncate text-[12px] font-bold text-slate-800">{display.name}</div><div className="mt-0.5 text-[9px] text-slate-400">{building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</div></div><div className="h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[#173f67]" style={{ width: `${building.pct}%` }} /></div><div className="text-right font-mono text-[10px] font-bold text-slate-500">{building.pct}%</div></div>; })}</div></div><div className="border-t border-slate-900/10 pt-5"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('İnsan onayı gerekli', 'Human review required')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('İncelenecek öneriler', 'Items to review')}</h2></div><div className="mt-5 divide-y divide-slate-900/8">{data.actions.slice(0, 5).map(action => <div key={action.id} className="py-3"><div className="flex items-start justify-between gap-4"><div><div className="text-[12px] font-bold text-slate-800">{actionTitle(action, locale)}</div><div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-[9px] text-slate-400"><span className="inline-flex items-center gap-1"><MapPin size={9} /> {action.location}</span><span>{action.time}</span></div></div><div className="shrink-0 text-right"><div className="font-mono text-[11px] font-black text-slate-700">{action.impact_value}</div><div className="text-[8px] text-slate-400">{action.impact_unit}</div></div></div></div>)}</div><Link href="/decisions" className="mt-4 inline-flex items-center gap-1.5 text-[11px] font-bold text-[#173f67]">{t('Tüm karar kayıtları', 'All decision records')} <ArrowRight size={12} /></Link></div></section>

    <section id="sources" className="border-t border-slate-900/10 pt-6"><div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Kaynak şeffaflığı', 'Source transparency')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('Veri nereden geliyor?', 'Where does the data come from?')}</h2></div><Link href="/data" className="inline-flex items-center gap-1.5 text-[11px] font-bold text-[#173f67]">{t('Kaynak ayrıntıları', 'Source details')} <ArrowRight size={12} /></Link></div><div className="mt-5 divide-y divide-slate-900/8 border-y border-slate-900/10">{(data.sources ?? []).map(source => <a key={source.id} href={source.url} target={source.url.startsWith('http') ? '_blank' : undefined} rel={source.url.startsWith('http') ? 'noreferrer' : undefined} className="grid gap-2 py-3 transition hover:bg-white sm:grid-cols-[180px_150px_minmax(0,1fr)_20px] sm:items-center sm:px-2"><div className="text-[11px] font-bold text-slate-800">{source.label}</div><SourceState source={source} /><div className="text-[10px] leading-5 text-slate-500">{source.detail}</div>{source.url.startsWith('http') ? <ExternalLink size={11} className="text-slate-300" /> : <span />}</a>)}</div></section>
  </div>;
}
