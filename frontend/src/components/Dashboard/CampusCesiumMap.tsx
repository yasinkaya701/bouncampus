'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Building } from '@/lib/types';
import Link from 'next/link';
import { 
  Compass, RotateCcw, Sun, Moon, Eye, Layers, Box, Globe2, 
  Loader2, Sparkles, Play, Square, Ruler, CloudSun, Film
} from 'lucide-react';

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

const TOUR_WAYPOINTS = [
  { name: 'Bebek Koyu & Boğaz Köprüsü Panoraması', coords: [29.0550, 41.0790, 620], heading: 335, pitch: -28, duration: 3.5 },
  { name: 'Güney Kampüs: Albert Long & Tarihi Meydan', coords: [29.0524, 41.0820, 240], heading: 315, pitch: -30, duration: 3.0 },
  { name: 'Hamlin Hall & Bebek Sırtları', coords: [29.0545, 41.0835, 190], heading: 240, pitch: -25, duration: 3.0 },
  { name: 'Kuzey Kampüs: New Hall & Kare Blok', coords: [29.0435, 41.0852, 280], heading: 45, pitch: -35, duration: 3.5 },
  { name: 'Aptullah Kuran Kütüphanesi & Piramit', coords: [29.0450, 41.0865, 210], heading: 140, pitch: -30, duration: 3.0 },
  { name: 'Fatih Sultan Mehmet Köprüsü & Genel Bakış', coords: [29.0495, 41.0825, 800], heading: 345, pitch: -32, duration: 4.0 },
];

