'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Database,
  ExternalLink,
  Gauge,
  Leaf,
  Scale,
  ShieldCheck,
  Sparkles,
  Utensils,
} from 'lucide-react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  CURRENT_RECOVERY_RATE_PCT,
  FOOD_WASTE_2025,
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type DemandContext = {
  available: boolean;
  productionBand: null | {
    predictedMeals: number;
    lowerBound: number;
    upperBound: number;
    provenance: 'MODEL_ESTIMATE';
  };
};

const formatKg = (value: number, locale: 'tr' | 'en') =>
  `${Math.round(value).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} kg`;

export default function FoodWastePage() {
  const { locale, t } = useLocale();
  const [preventionRate, setPreventionRate] = useState(15);
  const [recoveryRate, setRecoveryRate] = useState(85);
  const [demand, setDemand] = useState<DemandContext | null>(null);

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then(payload => setDemand(payload?.demandContext ?? null))
      .catch(() => setDemand(null));
  }, []);

  const scenario = useMemo(
    () => simulateFoodWasteScenario(preventionRate, recoveryRate),
    [preventionRate, recoveryRate],
  );

  const monthlyChart = useMemo(
    () => FOOD_WASTE_2025.map(item => ({
      month: locale === 'tr' ? item.monthTr : item.month,
      wasteKg: item.wasteKg,
    })),
    [locale],
  );

  return (
    <div className="space-y-8 sm:space-y-10">
      <section className="bc-panel-dark bc-grid-bg overflow-hidden rounded-[28px] p-6 text-white sm:p-8 lg:p-10">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1.25fr)_minmax(320px,.75fr)] lg:items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#b8e467]">
              <Utensils size={12} /> {t('KREATE odak problemi · yemek israfı', 'KREATE focus problem · food waste')}
            </div>
            <h1 className="mt-4 max-w-4xl text-[40px] font-black leading-[.98] tracking-[-0.06em] sm:text-[56px]">
              {t('48.251 kg gerçek atığı, bir sonraki öğünde önlenecek karara çevir.', 'Turn 48,251 kg of measured waste into a decision that prevents the next kilogram.')}
            </h1>
            <p className="mt-5 max-w-3xl text-[12px] leading-6 text-white/62 sm:text-[13px]">
              {t(
                'BOUNCAMPUS bir sürdürülebilirlik raporu değil. Resmi atık geçmişini; ders programı, akademik takvim, hava ve menü bağlamıyla birleştirip üretim bandı öneren, operatör onayı isteyen ve pilot sonucuyla kendini kalibre eden kampüs yemek operasyon sistemi.',
                'BOUNCAMPUS is not a sustainability report. It combines official waste history with schedule, academic-calendar, weather and menu context to propose a production band, require operator approval, and recalibrate from measured pilot outcomes.',
              )}
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              <a
                href={FOOD_WASTE_SOURCE.url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 rounded-xl border border-white/12 bg-white/[0.08] px-3 py-2 text-[9px] font-black text-white transition hover:bg-white/[0.13]"
              >
                <Database size={11} /> {t('Resmi veriyi aç', 'Open official data')} <ExternalLink size={9} />
              </a>
              <Link href="/demo" className="inline-flex items-center gap-1.5 rounded-xl bg-[#b8e467] px-3 py-2 text-[9px] font-black text-[#071c33] transition hover:-translate-y-0.5">
                <Sparkles size={11} /> {t('90 sn jüri akışı', '90 sec jury flow')} <ArrowRight size={10} />
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <MetricCard label={t('2025 resmi yemek atığı', 'Official 2025 food waste')} value={formatKg(FOOD_WASTE_BASELINE.year2025WasteKg, locale)} />
            <MetricCard label={t('İSTAÇ geri kazanımına giden', 'Sent to İSTAÇ recovery')} value={formatKg(FOOD_WASTE_BASELINE.year2025RecoveredKg, locale)} />
            <MetricCard label={t('2024 → 2025 değişim', '2024 → 2025 change')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}%`} />
            <MetricCard label={t('Yemekhane toplam kapasitesi', 'Total dining-hall capacity')} value={FOOD_WASTE_BASELINE.diningHallCapacity.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.2fr_.8fr]">
        <article className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <div className="bc-eyebrow">{t('Resmi baz çizgisi', 'Official baseline')}</div>
              <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">
                {t('Problem ölçülmüş durumda; ürünün işi onu önlemek.', 'The problem is already measured; the product must prevent it.')}
              </h2>
            </div>
            <span className="bc-chip border-emerald-900/10 bg-emerald-50 text-emerald-700">
              <ShieldCheck size={10} /> OFFICIAL_PUBLIC
            </span>
          </div>

          <div className="mt-6 h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyChart} margin={{ top: 8, right: 4, left: -12, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#dfe5df" />
                <XAxis dataKey="month" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 9 }} axisLine={false} tickLine={false} />
                <Tooltip formatter={(value: number) => [formatKg(value, locale), t('Yemek atığı', 'Food waste')]} />
                <Bar dataKey="wasteKg" fill="#173f67" radius={[7, 7, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-2 text-[9px] leading-4 text-slate-400">
            {t(
              'Aylık sütunlar Boğaziçi Üniversitesi’nin yayımladığı 2025 yemek atığı değerleridir. Ürün bu sayıları canlı sensör verisi gibi sunmaz.',
              'Monthly bars are the 2025 food-waste values published by Boğaziçi University. The product does not present them as live sensor telemetry.',
            )}
          </p>
        </article>

        <aside className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.16em] text-slate-400">
            <Gauge size={12} /> {t('Bir sonraki servis · planlama bağlamı', 'Next service · planning context')}
          </div>
          <h2 className="mt-3 text-[25px] font-black tracking-[-0.045em] text-slate-950">
            {demand?.available
              ? t('Model tek sayı değil, güvenli bir üretim bandı öneriyor.', 'The model proposes a safe production band, not a magic number.')
              : t('Talep modeli yoksa sistem üretim sayısı uydurmuyor.', 'If demand context is unavailable, the system does not invent a production number.')}
          </h2>

          {demand?.available && demand.productionBand ? (
            <div className="mt-6 space-y-4">
              <div className="grid grid-cols-3 gap-2">
                <MiniMetric label={t('Tahmin', 'Forecast')} value={demand.productionBand.predictedMeals.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
                <MiniMetric label={t('Alt bant', 'Lower band')} value={demand.productionBand.lowerBound.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
                <MiniMetric label={t('Üst bant', 'Upper band')} value={demand.productionBand.upperBound.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
              </div>
              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-[9px] leading-5 text-amber-900">
                <strong>MODEL_ESTIMATE.</strong>{' '}
                {t('Bu bant gerçek üretim ya da servis verisi değildir. Pilot sırasında üretilen, servis edilen ve kalan miktarlar ölçülerek kalibre edilmelidir.', 'This band is not actual production or served-meal telemetry. It must be calibrated in a pilot using measured produced, served and leftover quantities.')}
              </div>
            </div>
          ) : (
            <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white p-5 text-[10px] leading-5 text-slate-500">
              {t('Resmi atık geçmişi yine kullanılabilir; fakat servis talebi hesaplanamadığında operasyon önerisi beklemeye alınır.', 'The official waste baseline remains usable; however, operational production advice is withheld when service demand cannot be calculated.')}
            </div>
          )}
        </aside>
      </section>

      <section className="bc-panel-dark overflow-hidden rounded-[26px] p-6 text-white sm:p-8">
        <div className="grid gap-8 xl:grid-cols-[.82fr_1.18fr] xl:items-start">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]">
              <Scale size={12} /> {t('Karar laboratuvarı', 'Decision lab')}
            </div>
            <h2 className="mt-3 text-[32px] font-black leading-[1.02] tracking-[-0.05em]">
              {t('Jüri, hedefi değiştirince yıllık operasyon sonucu anında görür.', 'Change the target and show the jury the annual operating outcome immediately.')}
            </h2>
            <p className="mt-3 text-[10px] leading-5 text-white/55">
              {t(
                'Bu alan geçmiş resmi 48.251 kg baz çizgisi üzerinde çalışan bir senaryo motorudur. Gerçek tasarruf iddiası değildir; pilot hedefini ve ölçüm planını somutlaştırır.',
                'This scenario engine runs on the official 48,251 kg historical baseline. It is not a claimed saving; it makes the pilot target and measurement plan concrete.',
              )}
            </p>

            <Slider
              label={t('Üretimde önleme hedefi', 'Prevention target at production')}
              value={preventionRate}
              min={0}
              max={30}
              onChange={setPreventionRate}
            />
            <Slider
              label={t('Kalan atıkta geri kazanım hedefi', 'Recovery target for remaining waste')}
              value={recoveryRate}
              min={Math.round(CURRENT_RECOVERY_RATE_PCT)}
              max={95}
              onChange={setRecoveryRate}
            />
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <ScenarioCard label={t('Kaynağında önlenen', 'Prevented at source')} value={formatKg(scenario.preventedKg, locale)} detail={t('Üretilmeden önlenmesi hedeflenen atık', 'Waste targeted to be avoided before production')} />
            <ScenarioCard label={t('Kalan toplam atık', 'Remaining total waste')} value={formatKg(scenario.remainingWasteKg, locale)} detail={t('Önleme sonrası baz çizgi', 'Post-prevention baseline')} />
            <ScenarioCard label={t('Geri kazanıma yönlenen', 'Directed to recovery')} value={formatKg(scenario.recoveredKg, locale)} detail={`${recoveryRate}% ${t('senaryo hedefi', 'scenario target')}`} />
            <ScenarioCard label={t('Artık yük', 'Residual load')} value={formatKg(scenario.residualKg, locale)} detail={`${formatKg(scenario.residualReductionKg, locale)} ${t('daha az artık', 'less residual')}`} />
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <FlowCard step="01" title={t('TAHMİN ET', 'FORECAST')} body={t('Program + akademik takvim + hava + menü tercih sinyallerinden servis talep bandı üret.', 'Produce a service-demand band from schedules, academic calendar, weather and menu-preference signals.')} />
        <FlowCard step="02" title={t('ONAYLA & ÜRET', 'APPROVE & PRODUCE')} body={t('Mutfak sorumlusu öneriyi kabul eder, düzenler veya reddeder. Model doğrudan mutfağa komut göndermez.', 'The kitchen operator accepts, edits or rejects the recommendation. The model never dispatches directly to kitchen operations.')} />
        <FlowCard step="03" title={t('ÖLÇ & ÖĞREN', 'MEASURE & LEARN')} body={t('Üretilen, servis edilen, yenilebilir fazla ve kaçınılmaz atığı ölç; sonraki öğün için tahmini kalibre et.', 'Measure produced, served, edible surplus and unavoidable waste; calibrate the next service forecast.')} />
      </section>

      <section className="grid gap-5 border-t border-slate-900/10 pt-7 lg:grid-cols-[1fr_1fr]">
        <div>
          <div className="bc-eyebrow">{t('14 günlük pilot', '14-day pilot')}</div>
          <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">{t('Hackathon demosundan sahaya çıkış planı hazır.', 'The path from hackathon demo to field pilot is already defined.')}</h2>
          <p className="mt-3 text-[10px] leading-5 text-slate-500">
            {t('Bir yemekhane/servis kontrol, benzer bir servis müdahale grubu olur. Her öğünde sadece dört veri tutulur: üretilen porsiyon, servis edilen porsiyon, yenilebilir fazla, atık kg. Başarı metriği tahmin doğruluğu değil doğrudan kg/servis atık azalımıdır.', 'Use one dining hall/service as control and a comparable service as intervention. Record only four values per service: portions produced, portions served, edible surplus and waste kg. The success metric is not forecast accuracy alone; it is waste kg per service.')}
          </p>
        </div>
        <div className="grid gap-2 sm:grid-cols-2">
          {[t('Atık kg / servis', 'Waste kg / service'), t('Fazla üretim oranı', 'Overproduction rate'), t('Yenilebilir fazla kurtarma', 'Edible surplus recovery'), t('Tahmin hata bandı', 'Forecast error band')].map(item => (
            <div key={item} className="flex items-center gap-2 rounded-xl border border-slate-900/10 bg-white p-3 text-[9px] font-black text-slate-700">
              <CheckCircle2 size={12} className="text-emerald-600" /> {item}
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-[24px] border border-slate-900/10 bg-[#f6f8f5] p-5 sm:p-6">
        <div className="flex items-start gap-3">
          <ShieldCheck className="mt-0.5 shrink-0 text-[#173f67]" size={18} />
          <div>
            <div className="text-[10px] font-black uppercase tracking-[0.14em] text-[#173f67]">{t('Jüri güven kuralı', 'Jury trust rule')}</div>
            <p className="mt-2 text-[10px] leading-5 text-slate-600">
              {t('Resmi: 2024/2025 toplam atık, 2025 aylık atık ve geri kazanım, yemekhane hizmet ölçeği. Model: bir sonraki servis talebi ve senaryo çıktıları. Şu anda yok: POS, üretilen/servis edilen gerçek porsiyon, tabak bazlı atık. BOUNCAMPUS bu sınırı ekranda saklamaz.', 'Official: 2024/2025 total waste, 2025 monthly waste/recovery and dining-service scale. Modeled: next-service demand and scenario outcomes. Not currently available: POS, actual produced/served portions and plate-level waste. BOUNCAMPUS keeps that boundary visible.')}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.065] p-4 backdrop-blur-sm">
      <div className="text-[8px] font-black uppercase tracking-[0.12em] text-white/45">{label}</div>
      <div className="mt-2 font-mono text-[24px] font-black tracking-[-0.04em] text-white">{value}</div>
    </div>
  );
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-900/10 bg-[#f7f9f6] p-3">
      <div className="text-[8px] font-black uppercase tracking-[0.1em] text-slate-400">{label}</div>
      <div className="mt-1 font-mono text-lg font-black text-slate-900">{value}</div>
    </div>
  );
}

function Slider({ label, value, min, max, onChange }: { label: string; value: number; min: number; max: number; onChange: (value: number) => void }) {
  return (
    <label className="mt-6 block">
      <div className="flex items-center justify-between gap-3 text-[9px] font-black uppercase tracking-[0.12em] text-white/65">
        <span>{label}</span><span className="font-mono text-[#b8e467]">{value}%</span>
      </div>
      <input
        className="mt-3 w-full accent-[#b8e467]"
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={event => onChange(Number(event.target.value))}
      />
    </label>
  );
}

function ScenarioCard({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.06] p-5">
      <div className="text-[8px] font-black uppercase tracking-[0.12em] text-white/42">{label}</div>
      <div className="mt-3 font-mono text-[28px] font-black tracking-[-0.05em] text-white">{value}</div>
      <div className="mt-2 text-[9px] leading-4 text-white/45">{detail}</div>
    </div>
  );
}

function FlowCard({ step, title, body }: { step: string; title: string; body: string }) {
  return (
    <article className="bc-panel rounded-[22px] p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="font-mono text-[9px] font-black text-emerald-700">{step}</span>
        <BarChart3 size={14} className="text-slate-300" />
      </div>
      <h3 className="mt-6 text-[12px] font-black tracking-[0.06em] text-slate-950">{title}</h3>
      <p className="mt-2 text-[10px] leading-5 text-slate-500">{body}</p>
    </article>
  );
}
