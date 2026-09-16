'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, CheckCircle2, ClipboardCheck, Clock3, Gauge, ShieldCheck, Sparkles } from 'lucide-react';
import ActionCards from '@/components/Dashboard/ActionCards';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';

export default function DecisionsPage() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard().then(setData);
  }, []);

  const stats = useMemo(() => {
    if (!data) return { high: 0, total: 0, energy: 0, food: 0 };
    return {
      high: data.actions.filter(action => action.priority === 'HIGH').length,
      total: data.actions.length,
      energy: data.actions.filter(action => action.type === 'energy').length,
      food: data.actions.filter(action => action.type === 'food').length,
    };
  }, [data]);

  if (!data) {
    return (
      <div className="grid min-h-[60vh] place-items-center">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-300 border-t-[#0b1226]" />
          <p className="mt-3 text-xs font-semibold text-slate-500">Decision workspace hazırlanıyor…</p>
        </div>
      </div>
    );
  }

  const degraded = data.data_quality?.mode === 'DEGRADED';

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[30px] bg-[#0b1226] text-white shadow-[0_22px_70px_rgba(11,18,38,0.20)]">
        <div className="grid gap-8 px-6 py-7 lg:grid-cols-[minmax(0,1fr)_360px] lg:px-8 lg:py-9">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="bc-chip border-blue-300/15 bg-blue-300/10 text-blue-200"><ClipboardCheck size={11} /> DECISION QUEUE</span>
              <span className={`bc-chip ${degraded ? 'border-amber-300/20 bg-amber-300/10 text-amber-200' : 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200'}`}>
                {degraded ? 'DEGRADED INPUTS' : 'INPUTS AVAILABLE'}
              </span>
            </div>
            <h1 className="mt-5 max-w-3xl text-3xl font-black leading-[1.02] tracking-[-0.055em] sm:text-4xl lg:text-[46px]">
              Turn campus signals into decisions people can verify.
            </h1>
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-slate-400">
              Every recommendation is a decision-support candidate, not an automatic command. Source provenance, assumptions and expected model impact remain visible before a human acts.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 self-end">
            {[
              ['Open candidates', stats.total],
              ['High priority', stats.high],
              ['Energy', stats.energy],
              ['Food', stats.food],
            ].map(([label, value]) => (
              <div key={label} className="rounded-[18px] border border-white/10 bg-white/[0.04] p-4">
                <div className="font-mono text-2xl font-black tracking-[-0.04em] text-white">{value}</div>
                <div className="mt-1 text-[10px] font-bold uppercase tracking-[0.12em] text-slate-500">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-3">
        <div className="bc-surface rounded-[22px] p-5">
          <div className="flex items-center gap-2 text-xs font-black text-[#0a1020]"><ShieldCheck size={15} className="text-blue-600" /> Human approval</div>
          <p className="mt-2 text-[11px] leading-relaxed text-slate-500">No BMS, kitchen or transport command is dispatched by this product. Recommendations stop at the decision-support boundary.</p>
        </div>
        <div className="bc-surface rounded-[22px] p-5">
          <div className="flex items-center gap-2 text-xs font-black text-[#0a1020]"><Gauge size={15} className="text-violet-600" /> Model impact</div>
          <p className="mt-2 text-[11px] leading-relaxed text-slate-500">Savings, demand and CO₂ values are modeled potential and must not be read as realized meter outcomes.</p>
        </div>
        <div className="bc-surface rounded-[22px] p-5">
          <div className="flex items-center gap-2 text-xs font-black text-[#0a1020]"><Clock3 size={15} className="text-emerald-600" /> Operating cadence</div>
          <p className="mt-2 text-[11px] leading-relaxed text-slate-500">Use the queue as a daily operating brief: review inputs, challenge assumptions, approve manually, then record outcomes.</p>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_340px]">
        <div>
          <div className="mb-4 flex items-end justify-between gap-4">
            <div>
              <div className="bc-eyebrow">Today&apos;s candidates</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Operational recommendations</h2>
            </div>
            <Link href="/scenarios" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-full border border-slate-950/10 bg-white px-3 py-2 text-[10px] font-black text-slate-700 shadow-sm">
              Test a what-if <ArrowRight size={11} />
            </Link>
          </div>
          {data.actions.length ? (
            <ActionCards actions={data.actions} />
          ) : (
            <div className="bc-surface rounded-[24px] p-8 text-center">
              <CheckCircle2 size={24} className="mx-auto text-emerald-600" />
              <h3 className="mt-3 text-sm font-black text-[#0a1020]">No decision candidates right now</h3>
              <p className="mt-1 text-[11px] text-slate-500">The product will not fabricate a recommendation when source inputs are unavailable or no rule is triggered.</p>
            </div>
          )}
        </div>

        <aside className="bc-surface-dark h-fit rounded-[26px] p-5 text-white">
          <div className="bc-eyebrow !text-slate-500">Decision protocol</div>
          <h2 className="mt-2 text-lg font-black tracking-[-0.03em]">Five checks before acting</h2>
          <div className="mt-5 space-y-4">
            {[
              ['01', 'Verify source', 'Open the provenance panel and confirm the upstream is healthy.'],
              ['02', 'Read the boundary', 'Confirm whether the number is live, snapshot or model estimate.'],
              ['03', 'Challenge assumptions', 'Check schedule, weather and capacity assumptions for the specific day.'],
              ['04', 'Approve manually', 'A responsible operator decides whether the recommendation is appropriate.'],
              ['05', 'Measure outcome', 'If implemented, compare actual outcome with the modeled potential.'],
            ].map(([n, title, note]) => (
              <div key={n} className="flex gap-3">
                <span className="font-mono text-[9px] font-black text-blue-300">{n}</span>
                <div>
                  <div className="text-xs font-black">{title}</div>
                  <p className="mt-1 text-[10px] leading-relaxed text-slate-400">{note}</p>
                </div>
              </div>
            ))}
          </div>
          <Link href="/#sources" className="mt-6 inline-flex items-center gap-1.5 text-[10px] font-black text-blue-300">Inspect provenance <ArrowRight size={11} /></Link>
        </aside>
      </section>
    </div>
  );
}
