'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BarChart3,
  BookOpen,
  BusFront,
  CheckCircle2,
  CloudSun,
  Database,
  ExternalLink,
  MapPin,
  ShieldCheck,
  Sparkles,
  Utensils,
  Zap,
} from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import {
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_SOURCE,
  YEAR_OVER_YEAR_REDUCTION_PCT,
} from '@/lib/food-waste';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

export default function DashboardPage() {
  const { locale, t } = useLocale();
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard().then(setData).catch(() => setData(null));
  }, []);

  const foodModel = useMemo(() => {
    if (!data?.food_demand_meals || data.food_demand_meals <= 0) return null;
    return Math.round(data.food_demand_meals);
  }, [data]);

  const sourceCount = data?.sources?.length ?? 0;
  const courses = data?.real_courses_loaded ?? 0;
  const weather = data?.live_weather?.temperature;

  return (
    <div className="space-y-8 sm:space-y-10">
      <section className="bc-panel-dark bc-grid-bg relative overflow-hidden rounded-[30px] p-6 text-white sm:p-8 lg:p-10">
        <div aria-hidden="true" className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-[#b8e467]/10 blur-3xl" />
        <div className="relative grid gap-10 lg:grid-cols-[minmax(0,1.22fr)_minmax(340px,.78fr)] lg:items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Sparkles size={12} /> {t('KREATE for Climate · BOUNCAMPUS', 'KREATE for Climate · BOUNCAMPUS')}
            </div>
            <h1 className="mt-4 max-w-5xl text-[42px] font-black leading-[.96] tracking-[-0.065em] sm:text-[60px] lg:text-[68px]">
              {t('Kampüsün 48.251 kg yemek atığını, önlenebilir bir operasyona çeviriyoruz.', 'We turn 48,251 kg of campus food waste into an operation that can prevent the next kilogram.')}
            </h1>
            <p className="mt-5 max-w-3xl text-[12px] leading-6 text-white/62 sm:text-[13px]">
              {t(
                'Resmi atık geçmişi + ders programı + akademik takvim + hava + menü bağlamı → servis talep bandı → insan onayı → ölçümlü pilot → öğrenme. BOUNCAMPUS’ın hackathon odağı tek ve ölçülebilir: yemekhane fazla üretimini ve atığı azaltmak.',
                'Official waste history + schedules + academic calendar + weather + menu context → service demand band → human approval → measured pilot → learning. The hackathon focus is singular and measurable: reduce cafeteria overproduction and food waste.',
              )}
            </p>

            <div className="mt-7 flex flex-wrap gap-2">
              <Link href="/food-waste" className="inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[10px] font-black text-[#071c33] shadow-[0_16px_40px_rgba(184,228,103,.16)] transition hover:-translate-y-0.5">
                <Utensils size={13} /> {t('Ürünü aç', 'Open product')} <ArrowRight size={11} />
              </Link>
              <Link href="/demo" className="inline-flex items-center gap-2 rounded-xl border border-white/12 bg-white/[0.07] px-4 py-3 text-[10px] font-black text-white transition hover:bg-white/[0.12]">
                <Sparkles size={13} /> {t('90 sn jüri modu', '90 sec jury mode')}
              </Link>
              <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 rounded-xl border border-white/12 px-4 py-3 text-[10px] font-black text-white/72 transition hover:text-white">
                <Database size={12} /> {t('Resmi veri', 'Official data')} <ExternalLink size={9} />
              </a>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <HeroMetric label={t('2025 resmi atık', 'Official 2025 waste')} value={FOOD_WASTE_BASELINE.year2025WasteKg.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} suffix="kg" />
            <HeroMetric label={t('Geri kazanıma giden', 'Sent to recovery')} value={FOOD_WASTE_BASELINE.year2025RecoveredKg.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} suffix="kg" />
            <HeroMetric label={t('2024→2025', '2024→2025')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}`} suffix="%" />
            <HeroMetric label={t('Yemekhane kapasitesi', 'Dining capacity')} value={FOOD_WASTE_BASELINE.diningHallCapacity.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-4">
        <SignalCard icon={Database} label={t('Resmi problem', 'Measured problem')} value="48.251 kg" detail={t('2025 yemek atığı', '2025 food waste')} provenance="OFFICIAL_PUBLIC" />
        <SignalCard icon={BookOpen} label={t('Talep bağlamı', 'Demand context')} value={courses ? courses.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail={t('program kaydı', 'schedule records')} provenance="OFFICIAL_SNAPSHOT" />
        <SignalCard icon={CloudSun} label={t('Dış koşul', 'Outdoor condition')} value={weather == null ? '—' : `${weather}°C`} detail={t('hava sinyali', 'weather signal')} provenance="EXTERNAL_LIVE" />
        <SignalCard icon={BarChart3} label={t('Servis talep modeli', 'Service demand model')} value={foodModel ? foodModel.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail={t('öğün planlama tahmini', 'meal-planning estimate')} provenance="MODEL_ESTIMATE" />
      </section>

      <section className="grid gap-4 lg:grid-cols-[.78fr_1.22fr]">
        <div className="bc-panel rounded-[26px] p-5 sm:p-6">
          <div className="bc-eyebrow">{t('Neden bu problem?', 'Why this problem?')}</div>
          <h2 className="mt-2 text-[30px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950">
            {t('Çünkü etkiyi jüriye model çıktısıyla değil, gerçek baz çizgisiyle gösteriyoruz.', 'Because we show the jury impact from a measured baseline, not from invented telemetry.')}
          </h2>
          <p className="mt-4 text-[10px] leading-5 text-slate-500">
            {t(
              'Boğaziçi 2024’te 50.993 kg, 2025’te 48.251 kg yemek atığı raporladı. Üniversite zaten porsiyon kontrolü, kompost ve fazla yemeğin değerlendirilmesi gibi yöntemler kullanıyor. BOUNCAMPUS eksik halkayı hedefliyor: bir sonraki servis için ne kadar üretileceğini veriyle planlamak ve sonucu ölçerek öğrenmek.',
              'Boğaziçi reported 50,993 kg of food waste in 2024 and 48,251 kg in 2025. The university already uses portion control, composting and surplus-food recovery. BOUNCAMPUS targets the missing loop: plan how much to produce for the next service and learn from measured outcomes.',
            )}
          </p>
          <Link href="/food-waste" className="mt-5 inline-flex items-center gap-1.5 text-[10px] font-black text-[#173f67]">
            {t('Resmi baz çizgisi + senaryo laboratuvarı', 'Official baseline + scenario lab')} <ArrowRight size={10} />
          </Link>
        </div>

        <div className="bc-panel-dark rounded-[26px] p-5 text-white sm:p-6">
          <div className="flex items-center justify-between gap-3">
            <div className="text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]">{t('Tek operasyon döngüsü', 'One operating loop')}</div>
            <ShieldCheck size={16} className="text-white/35" />
          </div>
          <div className="mt-6 grid gap-2 sm:grid-cols-5">
            {[
              ['01', t('TAHMİN', 'FORECAST'), t('Talep bandı', 'Demand band')],
              ['02', t('ÖNER', 'RECOMMEND'), t('Üretim bandı', 'Production band')],
              ['03', t('ONAY', 'APPROVE'), t('Mutfak sorumlusu', 'Kitchen operator')],
              ['04', t('ÖLÇ', 'MEASURE'), t('Üret / servis / atık', 'Produce / serve / waste')],
              ['05', t('ÖĞREN', 'LEARN'), t('Modeli kalibre et', 'Calibrate model')],
            ].map(([step, title, detail], index) => (
              <div key={step} className="rounded-2xl border border-white/10 bg-white/[0.055] p-4">
                <div className="flex items-center justify-between"><span className="font-mono text-[8px] font-black text-[#b8e467]">{step}</span>{index === 4 ? <CheckCircle2 size={10} className="text-[#b8e467]" /> : <span className="text-white/20">→</span>}</div>
                <div className="mt-5 text-[9px] font-black tracking-[0.06em]">{title}</div>
                <div className="mt-1 text-[8px] leading-4 text-white/42">{detail}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bc-panel overflow-hidden rounded-[28px] p-3 sm:p-4">
        <div className="flex flex-col gap-4 px-2 pb-4 pt-2 sm:px-3 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="bc-eyebrow">{t('Kampüs operasyon bağlamı', 'Campus operating context')}</div>
            <h2 className="mt-2 text-[29px] font-black tracking-[-0.05em] text-slate-950 sm:text-[36px]">
              {t('Yemekhane kararını kampüsün geri kalanından koparmıyoruz.', 'The dining decision stays connected to the rest of campus.')}
            </h2>
            <p className="mt-2 max-w-3xl text-[10px] leading-5 text-slate-500">
              {t(
                'Derslerin nerede ve ne zaman yoğunlaştığı, kampüsler arası hareket ve hava koşulları talebi etkiler. 3D/harita katmanı ürünün ölçeklenebilir kampüs bağlamını korur.',
                'Where and when classes concentrate, inter-campus movement and weather all shape demand. The map/3D layer preserves the scalable campus context behind the focused food-waste wedge.',
              )}
            </p>
          </div>
          <span className="bc-chip border-slate-950/[0.08] bg-[#f7f9f6] text-slate-500"><MapPin size={10} /> {t('Boğaziçi kampüs bağlamı', 'Boğaziçi campus context')}</span>
        </div>
        {data ? <CampusMap buildings={data.buildings} /> : <div className="grid h-[460px] place-items-center rounded-[22px] bg-slate-50 text-[10px] font-black uppercase tracking-[0.12em] text-slate-300">{t('Kampüs bağlamı yükleniyor…', 'Loading campus context…')}</div>}
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <ExpansionCard icon={Zap} title={t('Enerji kararları', 'Energy decisions')} body={t('Mevcut bina enerji ve senaryo yetenekleri korunuyor; hackathon ana hikâyesini bölmeden ikinci dikey olarak hazır.', 'Existing building-energy and scenario capabilities remain available as a second vertical without diluting the hackathon story.')} href="/scenarios" />
        <ExpansionCard icon={BusFront} title={t('Akıllı hareketlilik', 'Smart mobility')} body={t('Resmi mekik rotaları ve iklim senaryoları platform genişlemesi olarak korunuyor.', 'Source-backed shuttle routes and climate scenarios remain as platform expansion.')} href="/mobility" />
        <ExpansionCard icon={ShieldCheck} title={t('Kanıt katmanı', 'Evidence layer')} body={t('Her veri resmi, dış canlı, snapshot veya model tahmini olarak işaretleniyor. Jüride güven kaybetmiyoruz.', 'Every input is marked as official, external live, snapshot or model estimate. The jury can see the truth boundary.')} href="/data" />
      </section>

      <section className="rounded-[24px] border border-slate-900/10 bg-[#f6f8f5] p-5 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="text-[9px] font-black uppercase tracking-[0.15em] text-slate-400">{t('Jüri cümlesi', 'Jury one-liner')}</div>
            <div className="mt-2 max-w-4xl text-[19px] font-black tracking-[-0.035em] text-slate-950">
              {t('“BOUNCAMPUS, kampüsün gerçek yemek atığı geçmişini kullanarak bir sonraki serviste ne kadar üretileceğini önerir ve başarısını atık kg/servis ile ölçer.”', '“BOUNCAMPUS uses a campus’s measured food-waste history to recommend how much to produce for the next service, then measures success in waste kg per service.”')}
            </div>
          </div>
          <div className="shrink-0 text-[9px] font-black text-slate-400">{sourceCount ? `${sourceCount} ${t('izlenen kaynak', 'tracked sources')}` : t('Kaynaklar yükleniyor', 'Loading sources')}</div>
        </div>
      </section>
    </div>
  );
}

function HeroMetric({ label, value, suffix }: { label: string; value: string; suffix?: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.06] p-4 backdrop-blur-sm">
      <div className="text-[8px] font-black uppercase tracking-[0.12em] text-white/42">{label}</div>
      <div className="mt-2 flex items-baseline gap-1"><span className="font-mono text-[25px] font-black tracking-[-0.05em]">{value}</span>{suffix ? <span className="text-[9px] font-black text-white/45">{suffix}</span> : null}</div>
    </div>
  );
}

function SignalCard({ icon: Icon, label, value, detail, provenance }: { icon: typeof Database; label: string; value: string; detail: string; provenance: string }) {
  return (
    <article className="bc-panel rounded-2xl p-4 sm:p-5">
      <div className="flex items-center justify-between gap-3"><span className="bc-label">{label}</span><Icon size={14} className="text-slate-400" /></div>
      <div className="mt-5 font-mono text-[29px] font-black tracking-[-0.055em] text-slate-950">{value}</div>
      <div className="mt-1 text-[9px] text-slate-500">{detail}</div>
      <div className="mt-3 text-[7px] font-black uppercase tracking-[0.11em] text-emerald-700">{provenance}</div>
    </article>
  );
}

function ExpansionCard({ icon: Icon, title, body, href }: { icon: typeof Zap; title: string; body: string; href: string }) {
  return (
    <article className="bc-panel rounded-[22px] p-5">
      <div className="grid h-9 w-9 place-items-center rounded-xl bg-[#071c33] text-white"><Icon size={15} /></div>
      <h3 className="mt-5 text-[17px] font-black tracking-[-0.035em] text-slate-950">{title}</h3>
      <p className="mt-2 text-[10px] leading-5 text-slate-500">{body}</p>
      <Link href={href} className="mt-4 inline-flex items-center gap-1 text-[9px] font-black text-[#173f67]">{title} <ArrowRight size={9} /></Link>
    </article>
  );
}
