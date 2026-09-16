'use client';

import { useEffect, useState } from 'react';
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from 'react-leaflet';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { Box, Globe2, Layers3, Map as MapIcon, Sparkles } from 'lucide-react';
import type { Building } from '@/lib/types';

const CampusCesiumMap = dynamic(() => import('./CampusCesiumMap'), {
  ssr: false,
  loading: () => <MapLoading label="3D globe is loading" />,
});

const CampusMap3D = dynamic(() => import('./CampusMap3D'), {
  ssr: false,
  loading: () => <MapLoading label="Digital twin is loading" />,
});

function MapLoading({ label }: { label: string }) {
  return (
    <div className="grid h-[520px] w-full place-items-center rounded-[20px] bg-[#0b1226] text-white">
      <div className="text-center">
        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-white/20 border-t-blue-300" />
        <p className="mt-3 text-xs font-bold">{label}</p>
        <p className="mt-1 font-mono text-[9px] text-slate-500">preparing campus geometry</p>
      </div>
    </div>
  );
}

function getColor(occupancyRatio?: number) {
  if (occupancyRatio == null) return '#94a3b8';
  if (occupancyRatio < 0.4) return '#12805c';
  if (occupancyRatio <= 0.7) return '#b96b13';
  return '#c54848';
}

function MapViewController({ focusCoords, zoom }: { focusCoords: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(focusCoords, zoom, { duration: 0.9 });
  }, [focusCoords, zoom, map]);
  return null;
}

const TILE_LAYERS = {
  satellite: {
    label: 'Satellite',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles © Esri',
  },
  street: {
    label: 'Street',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '© OpenStreetMap contributors',
  },
  dark: {
    label: 'Dark',
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '© CARTO',
  },
} as const;

type MapMode = '2d' | 'cesium' | '3d';
type CampusFocus = 'all' | 'south' | 'north';
type TileType = keyof typeof TILE_LAYERS;

