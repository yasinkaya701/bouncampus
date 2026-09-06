'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import { Building } from '@/lib/types';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { Layers, Box, Globe, Compass } from 'lucide-react';

// Dynamic import for CesiumJS real geospatial 3D globe component
const CampusCesiumMap = dynamic(() => import('./CampusCesiumMap'), {
  ssr: false,
  loading: () => (
    <div className="h-[480px] w-full bg-slate-950 rounded-xl flex flex-col items-center justify-center text-slate-300 gap-3 border border-slate-800">
      <div className="w-10 h-10 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      <div className="text-center">
        <p className="text-sm font-semibold text-white">CesiumJS Gerçek 3D Küre Yükleniyor...</p>
        <p className="text-xs text-slate-400 mt-0.5">ArcGIS Uydu Dokuları & Boğaziçi 3D Binaları Hazırlanıyor</p>
      </div>
    </div>
  )
});

// Dynamic import for 3D Three.js component to avoid SSR issues
const CampusMap3D = dynamic(() => import('./CampusMap3D'), {
  ssr: false,
  loading: () => (
    <div className="h-[460px] w-full bg-slate-900 rounded-xl flex flex-col items-center justify-center text-gray-400 gap-2">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      <span className="text-xs">3D Dijital İkiz Yükleniyor...</span>
    </div>
  )
});

function getColor(occupancyRatio: number | undefined) {
  if (occupancyRatio === undefined) return '#9ca3af'; // gray
  if (occupancyRatio < 0.4) return '#10b981'; // green
  if (occupancyRatio <= 0.7) return '#f59e0b'; // yellow
  return '#ef4444'; // red
}

function MapViewController({ focusCoords, zoom }: { focusCoords: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(focusCoords, zoom, { duration: 1.2 });
  }, [focusCoords, zoom, map]);
  return null;
}

const TILE_LAYERS = {
  osm: {
    name: 'Cadde Haritası',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap contributors'
  },
  satellite: {
    name: 'Uydu 3D Görünüm',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  },
  dark: {
    name: 'Gece Modu',
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '&copy; CartoDB'
  }
};

