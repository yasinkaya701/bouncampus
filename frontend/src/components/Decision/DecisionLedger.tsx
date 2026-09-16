'use client';

import { useEffect, useMemo, useState } from 'react';
import { Check, CheckCircle2, Clock3, RotateCcw, ShieldCheck, X } from 'lucide-react';
import type { ActionItem } from '@/lib/types';

type DecisionState = 'REVIEW' | 'APPROVED_FOR_PILOT' | 'DECLINED';

type LedgerEntry = {
  state: DecisionState;
  updatedAt: string;
};

const STORAGE_KEY = 'bouncampus-decision-ledger-v1';

function stateTone(state: DecisionState) {
  if (state === 'APPROVED_FOR_PILOT') return 'border-emerald-200 bg-emerald-50 text-emerald-700';
  if (state === 'DECLINED') return 'border-rose-200 bg-rose-50 text-rose-700';
  return 'border-amber-200 bg-amber-50 text-amber-700';
}

export default function DecisionLedger({ actions }: { actions: ActionItem[] }) {
  const [ledger, setLedger] = useState<Record<string, LedgerEntry>>({});

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored) setLedger(JSON.parse(stored));
    } catch {
      // Browser storage is optional; decision recommendations still render without it.
    }
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ledger));
    } catch {
      // Ignore storage failures in private browsing / restricted environments.
    }
  }, [ledger]);

  const counts = useMemo(() => {
    return actions.reduce((acc, action) => {
      const state = ledger[action.id]?.state ?? 'REVIEW';
      acc[state] += 1;
      return acc;
    }, { REVIEW: 0, APPROVED_FOR_PILOT: 0, DECLINED: 0 });
  }, [actions, ledger]);

  function update(actionId: string, state: DecisionState) {
    const updatedAt = new Intl.DateTimeFormat('tr-TR', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: 'Europe/Istanbul',
    }).format(new Date());
    setLedger(current => ({ ...current, [actionId]: { state, updatedAt } }));
  }

  function reset() {
    setLedger({});
  }

  if (!actions.length) {
    return (
      <div className="bc-surface rounded-[24px] p-8 text-center">
        <CheckCircle2 size={25} className="mx-auto text-emerald-600" />
        <h3 className="mt-3 text-sm font-black text-[#0a1020]">No decision candidates above threshold</h3>
        <p className="mt-1 text-[11px] text-slate-500">The product stays quiet instead of fabricating an intervention.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-2 sm:grid-cols-3">
        {[
          ['Awaiting review', counts.REVIEW, 'text-amber-700 bg-amber-50'],
          ['Pilot approved', counts.APPROVED_FOR_PILOT, 'text-emerald-700 bg-emerald-50'],
          ['Declined', counts.DECLINED, 'text-rose-700 bg-rose-50'],
        ].map(([label, value, tone]) => (
          <div key={String(label)} className={`rounded-[18px] border border-slate-950/8 p-4 ${tone}`}>
            <div className="font-mono text-2xl font-black tracking-[-0.04em]">{value}</div>
            <div className="mt-1 text-[9px] font-black uppercase tracking-[0.12em] opacity-70">{label}</div>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        {actions.map(action => {
          const entry = ledger[action.id] ?? { state: 'REVIEW' as DecisionState, updatedAt: '' };
          return (
            <article key={action.id} className="overflow-hidden rounded-[24px] border border-slate-950/10 bg-white shadow-[0_12px_35px_rgba(10,16,32,0.04)]">
              <div className="grid gap-0 xl:grid-cols-[1fr_270px]">
                <div className="p-5 sm:p-6">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`rounded-full border px-2.5 py-1 font-mono text-[8px] font-black ${stateTone(entry.state)}`}>{entry.state.replaceAll('_', ' ')}</span>
                    <span className="rounded-full border border-violet-200 bg-violet-50 px-2.5 py-1 font-mono text-[8px] font-black text-violet-700">{action.provenance ?? 'MODEL_ESTIMATE'}</span>
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 font-mono text-[8px] font-black text-slate-500">{action.priority}</span>
                  </div>
                  <h3 className="mt-4 text-xl font-black tracking-[-0.035em] text-[#0a1020]">{action.title}</h3>
                  <p className="mt-2 max-w-4xl text-[11px] leading-relaxed text-slate-500">{action.description}</p>
                  <div className="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-[9px] font-bold text-slate-500">
                    <span className="inline-flex items-center gap-1.5"><Clock3 size={11} /> {action.time}</span>
                    <span>{action.location}</span>
                    <span className="font-mono font-black text-emerald-700">{action.impact_value.toLocaleString('tr-TR')} {action.impact_unit}</span>
                  </div>
                  {entry.updatedAt && <div className="mt-4 text-[8px] font-mono uppercase tracking-[0.1em] text-slate-400">Local demo ledger updated {entry.updatedAt}</div>}
                </div>

                <div className="border-t border-slate-950/8 bg-[#f7f8f5] p-4 xl:border-l xl:border-t-0">
                  <div className="flex h-full flex-col justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.12em] text-slate-500"><ShieldCheck size={12} /> Human gate</div>
                      <p className="mt-2 text-[9px] leading-relaxed text-slate-500">This changes only the browser demo ledger. No BMS, kitchen or transport command is sent.</p>
                    </div>
                    <div className="grid gap-2">
                      <button type="button" onClick={() => update(action.id, 'APPROVED_FOR_PILOT')} className="bc-focus-ring flex items-center justify-center gap-2 rounded-[13px] bg-[#0b1226] px-3 py-2.5 text-[10px] font-black text-white"><Check size={12} /> Approve for pilot</button>
                      <button type="button" onClick={() => update(action.id, 'DECLINED')} className="bc-focus-ring flex items-center justify-center gap-2 rounded-[13px] border border-slate-950/10 bg-white px-3 py-2.5 text-[10px] font-black text-slate-600"><X size={12} /> Decline</button>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          );
        })}
      </div>

      <button type="button" onClick={reset} className="bc-focus-ring inline-flex items-center gap-1.5 rounded-full border border-slate-950/10 bg-white px-3 py-2 text-[9px] font-black text-slate-500"><RotateCcw size={11} /> Reset local demo ledger</button>
    </div>
  );
}
