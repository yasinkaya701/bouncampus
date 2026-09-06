'use client';

import { DashboardData } from '@/lib/types';
import dynamic from 'next/dynamic';
import KPICards from '@/components/Dashboard/KPICards';
import ActionCards from '@/components/Dashboard/ActionCards';
import Timeline from '@/components/Dashboard/Timeline';
import { getDashboard } from '@/lib/api';
import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Wind } from 'lucide-react';

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
    return <div className="flex items-center justify-center h-64">Loading dashboard...</div>;
  }

  // Prepare occupancy data for the bottom chart
  const occupancyData = data.buildings.map(b => ({
    name: b.name,
    occupancy: b.occupancy_ratio ? Math.round(b.occupancy_ratio * 100) : 0,
    campus: b.campus
  })).sort((a, b) => b.occupancy - a.occupancy).slice(0, 10); // Top 10

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Live Campus Data Source Feed Bar */}
      <div className="bg-gradient-to-r from-emerald-50 via-teal-50 to-emerald-50 border border-emerald-200 rounded-xl p-4 shadow-sm">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">
              Live Real-World Campus Feeds
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2 md:gap-4 text-xs text-gray-700">
            {data.live_weather && (
              <div className="bg-white/80 backdrop-blur px-3 py-1.5 rounded-lg border border-emerald-100 flex items-center space-x-1.5 shadow-xs">
                <span>🌤️</span>
                <span>Weather: <strong>{data.live_weather.temperature}°C</strong> ({data.live_weather.humidity}% hum, {data.live_weather.rain ? 'Rain' : 'Dry'})</span>
              </div>
            )}

            {data.live_menu && (
              <div className="bg-white/80 backdrop-blur px-3 py-1.5 rounded-lg border border-emerald-100 flex items-center space-x-1.5 shadow-xs">
                <span>🍽️</span>
                <span>SKS Menu: <strong>{data.live_menu.main_dish}</strong> ({data.live_menu.calories} kcal)</span>
              </div>
            )}

            {data.live_wind && (
              <div className="bg-white/80 backdrop-blur px-3 py-1.5 rounded-lg border border-emerald-100 flex items-center space-x-1.5 shadow-xs">
                <span>💨</span>
                <span>Kilyos Wind Turbine (1.0 MW): <strong>{data.live_wind.wind_speed_kmh} km/h wind</strong></span>
              </div>
            )}

            {data.today_events && data.today_events.length > 0 && (
              <div className="bg-white/80 backdrop-blur px-3 py-1.5 rounded-lg border border-emerald-100 flex items-center space-x-1.5 shadow-xs">
                <span>🎭</span>
                <span>Event: <strong>{data.today_events[0].name.split(':')[0]}</strong></span>
              </div>
            )}
          </div>
        </div>
      </div>

      <KPICards data={data} />

      {/* Kilyos Wind Turbine Real-time Generation Banner */}
      {data.live_wind && (
        <div className="bg-white border border-teal-200 rounded-xl p-4 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="bg-teal-50 text-teal-700 p-2.5 rounded-lg">
              <Wind className="animate-spin" style={{ animationDuration: '8s' }} size={24} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-gray-800 text-sm">Kilyos Sarıtepe 1.0 MW Wind Turbine (Enercon E-44)</h3>
                <span className="text-[10px] bg-teal-100 text-teal-800 font-bold px-2 py-0.5 rounded-full">Live Clean Power</span>
              </div>
              <p className="text-xs text-gray-500 mt-0.5">
                Wind Speed: <strong>{data.live_wind.wind_speed_kmh} km/h</strong> • Clean Power: <strong>{data.live_wind.current_power_kw} kW</strong> • Today&apos;s Clean Energy: <strong>{data.live_wind.daily_clean_mwh} MWh</strong>
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-4 w-full md:w-auto justify-between md:justify-end">
            <div className="text-right">
              <div className="text-xs text-gray-500 font-medium">Campus Grid Offset</div>
              <div className="text-xl font-black text-teal-700">{data.live_wind.campus_electricity_coverage_percent}%</div>
            </div>
            <div className="w-28 bg-gray-100 rounded-full h-3 overflow-hidden">
              <div 
                className="bg-teal-500 h-full rounded-full transition-all duration-1000"
                style={{ width: `${Math.min(100, Math.max(8, data.live_wind.campus_electricity_coverage_percent))}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-800">Campus Map</h2>
            <div className="flex space-x-4 text-xs font-medium">
              <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-green-500 mr-1"></span> &lt;40%</span>
              <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-amber-500 mr-1"></span> 40-70%</span>
              <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-1"></span> &gt;70%</span>
            </div>
          </div>
          <CampusMap buildings={data.buildings} />
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-800">Action Plan</h2>
            <div className="bg-gray-100 p-1 rounded-lg flex text-sm">
              <button 
                onClick={() => setView('cards')} 
                className={`px-3 py-1 rounded-md transition ${view === 'cards' ? 'bg-white shadow-sm font-medium' : 'text-gray-500'}`}
              >
                Cards
              </button>
              <button 
                onClick={() => setView('timeline')} 
                className={`px-3 py-1 rounded-md transition ${view === 'timeline' ? 'bg-white shadow-sm font-medium' : 'text-gray-500'}`}
              >
                Timeline
              </button>
            </div>
          </div>
          
          <div className="h-[400px] overflow-y-auto pr-2 custom-scrollbar">
            {view === 'cards' ? (
              <ActionCards actions={data.actions} />
            ) : (
              <div className="h-full flex items-center pt-8">
                <Timeline actions={data.actions} />
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mt-8">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Building Occupancy Overview (Top 10)</h2>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={occupancyData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} unit="%" />
              <YAxis dataKey="name" type="category" width={150} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(value) => [`${value}%`, 'Occupancy']} />
              <Bar dataKey="occupancy" fill="#059669" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
