'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Building2, Compass, Navigation, Zap, Utensils, LayoutDashboard,
  Cpu, Shuffle, FileText, Users, Bus, GraduationCap, ChevronDown,
  Wrench, Droplets, Sun, Trophy, Network, ShieldAlert, Volume2, Server, BookOpen,
  Search, Database,
} from 'lucide-react';

export default function Header() {
  const pathname = usePathname();
  const [suiteMenuOpen, setSuiteMenuOpen] = useState(false);

  const primaryNav = [
    { href: '/', label: 'Genel Bakış', icon: LayoutDashboard },
    { href: '/courses', label: 'Ders & Amfi', icon: BookOpen },
    { href: '/flow', label: 'Akış Modeli', icon: Navigation },
    { href: '/microgrid', label: 'Enerji Senaryosu', icon: Zap },
    { href: '/control-room', label: 'Kontrol Simülasyonu', icon: Cpu },
    { href: '/anomalies', label: 'Anomali Modeli', icon: ShieldAlert },
    { href: '/buildings', label: 'Binalar', icon: Building2 },
    { href: '/scenarios', label: 'Simülatör', icon: Compass },
  ];

  const suiteCategories = [
    {
      title: 'Akademik & Amfiler',
      items: [
        { href: '/courses', label: 'BUIS/ÖBİKAS Ders & Amfi Motoru', desc: 'Resmî ders programı snapshot + tahmini derslik kullanımı', icon: BookOpen },
        { href: '/rescheduler', label: 'Amfi Konsolidatörü', desc: 'Ders programı üzerinde optimizasyon senaryosu', icon: Shuffle },
        { href: '/agent-simulation', label: 'Ajanlı Akış Simülatörü', desc: 'Sentetik öğrenci ajanlarıyla kampüs akış senaryosu', icon: Users },
        { href: '/student', label: 'Öğrenci Karar Destek', desc: 'Model tabanlı çalışma alanı ve yoğunluk önerileri', icon: GraduationCap },
      ],
    },
    {
      title: 'Enerji & Kontrol Senaryoları',
      items: [
        { href: '/control-room', label: 'Kontrol Odası Prototipi', desc: 'BMS entegrasyonuna hazır simülasyon arayüzü; canlı BMS bağlı değil', icon: Cpu },
        { href: '/microgrid', label: 'Kilyos Rüzgâr Senaryosu', desc: 'Haricî hava verisiyle üretim ve yük senaryosu', icon: Zap },
        { href: '/solar', label: 'Çatı GES Potansiyeli', desc: 'Güneş üretimi ve gölge senaryosu; saha ölçümü değil', icon: Sun },
        { href: '/maintenance', label: 'Kestirimci Bakım Prototipi', desc: 'Sentetik titreşim/arıza verisiyle bakım senaryosu', icon: Wrench },
      ],
    },
    {
      title: 'İzleme & Entegrasyon Prototipleri',
      items: [
        { href: '/anomalies', label: 'Anomali Radarı', desc: 'Model tabanlı su/enerji anomali senaryoları', icon: ShieldAlert },
        { href: '/acoustic', label: 'Akustik Harita', desc: 'Akustik kullanım senaryosu; canlı mikrofon ağı bağlı değil', icon: Volume2 },
        { href: '/iot-registry', label: 'IoT Entegrasyon Tasarımı', desc: 'BACnet, Modbus ve LoRaWAN için örnek cihaz modeli', icon: Network },
        { href: '/integrations', label: 'Protokol Gateway Tasarımı', desc: 'Gelecekteki kampüs sistem entegrasyonları için arayüz', icon: Server },
      ],
    },
    {
      title: 'Sürdürülebilirlik & Kaynaklar',
      items: [
        { href: '/esg-reports', label: 'Karbon Raporlama Taslağı', desc: 'ISO 14064 uyum hedefli hesaplama şablonu; sertifika/denetim değildir', icon: FileText },
        { href: '/food-waste', label: 'Gıda İsrafı Modeli', desc: 'SKS resmî menü + ders akışından talep tahmini', icon: Utensils },
        { href: '/water', label: 'Su & Yağmur Hasadı Senaryosu', desc: 'Su yönetimi için model tabanlı optimizasyon prototipi', icon: Droplets },
        { href: '/transit', label: 'Mekik & Mobilite', desc: 'Resmî Mekik tarifesi + model tabanlı talep senaryosu', icon: Bus },
        { href: '/league', label: 'Yeşil Lig', desc: 'Fakülte sürdürülebilirlik etkileşim prototipi', icon: Trophy },
      ],
    },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-slate-100 sticky top-0 z-50 backdrop-blur-md bg-opacity-95">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center font-mono text-sm font-black text-slate-100 group-hover:border-emerald-500 transition">
              BC
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-black tracking-tight text-white">BOUNCAMPUS</span>
                <span className="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-violet-950 text-violet-300 border border-violet-800">
                  HACKATHON PROTOTİPİ
                </span>
              </div>
              <span className="block text-[10px] text-slate-400 font-medium tracking-wide">
                Boğaziçi public data + şeffaf karar modelleri
              </span>
            </div>
          </Link>
        </div>

        <nav className="hidden xl:flex items-center space-x-1">
          {primaryNav.map(link => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition ${isActive ? 'bg-slate-800 text-white border border-slate-700 shadow-xs' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'}`}
              >
                <Icon size={14} className={isActive ? 'text-emerald-400' : 'text-slate-400'} />
                <span>{link.label}</span>
              </Link>
            );
          })}

          <div className="relative ml-2">
            <button
              onClick={() => setSuiteMenuOpen(!suiteMenuOpen)}
              onBlur={() => setTimeout(() => setSuiteMenuOpen(false), 250)}
              className="px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 text-slate-300 hover:text-white bg-slate-800/80 border border-slate-700 hover:bg-slate-800 transition"
            >
              <span>Tüm Modüller</span>
              <ChevronDown size={13} className={`transition duration-200 ${suiteMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {suiteMenuOpen && (
              <div className="absolute right-0 mt-2 w-[780px] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 grid grid-cols-2 gap-6 z-50 animate-in fade-in zoom-in-95 duration-150 text-left">
                {suiteCategories.map((category, index) => (
                  <div key={index} className="space-y-2.5">
                    <h4 className="text-[11px] font-bold font-mono uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-1.5">
                      {category.title}
                    </h4>
                    <div className="space-y-1.5">
                      {category.items.map(item => {
                        const Icon = item.icon;
                        return (
                          <Link key={item.href} href={item.href} className="flex items-start gap-2.5 p-2 rounded-xl hover:bg-slate-800/80 transition group">
                            <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 mt-0.5 group-hover:border-emerald-500">
                              <Icon size={13} className="text-slate-300 group-hover:text-emerald-400" />
                            </div>
                            <div>
                              <span className="text-xs font-bold text-white block group-hover:text-emerald-300">{item.label}</span>
                              <span className="text-[11px] text-slate-400 leading-tight block">{item.desc}</span>
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

        <div className="flex items-center gap-3">
          <Link href="/#sources" className="hidden sm:flex items-center gap-2 bg-slate-800/90 border border-slate-700/80 px-3 py-1.5 rounded-xl text-xs font-mono text-slate-300">
            <Database size={12} className="text-emerald-400" />
            <span>Kaynaklar etiketli</span>
          </Link>
          <Link href="/courses" className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3.5 py-1.5 rounded-xl transition shadow-xs flex items-center gap-1.5">
            <Search size={13} />
            <span className="hidden sm:inline">Ders Ara</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