export default function CampusMap({ buildings }: { buildings: Building[] }) {
  const [mounted, setMounted] = useState(false);
  const [mapMode, setMapMode] = useState<'cesium' | '3d' | '2d'>('cesium'); // Default to Cesium real 3D Globe!
  const [tileType, setTileType] = useState<'osm' | 'satellite' | 'dark'>('satellite');
  const [mapCenter, setMapCenter] = useState<[number, number]>([41.0850, 29.0475]);
  const [zoomLevel, setZoomLevel] = useState(16);
  const [activeCampus, setActiveCampus] = useState<'all' | 'south' | 'north'>('all');

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleFocus = (campus: 'all' | 'south' | 'north') => {
    setActiveCampus(campus);
    if (campus === 'south') {
      setMapCenter([41.0833, 29.0508]);
      setZoomLevel(17);
    } else if (campus === 'north') {
      setMapCenter([41.0867, 29.0442]);
      setZoomLevel(17);
    } else {
      setMapCenter([41.0850, 29.0475]);
      setZoomLevel(16);
    }
  };

  if (!mounted) {
    return (
      <div className="h-[460px] w-full bg-gray-100 rounded-xl flex items-center justify-center text-gray-500">
        Kampüs haritası yükleniyor...
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Top Map Control Bar */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        {/* Left: View Mode Toggle (Cesium vs Three.js 3D vs 2D) */}
        <div className="flex items-center space-x-1 bg-gray-100 p-1 rounded-xl shadow-xs border border-gray-200">
          <button
            onClick={() => setMapMode('cesium')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition ${mapMode === 'cesium' ? 'bg-white text-indigo-700 shadow-xs border border-indigo-100' : 'text-gray-600 hover:text-gray-900'}`}
          >
            <Globe size={14} className={mapMode === 'cesium' ? 'text-indigo-600' : ''} />
            <span>Cesium Gerçek 3D Küre</span>
            <span className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-[9px] px-1.5 py-0.2 rounded-full font-extrabold uppercase tracking-wider">CESIUM</span>
          </button>
          <button
            onClick={() => setMapMode('3d')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition ${mapMode === '3d' ? 'bg-white text-emerald-800 shadow-xs border border-emerald-100' : 'text-gray-600 hover:text-gray-900'}`}
          >
            <Box size={14} className={mapMode === '3d' ? 'text-emerald-600' : ''} />
            <span>Three.js İkiz</span>
            <span className="bg-emerald-100 text-emerald-800 text-[9px] px-1.5 py-0.2 rounded-full font-bold">WEBGL</span>
          </button>
          <button
            onClick={() => setMapMode('2d')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${mapMode === '2d' ? 'bg-white text-emerald-800 shadow-xs border border-emerald-100' : 'text-gray-600 hover:text-gray-900'}`}
          >
            <Layers size={14} />
            <span>2D Katman</span>
          </button>
        </div>

        {/* Right: Mode specific sub-controls */}
        {mapMode === '2d' ? (
          <div className="flex items-center space-x-2">
            {/* Campus Quick Focus */}
            <div className="flex items-center space-x-1 bg-gray-50 p-0.5 rounded-lg border border-gray-200">
              <button
                onClick={() => handleFocus('all')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${activeCampus === 'all' ? 'bg-emerald-700 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                Tümü
              </button>
              <button
                onClick={() => handleFocus('south')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${activeCampus === 'south' ? 'bg-emerald-700 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                Güney (Bebek)
              </button>
              <button
                onClick={() => handleFocus('north')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${activeCampus === 'north' ? 'bg-emerald-700 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                Kuzey (Hisarüstü)
              </button>
            </div>

            {/* Tile Layer Selector */}
            <div className="flex items-center space-x-1 bg-gray-50 p-0.5 rounded-lg border border-gray-200">
              <button
                onClick={() => setTileType('satellite')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${tileType === 'satellite' ? 'bg-gray-800 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                🛰️ Uydu
              </button>
              <button
                onClick={() => setTileType('osm')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${tileType === 'osm' ? 'bg-gray-800 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                🗺️ Cadde
              </button>
              <button
                onClick={() => setTileType('dark')}
                className={`px-2 py-1 rounded text-xs font-medium transition ${tileType === 'dark' ? 'bg-gray-800 text-white' : 'text-gray-600 hover:bg-gray-200'}`}
              >
                🌙 Gece
              </button>
            </div>
          </div>
        ) : mapMode === 'cesium' ? (
          <div className="text-xs text-indigo-700 font-medium flex items-center gap-1.5 bg-indigo-50 px-2.5 py-1 rounded-lg border border-indigo-100">
            <span className="inline-block w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
            <span>CesiumJS Küre • ArcGIS Uydu • 21 Boğaziçi 3D Binası • 360° Drone Uçuşu</span>
          </div>
        ) : (
          <div className="text-xs text-gray-500 flex items-center gap-1.5 bg-gray-50 px-2.5 py-1 rounded-lg border border-gray-200">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Canlı 3D WebGL Motoru • 21 Bina • Gerçek Kat & Doluluk Yükseklikleri</span>
          </div>
        )}
      </div>

      {/* Main Map Display (Cesium, Three.js 3D, or 2D) */}
      {mapMode === 'cesium' ? (
        <CampusCesiumMap buildings={buildings} />
      ) : mapMode === '3d' ? (
        <CampusMap3D buildings={buildings} />
      ) : (
        <div className="h-[460px] w-full rounded-xl overflow-hidden border border-gray-200 shadow-sm relative z-0">
          <MapContainer 
            center={mapCenter} 
            zoom={zoomLevel} 
            style={{ height: '100%', width: '100%' }}
          >
            <MapViewController focusCoords={mapCenter} zoom={zoomLevel} />
            <TileLayer
              attribution={TILE_LAYERS[tileType].attribution}
              url={TILE_LAYERS[tileType].url}
            />
            {buildings.map(b => (
              <CircleMarker
                key={b.id}
                center={b.coords}
                pathOptions={{ 
                  fillColor: getColor(b.occupancy_ratio), 
                  color: getColor(b.occupancy_ratio),
                  weight: 3,
                  fillOpacity: 0.8
                }}
                radius={11}
              >
                <Popup>
                  <div className="p-1 min-w-[190px]">
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <h3 className="font-bold text-sm text-gray-900">{b.name}</h3>
                      <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-gray-100 text-gray-600">{b.code}</span>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">
                      {b.campus === 'south' ? 'Güney' : 'Kuzey'} Kampüs • {b.floors} Kat • {b.type}
                    </p>
                    <div className="flex justify-between items-center mb-3 bg-gray-50 p-2 rounded">
                      <span className="text-xs text-gray-600 font-medium">Doluluk Oranı:</span>
                      <span className="text-xs font-bold" style={{ color: getColor(b.occupancy_ratio) }}>
                        %{b.occupancy_ratio ? Math.round(b.occupancy_ratio * 100) : 0} Dolu ({b.current_occupancy || 0} Kişi)
                      </span>
                    </div>
                    <Link 
                      href={`/buildings/${b.id}`} 
                      className="text-xs bg-emerald-700 text-white font-medium px-3 py-1.5 rounded-md block text-center hover:bg-emerald-800 transition shadow-xs"
                    >
                      Bina ve Kat Detayı &rarr;
                    </Link>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
      )}
    </div>
  );
}
