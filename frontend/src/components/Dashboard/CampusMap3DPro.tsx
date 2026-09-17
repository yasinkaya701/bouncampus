'use client';

import Link from 'next/link';
import { useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { Box, ExternalLink, Moon, RotateCcw, Sun } from 'lucide-react';
import type { Building } from '@/lib/types';
import { useLocale } from '@/lib/i18n';

interface CampusMap3DProps {
  buildings: Building[];
  onSelectBuilding?: (building: Building) => void;
}

type CampusKey = 'main' | 'south' | 'north' | 'hisar' | 'ucaksavar' | 'kandilli' | 'anadolu' | 'kilyos';
type SourceMode = 'LIVE_OSM' | 'FALLBACK_PRODUCT' | 'EMPTY';

type CampusGeometryBuilding = {
  osm_id: string;
  name: string | null;
  campus: string;
  coords: [number, number];
  footprint: [number, number][];
  height_m: number;
  levels?: number;
  min_height_m?: number;
  roof_height_m?: number;
  building?: string | null;
  source: string;
  osm_url: string;
};

type CampusGeometryPayload = {
  buildings?: CampusGeometryBuilding[];
  degraded?: boolean;
};

const CAMPUS_ORIGINS: Record<CampusKey, [number, number]> = {
  main: [41.0850, 29.0472],
  south: [41.0827, 29.0515],
  north: [41.0864, 29.0446],
  hisar: [41.0891, 29.0502],
  ucaksavar: [41.0858, 29.0400],
  kandilli: [41.0623, 29.0622],
  anadolu: [41.0809, 29.0716],
  kilyos: [41.2417, 29.0121],
};

const CAMPUS_OPTIONS: { key: CampusKey; tr: string; en: string }[] = [
  { key: 'main', tr: 'Ana alan', en: 'Main area' },
  { key: 'south', tr: 'Güney', en: 'South' },
  { key: 'north', tr: 'Kuzey', en: 'North' },
  { key: 'hisar', tr: 'Hisar', en: 'Hisar' },
  { key: 'ucaksavar', tr: 'Uçaksavar', en: 'Uçaksavar' },
  { key: 'kandilli', tr: 'Kandilli', en: 'Kandilli' },
  { key: 'anadolu', tr: 'Anadolu Hisarı', en: 'Anadolu Hisarı' },
  { key: 'kilyos', tr: 'Kilyos', en: 'Kilyos' },
];

const SCALE = 0.34;
const M_PER_DEG_LAT = 111_320;

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function normalize(value?: string | null) {
  return (value ?? '')
    .toLocaleLowerCase('tr-TR')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/ı/g, 'i')
    .replace(/[^a-z0-9]/g, '');
}

function distanceMeters(a: [number, number], b: [number, number]) {
  const meanLat = ((a[0] + b[0]) / 2) * Math.PI / 180;
  const dy = (a[0] - b[0]) * M_PER_DEG_LAT;
  const dx = (a[1] - b[1]) * M_PER_DEG_LAT * Math.cos(meanLat);
  return Math.hypot(dx, dy);
}

function fallbackGeometry(buildings: Building[], campus: CampusKey): CampusGeometryBuilding[] {
  const candidates = buildings.filter(building => campus === 'main' || building.campus === campus);
  return candidates.map(building => {
    const [lat, lon] = building.coords;
    const floors = Math.max(1, building.floors || 1);
    const widthM = clamp(Math.sqrt(Math.max(40, building.total_capacity)) * 1.45, 13, 34);
    const depthM = clamp(widthM * 0.68, 10, 24);
    const dLat = (depthM / 2) / M_PER_DEG_LAT;
    const dLon = (widthM / 2) / (M_PER_DEG_LAT * Math.cos(lat * Math.PI / 180));
    return {
      osm_id: `fallback/${building.id}`,
      name: building.name,
      campus: building.campus,
      coords: building.coords,
      footprint: [
        [lat - dLat, lon - dLon],
        [lat - dLat, lon + dLon],
        [lat + dLat, lon + dLon],
        [lat + dLat, lon - dLon],
      ],
      height_m: floors * 3.35,
      levels: floors,
      min_height_m: 0,
      roof_height_m: 0.6,
      building: building.type,
      source: 'BOUNCAMPUS product record fallback — approximate visualization footprint',
      osm_url: '',
    };
  });
}

