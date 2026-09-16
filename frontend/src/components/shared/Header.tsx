'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BookOpen,
  Building2,
  ChevronDown,
  Compass,
  Database,
  FlaskConical,
  LayoutDashboard,
  Search,
  Sparkles,
} from 'lucide-react';

const EXPERIMENTAL_PREFIXES = [
  '/flow', '/microgrid', '/control-room', '/anomalies', '/rescheduler', '/agent-simulation',
  '/student', '/solar', '/maintenance', '/acoustic', '/iot-registry', '/integrations',
  '/esg-reports', '/food-waste', '/water', '/transit', '/league',
];

const primaryNav = [
  { href: '/', label: 'Overview', icon: LayoutDashboard },
  { href: '/buildings', label: 'Campus', icon: Building2 },
  { href: '/courses', label: 'Courses', icon: BookOpen },
  { href: '/scenarios', label: 'Scenarios', icon: Compass },
];

const labModules = [
  ['Operations', [
    ['/flow', 'Akış modeli'], ['/rescheduler', 'Amfi konsolidasyonu'], ['/agent-simulation', 'Ajan simülasyonu'], ['/student', 'Öğrenci karar destek'],
  ]],
  ['Energy', [
    ['/microgrid', 'Enerji senaryosu'], ['/control-room', 'Kontrol odası'], ['/solar', 'Çatı GES'], ['/maintenance', 'Kestirimci bakım'],
  ]],
  ['Sensing', [
    ['/anomalies', 'Anomali modeli'], ['/acoustic', 'Akustik harita'], ['/iot-registry', 'IoT tasarımı'], ['/integrations', 'Protokol gateway'],
  ]],
  ['Sustainability', [
    ['/food-waste', 'Gıda israfı'], ['/water', 'Su yönetimi'], ['/transit', 'Mekik & mobilite'], ['/esg-reports', 'Karbon raporu'],
  ]],
] as const;

