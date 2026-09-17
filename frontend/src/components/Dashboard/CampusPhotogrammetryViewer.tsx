'use client';

import { useMemo, useState } from 'react';
import { ExternalLink, Film } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import { PHOTOGRAMMETRY_ASSETS, PHOTOGRAMMETRY_PROVENANCE_NOTE } from '@/lib/photogrammetry-assets';

export default function CampusPhotogrammetryViewer() {
  const { locale, t } = useLocale();
  const [selectedId, setSelectedId] = useState(PHOTOGRAMMETRY_ASSETS[0]?.id ?? '');
  const selected = useMemo(() => PHOTOGRAMMETRY_ASSETS.find(asset => asset.id === selectedId) ?? PHOTOGRAMMETRY_ASSETS[0], [selectedId]);

  if (!selected) {
    return <div className="grid h-[520px] place-items-center rounded-xl border border-slate-900/10 bg-slate-950 text-sm font-semibold text-slate-300">{t('Fotogrametri sahnesi bulunamadı.', 'No photogrammetry scene is available.')}</div>;
  }

  return (
    <section className="overflow-hidden rounded-xl border border-slate-900/10 bg-[#07131f] text-white shadow-2xl shadow-slate-950/10">
      <div className="border-b border-white/10 bg-white/[0.035] px-4 py-3">
        <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-cyan-300"><Film size={13} /> {t('Kaynak destekli fotogrametri', 'Source-backed photogrammetry')}</div>
            <h3 className="mt-1 text-lg font-black tracking-tight">{locale === 'tr' ? selected.titleTr : selected.titleEn}</h3>
            <p className="mt-1 max-w-3xl text-[11px] leading-5 text-slate-300">{locale === 'tr' ? selected.coverageTr : selected.coverageEn}</p>
          </div>
          <a href={selected.sourceUrl} target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex w-fit items-center gap-1.5 rounded-lg border border-white/15 bg-white/5 px-3 py-2 text-[10px] font-bold text-slate-100 transition hover:bg-white/10">{t('Orijinal 3D kaynağı aç', 'Open original 3D source')} <ExternalLink size={11} /></a>
        </div>

        <div className="mt-3 flex gap-2 overflow-x-auto pb-1">
          {PHOTOGRAMMETRY_ASSETS.map(asset => {
            const active = asset.id === selected.id;
            return (
              <button key={asset.id} type="button" onClick={() => setSelectedId(asset.id)} className={`bc-focus-ring shrink-0 rounded-lg border px-3 py-2 text-left transition ${active ? 'border-cyan-300/60 bg-cyan-300/10 text-white' : 'border-white/10 bg-white/[0.025] text-slate-400 hover:border-white/20 hover:text-slate-200'}`}>
                <span className="block text-[9px] font-black uppercase tracking-[0.14em] text-cyan-300/80">{asset.campus}</span>
                <span className="mt-0.5 block max-w-[210px] truncate text-[10px] font-bold">{locale === 'tr' ? asset.titleTr : asset.titleEn}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="relative bg-black">
        <iframe key={selected.modelId} title={locale === 'tr' ? selected.titleTr : selected.titleEn} src={selected.embedUrl} className="h-[520px] w-full border-0" allow="autoplay; fullscreen; xr-spatial-tracking" allowFullScreen loading="eager" referrerPolicy="strict-origin-when-cross-origin" />
        <div className="pointer-events-none absolute bottom-3 left-3 max-w-[calc(100%-1.5rem)] rounded-lg border border-white/10 bg-slate-950/80 px-3 py-2 text-[9px] leading-4 text-slate-300 shadow-xl backdrop-blur-md"><span className="font-black text-white">{selected.provider}</span><span className="mx-1.5 text-slate-600">•</span>{selected.author}<span className="mx-1.5 text-slate-600">•</span>{t('Harici sağlayıcıda barındırılıyor', 'Hosted by external provider')}</div>
      </div>

      <div className="grid gap-3 border-t border-white/10 bg-white/[0.025] px-4 py-3 lg:grid-cols-[1fr_auto] lg:items-center">
        <p className="text-[10px] leading-5 text-slate-400">{locale === 'tr' ? PHOTOGRAMMETRY_PROVENANCE_NOTE.tr : PHOTOGRAMMETRY_PROVENANCE_NOTE.en}</p>
        <div className="rounded-md border border-emerald-400/20 bg-emerald-400/5 px-2.5 py-1.5 text-[9px] font-bold text-emerald-200">{t('Kaynak + üretici kaydı korunuyor', 'Source + author provenance preserved')}</div>
      </div>
    </section>
  );
}
