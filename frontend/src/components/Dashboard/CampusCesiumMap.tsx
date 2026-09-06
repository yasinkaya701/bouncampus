'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Building } from '@/lib/types';
import Link from 'next/link';
import { Compass, RotateCcw, Sun, Eye, Layers, Box, Globe2, Loader2, Sparkles } from 'lucide-react';

interface CampusCesiumMapProps {
  buildings: Building[];
  onSelectBuilding?: (building: Building) => void;
}

declare global {
  interface Window {
    Cesium: any;
    CESIUM_BASE_URL: string;
  }
}

export default function CampusCesiumMap({ buildings, onSelectBuilding }: CampusCesiumMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const [cesiumLoaded, setCesiumLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState<string | null>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<Building | null>(null);
  const [activeCampusView, setActiveCampusView] = useState<'all' | 'south' | 'north'>('all');
  const [isRotating, setIsRotating] = useState(false);

  // 1. Dynamic Script & CSS Injection for CesiumJS
  useEffect(() => {
    if (typeof window === 'undefined') return;

    if (window.Cesium) {
      setCesiumLoaded(true);
      return;
    }

    // Set Cesium base URL for static assets (workers, skybox, etc.)
    window.CESIUM_BASE_URL = 'https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/';

    // Load Cesium CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Widgets/widgets.css';
    document.head.appendChild(link);

    // Load Cesium JS
    const script = document.createElement('script');
    script.src = 'https://cesium.com/downloads/cesiumjs/releases/1.119/Build/Cesium/Cesium.js';
    script.async = true;
    script.onload = () => {
      setCesiumLoaded(true);
    };
    script.onerror = () => {
      setLoadingError('CesiumJS kütüphanesi yüklenemedi. İnternet bağlantınızı kontrol edin.');
    };
    document.body.appendChild(script);

    return () => {
      // Cleanup script tag on unmount if needed
    };
  }, []);

  // 2. Initialize Cesium Viewer
  useEffect(() => {
    if (!cesiumLoaded || !containerRef.current || viewerRef.current) return;

    const Cesium = window.Cesium;
    if (!Cesium) return;

    try {
      // Disable default Ion token checks
      Cesium.Ion.defaultAccessToken = '';

      // High Resolution Esri World Imagery (Satellite) via UrlTemplateImageryProvider
      // This sets _resource immediately and avoids undefined getDerivedResource errors
      const satelliteProvider = new Cesium.UrlTemplateImageryProvider({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maximumLevel: 19,
        credit: 'Esri World Imagery'
      });

      const baseLayer = new Cesium.ImageryLayer(satelliteProvider);

      // Configure Cesium Viewer for ultra-fast, smooth performance
      const viewer = new Cesium.Viewer(containerRef.current, {
        baseLayer: baseLayer,
        animation: false,
        timeline: false,
        fullscreenButton: false,
        vrButton: false,
        geocoder: false,
        homeButton: false,
        infoBox: false,
        sceneModePicker: false,
        selectionIndicator: false,
        navigationHelpButton: false,
        navigationInstructionsInitiallyVisible: false,
        baseLayerPicker: false,
        terrainProvider: new Cesium.EllipsoidTerrainProvider(),
      });

      viewerRef.current = viewer;

      // Scene configuration
      viewer.scene.globe.enableLighting = true;
      viewer.scene.globe.depthTestAgainstTerrain = false;

      // Initial Camera Position: Boğaziçi University Bebek / Hisarüstü Overview
      // Looking from Bebek Bay towards North Campus
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(29.0495, 41.0825, 750),
        orientation: {
          heading: Cesium.Math.toRadians(345.0),
          pitch: Cesium.Math.toRadians(-32.0),
          roll: 0.0,
        },
        duration: 1.5,
      });

      // Add Custom 3D Extruded Buildings with Real OBIKAS Occupancy Lighting
      buildings.forEach(b => {
        const occ = b.occupancy_ratio || 0;
        let colorHex = '#10b981'; // green
        if (occ >= 0.7) colorHex = '#ef4444'; // red
        else if (occ >= 0.4) colorHex = '#f59e0b'; // amber

        const height = (b.floors || 4) * 3.8 + 6;
        const widthMeters = Math.max(22, Math.min(45, (b.total_capacity || 400) / 14));

        // 3D Box Entity for Building
        const buildingEntity = viewer.entities.add({
          name: b.name,
          position: Cesium.Cartesian3.fromDegrees(b.coords[1], b.coords[0], height / 2),
          box: {
            dimensions: new Cesium.Cartesian3(widthMeters, widthMeters * 0.75, height),
            material: Cesium.Color.fromCssColorString(colorHex).withAlpha(0.82),
            outline: true,
            outlineColor: Cesium.Color.WHITE.withAlpha(0.9),
            outlineWidth: 2,
          },
          userData: b,
        });

        // 3D Pin / Label on Top
        viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(b.coords[1], b.coords[0], height + 6),
          billboard: {
            image: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><circle cx="24" cy="24" r="18" fill="${encodeURIComponent(colorHex)}" stroke="white" stroke-width="3"/><text x="24" y="28" fill="white" font-size="11" font-weight="bold" font-family="sans-serif" text-anchor="middle">${b.code}</text></svg>`,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            scale: 0.85,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
          },
          userData: b,
        });
      });

      // Click Handler (Entity Selection)
      const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
      handler.setInputAction((click: any) => {
        const pickedObject = viewer.scene.pick(click.position);
        if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.userData) {
          const b = pickedObject.id.userData as Building;
          setSelectedBuilding(b);
          if (onSelectBuilding) onSelectBuilding(b);

          // Fly camera closer to clicked building
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(b.coords[1], b.coords[0] - 0.0018, 180),
            orientation: {
              heading: Cesium.Math.toRadians(0.0),
              pitch: Cesium.Math.toRadians(-35.0),
              roll: 0.0,
            },
            duration: 1.2,
          });
        }
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

    } catch (e) {
      console.error('Cesium init error', e);
      setLoadingError('Cesium 3D motoru başlatılırken bir hata oluştu.');
    }

    return () => {
      if (viewerRef.current && !viewerRef.current.isDestroyed()) {
        viewerRef.current.destroy();
        viewerRef.current = null;
      }
    };
  }, [cesiumLoaded, buildings, onSelectBuilding]);

  // 3. Camera View Navigation
  const handleFocus = (view: 'all' | 'south' | 'north') => {
    setActiveCampusView(view);
    const viewer = viewerRef.current;
    if (!viewer || !window.Cesium) return;
    const Cesium = window.Cesium;

    if (view === 'south') {
      // Güney Kampüs (Bebek) - Albert Long Hall / Perkins Focus
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(29.0520, 41.0815, 320),
        orientation: {
          heading: Cesium.Math.toRadians(340.0),
          pitch: Cesium.Math.toRadians(-30.0),
          roll: 0.0,
        },
        duration: 1.5,
      });
    } else if (view === 'north') {
      // Kuzey Kampüs (Hisarüstü) - New Hall / Kare Blok Focus
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(29.0442, 41.0848, 380),
        orientation: {
          heading: Cesium.Math.toRadians(20.0),
          pitch: Cesium.Math.toRadians(-32.0),
          roll: 0.0,
        },
        duration: 1.5,
      });
    } else {
      // Overview
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(29.0495, 41.0825, 750),
        orientation: {
          heading: Cesium.Math.toRadians(345.0),
          pitch: Cesium.Math.toRadians(-32.0),
          roll: 0.0,
        },
        duration: 1.5,
      });
    }
  };

  // 4. Drone Flyover / Orbit Animation
  const toggleRotate = () => {
    const viewer = viewerRef.current;
    if (!viewer) return;
    setIsRotating(!isRotating);

    if (!isRotating) {
      viewer.clock.onTick.addEventListener(rotateTick);
    } else {
      viewer.clock.onTick.removeEventListener(rotateTick);
    }
  };

  const rotateTick = () => {
    const viewer = viewerRef.current;
    if (!viewer || !window.Cesium) return;
    viewer.scene.camera.rotate(window.Cesium.Cartesian3.UNIT_Z, 0.0012);
  };

  return (
    <div className="relative w-full h-[520px] rounded-2xl overflow-hidden border border-gray-200 shadow-md bg-slate-950 select-none">
      {/* Loading Overlay */}
      {!cesiumLoaded && !loadingError && (
        <div className="absolute inset-0 bg-slate-950 flex flex-col items-center justify-center text-white z-20 gap-3">
          <Loader2 size={36} className="animate-spin text-emerald-400" />
          <div className="text-center">
            <span className="font-bold text-sm block">Cesium 3D Coğrafi Dünya Motoru Yükleniyor...</span>
            <span className="text-xs text-slate-400">Boğaziçi Uydu ve 3D Binaları Hazırlanıyor</span>
          </div>
        </div>
      )}

      {loadingError && (
        <div className="absolute inset-0 bg-slate-950 flex flex-col items-center justify-center text-rose-400 z-20 gap-2 p-6 text-center">
          <span className="font-bold text-sm">{loadingError}</span>
        </div>
      )}

      {/* Cesium Canvas Container */}
      <div ref={containerRef} className="w-full h-full" />

      {/* Top Floating Controls */}
      <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none z-10">
        {/* Campus Presets */}
        <div className="flex items-center space-x-1.5 pointer-events-auto bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-xl shadow-lg border border-slate-700 text-white">
          <button
            onClick={() => handleFocus('all')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition ${activeCampusView === 'all' ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            Tüm Kampüs
          </button>
          <button
            onClick={() => handleFocus('south')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition ${activeCampusView === 'south' ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            Güney (Bebek)
          </button>
          <button
            onClick={() => handleFocus('north')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition ${activeCampusView === 'north' ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            Kuzey (Hisarüstü)
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-2 pointer-events-auto bg-slate-900/90 backdrop-blur-md px-2.5 py-1.5 rounded-xl shadow-lg border border-slate-700 text-white">
          <button
            onClick={toggleRotate}
            title="360° Drone Uçuşu"
            className={`p-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${isRotating ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            <RotateCcw size={14} className={isRotating ? 'animate-spin' : ''} />
            <span className="hidden sm:inline">3D Uçuş</span>
          </button>
          <button
            onClick={() => handleFocus('all')}
            title="Kamerayı Sıfırla"
            className="p-1.5 rounded-lg text-xs text-slate-300 hover:bg-slate-800 transition"
          >
            <Compass size={14} />
          </button>
        </div>
      </div>

      {/* Bottom Cesium Badge & Legend */}
      <div className="absolute bottom-3 left-3 pointer-events-none z-10">
        <div className="bg-slate-900/90 backdrop-blur-md px-3.5 py-2.5 rounded-xl shadow-lg border border-slate-700 text-white text-[11px] space-y-1">
          <div className="font-bold flex items-center gap-2 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            Cesium Real 3D Geospatial Engine
            <span className="bg-emerald-500/20 text-emerald-300 text-[10px] px-1.5 py-0.2 rounded font-mono">
              v1.119
            </span>
          </div>
          <div className="flex items-center gap-3 text-[10px] text-slate-300">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-emerald-500"></span> Sakin (&lt;%40)</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-amber-500"></span> Normal (%40-70)</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-rose-500"></span> Yoğun (&gt;%70)</span>
          </div>
          <div className="text-[9px] text-slate-400">
            Sol tık: Döndür • Sağ tık/Tekerlek: Zoom • Orta tık: Eğim/Tilt • Binaya tıkla: İncele
          </div>
        </div>
      </div>

      {/* Selected Building Detail Popup */}
      {selectedBuilding && (
        <div className="absolute bottom-3 right-3 pointer-events-auto bg-white/95 backdrop-blur-md rounded-2xl p-4 shadow-2xl border border-gray-200 w-76 z-10 animate-in fade-in zoom-in-95 duration-200">
          <div className="flex items-start justify-between mb-2">
            <div>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 uppercase font-mono">
                {selectedBuilding.code}
              </span>
              <h3 className="font-bold text-sm text-gray-900 mt-1">{selectedBuilding.name}</h3>
              <p className="text-xs text-gray-500">
                {selectedBuilding.campus === 'south' ? 'Güney (Bebek)' : 'Kuzey (Hisarüstü)'} • {selectedBuilding.type}
              </p>
            </div>
            <button
              onClick={() => setSelectedBuilding(null)}
              className="text-gray-400 hover:text-gray-600 text-xs font-bold p-1 rounded-lg hover:bg-gray-100"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 my-3 text-xs">
            <div className="bg-gray-50 p-2 rounded-xl">
              <span className="text-gray-400 block text-[10px]">Kat Sayısı</span>
              <span className="font-bold text-gray-800">{selectedBuilding.floors} Kat</span>
            </div>
            <div className="bg-gray-50 p-2 rounded-xl">
              <span className="text-gray-400 block text-[10px]">Kapasite</span>
              <span className="font-bold text-gray-800">{selectedBuilding.total_capacity} Kişi</span>
            </div>
            <div className="bg-gray-50 p-2 rounded-xl">
              <span className="text-gray-400 block text-[10px]">OBIKAS Doluluk</span>
              <span className={`font-bold ${selectedBuilding.occupancy_ratio && selectedBuilding.occupancy_ratio >= 0.7 ? 'text-rose-600' : selectedBuilding.occupancy_ratio && selectedBuilding.occupancy_ratio >= 0.4 ? 'text-amber-600' : 'text-emerald-600'}`}>
                %{Math.round((selectedBuilding.occupancy_ratio || 0) * 100)} ({selectedBuilding.current_occupancy || 0} Öğrenci)
              </span>
            </div>
            <div className="bg-gray-50 p-2 rounded-xl">
              <span className="text-gray-400 block text-[10px]">Taban Yük</span>
              <span className="font-bold text-emerald-700">{selectedBuilding.energy_profile?.base_load_kw || 30} kW</span>
            </div>
          </div>

          <Link
            href={`/buildings/${selectedBuilding.id}`}
            className="w-full bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold py-2 px-3 rounded-xl block text-center transition shadow-xs"
          >
            3D Kat Modelini İncele &rarr;
          </Link>
        </div>
      )}
    </div>
  );
}