export default function Header() {
  const pathname = usePathname();
  const [labOpen, setLabOpen] = useState(false);
  const isExperimentalRoute = EXPERIMENTAL_PREFIXES.some(prefix => pathname.startsWith(prefix));

  return (
    <>
      <header className="sticky top-0 z-50 border-b border-slate-950/10 bg-[#f4f5f2]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] w-full max-w-[1640px] items-center justify-between gap-4 px-4 sm:px-5 md:px-7 lg:px-9">
          <div className="flex min-w-0 items-center gap-8">
            <Link href="/" className="group flex shrink-0 items-center gap-3 bc-focus-ring rounded-xl">
              <div className="grid h-10 w-10 place-items-center rounded-[14px] bg-[#0b1226] text-[11px] font-black tracking-[0.08em] text-white shadow-[0_8px_24px_rgba(11,18,38,0.16)] transition-transform group-hover:-translate-y-0.5">
                BC
              </div>
              <div className="hidden sm:block">
                <div className="flex items-center gap-2">
                  <span className="text-[15px] font-black tracking-[-0.035em] text-[#0a1020]">BOUNCAMPUS</span>
                  <span className="rounded-full border border-blue-200 bg-blue-50 px-1.5 py-0.5 font-mono text-[8px] font-extrabold tracking-[0.08em] text-blue-700">BETA</span>
                </div>
                <span className="block text-[10px] font-medium tracking-[0.01em] text-slate-500">Campus intelligence for Boğaziçi</span>
              </div>
            </Link>

            <nav className="hidden items-center gap-1 lg:flex">
              {primaryNav.map(link => {
                const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`bc-focus-ring flex items-center gap-1.5 rounded-xl px-3 py-2 text-xs font-bold transition ${
                      active ? 'bg-white text-[#0a1020] shadow-sm ring-1 ring-slate-950/10' : 'text-slate-500 hover:bg-white/70 hover:text-slate-900'
                    }`}
                  >
                    <Icon size={13} strokeWidth={2.1} />
                    {link.label}
                  </Link>
                );
              })}

              <div className="relative ml-1">
                <button
                  type="button"
                  onClick={() => setLabOpen(value => !value)}
                  className="bc-focus-ring flex items-center gap-1.5 rounded-xl px-3 py-2 text-xs font-bold text-slate-500 transition hover:bg-white/70 hover:text-slate-900"
                >
                  <Sparkles size={13} />
                  Lab
                  <ChevronDown size={12} className={`transition-transform ${labOpen ? 'rotate-180' : ''}`} />
                </button>

                {labOpen && (
                  <div className="absolute left-0 top-12 w-[660px] rounded-[24px] border border-slate-950/10 bg-[#0b1226] p-5 text-white shadow-[0_24px_80px_rgba(11,18,38,0.24)]">
                    <div className="mb-4 flex items-start justify-between gap-4 border-b border-white/10 pb-4">
                      <div>
                        <p className="text-sm font-black tracking-[-0.02em]">Prototype laboratory</p>
                        <p className="mt-1 max-w-md text-[11px] leading-relaxed text-slate-400">Pilot-ready product concepts. These modules are simulations until university telemetry integrations are authorized.</p>
                      </div>
                      <span className="rounded-full border border-amber-400/20 bg-amber-400/10 px-2.5 py-1 font-mono text-[9px] font-bold text-amber-300">SIMULATION</span>
                    </div>
                    <div className="grid grid-cols-2 gap-x-8 gap-y-5">
                      {labModules.map(([title, items]) => (
                        <div key={title}>
                          <div className="mb-2 text-[9px] font-black uppercase tracking-[0.18em] text-slate-500">{title}</div>
                          <div className="grid gap-1">
                            {items.map(([href, label]) => (
                              <Link key={href} href={href} onClick={() => setLabOpen(false)} className="rounded-lg px-2 py-1.5 text-xs font-semibold text-slate-300 transition hover:bg-white/7 hover:text-white">
                                {label}
                              </Link>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </nav>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link href="/#sources" className="bc-focus-ring hidden items-center gap-2 rounded-xl border border-slate-950/10 bg-white/75 px-3 py-2 text-[10px] font-bold text-slate-600 shadow-sm transition hover:bg-white md:flex">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-500 opacity-40" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-600" />
              </span>
              Source-traceable
            </Link>
            <Link href="/courses" className="bc-focus-ring flex items-center gap-2 rounded-xl bg-[#0b1226] px-3.5 py-2 text-xs font-bold text-white shadow-[0_8px_24px_rgba(11,18,38,0.14)] transition hover:-translate-y-0.5 hover:bg-[#111a32]">
              <Search size={13} />
              <span className="hidden sm:inline">Search campus</span>
            </Link>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-[1640px] gap-1 overflow-x-auto px-4 pb-2 lg:hidden sm:px-5 md:px-7">
          {primaryNav.map(link => {
            const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
            return (
              <Link key={link.href} href={link.href} className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-bold ${active ? 'bg-[#0b1226] text-white' : 'border border-slate-950/10 bg-white/60 text-slate-600'}`}>
                {link.label}
              </Link>
            );
          })}
        </div>
      </header>

      {isExperimentalRoute && (
        <div className="border-b border-amber-300/40 bg-[#fff6e8]">
          <div className="mx-auto flex w-full max-w-[1640px] items-start gap-2 px-4 py-2 text-[10px] leading-relaxed text-amber-950 sm:px-5 md:px-7 lg:px-9">
            <FlaskConical size={13} className="mt-0.5 shrink-0" />
            <strong className="shrink-0 font-black">PROTOTYPE MODE</strong>
            <span className="text-amber-900/75">This module demonstrates a future workflow. Sensor, SCADA/BMS, POS or IoT values shown here are not connected university telemetry.</span>
          </div>
        </div>
      )}
    </>
  );
}
