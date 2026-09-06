'use client';

import React, { useState } from 'react';
import { Calendar, ArrowRight, CheckCircle2, Zap, Building2, Shuffle, Download, Sparkles, Filter } from 'lucide-react';
import { runClassroomConsolidationOptimizer, ConsolidationOpportunity } from '@/lib/simulation-engine';

export default function ReschedulerPage() {
  const [opportunities, setOpportunities] = useState<ConsolidationOpportunity[]>(runClassroomConsolidationOptimizer());
  const [appliedCount, setAppliedCount] = useState(0);
  const [selectedDay, setSelectedDay] = useState<'M' | 'T' | 'W' | 'Th' | 'F'>('M');
  const [selectedBuildingFilter, setSelectedBuildingFilter] = useState<string>('all');

  const totalKwhSaved = opportunities.reduce((acc, curr) => acc + curr.energySavedKwh, 0);
  const totalTlSaved = opportunities.reduce((acc, curr) => acc + curr.costSavedTl, 0);

  const handleApplyAll = () => {
    setAppliedCount(opportunities.length);
  };

  const handleApplySingle = (index: number) => {
    setAppliedCount(prev => prev + 1);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-indigo-50 text-indigo-700 rounded-lg">
              <Shuffle size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Akıllı Amfi & Ders Programı Konsolidatörü</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            3.238 gerçek OBIKAS dersinin termodinamik optimizasyonu: Az dolu binalardaki sınıfları merkezi amfilere toplayarak kat kapatma önerisi.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleApplyAll}
            disabled={appliedCount === opportunities.length}
            className="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 disabled:bg-emerald-300 text-white rounded-xl text-xs font-bold transition shadow-sm flex items-center gap-2"
          >
            <Sparkles size={16} />
            <span>Tüm Taşımaları Onayla ({opportunities.length} Amfi)</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Kapatılacak Üst Kat Alanı</span>
          <div className="text-3xl font-black text-emerald-700">4,850 m²</div>
          <div className="text-xs text-gray-500 mt-1">TB 4. Kat + İB 5. Kat + EF 4. Kat komple uyku modunda</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">HVAC & Aydınlatma Kazancı</span>
          <div className="text-3xl font-black text-gray-900">+{totalKwhSaved} kWh/Gün</div>
          <div className="text-xs text-emerald-600 font-semibold mt-1">Gereksiz bina ısıtma/soğutması %0</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Haftalık Bütçe Tasarrufu</span>
          <div className="text-3xl font-black text-indigo-700">₺{totalTlSaved * 5}</div>
          <div className="text-xs text-gray-500 mt-1">Elektrik ve doğalgaz tepe fatura avantajı</div>
        </div>
      </div>

      {/* Optimization Opportunities Table */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg text-gray-900">Önerilen Amfi Taşıma & Kat Kapatma Çizelgesi</h3>
            <p className="text-xs text-gray-500">MIP (Karışık Tamsayılı Programlama) Çözücü Çıktısı</p>
          </div>
          <span className="text-xs bg-indigo-50 text-indigo-700 font-bold px-3 py-1 rounded-full font-mono">
            {appliedCount} / {opportunities.length} Taşındı
          </span>
        </div>

        <div className="divide-y divide-gray-100">
          {opportunities.map((opp, idx) => (
            <div key={idx} className="p-6 hover:bg-gray-50/70 transition flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div className="space-y-2 flex-1">
                <div className="flex flex-wrap items-center gap-3">
                  {/* Source */}
                  <div className="bg-rose-50 border border-rose-200 text-rose-900 px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-2">
                    <Building2 size={15} />
                    <span>{opp.sourceBuilding} • {opp.sourceRoom} (Kat {opp.sourceFloor})</span>
                    <span className="bg-rose-200 text-rose-800 text-[10px] px-1.5 py-0.2 rounded font-mono">
                      {opp.enrolledStudents} Öğrenci
                    </span>
                  </div>

                  <ArrowRight size={16} className="text-gray-400" />

                  {/* Target */}
                  <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-2">
                    <Building2 size={15} />
                    <span>{opp.targetBuilding} • {opp.targetRoom} (Kat {opp.targetFloor})</span>
                    <span className="bg-emerald-200 text-emerald-800 text-[10px] px-1.5 py-0.2 rounded font-mono">
                      Kapasite: {opp.targetCapacity}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-gray-600 leading-relaxed pt-1">
                  {opp.actionReason}
                </p>
              </div>

              {/* Savings & Action Button */}
              <div className="flex items-center gap-4 shrink-0">
                <div className="text-right">
                  <div className="text-sm font-black text-emerald-700">+{opp.energySavedKwh} kWh</div>
                  <div className="text-[11px] text-gray-500">₺{opp.costSavedTl} Günlük Kazanç</div>
                </div>

                <button
                  onClick={() => handleApplySingle(idx)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-gray-900 hover:bg-black text-white transition shadow-xs flex items-center gap-1.5"
                >
                  <CheckCircle2 size={14} className="text-emerald-400" />
                  <span>Onayla</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
