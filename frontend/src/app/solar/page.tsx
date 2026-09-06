'use client';

import React, { useState } from 'react';
import { Sun, Zap, TrendingUp, DollarSign, ShieldCheck, ArrowRight, Building2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const ROOFTOP_POTENTIAL = [
  { building: 'Kare Blok (KB)', roofAreaSqM: 1850, capacityKwp: 280, annualMwh: 364, paybackYears: 3.6 },
  { building: 'Teknopark / Kuzey Park', roofAreaSqM: 1400, capacityKwp: 210, annualMwh: 273, paybackYears: 3.7 },
  { building: 'Uçaksavar Spor Salonu', roofAreaSqM: 2600, capacityKwp: 390, annualMwh: 507, paybackYears: 3.4 },
  { building: 'New Hall (NH)', roofAreaSqM: 1200, capacityKwp: 180, annualMwh: 234, paybackYears: 3.9 },
  { building: 'Kuzey Yurtları', roofAreaSqM: 1950, capacityKwp: 290, annualMwh: 377, paybackYears: 3.5 },
];

export default function SolarRooftopPage() {
  const [selectedRoof, setSelectedRoof] = useState(ROOFTOP_POTENTIAL[0]);

  const totalKwp = ROOFTOP_POTENTIAL.reduce((a, b) => a + b.capacityKwp, 0);
  const totalAnnualMwh = ROOFTOP_POTENTIAL.reduce((a, b) => a + b.annualMwh, 0);

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-amber-50 text-amber-600 rounded-lg">
              <Sun size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Çatı Güneş Santralleri (SPP) & Gölge Analizi</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Boğaziçi çatı geometrisi, yıllık solar ışıma (GHI) simülasyonu ve yatırım geri dönüş (ROI) hesaplayıcısı.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-xl text-xs font-bold text-amber-800">
          <Zap size={15} className="text-amber-600" />
          <span>Toplam 1.35 MWp Çatı Potansiyeli</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Kurulabilir Çatı Gücü</span>
          <div className="text-3xl font-black text-amber-600">{totalKwp} kWp</div>
          <div className="text-xs text-gray-500 mt-1">9,000 m² Uygun Çatı Alanı</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Yıllık Temiz Elektrik</span>
          <div className="text-3xl font-black text-gray-900">{totalAnnualMwh} MWh</div>
          <div className="text-xs text-emerald-600 font-semibold mt-1">Kampüs elektrik ihtiyacının %22&apos;si</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Ortalama Geri Dönüş</span>
          <div className="text-3xl font-black text-emerald-700">3.6 Yıl</div>
          <div className="text-xs text-gray-500 mt-1">LCOE: $0.042 / kWh</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Yıllık Karbon Engelleme</span>
          <div className="text-3xl font-black text-teal-700">776 Ton</div>
          <div className="text-xs text-gray-500 mt-1">TEİAŞ şebeke emisyon ikamesi</div>
        </div>
      </div>

      {/* Rooftop Comparison Chart */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <h3 className="font-bold text-xl text-gray-900 mb-2">Bina Bazında Çatı Güneş Potansiyeli (kWp)</h3>
        <p className="text-xs text-gray-500 mb-6">En verimli binalar ve yıllık üretilecek MWh elektrik miktarı</p>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={ROOFTOP_POTENTIAL} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="building" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="capacityKwp" fill="#f59e0b" name="Kurulu Güç (kWp)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="annualMwh" fill="#10b981" name="Yıllık Üretim (MWh)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
