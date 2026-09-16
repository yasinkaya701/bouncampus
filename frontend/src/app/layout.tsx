import type { Metadata, Viewport } from 'next';
import './globals.css';
import Header from '@/components/shared/Header';
import Footer from '@/components/shared/Footer';
import { LocaleProvider } from '@/lib/i18n';
import { getSiteUrl } from '@/lib/site-url';
import 'leaflet/dist/leaflet.css';

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'BOUNCAMPUS — Boğaziçi Campus Data',
    template: '%s · BOUNCAMPUS',
  },
  description: 'Boğaziçi University campus buildings, schedules and public operational data with visible source provenance.',
  applicationName: 'BOUNCAMPUS',
  manifest: '/manifest.webmanifest',
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: 'tr_TR',
    url: '/',
    siteName: 'BOUNCAMPUS',
    title: 'BOUNCAMPUS — Boğaziçi Campus Data',
    description: 'A source-aware view of Boğaziçi campus data.',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BOUNCAMPUS — Boğaziçi Campus Data',
    description: 'A source-aware view of Boğaziçi campus data.',
  },
};

export const viewport: Viewport = {
  themeColor: '#102a43',
  colorScheme: 'light',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="tr">
      <body className="min-h-screen text-slate-950">
        <LocaleProvider>
          <a href="#main-content" className="bc-skip-link">Skip to main content</a>
          <Header />
          <main id="main-content" className="mx-auto w-full max-w-[1520px] flex-1 px-4 pb-10 pt-7 sm:px-6 lg:px-8 lg:pt-9">
            {children}
          </main>
          <Footer />
        </LocaleProvider>
      </body>
    </html>
  );
}
