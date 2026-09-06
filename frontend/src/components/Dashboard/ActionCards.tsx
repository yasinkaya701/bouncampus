'use client';

import { ActionItem } from '@/lib/types';
import { Zap, Utensils, Building2, Clock, MapPin, ArrowRight } from 'lucide-react';

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
    switch (priority) {
      case 'HIGH':
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 border border-rose-200">
            YÜKSEK ÖNCELİK
          </span>
        );
      case 'MEDIUM':
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200">
            ORTA ÖNCELİK
          </span>
        );
      case 'LOW':
      default:
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
            STANDART
          </span>
        );
    }
  };

  return (
    <div className="space-y-3">
      {actions.map(action => (
        <div 
          key={action.id} 
          className="bg-white border border-slate-200 rounded-2xl p-4.5 shadow-xs hover:border-slate-300 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
          <div className="flex items-start gap-3.5">
            <div className="w-9 h-9 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center shrink-0 mt-0.5">
              {getIcon(action.type)}
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h4 className="font-bold text-sm text-slate-900">{action.title}</h4>
                {getPriorityBadge(action.priority)}
              </div>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed max-w-2xl">
                {action.description}
              </p>
              <div className="flex flex-wrap items-center gap-4 text-[11px] text-slate-500 font-mono mt-2.5">
                <span className="flex items-center gap-1.5">
                  <Clock size={12} className="text-slate-400" />
                  <span>{action.time}</span>
                </span>
                <span className="flex items-center gap-1.5">
                  <MapPin size={12} className="text-slate-400" />
                  <span>{action.location}</span>
                </span>
              </div>
            </div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-right sm:text-center shrink-0 self-end sm:self-auto min-w-[120px]">
            <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Tahmini Tasarruf</span>
            <span className="text-base font-black text-slate-900 font-mono">
              {action.impact_value} <span className="text-xs font-normal text-slate-500">{action.impact_unit}</span>
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
