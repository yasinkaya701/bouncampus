'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  ArrowRight,
  CheckCircle2,
  Database,
  Gauge,
  ShieldCheck,
  Sparkles,
  Utensils,
} from 'lucide-react';
import { useLocale } from '@/lib/i18n';

const steps = [
  { tr: 'Baz çizgisi', en: 'Baseline' },
  { tr: 'Talep bandı', en: 'Demand band' },
  { tr: 'İnsan onayı', en: 'Human approval' },
  { tr: 'Ölç', en: 'Measure' },
  { tr: 'Öğren', en: 'Learn' },
];

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { locale, t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      aria-label={t('BOUNCAMPUS yemek atığı karar sistemi görseli', 'BOUNCAMPUS food-waste decision system visual')}
      className="bc-panel-dark bc-grid-bg relative mb-8 overflow-hidden rounded-[34px] text-white"
    >
      <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_10%_20%,rgba(184,228,103,.14),transparent_28rem),radial-gradient(circle_at_88%_12%,rgba(83,188,218,.14),transparent_28rem)]" />
      <div className="relative grid min-h-[430px] lg:grid-cols-[minmax(0,.72fr)_minmax(520px,1.28fr)]">
        <div className="flex flex-col justify-between p-6 sm:p-8 lg:p-10">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.07] px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.16em] text-white/78">
              <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-[#b8e467]" />
              {t('KREATE for Climate · odak problem', 'KREATE for Climate · focus problem')}
            </div>
            <div className="mt-8 flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]">
              <Utensils size={12} /> {t('Kampüs yemek atığı', 'Campus food waste')}
            </div>
            <div className="mt-3 flex items-end gap-3">
              <div className="font-mono text-[48px] font-black leading-none tracking-[-0.07em] sm:text-[64px]">48.251</div>
              <div className="pb-1 text-[12px] font-black uppercase tracking-[0.12em] text-white/48">kg · 2025</div>
            </div>
            <p className="mt-4 max-w-xl text-[11px] leading-5 text-white/58">
              {t(
                'Resmi problem baz çizgisi. BOUNCAMPUS bu sayıyı “dashboard KPI” olarak bırakmaz; bir sonraki servis için üretim kararına ve ölçülebilir pilot sonucuna bağlar.',
                'An official problem baseline. BOUNCAMPUS does not leave this as a dashboard KPI; it connects it to the next service production decision and a measurable pilot outcome.',
              )}
            </p>
          </div>

          <div className="mt-7 flex flex-wrap gap-2">
            <Link href="/food-waste" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[10px] font-black text-[#071c33] transition hover:-translate-y-0.5">
              {t('Karar sistemini aç', 'Open decision system')} <ArrowRight size={11} />
            </Link>
            <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/13 bg-white/[0.06] px-4 py-3 text-[10px] font-black text-white transition hover:bg-white/[0.11]">
              <Sparkles size={11} /> {t('90 sn jüri modu', '90 sec jury mode')}
            </Link>
          </div>
        </div>

        <div className="relative min-h-[400px] overflow-hidden border-t border-white/[0.08] bg-[#071826] lg:border-l lg:border-t-0">
          <Image
            src="/assets/campus-command-deck.svg"
            alt={t('Boğaziçi kampüsünü karar düğümleriyle gösteren BOUNCAMPUS görselleştirmesi', 'BOUNCAMPUS visualization showing Boğaziçi campus with decision nodes')}
            fill
            priority
            sizes="(min-width: 1024px) 62vw, 100vw"
            className="object-cover object-center opacity-[0.7] saturate-[1.05]"
          />
          <div aria-hidden="true" className="absolute inset-0 bg-[linear-gradient(90deg,rgba(7,24,38,.72),rgba(7,24,38,.18)_46%,rgba(7,24,38,.48)),linear-gradient(0deg,rgba(7,24,38,.86),transparent_62%)]" />
          <div aria-hidden="true" className="absolute -right-[5%] -top-[10%] h-[80%] w-[65%] opacity-55">
            <Image src="/assets/campus-signal-orbit.svg" alt="" fill sizes="38vw" className="object-contain" />
          </div>

          <div className="absolute left-4 top-4 grid gap-2 sm:left-6 sm:top-6 sm:grid-cols-3">
            <VisualChip icon={Database} label={t('Baz çizgisi', 'Baseline')} value="OFFICIAL_PUBLIC" />
            <VisualChip icon={Gauge} label={t('Talep', 'Demand')} value="MODEL_ESTIMATE" />
            <VisualChip icon={ShieldCheck} label={t('Karar', 'Decision')} value={t('İNSAN ONAYLI', 'HUMAN-GATED')} />
          </div>

          <div className="absolute inset-x-4 bottom-4 rounded-[22px] border border-white/10 bg-[#061727]/84 p-4 shadow-2xl backdrop-blur-xl sm:inset-x-6 sm:bottom-6">
            <div className="mb-4 flex items-center justify-between gap-3">
              <span className="text-[8px] font-black uppercase tracking-[0.14em] text-white/42">{t('Bir sonraki servise kadar karar zinciri', 'Decision chain before the next service')}</span>
              <span className="font-mono text-[8px] font-black text-[#b8e467]">MEASURE → LEARN</span>
            </div>
            <div className="grid grid-cols-5 gap-1.5">
              {steps.map((step, index) => (
                <div key={step.en} className="rounded-xl border border-white/[0.08] bg-white/[0.045] p-2.5 text-center">
                  <div className="mx-auto grid h-5 w-5 place-items-center rounded-full border border-[#b8e467]/30 bg-[#b8e467]/10 text-[#b8e467]">
                    {index === steps.length - 1 ? <CheckCircle2 size={9} /> : <span className="font-mono text-[7px] font-black">0{index + 1}</span>}
                  </div>
                  <div className="mt-2 truncate text-[7px] font-black uppercase tracking-[0.05em] text-white/62 sm:text-[8px]">
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

function VisualChip({ icon: Icon, label, value }: { icon: typeof Database; label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#061727]/78 px-3 py-2.5 backdrop-blur-xl">
      <div className="flex items-center gap-1.5 text-white/42"><Icon size={10} /><span className="text-[7px] font-black uppercase tracking-[0.1em]">{label}</span></div>
      <div className="mt-1.5 text-[8px] font-black text-white/82">{value}</div>
    </div>
  );
}
