'use client';

import React, { useState } from 'react';
import { Wrench, AlertTriangle, CheckCircle2, Activity, Cpu, Wind, ShieldAlert, Clock, ArrowRight, Gauge } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const FFT_VIBRATION_SPECTRUM = [
  { freqHz: 50, Amplitud: 0.12, Baslik: 'Şebeke Frekansı' },
  { freqHz: 100, Amplitud: 0.08, Baslik: '2x Şebeke' },
  { freqHz: 180, Amplitud: 0.35, Baslik: 'Rotor Dengesizliği' },
  { freqHz: 240, Amplitud: 0.15, Baslik: '' },
  { freqHz: 360, Amplitud: 0.88, Baslik: 'BPFO Rulman Dış Bilezik Hatası' }, // Fault peak!
  { freqHz: 480, Amplitud: 0.22, Baslik: '' },
  { freqHz: 720, Amplitud: 0.54, Baslik: '2x BPFO Harmoniği' },
  { freqHz: 960, Amplitud: 0.18, Baslik: '' },
  { freqHz: 1200, Amplitud: 0.09, Baslik: '' },
  { freqHz: 1500, Amplitud: 0.05, Baslik: '' },
];

const ASSETS = [
  { id: 'AST-CHILL-01', name: 'Merkezi Soğutma Grubu (Chiller-1)', location: 'New Hall Kazan Dairesi', healthScore: 92, rulDays: 180, vibrationRms: '1.4 mm/s', status: 'optimal' },
  { id: 'AST-AHU-02', name: 'AHU-02 Besleme Fan Motoru', location: 'Perkins Hall Çatı Santrali', healthScore: 68, rulDays: 24, vibrationRms: '4.8 mm/s', status: 'warning' },
  { id: 'AST-WIND-01', name: 'Kilyos RES Enercon Dişli Kutusu', location: 'Kilyos Sarıtepe Kampüsü', healthScore: 89, rulDays: 145, vibrationRms: '2.1 mm/s', status: 'optimal' },
  { id: 'AST-PUMP-03', name: 'Kuzey Isıtma Sirkülasyon Pompası', location: 'Kare Blok Bodrum Katı', healthScore: 54, rulDays: 12, vibrationRms: '6.2 mm/s', status: 'critical' },
];

export default function PredictiveMaintenancePage() {
  const [selectedAsset, setSelectedAsset] = useState(ASSETS[1]);
  const [workOrderCreated, setWorkOrderCreated] = useState(false);

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-amber-50 text-amber-700 rounded-lg">
              <Wrench size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Kestirimci Bakım & HVAC Titreşim AI</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            FFT spektrum analizi, rulman arıza frekansları (BPFO/BPFI) ve kalan faydalı ömür (RUL) tahmini.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-800">
          <ShieldAlert size={15} className="text-emerald-600" />
          <span>ISO 13373-1 Titreşim İzleme Uyumlu</span>
        </div>
      </div>

      {/* 4 Asset KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {ASSETS.map(asset => (
          <div
            key={asset.id}
            onClick={() => setSelectedAsset(asset)}
            className={`cursor-pointer rounded-2xl p-5 border transition-all ${
              selectedAsset.id === asset.id
                ? 'bg-emerald-50/50 border-emerald-500 shadow-md ring-2 ring-emerald-500/20'
                : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-xs'
            }`}
          >
            <div className="flex items-start justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-gray-400">{asset.id}</span>
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                  asset.status === 'optimal'
                    ? 'bg-emerald-100 text-emerald-800'
                    : asset.status === 'warning'
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-rose-100 text-rose-800 animate-pulse'
                }`}
              >
                {asset.status.toUpperCase()}
              </span>
            </div>
            <h3 className="font-bold text-sm text-gray-900 line-clamp-1">{asset.name}</h3>
            <p className="text-[11px] text-gray-500 mb-3">{asset.location}</p>

            <div className="space-y-1.5 text-xs pt-2 border-t border-gray-100">
              <div className="flex justify-between">
                <span className="text-gray-500">Sağlık Skoru:</span>
                <span className="font-bold text-gray-900">%{asset.healthScore}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Kalan Ömür (RUL):</span>
                <span className="font-bold text-emerald-700">{asset.rulDays} Gün</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Titreşim RMS:</span>
                <span className="font-bold text-gray-800">{asset.vibrationRms}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Selected Asset Detailed Diagnostics */}
      <div className="bg-slate-950 text-white rounded-2xl p-6 border border-slate-800 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <span className="text-xs text-amber-400 font-mono font-bold">CANLI FFT TİTREŞİM ANALİZÖRÜ</span>
            <h3 className="font-bold text-xl text-white">{selectedAsset.name}</h3>
            <p className="text-xs text-slate-400">{selectedAsset.location} • 3-Eksenli İvmeölçer Sensörü</p>
          </div>

          <button
            onClick={() => setWorkOrderCreated(true)}
            disabled={workOrderCreated}
            className={`px-5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
              workOrderCreated
                ? 'bg-emerald-600 text-white'
                : 'bg-amber-500 hover:bg-amber-600 text-slate-950 shadow-md'
            }`}
          >
            <Wrench size={15} />
            <span>{workOrderCreated ? 'İş Emri Açıldı (Mekanik Atölye #881)' : 'Mekanik İş Emri Oluştur'}</span>
          </button>
        </div>

        {/* FFT Frequency Spectrum Chart */}
        <div>
          <div className="flex items-center justify-between mb-3 text-xs">
            <span className="text-slate-300 font-semibold">Frekans Spektrumu (0 - 1500 Hz)</span>
            <span className="text-rose-400 font-bold flex items-center gap-1">
              <AlertTriangle size={13} /> 360 Hz: Rulman Dış Bilezik (BPFO) Pik Değeri Tespit Edildi
            </span>
          </div>

          <div className="h-64 w-full bg-slate-900 rounded-xl p-2 border border-slate-800">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={FFT_VIBRATION_SPECTRUM} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="freqHz" tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={v => `${v} Hz`} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(val: any) => [`${val} g`, 'Genlik']}
                  labelFormatter={l => `${l} Hz`}
                />
                <Line type="monotone" dataKey="Amplitud" stroke="#f59e0b" strokeWidth={2.5} dot={{ fill: '#f59e0b', r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Diagnosis & Recommendations */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[11px] text-slate-400 block">Arıza Teşhisi:</span>
            <div className="font-bold text-amber-400 text-sm">Rulman Aşınması (BPFO)</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Fan motorunun tahrik tarafı rulmanında mikro çatlak oluşumu gözlemlendi.
            </p>
          </div>

          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[11px] text-slate-400 block">Kalan Güvenli Çalışma:</span>
            <div className="font-bold text-emerald-400 text-sm">{selectedAsset.rulDays} Gün</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Planlı amfi boşluğunda (hafta sonu) rulman değişimi yapılması önerilir.
            </p>
          </div>

          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[11px] text-slate-400 block">Önlenen Duruş Maliyeti:</span>
            <div className="font-bold text-sky-400 text-sm">₺48,500</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Ani motor yanması ve ders iptali durumundaki tahmini operasyonel kayıp.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
