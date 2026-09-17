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
  roof_shape?: string | null;
  building?: string | null;
  building_material?: string | null;
  building_colour?: string | null;
  roof_material?: string | null;
  roof_colour?: string | null;
  start_date?: string | null;
  source: string;
  osm_url: string;
};

type CampusGeometryPayload = {
  campus: CampusKey;
  buildings?: CampusGeometryBuilding[];
  degraded?: boolean;
  source?: string;
  fetched_at?: string;
  note?: string;
  detail?: string;
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

const HISTORIC_NAMES = [
  'albertlong', 'anderson', 'washburn', 'hamlin', 'gates', 'perkins', 'sloane',
  'dodge', 'vanmillingen', 'kennedy', 'theodorus', 'natukbirkan', 'johnfreely',
];

function normalize(value?: string | null) {
  return (value ?? '').toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i').replace(/[^a-z0-9]/g, '');
}

function cleanRing(points: [number, number][]) {
  if (points.length < 3) return points;
  const cleaned = [...points];
  const first = cleaned[0];
  const last = cleaned[cleaned.length - 1];
  if (Math.abs(first[0] - last[0]) < 1e-8 && Math.abs(first[1] - last[1]) < 1e-8) cleaned.pop();
  return cleaned;
}

function planarDistanceMeters(a: [number, number], b: [number, number]) {
  const meanLat = ((a[0] + b[0]) / 2) * Math.PI / 180;
  const dy = (a[0] - b[0]) * M_PER_DEG_LAT;
  const dx = (a[1] - b[1]) * M_PER_DEG_LAT * Math.cos(meanLat);
  return Math.hypot(dx, dy);
}

function createOperationalMatches(geometry: CampusGeometryBuilding[], operational: Building[]) {
  const result = new Map<string, Building>();
  const used = new Set<string>();
  operational.forEach(building => {
    const buildingName = normalize(building.name);
    const candidates = geometry.map(item => {
      const itemName = normalize(item.name);
      const distance = planarDistanceMeters(building.coords, item.coords);
      const nameMatch = itemName && (itemName.includes(buildingName) || buildingName.includes(itemName));
      return { item, distance, score: nameMatch ? distance - 220 : distance };
    }).sort((a, b) => a.score - b.score);
    const best = candidates.find(candidate => !used.has(candidate.item.osm_id) && (candidate.score < -120 || candidate.distance <= 38));
    if (best) {
      result.set(best.item.osm_id, building);
      used.add(best.item.osm_id);
    }
  });
  return result;
}

function palette(item: CampusGeometryBuilding, operational?: Building) {
  const name = normalize(item.name ?? operational?.name);
  const historic = HISTORIC_NAMES.some(token => name.includes(token));
  const library = name.includes('aptullahkuran') || name.includes('library') || name.includes('kutuphane');
  const sports = (item.building ?? '').includes('sports') || name.includes('spor') || name.includes('gym');
  if (historic) return { facade: 0xb8aea0, roof: 0x78443a, trim: 0xe1d8c9, window: 0x263f4a, historic: true, modern: false };
  if (library) return { facade: 0xaaa79e, roof: 0x76746f, trim: 0xd3d0c7, window: 0x294959, historic: false, modern: false };
  if (sports) return { facade: 0xb8bec1, roof: 0x686f73, trim: 0xe0e4e5, window: 0x315465, historic: false, modern: true };
  return { facade: 0xc3c8c9, roof: 0x6f7679, trim: 0xe1e5e6, window: 0x2a5264, historic: false, modern: true };
}

function scenePoint(point: [number, number], origin: [number, number]) {
  const lngScale = M_PER_DEG_LAT * Math.cos(origin[0] * Math.PI / 180);
  return {
    x: (point[1] - origin[1]) * lngScale * SCALE,
    z: -(point[0] - origin[0]) * M_PER_DEG_LAT * SCALE,
  };
}

function localize(points: [number, number][], origin: [number, number]) {
  const projected = points.map(point => scenePoint(point, origin));
  const center = projected.reduce((acc, point) => ({ x: acc.x + point.x, z: acc.z + point.z }), { x: 0, z: 0 });
  center.x /= projected.length;
  center.z /= projected.length;
  return { center, local: projected.map(point => ({ x: point.x - center.x, z: point.z - center.z })) };
}

function shapeFromLocal(points: { x: number; z: number }[]) {
  const shape = new THREE.Shape();
  points.forEach((point, index) => index === 0 ? shape.moveTo(point.x, -point.z) : shape.lineTo(point.x, -point.z));
  shape.closePath();
  return shape;
}

function boundsOf(points: { x: number; z: number }[]) {
  const xs = points.map(point => point.x);
  const zs = points.map(point => point.z);
  return {
    width: Math.max(1.2, Math.max(...xs) - Math.min(...xs)),
    depth: Math.max(1.2, Math.max(...zs) - Math.min(...zs)),
  };
}

function addFacadeDetails(group: THREE.Group, local: { x: number; z: number }[], levels: number, height: number, colors: ReturnType<typeof palette>, night: boolean) {
  const floorHeight = height / Math.max(1, levels);
  const windowGeometry = new THREE.BoxGeometry(1, 1, 0.08);
  const windowMaterial = new THREE.MeshStandardMaterial({
    color: colors.window,
    emissive: night ? 0xe8b96b : 0x07151b,
    emissiveIntensity: night ? 0.18 : 0.02,
    roughness: 0.2,
    metalness: colors.modern ? 0.35 : 0.08,
  });

  local.forEach((a, edge) => {
    const b = local[(edge + 1) % local.length];
    const dx = b.x - a.x;
    const dz = b.z - a.z;
    const length = Math.hypot(dx, dz);
    if (length < 1.8) return;
    const count = Math.min(colors.historic ? 9 : 12, Math.max(1, Math.floor(length / (colors.historic ? 2.0 : 2.5))));
    const angle = Math.atan2(dz, dx);
    const windowWidth = Math.min(colors.historic ? 0.75 : 1.15, (length / count) * 0.55);
    const windowHeight = Math.min(floorHeight * 0.52, colors.historic ? 1.35 : 1.05);
    for (let floor = 0; floor < Math.min(levels, 9); floor += 1) {
      const y = floorHeight * (floor + 0.57);
      for (let index = 0; index < count; index += 1) {
        const t = (index + 0.5) / count;
        const mesh = new THREE.Mesh(windowGeometry, windowMaterial);
        mesh.scale.set(windowWidth, windowHeight, 1);
        mesh.position.set(a.x + dx * t, y, a.z + dz * t);
        mesh.rotation.y = -angle;
        group.add(mesh);
      }
    }
  });
}

function addHistoricTrim(group: THREE.Group, shape: THREE.Shape, height: number, colors: ReturnType<typeof palette>) {
  const trimMaterial = new THREE.MeshStandardMaterial({ color: colors.trim, roughness: 0.86 });
  [0.08, 0.5, 0.91].forEach(ratio => {
    const geometry = new THREE.ExtrudeGeometry(shape, { depth: 0.12, bevelEnabled: false });
    geometry.rotateX(-Math.PI / 2);
    const band = new THREE.Mesh(geometry, trimMaterial);
    band.position.y = height * ratio;
    band.scale.set(1.012, 1, 1.012);
    group.add(band);
  });
}

function addSignatureFeature(group: THREE.Group, item: CampusGeometryBuilding, bounds: { width: number; depth: number }, height: number, colors: ReturnType<typeof palette>) {
  const name = normalize(item.name);
  if (name.includes('albertlong')) {
    const width = Math.max(2.2, Math.min(bounds.width, bounds.depth) * 0.22);
    const towerHeight = Math.max(3.6, height * 0.32);
    const tower = new THREE.Mesh(new THREE.BoxGeometry(width, towerHeight, width), new THREE.MeshStandardMaterial({ color: colors.facade, roughness: 0.84 }));
    tower.position.y = height + towerHeight / 2 - 0.2;
    tower.castShadow = true;
    group.add(tower);
    const cap = new THREE.Mesh(new THREE.ConeGeometry(width * 0.82, width * 0.72, 4), new THREE.MeshStandardMaterial({ color: colors.roof, roughness: 0.85 }));
    cap.rotation.y = Math.PI / 4;
    cap.position.y = height + towerHeight + width * 0.34;
    group.add(cap);
    const clock = new THREE.Mesh(new THREE.CylinderGeometry(width * 0.24, width * 0.24, 0.08, 28), new THREE.MeshStandardMaterial({ color: 0xe8e2d6, roughness: 0.62 }));
    clock.rotation.x = Math.PI / 2;
    clock.position.set(0, height + towerHeight * 0.68, width / 2 + 0.04);
    group.add(clock);
  }

  if (name.includes('anderson') || name.includes('washburn')) {
    const pediment = new THREE.Mesh(new THREE.ConeGeometry(Math.max(1.6, bounds.width * 0.12), Math.max(1.0, height * 0.09), 3), new THREE.MeshStandardMaterial({ color: colors.trim, roughness: 0.86 }));
    pediment.rotation.z = Math.PI;
    pediment.position.set(0, height * 0.88, bounds.depth / 2 + 0.09);
    group.add(pediment);
  }
}

function buildMesh(item: CampusGeometryBuilding, origin: [number, number], operational: Building | undefined, night: boolean) {
  const ring = cleanRing(item.footprint);
  const { center, local } = localize(ring, origin);
  const shape = shapeFromLocal(local);
  const colors = palette(item, operational);
  const height = Math.max(2.8, item.height_m * SCALE);
  const minHeight = Math.max(0, (item.min_height_m ?? 0) * SCALE);
  const levels = Math.max(1, item.levels ?? Math.round(item.height_m / 3.35));
  const bounds = boundsOf(local);
  const group = new THREE.Group();
  group.position.set(center.x, 0, center.z);
  group.name = item.osm_id;
  group.userData = { geometry: item, operational };

  const bodyGeometry = new THREE.ExtrudeGeometry(shape, { depth: Math.max(0.6, height - minHeight), bevelEnabled: false });
  bodyGeometry.rotateX(-Math.PI / 2);
  const body = new THREE.Mesh(bodyGeometry, new THREE.MeshStandardMaterial({ color: night ? 0x3d4240 : colors.facade, roughness: colors.historic ? 0.88 : 0.7, metalness: colors.modern ? 0.06 : 0.01 }));
  body.position.y = minHeight;
  body.castShadow = true;
  body.receiveShadow = true;
  group.add(body);

  const roofGeometry = new THREE.ExtrudeGeometry(shape, { depth: Math.max(0.12, Math.min(0.7, (item.roof_height_m ?? 0.6) * SCALE)), bevelEnabled: false });
  roofGeometry.rotateX(-Math.PI / 2);
  const roof = new THREE.Mesh(roofGeometry, new THREE.MeshStandardMaterial({ color: colors.roof, roughness: 0.86 }));
  roof.position.y = height;
  roof.castShadow = true;
  group.add(roof);

  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(bodyGeometry, 24), new THREE.LineBasicMaterial({ color: night ? 0x7d8581 : 0x596463, transparent: true, opacity: colors.historic ? 0.34 : 0.2 }));
  edges.position.y = minHeight;
  group.add(edges);

  if (operational || colors.historic) addFacadeDetails(group, local, levels, height, colors, night);
  if (colors.historic) addHistoricTrim(group, shape, height, colors);
  if (colors.historic) addSignatureFeature(group, item, bounds, height, colors);

  if (operational) {
    const ratio = operational.occupancy_ratio ?? 0;
    const status = ratio >= 0.7 ? 0xb91c1c : ratio >= 0.4 ? 0xa16207 : 0x0f766e;
    const marker = new THREE.Mesh(new THREE.SphereGeometry(0.42, 12, 12), new THREE.MeshStandardMaterial({ color: status, emissive: status, emissiveIntensity: night ? 0.58 : 0.2 }));
    marker.position.y = height + 1.2;
    marker.userData.isMarker = true;
    group.add(marker);
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
  const [loading, setLoading] = useState(true);
  const [degraded, setDegraded] = useState(false);
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
        setGeometry(payload.buildings ?? []);
        setDegraded(Boolean(payload.degraded));
      })
      .catch(() => {
        if (!cancelled) {
          setGeometry([]);
          setDegraded(true);
        }
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [campus]);

  const matches = useMemo(() => createOperationalMatches(geometry, buildings), [geometry, buildings]);
  const sourceHeightCount = useMemo(() => geometry.filter(item => Boolean(item.levels) || Boolean(item.roof_height_m)).length, [geometry]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || geometry.length === 0) return;
    const width = container.clientWidth;
    const height = container.clientHeight || 600;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(night ? 0x071117 : 0xdde6e7);
    scene.fog = new THREE.Fog(night ? 0x071117 : 0xdde6e7, 170, 760);

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1600);
    cameraRef.current = camera;
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = night ? 0.86 : 1.02;
    container.replaceChildren(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxPolarAngle = Math.PI / 2.03;

    scene.add(new THREE.HemisphereLight(night ? 0x5c7284 : 0xffffff, night ? 0x0b1513 : 0x788675, night ? 0.65 : 1.25));
    const sun = new THREE.DirectionalLight(night ? 0x6f8aa6 : 0xfff3d4, night ? 1.0 : 2.2);
    sun.position.set(-80, 170, 75);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.near = 1;
    sun.shadow.camera.far = 650;
    sun.shadow.camera.left = -220;
    sun.shadow.camera.right = 220;
    sun.shadow.camera.top = 220;
    sun.shadow.camera.bottom = -220;
    scene.add(sun);

    const origin = CAMPUS_ORIGINS[campus];
    const modelRoot = new THREE.Group();
    geometry.forEach(item => modelRoot.add(buildMesh(item, origin, matches.get(item.osm_id), night)));
    scene.add(modelRoot);

    const box = new THREE.Box3().setFromObject(modelRoot);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const span = Math.max(size.x, size.z, 35);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(span * 1.55, span * 1.55), new THREE.MeshStandardMaterial({ color: night ? 0x17211d : 0x91aa8e, roughness: 1 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(center.x, -0.08, center.z);
    ground.receiveShadow = true;
    scene.add(ground);

    camera.position.set(center.x + span * 0.48, Math.max(42, span * 0.58), center.z + span * 0.76);
    controls.target.copy(center).setY(Math.max(2.5, size.y * 0.18));
    controls.minDistance = Math.max(12, span * 0.08);
    controls.maxDistance = Math.max(180, span * 2.4);
    camera.near = 0.1;
    camera.far = Math.max(1200, span * 6);
    camera.updateProjectionMatrix();
    controls.update();

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const pick = (event: PointerEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      const hit = raycaster.intersectObjects(modelRoot.children, true).find(entry => !(entry.object.userData?.isMarker));
      if (!hit) return;
      let object: THREE.Object3D | null = hit.object;
      while (object && !object.userData?.geometry) object = object.parent;
      if (!object?.userData?.geometry) return;
      const record = { geometry: object.userData.geometry as CampusGeometryBuilding, operational: object.userData.operational as Building | undefined };
      setSelected(record);
      if (record.operational) onSelectBuilding?.(record.operational);
    };
    renderer.domElement.addEventListener('pointerup', pick);

    const onResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight || 600;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
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
        if (object instanceof THREE.Mesh) {
          object.geometry.dispose();
          const materials = Array.isArray(object.material) ? object.material : [object.material];
          materials.forEach(material => material.dispose());
        }
      });
      renderer.dispose();
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
    <div className="relative h-[600px] overflow-hidden rounded-xl border border-slate-900/10 bg-slate-100">
      <div ref={containerRef} className="absolute inset-0" />

      <div className="absolute left-3 top-3 z-10 max-w-[calc(100%-1.5rem)] rounded-xl border border-white/60 bg-white/90 p-2 shadow-sm backdrop-blur-xl">
        <div className="mb-2 flex items-center gap-2 px-1"><Box size={13} className="text-[#173f67]" /><span className="text-[10px] font-black uppercase tracking-[0.13em] text-slate-700">{t('Kaynaklı kampüs geometrisi', 'Source-backed campus geometry')}</span></div>
        <div className="flex max-w-[78vw] gap-1 overflow-x-auto pb-0.5">
          {CAMPUS_OPTIONS.map(option => (
            <button key={option.key} type="button" onClick={() => setCampus(option.key)} className={`shrink-0 rounded-md px-2.5 py-1.5 text-[9px] font-bold transition ${campus === option.key ? 'bg-[#102a43] text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
              {locale === 'tr' ? option.tr : option.en}
            </button>
          ))}
        </div>
      </div>

      <div className="absolute right-3 top-3 z-10 flex gap-1 rounded-lg border border-white/60 bg-white/90 p-1 shadow-sm backdrop-blur-xl">
        <button type="button" onClick={() => setNight(value => !value)} className="rounded-md p-2 text-slate-600 transition hover:bg-slate-100" title={t('Gündüz/gece', 'Day/night')}>
          {night ? <Sun size={14} /> : <Moon size={14} />}
        </button>
        <button type="button" onClick={resetCamera} className="rounded-md p-2 text-slate-600 transition hover:bg-slate-100" title={t('Görüşü sıfırla', 'Reset view')}><RotateCcw size={14} /></button>
      </div>

      <div className="absolute bottom-3 left-3 z-10 max-w-[min(560px,calc(100%-1.5rem))] rounded-xl border border-white/60 bg-slate-950/80 px-3 py-2 text-white shadow-lg backdrop-blur-xl">
        {loading ? <div className="text-[10px] font-semibold text-white/75">{t('Bina geometrileri yükleniyor…', 'Loading building geometry…')}</div> : degraded ? <div className="text-[10px] font-semibold text-amber-200">{t('Açık geometri kaynağı şu an kullanılamıyor.', 'The open geometry source is currently unavailable.')}</div> : (
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[9px] text-white/70">
            <span><strong className="text-white">{geometry.length}</strong> {t('bina footprint’i', 'building footprints')}</span>
            <span><strong className="text-white">{matches.size}</strong> {t('ürün kaydıyla eşleşti', 'matched to product records')}</span>
            <span><strong className="text-white">{sourceHeightCount}</strong> {t('yükseklik/kat etiketi', 'height/level tags')}</span>
            <span>{t('Kaynak: OpenStreetMap. Eksik yükseklikler görselleştirme tahminidir.', 'Source: OpenStreetMap. Missing heights are visualization estimates.')}</span>
          </div>
        )}
      </div>

      {selected && (
        <div className="absolute bottom-3 right-3 z-20 w-[min(330px,calc(100%-1.5rem))] rounded-xl border border-white/60 bg-white/95 p-4 shadow-xl backdrop-blur-xl">
          <button type="button" onClick={() => setSelected(null)} className="absolute right-3 top-2 text-sm font-bold text-slate-400">×</button>
          <div className="pr-6 text-sm font-black text-slate-950">{selected.geometry.name ?? selected.operational?.name ?? t('Adsız OSM binası', 'Unnamed OSM building')}</div>
          <div className="mt-1 text-[9px] font-bold uppercase tracking-[0.12em] text-slate-400">{selected.geometry.campus}</div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-[10px]">
            <div className="rounded-lg bg-slate-50 p-2"><div className="text-slate-400">{t('Model yüksekliği', 'Model height')}</div><div className="mt-1 font-mono font-bold text-slate-800">{selected.geometry.height_m.toFixed(1)} m</div></div>
            <div className="rounded-lg bg-slate-50 p-2"><div className="text-slate-400">{t('Kat etiketi', 'Level tag')}</div><div className="mt-1 font-mono font-bold text-slate-800">{selected.geometry.levels ?? '—'}</div></div>
          </div>
          <div className="mt-3 text-[9px] leading-4 text-slate-500">{selected.geometry.levels ? t('Kat bilgisi açık kaynak bina etiketinden geliyor.', 'Level information comes from the open building tag.') : t('Kaynakta yükseklik/kat yoksa geometri yalnız görselleştirme amaçlı tahmini yükseklik kullanır.', 'When source height/levels are absent, geometry uses an estimated height for visualization only.')}</div>
          <div className="mt-3 flex gap-2">
            <a href={selected.geometry.osm_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 rounded-md border border-slate-200 px-2.5 py-1.5 text-[9px] font-bold text-slate-600">OSM <ExternalLink size={9} /></a>
            {selected.operational && <Link href={`/buildings/${selected.operational.id}`} className="rounded-md bg-[#102a43] px-2.5 py-1.5 text-[9px] font-bold text-white">{t('Bina detayı', 'Building detail')}</Link>}
          </div>
        </div>
      )}
    </div>
  );
}
