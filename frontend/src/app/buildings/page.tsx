'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Building2, Layers3, MapPin, Search, UsersRound } from 'lucide-react';
import { getBuildings } from '@/lib/api';
import type { Building } from '@/lib/types';

export default function BuildingsPage() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [campusFilter, setCampusFilter] = useState<'all' | 'south' | 'north'>('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBuildings()
      .then(setBuildings)
      .catch(() => setBuildings([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const term = search.toLocaleLowerCase('tr-TR').trim();
    return buildings.filter(building => {
      if (campusFilter !== 'all' && building.campus !== campusFilter) return false;
      if (!term) return true;
      return [building.name, building.code, building.type].some(value => value.toLocaleLowerCase('tr-TR').includes(term));
    });
  }, [buildings, campusFilter, search]);

  const totalCapacity = buildings.reduce((sum, building) => sum + building.total_capacity, 0);
  const totalFloors = buildings.reduce((sum, building) => sum + building.floors, 0);

  return (
    <div className="space-y-4 md:space-y-5">
      <section className="bc-surface-dark relative overflow-hidden rounded-[30px] px-5 py-7 text-white sm:px-7 lg:px-9 lg:py-9">
        <div className="pointer-events-none absolute -right-20 -top-28 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />
        <div className="relative flex flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <span className="bc-chip border-white/10 bg-white/5 text-slate-300"><Building2 size={10} /> CAMPUS INVENTORY</span>
            <h1 className="mt-6 text-[38px] font-black leading-[0.98] tracking-[-0.055em] sm:text-[48px]">One campus.<br /><span className="text-emerald-300">A network of operating spaces.</span></h1>
            <p className="mt-4 max-w-2xl text-[12px] leading-relaxed text-slate-400">Güney ve Kuzey Kampüs bina envanterini kapasite, kat sayısı ve kullanım tipleriyle keşfet. Doluluk tahminleri ayrı karar katmanında modellenir; bu ekran yapısal bina metadata’sını gösterir.</p>
          </div>

          <div className="grid grid-cols-3 gap-2 lg:min-w-[380px]">
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.16em] text-slate-500">Buildings</div><div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em]">{buildings.length || '—'}</div></div>
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.16em] text-slate-500">Capacity</div><div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em] text-blue-300">{totalCapacity ? totalCapacity.toLocaleString('tr-TR') : '—'}</div></div>
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4"><div className="text-[8px] font-black uppercase tracking-[0.16em] text-slate-500">Floors</div><div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em] text-emerald-300">{totalFloors || '—'}</div></div>
          </div>
        </div>
      </section>

      <section className="bc-surface rounded-[24px] p-3 sm:p-4">
        <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
          <label className="relative block lg:w-[360px]">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input value={search} onChange={event => setSearch(event.target.value)} placeholder="Search building, code or type…" className="bc-focus-ring w-full rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] py-2.5 pl-10 pr-3 text-[11px] font-semibold text-slate-800 placeholder:text-slate-400" />
          </label>

          <div className="flex w-fit rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] p-1">
            {(['all', 'south', 'north'] as const).map(campus => (
              <button key={campus} type="button" onClick={() => setCampusFilter(campus)} className={`bc-focus-ring rounded-[10px] px-3 py-1.5 text-[9px] font-black transition ${campusFilter === campus ? 'bg-[#0b1226] text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>
                {campus === 'all' ? `All ${buildings.length}` : campus === 'south' ? 'Güney' : 'Kuzey'}
              </button>
            ))}
          </div>
        </div>
      </section>

      {loading ? (
        <div className="grid min-h-[320px] place-items-center"><div className="text-center"><div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-300 border-t-blue-600" /><p className="mt-3 text-[10px] font-bold text-slate-400">Loading campus inventory</p></div></div>
      ) : filtered.length === 0 ? (
        <div className="bc-surface rounded-[26px] p-12 text-center"><Building2 size={28} className="mx-auto text-slate-300" /><h2 className="mt-4 text-sm font-black text-slate-800">No building matches this view.</h2></div>
      ) : (
        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((building, index) => (
            <Link key={building.id} href={`/buildings/${building.id}`} className="bc-surface group relative overflow-hidden rounded-[24px] p-5 transition duration-300 hover:-translate-y-1 hover:border-slate-950/15 hover:shadow-[0_18px_44px_rgba(10,16,32,0.08)]">
              <div className="flex items-start justify-between gap-4">
                <div className="grid h-10 w-10 place-items-center rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] text-slate-700 transition group-hover:bg-[#0b1226] group-hover:text-white"><Building2 size={17} /></div>
                <div className="flex items-center gap-2"><span className="font-mono text-[9px] font-black text-slate-300">{String(index + 1).padStart(2, '0')}</span><span className="rounded-full border border-slate-950/10 bg-[#f4f5f2] px-2 py-1 font-mono text-[9px] font-black text-slate-500">{building.code}</span></div>
              </div>

              <h2 className="mt-6 text-lg font-black tracking-[-0.035em] text-[#0a1020] transition group-hover:text-blue-700">{building.name}</h2>
              <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[10px] font-semibold text-slate-500"><span className="inline-flex items-center gap-1"><MapPin size={10} /> {building.campus === 'south' ? 'Güney Kampüs' : 'Kuzey Kampüs'}</span><span>{building.type}</span></div>

              <div className="mt-6 grid grid-cols-2 gap-2 border-t border-slate-900/10 pt-4">
                <div><div className="flex items-center gap-1 text-[8px] font-black uppercase tracking-[0.14em] text-slate-400"><UsersRound size={9} /> Capacity</div><div className="mt-1 font-mono text-base font-black text-slate-800">{building.total_capacity.toLocaleString('tr-TR')}</div></div>
                <div><div className="flex items-center gap-1 text-[8px] font-black uppercase tracking-[0.14em] text-slate-400"><Layers3 size={9} /> Floors</div><div className="mt-1 font-mono text-base font-black text-slate-800">{building.floors}</div></div>
              </div>

              <div className="mt-5 flex items-center justify-between text-[9px] font-black uppercase tracking-[0.1em] text-slate-400 transition group-hover:text-slate-700"><span>Open building intelligence</span><ArrowRight size={12} /></div>
            </Link>
          ))}
        </section>
      )}
    </div>
  );
}
