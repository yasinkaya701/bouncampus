'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { Building } from '@/lib/types';
import Link from 'next/link';
import { Layers, Eye, Compass, Sun, Moon, Maximize2, RotateCcw, Volume2, VolumeX, Sparkles } from 'lucide-react';

interface CampusMap3DProps {
  buildings: Building[];
  onSelectBuilding?: (building: Building) => void;
}

const CENTER_LAT = 41.0850;
const CENTER_LNG = 29.0475;
const SCALE_FACTOR = 16000;

export default function CampusMap3D({ buildings, onSelectBuilding }: CampusMap3DProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<Building | null>(null);
  const [hoveredBuilding, setHoveredBuilding] = useState<Building | null>(null);
  const [isAutoRotate, setIsAutoRotate] = useState(false);
  const [isNightMode, setIsNightMode] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [activeCampusView, setActiveCampusView] = useState<'all' | 'south' | 'north'>('all');

  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const buildingMeshesRef = useRef<Map<string, THREE.Group>>(new Map());
  const animationFrameRef = useRef<number | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);

  // Synthesized Web Audio Campus Soundscape
  const toggleSoundscape = () => {
    if (isPlayingAudio) {
      if (audioCtxRef.current) {
        audioCtxRef.current.close();
        audioCtxRef.current = null;
      }
      setIsPlayingAudio(false);
    } else {
      try {
        const AudioClass = window.AudioContext || (window as any).webkitAudioContext;
        if (!AudioClass) return;
        const ctx = new AudioClass();
        audioCtxRef.current = ctx;

        // Warm ambient synth chord (Fmaj9 / campus breeze feel)
        const freqs = [174.61, 220.0, 261.63, 329.63];
        const masterGain = ctx.createGain();
        masterGain.gain.setValueAtTime(0.015, ctx.currentTime);
        masterGain.connect(ctx.destination);

        freqs.forEach(freq => {
          const osc = ctx.createOscillator();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, ctx.currentTime);
          osc.connect(masterGain);
          osc.start();
        });

        setIsPlayingAudio(true);
      } catch (e) {
        console.error('Web Audio init error', e);
      }
    }
  };

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight || 460;

    // 1. Scene setup
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(isNightMode ? 0x0a1118 : 0xebf2f8);
    scene.fog = new THREE.FogExp2(isNightMode ? 0x0a1118 : 0xebf2f8, 0.0035);

    // 2. Camera setup
    const camera = new THREE.PerspectiveCamera(45, width / height, 1, 1000);
    camera.position.set(0, 75, 120);
    cameraRef.current = camera;

    // 3. Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    // 4. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2.05;
    controls.minDistance = 20;
    controls.maxDistance = 250;
    controls.target.set(0, 0, 0);

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(
      isNightMode ? 0x223344 : 0xffffff,
      isNightMode ? 0.6 : 0.85
    );
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(
      isNightMode ? 0x3b82f6 : 0xfffaed,
      isNightMode ? 0.8 : 1.3
    );
    sunLight.position.set(60, 100, 40);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 300;
    const d = 120;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    scene.add(sunLight);

    // Bosphorus Water Plane on the East
    const waterGeometry = new THREE.PlaneGeometry(160, 300);
    const waterMaterial = new THREE.MeshStandardMaterial({
      color: isNightMode ? 0x061525 : 0x1d4ed8,
      roughness: 0.2,
      metalness: 0.8,
      opacity: 0.85,
      transparent: true
    });
    const water = new THREE.Mesh(waterGeometry, waterMaterial);
    water.rotation.x = -Math.PI / 2;
    water.position.set(90, -1.5, 0);
    scene.add(water);

    // Ground Plane with grid
    const groundGeo = new THREE.PlaneGeometry(350, 350);
    const groundMat = new THREE.MeshStandardMaterial({
      color: isNightMode ? 0x111c26 : 0xd8e4ed,
      roughness: 0.9,
      metalness: 0.1
    });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    ground.position.y = -1;
    scene.add(ground);

    const gridHelper = new THREE.GridHelper(
      350,
      70,
      isNightMode ? 0x1f3448 : 0x94a3b8,
      isNightMode ? 0x142331 : 0xcfdce8
    );
    gridHelper.position.y = -0.9;
    scene.add(gridHelper);

    // 6. Add 3D Buildings
    const meshesMap = new Map<string, THREE.Group>();

    buildings.forEach(b => {
      const group = new THREE.Group();
      group.name = b.id;

      const x = (b.coords[1] - CENTER_LNG) * SCALE_FACTOR;
      const z = -(b.coords[0] - CENTER_LAT) * SCALE_FACTOR;

      const floors = b.floors || 4;
      const floorHeight = 2.4;
      const baseWidth = Math.max(7, Math.min(16, (b.total_capacity || 400) / 45));
      const baseDepth = Math.max(7, Math.min(14, baseWidth * 0.85));

      const occ = b.occupancy_ratio || 0;
      let buildingColor = 0x10b981; // green
      let emissiveColor = 0x059669;
      if (occ >= 0.7) {
        buildingColor = 0xef4444; // red
        emissiveColor = 0xdc2626;
      } else if (occ >= 0.4) {
        buildingColor = 0xf59e0b; // yellow/amber
        emissiveColor = 0xd97706;
      }

      const isHistoric = b.campus === 'south' && ['Anderson', 'Washburn', 'Perkins', 'Albert'].some(n => b.name.includes(n));
      const bodyColor = isHistoric ? (isNightMode ? 0x4a3b32 : 0xd6c2a8) : (isNightMode ? 0x223547 : 0xe2e8f0);

      // Building base plinth
      const plinthGeo = new THREE.BoxGeometry(baseWidth + 1, 0.6, baseDepth + 1);
      const plinthMat = new THREE.MeshStandardMaterial({
        color: isNightMode ? 0x1e293b : 0x64748b,
        roughness: 0.8
      });
      const plinth = new THREE.Mesh(plinthGeo, plinthMat);
      plinth.position.y = 0.3;
      plinth.receiveShadow = true;
      group.add(plinth);

      // Floors structure
      for (let f = 0; f < floors; f++) {
        const floorY = 0.6 + (f * floorHeight) + (floorHeight / 2);
        const fWidth = baseWidth - (f * 0.2);
        const fDepth = baseDepth - (f * 0.2);

        const floorGeo = new THREE.BoxGeometry(fWidth, floorHeight * 0.85, fDepth);
        const floorMat = new THREE.MeshStandardMaterial({
          color: bodyColor,
          roughness: 0.4,
          metalness: isHistoric ? 0.1 : 0.4,
        });
        const floorMesh = new THREE.Mesh(floorGeo, floorMat);
        floorMesh.position.y = floorY;
        floorMesh.castShadow = true;
        floorMesh.receiveShadow = true;
        group.add(floorMesh);

        // Window band with live occupancy glow
        const windowGeo = new THREE.BoxGeometry(fWidth + 0.15, floorHeight * 0.4, fDepth + 0.15);
        const windowMat = new THREE.MeshStandardMaterial({
          color: isNightMode ? buildingColor : 0x38bdf8,
          emissive: buildingColor,
          emissiveIntensity: occ > 0.4 ? (isNightMode ? 0.9 : 0.4) : 0.15,
          roughness: 0.1,
          metalness: 0.8,
          transparent: true,
          opacity: 0.85
        });
        const windowMesh = new THREE.Mesh(windowGeo, windowMat);
        windowMesh.position.y = floorY;
        group.add(windowMesh);
      }

      // Roof cap
      const roofGeo = new THREE.BoxGeometry(baseWidth - (floors * 0.2) + 0.4, 0.4, baseDepth - (floors * 0.2) + 0.4);
      const roofMat = new THREE.MeshStandardMaterial({
        color: isHistoric ? 0x991b1b : (isNightMode ? 0x0f172a : 0x475569),
        roughness: 0.5
      });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.y = 0.6 + (floors * floorHeight) + 0.2;
      roof.castShadow = true;
      group.add(roof);

      // 3D Floating Beacon on top
      const beaconGeo = new THREE.SphereGeometry(1.0, 16, 16);
      const beaconMat = new THREE.MeshStandardMaterial({
        color: buildingColor,
        emissive: emissiveColor,
        emissiveIntensity: 0.9,
        roughness: 0.2,
      });
      const beacon = new THREE.Mesh(beaconGeo, beaconMat);
      beacon.position.y = 0.6 + (floors * floorHeight) + 2.2;
      group.add(beacon);

      group.position.set(x, 0, z);
      (group as any).userData = { building: b };

      scene.add(group);
      meshesMap.set(b.id, group);
    });

    buildingMeshesRef.current = meshesMap;

    // 6.5 Dynamic 3D Student Flow Particles along Campus Roads
    const particleCount = 120;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleProgress = new Float32Array(particleCount);
    const particleSpeed = new Float32Array(particleCount);

    const curves = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-45, 1.2, -35),
        new THREE.Vector3(-42, 1.2, -20),
        new THREE.Vector3(-48, 1.2, -5),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(45, 1.2, 35),
        new THREE.Vector3(50, 1.2, 25),
        new THREE.Vector3(52, 1.2, 10),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-40, 1.5, -10),
        new THREE.Vector3(0, 1.5, 0),
        new THREE.Vector3(45, 1.5, 20),
      ])
    ];

    for (let i = 0; i < particleCount; i++) {
      particleProgress[i] = Math.random();
      particleSpeed[i] = 0.003 + Math.random() * 0.004;
      const c = curves[i % curves.length];
      const pt = c.getPoint(particleProgress[i]);
      particlePositions[i * 3] = pt.x;
      particlePositions[i * 3 + 1] = pt.y;
      particlePositions[i * 3 + 2] = pt.z;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0x10b981,
      size: 2.2,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending
    });
    const flowPoints = new THREE.Points(particleGeo, particleMat);
    scene.add(flowPoints);

    // 7. Raycasting for hover & click selection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handlePointerMove = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children, true);

      let foundBuilding: Building | null = null;
      for (const hit of intersects) {
        let parent: THREE.Object3D | null = hit.object;
        while (parent && !(parent as any).userData?.building) {
          parent = parent.parent;
        }
        if (parent && (parent as any).userData?.building) {
          foundBuilding = (parent as any).userData.building;
          break;
        }
      }

      setHoveredBuilding(foundBuilding);
      renderer.domElement.style.cursor = foundBuilding ? 'pointer' : 'default';
    };

    const handleClick = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children, true);

      for (const hit of intersects) {
        let parent: THREE.Object3D | null = hit.object;
        while (parent && !(parent as any).userData?.building) {
          parent = parent.parent;
        }
        if (parent && (parent as any).userData?.building) {
          const b = (parent as any).userData.building as Building;
          setSelectedBuilding(b);
          if (onSelectBuilding) onSelectBuilding(b);

          const bx = parent.position.x;
          const bz = parent.position.z;
          controls.target.set(bx, 10, bz);
          break;
        }
      }
    };

    const domElem = renderer.domElement;
    domElem.addEventListener('pointermove', handlePointerMove);
    domElem.addEventListener('click', handleClick);

    // 8. Animation loop
    const clock = new THREE.Clock();
    const animate = () => {
      animationFrameRef.current = requestAnimationFrame(animate);

      const elapsedTime = clock.getElapsedTime();

      // Gentle floating animation on building top beacons
      meshesMap.forEach(group => {
        const beacon = group.children[group.children.length - 1];
        if (beacon) {
          beacon.position.y += Math.sin(elapsedTime * 3 + group.position.x) * 0.008;
        }
      });

      // Advance 3D flow particles
      const posAttr = particleGeo.attributes.position;
      for (let i = 0; i < particleCount; i++) {
        particleProgress[i] = (particleProgress[i] + particleSpeed[i]) % 1.0;
        const c = curves[i % curves.length];
        const pt = c.getPoint(particleProgress[i]);
        posAttr.setXYZ(i, pt.x, pt.y, pt.z);
      }
      posAttr.needsUpdate = true;

      if (controlsRef.current) {
        controlsRef.current.autoRotate = isAutoRotate;
        controlsRef.current.autoRotateSpeed = 1.2;
        controlsRef.current.update();
      }

      renderer.render(scene, camera);
    };

    animate();

    // Resize handler
    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight || 460;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      domElem.removeEventListener('pointermove', handlePointerMove);
      domElem.removeEventListener('click', handleClick);
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      renderer.dispose();
    };
  }, [buildings, isNightMode, isAutoRotate, onSelectBuilding]);

  // Camera presets
  const handleFocus = (view: 'all' | 'south' | 'north') => {
    setActiveCampusView(view);
    if (!cameraRef.current || !controlsRef.current) return;

    if (view === 'south') {
      controlsRef.current.target.set(50, 5, 25);
      cameraRef.current.position.set(50, 45, 80);
    } else if (view === 'north') {
      controlsRef.current.target.set(-50, 5, -25);
      cameraRef.current.position.set(-50, 45, 30);
    } else {
      controlsRef.current.target.set(0, 0, 0);
      cameraRef.current.position.set(0, 75, 120);
    }
  };

  return (
    <div className="relative w-full h-[460px] rounded-xl overflow-hidden border border-gray-200 shadow-sm bg-slate-900 select-none">
      <div ref={containerRef} className="w-full h-full" />

      {/* Top Controls Overlay */}
      <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
        {/* Campus Focus Buttons */}
        <div className="flex items-center space-x-1.5 pointer-events-auto bg-white/90 backdrop-blur-md px-2.5 py-1.5 rounded-lg shadow-sm border border-gray-200">
          <button
            onClick={() => handleFocus('all')}
            className={`px-2.5 py-1 rounded-md text-xs font-semibold transition ${activeCampusView === 'all' ? 'bg-emerald-700 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            Tüm Kampüs
          </button>
          <button
            onClick={() => handleFocus('south')}
            className={`px-2.5 py-1 rounded-md text-xs font-semibold transition ${activeCampusView === 'south' ? 'bg-emerald-700 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            Güney (Bebek)
          </button>
          <button
            onClick={() => handleFocus('north')}
            className={`px-2.5 py-1 rounded-md text-xs font-semibold transition ${activeCampusView === 'north' ? 'bg-emerald-700 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            Kuzey (Hisarüstü)
          </button>
        </div>

        {/* 3D Toolbar Controls */}
        <div className="flex items-center space-x-1.5 pointer-events-auto bg-white/90 backdrop-blur-md px-2 py-1.5 rounded-lg shadow-sm border border-gray-200">
          <button
            onClick={() => setIsAutoRotate(!isAutoRotate)}
            title="Otomatik 3D Döndürme (Drone Turu)"
            className={`p-1.5 rounded-md text-xs font-medium transition flex items-center gap-1 ${isAutoRotate ? 'bg-indigo-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <RotateCcw size={14} className={isAutoRotate ? 'animate-spin' : ''} />
            <span className="hidden sm:inline">3D Tur</span>
          </button>
          <button
            onClick={toggleSoundscape}
            title={isPlayingAudio ? 'Kampüs Ambiyans Sesini Kapat' : 'Kampüs Ambiyans Sesini Aç'}
            className={`p-1.5 rounded-md text-xs transition ${isPlayingAudio ? 'bg-teal-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            {isPlayingAudio ? <Volume2 size={14} className="animate-pulse" /> : <VolumeX size={14} />}
          </button>
          <button
            onClick={() => setIsNightMode(!isNightMode)}
            title="Gece / Gündüz Aydınlatması"
            className={`p-1.5 rounded-md text-xs transition ${isNightMode ? 'bg-amber-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            {isNightMode ? <Sun size={14} /> : <Moon size={14} />}
          </button>
          <button
            onClick={() => handleFocus('all')}
            title="Kamerayı Sıfırla"
            className="p-1.5 rounded-md text-xs text-gray-700 hover:bg-gray-100 transition"
          >
            <Compass size={14} />
          </button>
        </div>
      </div>

      {/* 3D Legend & Particles Badge */}
      <div className="absolute bottom-3 left-3 pointer-events-none">
        <div className="bg-white/90 backdrop-blur-md px-3 py-2 rounded-lg shadow-sm border border-gray-200 text-[11px] text-gray-700 space-y-1">
          <div className="font-bold flex items-center justify-between gap-2 text-gray-900">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
              3D Dijital İkiz (Real-time WebGL)
            </span>
            <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.2 rounded">
              3D Akış Parçacıkları Aktif
            </span>
          </div>
          <div className="flex items-center gap-3 text-[10px] text-gray-600">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-emerald-500"></span> &lt;%40 Sakin</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-amber-500"></span> %40-70 Normal</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-rose-500"></span> &gt;%70 Yoğun</span>
          </div>
          <div className="text-[9px] text-gray-400">
            Sol tık: Döndür • Sağ tık: Kaydır • Scroll: Yakınlaş • Yeşil Parçacıklar: Canlı Öğrenci Akışı
          </div>
        </div>
      </div>

      {/* Hover Tooltip */}
      {hoveredBuilding && !selectedBuilding && (
        <div className="absolute top-16 left-1/2 -translate-x-1/2 pointer-events-none bg-gray-900/90 text-white px-3 py-1.5 rounded-lg text-xs shadow-lg backdrop-blur-md border border-gray-700 flex items-center gap-2 animate-fade-in">
          <span className="font-bold">{hoveredBuilding.name} ({hoveredBuilding.code})</span>
          <span className="text-gray-400">•</span>
          <span>{hoveredBuilding.floors} Kat</span>
          <span className="text-gray-400">•</span>
          <span className={`font-bold ${hoveredBuilding.occupancy_ratio && hoveredBuilding.occupancy_ratio >= 0.7 ? 'text-rose-400' : hoveredBuilding.occupancy_ratio && hoveredBuilding.occupancy_ratio >= 0.4 ? 'text-amber-400' : 'text-emerald-400'}`}>
            %{Math.round((hoveredBuilding.occupancy_ratio || 0) * 100)} Doluluk
          </span>
        </div>
      )}

      {/* Selected Building 3D Card / Modal Popup */}
      {selectedBuilding && (
        <div className="absolute bottom-3 right-3 pointer-events-auto bg-white/95 backdrop-blur-md rounded-xl p-4 shadow-xl border border-gray-200 w-72 transition-all">
          <div className="flex items-start justify-between mb-1.5">
            <div>
              <h3 className="font-bold text-sm text-gray-900">{selectedBuilding.name}</h3>
              <p className="text-xs text-gray-500">
                {selectedBuilding.campus === 'south' ? 'Güney (Bebek)' : 'Kuzey (Hisarüstü)'} • {selectedBuilding.type}
              </p>
            </div>
            <button
              onClick={() => setSelectedBuilding(null)}
              className="text-gray-400 hover:text-gray-600 text-xs font-bold px-1.5 py-0.5 rounded-md hover:bg-gray-100"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 my-3 text-xs">
            <div className="bg-gray-50 p-2 rounded-lg">
              <span className="text-gray-500 block text-[10px]">Kat Sayısı</span>
              <span className="font-bold text-gray-800">{selectedBuilding.floors} Kat</span>
            </div>
            <div className="bg-gray-50 p-2 rounded-lg">
              <span className="text-gray-500 block text-[10px]">Toplam Kapasite</span>
              <span className="font-bold text-gray-800">{selectedBuilding.total_capacity} Kişi</span>
            </div>
            <div className="bg-gray-50 p-2 rounded-lg">
              <span className="text-gray-500 block text-[10px]">Canlı Doluluk</span>
              <span className={`font-bold ${selectedBuilding.occupancy_ratio && selectedBuilding.occupancy_ratio >= 0.7 ? 'text-rose-600' : selectedBuilding.occupancy_ratio && selectedBuilding.occupancy_ratio >= 0.4 ? 'text-amber-600' : 'text-emerald-600'}`}>
                %{Math.round((selectedBuilding.occupancy_ratio || 0) * 100)} ({selectedBuilding.current_occupancy || 0} Kişi)
              </span>
            </div>
            <div className="bg-gray-50 p-2 rounded-lg">
              <span className="text-gray-500 block text-[10px]">Taban Enerji</span>
              <span className="font-bold text-emerald-700">{selectedBuilding.energy_profile?.base_load_kw || 30} kW</span>
            </div>
          </div>

          <Link
            href={`/buildings/${selectedBuilding.id}`}
            className="w-full bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold py-2 px-3 rounded-lg block text-center transition shadow-xs"
          >
            Kat & Enerji Detayını Aç &rarr;
          </Link>
        </div>
      )}
    </div>
  );
}
