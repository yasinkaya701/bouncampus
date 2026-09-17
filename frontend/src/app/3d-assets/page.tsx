'use client';

import { useMemo, useState } from 'react';
import { Box, Database, ExternalLink, ScanLine, ShieldCheck } from 'lucide-react';
import { CAMPUS_3D_ASSETS, EMBEDDABLE_CAMPUS_3D_ASSETS } from '@/lib/campus-3d-assets';
import { useLocale } from '@/lib/i18n';

const campusLabels: Record<string, { tr: string; en: string }> = {
  south: { tr: 'Güney', en: 'South' },
  north: { tr: 'Kuzey', en: 'North' },
  hisar: { tr: 'Hisar', en: 'Hisar' },
  ucaksavar: { tr: 'Uçaksavar', en: 'Uçaksavar' },
  kandilli: { tr: 'Kandilli', en: 'Kandilli' },
  anadolu: { tr: 'Anadolu Hisarı', en: 'Anadolu Hisarı' },
  kilyos: { tr: 'Kilyos', en: 'Kilyos' },
};

export default function Campus3DAssetsPage() {
  const { locale, t } = useLocale();
  const [selectedId, setSelectedId] = useState(EMBEDDABLE_CAMPUS_3D_ASSETS[0]?.id ?? '');
  const selected = useMemo(
    () => EMBEDDABLE_CAMPUS_3D_ASSETS.find(asset => asset.id === selectedId) ?? EMBEDDABLE_CAMPUS_3D_ASSETS[0],
    [selectedId],
  );
  const osmAsset = CAMPUS_3D_ASSETS.find(asset => asset.mode === 'runtime-derived');

  return (
    <div className="space-y-7">
      <section className="border-b border-slate-900/10 pb-7">
        <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">
          <Box size={13} /> {t('Kampüs 3D varlıkları', 'Campus 3D assets')}
        </div>
        <div className="mt-3 grid gap-6 lg:grid-cols-[minmax(0,1fr)_420px] lg:items-end">
          <div>
            <h1 className="text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">
              {t('Boğaziçi 3D kaynak kütüphanesi', 'Boğaziçi 3D source library')}
            </h1>
            <p className="mt-3 max-w-3xl text-[12px] leading-6 text-slate-500">
              {t(
                'Uygulama içindeki bina geometrisi OpenStreetMap footprint, kat/yükseklik ve çatı etiketlerinden üretilir. Yüksek detaylı üçüncü taraf fotogrametri modelleri ise yeniden dağıtım lisansları doğrulanana kadar yalnızca kaynağından gömülü olarak gösterilir; model dosyaları repoya kopyalanmaz.',
                'In-app building geometry is derived from OpenStreetMap footprints, level/height and roof tags. High-detail third-party photogrammetry is shown only as source-hosted embeds until redistribution rights are verified; model binaries are not copied into the repository.',
              )}
            </p>
          </div>
          <div className="grid grid-cols-2 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4">
            <div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Kapsanan kampüs', 'Campuses covered')}</div><div className="mt-1 font-mono text-xl font-black text-slate-900">7</div></div>
            <div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('3D kaynak', '3D sources')}</div><div className="mt-1 font-mono text-xl font-black text-emerald-700">{CAMPUS_3D_ASSETS.length}</div></div>
          </div>
        </div>
      </section>

      {osmAsset && (
        <section className="grid gap-4 rounded-xl border border-emerald-900/10 bg-emerald-50/50 p-5 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
          <div>
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.12em] text-emerald-800"><Database size={13} /> {t('Repo-içi geometri kaynağı', 'Repository geometry source')}</div>
            <h2 className="mt-2 text-xl font-black tracking-[-0.03em] text-slate-950">{osmAsset.title}</h2>
            <p className="mt-2 max-w-3xl text-[11px] leading-5 text-slate-600">{t('Footprint ve mevcut bina etiketleri /api/v1/campus-geometry üzerinden gelir. Eksik yükseklikler ölçüm gibi sunulmaz; görselleştirme tahmini olarak işaretlenir.', 'Footprints and available building tags are served through /api/v1/campus-geometry. Missing heights are never presented as measured values; they are marked as visualization estimates.')}</p>
            <div className="mt-3 flex flex-wrap gap-2">{osmAsset.campus.map(campus => <span key={campus} className="rounded-full border border-emerald-900/10 bg-white px-2 py-1 text-[9px] font-bold text-emerald-800">{campusLabels[campus]?.[locale] ?? campus}</span>)}</div>
          </div>
          <div className="flex flex-wrap gap-2 lg:justify-end">
            <a href="/api/v1/campus-geometry?campus=main" target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-lg bg-[#102a43] px-3 py-2 text-[10px] font-bold text-white"><ScanLine size={12} /> API</a>
            <a href={osmAsset.sourceUrl} target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-3 py-2 text-[10px] font-bold text-slate-700"><ExternalLink size={12} /> ODbL</a>
          </div>
        </section>
      )}

      <section className="grid gap-5 xl:grid-cols-[360px_minmax(0,1fr)]">
        <div className="space-y-2">
          <div className="mb-3 flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.12em] text-slate-400"><ScanLine size={13} /> {t('Yüksek detaylı dış kaynaklar', 'High-detail external sources')}</div>
          {EMBEDDABLE_CAMPUS_3D_ASSETS.map(asset => {
            const active = asset.id === selected?.id;
            return (
              <button key={asset.id} type="button" onClick={() => setSelectedId(asset.id)} className={`bc-focus-ring w-full rounded-xl border p-4 text-left transition ${active ? 'border-[#173f67]/30 bg-white shadow-sm' : 'border-slate-900/10 bg-white/60 hover:bg-white'}`}>
                <div className="flex items-start justify-between gap-3">
                  <div><div className="text-[9px] font-black uppercase tracking-[0.1em] text-slate-400">{asset.campus.map(campus => campusLabels[campus]?.[locale] ?? campus).join(' · ')}</div><div className="mt-1 text-[12px] font-black leading-5 text-slate-900">{asset.title}</div></div>
                  <span className={`mt-0.5 h-2 w-2 shrink-0 rounded-full ${active ? 'bg-emerald-500' : 'bg-slate-200'}`} />
                </div>
                <div className="mt-3 flex items-center gap-1.5 text-[9px] font-semibold text-amber-700"><ShieldCheck size={11} /> {t('Embed-only · yeniden dağıtım doğrulanmadı', 'Embed-only · redistribution unverified')}</div>
              </button>
            );
          })}
        </div>

        <div className="overflow-hidden rounded-xl border border-slate-900/10 bg-white">
          {selected ? (
            <>
              <div className="flex flex-col gap-3 border-b border-slate-900/10 p-4 sm:flex-row sm:items-center sm:justify-between">
                <div><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">Sketchfab · {selected.author}</div><h2 className="mt-1 text-[16px] font-black tracking-[-0.025em] text-slate-950">{selected.title}</h2></div>
                <a href={selected.sourceUrl} target="_blank" rel="noreferrer" className="bc-focus-ring inline-flex w-fit items-center gap-1.5 rounded-lg border border-slate-900/10 px-3 py-2 text-[10px] font-bold text-slate-700"><ExternalLink size={12} /> {t('Kaynağı aç', 'Open source')}</a>
              </div>
              <div className="aspect-[16/10] min-h-[420px] bg-slate-950">
                <iframe title={selected.title} src={selected.embedUrl} className="h-full w-full border-0" loading="lazy" allow="autoplay; fullscreen; xr-spatial-tracking" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" />
              </div>
              <div className="grid gap-3 border-t border-slate-900/10 p-4 sm:grid-cols-2">
                <div><div className="text-[9px] font-black uppercase tracking-[0.1em] text-slate-400">{t('Repo modu', 'Repository mode')}</div><div className="mt-1 text-[10px] font-bold text-slate-800">embed-only</div></div>
                <div><div className="text-[9px] font-black uppercase tracking-[0.1em] text-slate-400">{t('Lisans sınırı', 'License boundary')}</div><div className="mt-1 text-[10px] font-semibold leading-4 text-slate-600">{t('Model binary dosyası repoda tutulmuyor.', 'Model binary is not stored in the repository.')}</div></div>
              </div>
            </>
          ) : <div className="grid min-h-[420px] place-items-center text-xs font-semibold text-slate-400">{t('3D kaynak bulunamadı.', 'No 3D source found.')}</div>}
        </div>
      </section>

      <section className="rounded-xl border border-slate-900/10 bg-white p-5 text-[10px] leading-5 text-slate-500">
        <strong className="text-slate-800">{t('Provenans notu:', 'Provenance note:')}</strong> {t('Bu katalog görsel referans ile yeniden dağıtılabilir asseti bilinçli olarak ayırır. OpenStreetMap verisi ODbL ve atıf koşullarıyla kullanılır; Sketchfab modelleri ise lisans metni ayrıca doğrulanmadıkça yalnızca sağlayıcının viewer’ı üzerinden açılır.', 'This catalog deliberately separates visual references from redistributable assets. OpenStreetMap data is used under ODbL attribution/share-alike terms; Sketchfab models stay provider-hosted unless their model-specific redistribution license is separately verified.')}
      </section>
    </div>
  );
}
