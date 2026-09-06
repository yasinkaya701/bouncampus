'use client';

import React, { useState, useEffect, useRef } from 'react';
import Header from '@/components/shared/Header';
import { 
  Volume2, VolumeX, Mic, Activity, Headphones, AlertCircle, 
  MapPin, Radio, Sparkles, Sliders, ShieldCheck, Play, Pause
} from 'lucide-react';

interface SoundZone {
  id: string;
  name: string;
  campus: 'Güney' | 'Kuzey';
  building: string;
  type: 'LIBRARY' | 'CLASSROOM' | 'OUTDOOR' | 'DINING' | 'TRANSIT';
  currentDb: number;
  thresholdDb: number;
  status: 'OPTIMAL' | 'MODERATE' | 'NOISY';
  frequencyFocus: string;
  soundType: 'library' | 'nature' | 'cafeteria' | 'classroom';
  description: string;
}

const SOUND_ZONES: SoundZone[] = [
  {
    id: 'ZONE-LIB-3',
    name: 'Aptullah Kuran Kütüphanesi 3. Kat',
    campus: 'Kuzey',
    building: 'LIB',
    type: 'LIBRARY',
    currentDb: 34.2,
    thresholdDb: 40.0,
    status: 'OPTIMAL',
    frequencyFocus: '120 - 450 Hz (Fısıltı & Sayfa Çevirme)',
    soundType: 'library',
    description: 'Yüksek odaklanma gerektiren derin çalışma alanı. WHO kütüphane standardının 5.8 dB altında mükemmel sessizlik.'
  },
  {
    id: 'ZONE-KB-101',
    name: 'Kare Blok Amfi 101',
    campus: 'Kuzey',
    building: 'KB',
    type: 'CLASSROOM',
    currentDb: 64.8,
    thresholdDb: 70.0,
    status: 'MODERATE',
    frequencyFocus: '500 - 2200 Hz (İnsan Konuşması)',
    soundType: 'classroom',
    description: 'Aktif ders ve tartışma oturumu devam ediyor. Akustik yankılanma süresi (RT60) 0.85s ile konuşma netliği dengeli.'
  },
  {
    id: 'ZONE-ALH-SQR',
    name: 'Albert Long Hall Önü & Tarihi Meydan',
    campus: 'Güney',
    building: 'ALH',
    type: 'OUTDOOR',
    currentDb: 52.4,
    thresholdDb: 65.0,
    status: 'OPTIMAL',
    frequencyFocus: '800 - 4000 Hz (Kuş Sesi & Boğaz Rüzgarı)',
    soundType: 'nature',
    description: 'Açık hava çimler ve Boğaz esintisi. Doğal ses ortamı mental dinginlik indeksi %94 seviyesinde.'
  },
  {
    id: 'ZONE-KY-PIR',
    name: 'Kuzey Piramit Kafeterya',
    campus: 'Kuzey',
    building: 'KY',
    type: 'DINING',
    currentDb: 74.8,
    thresholdDb: 72.0,
    status: 'NOISY',
    frequencyFocus: '250 - 3500 Hz (Çatal Kaşık & Kalabalık)',
    soundType: 'cafeteria',
    description: 'Öğle saatleri yoğunluğu nedeniyle gürültü eşiği 2.8 dB aşıldı. Akustik tavan panelleri ses emilim modunda devrede.'
  },
  {
    id: 'ZONE-BEBEK-GATE',
    name: 'Güney Bebek Giriş Güvenlik & Ring Durağı',
    campus: 'Güney',
    building: 'BEBEK',
    type: 'TRANSIT',
    currentDb: 69.2,
    thresholdDb: 75.0,
    status: 'MODERATE',
    frequencyFocus: '60 - 500 Hz (Dizel/Elektrik Motor Sesi)',
    soundType: 'classroom',
    description: 'Bebek yokuşunu tırmanan EV ring araçları ve yolcu iniş-biniş telemetrisi.'
  }
];

