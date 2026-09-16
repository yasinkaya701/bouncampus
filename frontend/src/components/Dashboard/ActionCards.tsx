'use client';

import type { ActionItem } from '@/lib/types';
import { Building2, Clock3, MapPin, Sparkles, Utensils, Zap } from 'lucide-react';

const priorityStyles = {
  HIGH: 'border-rose-200 bg-rose-50 text-rose-700',
  MEDIUM: 'border-amber-200 bg-amber-50 text-amber-700',
  LOW: 'border-slate-200 bg-slate-50 text-slate-600',
};

function ActionIcon({ type }: { type: ActionItem['type'] }) {
  const className = type === 'energy' ? 'text-amber-600' : type === 'food' ? 'text-emerald-600' : 'text-blue-600';
  if (type === 'food') return <Utensils size={15} className={className} />;
  if (type === 'space') return <Building2 size={15} className={className} />;
  return <Zap size={15} className={className} />;
}

export default function ActionCards({ actions }: { actions: ActionItem[] }) {
  if (!actions.length) {
    return (
      <div className="rounded-[22px] border border-dashed border-slate-900/15 bg-white/60 p-6 text-center">
        <p className="text-xs font-bold text-slate-700">Şu an öne çıkan aksiyon yok.</p>
        <p className="mt-1 text-[11px] text-slate-500">Model, veri geldikçe karar adaylarını burada sıralar.</p>
      </div>
    );
  }

  return (
    <div className="space-y-2.5">
      {actions.map((action, index) => (
        <article key={action.id} className="group rounded-[22px] border border-slate-950/10 bg-white/90 p-4 shadow-[0_8px_24px_rgba(10,16,32,0.025)] transition hover:-translate-y-0.5 hover:border-slate-950/15 hover:shadow-[0_12px_34px_rgba(10,16,32,0.06)]">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 grid h-9 w-9 shrink-0 place-items-center rounded-[13px] border border-slate-950/10 bg-[#f4f5f2]">
              <ActionIcon type={action.type} />
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="font-mono text-[9px] font-black text-slate-400">0{index + 1}</span>
                <span className={`rounded-full border px-2 py-0.5 text-[8px] font-black tracking-[0.08em] ${priorityStyles[action.priority]}`}>
                  {action.priority === 'HIGH' ? 'HIGH PRIORITY' : action.priority === 'MEDIUM' ? 'MEDIUM' : 'STANDARD'}
                </span>
                {action.provenance === 'MODEL_ESTIMATE' && (
                  <span className="inline-flex items-center gap-1 rounded-full border border-violet-200 bg-violet-50 px-2 py-0.5 text-[8px] font-black tracking-[0.06em] text-violet-700">
                    <Sparkles size={8} /> MODEL
                  </span>
                )}
              </div>
              <h3 className="mt-2 text-[13px] font-black leading-snug tracking-[-0.015em] text-[#0a1020]">{action.title}</h3>
              <p className="mt-2 text-[11px] leading-relaxed text-slate-500">{action.description}</p>

              <div className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-[9px] font-bold text-slate-400">
                <span className="inline-flex items-center gap-1"><Clock3 size={10} /> {action.time}</span>
                <span className="inline-flex items-center gap-1"><MapPin size={10} /> {action.location}</span>
              </div>
            </div>
          </div>

          <div className="mt-4 flex items-end justify-between gap-4 border-t border-slate-900/8 pt-3">
            <span className="text-[9px] font-black uppercase tracking-[0.14em] text-slate-400">Modeled impact</span>
            <div className="text-right font-mono">
              <span className="text-base font-black tracking-[-0.03em] text-[#0a1020]">{action.impact_value.toLocaleString('tr-TR')}</span>
              <span className="ml-1 text-[9px] font-bold text-slate-500">{action.impact_unit}</span>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
