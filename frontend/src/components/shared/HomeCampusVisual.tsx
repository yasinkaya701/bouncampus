'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  ArrowRight,
  Building2,
  CheckCircle2,
  CircleGauge,
  CloudSun,
  Database,
  MapPin,
  Radar,
  ShieldCheck,
  Sparkles,
  Waves,
} from 'lucide-react';
import { useLocale } from '@/lib/i18n';

const productSignals = [
  { icon: Database, tr: 'Kaynak izi', en: 'Source trace', trValue: 'Görünür', enValue: 'Visible' },
  { icon: CircleGauge, tr: 'Karar modu', en: 'Decision mode', trValue: 'Model', enValue: 'Model' },
  { icon: ShieldCheck, tr: 'Güvenlik', en: 'Safety gate', trValue: 'İnsan', enValue: 'Human' },
  { icon: Waves, tr: 'Pilot döngüsü', en: 'Pilot loop', trValue: 'Ölç → Öğren', enValue: 'Measure → Learn' },
];

const operationRail = [
  { tr: 'Algıla', en: 'Sense' },
  { tr: 'Karar', en: 'Decide' },
  { tr: 'Stres testi', en: 'Stress-test' },
  { tr: 'Onay', en: 'Approve' },
  { tr: 'Pilot', en: 'Pilot' },
  { tr: 'Öğren', en: 'Learn' },
];

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { locale, t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      aria-label={t('BOUNCAMPUS iklim operasyonları ürün vitrini', 'BOUNCAMPUS climate operations product showcase')}
      className="bc-hero-shell bc-panel-dark bc-grid-bg bc-scan-line relative mb-8 overflow-hidden rounded-[34px] text-white"
    >
      <div aria-hidden="true" className="bc-hero-noise absolute inset-0 opacity-[0.16]" />
      <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_12%_18%,rgba(184,228,103,.13),transparent_25rem),radial-gradient(circle_at_85%_14%,rgba(83,188,218,.17),transparent_31rem),linear-gradient(115deg,rgba(255,255,255,.015),transparent_38%)]" />
      <div aria-hidden="true" className="absolute -left-20 top-20 h-64 w-64 rounded-full border border-white/[0.055]" />
      <div aria-hidden="true" className="absolute -left-2 top-40 h-36 w-36 rounded-full border border-[#b8e467]/10" />

      <div className="relative z-10 grid min-h-[720px] lg:grid-cols-[minmax(0,.84fr)_minmax(560px,1.16fr)]">
        <div className="relative flex flex-col justify-between overflow-hidden p-6 sm:p-8 lg:p-10 xl:p-12">
          <div aria-hidden="true" className="bc-hero-copy-glow pointer-events-none absolute -left-28 top-36 h-[420px] w-[420px] rounded-full" />

          <div className="relative flex flex-wrap items-center justify-between gap-3 lg:justify-start">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.07] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-white/78 backdrop-blur-xl">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" />
              {t('KREATE for Climate · İstanbul 2026', 'KREATE for Climate · Istanbul 2026')}
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/10 px-3 py-1.5 text-[9px] font-bold text-white/55 backdrop-blur-xl lg:hidden">
              <ShieldCheck size={11} /> {t('Kanıt sınırı açık', 'Evidence boundary on')}
            </div>
          </div>

          <div className="relative py-9 lg:py-12 xl:py-14">
            <div className="mb-4 inline-flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Sparkles size={13} /> {t('Kampüs iklim operasyon sistemi', 'Campus climate operations system')}
            </div>
            <h1 className="max-w-[760px] text-[46px] font-black leading-[0.94] tracking-[-0.07em] text-white sm:text-[62px] xl:text-[76px]">
              {t('Kampüsün görünmeyen israfını karara çevir.', 'Turn invisible campus waste into a decision.')}
            </h1>
            <p className="mt-5 max-w-2xl text-[13px] leading-6 text-white/62 sm:text-[14px] sm:leading-7">
              {t(
                'BOUNCAMPUS; ders programı, hava durumu ve bina bağlamını tek bir operasyon yüzeyinde birleştirir. Düşük kullanım penceresini bulur, senaryoyu stres testine sokar ve insan onaylı ölçülebilir pilot önerisine dönüştürür.',
                'BOUNCAMPUS combines schedules, weather and building context on one operational surface. It finds low-use windows, stress-tests scenarios and turns them into human-approved, measurable pilot proposals.',
              )}
            </p>

            <div className="mt-7 flex flex-wrap gap-2.5">
              <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[11px] font-black text-[#071c33] shadow-[0_14px_34px_rgba(184,228,103,.16)] transition hover:-translate-y-0.5 hover:bg-[#c7ed80]">
                {t('90 saniyelik jüri akışı', '90-second jury flow')} <ArrowRight size={13} />
              </Link>
              <Link href="/scenarios" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/14 bg-white/[0.07] px-4 py-3 text-[11px] font-black text-white backdrop-blur-xl transition hover:bg-white/[0.12]">
                <Radar size={13} /> {t('Senaryo çalıştır', 'Run a scenario')}
              </Link>
            </div>

            <div className="mt-8 rounded-2xl border border-white/[0.08] bg-black/10 p-3.5 backdrop-blur-sm">
              <div className="mb-3 flex items-center justify-between gap-3">
                <span className="text-[8px] font-black uppercase tracking-[0.16em] text-white/40">{t('Operasyon protokolü', 'Operations protocol')}</span>
                <span className="font-mono text-[8px] font-black text-[#b8e467]">SENSE → LEARN</span>
              </div>
              <div className="relative grid grid-cols-6 gap-1">
                <div aria-hidden="true" className="absolute left-[4%] right-[4%] top-[7px] h-px bg-gradient-to-r from-[#b8e467]/25 via-[#b8e467]/80 to-[#dff2f5]/20" />
                {operationRail.map((step, index) => (
                  <div key={step.en} className="relative min-w-0 text-center">
                    <span className={`mx-auto block h-3.5 w-3.5 rounded-full border ${index < 4 ? 'border-[#b8e467]/55 bg-[#b8e467]/20' : 'border-white/20 bg-[#071c33]'}`}>
                      <span className={`mx-auto mt-[4px] block h-1 w-1 rounded-full ${index < 4 ? 'bg-[#b8e467]' : 'bg-white/35'}`} />
                    </span>
                    <span className="mt-2 block truncate text-[7px] font-black uppercase tracking-[0.07em] text-white/46 sm:text-[8px]">
                      {locale === 'tr' ? step.tr : step.en}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="relative grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4">
            {productSignals.map(signal => {
              const Icon = signal.icon;
              return (
                <div key={signal.en} className="bc-asset-card rounded-2xl border border-white/10 bg-white/[0.055] p-3 backdrop-blur-xl">
                  <div className="flex items-center gap-2 text-white/45">
                    <Icon size={12} />
                    <span className="text-[8px] font-black uppercase tracking-[0.13em]">{locale === 'tr' ? signal.tr : signal.en}</span>
                  </div>
                  <div className="mt-2 text-[10px] font-black text-white/84">{locale === 'tr' ? signal.trValue : signal.enValue}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bc-hero-stage relative min-h-[560px] overflow-hidden border-t border-white/[0.07] bg-[#071826] lg:min-h-0 lg:border-l lg:border-t-0">
          <Image
            src="/assets/campus-command-deck.svg"
            alt={t('Boğaziçi kampüs bağlamını ve karar düğümlerini gösteren BOUNCAMPUS dijital ikiz illüstrasyonu', 'BOUNCAMPUS digital twin illustration showing Bosphorus campus context and decision nodes')}
            fill
            priority
            sizes="(min-width: 1024px) 58vw, 100vw"
            className="object-cover object-center opacity-[0.92] saturate-[1.05]"
          />

          <div aria-hidden="true" className="absolute inset-0 bg-[linear-gradient(90deg,rgba(7,24,38,.5),transparent_32%),linear-gradient(0deg,rgba(7,24,38,.74),transparent_45%),radial-gradient(circle_at_78%_24%,rgba(184,228,103,.08),transparent_22rem)]" />

          <div aria-hidden="true" className="bc-orbit-drift absolute -right-[9%] top-[5%] h-[62%] w-[62%] opacity-75 sm:h-[68%] sm:w-[68%]">
            <Image src="/assets/campus-signal-orbit.svg" alt="" fill sizes="36vw" className="object-contain" />
          </div>

          <div className="absolute left-4 top-4 rounded-2xl border border-white/12 bg-[#061727]/78 p-3.5 shadow-2xl backdrop-blur-xl sm:left-6 sm:top-6">
            <div className="flex items-center gap-2 text-[8px] font-black uppercase tracking-[0.14em] text-[#b8e467]">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" /> {t('Operasyon görünümü', 'Operations view')}
            </div>
            <div className="mt-2 text-[11px] font-black text-white">{t('South Campus · Bebek', 'South Campus · Bebek')}</div>
            <div className="mt-1 text-[8px] font-semibold text-white/45">{t('Görsel bağlam + kaynak izi + karar düğümü', 'Visual context + source trace + decision node')}</div>
          </div>

          <div className="absolute right-4 top-[31%] hidden w-[188px] space-y-2 sm:block lg:right-6 xl:w-[210px]">
            <div className="bc-hero-float-card rounded-2xl border border-white/10 bg-[#061727]/76 p-3.5 shadow-2xl backdrop-blur-xl">
              <div className="flex items-center gap-2 text-[#b8e467]"><Database size={12} /><span className="text-[8px] font-black uppercase tracking-[0.13em]">{t('Kaynak izi', 'Source trace')}</span></div>
              <div className="mt-2 text-[10px] font-black text-white">{t('Her kararın arkasında görünür kanıt', 'Visible evidence behind each decision')}</div>
            </div>
            <div className="bc-hero-float-card rounded-2xl border border-white/10 bg-[#061727]/76 p-3.5 shadow-2xl backdrop-blur-xl [animation-delay:1.2s]">
              <div className="flex items-center gap-2 text-[#b8e467]"><ShieldCheck size={12} /><span className="text-[8px] font-black uppercase tracking-[0.13em]">{t('İnsan kapısı', 'Human gate')}</span></div>
              <div className="mt-2 text-[10px] font-black text-white">{t('Pilot öncesi zorunlu onay', 'Required approval before pilot')}</div>
            </div>
          </div>

          <div className="absolute left-4 top-[35%] hidden w-[176px] space-y-2 xl:block">
            <div className="bc-glass-metric rounded-2xl p-3.5">
              <div className="flex items-center gap-2 text-white/45"><CloudSun size={12} /><span className="text-[8px] font-black uppercase tracking-[0.13em]">{t('Hava bağlamı', 'Weather context')}</span></div>
              <div className="mt-2 text-[10px] font-black text-white/86">{t('HVAC kararına bağlanır', 'Connected to HVAC logic')}</div>
            </div>
            <div className="bc-glass-metric rounded-2xl p-3.5">
              <div className="flex items-center gap-2 text-white/45"><Building2 size={12} /><span className="text-[8px] font-black uppercase tracking-[0.13em]">{t('Bina bağlamı', 'Building context')}</span></div>
              <div className="mt-2 text-[10px] font-black text-white/86">{t('Program + geometri', 'Schedule + geometry')}</div>
            </div>
          </div>

          <div className="absolute inset-x-3 bottom-3 overflow-hidden rounded-[22px] border border-white/[0.09] bg-[#061727]/82 shadow-2xl backdrop-blur-xl sm:inset-x-5 sm:bottom-5">
            <div className="relative h-[126px] sm:h-[146px]">
              <Image
                src="/assets/campus-atlas-strip.svg"
                alt={t('Boğaziçi kampüs bağlamlarını tek operasyon katmanında temsil eden stilize atlas', 'Stylized atlas representing Boğaziçi campus contexts on one operations layer')}
                fill
                sizes="(min-width: 1024px) 55vw, 100vw"
                className="object-cover object-center opacity-[0.86]"
              />
              <div aria-hidden="true" className="absolute inset-0 bg-gradient-to-r from-[#061727]/32 via-transparent to-[#061727]/28" />
              <div className="absolute right-3 top-3 inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-black/15 px-2.5 py-1 text-[7px] font-black uppercase tracking-[0.11em] text-white/55 backdrop-blur">
                <MapPin size={9} /> {t('Kampüs bağlam ağı', 'Campus context mesh')}
              </div>
            </div>
          </div>

          <div className="absolute bottom-[166px] left-5 right-5 hidden grid-cols-3 gap-2 sm:grid lg:bottom-[186px] lg:left-6 lg:right-6">
            {[
              [t('01 · ALGILA', '01 · SENSE'), t('Program + hava + bina', 'Schedule + weather + building')],
              [t('02 · KARAR VER', '02 · DECIDE'), t('Düşük kullanım penceresi', 'Low-use window')],
              [t('03 · PİLOTLA', '03 · PILOT'), t('Onayla → ölç → öğren', 'Approve → measure → learn')],
            ].map(([label, value], index) => (
              <div key={label} className={`bc-asset-card rounded-2xl border border-white/10 bg-[#061727]/74 p-3 shadow-xl backdrop-blur-xl ${index === 1 ? 'sm:-translate-y-2' : ''}`}>
                <div className="flex items-center justify-between gap-3">
                  <span className="text-[7px] font-black uppercase tracking-[0.14em] text-[#b8e467]">{label}</span>
                  <CheckCircle2 size={11} className="text-white/30" />
                </div>
                <div className="mt-1.5 text-[9px] font-bold leading-4 text-white/70">{value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