function createOperationalMatches(geometry: CampusGeometryBuilding[], operational: Building[]) {
  const result = new Map<string, Building>();
  const used = new Set<string>();

  geometry.forEach(item => {
    if (item.osm_id.startsWith('fallback/')) {
      const id = item.osm_id.replace('fallback/', '');
      const direct = operational.find(building => building.id === id);
      if (direct) result.set(item.osm_id, direct);
    }
  });

  operational.forEach(building => {
    if ([...result.values()].some(item => item.id === building.id)) return;
    const buildingName = normalize(building.name);
    const best = geometry
      .filter(item => !used.has(item.osm_id) && !item.osm_id.startsWith('fallback/'))
      .map(item => {
        const itemName = normalize(item.name);
        const distance = distanceMeters(building.coords, item.coords);
        const nameMatch = itemName && (itemName.includes(buildingName) || buildingName.includes(itemName));
        return { item, distance, score: nameMatch ? distance - 220 : distance };
      })
      .sort((a, b) => a.score - b.score)
      .find(candidate => candidate.score < -120 || candidate.distance <= 38);

    if (best) {
      result.set(best.item.osm_id, building);
      used.add(best.item.osm_id);
    }
  });

  return result;
}

function scenePoint(point: [number, number], origin: [number, number]) {
  const lngScale = M_PER_DEG_LAT * Math.cos(origin[0] * Math.PI / 180);
  return {
    x: (point[1] - origin[1]) * lngScale * SCALE,
    z: -(point[0] - origin[0]) * M_PER_DEG_LAT * SCALE,
  };
}

