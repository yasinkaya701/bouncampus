'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/shared/Header';
import { 
  AlertTriangle, ShieldAlert, CheckCircle2, RefreshCw, Zap, 
  Droplets, Flame, Cpu, Wrench, ArrowRight, Play, Check, 
  Clock, Activity, Filter, Radio
} from 'lucide-react';

interface Anomaly {
  id: string;
  timestamp: string;
  building: string;
  buildingCode: string;
  campus: 'Güney' | 'Kuzey' | 'Kilyos';
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  category: 'HVAC' | 'ELECTRICAL' | 'WATER' | 'IAQ' | 'SECURITY';
  title: string;
  description: string;
  metric: string;
  normalRange: string;
  currentValue: string;
  status: 'ACTIVE' | 'RESOLVING' | 'RESOLVED';
  suggestedAction: string;
}

const INITIAL_ANOMALIES: Anomaly[] = [
  {
    id: 'ANOM-2026-091',
    timestamp: '02:18:42',
    building: 'Natuk Birkan Binası',
    buildingCode: 'NB-K2',
    campus: 'Güney',
    severity: 'CRITICAL',
    category: 'WATER',
    title: 'Akustik Şebeke Basınç Düşüşü & Ani Debi Patlaması',
    description: 'Kat 2 laboratuvar sıhhi tesisat hattında debi 28.4 L/dk seviyesine fırladı, statik basınç 4.2 bardan 1.8 bara düştü. Boru patlağı riski tespit edildi.',
    metric: 'Su Akış Debisi',
    normalRange: '0 - 4.5 L/dk',
    currentValue: '28.4 L/dk (+531%)',
    status: 'ACTIVE',
    suggestedAction: 'Motorlu Selenoid Vana V-102 Kapatma Emri Gönder'
  },
  {
    id: 'ANOM-2026-092',
    timestamp: '02:05:11',
    building: 'Hamlin Hall',
    buildingCode: 'HH-Z01',
    campus: 'Güney',
    severity: 'WARNING',
    category: 'HVAC',
    title: 'Sıfır Dolulukta Sürekli VRF Isıtma Tüketimi',
    description: 'OBIKAS ders programında ve PIR varlık sensöründe %0 doluluk olmasına rağmen 4 adet VRF iç ünite 26°C ayarında 21.8 kW yük çekmeye devam ediyor.',
    metric: 'Aktif Güç Tüketimi',
    normalRange: '1.2 - 3.5 kW',
    currentValue: '21.8 kW (Fazla Yük)',
    status: 'ACTIVE',
    suggestedAction: 'BACnet Eco-Set Komutu ile Klimaları Standby Moduna Al'
  },
  {
    id: 'ANOM-2026-093',
    timestamp: '01:44:03',
    building: 'Kuzey Trafo Merkezi TR-1',
    buildingCode: 'TR1-B0',
    campus: 'Kuzey',
    severity: 'CRITICAL',
    category: 'ELECTRICAL',
    title: 'Reaktif Güç Sıçraması & Faz Açısı Bozulması (Cos φ)',
    description: 'TR-1 ana dağıtım panosunda 3. harmonik bozulması %8.2 seviyesine ulaştı. Güç faktörü 0.74 seviyesine gerileyerek reaktif ceza eşiğine girdi.',
    metric: 'Güç Faktörü (Cos φ)',
    normalRange: '0.95 - 1.00',
    currentValue: '0.74 (Kritik Düşüş)',
    status: 'ACTIVE',
    suggestedAction: 'Dinamik SVC Kompanzasyon Kademe 4 Devreye Al'
  },
  {
    id: 'ANOM-2026-094',
    timestamp: '01:12:55',
    building: 'Aptullah Kuran Kütüphanesi',
    buildingCode: 'LIB-K3',
    campus: 'Kuzey',
    severity: 'WARNING',
    category: 'IAQ',
    title: '3. Kat Sessiz Çalışma CO₂ Seviyesi Eşik Aşımı',
    description: 'Gece vaktinde havalandırma taze hava damper servomotorunun kapalı kalması sonucu CO₂ konsantrasyonu 1.480 ppm seviyesine ulaştı.',
    metric: 'Hava Kalitesi CO₂',
    normalRange: '400 - 800 ppm',
    currentValue: '1.480 ppm (Havasız)',
    status: 'ACTIVE',
    suggestedAction: 'AHU-3 Taze Hava Damperi Açıklığını %85 Seviyesine Zorla'
  },
  {
    id: 'ANOM-2026-095',
    timestamp: '00:32:10',
    building: 'Kilyos Rüzgar Türbini',
    buildingCode: 'KLY-WT1',
    campus: 'Kilyos',
    severity: 'INFO',
    category: 'HVAC',
    title: 'Sapma (Yaw) Mekanizması Yatak Sıcaklığı Yükselmesi',
    description: '18.2 m/s poyraz fırtınası esnasında rüzgar yönüne hizalanma sağlayan sapma dişli kutusu sıcaklığı 78.4°C seviyesine ulaştı.',
    metric: 'Yatak Sıcaklığı',
    normalRange: '< 65°C',
    currentValue: '78.4°C (+20%)',
    status: 'ACTIVE',
    suggestedAction: 'Ekstra Yağlama Döngüsü Başlat & Yaw Hızını Kısıtla'
  }
];

