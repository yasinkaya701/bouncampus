'use client';

import { DashboardData } from '@/lib/types';
import { Users, Zap, Utensils, TrendingDown, Leaf, Activity } from 'lucide-react';

export default function KPICards({ data }: { data: DashboardData }) {
  const occupancyPct = data.campus_occupancy <= 1
    ? Math.round(data.campus_occupancy * 100)
    : Math.round(data.campus_occupancy);

  const ModelTag = () => (
    <span className="text-[9px] font-black font-mono px-1.5 py-0.5 rounded bg-violet-50 text-violet-700 border border-violet-200">
      MODEL TAHMİNİ
    </span>
  );

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between gap-2">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Ders Kaynaklı Kullanım</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700"><Users size={16} /></div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">%{occupancyPct}</span>
            <ModelTag />
          </div>
          <p className="text-xs text-slate-500 mt-2">BUIS/ÖBİKAS oda-saat snapshot&apos;ından kapasite tabanlı tahmin</p>
          <div className="w-full bg-slate-100 h-1.5 rounded-full mt-3 overflow-hidden">
            <div className={`h-full rounded-full ${occupancyPct > 70 ? 'bg-rose-500' : occupancyPct > 40 ? 'bg-amber-500' : 'bg-emerald-500'}`} style={{ width: `${Math.min(100, occupancyPct)}%` }} />
          </div>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Günlük Enerji Yükü</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700"><Zap size={16} /></div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">{data.predicted_energy_mwh}</span>
            <span className="text-sm font-bold text-slate-500 font-mono">MWh</span>
          </div>
          <div className="mt-2"><ModelTag /></div>
          <p className="text-xs text-slate-500 mt-2 flex items-center gap-1"><Activity size={13} /> Bina profili + hava + tahmini kullanım; BMS sayaç değeri değil</p>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-500 tracking-wide uppercase">Öğle Talebi</span>
          <div className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700"><Utensils size={16} /></div>
        </div>
        <div className="mt-4">
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-black text-slate-900 font-mono tracking-tight">{data.food_demand_meals.toLocaleString('tr-TR')}</span>
            <span className="text-sm font-bold text-slate-500 font-mono">porsiyon</span>
          </div>
          <div className="mt-2"><ModelTag /></div>
          <p className="text-xs text-slate-500 mt-2">Ders çıkış akışı + yağış etkisi; POS satış sayımı değil</p>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xs flex flex-col justify-between text-white">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-400 tracking-wide uppercase">Optimizasyon Potansiyeli</span>
          <div className="w-8 h-8 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400"><TrendingDown size={16} /></div>
        </div>
        <div className="mt-4">
          <div className="text-3xl font-black text-emerald-400 font-mono tracking-tight">₺{data.potential_saving_tl.toLocaleString('tr-TR')}</div>
          <span className="inline-block mt-2 text-[9px] font-black font-mono px-1.5 py-0.5 rounded bg-violet-950 text-violet-300 border border-violet-800">MODEL TAHMİNİ</span>
          <div className="flex items-center gap-1.5 text-xs text-slate-300 mt-2">
            <Leaf size={13} className="text-emerald-400" />
            <span><strong>{data.co2_avoided_kg.toLocaleString('tr-TR')} kg</strong> CO₂e model karşılığı</span>
          </div>
        </div>
      </div>
    </div>
  );
}
