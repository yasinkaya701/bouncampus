'use client';

import Link from 'next/link';
import { ArrowRight, ShieldCheck } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

export default function Footer() {
  const { t } = useLocale();

  return (
    <footer className="mt-12 border-t border-slate-950/[0.07] bg-white/55 backdrop-blur-sm">
      <div className="mx-auto w-full max-w-[1520px] px-4 py-8 sm:px-6 lg:px-8">
        <div
          className="relative overflow-hidden rounded-[24px] border border-slate-950/[0.08] bg-[#f8faf7] p-5 sm:p-6"
          style={{ backgroundImage: "url('/assets/campus-topography.svg')", backgroundSize: '520px 520px' }}
        >
          <div aria-hidden="true" className="absolute inset-0 bg-[linear-gradient(90deg,rgba(248,250,247,.98),rgba(248,250,247,.88),rgba(248,250,247,.72))]" />
          <div className="relative grid gap-6 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
            <div className="max-w-3xl">
              <div className="flex items-center gap-2">
                <span className="grid h-8 w-8 place-items-center rounded-lg bg-[#071c33] text-[8px] font-black tracking-[0.1em] text-white">BC</span>
                <div>
                  <div className="text-[13px] font-black tracking-[-0.03em] text-slate-950">BOUNCAMPUS</div>
                  <div className="text-[8px] font-black uppercase tracking-[0.14em] text-slate-400">Campus climate intelligence</div>
                </div>
              </div>
              <p className="mt-4 max-w-2xl text-[10px] leading-5 text-slate-500">
                {t(
                  'Boğaziçi Üniversitesi’nin kamuya açık kaynaklarını karar bağlamına taşır. Sensör, BMS, POS veya geçiş sistemi bağlı değilse bunu canlı veri gibi sunmaz; model çıktısını model çıktısı olarak etiketler.',
                  'Turns Boğaziçi University public sources into decision context. Sensor, BMS, POS or access-control data is never presented as live unless actually integrated; model outputs remain explicitly labeled as model outputs.',
                )}
              </p>
              <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-emerald-900/10 bg-emerald-50 px-3 py-1.5 text-[8px] font-black text-emerald-700">
                <ShieldCheck size={10} /> {t('Şeffaf veri provenansı', 'Transparent data provenance')}
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <Link href="/buildings" className="rounded-lg px-2.5 py-2 text-[9px] font-bold text-slate-500 transition hover:bg-white hover:text-slate-950">{t('Binalar', 'Buildings')}</Link>
              <Link href="/courses" className="rounded-lg px-2.5 py-2 text-[9px] font-bold text-slate-500 transition hover:bg-white hover:text-slate-950">{t('Dersler', 'Courses')}</Link>
              <Link href="/data" className="rounded-lg px-2.5 py-2 text-[9px] font-bold text-slate-500 transition hover:bg-white hover:text-slate-950">{t('Veri kaynakları', 'Data sources')}</Link>
              <Link href="/lab" className="rounded-lg px-2.5 py-2 text-[9px] font-bold text-slate-500 transition hover:bg-white hover:text-slate-950">{t('Deneyler', 'Lab')}</Link>
              <Link href="/demo" className="inline-flex items-center gap-1.5 rounded-xl bg-[#071c33] px-3.5 py-2.5 text-[9px] font-black text-white shadow-sm transition hover:bg-[#0b3153]">{t('Jüri demosu', 'Jury demo')} <ArrowRight size={10} /></Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
