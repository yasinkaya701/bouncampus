'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  CheckCircle2,
  Database,
  ExternalLink,
  Gauge,
  Play,
  ShieldCheck,
  Sparkles,
  Utensils,
} from 'lucide-react';
import {
  CURRENT_RECOVERY_RATE_PCT,
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type FoodApi = {
  demandContext: {
    available: boolean;
    productionBand: null | {
      predictedMeals: number;
      lowerBound: number;
      upperBound: number;
      provenance: 'MODEL_ESTIMATE';
    };
  };
};

export default function DemoPage() {
  const { locale, t } = useLocale();
  const [food, setFood] = useState<FoodApi | null>(null);
  const [prevention, setPrevention] = useState(15);
  const [recovery, setRecovery] = useState(85);
  const scenario = useMemo(() => simulateFoodWasteScenario(prevention, recovery), [prevention, recovery]);

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then(setFood)
      .catch(() => setFood(null));
  }, []);

  const nf = (value: number) => Math.round(value).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US');
  const band = food?.demandContext.productionBand;

  return (
    <div className="space-y-8">
      <section className="bc-panel-dark bc-grid-bg rounded-[28px] p-6 text-white sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_.8fr] lg:items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Sparkles size={12} /> {t('KREATE jüri akışı · 90 saniye', 'KREATE jury flow · 90 seconds')}
            </div>
            <h1 className="mt-4 max-w-4xl text-[42px] font-black leading-[.98] tracking-[-0.06em] sm:text-[58px]">
              {t('48.251 kg problemi göster. Bir sonraki öğün kararına indir. Pilotla kanıtla.', 'Show the 48,251 kg problem. Turn it into the next-service decision. Prove it in a pilot.')}
            </h1>
            <p className="mt-4 max-w-3xl text-[12px] leading-6 text-white/58">
              {t(
                'Bu demo tek bir hikâye anlatır: resmi yemek atığı → talep bandı → operatör kontrollü üretim önerisi → kg/servis ile ölçülen pilot sonucu. Enerji, mobilite ve 3D kampüs yetenekleri platformun genişlemesidir; ana hikâyeyi bölmez.',
                'This demo tells one story: official food waste → demand band → operator-controlled production recommendation → pilot outcome measured in kg/service. Energy, mobility and 3D campus capabilities remain platform expansion, not competing narratives.',
              )}
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <TopMetric label={t('2025 atık', '2025 waste')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg)} kg`} />
            <TopMetric label={t('Yıllık iyileşme', 'YoY improvement')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}%`} />
            <TopMetric label={t('Mevcut geri kazanım', 'Current recovery')} value={`${CURRENT_RECOVERY_RATE_PCT.toFixed(1)}%`} />
          </div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-[.72fr_1.28fr]">
        <div className="border-t border-slate-900/10 pt-5">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-slate-400"><Database size={12} /> {t('1 · Problemi kanıtla', '1 · Prove the problem')}</div>
          <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">{t('Jürinin ilk gördüğü sayı model değil.', 'The first number the jury sees is not a model output.')}</h2>
          <p className="mt-3 text-[10px] leading-5 text-slate-500">
            {t('Boğaziçi Üniversitesi 2025 için 48.251 kg yemek atığı ve 33.430 kg İSTAÇ geri kazanımı yayımlıyor. 2024 toplamı 50.993 kg. Bu ürünün baz çizgisi doğrudan kurumun raporu.', 'Boğaziçi University publishes 48,251 kg of food waste and 33,430 kg sent to İSTAÇ recovery for 2025; the 2024 total is 50,993 kg. The product baseline comes directly from the institution.')}
          </p>
          <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-1 text-[10px] font-black text-[#173f67]">
            {t('Resmi kaynağı aç', 'Open official source')} <ExternalLink size={10} />
          </a>
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          <ProofCard label={t('2025 toplam atık', '2025 total waste')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg)} kg`} provenance="OFFICIAL_PUBLIC" />
          <ProofCard label={t('İSTAÇ geri kazanımı', 'İSTAÇ recovery')} value={`${nf(FOOD_WASTE_BASELINE.year2025RecoveredKg)} kg`} provenance="OFFICIAL_PUBLIC" />
          <ProofCard label={t('Mevcut artık yük', 'Current residual load')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg - FOOD_WASTE_BASELINE.year2025RecoveredKg)} kg`} provenance="DERIVED_FROM_OFFICIAL" />
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-[.72fr_1.28fr]">
        <div className="border-t border-slate-900/10 pt-5">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-slate-400"><Gauge size={12} /> {t('2 · Bir sonraki servisi tahmin et', '2 · Forecast the next service')}</div>
          <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">{t('Tek sayı yerine güvenli üretim bandı.', 'A safe production band instead of a magic number.')}</h2>
          <p className="mt-3 text-[10px] leading-5 text-slate-500">
            {t('Ders programı, akademik takvim, hava ve menü bağlamı bir sonraki servis talebini tahmin eder. Bu POS ya da gerçek üretim telemetrisi değildir; mutfak sorumlusuna karar desteğidir.', 'Schedules, academic calendar, weather and menu context estimate demand for the next service. This is not POS or production telemetry; it is decision support for the kitchen operator.')}
          </p>
        </div>

        <div className="rounded-[22px] border border-slate-900/10 bg-white p-5">
          {band ? (
            <>
              <div className="grid grid-cols-3 gap-3">
                <BandMetric label={t('Talep tahmini', 'Demand forecast')} value={nf(band.predictedMeals)} />
                <BandMetric label={t('Alt bant', 'Lower band')} value={nf(band.lowerBound)} />
                <BandMetric label={t('Üst bant', 'Upper band')} value={nf(band.upperBound)} />
              </div>
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-[9px] leading-4 text-amber-900"><strong>MODEL_ESTIMATE.</strong> {t('Pilot ölçümü olmadan “tasarruf ettik” demiyoruz.', 'We do not claim savings without pilot measurements.')}</div>
            </>
          ) : (
            <div className="grid min-h-[150px] place-items-center text-center text-[10px] leading-5 text-slate-400">
              {t('Talep bağlamı yoksa sistem sayı uydurmaz; resmi atık baz çizgisi görünür kalır ve öneri bekletilir.', 'If demand context is unavailable, the system does not invent a number; the official baseline remains visible and the recommendation is withheld.')}
            </div>
          )}
        </div>
      </section>

      <section className="bc-panel-dark rounded-[26px] p-6 text-white sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[.72fr_1.28fr]">
          <div>
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-[#b8e467]"><Play size={11} /> {t('3 · Kararı stres-test et', '3 · Stress-test the decision')}</div>
            <h2 className="mt-3 text-[30px] font-black tracking-[-0.05em]">{t('Önleme hedefini değiştir; yıllık sonucu saniyede gör.', 'Change the prevention target; see the annual outcome instantly.')}</h2>
            <p className="mt-3 text-[10px] leading-5 text-white/52">{t('Bu sonuç 2025 resmi baz çizgisine uygulanan senaryodur. Pilot sonucu değildir.', 'This outcome is a scenario applied to the official 2025 baseline. It is not a pilot result.')}</p>
            <DemoSlider label={t('Üretimde önleme hedefi', 'Prevention at production')} value={prevention} min={0} max={30} onChange={setPrevention} />
            <DemoSlider label={t('Geri kazanım hedefi', 'Recovery target')} value={recovery} min={Math.round(CURRENT_RECOVERY_RATE_PCT)} max={95} onChange={setRecovery} />
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <ScenarioMetric label={t('Kaynağında önlenen', 'Prevented at source')} value={`${nf(scenario.preventedKg)} kg`} />
            <ScenarioMetric label={t('Kalan toplam atık', 'Remaining waste')} value={`${nf(scenario.remainingWasteKg)} kg`} />
            <ScenarioMetric label={t('Geri kazanıma yönlenen', 'Directed to recovery')} value={`${nf(scenario.recoveredKg)} kg`} />
            <ScenarioMetric label={t('Artık yük', 'Residual load')} value={`${nf(scenario.residualKg)} kg`} />
          </div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-[.72fr_1.28fr]">
        <div className="border-t border-slate-900/10 pt-5">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-slate-400"><ShieldCheck size={12} /> {t('4 · Pilotta kanıtla', '4 · Prove it in the pilot')}</div>
          <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">{t('Başarı metriği: kg/servis.', 'Success metric: kg/service.')}</h2>
          <p className="mt-3 text-[10px] leading-5 text-slate-500">{t('14 günlük A/B pilotta bir kontrol ve bir müdahale servisi seçilir. Her servis sonunda dört veri tutulur; model, sonuçla yeniden kalibre edilir.', 'A 14-day A/B pilot uses one control and one intervention service. Four values are recorded after each service; the model is recalibrated from the outcome.')}</p>
        </div>
        <div className="grid gap-2 sm:grid-cols-4">
          {[t('Üretilen porsiyon', 'Portions produced'), t('Servis edilen porsiyon', 'Portions served'), t('Yenilebilir fazla', 'Edible surplus'), t('Atık kg', 'Waste kg')].map((item, index) => (
            <div key={item} className="rounded-xl border border-slate-900/10 bg-white p-4">
              <div className="font-mono text-[8px] font-black text-emerald-700">0{index + 1}</div>
              <div className="mt-5 text-[9px] font-black text-slate-800">{item}</div>
              <CheckCircle2 size={12} className="mt-2 text-slate-300" />
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-[24px] border border-emerald-900/10 bg-emerald-50/70 p-5 sm:p-6">
        <div className="flex items-start gap-3">
          <Utensils size={18} className="mt-0.5 shrink-0 text-emerald-700" />
          <div>
            <div className="text-[10px] font-black uppercase tracking-[0.14em] text-emerald-800">{t('Kapanış cümlesi', 'Closing line')}</div>
            <p className="mt-2 max-w-5xl text-[18px] font-black leading-7 tracking-[-0.03em] text-slate-950">
              {t('“48 tonluk problemi zaten biliyoruz. BOUNCAMPUS’ın farkı, raporlamak yerine bir sonraki öğünde önlemek ve sonucu ölçmek.”', '“The 48-ton problem is already known. BOUNCAMPUS moves from reporting it to preventing the next kilogram and measuring the result.”')}
            </p>
            <Link href="/food-waste" className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-black text-[#173f67]">{t('Tam ürün çalışma alanını aç', 'Open the full product workspace')} <ArrowRight size={10} /></Link>
          </div>
        </div>
      </section>
    </div>
  );
}

function TopMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-white/10 bg-white/[0.06] p-3"><div className="text-[7px] font-black uppercase tracking-[0.1em] text-white/40">{label}</div><div className="mt-2 font-mono text-[17px] font-black">{value}</div></div>;
}

function ProofCard({ label, value, provenance }: { label: string; value: string; provenance: string }) {
  return <div className="rounded-[20px] border border-slate-900/10 bg-white p-5"><div className="text-[8px] font-black uppercase tracking-[0.11em] text-slate-400">{label}</div><div className="mt-4 font-mono text-[27px] font-black tracking-[-0.05em] text-slate-950">{value}</div><div className="mt-3 text-[7px] font-black uppercase tracking-[0.1em] text-emerald-700">{provenance}</div></div>;
}

function BandMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl bg-[#f6f8f5] p-3"><div className="text-[8px] font-black uppercase tracking-[0.1em] text-slate-400">{label}</div><div className="mt-2 font-mono text-xl font-black text-slate-950">{value}</div></div>;
}

function DemoSlider({ label, value, min, max, onChange }: { label: string; value: number; min: number; max: number; onChange: (value: number) => void }) {
  return <label className="mt-6 block"><div className="flex items-center justify-between gap-3 text-[9px] font-black uppercase tracking-[0.1em] text-white/55"><span>{label}</span><span className="font-mono text-[#b8e467]">{value}%</span></div><input className="mt-3 w-full accent-[#b8e467]" type="range" min={min} max={max} value={value} onChange={event => onChange(Number(event.target.value))} /></label>;
}

function ScenarioMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-2xl border border-white/10 bg-white/[0.06] p-5"><div className="text-[8px] font-black uppercase tracking-[0.11em] text-white/42">{label}</div><div className="mt-3 font-mono text-[28px] font-black tracking-[-0.05em]">{value}</div></div>;
}
