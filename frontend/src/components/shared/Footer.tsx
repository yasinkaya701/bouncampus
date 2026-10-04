'use client';

import Link from 'next/link';
import { ArrowUpRight, ShieldCheck } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

const links = [
  { href: '/buildings', tr: 'Binalar', en: 'Buildings' },
  { href: '/mobility', tr: 'Ulaşım', en: 'Mobility' },
  { href: '/courses', tr: 'Dersler', en: 'Courses' },
  { href: '/scenarios', tr: 'Senaryolar', en: 'Scenarios' },
  { href: '/lab', tr: 'Lab', en: 'Lab' },
];

export default function Footer() {
  const { locale, t } = useLocale();

  return (
    <footer className="mt-10 border-t border-[#111712]/10 bg-[#ece8de]">
      <div className="mx-auto w-full max-w-[1440px] px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
          <div className="max-w-2xl">
            <div className="flex items-center gap-3">
              <span className="grid h-9 w-9 place-items-center rounded-lg bg-[#18372b] text-[9px] font-black tracking-[0.08em] text-white">BC</span>
              <div>
                <div className="text-[13px] font-black tracking-[-0.02em] text-[#111712]">BOUNCAMPUS</div>
                <div className="mt-0.5 text-[8px] font-bold uppercase tracking-[0.16em] text-[#777e78]">Campus decision intelligence</div>
              </div>
            </div>
            <p className="mt-4 max-w-xl text-[10px] leading-5 text-[#626a63]">
              {t(
                'Kamuya açık kampüs verisini model çıktısından ayırır; üniversite sensörü, POS, BMS veya geçiş sistemi entegre değilse varmış gibi göstermez. Amaç daha fazla dashboard değil, ölçülebilir ve insan onaylı daha iyi karar üretmektir.',
                'Keeps public campus evidence separate from model output; university sensors, POS, BMS or access-control systems are never implied unless actually integrated. The goal is not more dashboards, but measurable, human-approved decisions.',
              )}
            </p>
            <div className="mt-4 inline-flex items-center gap-2 text-[9px] font-bold text-[#365849]"><ShieldCheck size={11} /> {t('Şeffaf provenans · insan kapısı', 'Transparent provenance · human gate')}</div>
          </div>

          <div className="lg:text-right">
            <div className="flex flex-wrap gap-x-4 gap-y-2 lg:justify-end">
              {links.map(link => (
                <Link key={link.href} href={link.href} className="text-[10px] font-bold text-[#687069] transition hover:text-[#111712]">
                  {locale === 'tr' ? link.tr : link.en}
                </Link>
              ))}
            </div>
            <Link href="/demo" className="bc-focus-ring mt-5 inline-flex items-center gap-2 rounded-lg border border-[#111712]/15 bg-white px-3.5 py-2.5 text-[10px] font-black text-[#111712] transition hover:border-[#18372b]">
              {t('90 saniyelik jüri akışı', '90-second jury flow')} <ArrowUpRight size={11} />
            </Link>
          </div>
        </div>

        <div className="mt-8 flex flex-col gap-2 border-t border-[#111712]/10 pt-4 text-[8px] font-bold uppercase tracking-[0.12em] text-[#858b85] sm:flex-row sm:items-center sm:justify-between">
          <span>Boğaziçi University · KREATE for Climate</span>
          <span>{t('Pilot hedefleri sonuç iddiası değildir', 'Pilot targets are not achieved-result claims')}</span>
        </div>
      </div>
    </footer>
  );
}
