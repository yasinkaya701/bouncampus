import type { Metadata, Viewport } from 'next';
import Link from 'next/link';
import './globals.css';
import Header from '@/components/shared/Header';
import CampusAICopilot from '@/components/AI/CampusAICopilot';
import { getSiteUrl } from '@/lib/site-url';
import 'leaflet/dist/leaflet.css';

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'BOUNCAMPUS — Mission Control for Boğaziçi',
    template: '%s · BOUNCAMPUS',
  },
  description: 'A source-traceable decision layer that turns Boğaziçi public data into operational missions, counterfactuals, human approvals and calibration evidence.',
  applicationName: 'BOUNCAMPUS Mission Control',
  manifest: '/manifest.webmanifest',
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: 'tr_TR',
    url: '/',
    siteName: 'BOUNCAMPUS',
    title: 'BOUNCAMPUS — Campus Mission Control',
    description: 'The decision layer between campus data and real operations.',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BOUNCAMPUS — Campus Mission Control',
    description: 'The decision layer between campus data and real operations.',
  },
  appleWebApp: {
    capable: true,
    title: 'BOUNCAMPUS',
    statusBarStyle: 'black-translucent',
  },
};

export const viewport: Viewport = {
  themeColor: '#0b1226',
  colorScheme: 'light',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="tr">
      <body className="min-h-screen text-[#0a1020]">
        <a href="#main-content" className="bc-skip-link">Skip to main content</a>
        <Header />
        <main id="main-content" className="mx-auto w-full max-w-[1640px] flex-1 px-3 pb-16 pt-4 sm:px-5 md:px-7 lg:px-9 lg:pt-6">
          {children}
        </main>
        <CampusAICopilot />
        <footer className="border-t border-slate-900/10 bg-[#eef0ec]/75">
          <div className="mx-auto w-full max-w-[1640px] px-5 py-8 md:px-7 lg:px-9">
            <div className="grid gap-7 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
              <div className="max-w-xl text-xs text-slate-500">
                <div className="mb-1.5 flex items-center gap-2 text-slate-900">
                  <span className="font-black tracking-[-0.02em]">BOUNCAMPUS</span>
                  <span className="rounded-full border border-slate-900/10 bg-white px-2 py-0.5 font-mono text-[9px] font-bold text-slate-500">MISSION CONTROL</span>
                </div>
                <p className="leading-relaxed">Boğaziçi public kaynaklarını doğrulanabilir operasyon görevlerine çeviren insan-onaylı karar katmanı. Üniversite BMS, POS, Wi-Fi occupancy veya geçiş sistemlerine bağlı değildir.</p>
              </div>

              <div className="flex flex-wrap gap-x-5 gap-y-2 text-[10px] font-black text-slate-500">
                <Link href="/demo" className="transition hover:text-slate-900">Jury Mode</Link>
                <Link href="/decisions" className="transition hover:text-slate-900">Decisions</Link>
                <Link href="/scenarios" className="transition hover:text-slate-900">Simulate</Link>
                <Link href="/data" className="transition hover:text-slate-900">Data Trust</Link>
                <Link href="/lab" className="transition hover:text-slate-900">Prototype Lab</Link>
              </div>
            </div>

            <div className="mt-6 flex flex-col gap-2 border-t border-slate-900/8 pt-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-[9px] uppercase tracking-[0.08em] text-slate-400">
                <span>SKS</span><span>Mekik</span><span>Akademik Takvim</span><span>BUIS/ÖBİKAS Snapshot</span>
              </div>
              <span className="font-mono text-[9px] uppercase tracking-[0.08em] text-slate-400">© {new Date().getFullYear()} BOUNCAMPUS</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