export default function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>(INITIAL_ANOMALIES);
  const [filterSeverity, setFilterSeverity] = useState<'ALL' | 'CRITICAL' | 'WARNING'>('ALL');
  const [actionFeed, setActionFeed] = useState<string[]>([]);
  const [autoScanActive, setAutoScanActive] = useState(true);

  // Auto-scan telemetry simulation
  useEffect(() => {
    if (!autoScanActive) return;
    const interval = setInterval(() => {
      const timeStr = new Date().toTimeString().split(' ')[0];
      const logs = [
        `[${timeStr}] SCADA Modbus Gateway poll: 148 IoT düğüm taranıyor... 0 paket kaybı`,
        `[${timeStr}] XGBoost Rezidüel Model: 21 bina enerji tahmin sapmaları ±%2.4 tolerans içinde`,
        `[${timeStr}] Bebek Su Basınç Hattı Telemetrisi: 4.1 bar stabil`
      ];
      const randomLog = logs[Math.floor(Math.random() * logs.length)];
      setActionFeed(prev => [randomLog, ...prev.slice(0, 15)]);
    }, 4500);

    return () => clearInterval(interval);
  }, [autoScanActive]);

  const handleResolve = (id: string, actionText: string) => {
    setAnomalies(prev => prev.map(a => {
      if (a.id === id) {
        return { ...a, status: 'RESOLVING' };
      }
      return a;
    }));

    const timeStr = new Date().toTimeString().split(' ')[0];
    setActionFeed(prev => [
      `[${timeStr}] ⚡ OTONOM MÜDAHALE: ${actionText} komutu BACnet/IP üzerinden sahaya iletildi.`,
      ...prev
    ]);

    setTimeout(() => {
      setAnomalies(prev => prev.map(a => {
        if (a.id === id) {
          return { ...a, status: 'RESOLVED' };
        }
        return a;
      }));
      const resolveTime = new Date().toTimeString().split(' ')[0];
      setActionFeed(prev => [
        `[${resolveTime}] ✅ BAŞARILI: ${id} nolu anomali normale döndü. Saha onaylandı.`,
        ...prev
      ]);
    }, 1800);
  };

  const filtered = anomalies.filter(a => {
    if (filterSeverity === 'ALL') return true;
    return a.severity === filterSeverity;
  });

  const activeCriticalCount = anomalies.filter(a => a.severity === 'CRITICAL' && a.status === 'ACTIVE').length;
  const activeWarningCount = anomalies.filter(a => a.severity === 'WARNING' && a.status === 'ACTIVE').length;
  const resolvedCount = anomalies.filter(a => a.status === 'RESOLVED').length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8 space-y-6">
        {/* Page Title & Status Banner */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-mono text-xs font-bold flex items-center gap-1.5 border border-rose-500/30">
                <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                AI ANOMALY RADAR v4.2
              </span>
              <span className="text-xs text-slate-400 font-mono">Isolation Forest & ResNet Autoencoder</span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
              Otonom Anomali & Olay Müdahale Merkezi
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              21 Boğaziçi binasında 4.200 sensörden gelen su, elektrik, HVAC ve iç hava kalitesi anormalliklerini milisaniyeler içinde teşhis ve izole eder.
            </p>
          </div>

          {/* Quick Metrics Cards */}
          <div className="flex items-center gap-3">
            <div className="bg-rose-950/40 border border-rose-800/60 px-4 py-2.5 rounded-xl text-center">
              <span className="text-[10px] text-rose-300 font-bold uppercase block">Kritik Anomali</span>
              <span className="text-2xl font-black text-rose-400">{activeCriticalCount}</span>
            </div>
            <div className="bg-amber-950/40 border border-amber-800/60 px-4 py-2.5 rounded-xl text-center">
              <span className="text-[10px] text-amber-300 font-bold uppercase block">Uyarı Eşiği</span>
              <span className="text-2xl font-black text-amber-400">{activeWarningCount}</span>
            </div>
            <div className="bg-emerald-950/40 border border-emerald-800/60 px-4 py-2.5 rounded-xl text-center">
              <span className="text-[10px] text-emerald-300 font-bold uppercase block">Çözülen</span>
              <span className="text-2xl font-black text-emerald-400">{resolvedCount}</span>
            </div>
          </div>
        </div>

        {/* Action Controls & Filters */}
        <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/80 p-3 rounded-xl border border-slate-800">
          <div className="flex items-center gap-2">
            <Filter size={14} className="text-slate-400" />
            <span className="text-xs font-semibold text-slate-300">Filtrele:</span>
            <button
              onClick={() => setFilterSeverity('ALL')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterSeverity === 'ALL' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Tümü ({anomalies.length})
            </button>
            <button
              onClick={() => setFilterSeverity('CRITICAL')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterSeverity === 'CRITICAL' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Kritikler ({anomalies.filter(a => a.severity === 'CRITICAL').length})
            </button>
            <button
              onClick={() => setFilterSeverity('WARNING')}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${filterSeverity === 'WARNING' ? 'bg-amber-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Uyarılar ({anomalies.filter(a => a.severity === 'WARNING').length})
            </button>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={() => setAutoScanActive(!autoScanActive)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-lg border font-semibold transition ${autoScanActive ? 'bg-emerald-950/60 border-emerald-500/50 text-emerald-300' : 'bg-slate-800 border-slate-700 text-slate-400'}`}
            >
              <Radio size={13} className={autoScanActive ? 'animate-pulse text-emerald-400' : ''} />
              <span>{autoScanActive ? 'Canlı Telemetri Taraması Aktif' : 'Tarama Duraklatıldı'}</span>
            </button>
          </div>
        </div>

        {/* Main 2-Column Grid: Anomalies List & Live Terminal */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Anomalies Cards (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            {filtered.map(item => (
              <div 
                key={item.id}
                className={`rounded-2xl border p-5 transition relative overflow-hidden backdrop-blur-md ${
                  item.status === 'RESOLVED'
                    ? 'bg-slate-900/40 border-slate-800/80 opacity-75'
                    : item.severity === 'CRITICAL'
                    ? 'bg-rose-950/20 border-rose-800/60 hover:border-rose-600 shadow-lg shadow-rose-950/20'
                    : 'bg-amber-950/20 border-amber-800/60 hover:border-amber-600 shadow-lg shadow-amber-950/20'
                }`}
              >
                {/* Header Row */}
                <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${
                      item.severity === 'CRITICAL' ? 'bg-rose-500 text-white' : 'bg-amber-500 text-black'
                    }`}>
                      {item.severity}
                    </span>
                    <span className="text-xs font-mono text-slate-400 font-bold">{item.id}</span>
                    <span className="text-xs text-slate-500">•</span>
                    <span className="text-xs font-semibold text-slate-300">{item.building} ({item.buildingCode})</span>
                    <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded-md font-mono">{item.campus} Kampüs</span>
                  </div>

                  <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                    <Clock size={12} /> {item.timestamp}
                  </span>
                </div>

                {/* Body Content */}
                <h3 className="text-base font-bold text-white mb-1.5 flex items-center gap-2">
                  {item.category === 'WATER' && <Droplets size={16} className="text-cyan-400" />}
                  {item.category === 'HVAC' && <Flame size={16} className="text-amber-400" />}
                  {item.category === 'ELECTRICAL' && <Zap size={16} className="text-yellow-400" />}
                  {item.category === 'IAQ' && <Activity size={16} className="text-emerald-400" />}
                  {item.title}
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed mb-4">
                  {item.description}
                </p>

                {/* Metric Comparisons */}
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 bg-slate-900/80 p-3 rounded-xl border border-slate-800 mb-4 text-xs font-mono">
                  <div>
                    <span className="text-slate-500 text-[10px] block">İzlenen Parametre</span>
                    <span className="text-slate-200 font-bold">{item.metric}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] block">Beklenen Normal Aralık</span>
                    <span className="text-emerald-400 font-bold">{item.normalRange}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] block">Okunan Anormal Değer</span>
                    <span className={`font-bold ${item.severity === 'CRITICAL' ? 'text-rose-400' : 'text-amber-400'}`}>
                      {item.currentValue}
                    </span>
                  </div>
                </div>

                {/* Action Footer */}
                <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/80">
                  <div className="text-xs text-slate-300 flex items-center gap-1.5">
                    <Wrench size={13} className="text-indigo-400" />
                    <span>Öneri: <strong className="text-indigo-300">{item.suggestedAction}</strong></span>
                  </div>

                  <div>
                    {item.status === 'RESOLVED' ? (
                      <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 bg-emerald-950/60 px-3 py-1.5 rounded-xl border border-emerald-600/40">
                        <CheckCircle2 size={14} /> Çözüldü & Kapatıldı
                      </span>
                    ) : item.status === 'RESOLVING' ? (
                      <span className="flex items-center gap-1.5 text-xs font-bold text-amber-300 bg-amber-950/60 px-3 py-1.5 rounded-xl border border-amber-600/40">
                        <RefreshCw size={14} className="animate-spin" /> BACnet Komutu İletiliyor...
                      </span>
                    ) : (
                      <button
                        onClick={() => handleResolve(item.id, item.suggestedAction)}
                        className="bg-gradient-to-r from-rose-600 to-indigo-600 hover:from-rose-500 hover:to-indigo-500 text-white text-xs font-bold px-4 py-2 rounded-xl transition shadow-md flex items-center gap-1.5"
                      >
                        <Zap size={14} />
                        <span>Otonom Müdahale Uygula</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Right Column: Live Terminal & Incident Feed */}
          <div className="space-y-4">
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col h-[580px]">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  <h3 className="font-bold text-sm text-white font-mono">SCADA Gateway Terminali</h3>
                </div>
                <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">TCP 47808</span>
              </div>

              <div className="flex-1 font-mono text-[11px] text-slate-300 overflow-y-auto space-y-2 pr-1 select-text">
                <p className="text-slate-500">{'// Boğaziçi SCADA BACnet/IP ve Modbus olay akışı:'}</p>
                {actionFeed.length === 0 && (
                  <p className="text-slate-600 italic">Telemetri dinleniyor...</p>
                )}
                {actionFeed.map((log, idx) => (
                  <div 
                    key={idx} 
                    className={`p-2 rounded-lg border leading-relaxed ${
                      log.includes('OTONOM')
                        ? 'bg-indigo-950/60 border-indigo-500/40 text-indigo-200'
                        : log.includes('BAŞARILI')
                        ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-200'
                        : 'bg-slate-950/60 border-slate-800/80 text-slate-300'
                    }`}
                  >
                    {log}
                  </div>
                ))}
              </div>

              <div className="pt-3 border-t border-slate-800 mt-2 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                <span>Buffer: 100 log</span>
                <span>Gecikme: 4ms (Boğaziçi LAN)</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
