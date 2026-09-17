'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, BookOpen, Building2, CloudSun, MapPin, ShieldCheck, Zap } from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { presentBuilding } from '@/lib/campus-directory';
import { actionTitle } from '@/lib/action-copy';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

export default function DashboardPage() {
  const { locale, t } = useLocale();
  const [data, setData] = useState<DashboardData | null>(null);
  useEffect(() => { getDashboard().then(setData); }, []);

  const energyActions = useMemo(() => (data?.actions ?? []).filter(action => action.type === 'energy'), [data]);
  const lowUseBuildings = useMemo(() => (data?.buildings ?? []).filter(building => (building.occupancy_ratio ?? 0) < 0.4), [data]);
  const utilization = useMemo(() => (data?.buildings ?? [])
    .map(building => ({ ...building, pct: Math.round((building.occupancy_ratio ?? 0) * 100) }))
    .sort((a, b) => a.pct - b.pct)
    .slice(0, 6), [data]);

  if (!data) return <div className="grid min-h-[58vh] place-items-center text-sm font-semibold text-slate-400">{t('Kampüs verileri yükleniyor…', 'Loading campus data…')}</div>;

  const facts = [
    { icon: CloudSun, label: t('Bebek hava', 'Bebek weather'), value: data.live_weather?.temperature == null ? '—' : `${data.live_weather.temperature}°C`, detail: t('HVAC yükü için dış koşul', 'Outdoor condition for HVAC load') },
    { icon: BookOpen, label: t('Ders kaydı', 'Course records'), value: (data.real_courses_loaded ?? 0).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US'), detail: t('Program tabanlı talep sinyali', 'Schedule-derived demand signal') },
    { icon: Building2, label: t('Düşük kullanım adayı', 'Low-use candidates'), value: lowUseBuildings.length.toString(), detail: t('Doluluk tahmini %40 altı', 'Estimated occupancy below 40%') },
    { icon: Zap, label: t('Enerji kararı adayı', 'Energy decision candidates'), value: energyActions.length.toString(), detail: t('İnsan incelemesi gerektirir', 'Requires human review') },
  ];

  return <div className="space-y-8">
    <section className="grid gap-8 border-b border-slate-900/10 pb-9 lg:grid-cols-[minmax(0,1fr)_370px] lg:items-end">
      <div>
        <div className="text-[10px] font-black uppercase tracking-[0.16em] text-emerald-700">{t('KREATE for Climate · Clean Energy + Carbon', 'KREATE for Climate · Clean Energy + Carbon')}</div>
        <h1 className="mt-3 max-w-4xl text-[40px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950 sm:text-[54px]">{t('Kampüs binalarındaki kaçınılabilir enerji israfını karara dönüştür.', 'Turn avoidable campus building energy waste into an operational decision.')}</h1>
        <p className="mt-5 max-w-3xl text-[13px] leading-6 text-slate-500">{t('BOUNCAMPUS; ders programı, hava durumu ve bina bağlamını birleştirerek düşük kullanım pencerelerini bulur, enerji müdahalelerini stres testinden geçirir ve yalnızca insan onayından sonra pilotlanabilecek öneriler üretir.', 'BOUNCAMPUS combines schedules, weather and building context to find low-use windows, stress-test energy interventions and surface recommendations that can only move to a pilot after human approval.')}</p>
        <div className="mt-5 flex flex-wrap gap-2">
          <Link href="/demo" className="inline-flex items-center gap-1.5 rounded-lg bg-[#102a43] px-4 py-2.5 text-[11px] font-black text-white">{t('90 saniyelik KREATE demosu', '90-second KREATE demo')} <ArrowRight size={12} /></Link>
          <Link href="/data" className="inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-4 py-2.5 text-[11px] font-black text-slate-700">{t('Veri provenansını gör', 'Inspect data provenance')}</Link>
        </div>
      </div>

      <aside className="border-l border-slate-900/10 pl-5">
        <div className="flex items-center gap-2 text-[11px] font-black text-slate-950"><ShieldCheck size={14} /> {t('Bugünkü kanıt sınırı', 'Evidence boundary today')}</div>
        <p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Gösterilen doluluk, enerji, tasarruf ve CO₂ değerleri model çıktısıdır. Gerçek etki ancak smart-meter ve anonim toplu doluluk verisiyle yapılacak pilot sonrası ölçülür.', 'Occupancy, energy, savings and CO₂ values shown here are model outputs. Real impact is established only after a pilot with smart-meter and anonymous aggregate occupancy data.')}</p>
        <div className="mt-4 grid grid-cols-3 gap-2 text-[9px] font-black uppercase tracking-[0.08em] text-slate-400"><span>SENSE</span><span>DECIDE</span><span>STRESS-TEST</span><span>APPROVE</span><span>PILOT</span><span>LEARN</span></div>
      </aside>
    </section>

    <section className="grid overflow-hidden rounded-xl border border-slate-900/10 bg-white sm:grid-cols-2 xl:grid-cols-4">
      {facts.map((fact, index) => { const Icon = fact.icon; return <article key={fact.label} className={`p-4 ${index > 0 ? 'border-t border-slate-900/10 sm:border-l sm:border-t-0' : ''} ${index === 2 ? 'sm:border-l-0 xl:border-l' : ''}`}><div className="flex items-center justify-between gap-3"><span className="text-[10px] font-black uppercase tracking-[0.11em] text-slate-400">{fact.label}</span><Icon size={14} className="text-slate-400" /></div><div className="mt-4 text-2xl font-black tracking-[-0.04em] text-slate-950">{fact.value}</div><div className="mt-1 text-[10px] leading-4 text-slate-500">{fact.detail}</div></article>; })}
    </section>

    <section className="rounded-2xl border border-slate-900/10 bg-white p-3 sm:p-4">
      <div className="flex flex-col gap-3 px-1 pb-4 sm:flex-row sm:items-end sm:justify-between"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Boğaziçi dijital kampüs bağlamı', 'Boğaziçi digital campus context')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('3D kampüste müdahale adaylarını gör', 'See intervention candidates in the 3D campus')}</h2><p className="mt-1 max-w-3xl text-[11px] leading-5 text-slate-500">{t('3D görünüm ürünün vitrin süsü değil; bina bazlı doluluk tahmini, konum ve karar bağlamını aynı yüzeyde tutar. Konumlar mümkün olduğunda kaynak-backed eşleştirilir.', 'The 3D view is not decoration; it keeps building-level occupancy estimates, location and decision context on one surface. Locations are source-backed whenever possible.')}</p></div><Link href="/buildings" className="inline-flex items-center gap-1.5 text-[11px] font-bold text-[#173f67]">{t('Bina dizinini aç', 'Open building directory')} <ArrowRight size={12} /></Link></div>
      <CampusMap buildings={data.buildings} />
    </section>

    <section className="grid gap-7 lg:grid-cols-2">
      <div className="border-t border-slate-900/10 pt-5">
        <div className="flex items-end justify-between gap-4"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Program tabanlı model', 'Schedule-derived model')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('En düşük kullanımlı binalar', 'Lowest-use buildings')}</h2></div><span className="text-[9px] font-bold text-slate-400">{t('canlı sensör değil', 'not a live sensor')}</span></div>
        <div className="mt-5 divide-y divide-slate-900/8">{utilization.map(building => { const display = presentBuilding(building, locale); return <div key={building.id} className="grid grid-cols-[minmax(0,1fr)_120px_38px] items-center gap-3 py-3"><div className="min-w-0"><div className="truncate text-[12px] font-bold text-slate-800">{display.name}</div><div className="mt-0.5 text-[9px] text-slate-400">{building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</div></div><div className="h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[#173f67]" style={{ width: `${building.pct}%` }} /></div><div className="text-right font-mono text-[10px] font-bold text-slate-500">{building.pct}%</div></div>; })}</div>
      </div>

      <div className="border-t border-slate-900/10 pt-5">
        <div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('İnsan onayı gerekli', 'Human review required')}</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-slate-950">{t('Enerji müdahalesi adayları', 'Energy intervention candidates')}</h2></div>
        <div className="mt-5 divide-y divide-slate-900/8">
          {energyActions.length ? energyActions.slice(0, 5).map(action => <div key={action.id} className="py-3"><div className="flex items-start justify-between gap-4"><div><div className="text-[12px] font-bold text-slate-800">{actionTitle(action, locale)}</div><div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-[9px] text-slate-400"><span className="inline-flex items-center gap-1"><MapPin size={9} /> {action.location}</span><span>{action.time}</span></div></div><div className="shrink-0 text-right"><div className="font-mono text-[11px] font-black text-slate-700">{action.impact_value}</div><div className="text-[8px] text-slate-400">{action.impact_unit}</div></div></div></div>) : <div className="py-6 text-[10px] leading-5 text-slate-400">{t('Bugünkü model eşiğinin üzerinde enerji müdahalesi yok. Sistem karar uydurmak yerine izlemeye devam eder.', 'No energy intervention is above today’s model threshold. The system keeps monitoring instead of inventing a decision.')}</div>}
        </div>
        <Link href="/decisions" className="mt-4 inline-flex items-center gap-1.5 text-[11px] font-bold text-[#173f67]">{t('Karar kayıtlarını aç', 'Open decision ledger')} <ArrowRight size={12} /></Link>
      </div>
    </section>
  </div>;
}
