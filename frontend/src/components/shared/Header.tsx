'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Building2, BusFront, CheckSquare2, Compass, Database, LayoutDashboard, Trophy } from 'lucide-react';
import { useLocale, type Locale } from '@/lib/i18n';

const primaryNav = [
  { href: '/', tr: 'Kontrol merkezi', en: 'Command center', icon: LayoutDashboard },
  { href: '/buildings', tr: 'Binalar', en: 'Buildings', icon: Building2 },
  { href: '/mobility', tr: 'Mekik', en: 'Shuttle', icon: BusFront },
  { href: '/decisions', tr: 'Kararlar', en: 'Decisions', icon: CheckSquare2 },
  { href: '/scenarios', tr: 'Senaryolar', en: 'Scenarios', icon: Compass },
  { href: '/data', tr: 'Kanıt', en: 'Evidence', icon: Database },
];

function LocaleButton({ value, current, onClick }: { value: Locale; current: Locale; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={current === value}
      className={`rounded-lg px-2.5 py-1.5 text-[9px] font-black tracking-[0.06em] transition ${current === value ? 'bg-[#071c33] text-white shadow-sm' : 'text-slate-400 hover:text-slate-900'}`}
    >
      {value.toUpperCase()}
    </button>
  );
}

export default function Header() {
  const pathname = usePathname();
  const { locale, setLocale, t } = useLocale();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-950/[0.07] bg-[#f8faf7]/82 backdrop-blur-2xl supports-[backdrop-filter]:bg-[#f8faf7]/72">
      <div className="mx-auto flex min-h-[72px] w-full max-w-[1520px] items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <div className="flex min-w-0 items-center gap-7">
          <Link href="/" className="bc-focus-ring group flex shrink-0 items-center gap-3 rounded-xl">
            <span className="relative h-10 w-10 overflow-hidden rounded-[13px] shadow-[0_10px_24px_rgba(7,28,51,.16)] ring-1 ring-slate-950/[0.06] transition duration-300 group-hover:-translate-y-0.5 group-hover:shadow-[0_14px_32px_rgba(7,28,51,.22)]">
              <Image src="/assets/bouncampus-mark.svg" alt="" fill sizes="40px" className="object-cover" priority />
            </span>
            <div className="hidden sm:block">
              <div className="flex items-center gap-2">
                <div className="text-[14px] font-black tracking-[-0.04em] text-slate-950">BOUNCAMPUS</div>
                <span className="rounded-full border border-emerald-900/10 bg-emerald-50 px-1.5 py-0.5 text-[7px] font-black uppercase tracking-[0.12em] text-emerald-700">KREATE</span>
              </div>
              <div className="mt-0.5 text-[8px] font-bold uppercase tracking-[0.16em] text-slate-400">Campus climate intelligence</div>
            </div>
          </Link>

          <nav className="hidden items-center rounded-xl border border-slate-950/[0.07] bg-white/70 p-1 shadow-[0_8px_24px_rgba(7,17,31,.035)] xl:flex">
            {primaryNav.map(link => {
              const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`bc-focus-ring flex items-center gap-1.5 rounded-lg px-3 py-2 text-[10px] font-bold transition ${active ? 'bg-[#071c33] text-white shadow-sm' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-950'}`}
                >
                  <Icon size={12} strokeWidth={2.2} /> {locale === 'tr' ? link.tr : link.en}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <div className="hidden items-center gap-2 rounded-full border border-emerald-900/10 bg-emerald-50/80 px-3 py-2 text-[9px] font-black text-emerald-800 lg:flex">
            <span className="bc-live-dot h-1.5 w-1.5 rounded-full bg-emerald-500" />
            {t('Karar motoru aktif', 'Decision engine active')}
          </div>
          <div className="flex rounded-xl border border-slate-950/[0.08] bg-white/80 p-0.5 shadow-sm" aria-label={t('Dil seçimi', 'Language selection')}>
            <LocaleButton value="tr" current={locale} onClick={() => setLocale('tr')} />
            <LocaleButton value="en" current={locale} onClick={() => setLocale('en')} />
          </div>
          <Link href="/demo" className="bc-focus-ring hidden items-center gap-1.5 rounded-xl bg-[#071c33] px-3.5 py-2.5 text-[10px] font-black text-white shadow-[0_10px_24px_rgba(7,28,51,.14)] transition hover:-translate-y-0.5 hover:bg-[#0b3153] sm:flex">
            <Trophy size={12} /> {t('Jüri modu', 'Jury mode')}
          </Link>
        </div>
      </div>

      <div className="mx-auto flex w-full max-w-[1520px] gap-1.5 overflow-x-auto px-4 pb-2.5 xl:hidden sm:px-6 lg:px-8">
        {primaryNav.map(link => {
          const active = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
          const Icon = link.icon;
          return (
            <Link key={link.href} href={link.href} className={`flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-full px-3 py-1.5 text-[9px] font-black ${active ? 'bg-[#071c33] text-white' : 'border border-slate-950/[0.08] bg-white/80 text-slate-500'}`}>
              <Icon size={10} /> {locale === 'tr' ? link.tr : link.en}
            </Link>
          );
        })}
      </div>
    </header>
  );
}
