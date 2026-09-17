'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Activity,
  ArrowRight,
  CheckCircle2,
  Database,
  Gauge,
  Leaf,
  ShieldCheck,
  Sparkles,
  TrendingDown,
  Utensils,
} from 'lucide-react';
import { useLocale } from '@/lib/i18n';

const steps = [
  { tr: 'Baz çizgisi', en: 'Baseline' },
  { tr: 'Talep bandı', en: 'Demand band' },
  { tr: 'İnsan onayı', en: 'Human approval' },
  { tr: 'Pilot', en: 'Pilot' },
  { tr: 'Öğren', en: 'Learn' },
];

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { locale, t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      aria-label={t('BOUNCAMPUS iklim operasyon sistemi', 'BOUNCAMPUS climate operations system')}
      className="bc-hero-shell bc-panel-dark relative mb-8 overflow-hidden rounded-[36px] text-white"
    >
      <div aria-hidden="true" className="bc-hero-noise absolute inset-0 z-[1] opacity-[0.16]" />
      <div aria-hidden="true" className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_9%_10%,rgba(184,228,103,.18),transparent_24rem),radial-gradient(circle_at_82%_8%,rgba(71,170,204,.16),transparent_29rem)]" />
      <div aria-hidden="true" className="absolute left-[28%] top-[-26%] h-[520px] w-[520px] rounded-full bg-[#b8e467]/[0.035] blur-3xl" />

      <div className="relative z-[2] grid min-h-[560px] lg:grid-cols-[minmax(0,.82fr)_minmax(620px,1.18fr)]">
        <div className="relative flex flex-col justify-between p-6 sm:p-8 lg:p-10 xl:p-12">
          <div aria-hidden="true" className="bc-hero-copy-glow absolute -left-24 top-8 h-72 w-72 rounded-full" />

          <div className="relative">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.065] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-white/78 backdrop-blur-xl">
                <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" />
                {t('KREATE for Climate · canlı ürün', 'KREATE for Climate · live product')}
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full border border-[#b8e467]/20 bg-[#b8e467]/10 px-3 py-1.5 text-[8px] font-black uppercase tracking-[0.13em] text-[#d9f5a6]">
                <ShieldCheck size={10} /> {t('İnsan onaylı karar', 'Human-gated decision')}
              </span>
            </div>

            <div className="mt-8 flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Leaf size={12} /> {t('Kampüs iklim operasyon sistemi', 'Campus climate operations system')}
            </div>

            <h1 className="mt-4 max-w-[760px] text-[42px] font-black leading-[0.94] tracking-[-0.068em] sm:text-[56px] xl:text-[68px]">
              {t(
                'Atığı ölçmek yetmez. Bir sonraki kilogramı hiç üretmemek gerekir.',
                'Measuring waste is not enough. The next kilogram should never be produced.',
              )}
            </h1>

            <p className="mt-6 max-w-2xl text-[12px] leading-6 text-white/60 sm:text-[13px]">
              {t(
                'BOUNCAMPUS resmi kampüs verisini, talep sinyallerini ve belirsizliği tek bir operasyon akışında birleştirir; mutfak ekibine sadece “ne oldu?” değil, “bir sonraki serviste ne yapmalıyız?” cevabını verir.',
                'BOUNCAMPUS combines official campus data, demand signals and uncertainty in one operating loop; it answers not only “what happened?” but “what should we do before the next service?”.',
              )}
            </p>

            <div className="mt-8 flex flex-wrap gap-2.5">
              <Link href="/food-waste" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[10px] font-black text-[#071c33] shadow-[0_18px_45px_rgba(184,228,103,.18)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_22px_55px_rgba(184,228,103,.24)]">
                <Utensils size={13} /> {t('Karar motorunu aç', 'Open decision engine')} <ArrowRight size={11} />
              </Link>
              <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/13 bg-white/[0.065] px-4 py-3 text-[10px] font-black text-white backdrop-blur-xl transition hover:bg-white/[0.11]">
                <Sparkles size={12} /> {t('90 sn jüri modu', '90 sec jury mode')}
              </Link>
            </div>
          </div>

          <div className="relative mt-10 grid grid-cols-3 gap-2.5 border-t border-white/[0.08] pt-5">
            <TrustMetric icon={Database} label={t('Resmi baz çizgisi', 'Official baseline')} value="48.251 kg" />
            <TrustMetric icon={TrendingDown} label={t('Pilot hedefi', 'Pilot target')} value="≥10%" muted={t('sonuç değil', 'not a result')} />
            <TrustMetric icon={ShieldCheck} label={t('Karar kapısı', 'Decision gate')} value={t('İnsan', 'Human')} />
          </div>
        </div>

        <div className="bc-hero-stage bc-scan-line relative min-h-[520px] overflow-hidden border-t border-white/[0.08] bg-[#061625] lg:border-l lg:border-t-0">
          <Image
            src="/assets/campus-command-deck.svg"
            alt={t('Boğaziçi kampüsünde BOUNCAMPUS karar düğümleri', 'BOUNCAMPUS decision nodes across Boğaziçi campus')}
            fill
            priority
            sizes="(min-width: 1024px) 58vw, 100vw"
            className="object-cover object-center opacity-[0.72] saturate-[1.12] contrast-[1.03]"
          />
          <div aria-hidden="true" className="absolute inset-0 z-[2] bg-[linear-gradient(90deg,rgba(6,22,37,.78),rgba(6,22,37,.12)_42%,rgba(6,22,37,.48)),linear-gradient(0deg,rgba(6,22,37,.92),transparent_62%)]" />
          <div aria-hidden="true" className="bc-orbit-drift absolute -right-[8%] -top-[12%] z-[3] h-[76%] w-[67%] opacity-60">
            <Image src="/assets/campus-signal-orbit.svg" alt="" fill sizes="42vw" className="object-contain" />
          </div>
          <div aria-hidden="true" className="absolute inset-x-[10%] top-[15%] z-[3] h-px bg-gradient-to-r from-transparent via-[#b8e467]/30 to-transparent" />

          <div className="absolute left-4 right-4 top-4 z-[5] flex items-center justify-between gap-3 sm:left-6 sm:right-6 sm:top-6">
            <div className="rounded-full border border-white/10 bg-[#061727]/78 px-3 py-2 text-[8px] font-black uppercase tracking-[0.14em] text-white/48 backdrop-blur-xl">
              {t('Campus Climate Ops · Decision Window', 'Campus Climate Ops · Decision Window')}
            </div>
            <div className="hidden items-center gap-2 rounded-full border border-[#b8e467]/15 bg-[#b8e467]/[0.08] px-3 py-2 text-[8px] font-black text-[#d9f5a6] backdrop-blur-xl sm:flex">
              <Activity size={10} /> {t('Sinyaller senkronize', 'Signals synchronized')}
            </div>
          </div>

          <div className="bc-hero-float-card absolute left-[6%] top-[19%] z-[5] w-[54%] min-w-[270px] rounded-[24px] border border-white/10 bg-[#061727]/84 p-4 backdrop-blur-2xl sm:left-[7%] sm:top-[21%] sm:p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-[8px] font-black uppercase tracking-[0.15em] text-white/38">{t('Demo karar kartı · model tahmini', 'Demo decision card · model estimate')}</div>
                <div className="mt-2 text-[17px] font-black tracking-[-0.035em] text-white sm:text-[20px]">{t('Yarın öğle servisi', 'Tomorrow lunch service')}</div>
              </div>
              <div className="grid h-9 w-9 place-items-center rounded-xl border border-[#b8e467]/20 bg-[#b8e467]/10 text-[#b8e467]"><Gauge size={15} /></div>
            </div>

            <div className="mt-5 grid grid-cols-2 gap-2.5">
              <DecisionMetric label={t('Talep bandı', 'Demand band')} value="2.730–2.980" suffix={t('öğün', 'meals')} />
              <DecisionMetric label={t('Önerilen üretim', 'Recommended production')} value="2.820" suffix={t('öğün', 'meals')} accent />
            </div>

            <div className="mt-3 flex items-center justify-between rounded-xl border border-white/[0.07] bg-white/[0.035] px-3 py-2.5">
              <div className="flex items-center gap-2 text-[8px] font-black text-white/50"><ShieldCheck size={10} className="text-[#b8e467]" /> {t('Operatör onayı gerekli', 'Operator approval required')}</div>
              <span className="rounded-full bg-amber-300/10 px-2 py-1 text-[7px] font-black uppercase tracking-[0.1em] text-amber-200">REVIEW</span>
            </div>
          </div>

          <div className="bc-float absolute right-[5%] top-[25%] z-[6] hidden w-[31%] min-w-[180px] rounded-[20px] border border-white/10 bg-[#071a2b]/80 p-4 shadow-2xl backdrop-blur-2xl sm:block">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[7px] font-black uppercase tracking-[0.14em] text-white/40">{t('Problem baz çizgisi', 'Problem baseline')}</span>
              <Database size={11} className="text-[#b8e467]" />
            </div>
            <div className="mt-3 font-mono text-[28px] font-black tracking-[-0.06em]">48.251</div>
            <div className="mt-1 text-[8px] font-black uppercase tracking-[0.12em] text-white/42">kg · 2025 · OFFICIAL_PUBLIC</div>
          </div>

          <div className="absolute right-[7%] top-[56%] z-[6] hidden rounded-[18px] border border-white/10 bg-[#071a2b]/76 px-4 py-3 shadow-2xl backdrop-blur-2xl md:block">
            <div className="flex items-center gap-2 text-[8px] font-black uppercase tracking-[0.11em] text-white/50"><TrendingDown size={11} className="text-[#b8e467]" /> {t('Pilot başarı kapısı', 'Pilot success gate')}</div>
            <div className="mt-2 flex items-baseline gap-2"><span className="font-mono text-[24px] font-black text-[#d9f5a6]">≥10%</span><span className="text-[7px] font-bold text-white/34">{t('azalma hedefi · sonuç değil', 'reduction target · not result')}</span></div>
          </div>

          <div className="absolute inset-x-4 bottom-4 z-[7] rounded-[24px] border border-white/10 bg-[#051522]/88 p-4 shadow-2xl backdrop-blur-2xl sm:inset-x-6 sm:bottom-6 sm:p-5">
            <div className="mb-4 flex items-center justify-between gap-3">
              <span className="text-[8px] font-black uppercase tracking-[0.14em] text-white/42">{t('Bir sonraki servise kadar kapalı çevrim', 'Closed loop before the next service')}</span>
              <span className="font-mono text-[8px] font-black text-[#b8e467]">SENSE → DECIDE → PILOT → LEARN</span>
            </div>
            <div className="grid grid-cols-5 gap-1.5 sm:gap-2">
              {steps.map((step, index) => (
                <div key={step.en} className="group rounded-xl border border-white/[0.075] bg-white/[0.04] p-2.5 text-center transition hover:border-[#b8e467]/20 hover:bg-[#b8e467]/[0.06]">
                  <div className="mx-auto grid h-6 w-6 place-items-center rounded-full border border-[#b8e467]/25 bg-[#b8e467]/[0.08] text-[#b8e467]">
                    {index === steps.length - 1 ? <CheckCircle2 size={10} /> : <span className="font-mono text-[7px] font-black">0{index + 1}</span>}
                  </div>
                  <div className="mt-2 truncate text-[7px] font-black uppercase tracking-[0.045em] text-white/58 sm:text-[8px]">
                    {locale === 'tr' ? step.tr : step.en}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function TrustMetric({ icon: Icon, label, value, muted }: { icon: typeof Database; label: string; value: string; muted?: string }) {
  return (
    <div className="min-w-0">
      <div className="flex items-center gap-1.5 text-white/38"><Icon size={10} /><span className="truncate text-[7px] font-black uppercase tracking-[0.1em] sm:text-[8px]">{label}</span></div>
      <div className="mt-2 truncate font-mono text-[17px] font-black tracking-[-0.04em] text-white sm:text-[20px]">{value}</div>
      {muted ? <div className="mt-0.5 truncate text-[7px] font-bold uppercase tracking-[0.08em] text-white/28">{muted}</div> : null}
    </div>
  );
}

function DecisionMetric({ label, value, suffix, accent = false }: { label: string; value: string; suffix: string; accent?: boolean }) {
  return (
    <div className={`rounded-xl border p-3 ${accent ? 'border-[#b8e467]/20 bg-[#b8e467]/[0.07]' : 'border-white/[0.07] bg-white/[0.035]'}`}>
      <div className="text-[7px] font-black uppercase tracking-[0.1em] text-white/34">{label}</div>
      <div className={`mt-2 font-mono text-[18px] font-black tracking-[-0.05em] ${accent ? 'text-[#d9f5a6]' : 'text-white'}`}>{value}</div>
      <div className="mt-0.5 text-[7px] font-bold text-white/32">{suffix}</div>
    </div>
  );
}
