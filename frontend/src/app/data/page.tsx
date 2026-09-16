'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowUpRight, CheckCircle2, Database, ExternalLink, RefreshCw, ShieldAlert } from 'lucide-react';
import type { SourceMeta } from '@/lib/live-sources';

type HealthPayload = {
  status: 'ok' | 'degraded';
  checked_at: string;
  latency_ms: number;
  sources: SourceMeta[];
  failed_source_ids: string[];
  schedule_snapshot?: SourceMeta;
};

const provenanceLabel: Record<string, string> = {
  OFFICIAL_LIVE: 'OFFICIAL LIVE',
  OFFICIAL_SNAPSHOT: 'OFFICIAL SNAPSHOT',
  EXTERNAL_LIVE: 'EXTERNAL LIVE',
  MODEL_ESTIMATE: 'MODEL ESTIMATE',
  FALLBACK: 'UNAVAILABLE',
};

export default function DataTrustPage() {
  const [health, setHealth] = useState<HealthPayload | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/health', { cache: 'no-store' });
      const payload = await response.json();
      setHealth(payload);
    } catch {
      setHealth({ status: 'degraded', checked_at: new Date().toISOString(), latency_ms: 0, sources: [], failed_source_ids: ['health-endpoint'] });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const sources = health?.sources ?? [];
  const healthy = sources.filter(source => source.ok).length;
  const failed = sources.filter(source => !source.ok).length;

  return (
    <div className="space-y-6">
      <section className="grid gap-5 rounded-[30px] border border-slate-950/10 bg-[#e9ece8] p-6 lg:grid-cols-[minmax(0,1fr)_360px] lg:p-8">
        <div>
          <div className="bc-eyebrow">Data trust layer</div>
          <h1 className="mt-2 max-w-3xl text-3xl font-black leading-[1.04] tracking-[-0.055em] text-[#0a1020] sm:text-4xl">
            Know exactly what is live, modeled, stale or unavailable.
          </h1>
          <p className="mt-4 max-w-2xl text-sm leading-relaxed text-slate-600">
            BOUNCAMPUS keeps public university sources, dated official snapshots, external weather and model outputs in separate provenance classes. The UI never upgrades an estimate into telemetry.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-2 self-end">
          <div className="rounded-[18px] bg-white/80 p-4 ring-1 ring-slate-950/8">
            <div className="font-mono text-2xl font-black tracking-[-0.04em] text-[#0a1020]">{healthy}</div>
            <div className="mt-1 text-[10px] font-bold uppercase tracking-[0.12em] text-slate-500">healthy sources</div>
          </div>
          <div className="rounded-[18px] bg-white/80 p-4 ring-1 ring-slate-950/8">
            <div className="font-mono text-2xl font-black tracking-[-0.04em] text-[#0a1020]">{failed}</div>
            <div className="mt-1 text-[10px] font-bold uppercase tracking-[0.12em] text-slate-500">degraded</div>
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-4">
        {[
          ['OFFICIAL LIVE', 'Published by Boğaziçi and fetched from the current public page.'],
          ['OFFICIAL SNAPSHOT', 'Published by Boğaziçi but stored as a dated local snapshot.'],
          ['EXTERNAL LIVE', 'Current external feed, such as weather, not a university sensor.'],
          ['MODEL ESTIMATE', 'Computed output from schedules, assumptions or scenario logic.'],
        ].map(([title, note]) => (
          <div key={title} className="bc-surface rounded-[22px] p-5">
            <div className="text-[10px] font-black tracking-[0.08em] text-[#0a1020]">{title}</div>
            <p className="mt-2 text-[11px] leading-relaxed text-slate-500">{note}</p>
          </div>
        ))}
      </section>

      <section className="bc-surface rounded-[28px] p-5 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="bc-eyebrow">Runtime health</div>
            <div className="mt-1 flex items-center gap-2">
              {health?.status === 'ok' ? <CheckCircle2 size={18} className="text-emerald-600" /> : <ShieldAlert size={18} className="text-amber-600" />}
              <h2 className="text-xl font-black tracking-[-0.035em] text-[#0a1020]">{health?.status === 'ok' ? 'Sources available' : 'Degraded source state'}</h2>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">
              {health ? `Checked ${new Date(health.checked_at).toLocaleString('tr-TR')} · ${health.latency_ms} ms` : 'Health endpoint is being checked.'}
            </p>
          </div>
          <button onClick={refresh} disabled={loading} className="bc-focus-ring inline-flex items-center gap-2 self-start rounded-full bg-[#0b1226] px-3.5 py-2 text-[10px] font-black text-white disabled:opacity-50">
            <RefreshCw size={12} className={loading ? 'animate-spin' : ''} /> Refresh sources
          </button>
        </div>

        <div className="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {sources.length ? sources.map(source => (
            <a key={source.id} href={source.url} target={source.url.startsWith('http') ? '_blank' : undefined} rel="noreferrer" className="group rounded-[20px] border border-slate-950/8 bg-[#fafaf8] p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-sm">
              <div className="flex items-start justify-between gap-4">
                <span className={`rounded-full px-2 py-1 font-mono text-[9px] font-black ${source.ok ? 'bg-slate-100 text-slate-700' : 'bg-amber-100 text-amber-800'}`}>
                  {source.ok ? (provenanceLabel[source.provenance] ?? source.provenance) : 'UNAVAILABLE'}
                </span>
                {source.url.startsWith('http') && <ExternalLink size={12} className="text-slate-300 group-hover:text-slate-600" />}
              </div>
              <h3 className="mt-4 text-xs font-black leading-snug text-[#0a1020]">{source.label}</h3>
              <p className="mt-2 text-[10px] leading-relaxed text-slate-500">{source.detail}</p>
              <div className="mt-3 font-mono text-[9px] text-slate-400">{new Date(source.fetched_at).toLocaleString('tr-TR')}</div>
            </a>
          )) : (
            <div className="md:col-span-2 xl:col-span-3 rounded-[20px] border border-dashed border-slate-300 p-8 text-center">
              <Database size={20} className="mx-auto text-slate-300" />
              <p className="mt-2 text-xs font-bold text-slate-500">No source metadata available.</p>
            </div>
          )}
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="bc-surface-dark rounded-[26px] p-5 text-white">
          <div className="bc-eyebrow !text-slate-500">Not connected today</div>
          <h2 className="mt-2 text-lg font-black tracking-[-0.03em]">What BOUNCAMPUS does not claim</h2>
          <p className="mt-3 text-[11px] leading-relaxed text-slate-400">University BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS and live IoT telemetry are not connected. Any workflow that depends on them remains a model or prototype until authorized access exists.</p>
        </div>
        <div className="bc-surface rounded-[26px] p-5">
          <div className="bc-eyebrow">Documentation</div>
          <h2 className="mt-2 text-lg font-black tracking-[-0.03em] text-[#0a1020]">Audit the contract</h2>
          <p className="mt-3 text-[11px] leading-relaxed text-slate-500">The repository documents source classes, degradation rules, freshness boundaries and the pilot path for authorized university integrations.</p>
          <Link href="/#sources" className="mt-5 inline-flex items-center gap-1.5 text-[10px] font-black text-blue-700">Open overview provenance <ArrowUpRight size={11} /></Link>
        </div>
      </section>
    </div>
  );
}
