'use client';

import type { DashboardData } from '@/lib/types';
import { ArrowDownRight, Gauge, Leaf, Sparkles, Utensils, Users, Zap } from 'lucide-react';

type MetricCardProps = {
  label: string;
  value: string;
  unit?: string;
  note: string;
  icon: React.ComponentType<{ size?: number; strokeWidth?: number }>;
  dark?: boolean;
  footer?: React.ReactNode;
};

function MetricCard({ label, value, unit, note, icon: Icon, dark = false, footer }: MetricCardProps) {
  return (
    <article className={`group relative overflow-hidden rounded-[24px] p-5 transition duration-300 hover:-translate-y-0.5 ${dark ? 'bc-surface-dark text-white' : 'bc-surface text-[#0a1020]'}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className={`bc-eyebrow ${dark ? '!text-slate-500' : ''}`}>{label}</div>
          <div className="mt-5 flex items-baseline gap-1.5">
            <span className="font-mono text-[34px] font-black leading-none tracking-[-0.055em]">{value}</span>
            {unit && <span className={`font-mono text-xs font-bold ${dark ? 'text-slate-400' : 'text-slate-500'}`}>{unit}</span>}
          </div>
        </div>
        <div className={`grid h-10 w-10 shrink-0 place-items-center rounded-[14px] border ${dark ? 'border-white/10 bg-white/5 text-blue-300' : 'border-slate-950/10 bg-[#f4f5f2] text-slate-700'}`}>
          <Icon size={17} strokeWidth={2} />
        </div>
      </div>
      <p className={`mt-4 min-h-10 text-[11px] leading-relaxed ${dark ? 'text-slate-400' : 'text-slate-500'}`}>{note}</p>
      <div className="mt-4 border-t border-current/10 pt-3">{footer}</div>
    </article>
  );
}

export default function KPICards({ data }: { data: DashboardData }) {
  const occupancyPct = Math.round((data.campus_occupancy <= 1 ? data.campus_occupancy : data.campus_occupancy / 100) * 100);

  const modelTag = (
    <span className="bc-chip border-violet-200 bg-violet-50 text-violet-700">
      <Sparkles size={10} /> MODEL ESTIMATE
    </span>
  );

  return (
    <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      <MetricCard
        label="Schedule-derived use"
        value={`${occupancyPct}%`}
        note="Ders programındaki oda ve saatler üzerinden kapasite tabanlı anlık kullanım tahmini."
        icon={Users}
        footer={
          <div className="flex items-center justify-between gap-3">
            {modelTag}
            <div className="h-1.5 w-20 overflow-hidden rounded-full bg-slate-100">
              <div className="h-full rounded-full bg-[#2f5cff]" style={{ width: `${Math.max(4, Math.min(100, occupancyPct))}%` }} />
            </div>
          </div>
        }
      />

      <MetricCard
        label="Daily energy load"
        value={data.predicted_energy_mwh.toLocaleString('tr-TR', { maximumFractionDigits: 1 })}
        unit="MWh"
        note="Bina profili, tahmini kullanım ve dış hava ile hesaplanan physics-lite yük modeli."
        icon={Zap}
        footer={<div className="flex items-center justify-between">{modelTag}<Gauge size={14} className="text-slate-400" /></div>}
      />

      <MetricCard
        label="Lunch demand"
        value={data.food_demand_meals.toLocaleString('tr-TR')}
        unit="porsiyon"
        note="Öğle saatindeki ders çıkış akışı ve hava koşullarından türetilen üretim planlama girdisi."
        icon={Utensils}
        footer={modelTag}
      />

      <MetricCard
        label="Decision potential"
        value={`₺${data.potential_saving_tl.toLocaleString('tr-TR')}`}
        note="Optimizasyon senaryosunun parasal potansiyeli; uygulanmış tasarruf veya sayaç ölçümü değildir."
        icon={ArrowDownRight}
        dark
        footer={
          <div className="flex items-center justify-between gap-3">
            <span className="bc-chip border-white/10 bg-white/5 text-violet-200"><Sparkles size={10} /> MODEL</span>
            <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-300"><Leaf size={11} /> {data.co2_avoided_kg.toLocaleString('tr-TR')} kg CO₂e</span>
          </div>
        }
      />
    </section>
  );
}
