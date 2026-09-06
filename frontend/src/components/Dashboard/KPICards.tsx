'use client';

import { DashboardData } from '@/lib/types';
import { Users, Zap, Utensils, TrendingDown, Leaf, ArrowDownRight, Activity } from 'lucide-react';

export default function KPICards({ data }: { data: DashboardData }) {
  // Format percentage properly (data.campus_occupancy is 0.0 - 1.0 or already 100-based)
  const occupancyPct = data.campus_occupancy <= 1.0 
    ? Math.round(data.campus_occupancy * 100) 
    : Math.round(data.campus_occupancy);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Campus Occupancy */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Kampüs Doluluk Oranı</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700">
            <Users size={16} />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">%{occupancyPct}</span>
            <span className="text-xs text-slate-500 font-medium">aktif amfi & kütüphane</span>
          </div>
          <div className="w-full bg-slate-100 h-1.5 rounded-full mt-3 overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-500 ${
                occupancyPct > 70 ? 'bg-rose-500' : occupancyPct > 40 ? 'bg-amber-500' : 'bg-emerald-500'
              }`}
              style={{ width: `${Math.min(100, occupancyPct)}%` }}
            />
          </div>
        </div>
      </div>

      {/* 2. Predicted Energy */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Tahmini Günlük Yük</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700">
            <Zap size={16} />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">{data.predicted_energy_mwh}</span>
            <span className="text-sm font-bold text-slate-500 font-mono">MWh</span>
          </div>
          <p className="text-xs text-slate-500 mt-2 flex items-center gap-1">
            <Activity size={13} className="text-emerald-600" />
            <span>21 bina termodinamik taban yükü</span>
          </p>
        </div>
      </div>

      {/* 3. Food Demand */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between hover:border-slate-300 transition">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Yemekhane Öğün Talebi</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700">
            <Utensils size={16} />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">{data.food_demand_meals.toLocaleString('tr-TR')}</span>
            <span className="text-sm font-bold text-slate-500 font-mono">porsiyon</span>
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Kuzey (660 koltuk) + Güney (159 koltuk)
          </p>
        </div>
      </div>

      {/* 4. Potential Saving & CO2 Avoided */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xs flex flex-col justify-between text-white">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-400 tracking-wide uppercase">Günlük Tasarruf Potansiyeli</span>
          <div className="w-8 h-8 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400">
            <TrendingDown size={16} />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-emerald-400 font-mono tracking-tight">
              ₺{data.potential_saving_tl.toLocaleString('tr-TR')}
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-slate-300 mt-2">
            <Leaf size={13} className="text-emerald-400" />
            <span><strong>{data.co2_avoided_kg.toLocaleString('tr-TR')} kg</strong> CO₂e engellenen salım</span>
          </div>
        </div>
      </div>
    </div>
  );
}
