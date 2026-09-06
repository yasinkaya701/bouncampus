'use client';

import React, { useState } from 'react';
import { Bus, BookOpen, Utensils, Users, ArrowRight, Clock, MapPin, AlertCircle, CheckCircle, Navigation } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const HOURLY_FLOW_DATA = [
  { time: '08:00', Derslikler: 240, Yemekhane: 80, Kütüphane: 40, RingBekleyen: 65 },
  { time: '09:00', Derslikler: 920, Yemekhane: 110, Kütüphane: 120, RingBekleyen: 85 },
  { time: '10:00', Derslikler: 1480, Yemekhane: 150, Kütüphane: 210, RingBekleyen: 45 },
  { time: '11:00', Derslikler: 1750, Yemekhane: 280, Kütüphane: 290, RingBekleyen: 40 },
  { time: '12:00', Derslikler: 780, Yemekhane: 1212, Kütüphane: 260, RingBekleyen: 95 },
  { time: '13:00', Derslikler: 910, Yemekhane: 1050, Kütüphane: 310, RingBekleyen: 80 },
  { time: '14:00', Derslikler: 1620, Yemekhane: 340, Kütüphane: 350, RingBekleyen: 35 },
  { time: '15:00', Derslikler: 1510, Yemekhane: 190, Kütüphane: 390, RingBekleyen: 30 },
  { time: '16:00', Derslikler: 1180, Yemekhane: 150, Kütüphane: 425, RingBekleyen: 50 },
  { time: '17:00', Derslikler: 620, Yemekhane: 220, Kütüphane: 430, RingBekleyen: 75 },
  { time: '18:00', Derslikler: 280, Yemekhane: 650, Kütüphane: 410, RingBekleyen: 60 },
  { time: '19:00', Derslikler: 120, Yemekhane: 380, Kütüphane: 380, RingBekleyen: 35 },
  { time: '20:00', Derslikler: 40, Yemekhane: 120, Kütüphane: 360, RingBekleyen: 20 },
];

