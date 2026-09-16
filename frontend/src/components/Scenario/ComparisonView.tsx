import { ArrowDownRight, ArrowRight, ArrowUpRight, BarChart3, Sparkles } from 'lucide-react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { ScenarioResult } from '@/lib/types';

type MetricRowProps = {
  label: string;
  original: number;
  modified: number;
  change: number;
  unit: string;
};

function MetricRow({ label, original, modified, change, unit }: MetricRowProps) {
  const increased = change > 0;
  const Icon = increased ? ArrowUpRight : ArrowDownRight;
  const tone = increased ? 'text-rose-600 bg-rose-50 border-rose-200' : 'text-emerald-700 bg-emerald-50 border-emerald-200';

  return (
    <div className="grid gap-3 border-b border-slate-900/10 py-4 last:border-0 sm:grid-cols-[1fr_auto_auto_auto] sm:items-center">
      <div>
        <div className="text-[10px] font-black uppercase tracking-[0.12em] text-slate-400">{label}</div>
        <div className="mt-1 flex items-center gap-2 font-mono text-[11px] font-bold text-slate-500"><span>{original.toLocaleString('tr-TR')} {unit}</span><ArrowRight size={11} className="text-slate-300" /><strong className="text-slate-900">{modified.toLocaleString('tr-TR')} {unit}</strong></div>
      </div>
      <span className={`inline-flex w-fit items-center gap-1 rounded-full border px-2.5 py-1 font-mono text-[9px] font-black ${tone}`}>{Math.abs(change).toFixed(1)}% <Icon size={10} /></span>
    </div>
  );
}

export default function ComparisonView({ result }: { result: ScenarioResult | null }) {
  if (!result) {
    return (
      <div className="bc-surface grid h-full min-h-[560px] place-items-center rounded-[28px] border-dashed">
        <div className="max-w-sm px-6 text-center">
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-[16px] border border-slate-950/10 bg-[#f4f5f2] text-slate-400"><BarChart3 size={20} /></div>
          <h2 className="mt-5 text-lg font-black tracking-[-0.03em] text-[#0a1020]">Run a counterfactual.</h2>
          <p className="mt-2 text-[11px] leading-relaxed text-slate-500">The comparison layer will show how modeled energy, food demand and carbon-related outputs shift under the selected scenario.</p>
          <span className="bc-chip mt-4 border-violet-200 bg-violet-50 text-violet-700"><Sparkles size={10} /> MODEL OUTPUT ONLY</span>
        </div>
      </div>
    );
  }

  const changes = result.changes;
  const chartData = [
    { name: 'Energy', Baseline: result.original.predicted_energy_mwh, Scenario: result.modified.predicted_energy_mwh },
    { name: 'Food / 1k', Baseline: result.original.food_demand_meals / 1000, Scenario: result.modified.food_demand_meals / 1000 },
    { name: 'CO₂ / 10', Baseline: result.original.co2_avoided_kg / 10, Scenario: result.modified.co2_avoided_kg / 10 },
  ];

  return (
    <div className="bc-surface flex h-full min-h-[560px] flex-col rounded-[28px] p-5 sm:p-6">
      <div className="flex flex-col gap-3 border-b border-slate-900/10 pb-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="bc-eyebrow">Counterfactual result</div>
          <h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">How the system changes.</h2>
          <p className="mt-1 text-[11px] text-slate-500">Baseline versus scenario output from the decision model.</p>
        </div>
        <span className="bc-chip self-start border-violet-200 bg-violet-50 text-violet-700"><Sparkles size={10} /> SIMULATION</span>
      </div>

      <div className="mt-3">
        <MetricRow label="Energy demand" original={result.original.predicted_energy_mwh} modified={result.modified.predicted_energy_mwh} change={changes.energy_change_percent} unit="MWh" />
        <MetricRow label="Food demand" original={result.original.food_demand_meals} modified={result.modified.food_demand_meals} change={changes.food_change_percent} unit="meals" />
        <MetricRow label="CO₂ model output" original={result.original.co2_avoided_kg} modified={result.modified.co2_avoided_kg} change={changes.co2_change_percent} unit="kg" />
      </div>

      <div className="mt-5 flex-1 rounded-[20px] bg-[#f4f5f2] p-4">
        <div className="mb-4 flex items-center justify-between"><div><div className="bc-eyebrow">Normalized comparison</div><div className="mt-1 text-[11px] font-bold text-slate-700">Baseline vs scenario</div></div><BarChart3 size={16} className="text-slate-400" /></div>
        <div className="h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 12, right: 8, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="2 6" vertical={false} stroke="rgba(15,23,42,0.08)" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#64748b', fontWeight: 600 }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} />
              <Tooltip contentStyle={{ borderRadius: '14px', borderColor: 'rgba(15,23,42,0.10)', fontSize: '10px' }} />
              <Bar dataKey="Baseline" fill="#94a3b8" radius={[7, 7, 0, 0]} barSize={20} />
              <Bar dataKey="Scenario" fill="#2f5cff" radius={[7, 7, 0, 0]} barSize={20} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-4 rounded-[16px] border border-blue-200 bg-blue-50 p-3 text-[10px] leading-relaxed text-blue-900">Scenario outputs are explanatory model comparisons. They are not measured outcomes, forecasts with calibrated uncertainty, or commands sent to campus systems.</div>
    </div>
  );
}
