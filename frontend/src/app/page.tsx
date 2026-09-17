'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  Building2,
  CheckCircle2,
  CloudSun,
  Compass,
  MapPin,
  ShieldCheck,
  Sparkles,
  Zap,
} from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { presentBuilding } from '@/lib/campus-directory';
import { actionTitle } from '@/lib/action-copy';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

export default function DashboardPage() {
  const { locale, t } = useLocale();
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard().then(setData);
  }, []);

  const energyActions = useMemo(() => (data?.actions ?? []).filter(action => action.type === 'energy'), [data]);
  const lowUseBuildings = useMemo(() => (data?.buildings ?? []).filter(building => (building.occupancy_ratio ?? 0) < 0.4), [data]);
  const utilization = useMemo(
    () => (data?.buildings ?? [])
      .map(building => ({ ...building, pct: Math.round((building.occupancy_ratio ?? 0) * 100) }))
      .sort((a, b) => a.pct - b.pct)
      .slice(0, 6),
    [data],
  );

  if (!data) {
    return (
      <div className="space-y-5 py-4" aria-live="polite" aria-busy="true">
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {[0, 1, 2, 3].map(item => <div key={item} className="h-32 animate-pulse rounded-2xl border border-slate-950/[0.06] bg-white/70" />)}
        </div>
        <div className="h-[480px] animate-pulse rounded-[26px] border border-slate-950/[0.06] bg-white/70" />
        <div className="text-center text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('Kampüs karar bağlamı hazırlanıyor…', 'Preparing campus decision context…')}</div>
      </div>
    );
  }

  const sourceCount = data.sources?.length ?? 0;
  const qualityMode = data.data_quality?.mode ?? 'MODEL_SANDBOX';
  const qualityLabel = qualityMode === 'LIVE_PUBLIC_DATA'
    ? t('Kamu verisi aktif', 'Public data active')
    : qualityMode === 'DEGRADED'
      ? t('Kısmi veri modu', 'Partial data mode')
      : t('Model sandbox', 'Model sandbox');

  const facts = [
    {
      icon: CloudSun,
      label: t('Bebek dış koşulu', 'Bebek outdoor condition'),
      value: data.live_weather?.temperature == null ? '—' : `${data.live_weather.temperature}°C`,
      detail: t('HVAC kararına bağlanan hava sinyali', 'Weather signal connected to HVAC decisions'),
    },
    {
      icon: BookOpen,
      label: t('Ders programı kaydı', 'Course schedule records'),
      value: (data.real_courses_loaded ?? 0).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US'),
      detail: t('Talep tahmini için kullanılan program bağlamı', 'Schedule context used for demand estimation'),
    },
    {
      icon: Building2,
      label: t('Düşük kullanım adayı', 'Low-use candidates'),
      value: lowUseBuildings.length.toString(),
      detail: t('Model doluluğu %40 altında görünen bina', 'Buildings estimated below 40% occupancy'),
    },
    {
      icon: Zap,
      label: t('Enerji kararı adayı', 'Energy decision candidates'),
      value: energyActions.length.toString(),
      detail: t('Pilot öncesi insan incelemesine gönderilir', 'Sent to human review before any pilot'),
    },
  ];

  return (
    <div className="space-y-8 sm:space-y-10">
      <section className="grid gap-4 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,.65fr)]">
        <div className="bc-panel rounded-[24px] p-5 sm:p-6 lg:p-7">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="bc-eyebrow">{t('Bugünün operasyon özeti', 'Today’s operational brief')}</div>
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-900/10 bg-emerald-50 px-2.5 py-1 text-[8px] font-black uppercase tracking-[0.11em] text-emerald-700">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-emerald-500" /> {qualityLabel}
            </div>
          </div>

          <div className="mt-5 grid gap-6 xl:grid-cols-[minmax(0,1fr)_250px] xl:items-end">
            <div>
              <h2 className="max-w-3xl text-[29px] font-black leading-[1.03] tracking-[-0.055em] text-slate-950 sm:text-[36px]">
                {energyActions.length
                  ? t('Bugün sistem müdahale edilebilir enerji israfı pencereleri görüyor.', 'Today the system sees actionable windows of avoidable energy waste.')
                  : t('Bugün eşik üstü müdahale yok; sistem karar uydurmuyor.', 'No intervention clears the threshold today; the system does not invent decisions.')}
              </h2>
              <p className="mt-3 max-w-2xl text-[11px] leading-5 text-slate-500 sm:text-[12px] sm:leading-6">
                {t(
                  'Ders programı, hava durumu ve bina bağlamı birlikte okunuyor. Çıktı doğrudan otomasyon değil; stres testinden ve insan onayından geçecek ölçülebilir bir pilot önerisi.',
                  'Schedules, weather and building context are read together. The output is not direct automation; it is a measurable pilot recommendation that must pass stress-testing and human approval.',
                )}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-950/[0.07] bg-[#f6f8f5] p-4">
              <div className="bc-label">{t('Karar motoru', 'Decision engine')}</div>
              <div className="mt-3 grid grid-cols-2 gap-3">
                <div>
                  <div className="bc-metric-value bc-mono">{energyActions.length}</div>
                  <div className="mt-0.5 text-[9px] font-semibold text-slate-500">{t('inceleme adayı', 'review candidates')}</div>
                </div>
                <div>
                  <div className="bc-metric-value bc-mono">{sourceCount || '—'}</div>
                  <div className="mt-0.5 text-[9px] font-semibold text-slate-500">{t('izlenen kaynak', 'tracked sources')}</div>
                </div>
              </div>
              <Link href="/decisions" className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-black text-[#123f68] hover:text-slate-950">
                {t('Karar günlüğünü aç', 'Open decision ledger')} <ArrowRight size={11} />
              </Link>
            </div>
          </div>
        </div>

        <aside className="bc-panel-dark relative overflow-hidden rounded-[24px] p-5 text-white sm:p-6">
          <div aria-hidden="true" className="absolute -right-14 -top-14 h-44 w-44 rounded-full bg-[#b8e467]/10 blur-3xl" />
          <div className="relative">
            <div className="flex items-center justify-between gap-3">
              <div className="text-[9px] font-black uppercase tracking-[0.16em] text-[#b8e467]">{t('Kanıt sınırı', 'Evidence boundary')}</div>
              <ShieldCheck size={16} className="text-white/40" />
            </div>
            <h3 className="mt-4 text-xl font-black tracking-[-0.04em]">{t('Ne bildiğimizi ve neyi tahmin ettiğimizi ayırıyoruz.', 'We separate what we know from what we estimate.')}</h3>
            <p className="mt-3 text-[10px] leading-5 text-white/58">
              {t(
                'Doluluk, enerji, tasarruf ve CO₂ çıktıları model tahminidir. Gerçek iklim etkisi ancak smart-meter ve anonim toplu doluluk verisiyle yürütülecek pilot sonrası ölçülür.',
                'Occupancy, energy, savings and CO₂ outputs are model estimates. Real climate impact is established only after a pilot with smart-meter and anonymous aggregate occupancy data.',
              )}
            </p>
            <Link href="/data" className="mt-5 inline-flex items-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.07] px-3 py-2 text-[9px] font-black text-white transition hover:bg-white/[0.12]">
              <ShieldCheck size={11} /> {t('Kaynak provenansını incele', 'Inspect source provenance')}
            </Link>
          </div>
        </aside>
      </section>

      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4" aria-label={t('Kampüs durum metrikleri', 'Campus status metrics')}>
        {facts.map(fact => {
          const Icon = fact.icon;
          return (
            <article key={fact.label} className="bc-panel group rounded-2xl p-4 transition duration-200 hover:-translate-y-0.5 hover:border-slate-950/15 sm:p-5">
              <div className="flex items-center justify-between gap-3">
                <span className="bc-label">{fact.label}</span>
                <span className="grid h-8 w-8 place-items-center rounded-xl border border-slate-950/[0.07] bg-[#f7f9f6] text-slate-500 transition group-hover:bg-[#071c33] group-hover:text-white">
                  <Icon size={14} />
                </span>
              </div>
              <div className="mt-5 text-[30px] font-black tracking-[-0.06em] text-slate-950 bc-mono">{fact.value}</div>
              <div className="mt-1.5 text-[9px] leading-4 text-slate-500">{fact.detail}</div>
            </article>
          );
        })}
      </section>

      <section className="bc-panel-dark bc-grid-bg overflow-hidden rounded-[26px] p-5 text-white sm:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]"><Sparkles size={12} /> {t('Karar zinciri', 'Decision chain')}</div>
            <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] sm:text-[34px]">{t('Tahminden otomasyona atlamıyoruz.', 'We do not jump from prediction to automation.')}</h2>
            <p className="mt-2 max-w-2xl text-[10px] leading-5 text-white/55">{t('Her öneri görünür bir güvenlik ve öğrenme zincirinden geçer. Jüriye gösterdiğimiz fark yalnızca model değil; uygulanabilir operasyon protokolü.', 'Every recommendation moves through a visible safety and learning chain. The differentiator is not only the model; it is an operational protocol that can actually be piloted.')}</p>
          </div>
          <Link href="/flow" className="inline-flex shrink-0 items-center gap-2 text-[10px] font-black text-white/80 transition hover:text-white">{t('Tam akışı aç', 'Open full flow')} <ArrowRight size={12} /></Link>
        </div>

        <div className="mt-7 grid gap-2 md:grid-cols-6">
          {[
            ['01', 'SENSE', t('Program + hava', 'Schedule + weather')],
            ['02', 'DECIDE', t('Düşük kullanım', 'Low-use window')],
            ['03', 'STRESS-TEST', t('Senaryo testi', 'Scenario test')],
            ['04', 'APPROVE', t('İnsan onayı', 'Human approval')],
            ['05', 'PILOT', t('Ölçülebilir saha', 'Measured field pilot')],
            ['06', 'LEARN', t('Sonucu geri besle', 'Feed outcome back')],
          ].map(([step, label, detail], index) => (
            <div key={label} className="relative rounded-2xl border border-white/9 bg-white/[0.055] p-3.5 backdrop-blur-sm">
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-[8px] font-black text-[#b8e467]">{step}</span>
                {index < 5 ? <span className="hidden text-white/20 md:block">→</span> : <CheckCircle2 size={11} className="text-[#b8e467]" />}
              </div>
              <div className="mt-5 text-[9px] font-black tracking-[0.08em] text-white">{label}</div>
              <div className="mt-1 text-[8px] leading-4 text-white/45">{detail}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="bc-panel overflow-hidden rounded-[26px] p-3 sm:p-4">
        <div className="flex flex-col gap-4 px-2 pb-4 pt-2 sm:px-3 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="bc-eyebrow">{t('Boğaziçi dijital kampüs bağlamı', 'Boğaziçi digital campus context')}</div>
            <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950 sm:text-[34px]">{t('Kararı haritada değil, kampüsün içinde gör.', 'See the decision inside the campus, not beside a map.')}</h2>
            <p className="mt-2 max-w-3xl text-[10px] leading-5 text-slate-500 sm:text-[11px]">
              {t(
                'Bina bazlı doluluk tahmini, konum ve müdahale bağlamı aynı yüzeyde kalır. 3D katman vitrin süsü değil; operatörün “nerede, neden, ne zaman?” sorusunu tek bakışta cevaplar.',
                'Building-level occupancy estimates, location and intervention context stay on one surface. The 3D layer is not decoration; it answers “where, why and when?” at a glance.',
              )}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="bc-chip border-slate-950/[0.08] bg-[#f7f9f6] text-slate-500"><MapPin size={10} /> {t('Kaynaklı konumlar', 'Source-backed locations')}</span>
            <Link href="/buildings" className="bc-button-secondary !px-3 !py-2">{t('Bina dizini', 'Building directory')} <ArrowRight size={11} /></Link>
          </div>
        </div>
        <div className="overflow-hidden rounded-[20px] border border-slate-950/[0.08] bg-[#e7eeeb] shadow-inner">
          <CampusMap buildings={data.buildings} />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex items-end justify-between gap-4">
            <div>
              <div className="bc-eyebrow">{t('Program tabanlı model', 'Schedule-derived model')}</div>
              <h2 className="mt-2 text-2xl font-black tracking-[-0.045em] text-slate-950">{t('En düşük kullanımlı binalar', 'Lowest-use buildings')}</h2>
            </div>
            <span className="rounded-full border border-amber-900/10 bg-amber-50 px-2.5 py-1 text-[8px] font-black text-amber-700">{t('sensör değil', 'not a sensor')}</span>
          </div>

          <div className="mt-5 space-y-1">
            {utilization.map((building, index) => {
              const display = presentBuilding(building, locale);
              return (
                <div key={building.id} className="group grid grid-cols-[28px_minmax(0,1fr)_110px_38px] items-center gap-3 rounded-xl px-2 py-2.5 transition hover:bg-[#f7f9f6] sm:grid-cols-[32px_minmax(0,1fr)_150px_42px]">
                  <div className="grid h-7 w-7 place-items-center rounded-lg bg-slate-950/[0.045] font-mono text-[8px] font-black text-slate-400">0{index + 1}</div>
                  <div className="min-w-0">
                    <div className="truncate text-[11px] font-black text-slate-800">{display.name}</div>
                    <div className="mt-0.5 text-[8px] font-semibold uppercase tracking-[0.08em] text-slate-400">{building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</div>
                  </div>
                  <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-gradient-to-r from-[#0d7c66] to-[#87bd69] transition-all" style={{ width: `${building.pct}%` }} />
                  </div>
                  <div className="text-right font-mono text-[9px] font-black text-slate-500">{building.pct}%</div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex items-end justify-between gap-4">
            <div>
              <div className="bc-eyebrow">{t('İnsan onayı gerekli', 'Human review required')}</div>
              <h2 className="mt-2 text-2xl font-black tracking-[-0.045em] text-slate-950">{t('Enerji müdahalesi adayları', 'Energy intervention candidates')}</h2>
            </div>
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-[#071c33] text-[#b8e467]"><Zap size={15} /></span>
          </div>

          <div className="mt-5 space-y-2">
            {energyActions.length ? energyActions.slice(0, 5).map(action => (
              <div key={action.id} className="rounded-2xl border border-slate-950/[0.07] bg-[#fbfcfa] p-3.5 transition hover:border-slate-950/15 hover:bg-white">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="text-[11px] font-black leading-5 text-slate-800">{actionTitle(action, locale)}</div>
                    <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-[8px] font-semibold text-slate-400">
                      <span className="inline-flex items-center gap-1"><MapPin size={9} /> {action.location}</span>
                      <span>{action.time}</span>
                      <span>{t('model tahmini', 'model estimate')}</span>
                    </div>
                  </div>
                  <div className="shrink-0 rounded-xl bg-white px-2.5 py-2 text-right shadow-sm ring-1 ring-slate-950/[0.06]">
                    <div className="font-mono text-[11px] font-black text-slate-800">{action.impact_value}</div>
                    <div className="mt-0.5 text-[7px] font-bold uppercase tracking-[0.08em] text-slate-400">{action.impact_unit}</div>
                  </div>
                </div>
              </div>
            )) : (
              <div className="grid min-h-52 place-items-center rounded-2xl border border-dashed border-slate-950/10 bg-[#fbfcfa] p-6 text-center">
                <div>
                  <CheckCircle2 size={24} className="mx-auto text-emerald-600" />
                  <div className="mt-3 text-[12px] font-black text-slate-800">{t('Eşik üstü müdahale yok', 'No intervention clears the threshold')}</div>
                  <div className="mx-auto mt-1 max-w-xs text-[9px] leading-4 text-slate-400">{t('Sistem sahte bir aksiyon üretmek yerine izlemeye devam ediyor.', 'The system keeps monitoring instead of manufacturing an action.')}</div>
                </div>
              </div>
            )}
          </div>

          <Link href="/decisions" className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-black text-[#123f68] hover:text-slate-950">{t('Tüm karar kayıtlarını aç', 'Open all decision records')} <ArrowRight size={11} /></Link>
        </div>
      </section>

      <section className="relative overflow-hidden rounded-[26px] border border-slate-950/[0.08] bg-[linear-gradient(135deg,#e8f4e4_0%,#edf6f5_48%,#f8faf7_100%)] p-6 sm:p-8">
        <div aria-hidden="true" className="absolute -right-10 -top-20 h-64 w-64 rounded-full border-[36px] border-white/45" />
        <div className="relative grid gap-6 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-emerald-700"><Compass size={12} /> {t('Jüri için tek cümle', 'One sentence for the jury')}</div>
            <h2 className="mt-3 max-w-4xl text-[28px] font-black leading-[1.04] tracking-[-0.055em] text-slate-950 sm:text-[38px]">
              {t('“BOUNCAMPUS, kampüs verisini dashboard’a değil, ölçülebilir iklim kararına dönüştürüyor.”', '“BOUNCAMPUS turns campus data not into a dashboard, but into a measurable climate decision.”')}
            </h2>
          </div>
          <Link href="/demo" className="bc-button-primary !px-5 !py-3.5">{t('Jüri demosunu başlat', 'Launch jury demo')} <ArrowRight size={13} /></Link>
        </div>
      </section>
    </div>
  );
}
