'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  CloudSun,
  Database,
  ExternalLink,
  ShieldCheck,
  Utensils,
} from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import {
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  YEAR_OVER_YEAR_REDUCTION_PCT,
} from '@/lib/food-waste';

export default function DashboardPage() {
  const { locale, t } = useLocale();
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard().then(setData).catch(() => setData(null));
  }, []);

  const numberLocale = locale === 'tr' ? 'tr-TR' : 'en-US';
  const foodModel = data?.food_demand_meals && data.food_demand_meals > 0 ? Math.round(data.food_demand_meals) : null;
  const weather = data?.live_weather?.temperature;
  const courses = data?.real_courses_loaded ?? 0;
  const officialLive = data?.data_quality?.official_live_sources ?? 0;
  const sourceCount = data?.sources?.length ?? 0;
  const qualityMode = data?.data_quality?.mode ?? 'CHECKING';

  return (
    <div className="space-y-12 sm:space-y-16">
      <section className="border-b border-[#111712]/10 pb-10 sm:pb-14">
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1.08fr)_minmax(360px,.92fr)] lg:gap-14">
          <div className="flex min-h-[470px] flex-col justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#657067]">
                <span>BOUNCAMPUS / KREATE</span>
                <span className="h-px w-7 bg-[#111712]/20" />
                <span>{t('Yemek atığı karar zekâsı', 'Food-waste decision intelligence')}</span>
              </div>

              <h1 className="mt-7 max-w-4xl text-[48px] font-black leading-[0.94] tracking-[-0.065em] text-[#111712] sm:text-[68px] lg:text-[78px]">
                {t('Bir sonraki öğünde ne kadar üretileceğine daha iyi karar ver.', 'Make a better decision about how much to produce for the next meal.')}
              </h1>

              <p className="mt-7 max-w-2xl text-[13px] leading-6 text-[#626a63] sm:text-[14px]">
                {t(
                  'BOUNCAMPUS, Boğaziçi’nin yayımlanmış yemek atığı verisini talep bağlamı ve model tahminiyle bir araya getirir. Sistem karar vermez; mutfak sorumlusuna kaynakları, belirsizliği ve güvenli üretim bandını aynı anda gösterir.',
                  'BOUNCAMPUS combines Boğaziçi’s published food-waste evidence with demand context and model estimates. It does not make the decision; it gives the kitchen operator the sources, uncertainty and a safe production band in one place.',
                )}
              </p>

              <div className="mt-7 flex flex-wrap gap-2.5">
                <Link href="/food-waste" className="bc-button-primary">
                  <Utensils size={13} /> {t('Karar workbench’ini aç', 'Open decision workbench')} <ArrowRight size={12} />
                </Link>
                <Link href="/data" className="bc-button-secondary">
                  <Database size={12} /> {t('Kanıtı incele', 'Inspect evidence')}
                </Link>
              </div>
            </div>

            <div className="mt-10 flex flex-wrap items-center gap-x-5 gap-y-2 border-t border-[#111712]/10 pt-5 text-[9px] font-bold text-[#697169]">
              <span className="flex items-center gap-1.5"><ShieldCheck size={11} /> {t('İnsan onayı zorunlu', 'Human approval required')}</span>
              <span className="flex items-center gap-1.5"><CheckCircle2 size={11} /> {t('Model çıktısı açıkça etiketli', 'Model output explicitly labeled')}</span>
              <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="bc-focus-ring flex items-center gap-1.5 rounded-sm font-black text-[#315846] hover:text-[#18372b]">
                {t('Resmi kaynak', 'Official source')} <ExternalLink size={10} />
              </a>
            </div>
          </div>

          <aside className="bc-workbench self-stretch rounded-2xl">
            <div className="flex items-start justify-between gap-4 border-b border-[#111712]/10 p-5 sm:p-6">
              <div>
                <div className="bc-eyebrow">{t('Şu anki karar bağlamı', 'Current decision context')}</div>
                <h2 className="mt-2 text-[24px] font-black tracking-[-0.04em] text-[#111712]">{t('Bir sonraki öğle servisi', 'Next lunch service')}</h2>
              </div>
              <span className={`rounded-md border px-2 py-1 font-mono text-[8px] font-black ${qualityMode === 'LIVE_PUBLIC_DATA' ? 'border-[#6f8e60]/30 bg-[#edf2e7] text-[#42613a]' : 'border-[#9b7b42]/25 bg-[#f7f0df] text-[#7e6233]'}`}>
                {qualityMode === 'LIVE_PUBLIC_DATA' ? 'PUBLIC DATA ONLINE' : 'SOURCE CHECK'}
              </span>
            </div>

            <div className="p-5 sm:p-6">
              <div className="text-[9px] font-black uppercase tracking-[0.16em] text-[#7c837c]">{t('Model başlangıç noktası', 'Model starting point')}</div>
              <div className="mt-2 flex items-end gap-2">
                <span className="bc-mono text-[54px] font-black leading-none tracking-[-0.065em] text-[#111712]">
                  {foodModel ? foodModel.toLocaleString(numberLocale) : '—'}
                </span>
                <span className="pb-1 text-[11px] font-bold text-[#737a74]">{t('öğün', 'meals')}</span>
              </div>
              <div className="mt-2 text-[9px] font-bold text-[#687068]">MODEL_ESTIMATE · {t('karar değil', 'not a decision')}</div>

              <div className="mt-7 divide-y divide-[#111712]/10 border-y border-[#111712]/10">
                <SignalRow icon={CloudSun} label={t('Hava', 'Weather')} value={weather == null ? '—' : `${weather}°C`} provenance="EXTERNAL_LIVE" />
                <SignalRow icon={BookOpen} label={t('Ders bağlamı', 'Course context')} value={courses ? courses.toLocaleString(numberLocale) : '—'} provenance="OFFICIAL_SNAPSHOT" />
                <SignalRow icon={Database} label={t('Sağlıklı resmi canlı kaynak', 'Healthy official live sources')} value={officialLive ? String(officialLive) : '—'} provenance={sourceCount ? `${sourceCount} ${t('izlenen', 'tracked')}` : 'CHECKING'} />
              </div>

              <Link href="/food-waste" className="bc-focus-ring mt-5 flex items-center justify-between rounded-lg bg-[#18372b] px-4 py-3 text-[10px] font-black text-white">
                <span>{t('Bandı, sinyal kapsamını ve operatör kapısını aç', 'Open band, signal coverage and operator gate')}</span>
                <ArrowRight size={12} />
              </Link>
            </div>
          </aside>
        </div>
      </section>

      <section>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="bc-eyebrow">{t('Ölçülmüş problem', 'Measured problem')}</div>
            <h2 className="mt-2 max-w-3xl text-[34px] font-black leading-[1] tracking-[-0.055em] text-[#111712] sm:text-[44px]">
              {t('Önce baz çizgisini kabul et. Sonra yalnız pilotta kanıtlayabildiğin etkiyi sahiplen.', 'Start with the baseline. Claim only the impact you can prove in the pilot.')}
            </h2>
          </div>
          <div className="max-w-sm text-[10px] leading-5 text-[#6d746e]">
            {t('2024 ve 2025 değerleri Boğaziçi’nin yayımlanmış kampüs yemek atığı verisidir.', '2024 and 2025 figures are published Boğaziçi campus food-waste data.')}
          </div>
        </div>

        <div className="mt-7 grid border-y border-[#111712]/10 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCell label={t('2025 resmi atık', 'Official 2025 waste')} value={FOOD_WASTE_BASELINE.year2025WasteKg.toLocaleString(numberLocale)} suffix="kg" />
          <MetricCell label={t('2024 → 2025', '2024 → 2025')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}`} suffix="%" />
          <MetricCell label={t('Pilot başarı kapısı', 'Pilot success gate')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}`} suffix="%" footnote={t('hedef · sonuç değil', 'target · not result')} />
          <MetricCell label={t('Otomatik dispatch', 'Automatic dispatch')} value={t('Kapalı', 'Off')} footnote={t('insan onayı gerekli', 'human approval required')} />
        </div>
      </section>

      <section className="grid gap-8 lg:grid-cols-[.72fr_1.28fr] lg:gap-14">
        <div>
          <div className="bc-eyebrow">{t('Ürünün tek işi', 'The product’s one job')}</div>
          <h2 className="mt-2 text-[34px] font-black leading-[1] tracking-[-0.055em] text-[#111712] sm:text-[42px]">
            {t('Ölçümden karara, karardan yeniden ölçüme.', 'From measurement to decision, then back to measurement.')}
          </h2>
          <p className="mt-4 max-w-lg text-[11px] leading-6 text-[#697169]">
            {t('Kampüs zekâsı ancak kapalı bir geri besleme döngüsüyse değerlidir. Bu yüzden arayüzde harita veya “AI” gösterisi değil, kararın yaşam döngüsü öne çıkıyor.', 'Campus intelligence matters only as a closed feedback loop. That is why the interface foregrounds the life cycle of a decision instead of a map or an “AI” showcase.')}
          </p>
        </div>

        <div className="divide-y divide-[#111712]/10 border-y border-[#111712]/10">
          <LoopStep n="01" title={t('Gözle', 'Observe')} detail={t('Resmi atık geçmişi ve karar bağlamını topla.', 'Collect the official waste baseline and decision context.')} />
          <LoopStep n="02" title={t('Tahmin et', 'Forecast')} detail={t('Tek sayı yerine belirsizliği görünür bir üretim bandı üret.', 'Produce an uncertainty-visible production band, not a magic number.')} />
          <LoopStep n="03" title={t('İnsan onayı', 'Human gate')} detail={t('Operatör onaylar, düzenler veya bekletir. Sistem otomatik emir göndermez.', 'The operator approves, edits or holds. The system never auto-dispatches.')} />
          <LoopStep n="04" title={t('Ölç ve öğren', 'Measure & learn')} detail={t('Pilot sonucunu kg / 100 servis edilen öğün ile kontrol koluna karşı ölç.', 'Measure pilot outcome as kg / 100 served meals against a control arm.')} />
        </div>
      </section>

      <section className="rounded-2xl bg-[#18372b] p-6 text-white sm:p-8 lg:p-10">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,.85fr)_minmax(0,1.15fr)] lg:gap-14">
          <div>
            <div className="text-[9px] font-black uppercase tracking-[0.18em] text-[#b9da72]">{t('Güven sınırı', 'Truth boundary')}</div>
            <h2 className="mt-3 text-[34px] font-black leading-[1] tracking-[-0.05em] sm:text-[43px]">
              {t('Kaynak verisi, snapshot ve model çıktısı aynı şey değil.', 'Source data, snapshots and model output are not the same thing.')}
            </h2>
          </div>
          <div className="divide-y divide-white/12 border-y border-white/12">
            <EvidenceRow label="OFFICIAL_PUBLIC" text={t('Yayımlanmış yemek atığı baz çizgisi.', 'Published food-waste baseline.')} />
            <EvidenceRow label="OFFICIAL_SNAPSHOT" text={t('Ders programı gibi periyodik resmi bağlam.', 'Periodic official context such as the course schedule.')} />
            <EvidenceRow label="EXTERNAL_LIVE" text={t('Hava gibi kampüs dışı canlı kaynak.', 'Live external sources such as weather.')} />
            <EvidenceRow label="MODEL_ESTIMATE" text={t('Tahmin; ölçülmüş gerçek talep değil.', 'An estimate, not measured demand truth.')} />
          </div>
        </div>
      </section>
    </div>
  );
}

