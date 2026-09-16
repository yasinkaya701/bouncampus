'use client';

import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, FlaskConical, RotateCcw, Target } from 'lucide-react';
import type { ActionItem } from '@/lib/types';

type OutcomeRecord = {
  actionId: string;
  observed: number;
  recordedAt: string;
};

const STORAGE_KEY = 'bouncampus-outcome-loop-v1';

export default function OutcomeLoop({ actions }: { actions: ActionItem[] }) {
  const [selectedId, setSelectedId] = useState(actions[0]?.id ?? '');
  const [observedInput, setObservedInput] = useState('');
  const [records, setRecords] = useState<Record<string, OutcomeRecord>>({});

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored) setRecords(JSON.parse(stored));
    } catch {
      // Calibration demo remains optional when browser storage is unavailable.
    }
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    } catch {
      // Ignore restricted storage environments.
    }
  }, [records]);

  const action = useMemo(() => actions.find(item => item.id === selectedId) ?? actions[0], [actions, selectedId]);
  const record = action ? records[action.id] : undefined;
  const errorPct = action && record && action.impact_value !== 0
    ? Math.round(((record.observed - action.impact_value) / action.impact_value) * 100)
    : null;

  function recordOutcome() {
    if (!action) return;
    const observed = Number(observedInput);
    if (!Number.isFinite(observed)) return;
    const recordedAt = new Intl.DateTimeFormat('tr-TR', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Istanbul',
    }).format(new Date());
    setRecords(current => ({ ...current, [action.id]: { actionId: action.id, observed, recordedAt } }));
    setObservedInput('');
  }

  function reset() {
    setRecords({});
    setObservedInput('');
  }

  if (!actions.length) return null;

  return (
    <section className="overflow-hidden rounded-[28px] border border-slate-950/10 bg-white shadow-[0_16px_45px_rgba(10,16,32,0.05)]">
      <div className="grid xl:grid-cols-[0.72fr_1.28fr]">
        <div className="bg-[#0b1226] p-6 text-white sm:p-7">
          <div className="flex items-center gap-2 text-emerald-300"><Target size={15} /><span className="text-[9px] font-black uppercase tracking-[0.14em]">Closed learning loop</span></div>
          <h3 className="mt-4 text-3xl font-black leading-[1.02] tracking-[-0.05em]">A pilot is only useful if the model learns from reality.</h3>
          <p className="mt-4 text-[11px] leading-relaxed text-slate-400">After a real pilot, an operator can enter the observed outcome and compare it with the modeled potential. In this hackathon build the record stays in the browser; in production it becomes calibration evidence.</p>
          <div className="mt-6 rounded-[20px] border border-white/10 bg-white/[0.04] p-4">
            <div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-500">Product loop</div>
            <div className="mt-3 flex flex-wrap items-center gap-2 text-[10px] font-black text-slate-300">
              <span className="rounded-full bg-white/5 px-3 py-1.5">Sense</span><ArrowRight size={11} className="text-slate-600" />
              <span className="rounded-full bg-white/5 px-3 py-1.5">Decide</span><ArrowRight size={11} className="text-slate-600" />
              <span className="rounded-full bg-white/5 px-3 py-1.5">Pilot</span><ArrowRight size={11} className="text-slate-600" />
              <span className="rounded-full bg-emerald-300/10 px-3 py-1.5 text-emerald-300">Learn</span>
            </div>
          </div>
        </div>

        <div className="p-5 sm:p-7">
          <div className="grid gap-4 lg:grid-cols-[1fr_0.7fr]">
            <div>
              <div className="bc-eyebrow">Outcome capture</div>
              <label className="mt-3 block text-[10px] font-black text-slate-600">Decision candidate</label>
              <select value={action?.id ?? ''} onChange={event => setSelectedId(event.target.value)} className="bc-focus-ring mt-2 w-full rounded-[14px] border border-slate-950/10 bg-[#f7f8f5] px-3 py-3 text-[11px] font-bold text-slate-700">
                {actions.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}
              </select>

              {action && (
                <div className="mt-4 rounded-[18px] border border-slate-950/8 bg-[#f7f8f5] p-4">
                  <div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">Modeled potential</div>
                  <div className="mt-2 font-mono text-3xl font-black tracking-[-0.05em] text-[#0a1020]">{action.impact_value.toLocaleString('tr-TR')} <span className="text-[10px] text-slate-500">{action.impact_unit}</span></div>
                  <p className="mt-2 text-[9px] leading-relaxed text-slate-500">This is the pre-pilot model expectation, not a measured outcome.</p>
                </div>
              )}
            </div>

            <div>
              <div className="bc-eyebrow">Observed pilot result</div>
              <input type="number" inputMode="decimal" value={observedInput} onChange={event => setObservedInput(event.target.value)} placeholder="Enter observed value" className="bc-focus-ring mt-3 w-full rounded-[14px] border border-slate-950/10 bg-white px-3 py-3 text-[12px] font-bold text-slate-800 shadow-sm placeholder:text-slate-300" />
              <button type="button" onClick={recordOutcome} disabled={!observedInput || !action} className="bc-focus-ring mt-2 flex w-full items-center justify-center gap-2 rounded-[14px] bg-[#2f5cff] px-3 py-3 text-[10px] font-black text-white disabled:opacity-40"><CheckCircle2 size={13} /> Record demo outcome</button>

              {record && action && (
                <div className="mt-4 rounded-[18px] border border-blue-200 bg-blue-50 p-4">
                  <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.12em] text-blue-700"><FlaskConical size={11} /> Calibration evidence</div>
                  <div className="mt-3 grid grid-cols-2 gap-3">
                    <div><div className="text-[8px] font-bold text-slate-400">Observed</div><div className="mt-1 font-mono text-xl font-black text-[#0a1020]">{record.observed.toLocaleString('tr-TR')}</div></div>
                    <div><div className="text-[8px] font-bold text-slate-400">Model error</div><div className={`mt-1 font-mono text-xl font-black ${errorPct == null ? 'text-slate-500' : Math.abs(errorPct) <= 10 ? 'text-emerald-700' : 'text-amber-700'}`}>{errorPct == null ? '—' : `${errorPct > 0 ? '+' : ''}${errorPct}%`}</div></div>
                  </div>
                  <div className="mt-3 text-[8px] font-mono text-slate-400">Recorded {record.recordedAt} · browser-only demo evidence</div>
                </div>
              )}
            </div>
          </div>

          <button type="button" onClick={reset} className="bc-focus-ring mt-5 inline-flex items-center gap-1.5 rounded-full border border-slate-950/10 bg-white px-3 py-2 text-[9px] font-black text-slate-500"><RotateCcw size={11} /> Reset outcome evidence</button>
        </div>
      </div>
    </section>
  );
}
