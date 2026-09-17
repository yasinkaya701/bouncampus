'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Database,
  Download,
  ExternalLink,
  Gauge,
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
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
  type DecisionReadiness,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type ProductionBand = {
  predictedMeals: number;
  lowerBound: number;
  recommendedTarget: number;
  upperBound: number;
  signalCoveragePct: number;
  decisionReadiness: DecisionReadiness;
  operatorApprovalRequired: true;
  autoDispatchAllowed: false;
  provenance: 'MODEL_ESTIMATE';
  signals: Array<{ id: string; label: string; available: boolean; weightPct: number }>;
  reasonCodes: string[];
};

type FoodApi = {
  demandContext: {
    available: boolean;
    productionBand: ProductionBand | null;
  };
  decisionPolicy: {
    humanApprovalRequired: boolean;
    automaticKitchenDispatch: boolean;
  };
};

type OperatorDecision = 'HOLD' | 'PILOT_APPROVED' | 'EDIT_REQUIRED';

const formatKg = (value: number, locale: 'tr' | 'en') =>
  `${Math.round(value).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} kg`;

export default function FoodWastePage() {
  const { locale, t } = useLocale();
  const [preventionRate, setPreventionRate] = useState(15);
  const [recoveryRate, setRecoveryRate] = useState(85);
  const [food, setFood] = useState<FoodApi | null>(null);
  const [operatorDecision, setOperatorDecision] = useState<OperatorDecision>('HOLD');

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then(payload => setFood(payload))
      .catch(() => setFood(null));
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

  const band = food?.demandContext.productionBand ?? null;
  const canApprovePilot = band?.decisionReadiness === 'PILOT_READY';

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
                'BOUNCAMPUS resmi atık geçmişini ders programı, akademik takvim, hava ve menü bağlamıyla birleştirir; veri eksikse öneriyi genişletir veya tamamen bekletir, operatör onayı olmadan hiçbir üretim komutu göndermez ve sonucu kontrollü pilotta ölçer.',
                'BOUNCAMPUS combines the official waste baseline with schedules, academic calendar, weather and menu context; it widens or withholds advice when evidence is missing, never dispatches production without an operator, and measures the result in a controlled pilot.',
              )}
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-xl border border-white/12 bg-white/[0.08] px-3 py-2 text-[9px] font-black text-white transition hover:bg-white/[0.13]">
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
            <MetricCard label={t('Pilot hedefi · iddia değil', 'Pilot target · not a claim')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} />
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.12fr_.88fr]">
        <article className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <div className="bc-eyebrow">{t('Resmi baz çizgisi', 'Official baseline')}</div>
              <h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">
                {t('Problem ölçülmüş; ürün sonucu sahiplenmeden önce pilotta ölçmek zorunda.', 'The problem is measured; the product must measure the outcome before claiming impact.')}
              </h2>
            </div>
            <span className="bc-chip border-emerald-900/10 bg-emerald-50 text-emerald-700"><ShieldCheck size={10} /> OFFICIAL_PUBLIC</span>
          </div>

          <div className="mt-6 h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyChart} margin={{ top: 8, right: 4, left: -12, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#dfe5df" />
                <XAxis dataKey="month" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 9 }} axisLine={false} tickLine={false} />
                <Tooltip formatter={value => [formatKg(Number(value ?? 0), locale), t('Yemek atığı', 'Food waste')]} />
                <Bar dataKey="wasteKg" fill="#173f67" radius={[7, 7, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-2 text-[9px] leading-4 text-slate-400">
            {t('Aylık sütunlar yayımlanmış 2025 değerleridir; canlı sensör telemetrisi değildir.', 'Monthly bars are published 2025 values; they are not live sensor telemetry.')}
          </p>
        </article>

        <aside className="bc-panel rounded-[24px] p-5 sm:p-6">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.16em] text-slate-400"><Gauge size={12} /> {t('Bir sonraki servis · karar kalitesi', 'Next service · decision quality')}</div>
          <h2 className="mt-3 text-[25px] font-black tracking-[-0.045em] text-slate-950">
            {band ? t('Sistem sadece bant değil, o bandın ne kadar kullanılabilir olduğunu da söyler.', 'The system exposes not just a band, but how usable that band is.') : t('Talep bağlamı yoksa sistem üretim sayısı uydurmuyor.', 'If demand context is unavailable, the system does not invent a production number.')}
          </h2>

          {band ? (
            <div className="mt-5 space-y-4">
              <div className="grid grid-cols-2 gap-2">
                <MiniMetric label={t('Önerilen başlangıç', 'Operator starting point')} value={band.recommendedTarget.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} />
                <MiniMetric label={t('Karar bandı', 'Decision band')} value={`${band.lowerBound.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')}–${band.upperBound.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')}`} />
              </div>

              <div className="rounded-2xl border border-slate-900/10 bg-[#f7f9f6] p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <ReadinessBadge readiness={band.decisionReadiness} />
                  <span className="font-mono text-[10px] font-black text-slate-600">{band.signalCoveragePct}% {t('sinyal kapsamı', 'signal coverage')}</span>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-2">
                  {band.signals.map(signal => (
                    <div key={signal.id} className="flex items-center gap-2 rounded-xl border border-slate-900/[0.07] bg-white px-3 py-2 text-[8px] font-black text-slate-600">
                      {signal.available ? <CheckCircle2 size={11} className="text-emerald-600" /> : <AlertTriangle size={11} className="text-amber-600" />}
                      <span>{signal.label}</span>
                      <span className="ml-auto font-mono text-slate-400">{signal.weightPct}%</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-[9px] leading-5 text-amber-900">
                <strong>MODEL_ESTIMATE.</strong> {t('Bant pilot öncesi doğrulanmış gerçek üretim talebi değildir. Eksik sinyal belirsizliği artırır; WITHHOLD durumunda öneri uygulanmaz.', 'The band is not validated production demand before the pilot. Missing signals widen uncertainty; a WITHHOLD decision must not be applied.')}
              </div>
            </div>
          ) : (
            <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white p-5 text-[10px] leading-5 text-slate-500">
              {t('Resmi baz çizgisi görünür kalır; operasyon önerisi veri gelene kadar bekletilir.', 'The official baseline remains visible; operational advice is withheld until decision context is available.')}
            </div>
          )}
        </aside>
      </section>

      <section className="rounded-[26px] border border-slate-900/10 bg-white p-5 sm:p-6">
        <div className="grid gap-6 xl:grid-cols-[.72fr_1.28fr] xl:items-start">
          <div>
            <div className="bc-eyebrow">{t('Operatör kapısı', 'Operator gate')}</div>
            <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('AI önerir. Mutfak sorumlusu karar verir.', 'AI recommends. The kitchen operator decides.')}</h2>
            <p className="mt-3 text-[10px] leading-5 text-slate-500">{t('Bu demo state’i hiçbir harici mutfak sistemine bağlı değildir. Ama gerçek ürün davranışı nettir: onay, düzenleme veya bekletme olmadan aksiyon yok.', 'This demo state is not connected to any external kitchen system. The production behavior is still explicit: no action without approve, edit, or hold.')}</p>
          </div>
          <div>
            <div className="grid gap-2 sm:grid-cols-3">
              <DecisionButton active={operatorDecision === 'PILOT_APPROVED'} disabled={!canApprovePilot} onClick={() => setOperatorDecision('PILOT_APPROVED')} label={t('Pilot için onayla', 'Approve for pilot')} detail={canApprovePilot ? t('Sadece kontrollü pilot', 'Controlled pilot only') : t('PILOT_READY gerekli', 'Requires PILOT_READY')} />
              <DecisionButton active={operatorDecision === 'EDIT_REQUIRED'} onClick={() => setOperatorDecision('EDIT_REQUIRED')} label={t('Düzenleme iste', 'Request edit')} detail={t('Bant / bağlamı gözden geçir', 'Review band / context')} />
              <DecisionButton active={operatorDecision === 'HOLD'} onClick={() => setOperatorDecision('HOLD')} label={t('Beklet', 'Hold')} detail={t('Eksik veri veya operasyon riski', 'Missing data or operational risk')} />
            </div>
            <div className="mt-3 rounded-xl bg-slate-950 px-4 py-3 text-[9px] font-bold text-white/70">
              {operatorDecision === 'PILOT_APPROVED'
                ? t('PILOT_APPROVED · UI-only. Harici üretim komutu gönderilmedi.', 'PILOT_APPROVED · UI-only. No external production command was sent.')
                : operatorDecision === 'EDIT_REQUIRED'
                  ? t('EDIT_REQUIRED · Öneri operatör revizyonuna döndü.', 'EDIT_REQUIRED · Recommendation returned for operator revision.')
                  : t('HOLD · Varsayılan güvenli durum. Otomatik dispatch kapalı.', 'HOLD · Safe default state. Automatic dispatch is disabled.')}
            </div>
          </div>
        </div>
      </section>

      <section className="bc-panel-dark overflow-hidden rounded-[26px] p-6 text-white sm:p-8">
        <div className="grid gap-8 xl:grid-cols-[.82fr_1.18fr] xl:items-start">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]"><Scale size={12} /> {t('Karar laboratuvarı', 'Decision lab')}</div>
            <h2 className="mt-3 text-[32px] font-black leading-[1.02] tracking-[-0.05em]">{t('Hedefi değiştir; bunun senaryo olduğunu hiç gizleme.', 'Change the target; never hide that this is a scenario.')}</h2>
            <p className="mt-3 text-[10px] leading-5 text-white/55">{t('2025 resmi baz çizgisine matematiksel senaryo uygulanır. Bu bölüm gerçek pilot sonucu veya gerçekleşmiş iklim tasarrufu değildir.', 'A mathematical scenario is applied to the official 2025 baseline. This is not a real pilot result or achieved climate saving.')}</p>
            <Slider label={t('Üretimde önleme hedefi', 'Prevention target at production')} value={preventionRate} min={0} max={30} onChange={setPreventionRate} />
            <Slider label={t('Kalan atıkta geri kazanım hedefi', 'Recovery target for remaining waste')} value={recoveryRate} min={Math.round(CURRENT_RECOVERY_RATE_PCT)} max={95} onChange={setRecoveryRate} />
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <ScenarioCard label={t('Kaynağında önlenen', 'Prevented at source')} value={formatKg(scenario.preventedKg, locale)} detail={t('Senaryo hedefi', 'Scenario target')} />
            <ScenarioCard label={t('Kalan toplam atık', 'Remaining total waste')} value={formatKg(scenario.remainingWasteKg, locale)} detail={t('Önleme sonrası senaryo', 'Post-prevention scenario')} />
            <ScenarioCard label={t('Geri kazanıma yönlenen', 'Directed to recovery')} value={formatKg(scenario.recoveredKg, locale)} detail={`${recoveryRate}% ${t('senaryo hedefi', 'scenario target')}`} />
            <ScenarioCard label={t('Artık yük', 'Residual load')} value={formatKg(scenario.residualKg, locale)} detail={`${formatKg(scenario.residualReductionKg, locale)} ${t('senaryoda daha az artık', 'less residual in scenario')}`} />
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        <FlowCard step="01" title={t('TAHMİN ET', 'FORECAST')} body={t('Program + takvim + hava + menü sinyallerini kaynak sağlığıyla birlikte değerlendir.', 'Evaluate schedule + calendar + weather + menu signals together with source health.')} />
        <FlowCard step="02" title={t('ONAYLA / BEKLET', 'APPROVE / WITHHOLD')} body={t('Karar kalitesi yetersizse sistem sayıyı uygulamaz. Operatör onayı her durumda zorunlu.', 'If decision quality is insufficient, the system withholds the recommendation. Operator approval is always required.')} />
        <FlowCard step="03" title={t('ÖLÇ & ÖĞREN', 'MEASURE & LEARN')} body={t('Normalize edilmiş atık metriği ve operasyon guardrail’leriyle sonucu ölç; sonra modeli kalibre et.', 'Measure the outcome with normalized waste metrics and operational guardrails, then recalibrate the model.')} />
      </section>

      <section className="rounded-[26px] border border-slate-900/10 bg-[#f6f8f5] p-5 sm:p-7">
        <div className="grid gap-7 lg:grid-cols-[.78fr_1.22fr]">
          <div>
            <div className="bc-eyebrow">{t('14 günlük falsifiable pilot', '14-day falsifiable pilot')}</div>
            <h2 className="mt-2 text-[29px] font-black tracking-[-0.05em] text-slate-950">{t('Başarı tanımı demo öncesinde kayıtlı.', 'Success is defined before the demo result exists.')}</h2>
            <p className="mt-3 text-[10px] leading-5 text-slate-500">{t('Ana KPI artık kg/servis değil, servis hacmine göre normalize edilmiş kg / 100 servis edilen öğün. Böylece daha sakin bir gün sahte başarı gibi görünmez.', 'The primary KPI is normalized to kg / 100 served meals, not just kg/service, so a quieter day cannot masquerade as success.')}</p>
            <a href="/api/v1/food/pilot-template" className="mt-5 inline-flex items-center gap-2 rounded-xl bg-[#173f67] px-4 py-2.5 text-[9px] font-black text-white">
              <Download size={12} /> {t('14 günlük ölçüm CSV’sini indir', 'Download 14-day measurement CSV')}
            </a>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <PilotCard label={t('Ana KPI', 'Primary KPI')} value={t('kg / 100 servis', 'kg / 100 served')} detail={FOOD_WASTE_PILOT_PROTOCOL.primaryMetric.formula} />
            <PilotCard label={t('Ön-kayıtlı hedef', 'Pre-registered target')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} detail={t('Kontrole göre azalma · henüz sonuç değil', 'Reduction vs control · not an achieved result')} />
            <PilotCard label={t('Hizmet guardrail’i', 'Service guardrail')} value={t('Erken tükenme artmasın', 'No early-sellout increase')} detail={t('Atığı azaltırken hizmet seviyesini bozmayı başarı saymıyoruz.', 'Waste reduction does not count as success if service reliability worsens.')} />
            <PilotCard label={t('Minimum kanıt', 'Minimum evidence')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm} + ${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} detail={t('Kontrol + müdahale ölçülmüş servis', 'Measured control + intervention services')} />
          </div>
        </div>
      </section>

      <section className="grid gap-3 lg:grid-cols-3">
        <TruthCard title={t('ŞİMDİ SÖYLEYEBİLİRİZ', 'WE CAN CLAIM NOW')} items={[t('48.251 kg resmi 2025 baz çizgisi', '48,251 kg official 2025 baseline'), t('Kaynak sağlığı / provenance', 'Source health / provenance'), t('Model tahmini ve senaryo olduğunu açıkça', 'Model estimates and scenarios, explicitly labeled')]} tone="good" />
        <TruthCard title={t('PİLOTTA TEST EDECEĞİZ', 'WE WILL TEST IN PILOT')} items={[t('Üretim bandı atığı azaltıyor mu?', 'Does the production band reduce waste?'), t('Erken tükenme artıyor mu?', 'Does early sell-out increase?'), t('Operatör ne sıklıkla override ediyor?', 'How often does the operator override?')]} tone="neutral" />
        <TruthCard title={t('ÖLÇMEDEN SÖYLEMEYİZ', 'WE WILL NOT CLAIM BEFORE MEASUREMENT')} items={[t('“X kg tasarruf ettik”', '“We saved X kg”'), t('“Y kg CO₂ azalttık”', '“We avoided Y kg CO₂”'), t('“Gerçek öğrenci talebini görüyoruz”', '“We observe actual student demand”')]} tone="warn" />
      </section>
    </div>
  );
}

