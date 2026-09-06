'use client';

import React, { useState, useEffect } from 'react';
import Header from '@/components/shared/Header';
import { 
  Network, Server, Cpu, Database, Send, Radio, Terminal, 
  CheckCircle2, RefreshCw, Layers, ShieldCheck, Zap, Globe, 
  Key, ArrowRight, Activity, Copy, Check
} from 'lucide-react';

interface GatewayProtocol {
  id: string;
  name: string;
  protocol: 'BACnet/IP' | 'Modbus TCP' | 'MQTT' | 'LoRaWAN' | 'REST/Webhook';
  port: string;
  endpoint: string;
  connectedNodes: number;
  throughput: string;
  latency: string;
  status: 'ONLINE' | 'STANDBY' | 'SYNCING';
  lastHeartbeat: string;
  samplePayload: Record<string, any>;
}

const GATEWAY_PROTOCOLS: GatewayProtocol[] = [
  {
    id: 'GW-BACNET',
    name: 'BACnet/IP HVAC & Saha Gateway',
    protocol: 'BACnet/IP',
    port: 'UDP 47808',
    endpoint: 'bacnet://10.29.1.50:47808',
    connectedNodes: 86,
    throughput: '34.2 paket/sn',
    latency: '3.8 ms',
    status: 'ONLINE',
    lastHeartbeat: '0s önce',
    samplePayload: {
      device_id: 10482,
      object_type: 'analog-value',
      instance: 101,
      property: 'present-value',
      value: 22.4,
      units: 'degrees-celsius',
      status_flags: [false, false, false, false]
    }
  },
  {
    id: 'GW-MODBUS',
    name: 'Modbus TCP Enerji Analizörleri',
    protocol: 'Modbus TCP',
    port: 'TCP 502',
    endpoint: 'modbus://10.29.1.60:502',
    connectedNodes: 24,
    throughput: '18.5 sorgu/sn',
    latency: '5.2 ms',
    status: 'ONLINE',
    lastHeartbeat: '1s önce',
    samplePayload: {
      unit_id: 1,
      function_code: 3,
      start_register: 40001,
      registers: [230.4, 231.1, 229.8, 148.2, 0.98]
    }
  },
  {
    id: 'GW-MQTT',
    name: 'Boğaziçi MQTT Broker (Mosquitto)',
    protocol: 'MQTT',
    port: 'TCP 1883 / WSS 9001',
    endpoint: 'mqtt://broker.boun.edu.tr:1883',
    connectedNodes: 148,
    throughput: '142.0 msg/sn',
    latency: '2.1 ms',
    status: 'ONLINE',
    lastHeartbeat: '0s önce',
    samplePayload: {
      topic: 'boun/campus/south/tb/occupancy',
      timestamp: 1788739200,
      building: 'TB',
      room: 'Z-01',
      pir_count: 42,
      co2_ppm: 580
    }
  },
  {
    id: 'GW-LORAWAN',
    name: 'LoRaWAN Tarım & Çevre Ağ Geçidi',
    protocol: 'LoRaWAN',
    port: 'UDP 1700 (Semtech)',
    endpoint: 'lora://10.29.2.10:1700',
    connectedNodes: 18,
    throughput: '1.2 uplink/sn',
    latency: '38.0 ms',
    status: 'ONLINE',
    lastHeartbeat: '4s önce',
    samplePayload: {
      dev_eui: '70B3D57ED00492F1',
      frequency: 868.1,
      snr: 9.2,
      rssi: -84,
      payload_hex: '016700FA026842'
    }
  },
  {
    id: 'GW-WEBHOOK',
    name: 'OBIKAS & SKS Entegrasyon Webhook',
    protocol: 'REST/Webhook',
    port: 'HTTPS 443',
    endpoint: 'https://bouncampus.boun.edu.tr/api/v1/webhooks',
    connectedNodes: 6,
    throughput: '0.4 event/sn',
    latency: '14.0 ms',
    status: 'ONLINE',
    lastHeartbeat: '12s önce',
    samplePayload: {
      event: 'COURSE_SCHEDULE_UPDATED',
      semester: '2026-FALL',
      course: 'CMPE250.01',
      assigned_room: 'NH-101',
      enrolled_count: 142
    }
  }
];