function buildMesh(item: CampusGeometryBuilding, origin: [number, number], operational: Building | undefined, night: boolean) {
  const points = item.footprint.map(point => scenePoint(point, origin));
  if (points.length < 3) return null;

  const center = points.reduce((acc, point) => ({ x: acc.x + point.x, z: acc.z + point.z }), { x: 0, z: 0 });
  center.x /= points.length;
  center.z /= points.length;
  const local = points.map(point => ({ x: point.x - center.x, z: point.z - center.z }));
  const shape = new THREE.Shape();
  local.forEach((point, index) => index === 0 ? shape.moveTo(point.x, -point.z) : shape.lineTo(point.x, -point.z));
  shape.closePath();

  const levels = Math.max(1, item.levels ?? Math.round(item.height_m / 3.35));
  const height = Math.max(2.8, item.height_m * SCALE);
  const minHeight = Math.max(0, (item.min_height_m ?? 0) * SCALE);
  const historicName = normalize(item.name);
  const historic = ['albertlong', 'anderson', 'washburn', 'hamlin', 'gates', 'perkins', 'sloane', 'dodge'].some(token => historicName.includes(token));
  const facade = historic ? 0xb9afa2 : operational ? 0xbfc8c6 : 0xaeb9bb;
  const roofColor = historic ? 0x78443a : 0x667074;

  const group = new THREE.Group();
  group.position.set(center.x, 0, center.z);
  group.name = item.osm_id;
  group.userData = { geometry: item, operational };

  const bodyGeometry = new THREE.ExtrudeGeometry(shape, {
    depth: Math.max(0.8, height - minHeight),
    bevelEnabled: false,
  });
  bodyGeometry.rotateX(-Math.PI / 2);
  const bodyMaterial = new THREE.MeshStandardMaterial({
    color: night ? 0x374340 : facade,
    roughness: historic ? 0.9 : 0.72,
    metalness: historic ? 0.01 : 0.04,
  });
  const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
  body.position.y = minHeight;
  body.castShadow = true;
  body.receiveShadow = true;
  group.add(body);

  const roofGeometry = new THREE.ExtrudeGeometry(shape, { depth: 0.16, bevelEnabled: false });
  roofGeometry.rotateX(-Math.PI / 2);
  const roof = new THREE.Mesh(roofGeometry, new THREE.MeshStandardMaterial({ color: roofColor, roughness: 0.86 }));
  roof.position.y = height;
  roof.castShadow = true;
  group.add(roof);

  const edges = new THREE.LineSegments(
    new THREE.EdgesGeometry(bodyGeometry, 24),
    new THREE.LineBasicMaterial({ color: night ? 0x82928c : 0x526164, transparent: true, opacity: 0.24 }),
  );
  edges.position.y = minHeight;
  group.add(edges);

  if (operational) {
    const status = (operational.occupancy_ratio ?? 0) >= 0.7 ? 0xc45252 : (operational.occupancy_ratio ?? 0) >= 0.4 ? 0xc89a39 : 0x4fa78b;
    const marker = new THREE.Mesh(
      new THREE.SphereGeometry(0.48, 14, 14),
      new THREE.MeshStandardMaterial({ color: status, emissive: status, emissiveIntensity: night ? 0.65 : 0.18 }),
    );
    marker.position.y = height + 1.35;
    marker.userData.isMarker = true;
    group.add(marker);
  }

  const floorHeight = height / levels;
  if (operational && floorHeight > 0.6) {
    const windowMaterial = new THREE.MeshStandardMaterial({
      color: 0x284c5b,
      emissive: night ? 0xe3b768 : 0x07151b,
      emissiveIntensity: night ? 0.22 : 0.01,
      roughness: 0.25,
      metalness: 0.22,
    });
    const windowGeometry = new THREE.BoxGeometry(0.65, Math.min(0.58, floorHeight * 0.42), 0.08);
    const xs = local.map(point => point.x);
    const zs = local.map(point => point.z);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const maxZ = Math.max(...zs);
    const count = clamp(Math.floor((maxX - minX) / 2.1), 2, 10);
    for (let floor = 0; floor < Math.min(levels, 8); floor += 1) {
      for (let index = 0; index < count; index += 1) {
        const window = new THREE.Mesh(windowGeometry, windowMaterial);
        window.position.set(minX + ((index + 0.5) / count) * (maxX - minX), floorHeight * (floor + 0.58), maxZ + 0.05);
        group.add(window);
      }
    }
  }

  return group;
}