function ReadinessBadge({ readiness }: { readiness: DecisionReadiness }) {
  const classes = readiness === 'PILOT_READY'
    ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
    : readiness === 'REVIEW_REQUIRED'
      ? 'border-amber-200 bg-amber-50 text-amber-700'
      : 'border-rose-200 bg-rose-50 text-rose-700';
  return <span className={`rounded-full border px-2.5 py-1 font-mono text-[8px] font-black ${classes}`}>{readiness}</span>;
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return <div className="rounded-2xl border border-white/10 bg-white/[0.065] p-4 backdrop-blur-sm"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-white/45">{label}</div><div className="mt-2 font-mono text-[24px] font-black tracking-[-0.04em] text-white">{value}</div></div>;
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-slate-900/10 bg-[#f7f9f6] p-3"><div className="text-[8px] font-black uppercase tracking-[0.1em] text-slate-400">{label}</div><div className="mt-1 font-mono text-lg font-black text-slate-900">{value}</div></div>;
}

function DecisionButton({ active, disabled = false, onClick, label, detail }: { active: boolean; disabled?: boolean; onClick: () => void; label: string; detail: string }) {
  return <button type="button" disabled={disabled} onClick={onClick} className={`rounded-2xl border p-4 text-left transition ${active ? 'border-[#173f67] bg-[#173f67] text-white' : 'border-slate-900/10 bg-[#f7f9f6] text-slate-800'} ${disabled ? 'cursor-not-allowed opacity-40' : 'hover:-translate-y-0.5'}`}><div className="text-[10px] font-black">{label}</div><div className={`mt-2 text-[8px] leading-4 ${active ? 'text-white/55' : 'text-slate-400'}`}>{detail}</div></button>;
}

function Slider({ label, value, min, max, onChange }: { label: string; value: number; min: number; max: number; onChange: (value: number) => void }) {
  return <label className="mt-6 block"><div className="flex items-center justify-between gap-3 text-[9px] font-black uppercase tracking-[0.12em] text-white/65"><span>{label}</span><span className="font-mono text-[#b8e467]">{value}%</span></div><input className="mt-3 w-full accent-[#b8e467]" type="range" min={min} max={max} value={value} onChange={event => onChange(Number(event.target.value))} /></label>;
}

function ScenarioCard({ label, value, detail }: { label: string; value: string; detail: string }) {
  return <div className="rounded-2xl border border-white/10 bg-white/[0.06] p-5"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-white/42">{label}</div><div className="mt-3 font-mono text-[28px] font-black tracking-[-0.05em] text-white">{value}</div><div className="mt-2 text-[9px] leading-4 text-white/45">{detail}</div></div>;
}

function FlowCard({ step, title, body }: { step: string; title: string; body: string }) {
  return <article className="bc-panel rounded-[22px] p-5"><div className="flex items-center justify-between gap-3"><span className="font-mono text-[9px] font-black text-emerald-700">{step}</span><BarChart3 size={14} className="text-slate-300" /></div><h3 className="mt-6 text-[12px] font-black tracking-[0.06em] text-slate-950">{title}</h3><p className="mt-2 text-[10px] leading-5 text-slate-500">{body}</p></article>;
}

function PilotCard({ label, value, detail }: { label: string; value: string; detail: string }) {
  return <div className="rounded-2xl border border-slate-900/10 bg-white p-5"><div className="text-[8px] font-black uppercase tracking-[0.11em] text-slate-400">{label}</div><div className="mt-3 text-[19px] font-black tracking-[-0.04em] text-slate-950">{value}</div><div className="mt-2 font-mono text-[8px] leading-4 text-slate-400">{detail}</div></div>;
}

function TruthCard({ title, items, tone }: { title: string; items: string[]; tone: 'good' | 'neutral' | 'warn' }) {
  const icon = tone === 'good' ? <CheckCircle2 size={14} /> : tone === 'warn' ? <AlertTriangle size={14} /> : <ShieldCheck size={14} />;
  const accent = tone === 'good' ? 'text-emerald-700' : tone === 'warn' ? 'text-amber-700' : 'text-[#173f67]';
  return <article className="rounded-[22px] border border-slate-900/10 bg-white p-5"><div className={`flex items-center gap-2 text-[9px] font-black tracking-[0.08em] ${accent}`}>{icon}{title}</div><div className="mt-4 space-y-2">{items.map(item => <div key={item} className="rounded-xl bg-[#f7f9f6] px-3 py-2 text-[9px] font-semibold leading-4 text-slate-600">{item}</div>)}</div></article>;
}
