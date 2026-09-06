import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/shared/Header";
import CampusAICopilot from "@/components/AI/CampusAICopilot";
import 'leaflet/dist/leaflet.css';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BOUNCAMPUS | Sustainability Dashboard",
  description: "Campus sustainability dashboard for Boğaziçi University",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          {children}
        </main>
        <CampusAICopilot />
        <footer className="bg-primary-medium text-white text-center py-4 mt-auto">
          <p className="text-sm">Boğaziçi University Campus Sustainability Platform © {new Date().getFullYear()}</p>
        </footer>
      </body>
    </html>
  );
}
