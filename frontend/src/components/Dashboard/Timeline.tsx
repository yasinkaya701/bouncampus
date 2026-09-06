'use client';

import { ActionItem } from '@/lib/types';
import { Zap, Utensils, Building2, Clock, MapPin } from 'lucide-react';

export default function Timeline({ actions }: { actions: ActionItem[] }) {
  const sortedActions = [...actions].sort((a, b) => a.time.localeCompare(b.time));

  const getIcon = (type: string) => {
    switch (type) {
      case 'energy': return <Zap size={14} className="text-amber-600" />;
      case 'food': return <Utensils size={14} className="text-emerald-600" />;
      case 'space': return <Building2 size={14} className="text-indigo-600" />;
      default: return <Zap size={14} className="text-slate-600" />;
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs overflow-x-auto">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
        <div>
          <h3 className="font-bold text-sm text-slate-900">Günlük Müdahale Zaman Çizelgesi</h3>
          <p className="text-xs text-slate-500">OBIKAS amfi programına ve yemekhane saatlerine göre optimize edilmiş eylemler</p>
        </div>
        <span className="text-xs font-mono font-bold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-lg">
          08:00 — 22:00
        </span>
      </div>

      <div className="relative pl-6 border-l-2 border-slate-200 space-y-6 my-2">
        {sortedActions.map(action => (
          <div key={action.id} className="relative group">
            {/* Timeline node dot */}
            <div className="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-white border-2 border-slate-900 flex items-center justify-center">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 hover:border-slate-300 transition flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center shrink-0 mt-0.5">
                  {getIcon(action.type)}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-900">{action.title}</span>
                    <span className="text-[10px] font-mono text-slate-500 bg-white px-1.5 py-0.2 rounded border border-slate-200">
                      {action.time}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">{action.description}</p>
                </div>
              </div>

              <div className="text-right sm:text-center shrink-0 font-mono text-xs font-bold text-slate-800 bg-white px-3 py-1.5 rounded-lg border border-slate-200">
                +{action.impact_value} {action.impact_unit}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