export default function CampusCesiumMap({ buildings, onSelectBuilding }: CampusCesiumMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const [cesiumLoaded, setCesiumLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState<string | null>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<Building | null>(null);
  const [activeCampusView, setActiveCampusView] = useState<'all' | 'south' | 'north'>('all');
  const [isRotating, setIsRotating] = useState(false);

  // Advanced features state
  const [timeHour, setTimeHour] = useState<number>(13); // 13:00 default noon
  const [timePreset, setTimePreset] = useState<'dawn' | 'noon' | 'sunset' | 'night'>('noon');
  const [tourActive, setTourActive] = useState(false);
  const [tourStepName, setTourStepName] = useState<string | null>(null);
  const tourIndexRef = useRef(0);
  const tourTimeoutRef = useRef<any>(null);

  // Measurement tool state
  const [measureMode, setMeasureMode] = useState(false);
  const [measurePoints, setMeasurePoints] = useState<any[]>([]);
  const [measuredDistance, setMeasuredDistance] = useState<number | null>(null);
  const measureEntitiesRef = useRef<any[]>([]);

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

      // Scene configuration: Enable real solar lighting
      viewer.scene.globe.enableLighting = true;
      viewer.scene.globe.depthTestAgainstTerrain = false;

      // Set initial solar time to noon 13:00 Istanbul time
      const initDate = new Date();
      initDate.setHours(13, 0, 0, 0);
      viewer.clock.currentTime = Cesium.JulianDate.fromDate(initDate);

      // Initial Camera Position: Boğaziçi University Bebek / Hisarüstü Overview
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(29.0495, 41.0825, 750),
        orientation: {
          heading: Cesium.Math.toRadians(345.0),
          pitch: Cesium.Math.toRadians(-32.0),
          roll: 0.0,
        },
        duration: 1.5,
      });

      // Add Custom 3D Extruded Buildings with Real OBIKAS Occupancy Lighting & Thermal Footprints
      buildings.forEach(b => {
        const occ = b.occupancy_ratio || 0;
        let colorHex = '#10b981'; // green
        if (occ >= 0.7) colorHex = '#ef4444'; // red
        else if (occ >= 0.4) colorHex = '#f59e0b'; // amber

        const height = (b.floors || 4) * 3.8 + 6;
        const widthMeters = Math.max(22, Math.min(45, (b.total_capacity || 400) / 14));

        // Ground Thermal Glow Cylinder
        viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(b.coords[1], b.coords[0], 0.2),
          cylinder: {
            length: 0.4,
            topRadius: widthMeters * 1.25,
            bottomRadius: widthMeters * 1.25,
            material: Cesium.Color.fromCssColorString(colorHex).withAlpha(0.25),
            outline: true,
            outlineColor: Cesium.Color.fromCssColorString(colorHex).withAlpha(0.6),
            outlineWidth: 1.5,
          }
        });

        // 3D Box Entity for Building
        viewer.entities.add({
          name: b.name,
          position: Cesium.Cartesian3.fromDegrees(b.coords[1], b.coords[0], height / 2),
          box: {
            dimensions: new Cesium.Cartesian3(widthMeters, widthMeters * 0.75, height),
            material: Cesium.Color.fromCssColorString(colorHex).withAlpha(0.85),
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

      // Click Handler (Entity Selection & Distance Measurement)
      const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
      handler.setInputAction((click: any) => {
        // Measurement Mode Active
        if ((window as any).__MEASURE_MODE_ACTIVE) {
          const ray = viewer.camera.getPickRay(click.position);
          const cartesian = viewer.scene.globe.pick(ray, viewer.scene);
          if (cartesian) {
            handleMeasureClick(cartesian);
          }
          return;
        }

        // Standard Building Inspection Click
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

  // Keep measure mode flag accessible to Cesium canvas event handler
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).__MEASURE_MODE_ACTIVE = measureMode;
    }
  }, [measureMode]);

  // Handle measurement click
  const handleMeasureClick = (cartesian: any) => {
    const Cesium = window.Cesium;
    const viewer = viewerRef.current;
    if (!Cesium || !viewer) return;

    setMeasurePoints(prev => {
      if (prev.length === 0) {
        // First point
        const p1Entity = viewer.entities.add({
          position: cartesian,
          point: { pixelSize: 10, color: Cesium.Color.YELLOW, outlineColor: Cesium.Color.BLACK, outlineWidth: 2 }
        });
        measureEntitiesRef.current.push(p1Entity);
        setMeasuredDistance(null);
        return [cartesian];
      } else {
        // Second point: Calculate distance
        const p1 = prev[0];
        const p2 = cartesian;
        const distance = Cesium.Cartesian3.distance(p1, p2);
        setMeasuredDistance(distance);

        const p2Entity = viewer.entities.add({
          position: p2,
          point: { pixelSize: 10, color: Cesium.Color.YELLOW, outlineColor: Cesium.Color.BLACK, outlineWidth: 2 }
        });
        const lineEntity = viewer.entities.add({
          polyline: {
            positions: [p1, p2],
            width: 4,
            material: Cesium.Color.YELLOW.withAlpha(0.9),
            clampToGround: true
          }
        });
        measureEntitiesRef.current.push(p2Entity, lineEntity);
        return [p1, p2];
      }
    });
  };

  const clearMeasurement = () => {
    const viewer = viewerRef.current;
    if (viewer) {
      measureEntitiesRef.current.forEach(ent => viewer.entities.remove(ent));
      measureEntitiesRef.current = [];
    }
    setMeasurePoints([]);
    setMeasuredDistance(null);
  };

  // Time of Day and Sun Adjustment
  const setSunTime = (hour: number, preset?: 'dawn' | 'noon' | 'sunset' | 'night') => {
    setTimeHour(hour);
    if (preset) setTimePreset(preset);
    const viewer = viewerRef.current;
    const Cesium = window.Cesium;
    if (!viewer || !Cesium) return;

    const d = new Date();
    d.setHours(Math.floor(hour), Math.floor((hour % 1) * 60), 0, 0);
    viewer.clock.currentTime = Cesium.JulianDate.fromDate(d);
  };

  // Camera View Navigation
  const handleFocus = (view: 'all' | 'south' | 'north') => {
    setActiveCampusView(view);
    const viewer = viewerRef.current;
    if (!viewer || !window.Cesium) return;
    const Cesium = window.Cesium;

    if (view === 'south') {
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

  // Cinematic Waypoint Tour
  const startTour = () => {
    if (tourActive) {
      stopTour();
      return;
    }
    setTourActive(true);
    tourIndexRef.current = 0;
    flyToNextWaypoint(0);
  };

  const stopTour = () => {
    setTourActive(false);
    setTourStepName(null);
    if (tourTimeoutRef.current) {
      clearTimeout(tourTimeoutRef.current);
      tourTimeoutRef.current = null;
    }
  };

  const flyToNextWaypoint = (idx: number) => {
    const viewer = viewerRef.current;
    const Cesium = window.Cesium;
    if (!viewer || !Cesium) return;

    if (idx >= TOUR_WAYPOINTS.length) {
      // Completed tour
      stopTour();
      handleFocus('all');
      return;
    }

    const wp = TOUR_WAYPOINTS[idx];
    setTourStepName(`[${idx + 1}/${TOUR_WAYPOINTS.length}] ${wp.name}`);

    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(wp.coords[0], wp.coords[1], wp.coords[2]),
      orientation: {
        heading: Cesium.Math.toRadians(wp.heading),
        pitch: Cesium.Math.toRadians(wp.pitch),
        roll: 0.0,
      },
      duration: wp.duration,
      complete: () => {
        tourTimeoutRef.current = setTimeout(() => {
          tourIndexRef.current = idx + 1;
          flyToNextWaypoint(idx + 1);
        }, 1600);
      }
    });
  };

  // 360 Drone Orbit
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
    <div className="relative w-full h-[560px] rounded-2xl overflow-hidden border border-gray-200 shadow-md bg-slate-950 select-none">
      {/* Loading Overlay */}
      {!cesiumLoaded && !loadingError && (
        <div className="absolute inset-0 bg-slate-950 flex flex-col items-center justify-center text-white z-20 gap-3">
          <Loader2 size={36} className="animate-spin text-emerald-400" />
          <div className="text-center">
            <span className="font-bold text-sm block">Cesium 3D Coğrafi Dünya Motoru Yükleniyor...</span>
            <span className="text-xs text-slate-400">Boğaziçi Uydu, Güneş Simülasyonu ve 3D Binalar Hazırlanıyor</span>
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

      {/* Tour Banner Overlay */}
      {tourActive && tourStepName && (
        <div className="absolute top-16 left-1/2 -translate-x-1/2 z-20 bg-slate-900/95 backdrop-blur-md px-5 py-2.5 rounded-2xl border border-indigo-500/50 shadow-2xl text-white flex items-center gap-3 animate-in fade-in slide-in-from-top-4 duration-300">
          <Film size={18} className="text-indigo-400 animate-pulse" />
          <div>
            <span className="text-[10px] text-indigo-300 font-bold uppercase tracking-wider block">Sinematik Drone Turu Aktif</span>
            <span className="text-xs font-extrabold text-white">{tourStepName}</span>
          </div>
          <button
            onClick={stopTour}
            className="ml-2 bg-rose-600 hover:bg-rose-700 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg transition"
          >
            Durdur
          </button>
        </div>
      )}

      {/* Top Floating Controls */}
      <div className="absolute top-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2 pointer-events-none z-10">
        {/* Campus Presets */}
        <div className="flex items-center space-x-1 pointer-events-auto bg-slate-900/90 backdrop-blur-md p-1 rounded-xl shadow-lg border border-slate-700 text-white">
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

        {/* Action Buttons: Tour, Measurement, Orbit, Reset */}
        <div className="flex items-center space-x-1.5 pointer-events-auto bg-slate-900/90 backdrop-blur-md p-1 rounded-xl shadow-lg border border-slate-700 text-white">
          {/* Cinema Tour */}
          <button
            onClick={startTour}
            title="Sinematik Kampüs Turu"
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${tourActive ? 'bg-indigo-600 text-white animate-pulse' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            <Film size={13} />
            <span className="hidden sm:inline">{tourActive ? 'Turu Bitir' : 'Sinema Turu'}</span>
          </button>

          {/* Distance Measure */}
          <button
            onClick={() => {
              const next = !measureMode;
              setMeasureMode(next);
              if (!next) clearMeasurement();
            }}
            title="Mesafe Ölçüm Cetveli (İki noktaya tıklayın)"
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${measureMode ? 'bg-amber-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            <Ruler size={13} />
            <span className="hidden sm:inline">Cetvel</span>
          </button>

          {/* 360 Drone Orbit */}
          <button
            onClick={toggleRotate}
            title="360° Drone Yörüngesi"
            className={`p-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1 ${isRotating ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            <RotateCcw size={14} className={isRotating ? 'animate-spin' : ''} />
            <span className="hidden md:inline">3D Uçuş</span>
          </button>

          {/* Compass Reset */}
          <button
            onClick={() => handleFocus('all')}
            title="Kamerayı Sıfırla"
            className="p-1.5 rounded-lg text-xs text-slate-300 hover:bg-slate-800 transition"
          >
            <Compass size={14} />
          </button>
        </div>
      </div>

      {/* Measurement Mode Floating HUD */}
      {measureMode && (
        <div className="absolute top-16 right-3 pointer-events-auto z-10 bg-slate-900/95 backdrop-blur-md px-3.5 py-2.5 rounded-xl border border-amber-500/40 shadow-xl text-white text-xs max-w-xs">
          <div className="flex items-center justify-between gap-2 mb-1.5">
            <span className="font-bold text-amber-400 flex items-center gap-1.5">
              <Ruler size={14} /> 3D Mesafe Ölçer
            </span>
            <button
              onClick={clearMeasurement}
              className="text-[10px] text-slate-400 hover:text-white px-1.5 py-0.5 rounded bg-slate-800"
            >
              Temizle
            </button>
          </div>
          <p className="text-[11px] text-slate-300 mb-1">
            {measurePoints.length === 0 ? '1. başlangıç noktasını haritadan seçin' : measurePoints.length === 1 ? '2. hedef noktayı haritadan seçin' : 'Mesafe hesaplandı:'}
          </p>
          {measuredDistance !== null && (
            <div className="bg-amber-950/60 border border-amber-500/50 rounded-lg p-2 text-center mt-1">
              <span className="text-lg font-black text-amber-300">{measuredDistance.toFixed(1)} m</span>
              <span className="block text-[10px] text-amber-200/80">({(measuredDistance / 1000).toFixed(3)} km kuş uçuşu mesafe)</span>
            </div>
          )}
        </div>
      )}

      {/* Bottom Floating Bar: Sun / Time of Day Controller */}
      <div className="absolute bottom-3 right-3 pointer-events-auto z-10 flex items-center space-x-1.5 bg-slate-900/90 backdrop-blur-md px-3 py-2 rounded-xl shadow-lg border border-slate-700 text-white">
        <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1 mr-1">
          <Sun size={13} className="text-amber-400" /> Güneş Simülasyonu:
        </span>
        <button
          onClick={() => setSunTime(6.5, 'dawn')}
          className={`px-2 py-0.8 rounded text-[10px] font-bold transition ${timePreset === 'dawn' ? 'bg-orange-500 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
        >
          🌅 Şafak (06:30)
        </button>
        <button
          onClick={() => setSunTime(13, 'noon')}
          className={`px-2 py-0.8 rounded text-[10px] font-bold transition ${timePreset === 'noon' ? 'bg-amber-500 text-black' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
        >
          ☀️ Öğle (13:00)
        </button>
        <button
          onClick={() => setSunTime(18.75, 'sunset')}
          className={`px-2 py-0.8 rounded text-[10px] font-bold transition ${timePreset === 'sunset' ? 'bg-pink-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
        >
          🌇 Batım (18:45)
        </button>
        <button
          onClick={() => setSunTime(22, 'night')}
          className={`px-2 py-0.8 rounded text-[10px] font-bold transition ${timePreset === 'night' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
        >
          🌙 Gece (22:00)
        </button>
      </div>

      {/* Bottom Cesium Badge & Legend */}
      <div className="absolute bottom-3 left-3 pointer-events-none z-10">
        <div className="bg-slate-900/90 backdrop-blur-md px-3.5 py-2 rounded-xl shadow-lg border border-slate-700 text-white text-[11px] space-y-1">
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
        <div className="absolute bottom-16 right-3 pointer-events-auto bg-white/95 backdrop-blur-md rounded-2xl p-4 shadow-2xl border border-gray-200 w-80 z-20 animate-in fade-in zoom-in-95 duration-200">
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
