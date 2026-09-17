'use client';

import { useEffect, useMemo, useState } from 'react';
import { ExternalLink, Film, Loader2, ShieldAlert } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import { PHOTOGRAMMETRY_ASSETS, PHOTOGRAMMETRY_PROVENANCE_NOTE } from '@/lib/photogrammetry-assets';

type Props = {
  onFallback?: () => void;
};

export default function CampusPhotogrammetryViewer({ onFallback }: Props) {
  const { locale, t } = useLocale();
  const [selectedId, setSelectedId] = useState(PHOTOGRAMMETRY_ASSETS[0]?.id ?? '');
  const [loaded, setLoaded] = useState(false);
  const [timedOut, setTimedOut] = useState(false);
  const selected = useMemo(() => PHOTOGRAMMETRY_ASSETS.find(asset => asset.id === selectedId) ?? PHOTOGRAMMETRY_ASSETS[0], [selectedId]);

  useEffect(() => {
    setLoaded(false);
    setTimedOut(false);
    const timer = window.setTimeout(() => {
      setTimedOut(true);
      onFallback?.();
    }, 10_000);
    return () => window.clearTimeout(timer);
  }, [selectedId, onFallback]);

  if (!selected) {
    return <div className="grid h-[520px] place-items-center rounded-[22px] border border-slate-900/10 bg-slate-950 text-sm font-semibold text-slate-300">{t('Fotogrametri sahnesi bulunamadı.', 'No photogrammetry scene is available.')}</div>;
  }

  return (
    <section className="overflow-hidden rounded-[22px] border border-slate-900/10 bg-[#07131f] text-white shadow-2xl shadow-slate-950/10">
      <div className="border-b border-white/10 bg-white/[0.035] px-4 py-3">
        <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-cyan-300"><Film size={13} /> {t('Harici fotogrametri', 'External photogrammetry')}</div>
            <h3 className="mt-1 text-lg font-black tracking-tight">{locale === 'tr' ? selected.titleTr : selected.titleEn}</h3>
            <p className="mt-1 max-w-3xl text-[11px] leading-5 text-slate-300">{locale === 'tr' ? selected.coverageTr : selected.coverageEn}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full border border-amber-300/15 bg-amber-300/[0.07] px-2.5 py-1.5 text-[8px] font-black uppercase tracking-[0.1em] text-amber-100">{t('Sağlayıcı bağımlı', 'Provider dependent')}</span>
            <a href={selected.sourceUrl} target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex w-fit items-center gap-1.5 rounded-lg border border-white/15 bg-white/5 px-3 py-2 text-[10px] font-bold text-slate-100 transition hover:bg-white/10">{t('Orijinal kaynağı aç', 'Open original source')} <ExternalLink size={11} /></a>
          </div>
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

      <div className="relative min-h-[520px] bg-black">
        {!loaded && !timedOut ? (
          <div className="absolute inset-0 z-10 grid place-items-center bg-[#07131f]">
            <div className="text-center">
              <Loader2 size={22} className="mx-auto animate-spin text-cyan-300" />
              <div className="mt-3 text-[10px] font-black uppercase tracking-[0.12em] text-white/48">{t('Fotogrametri sağlayıcısı yükleniyor', 'Loading photogrammetry provider')}</div>
              <div className="mt-1 text-[9px] text-white/28">{t('10 sn içinde yanıt gelmezse yerel 3D görünüme döner.', 'Falls back to local 3D if there is no response within 10 seconds.')}</div>
            </div>
          </div>
        ) : null}

        {timedOut ? (
          <div className="absolute inset-0 z-20 grid place-items-center bg-[#07131f] p-6 text-center">
            <div className="max-w-md">
              <ShieldAlert size={26} className="mx-auto text-amber-200" />
              <div className="mt-3 text-base font-black">{t('Harici 3D sağlayıcı yanıt vermedi.', 'The external 3D provider did not respond.')}</div>
              <p className="mt-2 text-[10px] leading-5 text-white/45">{t('Boş ekran bırakmıyoruz; ürün birinci taraf kampüs 3D görünümüne geri dönüyor.', 'The product does not leave a blank frame; it falls back to the first-party campus 3D view.')}</p>
              <button type="button" onClick={onFallback} className="mt-4 rounded-xl bg-[#b8e467] px-4 py-2.5 text-[10px] font-black text-[#071c33]">{t('Kampüs 3D’ye dön', 'Return to Campus 3D')}</button>
            </div>
          </div>
        ) : null}

        <iframe
          key={selected.modelId}
          title={locale === 'tr' ? selected.titleTr : selected.titleEn}
          src={selected.embedUrl}
          className="h-[520px] w-full border-0"
          allow="autoplay; fullscreen; xr-spatial-tracking"
          allowFullScreen
          loading="eager"
          referrerPolicy="strict-origin-when-cross-origin"
          onLoad={() => setLoaded(true)}
        />
        <div className="pointer-events-none absolute bottom-3 left-3 max-w-[calc(100%-1.5rem)] rounded-lg border border-white/10 bg-slate-950/80 px-3 py-2 text-[9px] leading-4 text-slate-300 shadow-xl backdrop-blur-md"><span className="font-black text-white">{selected.provider}</span><span className="mx-1.5 text-slate-600">•</span>{selected.author}<span className="mx-1.5 text-slate-600">•</span>{t('Harici sağlayıcıda barındırılıyor', 'Hosted by external provider')}</div>
      </div>

      <div className="grid gap-3 border-t border-white/10 bg-white/[0.025] px-4 py-3 lg:grid-cols-[1fr_auto] lg:items-center">
        <p className="text-[10px] leading-5 text-slate-400">{locale === 'tr' ? PHOTOGRAMMETRY_PROVENANCE_NOTE.tr : PHOTOGRAMMETRY_PROVENANCE_NOTE.en}</p>
        <div className="rounded-md border border-emerald-400/20 bg-emerald-400/5 px-2.5 py-1.5 text-[9px] font-bold text-emerald-200">{t('Kaynak + üretici kaydı korunuyor', 'Source + author provenance preserved')}</div>
      </div>
    </section>
  );
}
