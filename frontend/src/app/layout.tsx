import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/shared/Header';
import CampusAICopilot from '@/components/AI/CampusAICopilot';
import 'leaflet/dist/leaflet.css';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export const metadata: Metadata = {
  title: 'BOUNCAMPUS — Campus Intelligence for Boğaziçi',
  description: 'Boğaziçi public data feeds, transparent forecasting models and operational sustainability decisions in one campus intelligence product.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="tr">
      <body className={`${inter.className} min-h-screen text-[#0a1020]`}>
        <Header />
        <main className="mx-auto w-full max-w-[1640px] flex-1 px-3 pb-16 pt-4 sm:px-5 md:px-7 lg:px-9 lg:pt-6">
          {children}
        </main>
        <CampusAICopilot />
        <footer className="border-t border-slate-900/10 bg-[#eef0ec]/75">
          <div className="mx-auto flex w-full max-w-[1640px] flex-col gap-4 px-5 py-8 text-xs text-slate-500 sm:flex-row sm:items-end sm:justify-between md:px-7 lg:px-9">
            <div className="max-w-xl">
              <div className="mb-1.5 flex items-center gap-2 text-slate-900">
                <span className="font-black tracking-[-0.02em]">BOUNCAMPUS</span>
                <span className="rounded-full border border-slate-900/10 bg-white px-2 py-0.5 font-mono text-[9px] font-bold text-slate-500">HACKATHON BUILD</span>
              </div>
              <p className="leading-relaxed">
                Boğaziçi Üniversitesi public kaynakları ve açıkça etiketlenmiş karar modelleri. Üniversite BMS, POS veya geçiş sistemlerine bağlı değildir.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-[10px] uppercase tracking-[0.08em] text-slate-500">
              <span>SKS</span>
              <span>Mekik</span>
              <span>Akademik Takvim</span>
              <span>BUIS/ÖBİKAS Snapshot</span>
              <span>© {new Date().getFullYear()}</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
