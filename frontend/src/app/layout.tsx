import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/shared/Header";
import CampusAICopilot from "@/components/AI/CampusAICopilot";
import 'leaflet/dist/leaflet.css';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BOUNCAMPUS | Boğaziçi Üniversitesi Dijital İkiz & Karar Destek",
  description: "Boğaziçi Üniversitesi Otonom Kampüs Sürdürülebilirlik & Dijital İkiz Platformu",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body className={`${inter.className} flex flex-col min-h-screen bg-slate-50 text-slate-900`}>
        <Header />
        <main className="flex-grow container mx-auto px-4 py-6">
          {children}
        </main>
        <CampusAICopilot />
        <footer className="bg-slate-900 border-t border-slate-800 text-slate-400 py-6 mt-auto">
          <div className="container mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <span className="font-bold text-white tracking-wide">BOĞAZİÇİ ÜNİVERSİTESİ</span>
              <span>•</span>
              <span>Kampüs Dijital İkizi & Otonom Karar Destek Platformu</span>
            </div>
            <div className="flex items-center gap-3 text-slate-400 font-mono text-[11px]">
              <span>OBIKAS Canlı API</span>
              <span>•</span>
              <span>ISO 14064 Karbon Uyumlu</span>
              <span>•</span>
              <span>© {new Date().getFullYear()}</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