export default function AcousticNoisePage() {
  const [zones, setZones] = useState<SoundZone[]>(SOUND_ZONES);
  const [selectedZone, setSelectedZone] = useState<SoundZone>(SOUND_ZONES[0]);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Web Audio API references
  const audioCtxRef = useRef<AudioContext | null>(null);
  const oscillatorRef = useRef<OscillatorNode | null>(null);
  const gainNodeRef = useRef<GainNode | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  // Start / Stop Web Audio Synthesizer
  const toggleSoundscape = (zone: SoundZone) => {
    setSelectedZone(zone);

    if (isPlayingAudio && selectedZone.id === zone.id) {
      stopAudio();
      return;
    }

    startAudio(zone.soundType);
  };

  const startAudio = (type: 'library' | 'nature' | 'cafeteria' | 'classroom') => {
    stopAudio();

    try {
      const AudioCtxClass = window.AudioContext || (window as any).webkitAudioContext;
      const ctx = new AudioCtxClass();
      audioCtxRef.current = ctx;

      const analyser = ctx.createAnalyser();
      analyser.fftSize = 64;
      analyserRef.current = analyser;

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gainNodeRef.current = gain;

      // Synthesize ambient tone based on zone type
      const osc = ctx.createOscillator();
      if (type === 'library') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(140, ctx.currentTime); // calm low hum
      } else if (type === 'nature') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(320, ctx.currentTime); // gentle breeze tone
      } else if (type === 'cafeteria') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, ctx.currentTime); // crowd murmur base
      } else {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(180, ctx.currentTime);
      }

      osc.connect(gain);
      gain.connect(analyser);
      analyser.connect(ctx.destination);

      osc.start();
      oscillatorRef.current = osc;
      setIsPlayingAudio(true);

      startVisualizer();
    } catch (e) {
      console.error('AudioContext error', e);
    }
  };

  const stopAudio = () => {
    if (oscillatorRef.current) {
      try {
        oscillatorRef.current.stop();
        oscillatorRef.current.disconnect();
      } catch (e) {}
      oscillatorRef.current = null;
    }
    if (audioCtxRef.current) {
      try {
        audioCtxRef.current.close();
      } catch (e) {}
      audioCtxRef.current = null;
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    setIsPlayingAudio(false);
  };

  const startVisualizer = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const renderFrame = () => {
      animationFrameRef.current = requestAnimationFrame(renderFrame);
      const analyser = analyserRef.current;
      if (!analyser) return;

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      analyser.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const barWidth = (canvas.width / bufferLength) * 1.5;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height * 0.85 + 4;

        // Gradient color based on intensity
        const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
        gradient.addColorStop(0, '#059669');
        gradient.addColorStop(0.6, '#10b981');
        gradient.addColorStop(1, '#6ee7b7');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight);

        x += barWidth;
      }
    };

    renderFrame();
  };

  useEffect(() => {
    return () => {
      stopAudio();
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8 space-y-6">
        {/* Title Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded-full bg-teal-500/20 text-teal-400 font-mono text-xs font-bold flex items-center gap-1.5 border border-teal-500/30">
                <Volume2 size={13} className="text-teal-400" />
                AKUSTİK RADAR v2.8
              </span>
              <span className="text-xs text-slate-400 font-mono">24/7 Gürültü ve Desibel Haritalandırması</span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
              Boğaziçi Kampüs Akustik & Gürültü Haritası
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Kütüphane sessiz katları, amfiler, meydan ve kafeteryalardaki desibel (dB) seviyelerini canlı izler; çalışma konforunu korur.
            </p>
          </div>

          {/* Audio Synthesizer Status Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-3.5 flex items-center gap-4 shadow-xl">
            <div className="w-28 h-12 bg-slate-950 rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center p-1">
              <canvas ref={canvasRef} width={112} height={48} className="w-full h-full" />
            </div>
            <div>
              <span className="text-[10px] text-slate-400 font-mono block">Sanal Ortam Dinleme</span>
              <span className="text-xs font-bold text-white flex items-center gap-1.5">
                {isPlayingAudio ? (
                  <>
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span className="text-emerald-400">{selectedZone.name.split(' ')[0]} Dinleniyor</span>
                  </>
                ) : (
                  <span className="text-slate-500">Ses Kapalı</span>
                )}
              </span>
            </div>
          </div>
        </div>

        {/* Zones Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {zones.map(zone => {
            const isSelected = selectedZone.id === zone.id;
            const isPlayingThis = isPlayingAudio && isSelected;
            const dbPercent = Math.min(100, Math.round((zone.currentDb / 90) * 100));

            return (
              <div
                key={zone.id}
                onClick={() => setSelectedZone(zone)}
                className={`rounded-2xl border p-5 transition cursor-pointer relative overflow-hidden backdrop-blur-md ${
                  isSelected 
                    ? 'bg-slate-900/90 border-emerald-500/80 shadow-xl shadow-emerald-950/30 ring-1 ring-emerald-500/40' 
                    : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/60'
                }`}
              >
                {/* Status Bar */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${
                      zone.status === 'OPTIMAL' ? 'bg-emerald-400' : zone.status === 'MODERATE' ? 'bg-amber-400' : 'bg-rose-500 animate-pulse'
                    }`}></span>
                    <span className="text-[10px] font-bold text-slate-400 font-mono uppercase">{zone.campus} Kampüs • {zone.building}</span>
                  </div>

                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${
                    zone.status === 'OPTIMAL' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : zone.status === 'MODERATE' ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-rose-950 text-rose-300 border border-rose-800'
                  }`}>
                    {zone.status === 'OPTIMAL' ? 'İdeal Sessiz' : zone.status === 'MODERATE' ? 'Orta Düzey' : 'Eşik Aşımı'}
                  </span>
                </div>

                <h3 className="font-bold text-base text-white mb-2">{zone.name}</h3>
                <p className="text-xs text-slate-400 mb-4 line-clamp-2">{zone.description}</p>

                {/* Gauge Row */}
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 mb-4">
                  <div className="flex items-end justify-between mb-1.5">
                    <span className="text-[10px] text-slate-500 font-mono">Ses Basınç Seviyesi</span>
                    <span className="text-xl font-black text-white font-mono">
                      {zone.currentDb.toFixed(1)} <span className="text-xs text-slate-400 font-sans font-normal">dB(A)</span>
                    </span>
                  </div>
                  {/* Progress Bar */}
                  <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-500 rounded-full ${
                        zone.currentDb < 45 ? 'bg-emerald-500' : zone.currentDb < 70 ? 'bg-amber-500' : 'bg-rose-500'
                      }`}
                      style={{ width: `${dbPercent}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-[9px] text-slate-500 font-mono mt-1">
                    <span>Eşik: {zone.thresholdDb} dB(A)</span>
                    <span>Spektrum: {zone.frequencyFocus.split(' ')[0]}</span>
                  </div>
                </div>

                {/* Audio Listen Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleSoundscape(zone);
                  }}
                  className={`w-full py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 shadow-xs ${
                    isPlayingThis 
                      ? 'bg-rose-600 hover:bg-rose-700 text-white' 
                      : 'bg-emerald-800/80 hover:bg-emerald-700 text-white'
                  }`}
                >
                  {isPlayingThis ? (
                    <>
                      <Pause size={14} />
                      <span>Sesi Kapat</span>
                    </>
                  ) : (
                    <>
                      <Headphones size={14} />
                      <span>Ortamı Dinle (Sentez)</span>
                    </>
                  )}
                </button>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}
