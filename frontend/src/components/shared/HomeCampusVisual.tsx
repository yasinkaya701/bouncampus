'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ArrowRight, CheckCircle2, Radar, ShieldCheck, Sparkles } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      aria-label={t('BOUNCAMPUS iklim operasyonları ürün vitrini', 'BOUNCAMPUS climate operations product showcase')}
      className="bc-panel-dark bc-grid-bg bc-scan-line relative mb-8 min-h-[500px] overflow-hidden rounded-[28px] text-white sm:min-h-[540px] lg:min-h-[580px]"
    >
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-cover bg-[58%_center] opacity-55 mix-blend-screen sm:bg-center"
        style={{ backgroundImage: "url('/assets/bouncampus-hero.svg')" }}
      />
      <div aria-hidden="true" className="absolute inset-0 bg-[linear-gradient(90deg,rgba(4,15,28,.96)_0%,rgba(4,15,28,.88)_40%,rgba(4,15,28,.48)_70%,rgba(4,15,28,.26)_100%)]" />
      <div aria-hidden="true" className="absolute -right-20 -top-28 h-96 w-96 rounded-full bg-[#b8e467]/10 blur-3xl" />
      <div aria-hidden="true" className="absolute bottom-0 left-[42%] h-72 w-72 rounded-full bg-cyan-300/10 blur-3xl" />

      <div className="relative z-10 flex min-h-[500px] flex-col justify-between p-6 sm:min-h-[540px] sm:p-8 lg:min-h-[580px] lg:p-10">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.07] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-white/75 backdrop-blur-xl">
            <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" />
            {t('KREATE for Climate · İstanbul 2026', 'KREATE for Climate · Istanbul 2026')}
          </div>
          <div className="hidden items-center gap-2 rounded-full border border-white/10 bg-black/10 px-3 py-1.5 text-[9px] font-bold text-white/60 backdrop-blur-xl sm:flex">
            <ShieldCheck size={11} /> {t('Kaynak sınırı görünür', 'Evidence boundary visible')}
          </div>
        </div>

        <div className="grid items-end gap-8 lg:grid-cols-[minmax(0,1fr)_360px]">
          <div className="max-w-4xl">
            <div className="mb-4 inline-flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Sparkles size={13} /> {t('Kampüs iklim operasyon sistemi', 'Campus climate operations system')}
            </div>
            <h1 className="max-w-4xl text-[44px] font-black leading-[0.98] tracking-[-0.065em] text-white sm:text-[62px] lg:text-[74px]">
              {t('Kampüs, enerji israfını gerçekleşmeden önce görebilse?', 'What if a campus could see energy waste before it happens?')}
            </h1>
            <p className="mt-5 max-w-2xl text-[13px] leading-6 text-white/62 sm:text-[14px] sm:leading-7">
              {t(
                'BOUNCAMPUS; ders programı, hava durumu ve bina bağlamından düşük kullanım pencerelerini çıkarır, müdahaleyi simüle eder ve ölçülebilir bir pilot kararına dönüştürür.',
                'BOUNCAMPUS turns schedules, weather and building context into low-use windows, stress-tests an intervention, and converts it into a measurable pilot decision.',
              )}
            </p>
            <div className="mt-6 flex flex-wrap gap-2.5">
              <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[11px] font-black text-[#071c33] shadow-[0_14px_34px_rgba(184,228,103,.15)] transition hover:-translate-y-0.5 hover:bg-[#c7ed80]">
                {t('90 saniyede ürünü gör', 'See the product in 90 seconds')} <ArrowRight size={13} />
              </Link>
              <Link href="/scenarios" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/14 bg-white/[0.07] px-4 py-3 text-[11px] font-black text-white backdrop-blur-xl transition hover:bg-white/[0.12]">
                <Radar size={13} /> {t('Senaryo çalıştır', 'Run a scenario')}
              </Link>
            </div>
          </div>

          <div className="grid gap-2.5 sm:grid-cols-3 lg:grid-cols-1">
            {[
              [t('01 · Algıla', '01 · Sense'), t('Program + hava + bina bağlamı', 'Schedule + weather + building context')],
              [t('02 · Karar ver', '02 · Decide'), t('Düşük kullanım penceresini seç', 'Select the low-use window')],
              [t('03 · Pilotla', '03 · Pilot'), t('İnsan onayı → ölç → öğren', 'Human approval → measure → learn')],
            ].map(([label, value], index) => (
              <div key={label} className={`bc-float rounded-2xl border border-white/10 bg-white/[0.075] p-4 backdrop-blur-xl ${index === 1 ? 'lg:ml-6' : ''}`} style={{ animationDelay: `${index * 0.7}s` }}>
                <div className="flex items-center justify-between gap-3">
                  <span className="text-[9px] font-black uppercase tracking-[0.16em] text-[#b8e467]">{label}</span>
                  <CheckCircle2 size={13} className="text-white/35" />
                </div>
                <div className="mt-2 text-[11px] font-bold leading-5 text-white/78">{value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
