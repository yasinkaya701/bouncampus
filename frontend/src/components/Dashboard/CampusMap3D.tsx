'use client';

import Link from 'next/link';
import { useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { Compass, ExternalLink, Moon, RotateCcw, Sun } from 'lucide-react';
import type { Building } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { buildingTypeLabel } from '@/lib/campus-directory';
import {
  type BuildingFootprintLocation,
  type BuildingLocationPayload,
  effectiveHeightMeters,
  effectiveLevels,
  isUsableFootprint,
  modelProfileFor,
  roofHeightMeters,
  roofShapeFor,
} from '@/lib/campus-geometry';

interface CampusMap3DProps {
  buildings: Building[];
  onSelectBuilding?: (building: Building) => void;
}

const ORIGIN_LAT = 41.0850;
const ORIGIN_LNG = 29.0480;
const METERS_PER_DEG_LAT = 111_320;
const METERS_PER_DEG_LNG = 111_320 * Math.cos(ORIGIN_LAT * Math.PI / 180);
const SCENE_SCALE = 0.22;

function toScene(lat: number, lng: number) {
  return {
    x: (lng - ORIGIN_LNG) * METERS_PER_DEG_LNG * SCENE_SCALE,
    z: -(lat - ORIGIN_LAT) * METERS_PER_DEG_LAT * SCENE_SCALE,
  };
}

function cleanFootprint(points: [number, number][]) {
  if (points.length < 3) return points;
  const cleaned = [...points];
  const first = cleaned[0];
  const last = cleaned[cleaned.length - 1];
  if (Math.abs(first[0] - last[0]) < 1e-8 && Math.abs(first[1] - last[1]) < 1e-8) cleaned.pop();
  return cleaned;
}

function averageScenePoint(points: [number, number][], fallback: [number, number]) {
  const usable = points.length >= 3 ? points : [fallback];
  const sum = usable.reduce((acc, point) => {
    const scene = toScene(point[0], point[1]);
    return { x: acc.x + scene.x, z: acc.z + scene.z };
  }, { x: 0, z: 0 });
  return { x: sum.x / usable.length, z: sum.z / usable.length };
}

function footprintShape(points: [number, number][], center: { x: number; z: number }) {
  const shape = new THREE.Shape();
  points.forEach((point, index) => {
    const scene = toScene(point[0], point[1]);
    const x = scene.x - center.x;
    const y = -(scene.z - center.z);
    if (index === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  });
  shape.closePath();
  return shape;
}

function fallbackFootprint(building: Building) {
  const widthMeters = Math.max(18, Math.min(48, Math.sqrt(Math.max(building.total_capacity, 160)) * 1.8));
  const depthMeters = widthMeters * (building.type === 'Library' ? 0.72 : 0.78);
  const halfLat = (depthMeters / 2) / METERS_PER_DEG_LAT;
  const halfLng = (widthMeters / 2) / METERS_PER_DEG_LNG;
  const [lat, lng] = building.coords;
  return [
    [lat - halfLat, lng - halfLng],
    [lat - halfLat, lng + halfLng],
    [lat + halfLat, lng + halfLng],
    [lat + halfLat, lng - halfLng],
  ] as [number, number][];
}

function footprintBounds(local: { x: number; z: number }[]) {
  const xs = local.map(point => point.x);
  const zs = local.map(point => point.z);
  return {
    width: Math.max(2, Math.max(...xs) - Math.min(...xs)),
    depth: Math.max(2, Math.max(...zs) - Math.min(...zs)),
  };
}

function dominantEdgeAngle(local: { x: number; z: number }[]) {
  let longest = 0;
  let angle = 0;
  for (let index = 0; index < local.length; index += 1) {
    const current = local[index];
    const next = local[(index + 1) % local.length];
    const dx = next.x - current.x;
    const dz = next.z - current.z;
    const length = Math.hypot(dx, dz);
    if (length > longest) {
      longest = length;
      angle = Math.atan2(dz, dx);
    }
  }
  return angle;
}

function addWindowRows(
  group: THREE.Group,
  local: { x: number; z: number }[],
  levels: number,
  height: number,
  profile: ReturnType<typeof modelProfileFor>,
  isNightMode: boolean,
) {
  const floorHeight = height / Math.max(levels, 1);
  const windowHeight = Math.max(0.32, floorHeight * (profile.style === 'historic-stone' || profile.style === 'historic-ivy' ? 0.47 : 0.34));
  const material = new THREE.MeshStandardMaterial({
    color: profile.window,
    emissive: isNightMode ? 0xf6c86f : 0x0b1d25,
    emissiveIntensity: isNightMode ? 0.26 : 0.03,
    roughness: 0.18,
    metalness: profile.style === 'modern' ? 0.45 : 0.15,
  });
  const geometry = new THREE.BoxGeometry(1, 1, 0.12);
  const levelStep = Math.max(1, levels > 7 ? 2 : 1);

  for (let edgeIndex = 0; edgeIndex < local.length; edgeIndex += 1) {
    const a = local[edgeIndex];
    const b = local[(edgeIndex + 1) % local.length];
    const dx = b.x - a.x;
    const dz = b.z - a.z;
    const edgeLength = Math.hypot(dx, dz);
    const windows = Math.max(1, Math.min(11, Math.floor(edgeLength / (profile.style === 'brutalist' ? 2.6 : 1.9))));
    const angle = Math.atan2(dz, dx);
    const width = Math.min(1.15, (edgeLength / windows) * 0.56);

    for (let level = 0; level < levels; level += levelStep) {
      const y = Math.min(height - 0.35, floorHeight * (level + 0.56));
      if (profile.style === 'brutalist') {
        const band = new THREE.Mesh(geometry, material);
        band.scale.set(Math.max(0.7, edgeLength * 0.72), windowHeight * 0.52, 1);
        band.position.set((a.x + b.x) / 2, y, (a.z + b.z) / 2);
        band.rotation.y = -angle;
        group.add(band);
        continue;
      }
      for (let index = 0; index < windows; index += 1) {
        const t = (index + 0.5) / windows;
        const windowMesh = new THREE.Mesh(geometry, material);
        windowMesh.scale.set(width, windowHeight, 1);
        windowMesh.position.set(a.x + dx * t, y, a.z + dz * t);
        windowMesh.rotation.y = -angle;
        group.add(windowMesh);
      }
    }
  }
}

function addLandmarkFeature(
  group: THREE.Group,
  building: Building,
  bounds: { width: number; depth: number },
  height: number,
  roofHeight: number,
  isNightMode: boolean,
) {
  const profile = modelProfileFor(building);
  if (profile.landmark === 'clock-tower') {
    const towerWidth = Math.max(2.2, Math.min(bounds.width, bounds.depth) * 0.22);
    const towerHeight = Math.max(3.2, height * 0.28);
    const tower = new THREE.Mesh(
      new THREE.BoxGeometry(towerWidth, towerHeight, towerWidth),
      new THREE.MeshStandardMaterial({ color: isNightMode ? profile.facadeNight : profile.facade, roughness: 0.82 }),
    );
    tower.position.y = height + roofHeight * 0.4 + towerHeight / 2;
    tower.castShadow = true;
    group.add(tower);

    const clockMaterial = new THREE.MeshStandardMaterial({ color: 0xf4efe4, roughness: 0.55 });
    const clock = new THREE.Mesh(new THREE.CylinderGeometry(towerWidth * 0.23, towerWidth * 0.23, 0.12, 24), clockMaterial);
    clock.rotation.x = Math.PI / 2;
    clock.position.set(0, height + roofHeight * 0.4 + towerHeight * 0.62, towerWidth / 2 + 0.07);
    group.add(clock);
  } else if (profile.landmark === 'arched-center') {
    const pediment = new THREE.Mesh(
      new THREE.ConeGeometry(Math.max(1.4, bounds.width * 0.13), Math.max(1.1, height * 0.1), 3),
      new THREE.MeshStandardMaterial({ color: profile.trim, roughness: 0.85 }),
    );
    pediment.rotation.z = Math.PI;
    pediment.position.set(0, height * 0.88, bounds.depth / 2 + 0.08);
    group.add(pediment);
  } else if (profile.landmark === 'cantilever-bands') {
    const slabMaterial = new THREE.MeshStandardMaterial({ color: isNightMode ? 0x4a4d4d : 0xc9c5b9, roughness: 0.88 });
    const slab = new THREE.Mesh(new THREE.BoxGeometry(bounds.width * 1.05, Math.max(0.35, height * 0.055), bounds.depth * 0.96), slabMaterial);
    slab.position.y = height * 0.71;
    slab.castShadow = true;
    group.add(slab);
  }
}

function buildBuildingModel(
  building: Building,
  location: BuildingFootprintLocation | undefined,
  isNightMode: boolean,
) {
  const profile = modelProfileFor(building);
  const footprint = cleanFootprint(isUsableFootprint(location) ? location!.footprint! : fallbackFootprint(building));
  const center = averageScenePoint(footprint, building.coords);
  const local = footprint.map(point => {
    const scene = toScene(point[0], point[1]);
    return { x: scene.x - center.x, z: scene.z - center.z };
  });
  const shape = footprintShape(footprint, center);
  const height = effectiveHeightMeters(building, location) * SCENE_SCALE;
  const roofHeight = roofHeightMeters(building, location) * SCENE_SCALE;
  const levels = effectiveLevels(building, location);
  const bounds = footprintBounds(local);
  const group = new THREE.Group();
  group.name = building.id;
  group.position.set(center.x, 0, center.z);
  group.userData = { building };

  const foundationGeometry = new THREE.ExtrudeGeometry(shape, { depth: 0.32, bevelEnabled: false });
  foundationGeometry.rotateX(-Math.PI / 2);
  const foundation = new THREE.Mesh(
    foundationGeometry,
    new THREE.MeshStandardMaterial({ color: isNightMode ? 0x283039 : 0x8a8d86, roughness: 0.92 }),
  );
  foundation.position.y = -0.02;
  foundation.receiveShadow = true;
  group.add(foundation);

  const bodyGeometry = new THREE.ExtrudeGeometry(shape, { depth: height, bevelEnabled: true, bevelSize: 0.045, bevelThickness: 0.045, bevelSegments: 1 });
  bodyGeometry.rotateX(-Math.PI / 2);
  const bodyMaterial = new THREE.MeshStandardMaterial({
    color: isNightMode ? profile.facadeNight : profile.facade,
    roughness: profile.style === 'brutalist' ? 0.93 : profile.style === 'modern' ? 0.54 : 0.82,
    metalness: profile.style === 'modern' ? 0.12 : 0.02,
  });
  const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
  body.castShadow = true;
  body.receiveShadow = true;
  group.add(body);

  const edgeLines = new THREE.LineSegments(
    new THREE.EdgesGeometry(bodyGeometry, 20),
    new THREE.LineBasicMaterial({ color: isNightMode ? 0x7f8c91 : profile.trim, transparent: true, opacity: 0.55 }),
  );
  group.add(edgeLines);

  addWindowRows(group, local, levels, height, profile, isNightMode);

  const roofShape = roofShapeFor(building, location);
  if (roofShape === 'flat') {
    const roofGeometry = new THREE.ExtrudeGeometry(shape, { depth: Math.max(0.16, roofHeight), bevelEnabled: false });
    roofGeometry.rotateX(-Math.PI / 2);
    const roof = new THREE.Mesh(roofGeometry, new THREE.MeshStandardMaterial({ color: profile.roof, roughness: 0.78 }));
    roof.position.y = height;
    roof.castShadow = true;
    group.add(roof);
  } else if (roofShape === 'gabled') {
    const width = bounds.width * 1.02;
    const depth = bounds.depth * 1.02;
    const h = Math.max(0.7, roofHeight);
    const vertices = new Float32Array([
      -width / 2, 0, -depth / 2,
       width / 2, 0, -depth / 2,
      -width / 2, 0,  depth / 2,
       width / 2, 0,  depth / 2,
      -width / 2, h, 0,
       width / 2, h, 0,
    ]);
    const indices = [0, 1, 5, 0, 5, 4, 2, 4, 5, 2, 5, 3, 0, 4, 2, 1, 3, 5, 0, 2, 3, 0, 3, 1];
    const roofGeometry = new THREE.BufferGeometry();
    roofGeometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    roofGeometry.setIndex(indices);
    roofGeometry.computeVertexNormals();
    const roof = new THREE.Mesh(roofGeometry, new THREE.MeshStandardMaterial({ color: profile.roof, roughness: 0.8 }));
    roof.position.y = height;
    roof.rotation.y = -dominantEdgeAngle(local);
    roof.castShadow = true;
    group.add(roof);
  } else {
    const roof = new THREE.Mesh(
      new THREE.ConeGeometry(1, Math.max(0.8, roofHeight), 4),
      new THREE.MeshStandardMaterial({ color: profile.roof, roughness: 0.82 }),
    );
    roof.scale.set(bounds.width * 0.72, 1, bounds.depth * 0.72);
    roof.rotation.y = Math.PI / 4 - dominantEdgeAngle(local);
    roof.position.y = height + Math.max(0.8, roofHeight) / 2;
    roof.castShadow = true;
    group.add(roof);
  }

  addLandmarkFeature(group, building, bounds, height, roofHeight, isNightMode);

  const occupancy = building.occupancy_ratio ?? 0;
  const signalColor = occupancy >= 0.7 ? 0xb91c1c : occupancy >= 0.4 ? 0xa16207 : 0x0f766e;
  const signal = new THREE.Mesh(
    new THREE.SphereGeometry(0.52, 14, 14),
    new THREE.MeshStandardMaterial({ color: signalColor, emissive: signalColor, emissiveIntensity: isNightMode ? 0.72 : 0.3, roughness: 0.35 }),
  );
  signal.position.y = height + roofHeight + (profile.landmark === 'clock-tower' ? Math.max(3.2, height * 0.28) : 0) + 1.2;
  signal.userData.baseY = signal.position.y;
  signal.userData.isSignal = true;
  group.add(signal);

  return { group, usedRealFootprint: isUsableFootprint(location) };
}

export default function CampusMap3D({ buildings, onSelectBuilding }: CampusMap3DProps) {
  const { locale, t } = useLocale();
  const containerRef = useRef<HTMLDivElement>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<Building | null>(null);
  const [hoveredBuilding, setHoveredBuilding] = useState<Building | null>(null);
  const [isAutoRotate, setIsAutoRotate] = useState(false);
  const [isNightMode, setIsNightMode] = useState(false);
  const [activeCampusView, setActiveCampusView] = useState<'all' | 'south' | 'north'>('all');
  const [locations, setLocations] = useState<Record<string, BuildingFootprintLocation>>({});
  const [geometryDegraded, setGeometryDegraded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch('/api/v1/building-locations', { cache: 'no-store' })
      .then(response => response.ok ? response.json() as Promise<BuildingLocationPayload> : Promise.reject(new Error('geometry source')))
      .then(payload => {
        if (cancelled) return;
        setLocations(Object.fromEntries((payload.locations ?? []).map(location => [location.id, location])));
        setGeometryDegraded(Boolean(payload.degraded));
      })
      .catch(() => {
        if (!cancelled) setGeometryDegraded(true);
      });
    return () => { cancelled = true; };
  }, []);

  const realFootprintCount = useMemo(
    () => buildings.filter(building => isUsableFootprint(locations[building.id])).length,
    [buildings, locations],
  );

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight || 520;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(isNightMode ? 0x09131b : 0xe8eef0);
    scene.fog = new THREE.Fog(isNightMode ? 0x09131b : 0xe8eef0, 150, 340);

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 900);
    camera.position.set(15, 92, 185);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = isNightMode ? 0.82 : 1.05;
    container.replaceChildren(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;
    controls.enableDamping = true;
    controls.dampingFactor = 0.055;
    controls.maxPolarAngle = Math.PI / 2.04;
    controls.minDistance = 18;
    controls.maxDistance = 330;
    controls.target.set(0, 5, 0);

    scene.add(new THREE.HemisphereLight(isNightMode ? 0x5f7690 : 0xffffff, isNightMode ? 0x0c1720 : 0x77836f, isNightMode ? 0.65 : 1.15));
    const sun = new THREE.DirectionalLight(isNightMode ? 0x6c8bb4 : 0xfff5dc, isNightMode ? 1.0 : 2.1);
    sun.position.set(-75, 130, 65);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.near = 5;
    sun.shadow.camera.far = 340;
    sun.shadow.camera.left = -130;
    sun.shadow.camera.right = 130;
    sun.shadow.camera.top = 130;
    sun.shadow.camera.bottom = -130;
    scene.add(sun);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(360, 360),
      new THREE.MeshStandardMaterial({ color: isNightMode ? 0x17251f : 0x9fb49c, roughness: 1 }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.34;
    ground.receiveShadow = true;
    scene.add(ground);

    const water = new THREE.Mesh(
      new THREE.PlaneGeometry(105, 360),
      new THREE.MeshStandardMaterial({ color: isNightMode ? 0x071e2f : 0x477d9f, roughness: 0.25, metalness: 0.18 }),
    );
    water.rotation.x = -Math.PI / 2;
    water.position.set(142, -0.29, 5);
    scene.add(water);

    const groups = new Map<string, THREE.Group>();
    buildings.forEach(building => {
      const model = buildBuildingModel(building, locations[building.id], isNightMode);
      scene.add(model.group);
      groups.set(building.id, model.group);
    });

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const buildingFromHit = (object: THREE.Object3D | null) => {
      let current = object;
      while (current && !current.userData?.building) current = current.parent;
      return current?.userData?.building as Building | undefined;
    };

    const updatePointer = (event: PointerEvent | MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      return raycaster.intersectObjects([...groups.values()], true);
    };

    const handlePointerMove = (event: PointerEvent) => {
      const intersections = updatePointer(event);
      const building = intersections.length ? buildingFromHit(intersections[0].object) : undefined;
      setHoveredBuilding(building ?? null);
      renderer.domElement.style.cursor = building ? 'pointer' : 'grab';
    };

    const handleClick = (event: MouseEvent) => {
      const intersections = updatePointer(event);
      for (const hit of intersections) {
        const building = buildingFromHit(hit.object);
        if (!building) continue;
        setSelectedBuilding(building);
        onSelectBuilding?.(building);
        const target = groups.get(building.id)?.position;
        if (target) {
          controls.target.set(target.x, 4, target.z);
          const offset = new THREE.Vector3(30, 25, 38);
          camera.position.copy(new THREE.Vector3(target.x, 0, target.z).add(offset));
        }
        break;
      }
    };

    renderer.domElement.addEventListener('pointermove', handlePointerMove);
    renderer.domElement.addEventListener('click', handleClick);

    const clock = new THREE.Clock();
    const animate = () => {
      animationFrameRef.current = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();
      groups.forEach(group => {
        const signal = group.children.find(child => child.userData?.isSignal);
        if (signal && typeof signal.userData.baseY === 'number') signal.position.y = signal.userData.baseY + Math.sin(elapsed * 2.2 + group.position.x * 0.05) * 0.14;
      });
      controls.autoRotate = isAutoRotate;
      controls.autoRotateSpeed = 0.7;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      const nextWidth = container.clientWidth;
      const nextHeight = container.clientHeight || 520;
      camera.aspect = nextWidth / nextHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(nextWidth, nextHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      renderer.domElement.removeEventListener('pointermove', handlePointerMove);
      renderer.domElement.removeEventListener('click', handleClick);
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      scene.traverse(object => {
        if (object instanceof THREE.Mesh || object instanceof THREE.LineSegments) {
          object.geometry?.dispose();
          const material = object.material;
          if (Array.isArray(material)) material.forEach(item => item.dispose());
          else material?.dispose();
        }
      });
      controls.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement);
    };
  }, [buildings, locations, isAutoRotate, isNightMode, onSelectBuilding]);

  const handleFocus = (view: 'all' | 'south' | 'north') => {
    setActiveCampusView(view);
    const camera = cameraRef.current;
    const controls = controlsRef.current;
    if (!camera || !controls) return;
    if (view === 'south') {
      const target = toScene(41.0831, 29.0514);
      controls.target.set(target.x, 4, target.z);
      camera.position.set(target.x + 36, 48, target.z + 64);
    } else if (view === 'north') {
      const target = toScene(41.0866, 29.0442);
      controls.target.set(target.x, 5, target.z);
      camera.position.set(target.x - 42, 52, target.z + 58);
    } else {
      controls.target.set(0, 5, 0);
      camera.position.set(15, 92, 185);
    }
    controls.update();
  };

  const selectedLocation = selectedBuilding ? locations[selectedBuilding.id] : undefined;

  return (
    <div className="relative h-[520px] w-full select-none overflow-hidden rounded-xl border border-slate-900/10 bg-slate-950 shadow-sm">
      <div ref={containerRef} className="h-full w-full" />

      <div className="absolute left-3 right-3 top-3 flex items-start justify-between gap-3 pointer-events-none">
        <div className="pointer-events-auto flex flex-wrap items-center gap-1 rounded-lg border border-white/20 bg-slate-950/72 p-1.5 text-white shadow-lg backdrop-blur-md">
          {(['all', 'south', 'north'] as const).map(view => (
            <button key={view} type="button" onClick={() => handleFocus(view)} className={`rounded-md px-2.5 py-1.5 text-[10px] font-bold transition ${activeCampusView === view ? 'bg-white text-slate-950' : 'text-slate-200 hover:bg-white/10'}`}>
              {view === 'all' ? t('Tümü', 'All') : view === 'south' ? t('Güney', 'South') : t('Kuzey', 'North')}
            </button>
          ))}
        </div>
        <div className="pointer-events-auto flex items-center gap-1 rounded-lg border border-white/20 bg-slate-950/72 p-1.5 text-white shadow-lg backdrop-blur-md">
          <button type="button" onClick={() => setIsAutoRotate(value => !value)} title={t('Otomatik tur', 'Auto tour')} className={`rounded-md p-1.5 transition ${isAutoRotate ? 'bg-white text-slate-950' : 'text-slate-200 hover:bg-white/10'}`}><RotateCcw size={14} /></button>
          <button type="button" onClick={() => setIsNightMode(value => !value)} title={t('Gece / gündüz', 'Night / day')} className="rounded-md p-1.5 text-slate-200 transition hover:bg-white/10">{isNightMode ? <Sun size={14} /> : <Moon size={14} />}</button>
          <button type="button" onClick={() => handleFocus('all')} title={t('Kamerayı sıfırla', 'Reset camera')} className="rounded-md p-1.5 text-slate-200 transition hover:bg-white/10"><Compass size={14} /></button>
        </div>
      </div>

      <div className="absolute bottom-3 left-3 max-w-[min(92%,420px)] rounded-lg border border-white/15 bg-slate-950/78 px-3 py-2 text-[10px] text-slate-200 shadow-lg backdrop-blur-md pointer-events-none">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 font-bold text-white">
          <span>{t('Gerçek bina geometrisi', 'Real building geometry')}</span>
          <span className="font-mono text-emerald-300">{realFootprintCount}/{buildings.length} OSM</span>
          {geometryDegraded && <span className="text-amber-300">{t('OSM geçici olarak kullanılamıyor', 'OSM temporarily unavailable')}</span>}
        </div>
        <div className="mt-1 leading-4 text-slate-300">{t('Bina ayak izi, yönü ve varsa yükseklik/kat bilgisi OpenStreetMap geometrisinden; eşleşmeyen binalar açıkça yaklaşık modelden çizilir.', 'Footprints, orientation and available height/level data come from OpenStreetMap geometry; unmatched buildings use an explicit approximate fallback model.')}</div>
      </div>

      {hoveredBuilding && !selectedBuilding && (
        <div className="pointer-events-none absolute left-1/2 top-16 -translate-x-1/2 rounded-lg border border-white/15 bg-slate-950/86 px-3 py-2 text-[11px] text-white shadow-lg backdrop-blur-md">
          <span className="font-bold">{hoveredBuilding.name}</span>
          <span className="mx-2 text-slate-500">•</span>
          <span>{effectiveLevels(hoveredBuilding, locations[hoveredBuilding.id])} {t('kat', 'levels')}</span>
          <span className="mx-2 text-slate-500">•</span>
          <span>{Math.round(effectiveHeightMeters(hoveredBuilding, locations[hoveredBuilding.id]))} m</span>
        </div>
      )}

      {selectedBuilding && (
        <div className="pointer-events-auto absolute bottom-3 right-3 w-[min(320px,calc(100%-24px))] rounded-xl border border-slate-900/10 bg-white/96 p-4 text-slate-900 shadow-2xl backdrop-blur-md">
          <div className="flex items-start justify-between gap-3">
            <div><h3 className="text-sm font-black tracking-[-0.02em]">{selectedBuilding.name}</h3><p className="mt-0.5 text-[10px] text-slate-500">{buildingTypeLabel(selectedBuilding.type, locale)} · {selectedBuilding.campus === 'south' ? t('Güney Kampüs', 'South Campus') : t('Kuzey Kampüs', 'North Campus')}</p></div>
            <button type="button" onClick={() => setSelectedBuilding(null)} className="rounded p-1 text-xs font-bold text-slate-400 hover:bg-slate-100">✕</button>
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2">
            <div className="rounded-lg bg-slate-50 p-2"><span className="block text-[9px] text-slate-400">{t('Geometri', 'Geometry')}</span><span className={`mt-0.5 block text-[10px] font-bold ${isUsableFootprint(selectedLocation) ? 'text-emerald-700' : 'text-amber-700'}`}>{isUsableFootprint(selectedLocation) ? 'OSM footprint' : t('yaklaşık', 'fallback')}</span></div>
            <div className="rounded-lg bg-slate-50 p-2"><span className="block text-[9px] text-slate-400">{t('Kat', 'Levels')}</span><span className="mt-0.5 block text-[11px] font-black">{effectiveLevels(selectedBuilding, selectedLocation)}</span></div>
            <div className="rounded-lg bg-slate-50 p-2"><span className="block text-[9px] text-slate-400">{t('Yükseklik', 'Height')}</span><span className="mt-0.5 block text-[11px] font-black">≈{Math.round(effectiveHeightMeters(selectedBuilding, selectedLocation))} m</span></div>
          </div>
          <p className="mt-3 text-[9px] leading-4 text-slate-500">{t('Doluluk rengi yalnızca ders programı tabanlı tahmini göstergedir; canlı kişi sayacı değildir.', 'Occupancy color is a schedule-derived estimate only; it is not a live people counter.')}</p>
          <div className="mt-3 flex items-center justify-between gap-2">
            <Link href={`/buildings/${selectedBuilding.id}`} className="rounded-lg bg-[#102a43] px-3 py-2 text-[10px] font-bold text-white">{t('Bina detayı', 'Building detail')}</Link>
            {selectedLocation?.osm_url && <a href={selectedLocation.osm_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[10px] font-bold text-slate-500 hover:text-slate-900">OpenStreetMap <ExternalLink size={10} /></a>}
          </div>
        </div>
      )}
    </div>
  );
}
