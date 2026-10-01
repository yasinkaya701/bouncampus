'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { ArrowUpRight, Database, Menu, ShieldCheck, Utensils, X } from 'lucide-react';
import { useLocale, type Locale } from '@/lib/i18n';

const primaryNav = [
  { href: '/', tr: 'Genel bakış', en: 'Overview' },
  { href: '/campus-ops', tr: 'Operasyon', en: 'Operations' },
  { href: '/campus-ops/shuttle-frequency', tr: 'Mekik planı', en: 'Shuttle plan' },
  { href: '/food-waste', tr: 'Yemek atığı', en: 'Food waste' },
  { href: '/decisions', tr: 'Kararlar', en: 'Decisions' },
  { href: '/data', tr: 'Kanıt', en: 'Evidence' },
];

const secondaryNav = [
  { href: '/buildings', tr: 'Binalar', en: 'Buildings' },
  { href: '/mobility', tr: 'Ulaşım', en: 'Mobility' },
  { href: '/courses', tr: 'Dersler', en: 'Courses' },
  { href: '/scenarios', tr: 'Senaryolar', en: 'Scenarios' },
  { href: '/lab', tr: 'Lab', en: 'Lab' },
];

function isNavActive(pathname: string, href: string) {
  if (href === '/') return pathname === '/';
  if (href === '/campus-ops') return pathname === '/campus-ops';
  return pathname === href || pathname.startsWith(`${href}/`);
}

function LocaleButton({ value, current, onClick }: { value: Locale; current: Locale; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={current === value}
      className={`bc-focus-ring rounded-md px-2 py-1 text-[10px] font-bold transition ${current === value ? 'bg-[#18372b] text-white' : 'text-[#70776f] hover:text-[#111712]'}`}
    >
      {value.toUpperCase()}
    </button>
  );
}

export default function Header() {
  const pathname = usePathname();
  const { locale, setLocale, t } = useLocale();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => setMenuOpen(false), [pathname]);

  return (
    <header className="sticky top-0 z-50 border-b border-[#111712]/10 bg-[#f4f1ea]/95 backdrop-blur-xl">
      <div className="mx-auto flex h-[68px] w-full max-w-[1440px] items-center justify-between gap-6 px-4 sm:px-6 lg:px-8">
        <div className="flex min-w-0 items-center gap-8">
          <Link href="/" className="bc-focus-ring flex shrink-0 items-center gap-3 rounded-lg" aria-label="BOUNCAMPUS home">
            <span className="relative h-9 w-9 overflow-hidden rounded-[10px] border border-[#111712]/10 bg-white">
              <Image src="/assets/bouncampus-mark.svg" alt="" fill sizes="36px" className="object-cover" priority />
            </span>
            <div className="leading-none">
              <div className="text-[13px] font-black tracking-[-0.02em] text-[#111712]">BOUNCAMPUS</div>
              <div className="mt-1 text-[8px] font-bold uppercase tracking-[0.18em] text-[#778078]">KREATE · decision system</div>
            </div>
          </Link>

          <nav className="hidden h-full items-center gap-6 lg:flex" aria-label={t('Ana navigasyon', 'Primary navigation')}>
            {primaryNav.map(link => {
              const active = isNavActive(pathname, link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`bc-focus-ring relative flex h-full items-center rounded-sm text-[11px] font-bold transition ${active ? 'text-[#111712]' : 'text-[#6d746e] hover:text-[#111712]'}`}
                >
                  {locale === 'tr' ? link.tr : link.en}
                  {active && <span className="absolute inset-x-0 bottom-0 h-[2px] bg-[#18372b]" />}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <div className="hidden items-center gap-2 text-[9px] font-bold uppercase tracking-[0.12em] text-[#617067] xl:flex">
            <span className="h-1.5 w-1.5 rounded-full bg-[#7aa15f]" />
            {t('İnsan onaylı', 'Human approved')}
          </div>
          <div className="hidden rounded-lg border border-[#111712]/10 bg-white p-0.5 sm:flex" aria-label={t('Dil seçimi', 'Language selection')}>
            <LocaleButton value="tr" current={locale} onClick={() => setLocale('tr')} />
            <LocaleButton value="en" current={locale} onClick={() => setLocale('en')} />
          </div>
          <Link
            href="/demo"
            className="bc-focus-ring hidden items-center gap-2 rounded-lg bg-[#18372b] px-3.5 py-2.5 text-[10px] font-black text-white transition hover:bg-[#244a3a] sm:flex"
          >
            {t('Jüri modu', 'Jury mode')} <ArrowUpRight size={12} />
          </Link>
          <button
            type="button"
            className="bc-focus-ring grid h-10 w-10 place-items-center rounded-lg border border-[#111712]/10 bg-white text-[#111712] lg:hidden"
            onClick={() => setMenuOpen(value => !value)}
            aria-expanded={menuOpen}
            aria-label={t('Menüyü aç/kapat', 'Toggle menu')}
          >
            {menuOpen ? <X size={17} /> : <Menu size={17} />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="border-t border-[#111712]/10 bg-[#f4f1ea] lg:hidden">
          <div className="mx-auto grid w-full max-w-[1440px] gap-5 px-4 py-5 sm:px-6">
            <nav className="grid grid-cols-2 gap-2" aria-label={t('Mobil navigasyon', 'Mobile navigation')}>
              {primaryNav.map(link => {
                const active = isNavActive(pathname, link.href);
                return (
                  <Link key={link.href} href={link.href} className={`rounded-lg border px-3 py-3 text-[11px] font-bold ${active ? 'border-[#18372b] bg-[#18372b] text-white' : 'border-[#111712]/10 bg-white text-[#4f5751]'}`}>
                    {locale === 'tr' ? link.tr : link.en}
                  </Link>
                );
              })}
            </nav>
            <div className="border-t border-[#111712]/10 pt-4">
              <div className="mb-2 text-[9px] font-black uppercase tracking-[0.16em] text-[#858b85]">{t('Diğer modüller', 'Other modules')}</div>
              <div className="flex flex-wrap gap-x-4 gap-y-2">
                {secondaryNav.map(link => (
                  <Link key={link.href} href={link.href} className="text-[10px] font-bold text-[#616961] hover:text-[#111712]">
                    {locale === 'tr' ? link.tr : link.en}
                  </Link>
                ))}
              </div>
            </div>
            <div className="flex items-center justify-between gap-3 border-t border-[#111712]/10 pt-4">
              <div className="flex items-center gap-2 text-[9px] font-bold text-[#5f685f]"><ShieldCheck size={12} /> {t('Kaynak ve model ayrımı görünür', 'Source/model boundary visible')}</div>
              <div className="flex rounded-lg border border-[#111712]/10 bg-white p-0.5">
                <LocaleButton value="tr" current={locale} onClick={() => setLocale('tr')} />
                <LocaleButton value="en" current={locale} onClick={() => setLocale('en')} />
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="hidden border-t border-[#111712]/[0.06] bg-white/35 2xl:block">
        <div className="mx-auto flex h-8 w-full max-w-[1440px] items-center gap-5 px-8 text-[9px] font-bold text-[#777e78]">
          <span className="flex items-center gap-1.5"><Utensils size={10} /> {t('Odak: yemek atığını önlemek', 'Focus: prevent food waste')}</span>
          <span className="h-3 w-px bg-[#111712]/10" />
          <span className="flex items-center gap-1.5"><Database size={10} /> {t('Kamu verisi + model tahmini', 'Public data + model estimate')}</span>
        </div>
      </div>
    </header>
  );
}
