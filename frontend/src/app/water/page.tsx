'use client';

import React from 'react';
import { Droplets, CloudRain, ShieldCheck, CheckCircle2, Waves, Activity, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const WATER_FLOW_DATA = [
  { time: '06:00', SebekeSuyu: 45, YagmurHasadi: 20, GriSuGeriKazanim: 15 },
  { time: '08:00', SebekeSuyu: 120, YagmurHasadi: 35, GriSuGeriKazanim: 28 },
  { time: '10:00', SebekeSuyu: 210, YagmurHasadi: 45, GriSuGeriKazanim: 42 },
  { time: '12:00', SebekeSuyu: 340, YagmurHasadi: 50, GriSuGeriKazanim: 65 }, // Lunch rush
  { time: '14:00', SebekeSuyu: 290, YagmurHasadi: 48, GriSuGeriKazanim: 58 },
  { time: '16:00', SebekeSuyu: 240, YagmurHasadi: 40, GriSuGeriKazanim: 50 },
  { time: '18:00', SebekeSuyu: 190, YagmurHasadi: 30, GriSuGeriKazanim: 38 },
  { time: '20:00', SebekeSuyu: 110, YagmurHasadi: 25, GriSuGeriKazanim: 22 },
  { time: '22:00', SebekeSuyu: 60, YagmurHasadi: 15, GriSuGeriKazanim: 12 },
];

export default function SmartWaterPage() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-blue-50 text-blue-700 rounded-lg">
              <Droplets size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Akıllı Su & Yağmur Hasadı Yönetimi</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            500 m³ Kuzey Kampüs sarnıcı, Güney Kampüs gri su arıtması ve akustik şebeke boru kaçak tespiti.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-xl text-xs font-bold text-blue-800">
          <ShieldCheck size={15} className="text-blue-600" />
          <span>Sıfır Kaçak Su Güvenliği</span>
        </div>
      </div>

      {/* 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Yağmur Suyu Sarnıcı</span>
          <div className="text-3xl font-black text-blue-700">412 m³</div>
          <div className="text-xs text-gray-500 mt-1">500 m³ Kapasite • Doluluk: %82.4</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Peyzaj Sulaması:</span>
            <span className="font-bold text-emerald-700">%100 Karşılandı</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Gri Su Geri Kazanımı</span>
          <div className="text-3xl font-black text-teal-700">84.2 m³/Gün</div>
          <div className="text-xs text-gray-500 mt-1">Yurt lavabolarından rezervuarlara</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Şebeke Su Tasarrufu:</span>
            <span className="font-bold text-teal-800">-%28.5</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Akustik Kaçak Radarı</span>
          <div className="text-3xl font-black text-emerald-700">0 Kaçak</div>
          <div className="text-xs text-emerald-600 mt-1 font-semibold">18 Akustik Dinleme Sensörü</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Şebeke Basıncı:</span>
            <span className="font-bold text-gray-800">4.2 Bar (Stabil)</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Aylık Fatura Kazancı</span>
          <div className="text-3xl font-black text-gray-900">₺118,500</div>
          <div className="text-xs text-gray-500 mt-1">İSKİ şebeke suyu ikamesi</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Karbon Tasarrufu:</span>
            <span className="font-bold text-emerald-700">2.8 Ton CO₂</span>
          </div>
        </div>
      </div>

      {/* Water Flow Dynamics Chart */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h3 className="font-bold text-xl text-gray-900">24 Saatlik Kampüs Su Debisi (Litre / Dakika)</h3>
            <p className="text-xs text-gray-500">
              Şebeke suyu tüketimi ile yağmur hasadı ve gri su arıtmanın anlık ikame eğrisi
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-semibold">
            <span className="flex items-center gap-1 text-sky-600">
              <span className="w-3 h-3 rounded-full bg-sky-500"></span> Şebeke Suyu
            </span>
            <span className="flex items-center gap-1 text-blue-600">
              <span className="w-3 h-3 rounded-full bg-blue-600"></span> Yağmur Hasadı
            </span>
            <span className="flex items-center gap-1 text-teal-600">
              <span className="w-3 h-3 rounded-full bg-teal-500"></span> Gri Su
            </span>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={WATER_FLOW_DATA} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Area type="monotone" dataKey="SebekeSuyu" stroke="#0284c7" fill="#38bdf8" fillOpacity={0.4} name="Şebeke (L/dk)" />
              <Area type="monotone" dataKey="YagmurHasadi" stroke="#2563eb" fill="#60a5fa" fillOpacity={0.4} name="Yağmur Hasadı (L/dk)" />
              <Area type="monotone" dataKey="GriSuGeriKazanim" stroke="#0d9488" fill="#2dd4bf" fillOpacity={0.4} name="Gri Su (L/dk)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
