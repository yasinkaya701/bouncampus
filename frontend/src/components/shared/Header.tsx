'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BookOpen,
  Building2,
  CheckSquare2,
  ChevronDown,
  Compass,
  Database,
  FlaskConical,
  LayoutDashboard,
  Play,
  Sparkles,
  Trophy,
} from 'lucide-react';

const EXPERIMENTAL_PREFIXES = [
  '/flow', '/microgrid', '/control-room', '/anomalies', '/rescheduler', '/agent-simulation',
  '/student', '/solar', '/maintenance', '/acoustic', '/iot-registry', '/integrations',
  '/esg-reports', '/food-waste', '/water', '/transit', '/league',
];

const primaryNav = [
  { href: '/', label: 'Mission', icon: LayoutDashboard },
  { href: '/buildings', label: 'Campus', icon: Building2 },
  { href: '/courses', label: 'Schedule', icon: BookOpen },
  { href: '/decisions', label: 'Decisions', icon: CheckSquare2 },
  { href: '/scenarios', label: 'Simulate', icon: Compass },
  { href: '/data', label: 'Trust', icon: Database },
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
  const labActive = pathname === '/lab' || isExperimentalRoute;
  const demoActive = pathname === '/demo';

  return (
    <>
      <header className="sticky top-0 z-50 border-b border-slate-950/10 bg-[#f4f5f2]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] w-full max-w-[1640px] items-center justify-between gap-4 px-4 sm:px-5 md:px-7 lg:px-9">
          <div className="flex min-w-0 items-center gap-7">
            <Link href="/" className="group flex shrink-0 items-center gap-3 bc-focus-ring rounded-xl">
              <div className="grid h-10 w-10 place-items-center rounded-[14px] bg-[#0b1226] text-[11px] font-black tracking-[0.08em] text-white shadow-[0_8px_24px_rgba(11,18,38,0.16)] transition-transform group-hover:-translate-y-0.5">BC</div>
              <div className="hidden sm:block">
                <div className="flex items-center gap-2">
                  <span className="text-[15px] font-black tracking-[-0.035em] text-[#0a1020]">BOUNCAMPUS</span>
                  <span className="rounded-full border border-blue-200 bg-blue-50 px-1.5 py-0.5 font-mono text-[8px] font-extrabold tracking-[0.08em] text-blue-700">MISSION CONTROL</span>
                </div>
                <span className="block text-[10px] font-medium tracking-[0.01em] text-slate-500">Decision intelligence for Boğaziçi</span>
              </div>
            </Link>

            <nav className="hidden items-center gap-1 xl:flex">
              {primaryNav.map(link => {
                const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
                const Icon = link.icon;
                return (
                  <Link key={link.href} href={link.href} className={`bc-focus-ring flex items-center gap-1.5 rounded-xl px-2.5 py-2 text-[11px] font-bold transition ${active ? 'bg-white text-[#0a1020] shadow-sm ring-1 ring-slate-950/10' : 'text-slate-500 hover:bg-white/70 hover:text-slate-900'}`}>
                    <Icon size={12} strokeWidth={2.1} />{link.label}
                  </Link>
                );
              })}

              <div className="relative ml-1">
                <div className="flex items-center">
                  <Link href="/lab" className={`bc-focus-ring flex items-center gap-1.5 rounded-l-xl px-2.5 py-2 text-[11px] font-bold transition ${labActive ? 'bg-white text-[#0a1020] shadow-sm ring-1 ring-slate-950/10' : 'text-slate-500 hover:bg-white/70 hover:text-slate-900'}`}>
                    <Sparkles size={12} /> Lab
                  </Link>
                  <button type="button" onClick={() => setLabOpen(value => !value)} className={`bc-focus-ring rounded-r-xl border-l border-slate-950/8 px-1.5 py-2.5 text-slate-500 transition hover:bg-white/70 hover:text-slate-900 ${labActive ? 'bg-white shadow-sm ring-1 ring-slate-950/10' : ''}`} aria-label="Open prototype lab menu">
                    <ChevronDown size={11} className={`transition-transform ${labOpen ? 'rotate-180' : ''}`} />
                  </button>
                </div>

                {labOpen && (
                  <div className="absolute right-0 top-12 w-[660px] rounded-[24px] border border-slate-950/10 bg-[#0b1226] p-5 text-white shadow-[0_24px_80px_rgba(11,18,38,0.24)]">
                    <div className="mb-4 flex items-start justify-between gap-4 border-b border-white/10 pb-4">
                      <div>
                        <p className="text-sm font-black tracking-[-0.02em]">Prototype laboratory</p>
                        <p className="mt-1 max-w-md text-[11px] leading-relaxed text-slate-400">Future workflows stay outside the core product until their university data integrations are authorized and validated.</p>
                      </div>
                      <Link href="/lab" onClick={() => setLabOpen(false)} className="rounded-full border border-blue-300/20 bg-blue-300/10 px-2.5 py-1 font-mono text-[9px] font-bold text-blue-200">OPEN LAB</Link>
                    </div>
                    <div className="grid grid-cols-2 gap-x-8 gap-y-5">
                      {labModules.map(([title, items]) => (
                        <div key={title}>
                          <div className="mb-2 text-[9px] font-black uppercase tracking-[0.18em] text-slate-500">{title}</div>
                          <div className="grid gap-1">
                            {items.map(([href, label]) => (
                              <Link key={href} href={href} onClick={() => setLabOpen(false)} className="rounded-lg px-2 py-1.5 text-xs font-semibold text-slate-300 transition hover:bg-white/7 hover:text-white">{label}</Link>
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
            <Link href="/data" className="bc-focus-ring hidden items-center gap-2 rounded-xl border border-slate-950/10 bg-white/75 px-3 py-2 text-[10px] font-bold text-slate-600 shadow-sm transition hover:bg-white md:flex">
              <span className="relative flex h-2 w-2"><span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-500 opacity-40" /><span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-600" /></span>
              Source-traceable
            </Link>
            <Link href="/demo" className={`bc-focus-ring flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-black text-white shadow-[0_8px_24px_rgba(47,92,255,0.18)] transition hover:-translate-y-0.5 ${demoActive ? 'bg-blue-700' : 'bg-[#2f5cff] hover:bg-blue-700'}`}>
              <Trophy size={13} /><span className="hidden sm:inline">Jury Mode</span><Play size={10} fill="currentColor" />
            </Link>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-[1640px] gap-1 overflow-x-auto px-4 pb-2 xl:hidden sm:px-5 md:px-7">
          <Link href="/demo" className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-black ${demoActive ? 'bg-[#2f5cff] text-white' : 'border border-blue-200 bg-blue-50 text-blue-700'}`}>🏆 Jury Mode</Link>
          {primaryNav.map(link => {
            const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
            return <Link key={link.href} href={link.href} className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-bold ${active ? 'bg-[#0b1226] text-white' : 'border border-slate-950/10 bg-white/60 text-slate-600'}`}>{link.label}</Link>;
          })}
          <Link href="/lab" className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-bold ${labActive ? 'bg-[#0b1226] text-white' : 'border border-slate-950/10 bg-white/60 text-slate-600'}`}>Lab</Link>
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