export default function IntegrationsPage() {
  const [protocols] = useState<GatewayProtocol[]>(GATEWAY_PROTOCOLS);
  const [selectedProtocol, setSelectedProtocol] = useState<GatewayProtocol>(GATEWAY_PROTOCOLS[0]);
  const [packetStream, setPacketStream] = useState<string[]>([]);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Stream simulation
  useEffect(() => {
    const interval = setInterval(() => {
      const time = new Date().toTimeString().split(' ')[0];
      const randomGw = protocols[Math.floor(Math.random() * protocols.length)];
      const sample = JSON.stringify(randomGw.samplePayload);
      const line = `[${time}] [${randomGw.protocol}] ${randomGw.endpoint} -> RECV ${sample.slice(0, 75)}...`;
      setPacketStream(prev => [line, ...prev.slice(0, 15)]);
    }, 2800);

    return () => clearInterval(interval);
  }, [protocols]);

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 1800);
  };

  const handleInjectPacket = () => {
    const time = new Date().toTimeString().split(' ')[0];
    const line = `[${time}] [INJECT] ${selectedProtocol.protocol} <- TEST PACKET SENT TO ${selectedProtocol.endpoint} (ACK 200)`;
    setPacketStream(prev => [line, ...prev]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8 space-y-6">
        {/* Page Title */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 font-mono text-xs font-bold flex items-center gap-1.5 border border-cyan-500/30">
                <Network size={13} className="text-cyan-400" />
                ENTERPRISE GATEWAY v3.5
              </span>
              <span className="text-xs text-slate-400 font-mono">BMS & SCADA Protokol Köprüleri</span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
              Saha Protokol Entegrasyonları & Gateway
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              BACnet/IP, Modbus TCP, MQTT ve LoRaWAN endüstriyel ağlarının çift yönlü telemetri ve komut köprüsü.
            </p>
          </div>

          <button
            onClick={handleInjectPacket}
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition flex items-center gap-2 shadow-lg shadow-emerald-950/40"
          >
            <Send size={14} />
            <span>Test Paketi Gönder (Inject)</span>
          </button>
        </div>

        {/* Protocols Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {protocols.map(gw => {
            const isSelected = selectedProtocol.id === gw.id;
            return (
              <div
                key={gw.id}
                onClick={() => setSelectedProtocol(gw)}
                className={`rounded-2xl border p-5 transition cursor-pointer relative overflow-hidden backdrop-blur-md ${
                  isSelected 
                    ? 'bg-slate-900/90 border-cyan-500/80 shadow-xl shadow-cyan-950/30 ring-1 ring-cyan-500/40' 
                    : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/60'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider bg-cyan-950 text-cyan-300 border border-cyan-800/80">
                    {gw.protocol}
                  </span>
                  <span className="text-xs font-mono text-emerald-400 flex items-center gap-1 font-bold">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    {gw.status}
                  </span>
                </div>

                <h3 className="font-bold text-base text-white mb-1">{gw.name}</h3>
                <p className="text-xs font-mono text-slate-400 mb-4">{gw.endpoint}</p>

                <div className="grid grid-cols-3 gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-[11px] font-mono mb-4">
                  <div>
                    <span className="text-slate-500 text-[9px] block">Düğümler</span>
                    <span className="text-slate-200 font-bold">{gw.connectedNodes} Cihaz</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[9px] block">Veri Akışı</span>
                    <span className="text-cyan-300 font-bold">{gw.throughput}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[9px] block">Gecikme</span>
                    <span className="text-emerald-400 font-bold">{gw.latency}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-2 border-t border-slate-800">
                  <span>Port: {gw.port}</span>
                  <span>Son Nabız: {gw.lastHeartbeat}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom Section: Packet Inspector & Live Stream */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Selected Protocol JSON Payload Inspector */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
              <div>
                <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase">{selectedProtocol.protocol} Payload Şeması</span>
                <h3 className="text-sm font-bold text-white">{selectedProtocol.name}</h3>
              </div>
              <button
                onClick={() => copyToClipboard(JSON.stringify(selectedProtocol.samplePayload, null, 2), selectedProtocol.id)}
                className="text-xs text-slate-400 hover:text-white flex items-center gap-1 bg-slate-800 px-2.5 py-1 rounded-lg transition"
              >
                {copiedId === selectedProtocol.id ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                <span>{copiedId === selectedProtocol.id ? 'Kopyalandı' : 'JSON Kopyala'}</span>
              </button>
            </div>

            <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-emerald-400 overflow-x-auto leading-relaxed max-h-72">
              {JSON.stringify(selectedProtocol.samplePayload, null, 2)}
            </pre>
          </div>

          {/* Live Packet Sniffer Terminal */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col h-96">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
                <h3 className="text-sm font-bold text-white font-mono">Canlı Ağ Paket Dinleyici (Sniffer)</h3>
              </div>
              <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">Wireshark uyumlu</span>
            </div>

            <div className="flex-1 font-mono text-[11px] text-slate-300 overflow-y-auto space-y-1.5 pr-1 select-text">
              {packetStream.map((log, idx) => (
                <div 
                  key={idx} 
                  className={`p-1.5 rounded border leading-tight ${
                    log.includes('INJECT')
                      ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-200'
                      : 'bg-slate-950/60 border-slate-800/80 text-slate-300'
                  }`}
                >
                  {log}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
