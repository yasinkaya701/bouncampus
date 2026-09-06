'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { format } from 'date-fns';
import { 
  Building2, Compass, Navigation, Zap, Utensils, LayoutDashboard, 
  Cpu, Shuffle, FileText, Users, Bus, GraduationCap, ChevronDown,
  Wrench, Droplets, Sun, Trophy, Network 
} from 'lucide-react';
import { useState } from 'react';

export default function Header() {
  const pathname = usePathname();
  const currentDate = format(new Date(), 'EEEE, d MMMM yyyy');
  const [suiteMenuOpen, setSuiteMenuOpen] = useState(false);

  const primaryNav = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/flow', label: 'Akış & Ring', icon: Navigation, badge: 'Live' },
    { href: '/microgrid', label: 'Mikroşebeke & RES', icon: Zap, badge: '420kW' },
    { href: '/control-room', label: 'SCADA Merkezi', icon: Cpu, badge: 'BMS' },
    { href: '/buildings', label: 'Binalar', icon: Building2 },
    { href: '/scenarios', label: 'Simülatör', icon: Compass },
  ];

  const enterpriseSuites = [
    { href: '/maintenance', label: 'Kestirimci Bakım & Titreşim', desc: 'FFT Rulman Spektrumu & Kalan Ömür (RUL)', icon: Wrench },
    { href: '/water', label: 'Akıllı Su & Yağmur Hasadı', desc: '500 m³ Sarnıç & Akustik Kaçak Tespiti', icon: Droplets },
    { href: '/solar', label: 'Çatı Güneş Santralleri (SPP)', desc: '1.35 MWp Çatı Potansiyeli & Gölge Analizi', icon: Sun },
    { href: '/league', label: 'Fakülteler Arası Yeşil Lig', desc: 'Aylık Enerji & Sıfır Atık Şampiyonası', icon: Trophy },
    { href: '/iot-registry', label: 'IoT Cihaz Envanteri & Ağ', desc: '148 Gateway, BACnet & LoRaWAN Ağ Durumu', icon: Network },
    { href: '/rescheduler', label: 'Amfi Konsolidatörü', desc: 'MIP Algoritmasıyla Kat Kapatma & Taşımalar', icon: Shuffle },
    { href: '/esg-reports', label: 'ESG & Karbon Denetimi', desc: 'ISO 14064 Scope 1/2/3 Raporu', icon: FileText },
    { href: '/agent-simulation', label: 'Ajanlı Akış Motoru', desc: '450+ Otonom Öğrenci Ajan Simülasyonu', icon: Users },
    { href: '/food-waste', label: 'Sıfır Atık Mutfak', desc: 'SKS Yemekhane Porsiyon & Gıda Kurtarma', icon: Utensils },
    { href: '/transit', label: 'Elektrikli Ring Filosu', desc: 'Bebek Yokuşu Rejeneratif Telemetrisi', icon: Bus },
    { href: '/student', label: 'Öğrenci Portalı', desc: 'Sakin Çalışma Masası & Menü Puanlama', icon: GraduationCap },
  ];

  return (
    <header className="bg-emerald-950 text-white shadow-lg sticky top-0 z-50 border-b border-emerald-900/60 backdrop-blur-md bg-opacity-95">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center space-x-3">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center font-black text-white shadow-md group-hover:scale-105 transition">
              B
            </div>
            <div>
              <span className="text-xl font-black tracking-tight flex items-center gap-1.5">
                BOUNCAMPUS
                <span className="text-[10px] font-bold px-1.5 py-0.2 rounded-md bg-emerald-800 text-emerald-300 uppercase tracking-widest border border-emerald-700/50">
                  Enterprise
                </span>
              </span>
              <span className="block text-[10px] text-emerald-400 font-medium tracking-wide">
                Boğaziçi Karar Destek & Sürdürülebilirlik
              </span>
            </div>
          </Link>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden lg:flex items-center space-x-1">
          {primaryNav.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  isActive
                    ? 'bg-emerald-800/80 text-white shadow-xs border border-emerald-700/50'
                    : 'text-emerald-200/80 hover:text-white hover:bg-emerald-900/50'
                }`}
              >
                <Icon size={14} className={isActive ? 'text-emerald-400' : 'text-emerald-400/70'} />
                <span>{link.label}</span>
                {link.badge && (
                  <span className="text-[9px] bg-teal-500/20 text-teal-300 px-1.5 py-0.2 rounded-full font-mono font-bold">
                    {link.badge}
                  </span>
                )}
              </Link>
            );
          })}

          {/* More Suites Dropdown */}
          <div className="relative">
            <button
              onClick={() => setSuiteMenuOpen(!suiteMenuOpen)}
              onBlur={() => setTimeout(() => setSuiteMenuOpen(false), 200)}
              className="px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 text-emerald-300 hover:text-white hover:bg-emerald-900/50 transition"
            >
              <span>Gelişmiş Modüller</span>
              <ChevronDown size={13} className={`transition ${suiteMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {suiteMenuOpen && (
              <div className="absolute right-0 top-full mt-2 w-72 bg-slate-900 border border-emerald-800/60 rounded-2xl shadow-2xl p-2 z-50 animate-in fade-in zoom-in-95 duration-150">
                <div className="text-[10px] uppercase font-mono font-bold text-emerald-400 px-3 py-1 border-b border-slate-800 mb-1">
                  Optimizasyon & Karar Paketleri
                </div>
                {enterpriseSuites.map((item) => {
                  const SIcon = item.icon;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="p-2.5 rounded-xl hover:bg-emerald-950 flex items-start gap-2.5 transition text-left group"
                    >
                      <SIcon size={16} className="text-emerald-400 mt-0.5 group-hover:scale-110 transition" />
                      <div>
                        <div className="text-xs font-bold text-white group-hover:text-emerald-300">{item.label}</div>
                        <div className="text-[10px] text-slate-400">{item.desc}</div>
                      </div>
                    </Link>
                  );
                })}
              </div>
            )}
          </div>
        </nav>

        {/* Right Info */}
        <div className="flex items-center space-x-3">
          <div className="hidden sm:block text-right">
            <div className="text-xs font-semibold text-emerald-100">{currentDate}</div>
            <div className="text-[10px] text-emerald-400/80 flex items-center justify-end gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>3.238 Gerçek Ders • SCADA Canlı</span>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Scrollable Nav */}
      <div className="lg:hidden flex items-center gap-1 px-4 py-2 border-t border-emerald-900/40 overflow-x-auto no-scrollbar bg-emerald-950/90">
        {[...primaryNav, ...enterpriseSuites].map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`whitespace-nowrap px-2.5 py-1 rounded-md text-[11px] font-semibold flex items-center gap-1 transition ${
                isActive
                  ? 'bg-emerald-800 text-white'
                  : 'text-emerald-300 hover:text-white'
              }`}
            >
              <Icon size={12} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </div>
    </header>
  );
}
