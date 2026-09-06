'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { RotateCcw } from 'lucide-react';

interface Building3DFloorStackProps {
  floorsCount: number;
  buildingName: string;
  getFloorOccupancy: (floor: number) => number;
}

export default function Building3DFloorStack({
  floorsCount,
  buildingName,
  getFloorOccupancy
}: Building3DFloorStackProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredFloor, setHoveredFloor] = useState<{ floor: number; occ: number } | null>(null);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    if (!containerRef.current) return;
    const width = containerRef.current.clientWidth;
    const height = 280;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf8fafc); // slate-50

    // Camera
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(18, 14, 18);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;

    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = isRotating;
    controls.autoRotateSpeed = 2.0;
    controls.minDistance = 10;
    controls.maxDistance = 40;
    controls.target.set(0, (floorsCount * 2.2) / 2, 0);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(15, 25, 10);
    dirLight.castShadow = true;
    scene.add(dirLight);

    // Ground shadow plinth
    const groundGeo = new THREE.CylinderGeometry(10, 10, 0.4, 32);
    const groundMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.9 });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.position.y = -0.2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // Build 3D Floor Slabs
    const floorMeshes: THREE.Mesh[] = [];
    const slabWidth = 9;
    const slabDepth = 7;
    const slabHeight = 1.0;
    const verticalGap = 2.2;

    for (let f = 1; f <= floorsCount; f++) {
      const occ = getFloorOccupancy(f);
      const isEco = f > 2 && occ < 25;

      let floorColor = 0x10b981; // green
      let emissive = 0x059669;
      if (occ >= 70) {
        floorColor = 0xef4444; // red
        emissive = 0xb91c1c;
      } else if (occ >= 40) {
        floorColor = 0xf59e0b; // yellow
        emissive = 0xd97706;
      }

      // Main slab
      const geo = new THREE.BoxGeometry(slabWidth, slabHeight, slabDepth);
      const mat = new THREE.MeshStandardMaterial({
        color: floorColor,
        emissive: emissive,
        emissiveIntensity: 0.25,
        roughness: 0.2,
        metalness: 0.5,
        transparent: true,
        opacity: 0.88
      });
      const mesh = new THREE.Mesh(geo, mat);
      const yPos = (f - 1) * verticalGap + 1.2;
      mesh.position.set(0, yPos, 0);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      (mesh as any).userData = { floorNumber: f, occRatio: occ, isEco };

      // Slab glass border/perimeter frame
      const wireGeo = new THREE.EdgesGeometry(geo);
      const wireMat = new THREE.LineBasicMaterial({ color: 0xffffff });
      const wireframe = new THREE.LineSegments(wireGeo, wireMat);
      mesh.add(wireframe);

      scene.add(mesh);
      floorMeshes.push(mesh);
    }

    // Raycaster
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handlePointerMove = (e: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(floorMeshes);

      if (hits.length > 0) {
        const hit = hits[0].object as THREE.Mesh;
        const d = (hit as any).userData;
        if (d) {
          setHoveredFloor({ floor: d.floorNumber, occ: d.occRatio });
          renderer.domElement.style.cursor = 'pointer';
          return;
        }
      }
      setHoveredFloor(null);
      renderer.domElement.style.cursor = 'default';
    };

    const dom = renderer.domElement;
    dom.addEventListener('pointermove', handlePointerMove);

    // Animation Loop
    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      controls.autoRotate = isRotating;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      dom.removeEventListener('pointermove', handlePointerMove);
      cancelAnimationFrame(animId);
      renderer.dispose();
    };
  }, [floorsCount, isRotating, getFloorOccupancy]);

  return (
    <div className="relative w-full h-[280px] bg-slate-50 rounded-xl overflow-hidden border border-gray-200">
      <div ref={containerRef} className="w-full h-full" />

      {/* Top Header Badge */}
      <div className="absolute top-2 left-3 flex items-center gap-2 pointer-events-none">
        <span className="text-[11px] font-bold text-gray-700 bg-white/90 backdrop-blur-xs px-2 py-0.5 rounded border border-gray-200 shadow-2xs">
          3D Kat Modeli
        </span>
      </div>

      {/* Rotate Toggle */}
      <div className="absolute top-2 right-2">
        <button
          onClick={() => setIsRotating(!isRotating)}
          className={`p-1.5 rounded-md text-xs font-medium transition border shadow-2xs ${isRotating ? 'bg-emerald-700 text-white border-emerald-800' : 'bg-white text-gray-700 border-gray-200'}`}
          title="Döndürmeyi Aç/Kapat"
        >
          <RotateCcw size={12} className={isRotating ? 'animate-spin' : ''} />
        </button>
      </div>

      {/* Hover Info Tag */}
      {hoveredFloor ? (
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 bg-gray-900/90 text-white px-3 py-1 rounded-full text-xs shadow-md backdrop-blur-xs border border-gray-700 flex items-center gap-2 pointer-events-none">
          <span className="font-bold">Kat {hoveredFloor.floor}:</span>
          <span className="font-semibold text-emerald-400">%{hoveredFloor.occ} Dolu</span>
        </div>
      ) : (
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[10px] text-gray-400 pointer-events-none">
          Katı incelemek için üzerine gelin veya sürükleyin
        </div>
      )}
    </div>
  );
}
