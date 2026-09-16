'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { ArrowRight, BadgeCheck, Database, Gauge, Sparkles } from 'lucide-react';
import { getMissionBrief } from '@/lib/api';
import type { MissionBrief } from '@/lib/mission-types';

export default function MissionSpotlight() {
  const [brief, setBrief] = useState<MissionBrief | null>(null);

  useEffect(() => {
    getMissionBrief().then(setBrief);
  }, []);

  if (!brief) {
    return (
      <section className="bc-surface rounded-[28px] p-5 sm:p-6">
        <div className="h-5 w-40 animate-pulse rounded-full bg-slate-100" />
        <div className="mt-4 h-8 w-3/4 animate-pulse rounded-xl bg-slate-100" />
        <div className="mt-3 h-4 w-1/2 animate-pulse rounded-lg bg-slate-100" />
      </section>
    );
  }

  const impact = brief.impact[0];

  return (
    <section className="overflow-hidden rounded-[30px] border border-blue-900/10 bg-[#e9edff] shadow-[0_18px_55px_rgba(47,92,255,0.08)]">
      <div className="grid gap-0 xl:grid-cols-[1.45fr_0.55fr]">
        <div className="p-5 sm:p-7 lg:p-8">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-blue-300 bg-white/70 px-2.5 py-1 font-mono text-[9px] font-black tracking-[0.12em] text-blue-700"><Sparkles size={10} /> TODAY&apos;S CAMPUS MISSION</span>
            <span className="rounded-full border border-blue-300/60 bg-blue-100/70 px-2.5 py-1 font-mono text-[9px] font-black text-blue-700">{brief.confidence}% CONFIDENCE</span>
          </div>
          <h2 className="mt-5 max-w-4xl text-[30px] font-black leading-[1.02] tracking-[-0.055em] text-[#0a1020] sm:text-[38px]">{brief.title}</h2>
          <p className="mt-3 max-w-3xl text-[12px] leading-relaxed text-slate-600">{brief.one_liner}</p>

          <div className="mt-6 flex flex-wrap gap-2">
            <Link href="/demo" className="bc-focus-ring inline-flex items-center gap-2 rounded-[14px] bg-[#0b1226] px-4 py-3 text-[11px] font-black text-white shadow-[0_10px_28px_rgba(11,18,38,0.15)] transition hover:-translate-y-0.5">
              Run 90-second Jury Mode <ArrowRight size={13} />
            </Link>
            <Link href="/decisions" className="bc-focus-ring inline-flex items-center gap-2 rounded-[14px] border border-blue-900/10 bg-white/75 px-4 py-3 text-[11px] font-black text-blue-900 transition hover:bg-white">
              Open decision receipt
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-2 border-t border-blue-900/10 bg-white/45 xl:grid-cols-1 xl:border-l xl:border-t-0">
          <div className="p-5 sm:p-6">
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500"><Gauge size={12} /> Modeled impact</div>
            <div className="mt-3 font-mono text-3xl font-black tracking-[-0.05em] text-[#0a1020]">{impact ? impact.value.toLocaleString('tr-TR') : '—'} <span className="text-[9px] text-slate-500">{impact?.unit ?? ''}</span></div>
            <p className="mt-2 text-[9px] leading-relaxed text-slate-500">{impact?.note ?? 'No intervention currently exceeds the threshold.'}</p>
          </div>
          <div className="border-l border-blue-900/10 p-5 sm:p-6 xl:border-l-0 xl:border-t">
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500"><Database size={12} /> Evidence</div>
            <div className="mt-3 flex items-end gap-2"><span className="font-mono text-3xl font-black tracking-[-0.05em] text-[#0a1020]">{brief.source_health.passing}/{brief.source_health.total}</span><BadgeCheck size={16} className="mb-1 text-emerald-600" /></div>
            <p className="mt-2 text-[9px] leading-relaxed text-slate-500">Inputs passing source checks. Unavailable sources remain visible rather than being replaced with synthetic live data.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
