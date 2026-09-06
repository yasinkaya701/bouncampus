'use client';

import React from 'react';
import { Bus, BatteryCharging, Navigation, Gauge, Zap, MapPin, CheckCircle, ArrowRight, ShieldCheck } from 'lucide-react';

const FLEET = [
  { id: 'BUS-01', model: 'Karsan e-ATA 12m', route: 'Kuzey ⇄ Güney Ring', speedKmh: 24, socPct: 84, regenKwhToday: 18.4, status: 'in_service' },
  { id: 'BUS-02', model: 'Otokar e-KENT C', route: 'Kuzey ⇄ Güney Ring', speedKmh: 18, socPct: 62, regenKwhToday: 14.8, status: 'in_service' },
  { id: 'BUS-03', model: 'Karsan e-JEST Mini', route: 'Kandilli ⇄ Hisarüstü Ekspres', speedKmh: 35, socPct: 91, regenKwhToday: 22.1, status: 'in_service' },
  { id: 'CART-04', model: 'Kampüs İçi Güvenlik EV', route: 'Güney Kampüs Devriye', speedKmh: 12, socPct: 45, regenKwhToday: 4.2, status: 'charging' },
];

export default function TransitFleetPage() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-blue-50 text-blue-700 rounded-lg">
              <Bus size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Elektrikli Kampüs Filosu & Telemetri</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Bebek yokuşu rejeneratif frenleme enerjisi, batarya şarj seviyeleri ve akıllı filo çizelgeleme.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-xl text-xs font-bold text-blue-800">
          <Zap size={15} className="text-blue-600" />
          <span>%100 Sıfır Emisyonlu Elektrikli Ringler</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Toplam Filo</span>
          <div className="text-3xl font-black text-gray-900">4 Araç</div>
          <div className="text-xs text-emerald-600 font-semibold mt-1">3 Serviste • 1 Şarjda</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Rejeneratif Enerji Geri Kazanımı</span>
          <div className="text-3xl font-black text-emerald-700">59.5 kWh</div>
          <div className="text-xs text-gray-500 mt-1">Bebek yokuşu inişinde geri kazanılan elektrik</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Taşınan Günlük Yolcu</span>
          <div className="text-3xl font-black text-blue-700">3,420</div>
          <div className="text-xs text-gray-500 mt-1">Öğrenci & Akademik Personel</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Önlenen Dizel Tüketimi</span>
          <div className="text-3xl font-black text-teal-700">140 Litre</div>
          <div className="text-xs text-gray-500 mt-1">375 kg CO₂e tasarrufu</div>
        </div>
      </div>

      {/* Fleet Vehicles Table */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
          <h3 className="font-bold text-lg text-gray-900">Canlı Ring Araç Telemetrisi</h3>
          <span className="text-xs text-gray-400 font-mono">Fleet MQTT Feed v2.1</span>
        </div>

        <div className="divide-y divide-gray-100">
          {FLEET.map(bus => (
            <div key={bus.id} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-gray-50 transition">
              <div className="flex items-center space-x-4">
                <div className={`p-3 rounded-xl ${bus.status === 'in_service' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                  <Bus size={22} />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold text-sm text-gray-900">{bus.id}</h4>
                    <span className="text-[11px] text-gray-500">• {bus.model}</span>
                  </div>
                  <p className="text-xs text-gray-600 mt-0.5">{bus.route}</p>
                </div>
              </div>

              <div className="flex items-center gap-6 text-xs">
                <div>
                  <span className="text-gray-400 block text-[10px]">Hız</span>
                  <span className="font-bold text-gray-800">{bus.speedKmh} km/h</span>
                </div>
                <div>
                  <span className="text-gray-400 block text-[10px]">Batarya (SoC)</span>
                  <span className="font-bold text-emerald-700">%{bus.socPct}</span>
                </div>
                <div>
                  <span className="text-gray-400 block text-[10px]">Rejeneratif Kazanım</span>
                  <span className="font-bold text-blue-700">+{bus.regenKwhToday} kWh</span>
                </div>
                <div>
                  <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full ${
                    bus.status === 'in_service' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {bus.status === 'in_service' ? 'Hatta Aktif' : 'Şarj Oluyor'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
