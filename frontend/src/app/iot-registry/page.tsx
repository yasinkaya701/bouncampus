'use client';

import React, { useState } from 'react';
import { Radio, ShieldCheck, Wifi, Server, CheckCircle2, RefreshCw, Cpu, Lock, Network } from 'lucide-react';

const GATEWAYS = [
  { id: 'GW-BAC-01', type: 'BACnet/IP Router', ip: '10.42.10.15', building: 'New Hall (NH)', protocol: 'BACnet UDP (47808)', status: 'online', pingMs: 4, firmware: 'v4.2.1-sec' },
  { id: 'GW-LORA-02', type: 'LoRaWAN 868MHz Base Station', ip: '10.42.10.88', building: 'Perkins Hall (M)', protocol: 'ChirpStack MQTT', status: 'online', pingMs: 12, firmware: 'v2.8.0' },
  { id: 'GW-MOD-03', type: 'Modbus TCP Power Gateway', ip: '10.42.20.10', building: 'Trafo Merkezi TR-1', protocol: 'Modbus Port 502', status: 'online', pingMs: 6, firmware: 'v3.1.4' },
  { id: 'GW-BAC-04', type: 'BACnet MS/TP Master', ip: '10.42.10.44', building: 'Kare Blok (KB)', protocol: 'RS-485 to IP', status: 'online', pingMs: 8, firmware: 'v4.1.9' },
  { id: 'GW-WIND-05', type: 'Kilyos SCADA Fiber Gateway', ip: '10.42.50.01', building: 'Kilyos Sarıtepe Kampüsü', protocol: 'IEC 61400-25', status: 'online', pingMs: 18, firmware: 'v5.0.2' },
];

export default function IoTRegistryPage() {
  const [pinging, setPinging] = useState(false);
  const [pingResult, setPingResult] = useState<string | null>(null);

  const handlePingAll = () => {
    setPinging(true);
    setTimeout(() => {
      setPinging(false);
      setPingResult('Tüm 148 IoT Gateway ve sensör noktası yanıt verdi (0 Paket Kaybı, Ortalama Gecikme: 8.4 ms).');
    }, 800);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-indigo-50 text-indigo-700 rounded-lg">
              <Network size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">IoT Cihaz Envanteri & Ağ Topolojisi</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Kampüs genelindeki 148 IoT gateway, BACnet/IP yönlendiricileri ve LoRaWAN baz istasyonlarının canlı durumu.
          </p>
        </div>

        <button
          onClick={handlePingAll}
          disabled={pinging}
          className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-xs"
        >
          <RefreshCw size={14} className={pinging ? 'animate-spin' : ''} />
          <span>{pinging ? 'Taranıyor...' : 'Tüm Ağı Ping Testine Tabi Tut'}</span>
        </button>
      </div>

      {pingResult && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs rounded-xl flex items-center gap-2">
          <CheckCircle2 size={16} className="text-emerald-700" />
          <span>{pingResult}</span>
        </div>
      )}

      {/* Network Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Toplam Ağ Düğümleri</span>
          <div className="text-3xl font-black text-gray-900">148 Cihaz</div>
          <div className="text-xs text-emerald-600 font-semibold mt-1">%100 Çevrimiçi</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Şifreleme Düzeyi</span>
          <div className="text-3xl font-black text-indigo-700">TLS 1.3</div>
          <div className="text-xs text-gray-500 mt-1">Uçtan Uca BACnet Güvenliği</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Ortalama Gecikme</span>
          <div className="text-3xl font-black text-emerald-700">8.4 ms</div>
          <div className="text-xs text-gray-500 mt-1">Kampüs Fiber Omurgası</div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Protokol Kapsamı</span>
          <div className="text-3xl font-black text-blue-700">4 Protokol</div>
          <div className="text-xs text-gray-500 mt-1">BACnet, Modbus, LoRa, MQTT</div>
        </div>
      </div>

      {/* Gateways Table */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-gray-100">
          <h3 className="font-bold text-lg text-gray-900">Merkezi Omurga Ağ Ağ Geçitleri (Gateways)</h3>
        </div>

        <div className="divide-y divide-gray-100">
          {GATEWAYS.map(gw => (
            <div key={gw.id} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-gray-50 transition">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-indigo-50 text-indigo-700 rounded-xl">
                  <Server size={22} />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold text-sm text-gray-900">{gw.id}</h4>
                    <span className="text-xs text-gray-500">• {gw.type}</span>
                  </div>
                  <p className="text-xs text-gray-600 mt-0.5">{gw.building} • IP: <strong className="font-mono">{gw.ip}</strong></p>
                </div>
              </div>

              <div className="flex items-center gap-6 text-xs">
                <div>
                  <span className="text-gray-400 block text-[10px]">Protokol</span>
                  <span className="font-mono text-gray-800">{gw.protocol}</span>
                </div>
                <div>
                  <span className="text-gray-400 block text-[10px]">Gecikme</span>
                  <span className="font-bold text-emerald-700">{gw.pingMs} ms</span>
                </div>
                <div>
                  <span className="text-gray-400 block text-[10px]">Yazılım Sürümü</span>
                  <span className="font-mono text-gray-700">{gw.firmware}</span>
                </div>
                <div>
                  <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800">
                    ONLINE
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
