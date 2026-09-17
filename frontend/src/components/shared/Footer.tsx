'use client';

import Link from 'next/link';
import { useLocale } from '@/lib/i18n';

export default function Footer() {
  const { t } = useLocale();

  return (
    <footer
      className="mt-10 border-t border-slate-900/10 bg-white/70 bg-[length:420px_420px] bg-repeat"
      style={{ backgroundImage: "url('/assets/campus-topography.svg')" }}
    >
      <div className="mx-auto flex w-full max-w-[1520px] flex-col gap-5 px-4 py-7 sm:px-6 lg:flex-row lg:items-end lg:justify-between lg:px-8">
        <div className="max-w-2xl rounded-xl bg-[#f6f6f1]/80 p-4 backdrop-blur-sm">
          <div className="text-sm font-black tracking-[-0.025em] text-slate-950">BOUNCAMPUS</div>
          <p className="mt-2 text-[11px] leading-5 text-slate-500">
            {t(
              'Boğaziçi Üniversitesi’nin kamuya açık kaynaklarını tek yerde gösterir. Sensör, BMS, POS veya geçiş sistemi verisi bağlı değilse bunu canlı veri gibi sunmaz.',
              'Brings Boğaziçi University public sources into one view. Sensor, BMS, POS or access-control data is never presented as live unless a real integration exists.',
            )}
          </p>
        </div>
        <div className="flex flex-wrap gap-x-5 gap-y-2 rounded-xl bg-[#f6f6f1]/80 p-4 text-[11px] font-semibold text-slate-500 backdrop-blur-sm">
          <Link href="/buildings" className="hover:text-slate-950">{t('Binalar', 'Buildings')}</Link>
          <Link href="/courses" className="hover:text-slate-950">{t('Dersler', 'Courses')}</Link>
          <Link href="/data" className="hover:text-slate-950">{t('Veri kaynakları', 'Data sources')}</Link>
          <Link href="/lab" className="hover:text-slate-950">{t('Deneyler', 'Lab')}</Link>
        </div>
      </div>
    </footer>
  );
}
