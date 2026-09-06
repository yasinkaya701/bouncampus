'use client';

import { DashboardData } from '@/lib/types';
import dynamic from 'next/dynamic';
import KPICards from '@/components/Dashboard/KPICards';
import ActionCards from '@/components/Dashboard/ActionCards';
import Timeline from '@/components/Dashboard/Timeline';
import { getDashboard } from '@/lib/api';
import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Wind, Sun, CloudRain, Utensils, Calendar, ArrowRight, ShieldCheck, Activity, MapPin } from 'lucide-react';
import Link from 'next/link';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [view, setView] = useState<'cards' | 'timeline'>('cards');

  useEffect(() => {
    async function load() {
      const dbData = await getDashboard();
      setData(dbData);
    }
    load();
  }, []);

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center h-96 gap-3 text-slate-500">
        <div className="w-8 h-8 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin"></div>
        <span className="text-xs font-mono font-medium">Boğaziçi telemetri verileri yükleniyor...</span>
      </div>
    );
  }

  // Top 10 occupied buildings
  const occupancyData = data.buildings.map(b => ({
    name: b.name,
    code: b.code,
    occupancy: b.occupancy_ratio ? Math.round(b.occupancy_ratio * 100) : 0,
    campus: b.campus === 'south' ? 'Güney' : 'Kuzey'
  })).sort((a, b) => b.occupancy - a.occupancy).slice(0, 10);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* 1. Institutional Telemetry Ticker (Zero Emojis, Crisp SVG Icons) */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-sm text-slate-200">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3">
          <div className="flex items-center space-x-2 shrink-0">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-bold font-mono tracking-wider text-slate-300 uppercase">
              Canlı Saha Telemetrisi
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 text-xs">
            {/* Weather Metric */}
            <div className="bg-slate-950/80 border border-slate-800 px-3 py-1.5 rounded-xl flex items-center gap-2 font-mono text-slate-300">
              <Sun size={13} className="text-amber-400" />
              <span>Bebek: <strong className="text-white">21.4°C</strong> (%58 Nem)</span>
            </div>

            {/* SKS Dining */}
            <div className="bg-slate-950/80 border border-slate-800 px-3 py-1.5 rounded-xl flex items-center gap-2 font-mono text-slate-300">
              <Utensils size={13} className="text-emerald-400" />
              <span>SKS Canlı Menü: <strong className="text-white">Etli Nohut Yemeği & Pilav</strong> (580 kcal)</span>
            </div>

            {/* Kilyos Turbine */}
            <div className="bg-slate-950/80 border border-slate-800 px-3 py-1.5 rounded-xl flex items-center gap-2 font-mono text-slate-300">
              <Wind size={13} className="text-cyan-400" />
              <span>Kilyos RES: <strong className="text-white">38.4 km/s Rüzgar</strong> (420 kW Güç)</span>
            </div>

            {/* Schedule */}
            <Link 
              href="/courses"
              className="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-3 py-1.5 rounded-xl flex items-center gap-1.5 font-mono text-xs transition"
            >
              <span>OBIKAS: 3.238 Ders Aktif</span>
              <ArrowRight size={11} />
            </Link>
          </div>
        </div>
      </div>

      {/* 2. Primary KPI Cards */}
      <KPICards data={data} />

      {/* 3. Industrial Microgrid Clean Energy Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col md:flex-row items-center justify-between gap-5">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-emerald-400 shrink-0">
            <Wind size={22} className="animate-spin" style={{ animationDuration: '9s' }} />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h3 className="font-bold text-slate-900 text-sm">
                Kilyos Sarıtepe 1.0 MW Rüzgar Enerji Santrali (Enercon E-44)
              </h3>
              <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold font-mono px-2 py-0.5 rounded-md">
                Şebeke Senkronize
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-mono">
              Rüzgar Hızı: <strong className="text-slate-800">10.6 m/s (Poyraz)</strong> • Anlık Üretim: <strong className="text-emerald-700">420 kW</strong> • Günlük Temiz Enerji: <strong className="text-slate-800">6.84 MWh</strong>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-4 w-full md:w-auto justify-between md:justify-end border-t md:border-t-0 pt-3 md:pt-0 border-slate-100">
          <div className="text-right">
            <span className="text-[10px] uppercase font-bold text-slate-400 block font-mono">Kampüs Yük Karşılama</span>
            <span className="text-2xl font-black text-slate-900 font-mono">%34.8</span>
          </div>
          <div className="w-32 bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div className="bg-slate-900 h-full rounded-full" style={{ width: '34.8%' }}></div>
          </div>
        </div>
      </div>

      {/* 4. Main 2-Column: 3D Geospatial Map & Action Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map Panel (2 cols) */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Kampüs Jeo-uzamsal İkizi</h2>
              <p className="text-xs text-slate-500">Cesium 3D Dünya, WebGL Parçacık İkizi ve Katman Haritası</p>
            </div>
            <div className="flex items-center space-x-3 text-xs font-mono font-medium text-slate-500">
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> &lt;%40 Sakin</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-500"></span> %40-70 Normal</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-rose-500"></span> &gt;%70 Yoğun</span>
            </div>
          </div>

          <CampusMap buildings={data.buildings} />
        </div>

        {/* Action Panel (1 col) */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Operasyonel Aksiyonlar</h2>
              <p className="text-xs text-slate-500">Tasarruf & konsolidasyon önerileri</p>
            </div>
            <div className="bg-slate-100 p-1 rounded-xl flex text-xs font-semibold">
              <button 
                onClick={() => setView('cards')} 
                className={`px-3 py-1 rounded-lg transition ${view === 'cards' ? 'bg-white shadow-xs text-slate-900' : 'text-slate-500'}`}
              >
                Kartlar
              </button>
              <button 
                onClick={() => setView('timeline')} 
                className={`px-3 py-1 rounded-lg transition ${view === 'timeline' ? 'bg-white shadow-xs text-slate-900' : 'text-slate-500'}`}
              >
                Çizelge
              </button>
            </div>
          </div>
          
          <div className="h-[520px] overflow-y-auto pr-1">
            {view === 'cards' ? (
              <ActionCards actions={data.actions} />
            ) : (
              <Timeline actions={data.actions} />
            )}
          </div>
        </div>
      </div>

      {/* 5. Building Occupancy Overview (Top 10) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-6 pb-3 border-b border-slate-100">
          <div>
            <h2 className="text-base font-bold text-slate-900">En Yüksek Doluluklu Binalar (İlk 10)</h2>
            <p className="text-xs text-slate-500">OBIKAS ders programı ve yemekhane yoğunluk sıralaması</p>
          </div>
          <Link
            href="/buildings"
            className="text-xs font-bold text-slate-700 hover:text-slate-900 flex items-center gap-1"
          >
            <span>Tüm 21 Binayı İncele</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={occupancyData} layout="vertical" margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
              <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis dataKey="name" type="category" width={160} tick={{ fontSize: 11, fill: '#334155' }} />
              <Tooltip 
                formatter={(value: any) => [`%${value} Dolu`, 'Doluluk']}
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff', fontSize: '12px' }}
              />
              <Bar dataKey="occupancy" fill="#0f172a" radius={[0, 6, 6, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
