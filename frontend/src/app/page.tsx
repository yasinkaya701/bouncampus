'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BarChart3,
  BookOpen,
  Box,
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
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  YEAR_OVER_YEAR_REDUCTION_PCT,
} from '@/lib/food-waste';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), {
  ssr: false,
  loading: () => <MapSkeleton />,
});

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

  const courses = data?.real_courses_loaded ?? 0;
  const weather = data?.live_weather?.temperature;
  const sourceCount = data?.sources?.length ?? 0;
  const officialLive = data?.data_quality?.official_live_sources ?? 0;
  const qualityMode = data?.data_quality?.mode ?? 'CHECKING';

  return (
    <div className="space-y-5 sm:space-y-6">
      <section className="bc-command-hero relative overflow-hidden rounded-[34px] border border-white/8 bg-[#06131f] text-white shadow-[0_30px_80px_rgba(7,19,31,.18)]">
        <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_16%_12%,rgba(184,228,103,.16),transparent_26rem),radial-gradient(circle_at_88%_18%,rgba(76,166,210,.16),transparent_28rem)]" />
        <div aria-hidden="true" className="bc-hero-noise absolute inset-0 opacity-[0.09]" />

        <div className="relative grid lg:grid-cols-[minmax(0,1.02fr)_minmax(430px,.98fr)]">
          <div className="flex min-h-[520px] flex-col justify-between p-6 sm:p-8 lg:p-10 xl:p-12">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="inline-flex items-center gap-2 rounded-full border border-[#b8e467]/20 bg-[#b8e467]/10 px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-[#dff6ae]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#b8e467] shadow-[0_0_18px_rgba(184,228,103,.9)]" />
                  {t('KREATE for Climate · çalışan ürün', 'KREATE for Climate · working product')}
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.045] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.12em] text-white/58">
                  <ShieldCheck size={10} /> {t('Kaynak sınırı açık', 'Truth boundary visible')}
                </span>
              </div>

              <div className="mt-8 text-[10px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
                {t('Kampüs operasyon zekâsı', 'Campus operations intelligence')}
              </div>
              <h1 className="mt-3 max-w-4xl text-[44px] font-black leading-[0.93] tracking-[-0.07em] sm:text-[62px] xl:text-[72px]">
                {t('Bir sonraki öğünde daha az atık üretmek için karar ver.', 'Make the next meal produce less waste.')}
              </h1>
              <p className="mt-6 max-w-2xl text-[12px] leading-6 text-white/60 sm:text-[13px]">
                {t(
                  'BOUNCAMPUS; resmi yemek atığı geçmişini, ders yoğunluğunu, hava koşullarını ve talep modelini tek bir karar ekranında birleştirir. Çıktı otomatik emir değil; kaynağı görünen, belirsizliği açık ve insan onaylı bir pilot kararıdır.',
                  'BOUNCAMPUS combines official food-waste history, timetable density, weather and the demand model in one decision surface. The output is not an automatic command; it is a source-visible, uncertainty-aware, human-approved pilot decision.',
                )}
              </p>

              <div className="mt-8 flex flex-wrap gap-2.5">
                <Link href="/food-waste" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[10px] font-black text-[#071c33] shadow-[0_18px_45px_rgba(184,228,103,.2)] transition hover:-translate-y-0.5">
                  <Utensils size={13} /> {t('Karar motorunu aç', 'Open decision engine')} <ArrowRight size={11} />
                </Link>
                <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/12 bg-white/[0.06] px-4 py-3 text-[10px] font-black text-white transition hover:bg-white/[0.1]">
                  <Sparkles size={13} /> {t('90 sn jüri modu', '90 sec jury mode')}
                </Link>
                <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/12 px-4 py-3 text-[10px] font-black text-white/68 transition hover:text-white">
                  <Database size={12} /> {t('Resmi veri', 'Official source')} <ExternalLink size={9} />
                </a>
              </div>
            </div>

            <div className="mt-10 grid grid-cols-2 gap-2.5 border-t border-white/[0.08] pt-5 sm:grid-cols-4">
              <HeroStat label={t('2025 resmi atık', 'Official 2025 waste')} value={FOOD_WASTE_BASELINE.year2025WasteKg.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} suffix="kg" />
              <HeroStat label={t('2024→2025', '2024→2025')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}`} suffix="%" />
              <HeroStat label={t('Pilot başarı kapısı', 'Pilot success gate')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}`} suffix="%" muted={t('hedef, sonuç değil', 'target, not result')} />
              <HeroStat label={t('İnsan kapısı', 'Human gate')} value={t('Zorunlu', 'Required')} />
            </div>
          </div>

          <div className="relative flex min-h-[520px] flex-col justify-between border-t border-white/[0.08] bg-white/[0.025] p-4 sm:p-5 lg:border-l lg:border-t-0 lg:p-6">
            <div className="flex items-center justify-between gap-3 px-1 pb-4">
              <div>
                <div className="text-[9px] font-black uppercase tracking-[0.16em] text-white/38">{t('Karar penceresi', 'Decision window')}</div>
                <div className="mt-1 text-[20px] font-black tracking-[-0.04em]">{t('Şu an elimizde ne var?', 'What do we know right now?')}</div>
              </div>
              <span className={`rounded-full border px-2.5 py-1.5 font-mono text-[8px] font-black ${qualityMode === 'LIVE_PUBLIC_DATA' ? 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200' : 'border-amber-300/20 bg-amber-300/10 text-amber-200'}`}>
                {qualityMode === 'LIVE_PUBLIC_DATA' ? 'PUBLIC DATA ONLINE' : 'SOURCE CHECK'}
              </span>
            </div>

            <div className="grid flex-1 gap-3 sm:grid-cols-2">
              <LiveSignal icon={BarChart3} label={t('Öğle talep modeli', 'Lunch demand model')} value={foodModel ? foodModel.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail={t('öğün · MODEL_ESTIMATE', 'meals · MODEL_ESTIMATE')} emphasis />
              <LiveSignal icon={CloudSun} label={t('Dış koşul', 'Outdoor condition')} value={weather == null ? '—' : `${weather}°C`} detail="EXTERNAL_LIVE" />
              <LiveSignal icon={BookOpen} label={t('Ders bağlamı', 'Timetable context')} value={courses ? courses.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail="OFFICIAL_SNAPSHOT" />
              <LiveSignal icon={Database} label={t('Sağlıklı resmi canlı kaynak', 'Healthy official live sources')} value={officialLive ? String(officialLive) : '—'} detail={sourceCount ? `${sourceCount} ${t('izlenen kaynak', 'tracked sources')}` : t('kontrol ediliyor', 'checking')} />
            </div>

            <div className="mt-3 rounded-2xl border border-white/10 bg-[#0a1b2a]/86 p-4 backdrop-blur-xl">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.12em] text-[#dff6ae]"><ShieldCheck size={11} /> {t('Karar güvenliği', 'Decision safety')}</div>
                <span className="rounded-full bg-white/[0.055] px-2 py-1 font-mono text-[8px] text-white/45">HUMAN APPROVAL</span>
              </div>
              <p className="mt-2 text-[10px] leading-5 text-white/48">
                {t('Canlı üniversite sensörü yoksa varmış gibi göstermiyoruz. Tahmin, snapshot ve resmi canlı kaynaklar arayüzde birbirinden ayrılıyor.', 'If university telemetry is not integrated, we do not pretend it is. Model estimates, snapshots and official live sources stay visibly separated.')}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="bc-panel overflow-hidden rounded-[30px] border border-slate-900/[0.07] bg-white p-3 shadow-[0_20px_60px_rgba(15,23,42,.06)] sm:p-4">
        <div className="flex flex-col gap-4 px-2 pb-4 pt-2 sm:px-3 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="bc-eyebrow flex items-center gap-2"><Box size={11} /> {t('Çalışan kampüs yüzeyi', 'Working campus surface')}</div>
            <h2 className="mt-2 max-w-4xl text-[30px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950 sm:text-[40px]">
              {t('Harita ayrı demo değil; kararın gerçek mekânsal bağlamı.', 'The map is not a side demo; it is the spatial context of the decision.')}
            </h2>
            <p className="mt-2 max-w-3xl text-[10px] leading-5 text-slate-500 sm:text-[11px]">
              {t('İlk açılışta birinci taraf Three.js geometri görünümü gelir. Harici fotogrametri sağlayıcısı yüklenemezse ürün boş ekran yerine otomatik olarak güvenilir kampüs 3D görünümüne geri döner.', 'The first view uses the first-party Three.js geometry surface. If the external photogrammetry provider cannot load, the product falls back to the reliable campus 3D view instead of leaving a blank frame.')}
            </p>
          </div>
          <span className="bc-chip border-slate-950/[0.08] bg-[#f4f7f2] text-slate-600"><MapPin size={10} /> {t('Boğaziçi kampüsleri', 'Boğaziçi campuses')}</span>
        </div>
        {data ? <CampusMap buildings={data.buildings} /> : <MapSkeleton />}
      </section>

      <section className="grid gap-4 lg:grid-cols-[.8fr_1.2fr]">
        <div className="rounded-[28px] border border-slate-900/[0.07] bg-[#f5f7f3] p-5 sm:p-6">
          <div className="bc-eyebrow">{t('Neden bu problem?', 'Why this problem?')}</div>
          <h2 className="mt-2 text-[28px] font-black leading-[1.02] tracking-[-0.052em] text-slate-950">
            {t('Çünkü etkiyi “AI söyledi” diye değil, ölçülmüş baz çizgisi ve kontrollü pilotla savunabiliriz.', 'Because impact can be defended with a measured baseline and controlled pilot, not with “AI said so”.')}
          </h2>
          <p className="mt-4 text-[10px] leading-5 text-slate-500">
            {t(
              'Boğaziçi 2024’te 50.993 kg, 2025’te 48.251 kg yemek atığı raporladı. BOUNCAMPUS eksik halkayı hedefliyor: bir sonraki servis için üretimi planlamak, insan kararını kaydetmek ve sonucu kg / 100 servis edilen öğün ile ölçmek.',
              'Boğaziçi reported 50,993 kg of food waste in 2024 and 48,251 kg in 2025. BOUNCAMPUS targets the missing loop: plan production for the next service, retain the human decision and measure the result in kg / 100 served meals.',
            )}
          </p>
          <Link href="/food-waste" className="mt-5 inline-flex items-center gap-1.5 text-[10px] font-black text-[#173f67]">
            {t('Karar motoru + pilot sözleşmesi', 'Decision engine + pilot contract')} <ArrowRight size={10} />
          </Link>
        </div>

        <div className="rounded-[28px] bg-[#07131f] p-5 text-white shadow-[0_18px_55px_rgba(7,19,31,.12)] sm:p-6">
          <div className="flex items-center justify-between gap-3">
            <div className="text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]">{t('Tek operasyon döngüsü', 'One operating loop')}</div>
            <ShieldCheck size={16} className="text-white/30" />
          </div>
          <div className="mt-6 grid gap-2 sm:grid-cols-5">
            {[
              ['01', t('TAHMİN', 'FORECAST'), t('Talep bandı', 'Demand band')],
              ['02', t('NİTELE', 'QUALIFY'), t('Hazır / incele / beklet', 'Ready / review / withhold')],
              ['03', t('ONAY', 'APPROVE'), t('Mutfak sorumlusu', 'Kitchen operator')],
              ['04', t('ÖLÇ', 'MEASURE'), t('100 öğüne normalize et', 'Normalize per 100 meals')],
              ['05', t('ÖĞREN', 'LEARN'), t('Modeli kalibre et', 'Calibrate model')],
            ].map(([step, title, detail], index) => (
              <div key={step} className="rounded-2xl border border-white/10 bg-white/[0.045] p-4">
                <div className="flex items-center justify-between"><span className="font-mono text-[8px] font-black text-[#b8e467]">{step}</span>{index === 4 ? <CheckCircle2 size={10} className="text-[#b8e467]" /> : <span className="text-white/18">→</span>}</div>
                <div className="mt-5 text-[9px] font-black tracking-[0.06em]">{title}</div>
                <div className="mt-1 text-[8px] leading-4 text-white/40">{detail}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <SignalCard icon={Database} label={t('Resmi problem', 'Measured problem')} value="48.251 kg" detail={t('2025 yemek atığı', '2025 food waste')} provenance="OFFICIAL_PUBLIC" />
        <SignalCard icon={BookOpen} label={t('Talep bağlamı', 'Demand context')} value={courses ? courses.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail={t('program kaydı', 'schedule records')} provenance="OFFICIAL_SNAPSHOT" />
        <SignalCard icon={CloudSun} label={t('Dış koşul', 'Outdoor condition')} value={weather == null ? '—' : `${weather}°C`} detail={t('hava sinyali', 'weather signal')} provenance="EXTERNAL_LIVE" />
        <SignalCard icon={BarChart3} label={t('Servis talep modeli', 'Service demand model')} value={foodModel ? foodModel.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US') : '—'} detail={t('öğün planlama tahmini', 'meal-planning estimate')} provenance="MODEL_ESTIMATE" />
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <ExpansionCard icon={Zap} title={t('Enerji kararları', 'Energy decisions')} body={t('Bina enerji ve senaryo yetenekleri ikinci dikey olarak korunuyor.', 'Building-energy and scenario capabilities remain available as the second vertical.')} href="/scenarios" />
        <ExpansionCard icon={BusFront} title={t('Akıllı hareketlilik', 'Smart mobility')} body={t('Resmi mekik rotaları ve iklim senaryoları platform genişlemesi olarak korunuyor.', 'Source-backed shuttle routes and climate scenarios remain available as platform expansion.')} href="/mobility" />
        <ExpansionCard icon={ShieldCheck} title={t('Kanıt katmanı', 'Evidence layer')} body={t('Her veri resmi, dış canlı, snapshot veya model tahmini olarak işaretleniyor.', 'Every input is labeled as official, external live, snapshot or model estimate.')} href="/data" />
      </section>
    </div>
  );
}

function MapSkeleton() {
  return (
    <div className="relative h-[560px] overflow-hidden rounded-[24px] bg-[#07131f]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(184,228,103,.12),transparent_24rem),linear-gradient(135deg,rgba(255,255,255,.03),transparent)]" />
      <div className="absolute left-5 top-5 h-10 w-48 animate-pulse rounded-xl bg-white/[0.06]" />
      <div className="absolute bottom-5 left-5 h-16 w-72 animate-pulse rounded-2xl bg-white/[0.06]" />
      <div className="absolute inset-0 grid place-items-center text-[10px] font-black uppercase tracking-[0.14em] text-white/28">Loading campus context</div>
    </div>
  );
}

function HeroStat({ label, value, suffix, muted }: { label: string; value: string; suffix?: string; muted?: string }) {
  return (
    <div className="min-w-0 rounded-2xl border border-white/[0.08] bg-white/[0.035] p-3">
      <div className="text-[7px] font-black uppercase tracking-[0.11em] text-white/34 sm:text-[8px]">{label}</div>
      <div className="mt-2 flex items-baseline gap-1.5"><span className="font-mono text-[21px] font-black tracking-[-0.055em] text-white sm:text-[24px]">{value}</span>{suffix ? <span className="text-[8px] font-black uppercase text-[#b8e467]">{suffix}</span> : null}</div>
      {muted ? <div className="mt-1 text-[7px] font-bold uppercase tracking-[0.08em] text-white/26">{muted}</div> : null}
    </div>
  );
}

function LiveSignal({ icon: Icon, label, value, detail, emphasis = false }: { icon: typeof Database; label: string; value: string; detail: string; emphasis?: boolean }) {
  return (
    <div className={`rounded-2xl border p-4 ${emphasis ? 'border-[#b8e467]/20 bg-[#b8e467]/[0.07]' : 'border-white/10 bg-white/[0.035]'}`}>
      <div className="flex items-center justify-between gap-2"><span className="text-[8px] font-black uppercase tracking-[0.12em] text-white/38">{label}</span><Icon size={12} className={emphasis ? 'text-[#b8e467]' : 'text-white/28'} /></div>
      <div className="mt-5 font-mono text-[29px] font-black tracking-[-0.06em] text-white">{value}</div>
      <div className={`mt-1 text-[8px] font-black uppercase tracking-[0.1em] ${emphasis ? 'text-[#dff6ae]' : 'text-white/30'}`}>{detail}</div>
    </div>
  );
}

function SignalCard({ icon: Icon, label, value, detail, provenance }: { icon: typeof Database; label: string; value: string; detail: string; provenance: string }) {
  return (
    <div className="rounded-[24px] border border-slate-900/[0.07] bg-white p-5 shadow-[0_12px_34px_rgba(15,23,42,.04)]">
      <div className="flex items-start justify-between gap-3"><div className="grid h-9 w-9 place-items-center rounded-xl bg-[#edf2e7] text-[#173f67]"><Icon size={15} /></div><span className="rounded-full bg-slate-50 px-2 py-1 font-mono text-[7px] font-black text-slate-400">{provenance}</span></div>
      <div className="mt-5 text-[8px] font-black uppercase tracking-[0.13em] text-slate-400">{label}</div>
      <div className="mt-1 text-[26px] font-black tracking-[-0.055em] text-slate-950">{value}</div>
      <div className="mt-1 text-[9px] text-slate-500">{detail}</div>
    </div>
  );
}

function ExpansionCard({ icon: Icon, title, body, href }: { icon: typeof Zap; title: string; body: string; href: string }) {
  return (
    <Link href={href} className="group rounded-[24px] border border-slate-900/[0.07] bg-[#f6f8f5] p-5 transition hover:-translate-y-0.5 hover:border-slate-900/12 hover:bg-white hover:shadow-[0_18px_45px_rgba(15,23,42,.06)]">
      <div className="flex items-center justify-between"><div className="grid h-9 w-9 place-items-center rounded-xl bg-white text-[#173f67] shadow-sm"><Icon size={15} /></div><ArrowRight size={13} className="text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-slate-600" /></div>
      <h3 className="mt-5 text-[18px] font-black tracking-[-0.035em] text-slate-950">{title}</h3>
      <p className="mt-2 text-[10px] leading-5 text-slate-500">{body}</p>
    </Link>
  );
}
