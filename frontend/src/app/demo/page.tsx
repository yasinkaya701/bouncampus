'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BadgeCheck,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  CloudRain,
  Database,
  ExternalLink,
  Gauge,
  Play,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  ThermometerSun,
  Zap,
} from 'lucide-react';
import { getMissionBrief, simulateScenario } from '@/lib/api';
import type { MissionBrief } from '@/lib/mission-types';
import type { ScenarioResult } from '@/lib/types';

const steps = [
  { id: 0, label: 'Signal fusion', eyebrow: '01 / SENSE' },
  { id: 1, label: 'Decision', eyebrow: '02 / REASON' },
  { id: 2, label: 'Stress test', eyebrow: '03 / SIMULATE' },
  { id: 3, label: 'Human approval', eyebrow: '04 / ACT' },
];

function sourceTone(ok?: boolean) {
  return ok
    ? 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200'
    : 'border-amber-300/20 bg-amber-300/10 text-amber-200';
}

export default function JuryDemoPage() {
  const [brief, setBrief] = useState<MissionBrief | null>(null);
  const [step, setStep] = useState(0);
  const [scenario, setScenario] = useState<ScenarioResult | null>(null);
  const [scenarioLabel, setScenarioLabel] = useState('');
  const [simulating, setSimulating] = useState(false);
  const [approvedAt, setApprovedAt] = useState<string | null>(null);

  useEffect(() => {
    getMissionBrief().then(setBrief);
  }, []);

  const sourceScore = useMemo(() => {
    if (!brief || !brief.source_health.total) return 0;
    return Math.round((brief.source_health.passing / brief.source_health.total) * 100);
  }, [brief]);

  async function runScenario(type: 'rain' | 'heatwave') {
    setSimulating(true);
    setScenarioLabel(type === 'rain' ? 'Heavy rain' : 'Heatwave 38°C');
    try {
      const result = await simulateScenario({
        scenario_type: type,
        params: type === 'heatwave' ? { temp: 38 } : {},
      });
      setScenario(result);
    } finally {
      setSimulating(false);
    }
  }

  if (!brief) {
    return (
      <div className="grid min-h-[72vh] place-items-center">
        <div className="text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-slate-300 border-t-[#2f5cff]" />
          <div className="mt-4 text-sm font-black text-[#0a1020]">Building today&apos;s campus mission…</div>
          <div className="mt-1 font-mono text-[10px] text-slate-400">fusing public feeds + timetable + transparent models</div>
        </div>
      </div>
    );
  }

  const active = steps[step];
  const primaryImpact = brief.impact[0];

  return (
    <div className="space-y-4 pb-10">
      <section className="relative overflow-hidden rounded-[34px] bg-[#070d1c] px-5 py-6 text-white shadow-[0_28px_90px_rgba(7,13,28,0.28)] sm:px-7 lg:px-10 lg:py-9">
        <div className="pointer-events-none absolute right-[-8rem] top-[-9rem] h-[28rem] w-[28rem] rounded-full bg-blue-500/20 blur-3xl" />
        <div className="pointer-events-none absolute bottom-[-12rem] left-[20%] h-[25rem] w-[25rem] rounded-full bg-emerald-400/10 blur-3xl" />

        <div className="relative flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
          <div className="max-w-4xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full border border-blue-300/20 bg-blue-300/10 px-3 py-1 font-mono text-[9px] font-black tracking-[0.14em] text-blue-200">JURY MODE · 90 SEC</span>
              <span className={`rounded-full border px-3 py-1 font-mono text-[9px] font-black tracking-[0.12em] ${brief.status === 'DEGRADED' ? 'border-amber-300/20 bg-amber-300/10 text-amber-200' : 'border-emerald-300/20 bg-emerald-300/10 text-emerald-200'}`}>{brief.status}</span>
            </div>
            <h1 className="mt-6 max-w-4xl text-[40px] font-black leading-[0.95] tracking-[-0.065em] sm:text-[54px] lg:text-[68px]">
              Boğaziçi&apos;nin verisi var.
              <span className="block text-blue-300">Eksik olan karar katmanı.</span>
            </h1>
            <p className="mt-5 max-w-2xl text-sm leading-relaxed text-slate-400 sm:text-[15px]">
              BOUNCAMPUS, birbirinden kopuk public kampüs sinyallerini tek bir doğrulanabilir operasyona dönüştürür. Sensör uydurmaz; ne bildiğini, ne tahmin ettiğini ve neyin insan onayı beklediğini açıkça gösterir.
            </p>
          </div>

          <div className="grid min-w-[280px] grid-cols-3 gap-2">
            <div className="rounded-[20px] border border-white/10 bg-white/[0.05] p-4">
              <div className="font-mono text-3xl font-black tracking-[-0.05em] text-white">{brief.source_health.passing}/{brief.source_health.total}</div>
              <div className="mt-1 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">inputs ready</div>
            </div>
            <div className="rounded-[20px] border border-white/10 bg-white/[0.05] p-4">
              <div className="font-mono text-3xl font-black tracking-[-0.05em] text-blue-300">{brief.confidence}%</div>
              <div className="mt-1 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">confidence</div>
            </div>
            <div className="rounded-[20px] border border-white/10 bg-white/[0.05] p-4">
              <div className="font-mono text-3xl font-black tracking-[-0.05em] text-emerald-300">{brief.dashboard.actions.length}</div>
              <div className="mt-1 text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">candidates</div>
            </div>
          </div>
        </div>
      </section>

      <section className="bc-surface rounded-[26px] p-2 sm:p-3">
        <div className="grid grid-cols-2 gap-2 lg:grid-cols-4">
          {steps.map(item => {
            const selected = step === item.id;
            const done = step > item.id;
            return (
              <button key={item.id} type="button" onClick={() => setStep(item.id)} className={`bc-focus-ring rounded-[20px] px-4 py-4 text-left transition ${selected ? 'bg-[#0b1226] text-white shadow-[0_12px_32px_rgba(11,18,38,0.16)]' : 'bg-transparent text-slate-600 hover:bg-[#f4f5f2]'}`}>
                <div className={`font-mono text-[9px] font-black tracking-[0.14em] ${selected ? 'text-blue-300' : done ? 'text-emerald-600' : 'text-slate-400'}`}>{done ? '✓ COMPLETE' : item.eyebrow}</div>
                <div className="mt-2 text-sm font-black tracking-[-0.02em]">{item.label}</div>
              </button>
            );
          })}
        </div>
      </section>

      <section className="min-h-[570px] overflow-hidden rounded-[30px] border border-slate-950/10 bg-white shadow-[0_18px_60px_rgba(10,16,32,0.06)]">
        <div className="border-b border-slate-950/8 px-5 py-4 sm:px-7">
          <div className="flex items-center justify-between gap-4">
            <div>
              <div className="bc-eyebrow">{active.eyebrow}</div>
              <h2 className="mt-1 text-xl font-black tracking-[-0.04em] text-[#0a1020]">{active.label}</h2>
            </div>
            <div className="hidden items-center gap-2 sm:flex">
              <button type="button" onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0} className="bc-focus-ring grid h-9 w-9 place-items-center rounded-full border border-slate-950/10 text-slate-500 disabled:opacity-30"><ChevronLeft size={15} /></button>
              <button type="button" onClick={() => setStep(Math.min(steps.length - 1, step + 1))} disabled={step === steps.length - 1} className="bc-focus-ring grid h-9 w-9 place-items-center rounded-full bg-[#0b1226] text-white disabled:opacity-30"><ChevronRight size={15} /></button>
            </div>
          </div>
        </div>

        {step === 0 && (
          <div className="grid gap-6 p-5 sm:p-7 xl:grid-cols-[0.8fr_1.2fr]">
            <div className="rounded-[26px] bg-[#0b1226] p-6 text-white">
              <div className="flex items-center gap-2 text-blue-300"><Database size={16} /><span className="text-[10px] font-black uppercase tracking-[0.15em]">Signal fusion</span></div>
              <h3 className="mt-5 text-3xl font-black leading-[1.02] tracking-[-0.05em]">Four public signals become one operational context.</h3>
              <p className="mt-4 text-xs leading-relaxed text-slate-400">Instead of another campus dashboard, BOUNCAMPUS asks a harder question: what should an operator do differently because these signals changed today?</p>
              <div className="mt-7 rounded-[20px] border border-white/10 bg-white/[0.04] p-4">
                <div className="flex items-center justify-between"><span className="text-[10px] font-bold text-slate-400">Source readiness</span><span className="font-mono text-sm font-black text-emerald-300">{sourceScore}%</span></div>
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10"><div className="h-full rounded-full bg-emerald-400" style={{ width: `${sourceScore}%` }} /></div>
                <div className="mt-3 text-[9px] leading-relaxed text-slate-500">Healthy upstream sources increase mission confidence; unavailable inputs remain visible instead of being replaced with fake live values.</div>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              {brief.evidence.map((item, index) => (
                <article key={item.id} className="rounded-[24px] border border-slate-950/10 bg-[#f7f8f5] p-5">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-mono text-[9px] font-black text-slate-400">SIGNAL {String(index + 1).padStart(2, '0')}</span>
                    <span className={`rounded-full border px-2 py-1 font-mono text-[8px] font-black ${item.source?.ok ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-amber-200 bg-amber-50 text-amber-700'}`}>{item.source?.ok ? item.source.provenance : 'UNAVAILABLE'}</span>
                  </div>
                  <div className="mt-5 text-[11px] font-black uppercase tracking-[0.1em] text-slate-500">{item.label}</div>
                  <div className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">{item.value}</div>
                  <p className="mt-3 text-[10px] leading-relaxed text-slate-500">{item.interpretation}</p>
                  {item.source?.url && item.source.url !== '/' && (
                    <a href={item.source.url} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-1 text-[9px] font-black text-blue-600">Open source <ExternalLink size={10} /></a>
                  )}
                </article>
              ))}
            </div>
          </div>
        )}

        {step === 1 && (
          <div className="grid gap-5 p-5 sm:p-7 xl:grid-cols-[1.2fr_0.8fr]">
            <div className="rounded-[28px] bg-[#0b1226] p-6 text-white sm:p-8">
              <div className="flex flex-wrap items-center gap-2"><span className="rounded-full border border-blue-300/20 bg-blue-300/10 px-2.5 py-1 font-mono text-[8px] font-black text-blue-200">MISSION {brief.decision_id ?? 'WATCH'}</span><span className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 font-mono text-[8px] font-black text-slate-300">{brief.confidence_label} CONFIDENCE</span></div>
              <h3 className="mt-6 max-w-3xl text-[36px] font-black leading-[0.98] tracking-[-0.055em] sm:text-[46px]">{brief.title}</h3>
              <p className="mt-5 max-w-2xl text-sm leading-relaxed text-slate-400">{brief.one_liner}</p>
              <div className="mt-7 grid gap-3 sm:grid-cols-2">
                <div className="rounded-[20px] border border-white/10 bg-white/[0.04] p-4"><div className="text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">Where</div><div className="mt-2 text-sm font-black">{brief.location}</div></div>
                <div className="rounded-[20px] border border-white/10 bg-white/[0.04] p-4"><div className="text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">When</div><div className="mt-2 text-sm font-black">{brief.operating_window}</div></div>
              </div>
              <div className="mt-4 rounded-[20px] border border-blue-300/15 bg-blue-300/[0.06] p-5"><div className="text-[9px] font-black uppercase tracking-[0.13em] text-blue-300">Why now</div><p className="mt-2 text-xs leading-relaxed text-slate-300">{brief.why_now}</p></div>
            </div>

            <div className="space-y-3">
              <div className="bc-surface rounded-[24px] p-5"><div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.12em] text-slate-500"><Gauge size={13} /> Decision confidence</div><div className="mt-4 flex items-end justify-between"><div className="font-mono text-5xl font-black tracking-[-0.06em] text-[#0a1020]">{brief.confidence}<span className="text-lg text-slate-400">%</span></div><span className="rounded-full bg-blue-50 px-2.5 py-1 text-[9px] font-black text-blue-700">{brief.confidence_label}</span></div><div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[#2f5cff]" style={{ width: `${brief.confidence}%` }} /></div></div>
              {brief.impact.map(item => (
                <div key={item.label} className="bc-surface rounded-[24px] p-5"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{item.label}</div><div className="mt-2 font-mono text-3xl font-black tracking-[-0.05em] text-[#0a1020]">{item.value.toLocaleString('tr-TR')} <span className="text-[10px] text-slate-500">{item.unit}</span></div><p className="mt-2 text-[9px] leading-relaxed text-slate-500">{item.note}</p></div>
              ))}
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="grid gap-6 p-5 sm:p-7 xl:grid-cols-[0.72fr_1.28fr]">
            <div>
              <div className="bc-eyebrow">Break the recommendation before reality does</div>
              <h3 className="mt-2 text-3xl font-black leading-tight tracking-[-0.05em] text-[#0a1020]">Stress-test the same decision under a different campus condition.</h3>
              <p className="mt-3 text-xs leading-relaxed text-slate-500">The counterfactual starts from the current dashboard state. Nothing is sent to campus infrastructure.</p>
              <div className="mt-6 grid gap-2">
                <button type="button" onClick={() => runScenario('rain')} disabled={simulating} className="bc-focus-ring flex items-center justify-between rounded-[18px] border border-slate-950/10 bg-white px-4 py-4 text-left transition hover:border-blue-300 hover:bg-blue-50/40 disabled:opacity-50"><span className="flex items-center gap-3"><span className="grid h-9 w-9 place-items-center rounded-[12px] bg-blue-50 text-blue-600"><CloudRain size={16} /></span><span><span className="block text-xs font-black text-[#0a1020]">Heavy rain</span><span className="mt-0.5 block text-[9px] text-slate-500">Indoor + cafeteria pressure</span></span></span><Play size={13} /></button>
                <button type="button" onClick={() => runScenario('heatwave')} disabled={simulating} className="bc-focus-ring flex items-center justify-between rounded-[18px] border border-slate-950/10 bg-white px-4 py-4 text-left transition hover:border-amber-300 hover:bg-amber-50/40 disabled:opacity-50"><span className="flex items-center gap-3"><span className="grid h-9 w-9 place-items-center rounded-[12px] bg-amber-50 text-amber-600"><ThermometerSun size={16} /></span><span><span className="block text-xs font-black text-[#0a1020]">Heatwave 38°C</span><span className="mt-0.5 block text-[9px] text-slate-500">Cooling-load stress</span></span></span><Play size={13} /></button>
              </div>
            </div>

            <div className="rounded-[28px] bg-[#0b1226] p-6 text-white sm:p-7">
              {!scenario ? (
                <div className="grid min-h-[370px] place-items-center text-center"><div><span className="mx-auto grid h-14 w-14 place-items-center rounded-[20px] border border-white/10 bg-white/[0.05] text-blue-300"><Sparkles size={22} /></span><h4 className="mt-5 text-xl font-black">Choose a shock</h4><p className="mx-auto mt-2 max-w-sm text-[11px] leading-relaxed text-slate-400">BOUNCAMPUS will recompute energy, food and impact from the live product baseline instead of switching to a canned demo result.</p></div></div>
              ) : (
                <div>
                  <div className="flex items-center justify-between"><div><div className="text-[9px] font-black uppercase tracking-[0.14em] text-blue-300">COUNTERFACTUAL RESULT</div><div className="mt-1 text-lg font-black">{scenarioLabel}</div></div><button type="button" onClick={() => setScenario(null)} className="grid h-9 w-9 place-items-center rounded-full border border-white/10 text-slate-400"><RotateCcw size={14} /></button></div>
                  <div className="mt-6 grid gap-3 sm:grid-cols-2">
                    {[
                      ['Energy demand', scenario.original.predicted_energy_mwh, scenario.modified.predicted_energy_mwh, 'MWh'],
                      ['Food demand', scenario.original.food_demand_meals, scenario.modified.food_demand_meals, 'meals'],
                      ['Cost potential', scenario.original.potential_saving_tl, scenario.modified.potential_saving_tl, 'TL'],
                      ['CO₂ potential', scenario.original.co2_avoided_kg, scenario.modified.co2_avoided_kg, 'kg'],
                    ].map(([label, before, after, unit]) => {
                      const b = Number(before); const a = Number(after); const delta = a - b;
                      return <div key={String(label)} className="rounded-[20px] border border-white/10 bg-white/[0.04] p-4"><div className="text-[9px] font-black uppercase tracking-[0.1em] text-slate-500">{label}</div><div className="mt-3 flex items-baseline gap-2"><span className="font-mono text-2xl font-black">{a.toLocaleString('tr-TR')}</span><span className="text-[9px] text-slate-500">{unit}</span></div><div className={`mt-2 font-mono text-[10px] font-black ${delta > 0 ? 'text-amber-300' : delta < 0 ? 'text-emerald-300' : 'text-slate-500'}`}>{delta > 0 ? '+' : ''}{delta.toLocaleString('tr-TR')} vs baseline</div></div>;
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="grid gap-6 p-5 sm:p-7 xl:grid-cols-[1fr_0.78fr]">
            <div className="rounded-[28px] bg-[#0b1226] p-6 text-white sm:p-8">
              <div className="flex items-center gap-2 text-emerald-300"><ShieldCheck size={16} /><span className="text-[10px] font-black uppercase tracking-[0.14em]">Human-in-the-loop boundary</span></div>
              <h3 className="mt-5 text-4xl font-black leading-[1] tracking-[-0.055em]">The model recommends.<br />A person remains accountable.</h3>
              <p className="mt-5 max-w-2xl text-sm leading-relaxed text-slate-400">{brief.guardrail}</p>
              <div className="mt-7 rounded-[22px] border border-white/10 bg-white/[0.04] p-5"><div className="text-[9px] font-black uppercase tracking-[0.13em] text-slate-500">Decision receipt</div><div className="mt-3 text-lg font-black">{brief.recommendation}</div><div className="mt-4 grid gap-2 text-[10px] text-slate-400 sm:grid-cols-3"><div><span className="block text-slate-600">Location</span><strong className="text-slate-300">{brief.location}</strong></div><div><span className="block text-slate-600">Window</span><strong className="text-slate-300">{brief.operating_window}</strong></div><div><span className="block text-slate-600">Confidence</span><strong className="text-slate-300">{brief.confidence}%</strong></div></div></div>
            </div>

            <div className="bc-surface flex flex-col justify-between rounded-[28px] p-6">
              <div>
                <div className="bc-eyebrow">Demo review state</div>
                {!approvedAt ? (
                  <><h3 className="mt-2 text-2xl font-black tracking-[-0.04em] text-[#0a1020]">Ready for a human decision.</h3><p className="mt-3 text-[11px] leading-relaxed text-slate-500">Approving here records a browser-only demo review. It does not dispatch a campus command.</p></>
                ) : (
                  <><span className="mt-3 grid h-12 w-12 place-items-center rounded-[18px] bg-emerald-50 text-emerald-600"><BadgeCheck size={23} /></span><h3 className="mt-4 text-2xl font-black tracking-[-0.04em] text-[#0a1020]">Approved for pilot review.</h3><p className="mt-3 text-[11px] leading-relaxed text-slate-500">Decision receipt created at {approvedAt}. Next step in a real deployment would be field verification and outcome measurement.</p></>
                )}
              </div>
              <div className="mt-8 space-y-2">
                {!approvedAt ? <button type="button" onClick={() => setApprovedAt(new Intl.DateTimeFormat('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: 'Europe/Istanbul' }).format(new Date()))} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-[16px] bg-[#2f5cff] px-4 py-3.5 text-[11px] font-black text-white shadow-[0_12px_28px_rgba(47,92,255,0.20)]"><CheckCircle2 size={14} /> Approve for pilot review</button> : <button type="button" onClick={() => setApprovedAt(null)} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-[16px] border border-slate-950/10 bg-white px-4 py-3.5 text-[11px] font-black text-slate-700"><RotateCcw size={13} /> Reset demo approval</button>}
                <Link href="/decisions" className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-[16px] border border-slate-950/10 bg-[#f4f5f2] px-4 py-3.5 text-[11px] font-black text-slate-700">Open decision workspace <ArrowRight size={13} /></Link>
              </div>
            </div>
          </div>
        )}
      </section>

      <section className="flex flex-col gap-3 rounded-[26px] bg-[#e9edff] px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-7">
        <div><div className="text-[9px] font-black uppercase tracking-[0.14em] text-blue-700">THE PITCH IN ONE LINE</div><div className="mt-1 text-sm font-black tracking-[-0.02em] text-[#0a1020]">BOUNCAMPUS is the decision layer between campus public data and real operations.</div></div>
        <div className="flex flex-wrap gap-2"><Link href="/data" className="rounded-full border border-blue-900/10 bg-white px-3 py-2 text-[10px] font-black text-blue-800">Audit every source</Link><Link href="/scenarios" className="rounded-full bg-[#0b1226] px-3 py-2 text-[10px] font-black text-white">Open full simulator</Link></div>
      </section>
    </div>
  );
}