export default function CampusMap3DPro({ buildings, onSelectBuilding }: CampusMap3DProps) {
  const { locale, t } = useLocale();
  const containerRef = useRef<HTMLDivElement>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const frameRef = useRef<number | null>(null);
  const [campus, setCampus] = useState<CampusKey>('main');
  const [geometry, setGeometry] = useState<CampusGeometryBuilding[]>([]);
  const [sourceMode, setSourceMode] = useState<SourceMode>('EMPTY');
  const [loading, setLoading] = useState(true);
  const [night, setNight] = useState(false);
  const [selected, setSelected] = useState<{ geometry: CampusGeometryBuilding; operational?: Building } | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setSelected(null);

    fetch(`/api/v1/campus-geometry?campus=${campus}`, { cache: 'no-store' })
      .then(response => response.ok ? response.json() as Promise<CampusGeometryPayload> : Promise.reject(new Error('geometry source')))
      .then(payload => {
        if (cancelled) return;
        const liveGeometry = payload.buildings ?? [];
        if (!payload.degraded && liveGeometry.length > 0) {
          setGeometry(liveGeometry);
          setSourceMode('LIVE_OSM');
          return;
        }
        const fallback = fallbackGeometry(buildings, campus);
        setGeometry(fallback);
        setSourceMode(fallback.length > 0 ? 'FALLBACK_PRODUCT' : 'EMPTY');
      })
      .catch(() => {
        if (cancelled) return;
        const fallback = fallbackGeometry(buildings, campus);
        setGeometry(fallback);
        setSourceMode(fallback.length > 0 ? 'FALLBACK_PRODUCT' : 'EMPTY');
      })
      .finally(() => { if (!cancelled) setLoading(false); });

    return () => { cancelled = true; };
  }, [buildings, campus]);

  const matches = useMemo(() => createOperationalMatches(geometry, buildings), [geometry, buildings]);
  const sourceHeightCount = useMemo(() => geometry.filter(item => Boolean(item.levels) || Boolean(item.roof_height_m)).length, [geometry]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || geometry.length === 0) return;

    const width = Math.max(1, container.clientWidth);
    const height = Math.max(1, container.clientHeight || 600);
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(night ? 0x071117 : 0xdde6e7);
    scene.fog = new THREE.Fog(night ? 0x071117 : 0xdde6e7, 160, 760);

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1800);
    cameraRef.current = camera;

    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', alpha: false });
    } catch {
      setSourceMode('EMPTY');
      return;
    }

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.6));
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = night ? 0.9 : 1.02;
    container.replaceChildren(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxPolarAngle = Math.PI / 2.02;

    scene.add(new THREE.HemisphereLight(night ? 0x5b7488 : 0xffffff, night ? 0x0b1513 : 0x71806f, night ? 0.72 : 1.32));
    const sun = new THREE.DirectionalLight(night ? 0x728ea8 : 0xfff1d3, night ? 1.1 : 2.15);
    sun.position.set(-90, 180, 85);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    scene.add(sun);

    const origin = CAMPUS_ORIGINS[campus];
    const modelRoot = new THREE.Group();
    geometry.forEach(item => {
      const mesh = buildMesh(item, origin, matches.get(item.osm_id), night);
      if (mesh) modelRoot.add(mesh);
    });
    scene.add(modelRoot);

    const box = new THREE.Box3().setFromObject(modelRoot);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const span = Math.max(size.x, size.z, 35);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(span * 1.65, span * 1.65),
      new THREE.MeshStandardMaterial({ color: night ? 0x17211d : 0x8fa78b, roughness: 1 }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(center.x, -0.08, center.z);
    ground.receiveShadow = true;
    scene.add(ground);

    const grid = new THREE.GridHelper(span * 1.5, 30, night ? 0x35515a : 0x738b80, night ? 0x20353c : 0xaab9b0);
    grid.position.set(center.x, 0.01, center.z);
    (grid.material as THREE.Material).transparent = true;
    (grid.material as THREE.Material).opacity = night ? 0.22 : 0.2;
    scene.add(grid);

    camera.position.set(center.x + span * 0.5, Math.max(42, span * 0.58), center.z + span * 0.78);
    controls.target.copy(center).setY(Math.max(2.5, size.y * 0.18));
    controls.minDistance = Math.max(12, span * 0.08);
    controls.maxDistance = Math.max(180, span * 2.5);
    controls.update();

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const pick = (event: PointerEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      const hit = raycaster.intersectObjects(modelRoot.children, true).find(entry => !entry.object.userData?.isMarker);
      if (!hit) return;
      let object: THREE.Object3D | null = hit.object;
      while (object && !object.userData?.geometry) object = object.parent;
      if (!object?.userData?.geometry) return;
      const record = {
        geometry: object.userData.geometry as CampusGeometryBuilding,
        operational: object.userData.operational as Building | undefined,
      };
      setSelected(record);
      if (record.operational) onSelectBuilding?.(record.operational);
    };
    renderer.domElement.addEventListener('pointerup', pick);

    const onResize = () => {
      if (!containerRef.current) return;
      const nextWidth = Math.max(1, containerRef.current.clientWidth);
      const nextHeight = Math.max(1, containerRef.current.clientHeight || 600);
      camera.aspect = nextWidth / nextHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(nextWidth, nextHeight);
    };
    window.addEventListener('resize', onResize);

    const render = () => {
      controls.update();
      renderer.render(scene, camera);
      frameRef.current = requestAnimationFrame(render);
    };
    render();

    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
      renderer.domElement.removeEventListener('pointerup', pick);
      window.removeEventListener('resize', onResize);
      controls.dispose();
      scene.traverse(object => {
        if (object instanceof THREE.Mesh || object instanceof THREE.LineSegments || object instanceof THREE.GridHelper) {
          object.geometry?.dispose();
          const material = (object as THREE.Mesh).material;
          if (material) {
            const materials = Array.isArray(material) ? material : [material];
            materials.forEach(item => item.dispose());
          }
        }
      });
      renderer.dispose();
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement);
    };
  }, [geometry, matches, campus, night, onSelectBuilding]);

  const resetCamera = () => {
    const controls = controlsRef.current;
    const camera = cameraRef.current;
    if (!controls || !camera) return;
    const target = controls.target.clone();
    const distance = camera.position.distanceTo(target);
    camera.position.set(target.x + distance * 0.32, target.y + distance * 0.52, target.z + distance * 0.79);
    controls.update();
  };

  return (
    <div className="relative h-[600px] overflow-hidden rounded-[22px] border border-slate-900/10 bg-[#dfe8e7]">
      <div ref={containerRef} className="absolute inset-0" />

      <div className="absolute left-3 top-3 z-10 max-w-[calc(100%-1.5rem)] rounded-2xl border border-white/70 bg-white/90 p-2 shadow-[0_14px_40px_rgba(15,23,42,.12)] backdrop-blur-xl">
        <div className="mb-2 flex items-center gap-2 px-1"><Box size={13} className="text-[#173f67]" /><span className="text-[10px] font-black uppercase tracking-[0.13em] text-slate-700">{t('Kampüs 3D', 'Campus 3D')}</span></div>
        <div className="flex max-w-[78vw] gap-1 overflow-x-auto pb-0.5">
          {CAMPUS_OPTIONS.map(option => (
            <button key={option.key} type="button" onClick={() => setCampus(option.key)} className={`shrink-0 rounded-lg px-2.5 py-1.5 text-[9px] font-bold transition ${campus === option.key ? 'bg-[#071c33] text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
              {locale === 'tr' ? option.tr : option.en}
            </button>
          ))}
        </div>
      </div>

      <div className="absolute right-3 top-3 z-10 flex gap-1 rounded-xl border border-white/70 bg-white/90 p-1 shadow-sm backdrop-blur-xl">
        <button type="button" onClick={() => setNight(value => !value)} className="rounded-lg p-2 text-slate-600 transition hover:bg-slate-100" title={t('Gündüz/gece', 'Day/night')}>
          {night ? <Sun size={14} /> : <Moon size={14} />}
        </button>
        <button type="button" onClick={resetCamera} className="rounded-lg p-2 text-slate-600 transition hover:bg-slate-100" title={t('Görüşü sıfırla', 'Reset view')}><RotateCcw size={14} /></button>
      </div>

      {sourceMode === 'EMPTY' && !loading ? (
        <div className="absolute inset-0 z-[5] grid place-items-center bg-[#07131f] p-6 text-center text-white">
          <div className="max-w-md">
            <Box size={28} className="mx-auto text-white/28" />
            <div className="mt-4 text-lg font-black">{t('Bu kampüs için 3D geometri yüklenemedi.', '3D geometry is unavailable for this campus.')}</div>
            <p className="mt-2 text-[10px] leading-5 text-white/45">{t('Ana alan, Güney veya Kuzey kampüsü seçildiğinde ürün kayıtlarından güvenilir görsel fallback kullanılabilir.', 'Choose Main, South or North to use the reliable visualization fallback derived from product building records.')}</p>
          </div>
        </div>
      ) : null}

      <div className="absolute bottom-3 left-3 z-10 max-w-[min(680px,calc(100%-1.5rem))] rounded-2xl border border-white/10 bg-[#07131f]/88 px-3 py-2.5 text-white shadow-lg backdrop-blur-xl">
        {loading ? (
          <div className="text-[10px] font-semibold text-white/70">{t('Bina geometrileri yükleniyor…', 'Loading building geometry…')}</div>
        ) : sourceMode === 'LIVE_OSM' ? (
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[9px] text-white/65">
            <span className="rounded-full bg-emerald-300/10 px-2 py-1 font-black text-emerald-200">LIVE OSM</span>
            <span><strong className="text-white">{geometry.length}</strong> {t('bina footprint’i', 'building footprints')}</span>
            <span><strong className="text-white">{matches.size}</strong> {t('ürün kaydıyla eşleşti', 'matched to product records')}</span>
            <span><strong className="text-white">{sourceHeightCount}</strong> {t('yükseklik/kat etiketi', 'height/level tags')}</span>
          </div>
        ) : sourceMode === 'FALLBACK_PRODUCT' ? (
          <div className="flex flex-wrap items-center gap-2 text-[9px] text-white/68">
            <span className="rounded-full bg-amber-300/10 px-2 py-1 font-black text-amber-200">RESILIENT FALLBACK</span>
            <span>{t('Overpass yanıt vermedi; sahne ürünün mevcut bina konumları ve kat sayılarıyla yaklaşık görselleştirme olarak çalışmaya devam ediyor.', 'Overpass did not respond; the scene remains usable with approximate visualization geometry derived from the product’s existing building coordinates and floor counts.')}</span>
          </div>
        ) : (
          <div className="text-[10px] font-semibold text-amber-200">{t('Geometri bulunamadı.', 'No geometry available.')}</div>
        )}
      </div>

      {selected && (
        <div className="absolute bottom-3 right-3 z-20 w-[min(340px,calc(100%-1.5rem))] rounded-2xl border border-white/70 bg-white/95 p-4 shadow-xl backdrop-blur-xl">
          <button type="button" onClick={() => setSelected(null)} className="absolute right-3 top-2 text-sm font-bold text-slate-400">×</button>
          <div className="pr-6 text-sm font-black text-slate-950">{selected.geometry.name ?? selected.operational?.name ?? t('Adsız bina', 'Unnamed building')}</div>
          <div className="mt-1 text-[9px] font-bold uppercase tracking-[0.12em] text-slate-400">{selected.geometry.campus}</div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-[10px]">
            <div className="rounded-xl bg-slate-50 p-2"><div className="text-slate-400">{t('Görsel yükseklik', 'Visual height')}</div><div className="mt-1 font-mono font-bold text-slate-800">{selected.geometry.height_m.toFixed(1)} m</div></div>
            <div className="rounded-xl bg-slate-50 p-2"><div className="text-slate-400">{t('Kat', 'Levels')}</div><div className="mt-1 font-mono font-bold text-slate-800">{selected.geometry.levels ?? '—'}</div></div>
          </div>
          <div className="mt-3 text-[9px] leading-4 text-slate-500">{selected.geometry.source}</div>
          <div className="mt-3 flex gap-2">
            {selected.geometry.osm_url ? <a href={selected.geometry.osm_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-1.5 text-[9px] font-bold text-slate-600">OSM <ExternalLink size={9} /></a> : null}
            {selected.operational ? <Link href={`/buildings/${selected.operational.id}`} className="rounded-lg bg-[#102a43] px-2.5 py-1.5 text-[9px] font-bold text-white">{t('Bina detayı', 'Building detail')}</Link> : null}
          </div>
        </div>
      )}
    </div>
  );
}
