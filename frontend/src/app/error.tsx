'use client';

import { useEffect } from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  const { t } = useLocale();
  useEffect(() => { console.error(error); }, [error]);
  return <div className="grid min-h-[58vh] place-items-center"><div className="max-w-lg border-t border-slate-900/10 pt-5 text-center"><AlertTriangle size={22} className="mx-auto text-amber-600" /><h2 className="mt-3 text-2xl font-black tracking-[-0.04em] text-slate-950">{t('Bu görünüm yüklenemedi', 'This view could not be loaded')}</h2><p className="mt-3 text-[11px] leading-5 text-slate-500">{t('Veri kaynağı veya uygulama katmanında geçici bir hata oluştu. Eski demo verisi gösterilmedi.', 'A temporary source or application error occurred. No stale demo data was substituted.')}</p><button type="button" onClick={reset} className="mt-5 inline-flex items-center gap-1.5 rounded-lg bg-[#102a43] px-3 py-2 text-[10px] font-bold text-white"><RotateCcw size={11} /> {t('Tekrar dene', 'Try again')}</button></div></div>;
}
