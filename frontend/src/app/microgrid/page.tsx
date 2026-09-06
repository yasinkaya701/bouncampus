'use client';

import React, { useState } from 'react';
import { Wind, Sun, BatteryCharging, Zap, ShieldCheck, ArrowDownRight, ArrowUpRight, TrendingUp, Gauge, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

const POWER_DISPATCH_DATA = [
  { time: '00:00', KampusYuku: 240, KilyosRES: 380, GunesSPP: 0, BESS_Sarj: -140 },
  { time: '02:00', KampusYuku: 190, KilyosRES: 410, GunesSPP: 0, BESS_Sarj: -220 },
  { time: '04:00', KampusYuku: 180, KilyosRES: 430, GunesSPP: 0, BESS_Sarj: -250 },
  { time: '06:00', KampusYuku: 310, KilyosRES: 390, GunesSPP: 30, BESS_Sarj: -110 },
  { time: '08:00', KampusYuku: 850, KilyosRES: 360, GunesSPP: 180, BESS_Sarj: 150 },
  { time: '10:00', KampusYuku: 1420, KilyosRES: 350, GunesSPP: 380, BESS_Sarj: 320 },
  { time: '12:00', KampusYuku: 1890, KilyosRES: 420, GunesSPP: 430, BESS_Sarj: 480 }, // Peak shaving active!
  { time: '14:00', KampusYuku: 1780, KilyosRES: 440, GunesSPP: 410, BESS_Sarj: 450 },
  { time: '16:00', KampusYuku: 1350, KilyosRES: 390, GunesSPP: 220, BESS_Sarj: 240 },
  { time: '18:00', KampusYuku: 820, KilyosRES: 370, GunesSPP: 40, BESS_Sarj: 0 },
  { time: '20:00', KampusYuku: 560, KilyosRES: 380, GunesSPP: 0, BESS_Sarj: 0 },
  { time: '22:00', KampusYuku: 380, KilyosRES: 400, GunesSPP: 0, BESS_Sarj: -20 },
];

export default function MicrogridPage() {
  const [bessMode, setBessMode] = useState<'auto' | 'discharge' | 'charge'>('auto');

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-teal-50 text-teal-700 rounded-lg">
              <Zap size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Mikroşebeke & Kilyos RES / BESS Yönetimi</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Kilyos 1.0 MW Enercon E-44 Rüzgar Türbini, çatı fotovoltaik santralleri ve 2.0 MWh batarya depolama (BESS).
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-800">
          <ShieldCheck size={16} className="text-emerald-600" />
          <span>ISO 50001 Enerji Yönetimi Uyumlu</span>
        </div>
      </div>

      {/* 4 Generation & Storage KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Kilyos Wind Turbine */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Kilyos RES Türbini</span>
            <span className="p-2 bg-teal-50 text-teal-700 rounded-xl">
              <Wind size={20} className="animate-spin" style={{ animationDuration: '6s' }} />
            </span>
          </div>
          <div className="text-3xl font-black text-gray-900">420 kW</div>
          <div className="text-xs text-gray-500 mt-1">Enercon E-44 • Rüzgar: 23.4 km/h</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Bugünkü Üretim:</span>
            <span className="font-bold text-teal-700">6.84 MWh</span>
          </div>
        </div>

        {/* Solar Photovoltaics */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Çatı Güneş Santrali</span>
            <span className="p-2 bg-amber-50 text-amber-600 rounded-xl">
              <Sun size={20} />
            </span>
          </div>
          <div className="text-3xl font-black text-gray-900">380 kW</div>
          <div className="text-xs text-gray-500 mt-1">Kare Blok + Teknopark • Işıma: 720 W/m²</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Bugünkü Üretim:</span>
            <span className="font-bold text-amber-600">3.22 MWh</span>
          </div>
        </div>

        {/* BESS Battery Storage */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">2.0 MWh BESS Batarya</span>
            <span className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
              <BatteryCharging size={20} />
            </span>
          </div>
          <div className="text-3xl font-black text-gray-900">%78 SoC</div>
          <div className="text-xs text-indigo-700 font-semibold mt-1">Pik Tıraşlama Deşarjında (+480 kW)</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Depolanan Temiz Enerji:</span>
            <span className="font-bold text-indigo-700">1.56 MWh</span>
          </div>
        </div>

        {/* Grid Carbon Intensity */}
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Şebeke Ofseti</span>
            <span className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <Gauge size={20} />
            </span>
          </div>
          <div className="text-3xl font-black text-emerald-700">%42.3</div>
          <div className="text-xs text-gray-500 mt-1">Kampüs anlık temiz enerji karşılanması</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Dengelenen CO₂:</span>
            <span className="font-bold text-emerald-800">4.72 Ton</span>
          </div>
        </div>
      </div>

      {/* Peak-Shaving Dispatch Chart */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h3 className="font-bold text-xl text-gray-900">Mikroşebeke Güç Dengesi & Peak-Shaving Eğrisi</h3>
            <p className="text-xs text-gray-500">
              Saat 12:00-14:00 pik derslik yükünde batarya (BESS) devreye girerek şebeke tepe talep cezasını önler
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-semibold">
            <span className="flex items-center gap-1 text-rose-600">
              <span className="w-3 h-3 rounded-full bg-rose-500"></span> Kampüs Yükü (kW)
            </span>
            <span className="flex items-center gap-1 text-teal-600">
              <span className="w-3 h-3 rounded-full bg-teal-500"></span> Kilyos Rüzgar (kW)
            </span>
            <span className="flex items-center gap-1 text-amber-500">
              <span className="w-3 h-3 rounded-full bg-amber-400"></span> Çatı SPP (kW)
            </span>
            <span className="flex items-center gap-1 text-indigo-600">
              <span className="w-3 h-3 rounded-full bg-indigo-500"></span> BESS Deşarj (kW)
            </span>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={POWER_DISPATCH_DATA} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="KampusYuku" stroke="#ef4444" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="KilyosRES" stroke="#0d9488" strokeWidth={2} strokeDasharray="4 4" dot={false} />
              <Line type="monotone" dataKey="GunesSPP" stroke="#f59e0b" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="BESS_Sarj" stroke="#6366f1" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
