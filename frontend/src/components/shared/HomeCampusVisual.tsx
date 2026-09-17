'use client';

import { usePathname } from 'next/navigation';
import { useLocale } from '@/lib/i18n';

export default function HomeCampusVisual() {
  const pathname = usePathname();
  const { t } = useLocale();

  if (pathname !== '/') return null;

  return (
    <section
      role="img"
      aria-label={t('Boğaziçi Güney Kampüs ve dijital kampüs katmanını betimleyen özgün illüstrasyon', 'Original illustration of Boğaziçi South Campus and the digital campus layer')}
      className="mb-7 min-h-[220px] overflow-hidden rounded-2xl border border-slate-900/10 bg-white bg-cover bg-center shadow-[0_18px_60px_rgba(15,23,42,0.05)] sm:min-h-[280px] lg:min-h-[320px]"
      style={{ backgroundImage: "url('/assets/bouncampus-hero.svg')" }}
    />
  );
}
