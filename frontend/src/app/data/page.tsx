'use client';

import { useEffect, useState } from 'react';
import { CheckCircle2, ExternalLink, RefreshCw, ShieldAlert } from 'lucide-react';
import type { SourceMeta } from '@/lib/live-sources';
import { useLocale } from '@/lib/i18n';

type HealthPayload = { status: 'ok' | 'degraded'; checked_at: string; latency_ms: number; sources: SourceMeta[]; failed_source_ids: string[] };

export default function DataTrustPage() {
  const { locale, t } = useLocale();
  const [health, setHealth] = useState<HealthPayload | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    setLoading(true);
    try { const response = await fetch('/api/v1/health', { cache: 'no-store' }); setHealth(await response.json()); }
    catch { setHealth({ status: 'degraded', checked_at: new Date().toISOString(), latency_ms: 0, sources: [], failed_source_ids: ['health-endpoint'] }); }
    finally { setLoading(false); }
  }
  useEffect(() => { refresh(); }, []);

  const sources = health?.sources ?? [];
  const healthy = sources.filter(source => source.ok).length;
  const failed = sources.filter(source => !source.ok).length;
  const provenance = (value: SourceMeta['provenance']) => ({ OFFICIAL_LIVE: t('RESMÎ CANLI', 'OFFICIAL LIVE'), OFFICIAL_SNAPSHOT: t('RESMÎ SNAPSHOT', 'OFFICIAL SNAPSHOT'), EXTERNAL_LIVE: t('HARİCÎ CANLI', 'EXTERNAL LIVE'), MODEL_ESTIMATE: t('MODEL TAHMİNİ', 'MODEL ESTIMATE'), FALLBACK: t('KULLANILAMIYOR', 'UNAVAILABLE') }[value] ?? value);

  return (
    <div className="space-y-7">
      <section className="grid gap-6 border-b border-slate-900/10 pb-7 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-end"><div><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('Veri güveni', 'Data trust')}</div><h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Kaynaklar', 'Sources')}</h1><p className="mt-3 max-w-2xl text-[12px] leading-6 text-slate-500">{t('Canlı, snapshot, haricî ve model verileri aynı şey değildir. Bu sayfa her kaynağın durumunu ve sınırını açık tutar.', 'Live feeds, snapshots, external feeds and model outputs are not the same thing. This page keeps the status and boundary of every source explicit.')}</p></div><div className="grid grid-cols-2 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4"><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Sağlıklı', 'Healthy')}</div><div className="mt-1 font-mono text-xl font-black text-emerald-700">{healthy}</div></div><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Sorunlu', 'Degraded')}</div><div className="mt-1 font-mono text-xl font-black text-amber-700">{failed}</div></div></div></section>

      <section className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><div className="flex items-center gap-2">{health?.status === 'ok' ? <CheckCircle2 size={16} className="text-emerald-600" /> : <ShieldAlert size={16} className="text-amber-600" />}<div><div className="text-[11px] font-black text-slate-900">{health?.status === 'ok' ? t('Kaynaklar erişilebilir', 'Sources available') : t('Kısıtlı kaynak durumu', 'Degraded source state')}</div><div className="mt-0.5 text-[9px] text-slate-400">{health ? `${new Date(health.checked_at).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} · ${health.latency_ms} ms` : t('Kontrol ediliyor…', 'Checking…')}</div></div></div><button onClick={refresh} disabled={loading} className="inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-3 py-2 text-[10px] font-bold disabled:opacity-50"><RefreshCw size={11} className={loading ? 'animate-spin' : ''} /> {t('Yenile', 'Refresh')}</button></section>

      <section className="divide-y divide-slate-900/10 border-y border-slate-900/10 bg-white">{sources.length ? sources.map(source => <a key={source.id} href={source.url} target={source.url.startsWith('http') ? '_blank' : undefined} rel="noreferrer" className="grid gap-2 px-4 py-4 sm:grid-cols-[190px_160px_minmax(0,1fr)_20px] sm:items-center"><div className="text-[11px] font-black text-slate-900">{source.label}</div><div className={`text-[9px] font-bold ${source.ok ? 'text-emerald-700' : 'text-amber-700'}`}>{source.ok ? provenance(source.provenance) : t('KULLANILAMIYOR', 'UNAVAILABLE')}</div><div className="text-[10px] leading-5 text-slate-500">{source.detail}</div>{source.url.startsWith('http') ? <ExternalLink size={11} className="text-slate-300" /> : <span />}</a>) : <div className="p-10 text-center text-[11px] text-slate-400">{t('Kaynak metadata’sı alınamadı.', 'No source metadata is available.')}</div>}</section>

      <section className="grid gap-6 border-t border-slate-900/10 pt-5 md:grid-cols-2"><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Bağlı olmayan sistemler', 'Not connected')}</div><p className="mt-2 text-[11px] leading-5 text-slate-500">{t('Üniversite BMS, akıllı sayaç, turnike, Wi-Fi doluluk, yemekhane POS, mekik GPS ve canlı IoT telemetrisi bağlı değildir. Bu sistemlere dayanan değerler ancak model veya prototip olabilir.', 'University BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS and live IoT telemetry are not connected. Values that depend on them can only be model or prototype outputs.')}</p></div><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Provenans kuralı', 'Provenance rule')}</div><p className="mt-2 text-[11px] leading-5 text-slate-500">{t('Kaynak sağlığı düşerse arayüz bunu görünür yapar; eski veya tahmini veriyi canlı telemetriye yükseltmez.', 'When source health degrades, the interface makes that visible instead of upgrading stale or estimated values into live telemetry.')}</p></div></section>
    </div>
  );
}
