'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Building2, Compass, Navigation, Zap, Utensils, LayoutDashboard, 
  Cpu, Shuffle, FileText, Users, Bus, GraduationCap, ChevronDown,
  Wrench, Droplets, Sun, Trophy, Network, ShieldAlert, Volume2, Server, BookOpen,
  Activity, Search
} from 'lucide-react';

export default function Header() {
  const pathname = usePathname();
  const [suiteMenuOpen, setSuiteMenuOpen] = useState(false);

  const primaryNav = [
    { href: '/', label: 'Genel Bakış', icon: LayoutDashboard },
    { href: '/courses', label: 'Ders & Amfi', icon: BookOpen },
    { href: '/flow', label: 'İnsan Akışı', icon: Navigation },
    { href: '/microgrid', label: 'Mikroşebeke', icon: Zap },
    { href: '/control-room', label: 'SCADA', icon: Cpu },
    { href: '/anomalies', label: 'Anomali', icon: ShieldAlert },
    { href: '/buildings', label: 'Binalar', icon: Building2 },
    { href: '/scenarios', label: 'Simülatör', icon: Compass },
  ];

  const suiteCategories = [
    {
      title: 'Akademik & Amfiler',
      items: [
        { href: '/courses', label: 'OBIKAS Ders & Amfi Motoru', desc: '3.238 ders programı & canlı derslik doluluğu', icon: BookOpen },
        { href: '/rescheduler', label: 'Amfi Konsolidatörü', desc: 'MIP algoritmasıyla kat kapatma & ders taşıma', icon: Shuffle },
        { href: '/agent-simulation', label: 'Ajanlı Akış Simülatörü', desc: '450+ otonom öğrencinin kampüs içi göçü', icon: Users },
        { href: '/student', label: 'Öğrenci Çalışma Portalı', desc: 'Sakin kütüphane masaları & yemekhane oylama', icon: GraduationCap },
      ]
    },
    {
      title: 'Enerji, Şebeke & SCADA',
      items: [
        { href: '/control-room', label: 'SCADA & Dijital İkiz', desc: 'Canlı BMS şematikleri ve trafo telemetrisi', icon: Cpu },
        { href: '/microgrid', label: 'Kilyos RES & Mikroşebeke', desc: '1.0 MW rüzgar türbini ve 2.0 MWh BESS', icon: Zap },
        { href: '/solar', label: 'Çatı GES Potansiyeli', desc: '1.35 MWp güneş enerjisi ve gölge simülasyonu', icon: Sun },
        { href: '/maintenance', label: 'Kestirimci Bakım & FFT', desc: 'Rulman titreşim spektrumu ve kalan ömür', icon: Wrench },
      ]
    },
    {
      title: 'Otonom İzleme & Saha Ağları',
      items: [
        { href: '/anomalies', label: 'AI Anomali Radarı', desc: 'Otomatik su/elektrik kaçak izolasyonu', icon: ShieldAlert },
        { href: '/acoustic', label: 'Akustik Desibel Haritası', desc: 'Kütüphane sessiz katları ve ses sentezi', icon: Volume2 },
        { href: '/iot-registry', label: 'IoT Cihaz Envanteri', desc: '148 adet BACnet, Modbus ve LoRaWAN düğümü', icon: Network },
        { href: '/integrations', label: 'Protokol Gateway', desc: 'Endüstriyel ağ köprüsü ve paket dinleyici', icon: Server },
      ]
    },
    {
      title: 'Sürdürülebilirlik & Kaynaklar',
      items: [
        { href: '/esg-reports', label: 'ISO 14064 ESG Karbon Raporu', desc: 'Kapsam 1/2/3 kurumsal sera gazı denetimi', icon: FileText },
        { href: '/food-waste', label: 'Sıfır Atık Mutfak', desc: 'SKS yemek porsiyon optimizasyonu', icon: Utensils },
        { href: '/water', label: 'Akıllı Su & Yağmur Hasadı', desc: '500 m³ tarihi sarnıç ve akustik dinleme', icon: Droplets },
        { href: '/transit', label: 'Elektrikli Ring Filosu', desc: 'Bebek yokuşu rejeneratif fren enerjisi', icon: Bus },
        { href: '/league', label: 'Fakülteler Arası Yeşil Lig', desc: 'Aylık fakülte sürdürülebilirlik yarışı', icon: Trophy },
      ]
    }
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-slate-100 sticky top-0 z-50 backdrop-blur-md bg-opacity-95">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Institutional Brand Identity */}
        <div className="flex items-center space-x-3">
          <Link href="/" className="flex items-center gap-3 group">
            {/* Boğaziçi Emblem */}
            <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center font-serif text-lg font-black text-slate-100 group-hover:border-emerald-500 transition">
              BÜ
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-black tracking-tight text-white font-sans">
                  BOUNCAMPUS
                </span>
                <span className="text-[10px] font-mono font-bold px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  v4.2
                </span>
              </div>
              <span className="block text-[10px] text-slate-400 font-medium tracking-wide">
                Boğaziçi Üniversitesi Dijital İkiz & Karar Destek
              </span>
            </div>
          </Link>
        </div>

        {/* Primary Nav Links */}
        <nav className="hidden xl:flex items-center space-x-1">
          {primaryNav.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition ${
                  isActive
                    ? 'bg-slate-800 text-white border border-slate-700 shadow-xs'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon size={14} className={isActive ? 'text-emerald-400' : 'text-slate-400'} />
                <span>{link.label}</span>
              </Link>
            );
          })}

          {/* Institutional Megamenu Dropdown */}
          <div className="relative ml-2">
            <button
              onClick={() => setSuiteMenuOpen(!suiteMenuOpen)}
              onBlur={() => setTimeout(() => setSuiteMenuOpen(false), 250)}
              className="px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 text-slate-300 hover:text-white bg-slate-800/80 border border-slate-700 hover:bg-slate-800 transition"
            >
              <span>Tüm Modüller</span>
              <ChevronDown size={13} className={`transition duration-200 ${suiteMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Megamenu Panel */}
            {suiteMenuOpen && (
              <div className="absolute right-0 mt-2 w-[780px] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 grid grid-cols-2 gap-6 z-50 animate-in fade-in zoom-in-95 duration-150 text-left">
                {suiteCategories.map((cat, idx) => (
                  <div key={idx} className="space-y-2.5">
                    <h4 className="text-[11px] font-bold font-mono uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5">
                      {cat.title}
                    </h4>
                    <div className="space-y-1.5">
                      {cat.items.map((item) => {
                        const Icon = item.icon;
                        return (
                          <Link
                            key={item.href}
                            href={item.href}
                            className="flex items-start gap-2.5 p-2 rounded-xl hover:bg-slate-800/80 transition group"
                          >
                            <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 mt-0.5 group-hover:border-emerald-500">
                              <Icon size={13} className="text-slate-300 group-hover:text-emerald-400" />
                            </div>
                            <div>
                              <span className="text-xs font-bold text-white block group-hover:text-emerald-300">
                                {item.label}
                              </span>
                              <span className="text-[11px] text-slate-400 leading-tight block">
                                {item.desc}
                              </span>
                            </div>
                          </Link>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </nav>

        {/* Right Status Badge */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 bg-slate-800/90 border border-slate-700/80 px-3 py-1.5 rounded-xl text-xs font-mono text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>SCADA LAN: Nominal</span>
          </div>

          <Link
            href="/courses"
            className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3.5 py-1.5 rounded-xl transition shadow-xs flex items-center gap-1.5"
          >
            <Search size={13} />
            <span className="hidden sm:inline">Ders Ara</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
