'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import {
  Activity,
  ArrowRight,
  BusFront,
  CalendarDays,
  CheckCircle2,
  CloudSun,
  Database,
  ExternalLink,
  ShieldAlert,
  Utensils,
} from 'lucide-react';
import KPICards from '@/components/Dashboard/KPICards';
import ActionCards from '@/components/Dashboard/ActionCards';
import Timeline from '@/components/Dashboard/Timeline';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';

const CampusMap = dynamic(() => import('@/components/Dashboard/CampusMap'), { ssr: false });

const provenanceLabel: Record<string, string> = {
  OFFICIAL_LIVE: 'RESMÎ CANLI',
  OFFICIAL_SNAPSHOT: 'RESMÎ SNAPSHOT',
  EXTERNAL_LIVE: 'HARİCÎ CANLI',
  MODEL_ESTIMATE: 'MODEL TAHMİNİ',
  FALLBACK: 'ERİŞİLEMİYOR',
};

function fmt(value: number | null | undefined, suffix = '') {
  return value == null ? '—' : `${value}${suffix}`;
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [view, setView] = useState<'cards' | 'timeline'>('cards');

  useEffect(() => {
    getDashboard().then(setData);
  }, []);

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center h-96 gap-3 text-slate-500">
        <div className="w-8 h-8 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin" />
        <span className="text-xs font-mono font-medium">Canlı kampüs kaynakları ve karar modeli yükleniyor...</span>
      </div>
    );
  }

  const occupancyData = data.buildings
    .map(b => ({
      name: b.name,
      occupancy: Math.round((b.occupancy_ratio ?? 0) * 100),
    }))
    .sort((a, b) => b.occupancy - a.occupancy)
    .slice(0, 10);

  const degraded = data.data_quality?.mode === 'DEGRADED';

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <section className="bg-slate-950 text-white border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              {degraded ? <ShieldAlert size={17} className="text-amber-400" /> : <CheckCircle2 size={17} className="text-emerald-400" />}
              <span className="text-xs font-black tracking-[0.18em] text-slate-300 uppercase">BOUNCAMPUS Data Trust Layer</span>
            </div>
            <p className="text-xs text-slate-400 mt-2 max-w-2xl">
              Canlı resmî kaynaklar ile model tahminleri ayrı etiketlenir. Doluluk, enerji ve yemek talebi kampüs sensörü ölçümü değil; ders programı ve çevresel girdilerden üretilen karar destek tahminidir.
            </p>
          </div>
          <div className="flex flex-wrap gap-2 text-[11px] font-mono">
            <span className="px-2.5 py-1.5 rounded-lg bg-emerald-950 border border-emerald-800 text-emerald-300">
              {data.data_quality?.official_live_sources ?? 0} resmî canlı kaynak
            </span>
            <span className="px-2.5 py-1.5 rounded-lg bg-sky-950 border border-sky-800 text-sky-300">
              {data.data_quality?.external_live_sources ?? 0} haricî canlı kaynak
            </span>
            <span className={`px-2.5 py-1.5 rounded-lg border ${degraded ? 'bg-amber-950 border-amber-800 text-amber-300' : 'bg-slate-900 border-slate-700 text-slate-300'}`}>
              {degraded ? 'Kısmi kaynak kesintisi' : 'Kaynaklar erişilebilir'}
            </span>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        <div className="bg-white border border-slate-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase"><CloudSun size={15} /> Bebek hava</div>
          <div className="mt-3 text-xl font-black text-slate-900 font-mono">
            {fmt(data.live_weather?.temperature, '°C')}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Nem {fmt(data.live_weather?.humidity, '%')} · Rüzgâr {fmt(data.live_weather?.wind_speed, ' km/h')}
          </p>
          <span className="inline-block mt-3 text-[10px] font-bold font-mono text-sky-700">HARİCÎ CANLI</span>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase"><Utensils size={15} /> SKS menü</div>
          <div className="mt-3 text-sm font-black text-slate-900 line-clamp-2">
            {data.live_menu?.main_dish ?? 'Resmî sayfa erişildi; menü alanı ayrıştırılamadı'}
          </div>
          <p className="text-xs text-slate-500 mt-1">{data.live_menu?.soup ?? 'Çorba alanı yok'} {data.live_menu?.calories ? `· ${data.live_menu.calories} kcal` : ''}</p>
          <span className="inline-block mt-3 text-[10px] font-bold font-mono text-emerald-700">RESMÎ CANLI</span>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase"><BusFront size={15} /> Mekik</div>
          <div className="mt-3 text-xl font-black text-slate-900 font-mono">
            {data.live_shuttle?.next_departure ?? '—'}
          </div>
          <p className="text-xs text-slate-500 mt-1">{data.live_shuttle?.route ?? 'Güney → Kuzey'}</p>
          <span className="inline-block mt-3 text-[10px] font-bold font-mono text-emerald-700">RESMÎ CANLI</span>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase"><Database size={15} /> Ders programı</div>
          <div className="mt-3 text-xl font-black text-slate-900 font-mono">{(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')}</div>
          <p className="text-xs text-slate-500 mt-1">BUIS/ÖBİKAS public schedule snapshot</p>
          <span className="inline-block mt-3 text-[10px] font-bold font-mono text-violet-700">RESMÎ SNAPSHOT</span>
        </div>
      </section>

      <KPICards data={data} />

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-slate-900">Kampüs Operasyon Haritası</h2>
              <p className="text-xs text-slate-500">Doluluk renkleri ders programı tabanlı model tahminidir; sensör ölçümü değildir.</p>
            </div>
            <Link href="/buildings" className="text-xs font-bold text-slate-700 flex items-center gap-1">Binalar <ArrowRight size={13} /></Link>
          </div>
          <CampusMap buildings={data.buildings} />
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Karar Destek Aksiyonları</h2>
              <p className="text-xs text-slate-500">Uygulamadan önce saha/BMS doğrulaması gerekir.</p>
            </div>
            <div className="bg-slate-100 p-1 rounded-xl flex text-xs font-semibold">
              <button onClick={() => setView('cards')} className={`px-3 py-1 rounded-lg ${view === 'cards' ? 'bg-white shadow-xs text-slate-900' : 'text-slate-500'}`}>Kart</button>
              <button onClick={() => setView('timeline')} className={`px-3 py-1 rounded-lg ${view === 'timeline' ? 'bg-white shadow-xs text-slate-900' : 'text-slate-500'}`}>Çizelge</button>
            </div>
          </div>
          <div className="h-[520px] overflow-y-auto pr-1">
            {view === 'cards' ? <ActionCards actions={data.actions} /> : <Timeline actions={data.actions} />}
          </div>
        </div>
      </section>

      <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex items-center justify-between gap-3 mb-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Ders Programından Tahmini Bina Kullanımı</h2>
            <p className="text-xs text-slate-500">İlk 10 bina · oda kapasitesi ve ders saatlerinden türetilmiştir</p>
          </div>
          <Activity size={18} className="text-slate-500" />
        </div>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={occupancyData} layout="vertical" margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
              <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis dataKey="name" type="category" width={160} tick={{ fontSize: 11, fill: '#334155' }} />
              <Tooltip formatter={(value: any) => [`%${value}`, 'Tahmini kullanım']} />
              <Bar dataKey="occupancy" fill="#0f172a" radius={[0, 6, 6, 0]} barSize={14} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-4"><CalendarDays size={17} /><h2 className="font-bold text-slate-900">Akademik Takvim Akışı</h2></div>
          <div className="space-y-2">
            {(data.academic_calendar?.length ? data.academic_calendar : ['Resmî takvim erişilebilir; yapılandırılmış başlık ayrıştırılamadı.']).slice(0, 5).map((item, i) => (
              <div key={`${item}-${i}`} className="text-xs text-slate-600 border-l-2 border-slate-200 pl-3 py-1">{item}</div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-4"><Database size={17} /><h2 className="font-bold text-slate-900">Kaynak & Provenance</h2></div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {(data.sources ?? []).map(source => (
              <a key={source.id} href={source.url} target="_blank" rel="noreferrer" className="flex items-start justify-between gap-4 p-3 rounded-xl border border-slate-100 hover:border-slate-300 transition">
                <div>
                  <div className="text-xs font-bold text-slate-800">{source.label}</div>
                  <div className="text-[11px] text-slate-500 mt-1">{source.detail}</div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className={`text-[9px] font-black font-mono px-2 py-1 rounded ${source.ok ? 'bg-slate-100 text-slate-700' : 'bg-amber-100 text-amber-800'}`}>
                    {provenanceLabel[source.provenance] ?? source.provenance}
                  </span>
                  <ExternalLink size={12} className="text-slate-400" />
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
