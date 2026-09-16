'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { ArrowLeft, Building2, Database, Layers3, Leaf, Loader2, MapPin, Sparkles, UsersRound, Zap } from 'lucide-react';
import { getBuildings, getEnergy, getOccupancy } from '@/lib/api';
import type { Building, EnergyForecast, OccupancyForecast } from '@/lib/types';

function EmptyModelState({ title, detail }: { title: string; detail: string }) {
  return (
    <div className="grid h-[260px] place-items-center rounded-[20px] border border-dashed border-slate-950/15 bg-[#f4f5f2]/70 p-6 text-center">
      <div className="max-w-xs"><Database size={22} className="mx-auto text-slate-300" /><div className="mt-3 text-[11px] font-black text-slate-700">{title}</div><div className="mt-1 text-[10px] leading-relaxed text-slate-500">{detail}</div></div>
    </div>
  );
}

export default function BuildingDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [building, setBuilding] = useState<Building | null>(null);
  const [occupancy, setOccupancy] = useState<OccupancyForecast | null>(null);
  const [energy, setEnergy] = useState<EnergyForecast | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getBuildings(), getOccupancy(undefined, id), getEnergy()])
      .then(([buildings, occupancies, energies]) => {
        setBuilding(buildings.find(item => item.id === id) ?? null);
        setOccupancy(occupancies.find(item => item.building_id === id) ?? null);
        setEnergy(energies.find(item => item.building_id === id) ?? null);
      })
      .finally(() => setLoading(false));
  }, [id]);

  const occupancySeries = occupancy?.total_hourly ?? occupancy?.hourly ?? [];
  const energySeries = useMemo(() => (energy?.hourly_forecast ?? [])
    .filter(item => item.hour >= 6 && item.hour <= 22)
    .map(item => ({ time: `${String(item.hour).padStart(2, '0')}:00`, load: Math.round(item.total_kwh * 10) / 10 })), [energy]);

  if (loading) {
    return <div className="grid min-h-[62vh] place-items-center"><div className="text-center"><Loader2 className="mx-auto animate-spin text-blue-600" size={28} /><p className="mt-3 text-[10px] font-bold text-slate-400">Loading building intelligence</p></div></div>;
  }

  if (!building) {
    return <div className="bc-surface rounded-[28px] p-12 text-center"><Building2 size={28} className="mx-auto text-slate-300" /><h1 className="mt-4 text-lg font-black text-slate-800">Building not found</h1><Link href="/buildings" className="mt-4 inline-flex items-center gap-1 text-[10px] font-black text-blue-700"><ArrowLeft size={11} /> Back to campus</Link></div>;
  }

  const modeledUse = building.occupancy_ratio == null ? null : Math.round(building.occupancy_ratio * 100);

  return (
    <div className="space-y-4 md:space-y-5">
      <Link href="/buildings" className="bc-focus-ring inline-flex items-center gap-1.5 rounded-full border border-slate-950/10 bg-white/70 px-3 py-1.5 text-[9px] font-black text-slate-600"><ArrowLeft size={10} /> Campus inventory</Link>

      <section className="bc-surface-dark relative overflow-hidden rounded-[30px] px-5 py-7 text-white sm:px-7 lg:px-9 lg:py-9">
        <div className="pointer-events-none absolute -right-20 -top-24 h-72 w-72 rounded-full bg-blue-500/15 blur-3xl" />
        <div className="relative flex flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="flex flex-wrap items-center gap-2"><span className="bc-chip border-white/10 bg-white/5 text-slate-300"><Building2 size={10} /> {building.code}</span><span className="bc-chip border-white/10 bg-white/5 text-slate-300"><MapPin size={10} /> {building.campus === 'south' ? 'GÜNEY' : 'KUZEY'} CAMPUS</span></div>
            <h1 className="mt-6 text-[38px] font-black leading-[0.98] tracking-[-0.055em] sm:text-[48px]">{building.name}</h1>
            <p className="mt-4 max-w-xl text-[12px] leading-relaxed text-slate-400">{building.type} · structural inventory and model-derived operational signals. Occupancy values shown here are not live people-counter telemetry.</p>
          </div>
          <div className="grid grid-cols-3 gap-2 lg:min-w-[390px]">
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.15em] text-slate-500">Capacity</div><div className="mt-2 font-mono text-2xl font-black">{building.total_capacity.toLocaleString('tr-TR')}</div></div>
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.15em] text-slate-500">Floors</div><div className="mt-2 font-mono text-2xl font-black text-blue-300">{building.floors}</div></div>
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.15em] text-slate-500">Model use</div><div className="mt-2 font-mono text-2xl font-black text-emerald-300">{modeledUse == null ? '—' : `${modeledUse}%`}</div></div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="mb-5 flex items-start justify-between"><div><div className="bc-eyebrow">Utilization model</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Schedule-derived demand</h2><p className="mt-1 text-[10px] text-slate-500">Hourly model output when the occupancy endpoint is available.</p></div><span className="bc-chip border-violet-200 bg-violet-50 text-violet-700"><Sparkles size={10} /> MODEL</span></div>
          {occupancySeries.length ? (
            <div className="h-[270px]"><ResponsiveContainer width="100%" height="100%"><BarChart data={occupancySeries} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}><CartesianGrid strokeDasharray="2 6" vertical={false} stroke="rgba(15,23,42,0.08)" /><XAxis dataKey="hour" tickFormatter={value => `${value}:00`} axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><Tooltip contentStyle={{ borderRadius: '14px', borderColor: 'rgba(15,23,42,0.1)', fontSize: '10px' }} /><Bar dataKey="occupancy_count" fill="#2f5cff" radius={[6,6,0,0]} barSize={12} /></BarChart></ResponsiveContainer></div>
          ) : <EmptyModelState title="No occupancy model payload" detail="The operational occupancy endpoint returned no building series. No synthetic floor or people counts were substituted." />}
        </div>

        <div className="bc-surface rounded-[28px] p-5 sm:p-6">
          <div className="mb-5 flex items-start justify-between"><div><div className="bc-eyebrow">Energy model</div><h2 className="mt-1 text-xl font-black tracking-[-0.035em] text-[#0a1020]">Modeled hourly load</h2><p className="mt-1 text-[10px] text-slate-500">Physics-lite output; not a utility or BMS meter stream.</p></div><Zap size={17} className="text-slate-400" /></div>
          {energySeries.length ? (
            <div className="h-[270px]"><ResponsiveContainer width="100%" height="100%"><LineChart data={energySeries} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}><CartesianGrid strokeDasharray="2 6" vertical={false} stroke="rgba(15,23,42,0.08)" /><XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><Tooltip contentStyle={{ borderRadius: '14px', borderColor: 'rgba(15,23,42,0.1)', fontSize: '10px' }} /><Line type="monotone" dataKey="load" stroke="#12805c" strokeWidth={2.5} dot={false} /></LineChart></ResponsiveContainer></div>
          ) : <EmptyModelState title="No hourly energy payload" detail="No fallback curve was invented. Connect or restore the energy model endpoint to populate this panel." />}
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <div className="bc-surface rounded-[24px] p-5"><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-slate-400"><UsersRound size={11} /> Occupancy source</div><div className="mt-4 text-sm font-black text-slate-800">{occupancy ? 'Model payload available' : 'Unavailable'}</div><p className="mt-2 text-[10px] leading-relaxed text-slate-500">Uses timetable/model endpoint when available. It is not a turnstile or Wi‑Fi occupancy feed.</p></div>
        <div className="bc-surface rounded-[24px] p-5"><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-slate-400"><Layers3 size={11} /> Floor detail</div><div className="mt-4 text-sm font-black text-slate-800">{occupancy?.by_floor?.length ? `${occupancy.by_floor.length} modeled floors` : 'No floor model payload'}</div><p className="mt-2 text-[10px] leading-relaxed text-slate-500">Floor-level utilization is only shown when the endpoint returns it; no arbitrary 30% fallback is used.</p></div>
        <div className="bc-surface rounded-[24px] p-5"><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-slate-400"><Leaf size={11} /> Optimization</div><div className="mt-4 text-sm font-black text-slate-800">{energy?.saving_percent != null ? `${energy.saving_percent.toFixed(1)}% modeled potential` : 'Awaiting model output'}</div><p className="mt-2 text-[10px] leading-relaxed text-slate-500">Savings are model potential, not verified utility savings. Field validation is required before action.</p></div>
      </section>
    </div>
  );
}
