'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { ArrowLeft, Building2, Database, ExternalLink, Loader2, MapPin } from 'lucide-react';
import { getBuildings, getEnergy, getOccupancy } from '@/lib/api';
import type { Building, EnergyForecast, OccupancyForecast } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { buildingTypeLabel, presentBuilding } from '@/lib/campus-directory';

type LiveLocation = { id: string; coords: [number, number]; matched_name: string; osm_url: string; source: string };

function EmptyState({ text }: { text: string }) {
  return <div className="grid h-[250px] place-items-center border border-dashed border-slate-300 bg-white p-6 text-center"><div><Database size={20} className="mx-auto text-slate-300" /><p className="mt-2 max-w-xs text-[10px] leading-5 text-slate-500">{text}</p></div></div>;
}

export default function BuildingDetailPage() {
  const { locale, t } = useLocale();
  const params = useParams();
  const id = params.id as string;
  const [building, setBuilding] = useState<Building | null>(null);
  const [occupancy, setOccupancy] = useState<OccupancyForecast | null>(null);
  const [energy, setEnergy] = useState<EnergyForecast | null>(null);
  const [location, setLocation] = useState<LiveLocation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getBuildings(),
      getOccupancy(undefined, id),
      getEnergy(),
      fetch('/api/v1/building-locations', { cache: 'no-store' }).then(response => response.ok ? response.json() : { locations: [] }),
    ]).then(([buildings, occupancies, energies, locationsPayload]) => {
      setBuilding(buildings.find(item => item.id === id) ?? null);
      setOccupancy(occupancies.find(item => item.building_id === id) ?? null);
      setEnergy(energies.find(item => item.building_id === id) ?? null);
      setLocation(((locationsPayload as { locations?: LiveLocation[] }).locations ?? []).find(item => item.id === id) ?? null);
    }).finally(() => setLoading(false));
  }, [id]);

  const occupancySeries = occupancy?.total_hourly ?? occupancy?.hourly ?? [];
  const energySeries = useMemo(() => (energy?.hourly_forecast ?? []).filter(item => item.hour >= 6 && item.hour <= 22).map(item => ({ time: `${String(item.hour).padStart(2, '0')}:00`, load: Math.round(item.total_kwh * 10) / 10 })), [energy]);

  if (loading) return <div className="grid min-h-[58vh] place-items-center"><Loader2 className="animate-spin text-slate-400" size={24} /></div>;
  if (!building) return <div className="p-10 text-center"><Building2 size={24} className="mx-auto text-slate-300" /><h1 className="mt-3 text-lg font-black">{t('Bina bulunamadı', 'Building not found')}</h1><Link href="/buildings" className="mt-3 inline-flex items-center gap-1 text-[10px] font-bold text-[#173f67]"><ArrowLeft size={10} /> {t('Binalara dön', 'Back to buildings')}</Link></div>;

  const display = presentBuilding(building, locale);
  const modeledUse = building.occupancy_ratio == null ? null : Math.round(building.occupancy_ratio * 100);

  return <div className="space-y-7"><Link href="/buildings" className="inline-flex items-center gap-1 text-[10px] font-bold text-[#173f67]"><ArrowLeft size={10} /> {t('Bina dizini', 'Building directory')}</Link><section className="grid gap-6 border-b border-slate-900/10 pb-7 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-end"><div><div className="flex flex-wrap items-center gap-2 text-[9px] font-bold text-slate-400"><span>{display.code}</span><span>·</span><span>{building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</span><span>·</span><span>{buildingTypeLabel(building.type, locale)}</span></div><h1 className="mt-3 text-[34px] font-black leading-[1.04] tracking-[-0.05em] text-slate-950 sm:text-[44px]">{display.name}</h1><p className="mt-3 max-w-2xl text-[11px] leading-5 text-slate-500">{t('Bu sayfa konum ve model çıktısını ayırır. Kapasite/kat gibi yapılandırma değerleri resmî bina gerçeği olarak öne çıkarılmaz.', 'This page separates location evidence from model output. Configuration values such as capacity or floor count are not promoted as authoritative building facts.')}</p></div><div className="border-y border-slate-900/10 py-4">{location ? <div><div className="flex items-center gap-1.5 text-[10px] font-black text-emerald-700"><MapPin size={11} /> {t('OpenStreetMap eşleşmesi', 'OpenStreetMap match')}</div><div className="mt-2 font-mono text-[10px] text-slate-500">{location.coords[0].toFixed(6)}, {location.coords[1].toFixed(6)}</div><a href={location.osm_url} target="_blank" rel="noreferrer" className="mt-2 inline-flex items-center gap-1 text-[9px] font-bold text-[#173f67]">{t('Kaydı aç', 'Open record')} <ExternalLink size={9} /></a></div> : <div className="text-[10px] font-semibold leading-5 text-amber-700">{t('Kesin OSM eşleşmesi bulunamadı; yedek koordinat kesin konum olarak kabul edilmemelidir.', 'No exact OSM match was found; the fallback coordinate must not be treated as exact.')}</div>}</div></section><section className="grid gap-6 xl:grid-cols-2"><div><div className="mb-3"><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Program tabanlı model', 'Schedule-derived model')}</div><h2 className="mt-1 text-lg font-black">{t('Tahmini kullanım', 'Estimated utilization')}</h2></div>{occupancySeries.length ? <div className="h-[280px] border border-slate-900/10 bg-white p-2"><ResponsiveContainer width="100%" height="100%"><BarChart data={occupancySeries} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}><CartesianGrid strokeDasharray="2 6" vertical={false} stroke="rgba(15,23,42,0.08)" /><XAxis dataKey="hour" tickFormatter={value => `${value}:00`} axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><Tooltip contentStyle={{ fontSize: '10px' }} /><Bar dataKey="occupancy_count" fill="#173f67" radius={[4,4,0,0]} barSize={12} /></BarChart></ResponsiveContainer></div> : <EmptyState text={t('Bu bina için doluluk modeli verisi yok. Sentetik kişi sayısı üretilmedi.', 'No occupancy-model series is available for this building. No synthetic people count was substituted.')} />}<div className="mt-2 text-[9px] text-slate-400">{modeledUse == null ? t('Anlık model oranı yok', 'No current modeled ratio') : `${t('Mevcut model oranı', 'Current modeled ratio')}: ${modeledUse}%`}</div></div><div><div className="mb-3"><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Enerji modeli', 'Energy model')}</div><h2 className="mt-1 text-lg font-black">{t('Saatlik model yükü', 'Modeled hourly load')}</h2></div>{energySeries.length ? <div className="h-[280px] border border-slate-900/10 bg-white p-2"><ResponsiveContainer width="100%" height="100%"><LineChart data={energySeries} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}><CartesianGrid strokeDasharray="2 6" vertical={false} stroke="rgba(15,23,42,0.08)" /><XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#94a3b8' }} /><Tooltip contentStyle={{ fontSize: '10px' }} /><Line type="monotone" dataKey="load" stroke="#0f766e" strokeWidth={2.2} dot={false} /></LineChart></ResponsiveContainer></div> : <EmptyState text={t('Saatlik enerji modeli verisi yok. Yedek eğri uydurulmadı.', 'No hourly energy-model series is available. No fallback curve was invented.')} />}<div className="mt-2 text-[9px] text-slate-400">{t('Bu akış sayaç veya BMS telemetrisi değildir.', 'This is not meter or BMS telemetry.')}</div></div></section></div>;
}
