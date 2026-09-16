'use client';

import { useEffect, useMemo, useState } from 'react';
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from 'react-leaflet';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { Box, ExternalLink, Globe2, Map as MapIcon, MapPin } from 'lucide-react';
import type { Building } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { presentBuilding } from '@/lib/campus-directory';

const CampusCesiumMap = dynamic(() => import('./CampusCesiumMap'), { ssr: false, loading: () => <MapLoading /> });
const CampusMap3D = dynamic(() => import('./CampusMap3D'), { ssr: false, loading: () => <MapLoading /> });

function MapLoading() {
  return <div className="grid h-[520px] w-full place-items-center rounded-xl bg-slate-100 text-xs font-semibold text-slate-400">Map / Harita…</div>;
}

function getColor(occupancyRatio?: number) {
  if (occupancyRatio == null) return '#64748b';
  if (occupancyRatio < 0.4) return '#0f766e';
  if (occupancyRatio <= 0.7) return '#a16207';
  return '#b91c1c';
}

function MapViewController({ focusCoords, zoom }: { focusCoords: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => { map.flyTo(focusCoords, zoom, { duration: 0.75 }); }, [focusCoords, zoom, map]);
  return null;
}

const TILE_LAYERS = {
  satellite: { url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attribution: 'Tiles © Esri' },
  street: { url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attribution: '© OpenStreetMap contributors' },
} as const;

type MapMode = '2d' | 'cesium' | '3d';
type CampusFocus = 'all' | 'south' | 'north';
type TileType = keyof typeof TILE_LAYERS;
type LiveLocation = { id: string; coords: [number, number]; matched_name: string; osm_url: string; source: string };

type PositionedBuilding = Building & { liveLocation?: LiveLocation };

