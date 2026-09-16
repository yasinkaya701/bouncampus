'use client';

import { useState } from 'react';
import type { LucideIcon } from 'lucide-react';
import { BookOpen, CalendarDays, CloudRain, Play, ShieldAlert, Sun, Thermometer } from 'lucide-react';
import type { ScenarioRequest } from '@/lib/types';

interface SimulatorProps {
  onRunScenario: (request: ScenarioRequest) => void;
  isLoading: boolean;
}

const scenarios: { id: ScenarioRequest['scenario_type']; title: string; subtitle: string; icon: LucideIcon }[] = [
  { id: 'heatwave', title: 'Heatwave', subtitle: 'Cooling demand stress', icon: Thermometer },
  { id: 'exam_week', title: 'Exam week', subtitle: 'Extended building use', icon: BookOpen },
  { id: 'event', title: 'Campus event', subtitle: 'Visitor demand shock', icon: CalendarDays },
  { id: 'rain', title: 'Rain / storm', subtitle: 'Indoor demand shift', icon: CloudRain },
  { id: 'building_closure', title: 'Closure', subtitle: 'Capacity redistribution', icon: ShieldAlert },
  { id: 'summer_school', title: 'Summer school', subtitle: 'Low-density operation', icon: Sun },
];

export default function Simulator({ onRunScenario, isLoading }: SimulatorProps) {
  const [activeScenario, setActiveScenario] = useState<ScenarioRequest['scenario_type']>('heatwave');
  const [temp, setTemp] = useState(35);
  const [eventSize, setEventSize] = useState(500);

  const active = scenarios.find(scenario => scenario.id === activeScenario)!;

  const handleRun = () => {
    onRunScenario({ scenario_type: activeScenario, params: { temp, eventSize } });
  };

  return (
    <div className="bc-surface flex h-full flex-col rounded-[28px] p-4 sm:p-5">
      <div className="border-b border-slate-900/10 pb-4">
        <div className="bc-eyebrow">Scenario controls</div>
        <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Choose the shock.</h2>
        <p className="mt-1 text-[11px] leading-relaxed text-slate-500">Every output is a model counterfactual, not a forecast or operational command.</p>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2">
        {scenarios.map(scenario => {
          const Icon = scenario.icon;
          const selected = activeScenario === scenario.id;
          return (
            <button
              key={scenario.id}
              type="button"
              onClick={() => setActiveScenario(scenario.id)}
              className={`bc-focus-ring rounded-[18px] border p-3 text-left transition ${selected ? 'border-[#0b1226] bg-[#0b1226] text-white shadow-[0_10px_28px_rgba(11,18,38,0.14)]' : 'border-slate-950/10 bg-[#f4f5f2] text-slate-700 hover:bg-white'}`}
            >
              <div className={`grid h-8 w-8 place-items-center rounded-[11px] ${selected ? 'bg-white/10 text-blue-300' : 'bg-white text-slate-500 shadow-sm'}`}><Icon size={14} /></div>
              <div className="mt-3 text-[11px] font-black">{scenario.title}</div>
              <div className={`mt-0.5 text-[9px] leading-snug ${selected ? 'text-slate-400' : 'text-slate-400'}`}>{scenario.subtitle}</div>
            </button>
          );
        })}
      </div>

      <div className="mt-4 flex-1 rounded-[20px] border border-slate-950/10 bg-white p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <div className="bc-eyebrow">Parameters</div>
            <div className="mt-1 text-sm font-black tracking-[-0.02em] text-[#0a1020]">{active.title}</div>
          </div>
          <span className="rounded-full border border-violet-200 bg-violet-50 px-2 py-1 text-[8px] font-black tracking-[0.08em] text-violet-700">MODEL INPUT</span>
        </div>

        {activeScenario === 'heatwave' && (
          <div className="mt-7">
            <div className="flex items-end justify-between"><label className="text-[10px] font-bold text-slate-500">Outside temperature</label><span className="font-mono text-2xl font-black tracking-[-0.04em] text-[#0a1020]">{temp}°C</span></div>
            <input type="range" min="20" max="45" value={temp} onChange={event => setTemp(Number(event.target.value))} className="mt-4 w-full accent-[#2f5cff]" />
            <div className="mt-1 flex justify-between font-mono text-[8px] text-slate-400"><span>20°C</span><span>45°C</span></div>
          </div>
        )}

        {activeScenario === 'event' && (
          <div className="mt-7">
            <label className="text-[10px] font-bold text-slate-500">Additional campus visitors</label>
            <select value={eventSize} onChange={event => setEventSize(Number(event.target.value))} className="bc-focus-ring mt-3 w-full rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] px-3 py-3 text-[11px] font-black text-slate-700">
              <option value={500}>+500 people</option><option value={1000}>+1,000 people</option><option value={2000}>+2,000 people</option>
            </select>
          </div>
        )}

        {!['heatwave', 'event'].includes(activeScenario) && (
          <div className="mt-7 rounded-[15px] bg-[#f4f5f2] p-4 text-[10px] leading-relaxed text-slate-500">Standard scenario parameters are applied by the model. No campus system is modified.</div>
        )}
      </div>

      <button type="button" onClick={handleRun} disabled={isLoading} className="bc-focus-ring mt-4 flex w-full items-center justify-center gap-2 rounded-[16px] bg-[#2f5cff] px-4 py-3.5 text-[11px] font-black text-white shadow-[0_10px_26px_rgba(47,92,255,0.20)] transition hover:bg-blue-700 disabled:cursor-wait disabled:opacity-60">
        {isLoading ? <><span className="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white" /> Running model…</> : <><Play size={13} fill="currentColor" /> Run counterfactual</>}
      </button>
    </div>
  );
}