export default function CampusMap({ buildings }: { buildings: Building[] }) {
  const [mounted, setMounted] = useState(false);
  const [mapMode, setMapMode] = useState<MapMode>('2d');
  const [tileType, setTileType] = useState<TileType>('satellite');
  const [focus, setFocus] = useState<CampusFocus>('all');
  const [mapCenter, setMapCenter] = useState<[number, number]>([41.085, 29.0475]);
  const [zoomLevel, setZoomLevel] = useState(16);

  useEffect(() => setMounted(true), []);

  const focusCampus = (next: CampusFocus) => {
    setFocus(next);
    if (next === 'south') {
      setMapCenter([41.0833, 29.0508]);
      setZoomLevel(17);
    } else if (next === 'north') {
      setMapCenter([41.0867, 29.0442]);
      setZoomLevel(17);
    } else {
      setMapCenter([41.085, 29.0475]);
      setZoomLevel(16);
    }
  };

  if (!mounted) return <MapLoading label="Campus map is loading" />;

  return (
    <div>
      <div className="mb-3 flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex w-fit items-center gap-1 rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] p-1">
          <button type="button" onClick={() => setMapMode('2d')} className={`bc-focus-ring flex items-center gap-1.5 rounded-[10px] px-3 py-1.5 text-[10px] font-black transition ${mapMode === '2d' ? 'bg-white text-[#0a1020] shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>
            <MapIcon size={11} /> Map
          </button>
          <button type="button" onClick={() => setMapMode('cesium')} className={`bc-focus-ring flex items-center gap-1.5 rounded-[10px] px-3 py-1.5 text-[10px] font-black transition ${mapMode === 'cesium' ? 'bg-white text-[#0a1020] shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>
            <Globe2 size={11} /> Globe
          </button>
          <button type="button" onClick={() => setMapMode('3d')} className={`bc-focus-ring flex items-center gap-1.5 rounded-[10px] px-3 py-1.5 text-[10px] font-black transition ${mapMode === '3d' ? 'bg-white text-[#0a1020] shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>
            <Box size={11} /> Twin
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          {mapMode === '2d' ? (
            <>
              <div className="flex items-center gap-1 rounded-[13px] border border-slate-950/10 bg-white p-1">
                {(['all', 'south', 'north'] as const).map(item => (
                  <button key={item} type="button" onClick={() => focusCampus(item)} className={`bc-focus-ring rounded-[9px] px-2.5 py-1 text-[9px] font-black transition ${focus === item ? 'bg-[#0b1226] text-white' : 'text-slate-500 hover:bg-[#f4f5f2]'}`}>
                    {item === 'all' ? 'All' : item === 'south' ? 'Güney' : 'Kuzey'}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-1 rounded-[13px] border border-slate-950/10 bg-white p-1">
                {(['satellite', 'street', 'dark'] as const).map(item => (
                  <button key={item} type="button" onClick={() => setTileType(item)} className={`bc-focus-ring rounded-[9px] px-2.5 py-1 text-[9px] font-black transition ${tileType === item ? 'bg-blue-50 text-blue-700' : 'text-slate-500 hover:bg-[#f4f5f2]'}`}>
                    {TILE_LAYERS[item].label}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <span className="bc-chip border-violet-200 bg-violet-50 text-violet-700"><Sparkles size={10} /> VISUALIZATION MODE</span>
          )}
        </div>
      </div>

      {mapMode === 'cesium' ? (
        <div className="overflow-hidden rounded-[20px]"><CampusCesiumMap buildings={buildings} /></div>
      ) : mapMode === '3d' ? (
        <div className="overflow-hidden rounded-[20px]"><CampusMap3D buildings={buildings} /></div>
      ) : (
        <div className="relative h-[520px] w-full overflow-hidden rounded-[20px] border border-slate-950/10 bg-slate-200 shadow-inner">
          <MapContainer center={mapCenter} zoom={zoomLevel} style={{ height: '100%', width: '100%' }}>
            <MapViewController focusCoords={mapCenter} zoom={zoomLevel} />
            <TileLayer attribution={TILE_LAYERS[tileType].attribution} url={TILE_LAYERS[tileType].url} />
            {buildings.map(building => (
              <CircleMarker
                key={building.id}
                center={building.coords}
                pathOptions={{ fillColor: getColor(building.occupancy_ratio), color: '#ffffff', weight: 2, fillOpacity: 0.92 }}
                radius={9}
              >
                <Popup>
                  <div className="min-w-[210px] p-1 font-sans">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="text-sm font-black text-slate-900">{building.name}</div>
                        <div className="mt-0.5 text-[10px] font-semibold text-slate-500">{building.campus === 'south' ? 'Güney' : 'Kuzey'} Campus · {building.floors} floors</div>
                      </div>
                      <span className="rounded-md bg-slate-100 px-1.5 py-0.5 font-mono text-[9px] font-black text-slate-500">{building.code}</span>
                    </div>
                    <div className="mt-3 rounded-lg bg-slate-50 p-2.5">
                      <div className="text-[9px] font-black uppercase tracking-wider text-slate-400">Schedule-derived use</div>
                      <div className="mt-1 font-mono text-lg font-black" style={{ color: getColor(building.occupancy_ratio) }}>%{Math.round((building.occupancy_ratio ?? 0) * 100)}</div>
                      <div className="text-[9px] text-slate-400">Model estimate · not a people counter</div>
                    </div>
                    <Link href={`/buildings/${building.id}`} className="mt-3 flex items-center justify-between rounded-lg bg-[#0b1226] px-3 py-2 text-[10px] font-black text-white">
                      Building detail <span>→</span>
                    </Link>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
          <div className="pointer-events-none absolute bottom-3 left-3 z-[500] flex items-center gap-2 rounded-full border border-white/30 bg-[#0b1226]/85 px-3 py-1.5 text-[9px] font-bold text-white backdrop-blur-md">
            <Layers3 size={10} /> schedule-derived utilization layer
          </div>
        </div>
      )}
    </div>
  );
}
