'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  ArrowRight,
  CheckCircle2,
  CircleGauge,
  Database,
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

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { locale, t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      aria-label={t('BOUNCAMPUS iklim operasyonları ürün vitrini', 'BOUNCAMPUS climate operations product showcase')}
      className="bc-panel-dark bc-grid-bg bc-scan-line relative mb-8 overflow-hidden rounded-[30px] text-white shadow-[0_38px_100px_rgba(7,28,51,.24)]"
    >
      <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_15%_20%,rgba(184,228,103,.12),transparent_28rem),radial-gradient(circle_at_84%_14%,rgba(83,188,218,.15),transparent_30rem)]" />
      <div aria-hidden="true" className="absolute -left-24 top-16 h-64 w-64 rounded-full border border-white/[0.06]" />
      <div aria-hidden="true" className="absolute -left-10 top-32 h-40 w-40 rounded-full border border-[#b8e467]/10" />

      <div className="relative z-10 grid min-h-[690px] lg:grid-cols-[minmax(0,.86fr)_minmax(520px,1.14fr)]">
        <div className="flex flex-col justify-between p-6 sm:p-8 lg:p-10 xl:p-12">
          <div className="flex flex-wrap items-center justify-between gap-3 lg:justify-start">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.07] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-white/78 backdrop-blur-xl">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" />
              {t('KREATE for Climate · İstanbul 2026', 'KREATE for Climate · Istanbul 2026')}
            </div>
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/10 px-3 py-1.5 text-[9px] font-bold text-white/55 backdrop-blur-xl lg:hidden">
              <ShieldCheck size={11} /> {t('Kanıt sınırı açık', 'Evidence boundary on')}
            </div>
          </div>

          <div className="py-10 lg:py-14">
            <div className="mb-4 inline-flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Sparkles size={13} /> {t('Kampüs iklim operasyon sistemi', 'Campus climate operations system')}
            </div>
            <h1 className="max-w-[760px] text-[44px] font-black leading-[0.96] tracking-[-0.068em] text-white sm:text-[60px] xl:text-[72px]">
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
          </div>

          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4">
            {productSignals.map(signal => {
              const Icon = signal.icon;
              return (
                <div key={signal.en} className="rounded-2xl border border-white/10 bg-white/[0.055] p-3 backdrop-blur-xl">
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

        <div className="relative min-h-[500px] overflow-hidden border-t border-white/[0.07] bg-[#071826] lg:min-h-0 lg:border-l lg:border-t-0">
          <Image
            src="/assets/campus-command-deck.svg"
            alt={t('Boğaziçi kampüs bağlamını ve karar düğümlerini gösteren BOUNCAMPUS dijital ikiz illüstrasyonu', 'BOUNCAMPUS digital twin illustration showing Bosphorus campus context and decision nodes')}
            fill
            priority
            sizes="(min-width: 1024px) 56vw, 100vw"
            className="object-cover object-center opacity-[0.96]"
          />
          <div aria-hidden="true" className="absolute inset-0 bg-[linear-gradient(90deg,rgba(7,24,38,.35),transparent_34%),linear-gradient(0deg,rgba(7,24,38,.42),transparent_34%)]" />

          <div className="absolute left-4 top-4 rounded-2xl border border-white/12 bg-[#061727]/78 p-3.5 shadow-2xl backdrop-blur-xl sm:left-6 sm:top-6">
            <div className="flex items-center gap-2 text-[8px] font-black uppercase tracking-[0.14em] text-[#b8e467]">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" /> {t('Operasyon görünümü', 'Operations view')}
            </div>
            <div className="mt-2 text-[11px] font-black text-white">{t('South Campus · Bebek', 'South Campus · Bebek')}</div>
            <div className="mt-1 text-[8px] font-semibold text-white/45">{t('Görsel bağlam + kaynak izi + karar düğümü', 'Visual context + source trace + decision node')}</div>
          </div>

          <div className="absolute bottom-4 left-4 right-4 grid gap-2 sm:bottom-6 sm:left-6 sm:right-6 sm:grid-cols-3">
            {[
              [t('01 · ALGILA', '01 · SENSE'), t('Program + hava + bina', 'Schedule + weather + building')],
              [t('02 · KARAR VER', '02 · DECIDE'), t('Düşük kullanım penceresi', 'Low-use window')],
              [t('03 · PİLOTLA', '03 · PILOT'), t('Onayla → ölç → öğren', 'Approve → measure → learn')],
            ].map(([label, value], index) => (
              <div key={label} className={`bc-asset-card rounded-2xl border border-white/10 bg-[#061727]/74 p-3.5 shadow-xl backdrop-blur-xl ${index === 1 ? 'sm:-translate-y-2' : ''}`}>
                <div className="flex items-center justify-between gap-3">
                  <span className="text-[8px] font-black uppercase tracking-[0.15em] text-[#b8e467]">{label}</span>
                  <CheckCircle2 size={12} className="text-white/30" />
                </div>
                <div className="mt-2 text-[10px] font-bold leading-5 text-white/76">{value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