export default function CampusMap({ buildings }: { buildings: Building[] }) {
  const { locale, t } = useLocale();
  const [mounted, setMounted] = useState(false);
  const [mapMode, setMapMode] = useState<MapMode>('2d');
  const [tileType, setTileType] = useState<TileType>('street');
  const [focus, setFocus] = useState<CampusFocus>('all');
  const [mapCenter, setMapCenter] = useState<[number, number]>([41.0849, 29.0488]);
  const [zoomLevel, setZoomLevel] = useState(16);
  const [locations, setLocations] = useState<Record<string, LiveLocation>>({});

  useEffect(() => setMounted(true), []);
  useEffect(() => {
    fetch('/api/v1/building-locations', { cache: 'no-store' })
      .then(response => response.ok ? response.json() : Promise.reject(new Error('location source')))
      .then((payload: { locations?: LiveLocation[] }) => setLocations(Object.fromEntries((payload.locations ?? []).map(location => [location.id, location]))))
      .catch(() => setLocations({}));
  }, []);

  const positionedBuildings = useMemo<PositionedBuilding[]>(() => buildings.map(building => {
    const location = locations[building.id];
    const display = presentBuilding(building, locale);
    return {
      ...building,
      name: display.name,
      code: display.code,
      coords: location?.coords ?? building.coords,
      liveLocation: location,
    };
  }), [buildings, locale, locations]);

  const focusCampus = (next: CampusFocus) => {
    setFocus(next);
    if (next === 'south') {
      setMapCenter([41.0836, 29.0520]);
      setZoomLevel(17);
    } else if (next === 'north') {
      setMapCenter([41.0863, 29.0444]);
      setZoomLevel(17);
    } else {
      setMapCenter([41.0849, 29.0488]);
      setZoomLevel(16);
    }
  };

  if (!mounted) return <MapLoading />;

  return (
    <div>
      <div className="mb-3 flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex w-fit items-center gap-1 rounded-lg border border-slate-900/10 bg-slate-50 p-1">
          <button type="button" onClick={() => setMapMode('2d')} className={`bc-focus-ring flex items-center gap-1.5 rounded-md px-3 py-1.5 text-[10px] font-bold ${mapMode === '2d' ? 'bg-white text-slate-950 shadow-sm' : 'text-slate-500'}`}><MapIcon size={11} /> {t('Harita', 'Map')}</button>
          <button type="button" onClick={() => setMapMode('cesium')} className={`bc-focus-ring flex items-center gap-1.5 rounded-md px-3 py-1.5 text-[10px] font-bold ${mapMode === 'cesium' ? 'bg-white text-slate-950 shadow-sm' : 'text-slate-500'}`}><Globe2 size={11} /> {t('Küre', 'Globe')}</button>
          <button type="button" onClick={() => setMapMode('3d')} className={`bc-focus-ring flex items-center gap-1.5 rounded-md px-3 py-1.5 text-[10px] font-bold ${mapMode === '3d' ? 'bg-white text-slate-950 shadow-sm' : 'text-slate-500'}`}><Box size={11} /> 3D</button>
        </div>

        {mapMode === '2d' && (
          <div className="flex flex-wrap items-center gap-1.5">
            <div className="flex items-center gap-1 rounded-lg border border-slate-900/10 bg-white p-1">
              {(['all', 'south', 'north'] as const).map(item => (
                <button key={item} type="button" onClick={() => focusCampus(item)} className={`bc-focus-ring rounded-md px-2.5 py-1 text-[9px] font-bold ${focus === item ? 'bg-[#102a43] text-white' : 'text-slate-500'}`}>
                  {item === 'all' ? t('Tümü', 'All') : item === 'south' ? t('Güney', 'South') : t('Kuzey', 'North')}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-1 rounded-lg border border-slate-900/10 bg-white p-1">
              {(['street', 'satellite'] as const).map(item => (
                <button key={item} type="button" onClick={() => setTileType(item)} className={`bc-focus-ring rounded-md px-2.5 py-1 text-[9px] font-bold ${tileType === item ? 'bg-slate-100 text-slate-950' : 'text-slate-500'}`}>
                  {item === 'street' ? t('Sokak', 'Street') : t('Uydu', 'Satellite')}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {mapMode === 'cesium' ? (
        <div className="overflow-hidden rounded-xl"><CampusCesiumMap buildings={positionedBuildings} /></div>
      ) : mapMode === '3d' ? (
        <div className="overflow-hidden rounded-xl"><CampusMap3D buildings={positionedBuildings} /></div>
      ) : (
        <div className="relative h-[520px] w-full overflow-hidden rounded-xl border border-slate-900/10 bg-slate-100">
          <MapContainer center={mapCenter} zoom={zoomLevel} style={{ height: '100%', width: '100%' }}>
            <MapViewController focusCoords={mapCenter} zoom={zoomLevel} />
            <TileLayer attribution={TILE_LAYERS[tileType].attribution} url={TILE_LAYERS[tileType].url} />
            {positionedBuildings.map(building => {
              const verified = Boolean(building.liveLocation);
              return (
                <CircleMarker key={building.id} center={building.coords} pathOptions={{ fillColor: verified ? getColor(building.occupancy_ratio) : '#f8fafc', color: verified ? '#ffffff' : '#b45309', weight: verified ? 2 : 2.5, fillOpacity: 0.9 }} radius={verified ? 8 : 6}>
                  <Popup>
                    <div className="min-w-[220px] p-1 font-sans">
                      <div className="flex items-start justify-between gap-3"><div><div className="text-sm font-black text-slate-950">{building.name}</div><div className="mt-1 text-[10px] font-semibold text-slate-500">{building.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</div></div><span className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-[9px] font-black text-slate-500">{building.code}</span></div>
                      <div className="mt-3 border-t border-slate-200 pt-3 text-[10px] leading-4 text-slate-500">{verified ? <><div className="flex items-center gap-1.5 font-bold text-emerald-700"><MapPin size={10} /> {t('Konum OpenStreetMap üzerinden eşleştirildi', 'Location matched from OpenStreetMap')}</div><a href={building.liveLocation?.osm_url} target="_blank" rel="noreferrer" className="mt-1.5 inline-flex items-center gap-1 text-slate-500 underline underline-offset-2">{t('Kaydı aç', 'Open source')} <ExternalLink size={9} /></a></> : <div className="font-semibold text-amber-700">{t('Kesin OSM eşleşmesi bulunamadı; yedek kampüs konumu gösteriliyor.', 'No exact OSM match was found; the fallback campus position is shown.')}</div>}</div>
                      <div className="mt-3 text-[9px] text-slate-400">{t('Kullanım rengi ders programı tabanlı modeldir; canlı kişi sayacı değildir.', 'Utilization color is schedule-derived; it is not a live people counter.')}</div>
                      <Link href={`/buildings/${building.id}`} className="mt-3 flex items-center justify-between rounded-lg bg-[#102a43] px-3 py-2 text-[10px] font-bold text-white">{t('Bina detayını aç', 'Open building detail')} <span>→</span></Link>
                    </div>
                  </Popup>
                </CircleMarker>
              );
            })}
          </MapContainer>
          <div className="pointer-events-none absolute bottom-3 left-3 z-[500] rounded-md border border-slate-900/10 bg-white/90 px-2.5 py-1.5 text-[9px] font-semibold text-slate-600 backdrop-blur">{t('Dolu: OSM eşleşmesi · Turuncu çerçeve: yedek konum', 'Filled: OSM match · Amber outline: fallback position')}</div>
        </div>
      )}
    </div>
  );
}
