'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Building2, ExternalLink, MapPin, Search } from 'lucide-react';
import { getBuildings } from '@/lib/api';
import type { Building } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { buildingTypeLabel, presentBuilding } from '@/lib/campus-directory';

type LiveLocation = { id: string; coords: [number, number]; matched_name: string; osm_url: string; source: string };

export default function BuildingsPage() {
  const { locale, t } = useLocale();
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [locations, setLocations] = useState<Record<string, LiveLocation>>({});
  const [campusFilter, setCampusFilter] = useState<'all' | 'south' | 'north'>('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBuildings().then(setBuildings).catch(() => setBuildings([])).finally(() => setLoading(false));
    fetch('/api/v1/building-locations', { cache: 'no-store' })
      .then(response => response.ok ? response.json() : Promise.reject(new Error('locations')))
      .then((payload: { locations?: LiveLocation[] }) => setLocations(Object.fromEntries((payload.locations ?? []).map(location => [location.id, location]))))
      .catch(() => setLocations({}));
  }, []);

  const filtered = useMemo(() => {
    const term = search.toLocaleLowerCase(locale === 'tr' ? 'tr-TR' : 'en-US').trim();
    return buildings.filter(building => {
      if (campusFilter !== 'all' && building.campus !== campusFilter) return false;
      if (!term) return true;
      const display = presentBuilding(building, locale);
      const typeLabel = buildingTypeLabel(building.type, locale);
      return [display.name, display.code, typeLabel, building.name, building.code].some(value => value.toLocaleLowerCase(locale === 'tr' ? 'tr-TR' : 'en-US').includes(term));
    });
  }, [buildings, campusFilter, locale, search]);

  const southCount = buildings.filter(building => building.campus === 'south').length;
  const northCount = buildings.filter(building => building.campus === 'north').length;
  const verifiedCount = Object.keys(locations).length;

  return (
    <div className="space-y-7">
      <section className="grid gap-6 border-b border-slate-900/10 pb-7 lg:grid-cols-[minmax(0,1fr)_430px] lg:items-end">
        <div><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('Kampüs dizini', 'Campus directory')}</div><h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Binalar', 'Buildings')}</h1><p className="mt-3 max-w-2xl text-[12px] leading-6 text-slate-500">{t('Bina adları ve derslik kodları resmî Boğaziçi dizininden sunulur; harita koordinatları mümkün olduğunda OpenStreetMap ile eşleştirilir. Eşleşmeyen koordinatlar kesin konum gibi gösterilmez.', 'Building names and classroom codes are presented from the official Boğaziçi directory; map coordinates are matched from OpenStreetMap when possible. Unmatched coordinates are not presented as exact locations.')}</p></div>
        <div className="grid grid-cols-3 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4"><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Güney', 'South')}</div><div className="mt-1 font-mono text-xl font-black text-slate-900">{southCount}</div></div><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Kuzey', 'North')}</div><div className="mt-1 font-mono text-xl font-black text-slate-900">{northCount}</div></div><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">OSM</div><div className="mt-1 font-mono text-xl font-black text-emerald-700">{verifiedCount}</div></div></div>
      </section>

      <section className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><label className="relative block sm:w-[380px]"><Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input value={search} onChange={event => setSearch(event.target.value)} placeholder={t('Bina, kod veya tür ara…', 'Search building, code or type…')} className="bc-focus-ring w-full rounded-lg border border-slate-900/10 bg-white py-2.5 pl-9 pr-3 text-[11px] font-semibold text-slate-800 placeholder:text-slate-400" /></label><div className="flex w-fit rounded-lg border border-slate-900/10 bg-white p-1">{(['all', 'south', 'north'] as const).map(campus => <button key={campus} type="button" onClick={() => setCampusFilter(campus)} className={`bc-focus-ring rounded-md px-3 py-1.5 text-[9px] font-bold ${campusFilter === campus ? 'bg-[#102a43] text-white' : 'text-slate-500'}`}>{campus === 'all' ? t('Tümü', 'All') : campus === 'south' ? t('Güney', 'South') : t('Kuzey', 'North')}</button>)}</div></section>

      {loading ? <div className="grid min-h-[280px] place-items-center text-xs font-semibold text-slate-400">{t('Bina dizini yükleniyor…', 'Loading building directory…')}</div> : filtered.length === 0 ? <div className="rounded-xl border border-slate-900/10 bg-white p-10 text-center text-sm font-bold text-slate-500">{t('Bu filtreye uyan bina yok.', 'No building matches this filter.')}</div> : <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{filtered.map(building => {
        const location = locations[building.id];
        const display = presentBuilding(building, locale);
        return <article key={building.id} className="rounded-xl border border-slate-900/10 bg-white p-4 transition hover:border-slate-900/20"><div className="flex items-start justify-between gap-3"><div className="grid h-9 w-9 place-items-center rounded-lg bg-slate-100 text-slate-600"><Building2 size={16} /></div><span className="font-mono text-[9px] font-black text-slate-400">{display.code}</span></div><h2 className="mt-5 text-[16px] font-black tracking-[-0.025em] text-slate-950">{display.name}</h2><div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[10px] text-slate-500"><span className="inline-flex items-center gap-1"><MapPin size={10} /> {building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</span><span>{buildingTypeLabel(building.type, locale)}</span></div><div className="mt-5 border-t border-slate-900/8 pt-3">{location ? <div className="flex items-center justify-between gap-3"><div><div className="text-[9px] font-bold text-emerald-700">{t('OpenStreetMap eşleşmesi', 'OpenStreetMap match')}</div><div className="mt-1 font-mono text-[9px] text-slate-400">{location.coords[0].toFixed(5)}, {location.coords[1].toFixed(5)}</div></div><a href={location.osm_url} target="_blank" rel="noreferrer" className="bc-focus-ring rounded-md p-2 text-slate-400 hover:bg-slate-50 hover:text-slate-800" aria-label={t('OpenStreetMap kaydını aç', 'Open OpenStreetMap record')}><ExternalLink size={12} /></a></div> : <div className="text-[9px] font-semibold leading-4 text-amber-700">{t('Kesin OSM eşleşmesi bekleniyor; mevcut koordinat yedek referanstır.', 'Exact OSM match pending; current coordinate is a fallback reference.')}</div>}</div><Link href={`/buildings/${building.id}`} className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-bold text-[#173f67]">{t('Detay', 'Details')} <ArrowRight size={11} /></Link></article>;
      })}</section>}
    </div>
  );
}
