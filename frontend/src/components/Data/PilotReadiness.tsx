import Link from 'next/link';
import { ArrowRight, CheckCircle2, LockKeyhole, PlugZap, Radar, Target } from 'lucide-react';

const integrations = [
  {
    name: 'Anonymous occupancy aggregates',
    source: 'Wi‑Fi AP / turnstile / room counter',
    priority: 'P0',
    unlock: 'Calibrate schedule-derived occupancy and measure space-consolidation accuracy.',
    privacy: 'Aggregate counts only; no MAC addresses, device IDs or individual trajectories.',
  },
  {
    name: 'Building smart-meter / BMS totals',
    source: 'Hourly building or floor energy',
    priority: 'P0',
    unlock: 'Turn modeled savings into measured baseline-vs-pilot evidence.',
    privacy: 'Operational telemetry only; read-only integration first.',
  },
  {
    name: 'Cafeteria POS totals',
    source: '15–30 minute anonymized sales buckets',
    priority: 'P1',
    unlock: 'Calibrate lunch-demand forecasts and quantify overproduction reduction.',
    privacy: 'No student IDs, payment identifiers or basket-level personal history.',
  },
  {
    name: 'Shuttle AVL / GPS',
    source: 'Vehicle location and route status',
    priority: 'P1',
    unlock: 'Upgrade published timetable context into arrival reliability and mobility decisions.',
    privacy: 'Vehicle-level telemetry; no passenger identity required.',
  },
];

const phases = [
  ['Week 1', 'Read-only integration', 'Connect aggregate feeds behind the same provenance contract. No automatic control.'],
  ['Week 2', 'Calibration', 'Compare BOUNCAMPUS estimates with measured occupancy, energy and demand.'],
  ['Week 3', 'Operator pilot', 'Run a small number of human-approved decisions with clear rollback criteria.'],
  ['Week 4', 'Outcome proof', 'Capture realized impact, model error and operator feedback in the decision ledger.'],
];

const successGates = [
  {
    metric: 'Occupancy model error',
    target: '≤ 20% MAPE',
    evidence: 'Aggregate measured occupancy vs schedule-derived utilization during pilot windows.',
  },
  {
    metric: 'Energy intervention',
    target: 'Measured positive savings',
    evidence: 'Weather-normalized smart-meter baseline vs human-approved consolidation pilot.',
  },
  {
    metric: 'Food-demand model',
    target: '≤ 15% MAPE',
    evidence: 'Predicted lunch demand vs anonymized POS totals by time bucket.',
  },
  {
    metric: 'Operator usefulness',
    target: '≥ 70% accepted/useful',
    evidence: 'Decision-ledger review outcome and short operator feedback for surfaced missions.',
  },
];

