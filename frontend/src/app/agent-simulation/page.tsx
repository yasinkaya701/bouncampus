'use client';

import React, { useRef, useEffect, useState } from 'react';
import { Play, Pause, RotateCcw, Users, Zap, FastForward, Activity, MapPin, Eye } from 'lucide-react';
import { initializeStudentPopulation, updateAgentPositions, StudentAgent, CAMPUS_NODES } from '@/lib/simulation-engine';

export default function AgentSimulationPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [speedMultiplier, setSpeedMultiplier] = useState(1);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [agentsCount, setAgentsCount] = useState(450);
  const [simHour, setSimHour] = useState(12);

  const agentsRef = useRef<StudentAgent[]>(initializeStudentPopulation(450));
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let lastTime = performance.now();

    const loop = (currentTime: number) => {
      const dt = (currentTime - lastTime) / 1000;
      lastTime = currentTime;

      if (isPlaying) {
        agentsRef.current = updateAgentPositions(agentsRef.current, simHour);
      }

      // 1. Clear background
      ctx.fillStyle = '#0f172a'; // slate-900
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // 2. Draw Campus Roads / Paths
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 14;
      ctx.lineCap = 'round';
      ctx.beginPath();
      // Kuzey amfiler to dining
      ctx.moveTo(180, 140);
      ctx.lineTo(200, 220);
      ctx.lineTo(270, 210);
      ctx.lineTo(220, 270);
      // North to South connection
      ctx.lineTo(360, 350);
      ctx.lineTo(500, 430);
      ctx.lineTo(550, 460);
      ctx.lineTo(610, 480);
      ctx.lineTo(630, 440);
      ctx.stroke();

      // 3. Draw Building Nodes
      Object.values(CAMPUS_NODES).forEach(node => {
        ctx.fillStyle = node.type === 'dining' ? '#ea580c' : node.type === 'academic' ? '#059669' : node.type === 'library' ? '#4f46e5' : '#0284c7';
        ctx.beginPath();
        ctx.arc(node.x, node.y, 16, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Label
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(node.name, node.x, node.y + 28);
      });

      // 4. Draw Student Agents
      agentsRef.current.forEach(agent => {
        ctx.fillStyle = agent.state === 'dining' ? '#fb923c' : agent.state === 'in_class' ? '#34d399' : '#38bdf8';
        ctx.beginPath();
        ctx.arc(agent.x, agent.y, 3, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameRef.current = requestAnimationFrame(loop);
    };

    animationFrameRef.current = requestAnimationFrame(loop);

    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };
  }, [isPlaying, simHour]);

  const inClassCount = agentsRef.current.filter(a => a.state === 'in_class').length;
  const inDiningCount = agentsRef.current.filter(a => a.state === 'dining').length;
  const inWalkingCount = agentsRef.current.filter(a => a.state === 'walking').length;

  const handleReset = () => {
    agentsRef.current = initializeStudentPopulation(agentsCount);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-indigo-50 text-indigo-700 rounded-lg">
              <Users size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Çoklu Ajanlı (ABM) İnsan Akış Simülasyonu</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Sosyal kuvvet modeli ve kuyruk fiziğiyle 450+ otonom öğrenci ajanının derslikler, yemekhaneler ve ring durakları arasındaki mikro-akışı.
          </p>
        </div>

        {/* Sim Controls */}
        <div className="flex items-center gap-2 bg-gray-100 p-1 rounded-xl">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="px-3 py-1.5 bg-white text-gray-900 font-bold rounded-lg text-xs shadow-xs flex items-center gap-1.5 hover:bg-gray-50"
          >
            {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            <span>{isPlaying ? 'Durdur' : 'Başlat'}</span>
          </button>
          <button
            onClick={handleReset}
            className="p-1.5 text-gray-600 hover:text-gray-900 rounded-lg text-xs transition"
            title="Sıfırla"
          >
            <RotateCcw size={14} />
          </button>
        </div>
      </div>

      {/* Population Counters */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
          <span className="text-[10px] font-bold text-gray-400 uppercase block">Toplam Ajan Nüfusu</span>
          <div className="text-2xl font-black text-gray-900">{agentsRef.current.length} Öğrenci</div>
          <div className="text-[11px] text-gray-500 mt-0.5">Sosyal Kuvvet Modeli Aktif</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
          <span className="text-[10px] font-bold text-gray-400 uppercase block">Amfilerdeki Öğrenci</span>
          <div className="text-2xl font-black text-emerald-700">{inClassCount}</div>
          <div className="text-[11px] text-gray-500 mt-0.5">Ders Saatinde</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
          <span className="text-[10px] font-bold text-gray-400 uppercase block">Yemekhanede Olan</span>
          <div className="text-2xl font-black text-orange-600">{inDiningCount}</div>
          <div className="text-[11px] text-gray-500 mt-0.5">Kuzey / Güney Yemekhane</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-xs">
          <span className="text-[10px] font-bold text-gray-400 uppercase block">Yolda Yürüyenler</span>
          <div className="text-2xl font-black text-blue-600">{inWalkingCount}</div>
          <div className="text-[11px] text-gray-500 mt-0.5">Kampüs İçi Göç Hali</div>
        </div>
      </div>

      {/* Micro-Simulation Canvas */}
      <div className="bg-slate-950 rounded-2xl p-4 border border-slate-800 shadow-2xl overflow-hidden relative">
        <canvas
          ref={canvasRef}
          width={800}
          height={560}
          className="w-full h-auto rounded-xl border border-slate-800"
        />

        {/* Live HUD Overlay */}
        <div className="absolute top-8 left-8 bg-slate-900/90 backdrop-blur-md px-3 py-2 rounded-xl border border-slate-700 text-white text-xs space-y-1">
          <div className="font-bold flex items-center gap-1.5 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            Canlı Ajan Tabanlı Mikro Motor
          </div>
          <div className="text-[10px] text-slate-400">
            Yeşil Noktalar: Amfi • Turuncu: Yemekhane • Mavi: Yol
          </div>
        </div>
      </div>
    </div>
  );
}
