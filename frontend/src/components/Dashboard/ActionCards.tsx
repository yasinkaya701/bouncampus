'use client';

import { ActionItem } from '@/lib/types';
import { Zap, Utensils, Building2, Clock, MapPin } from 'lucide-react';

export default function ActionCards({ actions }: { actions: ActionItem[] }) {
  const getIcon = (type: string) => {
    switch (type) {
      case 'energy': return <Zap size={16} className="text-amber-600" />;
      case 'food': return <Utensils size={16} className="text-emerald-600" />;
      case 'space': return <Building2 size={16} className="text-indigo-600" />;
      default: return <Zap size={16} className="text-slate-600" />;
    }
  };

  const getPriorityBadge = (priority: string) => {
    if (priority === 'HIGH') return <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 border border-rose-200">YÜKSEK ÖNCELİK</span>;
    if (priority === 'MEDIUM') return <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200">ORTA ÖNCELİK</span>;
    return <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200">STANDART</span>;
  };

  return (
    <div className="space-y-3">
      {actions.map(action => (
        <div key={action.id} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs hover:border-slate-300 transition flex flex-col gap-4">
          <div className="flex items-start gap-3.5">
            <div className="w-9 h-9 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center shrink-0 mt-0.5">
              {getIcon(action.type)}
            </div>
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <h4 className="font-bold text-sm text-slate-900">{action.title}</h4>
                {getPriorityBadge(action.priority)}
                {action.provenance && (
                  <span className="text-[9px] font-black font-mono px-2 py-0.5 rounded-md bg-violet-50 text-violet-700 border border-violet-200">
                    {action.provenance === 'MODEL_ESTIMATE' ? 'MODEL TAHMİNİ' : action.provenance}
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{action.description}</p>
              <div className="flex flex-wrap items-center gap-4 text-[11px] text-slate-500 font-mono mt-2.5">
                <span className="flex items-center gap-1.5"><Clock size={12} className="text-slate-400" />{action.time}</span>
                <span className="flex items-center gap-1.5"><MapPin size={12} className="text-slate-400" />{action.location}</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 flex items-center justify-between gap-3">
            <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Hesaplanan model etkisi</span>
            <span className="text-sm font-black text-slate-900 font-mono text-right">
              {action.impact_value.toLocaleString('tr-TR')} <span className="text-[11px] font-normal text-slate-500">{action.impact_unit}</span>
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
