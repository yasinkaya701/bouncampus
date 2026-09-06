'use client';

import React, { useState, useEffect } from 'react';
import { 
  Activity, Radio, Sliders, AlertTriangle, CheckCircle, ShieldAlert, Cpu, 
  Wind, Thermometer, Droplets, Zap, Fan, Eye, Power, RefreshCcw, BellRing, Settings2, Gauge
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

interface SensorTelemetry {
  id: string;
  tag: string;
  building: string;
  floor: number;
  location: string;
  tempC: number;
  humidityPct: number;
  co2Ppm: number;
  lux: number;
  occupancy: number;
  status: 'normal' | 'warning' | 'critical';
}

interface AHUUnit {
  id: string;
  name: string;
  building: string;
  supplyAirTempC: number;
  returnAirTempC: number;
  setpointC: number;
  fanSpeedPct: number;
  coolingCoilPct: number;
  heatingCoilPct: number;
  filterPressurePa: number;
  airFlowCfm: number;
  mode: 'eco_cooling' | 'standard' | 'night_setback';
}

const INITIAL_SENSORS: SensorTelemetry[] = [
  { id: 'SEN-NH-101', tag: 'TEMP_CO2_01', building: 'New Hall (NH)', floor: 1, location: 'NH 101 Büyük Amfi', tempC: 22.4, humidityPct: 48, co2Ppm: 680, lux: 450, occupancy: 124, status: 'normal' },
  { id: 'SEN-NH-401', tag: 'TEMP_CO2_02', building: 'New Hall (NH)', floor: 4, location: 'NH 401 Seminer', tempC: 25.8, humidityPct: 56, co2Ppm: 1120, lux: 380, occupancy: 42, status: 'warning' },
  { id: 'SEN-KB-001', tag: 'TEMP_CO2_03', building: 'Kare Blok (KB)', floor: 1, location: 'KB 001 Konferans', tempC: 21.8, humidityPct: 45, co2Ppm: 540, lux: 520, occupancy: 95, status: 'normal' },
  { id: 'SEN-M-1100', tag: 'TEMP_CO2_04', building: 'Perkins Hall (M)', floor: 1, location: 'M 1100 Makine Amfisi', tempC: 23.1, humidityPct: 51, co2Ppm: 810, lux: 410, occupancy: 140, status: 'normal' },
  { id: 'SEN-TB-410', tag: 'TEMP_CO2_05', building: 'Anderson Hall (TB)', floor: 4, location: 'TB 410 Çatı Katı', tempC: 26.9, humidityPct: 62, co2Ppm: 1280, lux: 280, occupancy: 18, status: 'critical' },
  { id: 'SEN-LIB-201', tag: 'TEMP_CO2_06', building: 'Aptullah Kuran', floor: 2, location: '2. Kat Sessiz Salon', tempC: 22.0, humidityPct: 44, co2Ppm: 720, lux: 350, occupancy: 210, status: 'normal' },
  { id: 'SEN-KY-101', tag: 'TEMP_CO2_07', building: 'Kuzey Yemekhane', floor: 1, location: 'Turnike Giriş Salonu', tempC: 24.2, humidityPct: 58, co2Ppm: 990, lux: 480, occupancy: 460, status: 'warning' },
];

const INITIAL_AHU: AHUUnit[] = [
  { id: 'AHU-01', name: 'AHU-01 (Kuzey Amfiler)', building: 'New Hall', supplyAirTempC: 17.2, returnAirTempC: 23.4, setpointC: 22.0, fanSpeedPct: 78, coolingCoilPct: 64, heatingCoilPct: 0, filterPressurePa: 142, airFlowCfm: 8500, mode: 'eco_cooling' },
  { id: 'AHU-02', name: 'AHU-02 (Perkins / M)', building: 'Perkins Hall', supplyAirTempC: 18.0, returnAirTempC: 24.1, setpointC: 22.5, fanSpeedPct: 82, coolingCoilPct: 72, heatingCoilPct: 0, filterPressurePa: 158, airFlowCfm: 9200, mode: 'standard' },
  { id: 'AHU-03', name: 'AHU-03 (Kare Blok Çekirdek)', building: 'Kare Blok', supplyAirTempC: 16.8, returnAirTempC: 22.9, setpointC: 21.5, fanSpeedPct: 65, coolingCoilPct: 45, heatingCoilPct: 0, filterPressurePa: 110, airFlowCfm: 7100, mode: 'eco_cooling' },
  { id: 'AHU-04', name: 'AHU-04 (Kütüphane Hava Kalitesi)', building: 'Aptullah Kuran', supplyAirTempC: 17.5, returnAirTempC: 22.6, setpointC: 22.0, fanSpeedPct: 70, coolingCoilPct: 55, heatingCoilPct: 0, filterPressurePa: 125, airFlowCfm: 6400, mode: 'eco_cooling' },
];

const POWER_TELEMETRY = [
  { time: '12:00', TR1_Amper: 420, TR2_Amper: 380, HarmonikTHD: 2.8, CosPhi: 0.98 },
  { time: '12:10', TR1_Amper: 460, TR2_Amper: 410, HarmonikTHD: 3.1, CosPhi: 0.97 },
  { time: '12:20', TR1_Amper: 510, TR2_Amper: 440, HarmonikTHD: 3.4, CosPhi: 0.96 },
  { time: '12:30', TR1_Amper: 540, TR2_Amper: 480, HarmonikTHD: 3.6, CosPhi: 0.96 },
  { time: '12:40', TR1_Amper: 520, TR2_Amper: 470, HarmonikTHD: 3.3, CosPhi: 0.97 },
  { time: '12:50', TR1_Amper: 490, TR2_Amper: 430, HarmonikTHD: 3.0, CosPhi: 0.98 },
];

export default function ControlRoomPage() {
  const [sensors, setSensors] = useState<SensorTelemetry[]>(INITIAL_SENSORS);
  const [ahus, setAhus] = useState<AHUUnit[]>(INITIAL_AHU);
  const [selectedAhu, setSelectedAhu] = useState<AHUUnit>(INITIAL_AHU[0]);
  const [activeTab, setActiveTab] = useState<'iot' | 'ahu' | 'grid' | 'alarms'>('iot');
  const [emergencyDemandResponse, setEmergencyDemandResponse] = useState(false);
  const [alarmList, setAlarmList] = useState([
    { id: 'ALM-902', severity: 'CRITICAL', text: 'Anderson Hall TB 410: CO2 konsantrasyonu 1280 ppm aşıldı! Taze hava damperi %100 açılmalı.', time: '12:28', ack: false },
    { id: 'ALM-903', severity: 'WARNING', text: 'New Hall NH 401: Sıcaklık setpoint değerinden +3.8°C yukarıda.', time: '12:24', ack: false },
    { id: 'ALM-904', severity: 'INFO', text: 'Kilyos 1.0 MW Türbin: Rüzgar hızı 23.4 km/h, stabil şebeke senkronizasyonu.', time: '12:15', ack: true },
  ]);

  // Live real-time IoT jitter simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setSensors(prev =>
        prev.map(s => ({
          ...s,
          tempC: Math.round((s.tempC + (Math.random() - 0.5) * 0.2) * 10) / 10,
          co2Ppm: Math.max(400, Math.min(1600, Math.round(s.co2Ppm + (Math.random() - 0.5) * 12))),
          humidityPct: Math.round(s.humidityPct + (Math.random() - 0.5) * 0.4)
        }))
      );
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  const handleAcknowledge = (id: string) => {
    setAlarmList(prev => prev.map(a => a.id === id ? { ...a, ack: true } : a));
  };

  const toggleEmergencyDemandResponse = () => {
    const nextState = !emergencyDemandResponse;
    setEmergencyDemandResponse(nextState);
    if (nextState) {
      setAhus(prev => prev.map(a => ({ ...a, fanSpeedPct: Math.max(50, a.fanSpeedPct - 20), setpointC: a.setpointC + 1.5, mode: 'night_setback' })));
    } else {
      setAhus(INITIAL_AHU);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* SCADA Header */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-xl border border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
            <Cpu size={28} className="animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-black tracking-tight">SCADA & Dijital İkiz Kontrol Merkezi</h1>
              <span className="bg-emerald-500/20 text-emerald-300 text-xs px-2.5 py-0.5 rounded-full font-mono font-bold border border-emerald-500/30 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                ONLINE 200 OK
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Boğaziçi Üniversitesi Kampüs Otomasyonu • BACnet/IP • Modbus TCP • LoRaWAN IoT Gateway
            </p>
          </div>
        </div>

        {/* Emergency Demand Response Button */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={toggleEmergencyDemandResponse}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-md flex items-center gap-2 ${
              emergencyDemandResponse
                ? 'bg-rose-600 text-white animate-pulse border border-rose-400'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
            }`}
          >
            <ShieldAlert size={16} />
            <span>{emergencyDemandResponse ? 'Tepe Talep Kısıtlaması (AKTİF)' : 'Otomatik Şebeke Talep Yanıtı (DR)'}</span>
          </button>

          <div className="text-xs font-mono bg-slate-800 px-3 py-2 rounded-xl border border-slate-700 text-slate-300">
            MQTT Gecikme: <span className="text-emerald-400 font-bold">18 ms</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-gray-200 pb-2 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setActiveTab('iot')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeTab === 'iot' ? 'bg-emerald-700 text-white shadow-xs' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <Radio size={15} />
          <span>Canlı IoT Telemetrisi ({sensors.length} Nokta)</span>
        </button>
        <button
          onClick={() => setActiveTab('ahu')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeTab === 'ahu' ? 'bg-emerald-700 text-white shadow-xs' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <Fan size={15} />
          <span>HVAC Santralleri (AHU Şematikleri)</span>
        </button>
        <button
          onClick={() => setActiveTab('grid')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeTab === 'grid' ? 'bg-emerald-700 text-white shadow-xs' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <Zap size={15} />
          <span>Trafo & Elektrik Analizörleri (TR-1 / TR-2)</span>
        </button>
        <button
          onClick={() => setActiveTab('alarms')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 ${activeTab === 'alarms' ? 'bg-emerald-700 text-white shadow-xs' : 'text-gray-600 hover:bg-gray-100'}`}
        >
          <BellRing size={15} />
          <span>Alarm Konsolu ({alarmList.filter(a => !a.ack).length} Bekleyen)</span>
        </button>
      </div>

      {/* TAB 1: IOT TELEMETRY MATRIX */}
      {activeTab === 'iot' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {sensors.map(sensor => (
              <div
                key={sensor.id}
                className={`bg-white rounded-2xl p-4 border transition hover:shadow-md ${
                  sensor.status === 'critical'
                    ? 'border-rose-400 bg-rose-50/20'
                    : sensor.status === 'warning'
                    ? 'border-amber-400 bg-amber-50/20'
                    : 'border-gray-200'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <span className="text-[10px] font-mono font-bold text-gray-400 block">{sensor.id}</span>
                    <h3 className="font-bold text-sm text-gray-900">{sensor.location}</h3>
                    <p className="text-[11px] text-gray-500">{sensor.building} • Kat {sensor.floor}</p>
                  </div>
                  <span
                    className={`w-2.5 h-2.5 rounded-full ${
                      sensor.status === 'critical'
                        ? 'bg-rose-500 animate-ping'
                        : sensor.status === 'warning'
                        ? 'bg-amber-500'
                        : 'bg-emerald-500'
                    }`}
                  ></span>
                </div>

                <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
                  <div className="bg-gray-50 p-2 rounded-lg">
                    <span className="text-gray-500 block text-[10px] flex items-center gap-1">
                      <Thermometer size={11} className="text-rose-500" /> Sıcaklık
                    </span>
                    <span className="font-bold text-gray-800 text-sm">{sensor.tempC}°C</span>
                  </div>
                  <div className="bg-gray-50 p-2 rounded-lg">
                    <span className="text-gray-500 block text-[10px] flex items-center gap-1">
                      <Droplets size={11} className="text-blue-500" /> Nem
                    </span>
                    <span className="font-bold text-gray-800 text-sm">%{sensor.humidityPct}</span>
                  </div>
                  <div className="bg-gray-50 p-2 rounded-lg">
                    <span className="text-gray-500 block text-[10px] flex items-center gap-1">
                      <Wind size={11} className="text-indigo-500" /> CO₂ Düzeyi
                    </span>
                    <span className={`font-bold text-sm ${sensor.co2Ppm > 1000 ? 'text-rose-600' : 'text-gray-800'}`}>
                      {sensor.co2Ppm} ppm
                    </span>
                  </div>
                  <div className="bg-gray-50 p-2 rounded-lg">
                    <span className="text-gray-500 block text-[10px] flex items-center gap-1">
                      <Activity size={11} className="text-emerald-500" /> Canlı Kişi
                    </span>
                    <span className="font-bold text-gray-800 text-sm">{sensor.occupancy}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: AHU SCHEMATICS & CONTROL */}
      {activeTab === 'ahu' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: AHU Selector */}
          <div className="space-y-3">
            <h3 className="font-bold text-sm text-gray-700 uppercase tracking-wider">Klima Santralleri</h3>
            {ahus.map(ahu => (
              <button
                key={ahu.id}
                onClick={() => setSelectedAhu(ahu)}
                className={`w-full text-left p-4 rounded-xl border transition flex items-center justify-between ${
                  selectedAhu.id === ahu.id
                    ? 'bg-emerald-50 border-emerald-500 shadow-xs'
                    : 'bg-white border-gray-200 hover:bg-gray-50'
                }`}
              >
                <div>
                  <h4 className="font-bold text-sm text-gray-900">{ahu.name}</h4>
                  <p className="text-xs text-gray-500">{ahu.building} • Hava Debisi: {ahu.airFlowCfm} CFM</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold text-emerald-700">{ahu.fanSpeedPct}% Fan</span>
                  <span className="block text-[10px] text-gray-400">{ahu.supplyAirTempC}°C Besleme</span>
                </div>
              </button>
            ))}
          </div>

          {/* Right: Interactive AHU Schematic */}
          <div className="lg:col-span-2 bg-slate-950 text-white rounded-2xl p-6 border border-slate-800 shadow-xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
              <div>
                <span className="text-xs text-emerald-400 font-mono font-bold">{selectedAhu.id} SCHEMATIC</span>
                <h3 className="font-bold text-lg text-white">{selectedAhu.name}</h3>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-full font-mono border border-emerald-500/30">
                  Mod: {selectedAhu.mode.toUpperCase()}
                </span>
              </div>
            </div>

            {/* SVG Visual Flow Schematic */}
            <div className="relative w-full h-64 bg-slate-900 rounded-xl p-4 border border-slate-800 flex items-center justify-between overflow-x-auto">
              {/* Fresh Air Intake */}
              <div className="flex flex-col items-center text-center p-3 bg-slate-800/80 rounded-xl border border-slate-700 min-w-[100px]">
                <Wind size={24} className="text-sky-400 mb-1 animate-pulse" />
                <span className="text-[10px] text-slate-400">Taze Hava Girişi</span>
                <span className="text-xs font-bold text-white mt-1">21.5°C</span>
              </div>

              <div className="w-8 h-0.5 bg-sky-500/50"></div>

              {/* Air Filter */}
              <div className="flex flex-col items-center text-center p-3 bg-slate-800/80 rounded-xl border border-slate-700 min-w-[100px]">
                <Sliders size={24} className="text-amber-400 mb-1" />
                <span className="text-[10px] text-slate-400">Filtre Fark Basıncı</span>
                <span className="text-xs font-bold text-amber-300 mt-1">{selectedAhu.filterPressurePa} Pa (F7)</span>
              </div>

              <div className="w-8 h-0.5 bg-sky-500/50"></div>

              {/* Cooling Coil */}
              <div className="flex flex-col items-center text-center p-3 bg-slate-800/80 rounded-xl border border-slate-700 min-w-[100px]">
                <Droplets size={24} className="text-blue-400 mb-1" />
                <span className="text-[10px] text-slate-400">Soğutma Bataryası</span>
                <span className="text-xs font-bold text-blue-300 mt-1">%{selectedAhu.coolingCoilPct} Açık</span>
              </div>

              <div className="w-8 h-0.5 bg-sky-500/50"></div>

              {/* Supply Fan */}
              <div className="flex flex-col items-center text-center p-3 bg-slate-800/80 rounded-xl border border-slate-700 min-w-[100px]">
                <Fan size={24} className="text-emerald-400 mb-1 animate-spin" style={{ animationDuration: '3s' }} />
                <span className="text-[10px] text-slate-400">Besleme Fanı (VSD)</span>
                <span className="text-xs font-bold text-emerald-300 mt-1">%{selectedAhu.fanSpeedPct} Hız</span>
              </div>

              <div className="w-8 h-0.5 bg-emerald-500/50"></div>

              {/* Supply to Room */}
              <div className="flex flex-col items-center text-center p-3 bg-slate-800/80 rounded-xl border border-slate-700 min-w-[100px]">
                <Thermometer size={24} className="text-emerald-400 mb-1" />
                <span className="text-[10px] text-slate-400">Amfiye Üfleme</span>
                <span className="text-xs font-bold text-white mt-1">{selectedAhu.supplyAirTempC}°C</span>
              </div>
            </div>

            {/* Setpoint Sliders */}
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Hedef Setpoint:</span>
                <span className="text-xl font-bold text-emerald-400">{selectedAhu.setpointC}°C</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Dönüş Havası:</span>
                <span className="text-xl font-bold text-white">{selectedAhu.returnAirTempC}°C</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Toplam Debi:</span>
                <span className="text-xl font-bold text-sky-400">{selectedAhu.airFlowCfm} CFM</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: ELECTRICAL GRID & TRANSFORMERS */}
      {activeTab === 'grid' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
              <span className="text-xs text-gray-500 font-bold uppercase tracking-wider block mb-1">Trafo TR-1 (Güney)</span>
              <div className="text-3xl font-black text-gray-900">512 A</div>
              <div className="text-xs text-emerald-600 mt-1 font-semibold">Kapasite: %64 Yükte</div>
              <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-600">
                <span>Güç Faktörü (Cos φ):</span>
                <span className="font-bold text-gray-900">0.98</span>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
              <span className="text-xs text-gray-500 font-bold uppercase tracking-wider block mb-1">Trafo TR-2 (Kuzey)</span>
              <div className="text-3xl font-black text-gray-900">448 A</div>
              <div className="text-xs text-emerald-600 mt-1 font-semibold">Kapasite: %56 Yükte</div>
              <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-600">
                <span>Güç Faktörü (Cos φ):</span>
                <span className="font-bold text-gray-900">0.97</span>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
              <span className="text-xs text-gray-500 font-bold uppercase tracking-wider block mb-1">Toplam Harmonik Bozulma (THD)</span>
              <div className="text-3xl font-black text-emerald-700">%3.2</div>
              <div className="text-xs text-gray-500 mt-1">IEEE 519 standardına uygun (&lt;%5)</div>
              <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-600">
                <span>Aktif Filtre:</span>
                <span className="font-bold text-emerald-700">Devrede</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-xs">
            <h3 className="font-bold text-lg text-gray-900 mb-4">Trafo Akım Yükü (Amper) & Harmonik Eğrisi</h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={POWER_TELEMETRY} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="TR1_Amper" stroke="#059669" fill="#10b981" fillOpacity={0.4} name="TR-1 Akım (A)" />
                  <Area type="monotone" dataKey="TR2_Amper" stroke="#0284c7" fill="#38bdf8" fillOpacity={0.3} name="TR-2 Akım (A)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: ALARMS CONSOLE */}
      {activeTab === 'alarms' && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-bold text-lg text-gray-900">Sistem & Sensör Alarmları</h3>
            <span className="text-xs text-gray-500 font-mono">BMS Event Log v2.4</span>
          </div>

          <div className="space-y-3">
            {alarmList.map(alarm => (
              <div
                key={alarm.id}
                className={`p-4 rounded-xl border flex items-center justify-between gap-4 ${
                  alarm.ack
                    ? 'bg-gray-50 border-gray-200 opacity-60'
                    : alarm.severity === 'CRITICAL'
                    ? 'bg-rose-50 border-rose-300'
                    : 'bg-amber-50 border-amber-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded font-mono ${
                      alarm.severity === 'CRITICAL'
                        ? 'bg-rose-600 text-white'
                        : 'bg-amber-600 text-white'
                    }`}
                  >
                    {alarm.severity}
                  </span>
                  <div>
                    <span className="font-bold text-xs text-gray-900 block">{alarm.text}</span>
                    <span className="text-[10px] text-gray-500">{alarm.time} • Olay Kodu: {alarm.id}</span>
                  </div>
                </div>

                <div>
                  {alarm.ack ? (
                    <span className="text-xs text-gray-500 font-medium flex items-center gap-1">
                      <CheckCircle size={14} className="text-emerald-600" /> Onaylandı
                    </span>
                  ) : (
                    <button
                      onClick={() => handleAcknowledge(alarm.id)}
                      className="px-3 py-1.5 bg-gray-900 text-white rounded-lg text-xs font-semibold hover:bg-black transition"
                    >
                      Onayla (ACK)
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
