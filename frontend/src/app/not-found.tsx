'use client';

import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

export default function NotFound() {
  const { t } = useLocale();
  return <div className="grid min-h-[58vh] place-items-center"><div className="max-w-md text-center"><div className="font-mono text-[11px] font-black text-slate-400">404</div><h1 className="mt-3 text-3xl font-black tracking-[-0.05em] text-slate-950">{t('Sayfa bulunamadı', 'Page not found')}</h1><p className="mt-3 text-[11px] leading-5 text-slate-500">{t('Bu adres artık mevcut değil veya taşınmış olabilir.', 'This address may no longer exist or may have moved.')}</p><Link href="/" className="mt-5 inline-flex items-center gap-1.5 rounded-lg bg-[#102a43] px-3 py-2 text-[10px] font-bold text-white"><ArrowLeft size={11} /> {t('Genel bakışa dön', 'Back to overview')}</Link></div></div>;
}
