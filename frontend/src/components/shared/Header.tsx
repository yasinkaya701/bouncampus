'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BookOpen, Building2, CheckSquare2, Compass, Database, FlaskConical, LayoutDashboard, Trophy } from 'lucide-react';
import { useLocale, type Locale } from '@/lib/i18n';

const EXPERIMENTAL_PREFIXES = [
  '/flow', '/microgrid', '/control-room', '/anomalies', '/rescheduler', '/agent-simulation',
  '/student', '/solar', '/maintenance', '/acoustic', '/iot-registry', '/integrations',
  '/esg-reports', '/food-waste', '/water', '/transit', '/league',
];

const primaryNav = [
  { href: '/', tr: 'Genel bakış', en: 'Overview', icon: LayoutDashboard },
  { href: '/buildings', tr: 'Binalar', en: 'Buildings', icon: Building2 },
  { href: '/courses', tr: 'Dersler', en: 'Courses', icon: BookOpen },
  { href: '/decisions', tr: 'Kararlar', en: 'Decisions', icon: CheckSquare2 },
  { href: '/scenarios', tr: 'Senaryolar', en: 'Scenarios', icon: Compass },
  { href: '/data', tr: 'Kaynaklar', en: 'Sources', icon: Database },
];

function LocaleButton({ value, current, onClick }: { value: Locale; current: Locale; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={current === value}
      className={`rounded-md px-2.5 py-1.5 text-[10px] font-black transition ${current === value ? 'bg-slate-900 text-white' : 'text-slate-500 hover:text-slate-900'}`}
    >
      {value.toUpperCase()}
    </button>
  );
}

export default function Header() {
  const pathname = usePathname();
  const { locale, setLocale, t } = useLocale();
  const isExperimentalRoute = EXPERIMENTAL_PREFIXES.some(prefix => pathname.startsWith(prefix));
  const labActive = pathname === '/lab' || isExperimentalRoute;

  return (
    <>
      <header className="sticky top-0 z-50 border-b border-slate-900/10 bg-[#f6f6f1]/95 backdrop-blur-lg">
        <div className="mx-auto flex min-h-[66px] w-full max-w-[1520px] items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-8">
            <Link href="/" className="bc-focus-ring flex shrink-0 items-center gap-2.5 rounded-lg">
              <span className="grid h-9 w-9 place-items-center rounded-lg bg-[#102a43] text-[10px] font-black tracking-[0.08em] text-white">BC</span>
              <div className="hidden sm:block">
                <div className="text-[14px] font-black tracking-[-0.035em] text-slate-950">BOUNCAMPUS</div>
                <div className="text-[9px] font-semibold tracking-[0.02em] text-slate-400">BOĞAZİÇİ UNIVERSITY</div>
              </div>
            </Link>

            <nav className="hidden items-center gap-0.5 xl:flex">
              {primaryNav.map(link => {
                const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
                const Icon = link.icon;
                return (
                  <Link key={link.href} href={link.href} className={`bc-focus-ring flex items-center gap-1.5 rounded-lg px-2.5 py-2 text-[11px] font-semibold transition ${active ? 'bg-white text-slate-950 ring-1 ring-slate-900/10' : 'text-slate-500 hover:text-slate-950'}`}>
                    <Icon size={12} /> {locale === 'tr' ? link.tr : link.en}
                  </Link>
                );
              })}
              <Link href="/lab" className={`bc-focus-ring ml-1 flex items-center gap-1.5 rounded-lg px-2.5 py-2 text-[11px] font-semibold transition ${labActive ? 'bg-white text-slate-950 ring-1 ring-slate-900/10' : 'text-slate-500 hover:text-slate-950'}`}>
                <FlaskConical size={12} /> {t('Deneyler', 'Lab')}
              </Link>
            </nav>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <div className="flex rounded-lg border border-slate-900/10 bg-white p-0.5" aria-label={t('Dil seçimi', 'Language selection')}>
              <LocaleButton value="tr" current={locale} onClick={() => setLocale('tr')} />
              <LocaleButton value="en" current={locale} onClick={() => setLocale('en')} />
            </div>
            <Link href="/demo" className="bc-focus-ring hidden items-center gap-1.5 rounded-lg bg-[#102a43] px-3 py-2 text-[11px] font-bold text-white transition hover:bg-[#173f67] sm:flex">
              <Trophy size={12} /> {t('Demo', 'Demo')}
            </Link>
          </div>
        </div>

        <div className="mx-auto flex w-full max-w-[1520px] gap-1 overflow-x-auto px-4 pb-2 xl:hidden sm:px-6 lg:px-8">
          {primaryNav.map(link => {
            const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
            return (
              <Link key={link.href} href={link.href} className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-bold ${active ? 'bg-[#102a43] text-white' : 'border border-slate-900/10 bg-white text-slate-600'}`}>
                {locale === 'tr' ? link.tr : link.en}
              </Link>
            );
          })}
          <Link href="/lab" className={`whitespace-nowrap rounded-full px-3 py-1.5 text-[10px] font-bold ${labActive ? 'bg-[#102a43] text-white' : 'border border-slate-900/10 bg-white text-slate-600'}`}>{t('Deneyler', 'Lab')}</Link>
        </div>
      </header>

      {isExperimentalRoute && (
        <div className="border-b border-amber-300/50 bg-amber-50">
          <div className="mx-auto flex w-full max-w-[1520px] items-start gap-2 px-4 py-2 text-[10px] leading-relaxed text-amber-950 sm:px-6 lg:px-8">
            <FlaskConical size={13} className="mt-0.5 shrink-0" />
            <strong className="shrink-0 font-black">{t('DENEYSEL MODÜL', 'EXPERIMENTAL MODULE')}</strong>
            <span className="text-amber-900/75">{t('Bu sayfadaki sensör veya otomasyon değerleri gerçek üniversite telemetrisi olarak kabul edilmemelidir.', 'Sensor or automation values on this page must not be treated as connected university telemetry.')}</span>
          </div>
        </div>
      )}
    </>
  );
}