export default function CampusFlowPage() {
  const [selectedFacility, setSelectedFacility] = useState<'all' | 'library' | 'shuttle' | 'dining'>('all');

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-indigo-50 text-indigo-700 rounded-lg">
              <Navigation size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Canlı İnsan Akışı & Ring Radarı</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            OBIKAS ders dağılımı ve sensör verileriyle amfi çıkışları, kütüphane boş masa ve servis kuyruk tahmini.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-gray-100 p-1 rounded-xl text-xs font-semibold">
          <button
            onClick={() => setSelectedFacility('all')}
            className={`px-3 py-1.5 rounded-lg transition ${selectedFacility === 'all' ? 'bg-white text-indigo-900 shadow-xs' : 'text-gray-600'}`}
          >
            Tüm Kampüs
          </button>
          <button
            onClick={() => setSelectedFacility('shuttle')}
            className={`px-3 py-1.5 rounded-lg transition ${selectedFacility === 'shuttle' ? 'bg-white text-indigo-900 shadow-xs' : 'text-gray-600'}`}
          >
            Ring Servisleri
          </button>
          <button
            onClick={() => setSelectedFacility('library')}
            className={`px-3 py-1.5 rounded-lg transition ${selectedFacility === 'library' ? 'bg-white text-indigo-900 shadow-xs' : 'text-gray-600'}`}
          >
            Kütüphane Masaları
          </button>
          <button
            onClick={() => setSelectedFacility('dining')}
            className={`px-3 py-1.5 rounded-lg transition ${selectedFacility === 'dining' ? 'bg-white text-indigo-900 shadow-xs' : 'text-gray-600'}`}
          >
            Yemek Kuyrukları
          </button>
        </div>
      </div>

      {/* Top 3 Live Radar Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Ring Bus Card */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs hover:shadow-md transition">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2.5 bg-blue-50 text-blue-700 rounded-xl">
              <Bus size={22} />
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 bg-amber-100 text-amber-800 rounded-full flex items-center gap-1">
              <Clock size={12} /> Pik Sefer Frekansı
            </span>
          </div>
          <h3 className="font-bold text-gray-900 text-lg">Kuzey ⇄ Güney Ring Servisi</h3>
          <p className="text-xs text-gray-500 mt-0.5">Hisarüstü Kapı - Bebek Meydan Hattı</p>

          <div className="mt-4 space-y-3 bg-gray-50 p-3.5 rounded-xl text-xs">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Sıradaki Bekleyen:</span>
              <span className="font-bold text-gray-900 text-sm">~68 Öğrenci</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Ortalama Bekleme:</span>
              <span className="font-bold text-amber-600 text-sm">6 Dakika</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Aktif Ring Sayısı:</span>
              <span className="font-bold text-emerald-700 text-sm">3 Elektrikli Araç</span>
            </div>
          </div>
          <div className="mt-3 text-[11px] text-gray-500 flex items-center gap-1">
            <CheckCircle size={13} className="text-emerald-600" />
            <span>AI Önerisi: Saat 12:30&apos;da frekans 15 dk &rarr; 7 dk olarak güncellendi.</span>
          </div>
        </div>

        {/* Library Seats Card */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs hover:shadow-md transition">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2.5 bg-emerald-50 text-emerald-700 rounded-xl">
              <BookOpen size={22} />
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 bg-emerald-100 text-emerald-800 rounded-full">
              Canlı Masa Radarı
            </span>
          </div>
          <h3 className="font-bold text-gray-900 text-lg">Aptullah Kuran Kütüphanesi</h3>
          <p className="text-xs text-gray-500 mt-0.5">Kuzey Kampüs • 4 Katlı Çalışma Alanı</p>

          <div className="mt-4 space-y-2.5 bg-gray-50 p-3.5 rounded-xl text-xs">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">2. Kat Bireysel Sessiz Salon:</span>
              <span className="font-bold text-emerald-700">46 Boş Masa (%54)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">1. Kat Süreli Yayınlar:</span>
              <span className="font-bold text-amber-600">31 Boş Masa (%62)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Zemin Kat Grup Çalışma:</span>
              <span className="font-bold text-rose-600">8 Boş Masa (%89)</span>
            </div>
          </div>
          <div className="mt-3 text-[11px] text-gray-500 flex items-center gap-1">
            <CheckCircle size={13} className="text-emerald-600" />
            <span>Toplam 512 koltuk • 130 aktif boş yer mevcut.</span>
          </div>
        </div>

        {/* Cafeteria Wait Time Card */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs hover:shadow-md transition">
          <div className="flex items-center justify-between mb-3">
            <div className="p-2.5 bg-orange-50 text-orange-700 rounded-xl">
              <Utensils size={22} />
            </div>
            <span className="text-[11px] font-bold px-2.5 py-1 bg-orange-100 text-orange-800 rounded-full">
              Turnike Barometresi
            </span>
          </div>
          <h3 className="font-bold text-gray-900 text-lg">Yemekhane & Kantin Kuyrukları</h3>
          <p className="text-xs text-gray-500 mt-0.5">Turnike Geçiş Hızı & Bekleme Süreleri</p>

          <div className="mt-4 space-y-2.5 bg-gray-50 p-3.5 rounded-xl text-xs">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Kuzey Yemekhanesi:</span>
              <span className="font-bold text-rose-600">~14 Dk (633 Kişi)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Güney Yemekhanesi:</span>
              <span className="font-bold text-emerald-700">~4 Dk (152 Kişi)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Orta Kantin & Çay Ocağı:</span>
              <span className="font-bold text-amber-600">~6 Dk (430 Kişi)</span>
            </div>
          </div>
          <div className="mt-3 text-[11px] text-gray-500 flex items-center gap-1">
            <AlertCircle size={13} className="text-amber-600" />
            <span>Saat 12:15 New Hall çıkışında Güney Yemekhanesi önerilir.</span>
          </div>
        </div>
      </div>

      {/* Migration Stream Chart */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h3 className="font-bold text-xl text-gray-900">24 Saatlik Kampüs İçi İnsan Göçü Eğrisi</h3>
            <p className="text-xs text-gray-500">
              Derslik amfilerinden yemekhane, kütüphane ve servis duraklarına akan eş zamanlı nüfus
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-semibold">
            <span className="flex items-center gap-1 text-emerald-700">
              <span className="w-3 h-3 rounded-full bg-emerald-600"></span> Amfiler
            </span>
            <span className="flex items-center gap-1 text-orange-600">
              <span className="w-3 h-3 rounded-full bg-orange-500"></span> Yemekhane
            </span>
            <span className="flex items-center gap-1 text-indigo-600">
              <span className="w-3 h-3 rounded-full bg-indigo-500"></span> Kütüphane
            </span>
            <span className="flex items-center gap-1 text-blue-600">
              <span className="w-3 h-3 rounded-full bg-blue-500"></span> Ring Bekleyen
            </span>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={HOURLY_FLOW_DATA} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="amfiGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="yemekGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="libGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Area type="monotone" dataKey="Derslikler" stroke="#059669" fillOpacity={1} fill="url(#amfiGrad)" />
              <Area type="monotone" dataKey="Yemekhane" stroke="#ea580c" fillOpacity={1} fill="url(#yemekGrad)" />
              <Area type="monotone" dataKey="Kütüphane" stroke="#4f46e5" fillOpacity={1} fill="url(#libGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