export default function PilotReadiness() {
  return (
    <section className="space-y-4">
      <div className="overflow-hidden rounded-[30px] border border-blue-900/10 bg-[#e9edff]">
        <div className="grid lg:grid-cols-[1fr_360px]">
          <div className="p-6 sm:p-7 lg:p-8">
            <div className="flex items-center gap-2 text-blue-700"><PlugZap size={15} /><span className="text-[9px] font-black uppercase tracking-[0.14em]">Pilot readiness</span></div>
            <h2 className="mt-4 max-w-4xl text-3xl font-black leading-[1.02] tracking-[-0.05em] text-[#0a1020] sm:text-4xl">The hackathon build already has the decision layer. A real pilot only needs read-only calibration feeds.</h2>
            <p className="mt-4 max-w-3xl text-[12px] leading-relaxed text-slate-600">The architecture does not depend on replacing university systems. BOUNCAMPUS sits above existing sources, keeps provenance intact, and can start with aggregate data before any control integration is considered.</p>
          </div>
          <div className="grid grid-cols-2 border-t border-blue-900/10 bg-white/45 lg:grid-cols-1 lg:border-l lg:border-t-0">
            <div className="p-5 sm:p-6"><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500"><Radar size={12} /> Today</div><div className="mt-2 text-2xl font-black tracking-[-0.04em] text-[#0a1020]">Public-data mission control</div><p className="mt-2 text-[9px] leading-relaxed text-slate-500">Source-traceable decisions, counterfactuals, human approval and outcome capture.</p></div>
            <div className="border-l border-blue-900/10 p-5 sm:p-6 lg:border-l-0 lg:border-t"><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500"><Target size={12} /> Pilot target</div><div className="mt-2 text-2xl font-black tracking-[-0.04em] text-[#0a1020]">Measured decision accuracy</div><p className="mt-2 text-[9px] leading-relaxed text-slate-500">Replace assumptions with aggregate operational evidence, one adapter at a time.</p></div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="bc-eyebrow">Integration backlog</div>
          <h3 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Four feeds unlock a production pilot</h3>
          <div className="mt-5 space-y-2">
            {integrations.map(item => (
              <article key={item.name} className="rounded-[20px] border border-slate-950/8 bg-[#f7f8f5] p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div><div className="text-sm font-black tracking-[-0.02em] text-[#0a1020]">{item.name}</div><div className="mt-1 font-mono text-[9px] text-slate-400">{item.source}</div></div>
                  <span className="rounded-full border border-blue-200 bg-blue-50 px-2 py-1 font-mono text-[8px] font-black text-blue-700">{item.priority}</span>
                </div>
                <div className="mt-3 grid gap-3 md:grid-cols-2">
                  <p className="text-[10px] leading-relaxed text-slate-600"><strong className="text-slate-800">Unlock:</strong> {item.unlock}</p>
                  <p className="text-[10px] leading-relaxed text-slate-500"><strong className="text-slate-700">Privacy:</strong> {item.privacy}</p>
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <div className="bc-surface-dark rounded-[28px] p-5 text-white sm:p-6">
            <div className="flex items-center gap-2 text-emerald-300"><LockKeyhole size={14} /><span className="text-[9px] font-black uppercase tracking-[0.13em]">Privacy-safe by default</span></div>
            <h3 className="mt-4 text-2xl font-black tracking-[-0.04em]">No identity is required to optimize a building.</h3>
            <div className="mt-5 space-y-3">
              {['Aggregate counts before individual records', 'Read-only integrations before control', 'No raw student identifiers in the decision layer', 'Every adapter inherits provenance + freshness metadata'].map(item => (
                <div key={item} className="flex gap-2 text-[10px] leading-relaxed text-slate-400"><CheckCircle2 size={12} className="mt-0.5 shrink-0 text-emerald-300" />{item}</div>
              ))}
            </div>
          </div>

          <div className="bc-surface rounded-[28px] p-5 sm:p-6">
            <div className="bc-eyebrow">30-day university pilot</div>
            <div className="mt-4 space-y-4">
              {phases.map(([week, title, note], index) => (
                <div key={week} className="flex gap-3">
                  <div className="flex flex-col items-center"><span className="grid h-7 w-7 place-items-center rounded-full bg-[#0b1226] font-mono text-[8px] font-black text-white">{index + 1}</span>{index < phases.length - 1 && <span className="mt-1 h-full w-px bg-slate-200" />}</div>
                  <div className="pb-2"><div className="font-mono text-[8px] font-black uppercase tracking-[0.1em] text-blue-600">{week}</div><div className="mt-1 text-xs font-black text-[#0a1020]">{title}</div><p className="mt-1 text-[9px] leading-relaxed text-slate-500">{note}</p></div>
                </div>
              ))}
            </div>
            <Link href="/demo" className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-black text-blue-700">See the full decision loop <ArrowRight size={11} /></Link>
          </div>
        </div>
      </div>

      <div className="bc-surface rounded-[28px] p-5 sm:p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="bc-eyebrow">Pilot success gates</div>
            <h3 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Winning the pilot means beating measurable thresholds.</h3>
            <p className="mt-2 max-w-3xl text-[10px] leading-relaxed text-slate-500">These are proposed validation targets for a university pilot, not claimed current performance. They turn the next phase into a falsifiable experiment instead of a vague deployment promise.</p>
          </div>
          <span className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 font-mono text-[9px] font-black text-emerald-700">MEASURE → ACCEPT / REJECT</span>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {successGates.map(gate => (
            <article key={gate.metric} className="rounded-[20px] border border-slate-950/8 bg-[#f7f8f5] p-4">
              <div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{gate.metric}</div>
              <div className="mt-2 font-mono text-xl font-black tracking-[-0.035em] text-[#0a1020]">{gate.target}</div>
              <p className="mt-3 text-[9px] leading-relaxed text-slate-500">{gate.evidence}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