function SignalRow({ icon: Icon, label, value, provenance }: { icon: typeof CloudSun; label: string; value: string; provenance: string }) {
  return (
    <div className="grid grid-cols-[22px_minmax(0,1fr)_auto] items-center gap-3 py-3.5">
      <Icon size={13} className="text-[#657067]" />
      <div>
        <div className="text-[10px] font-black text-[#242b25]">{label}</div>
        <div className="mt-0.5 font-mono text-[8px] font-bold text-[#858b85]">{provenance}</div>
      </div>
      <div className="bc-mono text-[13px] font-black text-[#111712]">{value}</div>
    </div>
  );
}

function MetricCell({ label, value, suffix, footnote }: { label: string; value: string; suffix?: string; footnote?: string }) {
  return (
    <div className="border-[#111712]/10 px-0 py-5 sm:px-5 sm:first:pl-0 sm:[&:nth-child(2)]:border-l lg:[&:nth-child(3)]:border-l lg:[&:nth-child(4)]:border-l">
      <div className="bc-label">{label}</div>
      <div className="mt-2 flex items-baseline gap-1.5">
        <span className="bc-mono text-[31px] font-black tracking-[-0.05em] text-[#111712]">{value}</span>
        {suffix && <span className="text-[10px] font-black text-[#767d77]">{suffix}</span>}
      </div>
      {footnote && <div className="mt-1 text-[8px] font-bold uppercase tracking-[0.1em] text-[#878d87]">{footnote}</div>}
    </div>
  );
}

function LoopStep({ n, title, detail }: { n: string; title: string; detail: string }) {
  return (
    <div className="grid gap-3 py-5 sm:grid-cols-[50px_150px_minmax(0,1fr)] sm:items-start">
      <div className="font-mono text-[9px] font-black text-[#7b827c]">{n}</div>
      <div className="text-[14px] font-black tracking-[-0.02em] text-[#111712]">{title}</div>
      <p className="text-[10px] leading-5 text-[#687068]">{detail}</p>
    </div>
  );
}

function EvidenceRow({ label, text }: { label: string; text: string }) {
  return (
    <div className="grid gap-2 py-4 sm:grid-cols-[150px_minmax(0,1fr)] sm:items-center">
      <div className="font-mono text-[9px] font-black text-[#b9da72]">{label}</div>
      <div className="text-[10px] leading-5 text-white/62">{text}</div>
    </div>
  );
}
