import type { Metadata, Viewport } from 'next';
import './globals.css';
import './polish.css';
import AppShell from '@/components/shared/AppShell';
import { LocaleProvider } from '@/lib/i18n';
import { getSiteUrl } from '@/lib/site-url';
import 'leaflet/dist/leaflet.css';

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'BOUNCAMPUS — Campus Food-Waste Decision Intelligence',
    template: '%s · BOUNCAMPUS',
  },
  description: 'A source-traceable decision system that turns measured campus food waste into human-approved production planning and measurable pilot outcomes.',
  applicationName: 'BOUNCAMPUS',
  manifest: '/manifest.webmanifest',
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: 'tr_TR',
    url: '/',
    siteName: 'BOUNCAMPUS',
    title: 'BOUNCAMPUS — Campus Food-Waste Decision Intelligence',
    description: 'From official food-waste baseline to next-service production decision and measured pilot outcome.',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BOUNCAMPUS — Campus Food-Waste Decision Intelligence',
    description: 'From official food-waste baseline to next-service production decision and measured pilot outcome.',
  },
};

export const viewport: Viewport = {
  themeColor: '#f4f1ea',
  colorScheme: 'light',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="tr">
      <body className="min-h-screen text-[#111712]">
        <LocaleProvider>
          <a href="#main-content" className="bc-skip-link">Skip to main content</a>
          <AppShell>{children}</AppShell>
        </LocaleProvider>
      </body>
    </html>
  );
}
