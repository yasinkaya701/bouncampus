'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Database,
  ExternalLink,
  Gauge,
  ShieldCheck,
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
  type ProductionDecisionBand,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type FoodApi = {
  demandContext: {
    available: boolean;
    productionBand: ProductionDecisionBand | null;
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
  const numberLocale = locale === 'tr' ? 'tr-TR' : 'en-US';
  const [food, setFood] = useState<FoodApi | null>(null);
  const [operatorDecision, setOperatorDecision] = useState<OperatorDecision>('HOLD');
  const [preventionRate, setPreventionRate] = useState(10);
  const [recoveryRate, setRecoveryRate] = useState(Math.round(CURRENT_RECOVERY_RATE_PCT));

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then(payload => setFood(payload))
      .catch(() => setFood(null));
  }, []);

  const monthlyChart = useMemo(
    () => FOOD_WASTE_2025.map(item => ({
      month: locale === 'tr' ? item.monthTr : item.month,
      wasteKg: item.wasteKg,
    })),
    [locale],
  );

  const scenario = useMemo(
    () => simulateFoodWasteScenario(preventionRate, recoveryRate),
    [preventionRate, recoveryRate],
  );

  const band = food?.demandContext.productionBand ?? null;
  const canApprovePilot = band?.decisionReadiness === 'PILOT_READY';

  return (
    <div className="space-y-12 sm:space-y-16">
      <section className="border-b border-[#111712]/10 pb-8 sm:pb-10">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#687168]">
              <Utensils size={11} /> {t('Next service / food waste', 'Next service / food waste')}
            </div>
            <h1 className="mt-4 max-w-4xl text-[44px] font-black leading-[0.95] tracking-[-0.06em] text-[#111712] sm:text-[62px]">
              {t('Önce kanıtı gör. Sonra üretim kararını ver.', 'See the evidence first. Then make the production decision.')}
            </h1>
          </div>
          <div className="max-w-md">
            <p className="text-[11px] leading-5 text-[#687068]">
              {t(
                'Bu ekran otomatik üretim komutu göndermez. Model bir başlangıç bandı üretir; mutfak sorumlusu onaylar, düzenler veya bekletir.',
                'This surface never auto-dispatches production. The model produces a starting band; the kitchen operator approves, edits or holds.',
              )}
            </p>
            <a
              href={FOOD_WASTE_SOURCE.url}
              target="_blank"
              rel="noreferrer"
              className="bc-focus-ring mt-3 inline-flex items-center gap-1.5 rounded-sm text-[9px] font-black text-[#315846] hover:text-[#18372b]"
            >
              <Database size={10} /> {t('Resmi baz çizgisini aç', 'Open official baseline')} <ExternalLink size={9} />
            </a>
          </div>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.22fr)_minmax(360px,.78fr)]">
        <article className="bc-workbench overflow-hidden rounded-2xl">
          <div className="flex flex-wrap items-start justify-between gap-4 border-b border-[#111712]/10 p-5 sm:p-6">
            <div>
              <div className="bc-eyebrow">{t('Karar workbench’i', 'Decision workbench')}</div>
              <h2 className="mt-2 text-[28px] font-black tracking-[-0.045em] text-[#111712]">
                {t('Bir sonraki öğle servisi için üretim bandı', 'Production band for the next lunch service')}
              </h2>
            </div>
            {band ? <ReadinessBadge readiness={band.decisionReadiness} /> : <StatusBadge label="WAITING FOR CONTEXT" tone="neutral" />}
          </div>

          <div className="grid lg:grid-cols-[minmax(0,.95fr)_minmax(300px,1.05fr)]">
            <div className="border-b border-[#111712]/10 p-5 sm:p-6 lg:border-b-0 lg:border-r">
              {band ? (
                <>
                  <div className="text-[9px] font-black uppercase tracking-[0.16em] text-[#7b827c]">{t('Operatör başlangıç noktası', 'Operator starting point')}</div>
                  <div className="mt-3 flex items-end gap-2">
                    <span className="bc-mono text-[68px] font-black leading-[0.82] tracking-[-0.07em] text-[#111712] sm:text-[82px]">
                      {band.recommendedTarget.toLocaleString(numberLocale)}
                    </span>
                    <span className="pb-1.5 text-[11px] font-black text-[#6d746e]">{t('öğün', 'meals')}</span>
                  </div>
                  <div className="mt-5 grid grid-cols-2 gap-3 border-y border-[#111712]/10 py-4">
                    <BandMetric label={t('Alt sınır', 'Lower bound')} value={band.lowerBound.toLocaleString(numberLocale)} />
                    <BandMetric label={t('Üst sınır', 'Upper bound')} value={band.upperBound.toLocaleString(numberLocale)} />
                  </div>
                  <div className="mt-4 flex items-center justify-between gap-3">
                    <div>
                      <div className="text-[9px] font-black uppercase tracking-[0.14em] text-[#7d847e]">{t('Sinyal kapsamı', 'Signal coverage')}</div>
                      <div className="mt-1 font-mono text-[15px] font-black text-[#111712]">{band.signalCoveragePct}%</div>
                    </div>
                    <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-[#e4e0d7]">
                      <div className="h-full bg-[#18372b]" style={{ width: `${band.signalCoveragePct}%` }} />
                    </div>
                  </div>
                  <div className="mt-4 rounded-lg bg-[#efede6] px-3.5 py-3 text-[9px] leading-4 text-[#636b64]">
                    <strong className="font-black text-[#303831]">MODEL_ESTIMATE.</strong>{' '}
                    {t('Bu sayı ölçülmüş gerçek talep değildir. Eksik sinyaller belirsizliği artırır; WITHHOLD durumunda uygulanmaz.', 'This is not measured demand truth. Missing signals increase uncertainty; a WITHHOLD recommendation must not be applied.')}
                  </div>
                </>
              ) : (
                <div className="flex min-h-[280px] flex-col justify-center">
                  <div className="text-[9px] font-black uppercase tracking-[0.16em] text-[#7d847e]">{t('Güvenli varsayılan', 'Safe default')}</div>
                  <div className="mt-3 text-[34px] font-black leading-none tracking-[-0.045em] text-[#111712]">HOLD</div>
                  <p className="mt-4 max-w-md text-[10px] leading-5 text-[#697169]">
                    {t('Karar bağlamı gelmeden sistem üretim sayısı uydurmaz. Resmi baz çizgisi görünür kalır; operasyon önerisi bekletilir.', 'Until decision context is available, the system does not invent a production number. The official baseline remains visible and operational advice is withheld.')}
                  </p>
                </div>
              )}
            </div>

            <div className="p-5 sm:p-6">
              <div className="flex items-center justify-between gap-3">
                <div className="bc-eyebrow">{t('Kararı taşıyan sinyaller', 'Signals behind the decision')}</div>
                <span className="font-mono text-[8px] font-black text-[#858b85]">PROVENANCE ON</span>
              </div>

              <div className="mt-4 divide-y divide-[#111712]/10 border-y border-[#111712]/10">
                {band ? band.signals.map(signal => (
                  <div key={signal.id} className="grid grid-cols-[18px_minmax(0,1fr)_auto] items-center gap-3 py-3.5">
                    {signal.available ? <CheckCircle2 size={12} className="text-[#55794a]" /> : <AlertTriangle size={12} className="text-[#9a7536]" />}
                    <div>
                      <div className="text-[10px] font-black text-[#2d342e]">{signal.label}</div>
                      <div className="mt-0.5 text-[8px] font-bold uppercase tracking-[0.1em] text-[#858b85]">{signal.available ? t('mevcut', 'available') : t('eksik', 'missing')}</div>
                    </div>
                    <div className="font-mono text-[10px] font-black text-[#6c746d]">{signal.weightPct}%</div>
                  </div>
                )) : (
                  <div className="py-5 text-[10px] leading-5 text-[#6d746e]">{t('Karar sinyalleri henüz yüklenmedi.', 'Decision signals have not loaded yet.')}</div>
                )}
              </div>

              {band?.reasonCodes?.length ? (
                <div className="mt-4">
                  <div className="text-[8px] font-black uppercase tracking-[0.14em] text-[#878d87]">{t('Neden kodları', 'Reason codes')}</div>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {band.reasonCodes.map(code => <span key={code} className="rounded bg-[#efede6] px-2 py-1 font-mono text-[7px] font-bold text-[#646c65]">{code}</span>)}
                  </div>
                </div>
              ) : null}
            </div>
          </div>

          <div className="border-t border-[#111712]/10 bg-[#f0eee8] p-5 sm:p-6">
            <div className="grid gap-5 lg:grid-cols-[220px_minmax(0,1fr)] lg:items-start">
              <div>
                <div className="bc-eyebrow">{t('Operatör kapısı', 'Operator gate')}</div>
                <h3 className="mt-2 text-[21px] font-black tracking-[-0.035em] text-[#111712]">{t('Model önerir. İnsan karar verir.', 'Model recommends. Human decides.')}</h3>
              </div>
              <div>
                <div className="grid gap-2 sm:grid-cols-3">
                  <DecisionButton
                    active={operatorDecision === 'PILOT_APPROVED'}
                    disabled={!canApprovePilot}
                    onClick={() => setOperatorDecision('PILOT_APPROVED')}
                    label={t('Pilot için onayla', 'Approve for pilot')}
                    detail={canApprovePilot ? t('Kontrollü pilot', 'Controlled pilot') : t('PILOT_READY gerekli', 'Requires PILOT_READY')}
                  />
                  <DecisionButton
                    active={operatorDecision === 'EDIT_REQUIRED'}
                    onClick={() => setOperatorDecision('EDIT_REQUIRED')}
                    label={t('Düzenleme iste', 'Request edit')}
                    detail={t('Bandı / bağlamı gözden geçir', 'Review band / context')}
                  />
                  <DecisionButton
                    active={operatorDecision === 'HOLD'}
                    onClick={() => setOperatorDecision('HOLD')}
                    label={t('Beklet', 'Hold')}
                    detail={t('Güvenli varsayılan', 'Safe default')}
                  />
                </div>
                <DecisionResult decision={operatorDecision} t={t} />
              </div>
            </div>
          </div>
        </article>

        <aside className="rounded-2xl bg-[#18372b] p-5 text-white sm:p-6">
          <div className="flex items-center justify-between gap-3">
            <div className="text-[9px] font-black uppercase tracking-[0.17em] text-[#b9da72]">{t('Resmi baz çizgisi', 'Official baseline')}</div>
            <ShieldCheck size={15} className="text-white/40" />
          </div>
          <div className="mt-7">
            <div className="font-mono text-[56px] font-black leading-none tracking-[-0.065em]">{FOOD_WASTE_BASELINE.year2025WasteKg.toLocaleString(numberLocale)}</div>
            <div className="mt-1 text-[10px] font-bold text-white/55">kg · {t('2025 yemek atığı', '2025 food waste')}</div>
          </div>

          <div className="mt-7 divide-y divide-white/12 border-y border-white/12">
            <DarkMetric label={t('2024 → 2025', '2024 → 2025')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}%`} />
            <DarkMetric label={t('Geri kazanıma giden', 'Sent to recovery')} value={formatKg(FOOD_WASTE_BASELINE.year2025RecoveredKg, locale)} />
            <DarkMetric label={t('Pilot başarı kapısı', 'Pilot success gate')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} note={t('hedef · sonuç değil', 'target · not result')} />
            <DarkMetric label={t('Otomatik dispatch', 'Automatic dispatch')} value={food?.decisionPolicy.automaticKitchenDispatch ? 'ON' : 'OFF'} note={t('insan onayı zorunlu', 'human approval required')} />
          </div>

          <p className="mt-5 text-[9px] leading-5 text-white/48">
            {t('Yayımlanmış baz çizgisi üründen önce vardır. Ürün yalnız pilotta ölçülen farkı sahiplenebilir.', 'The published baseline exists independently of the product. The product can claim only the difference measured in the pilot.')}
          </p>
        </aside>
      </section>

      <section className="grid gap-8 lg:grid-cols-[minmax(0,.7fr)_minmax(0,1.3fr)] lg:gap-12">
        <div>
          <div className="bc-eyebrow">{t('2025 resmi dağılım', 'Official 2025 distribution')}</div>
          <h2 className="mt-2 text-[34px] font-black leading-[1] tracking-[-0.055em] text-[#111712]">
            {t('Sorun tek bir kötü aya indirgenemez.', 'The problem is not one bad month.')}
          </h2>
          <p className="mt-4 max-w-md text-[10px] leading-5 text-[#697169]">
            {t('Aylık değerler yayımlanmış 2025 kayıtlarıdır. Canlı kampüs sensörü veya mutfak POS telemetrisi değildir.', 'Monthly values are published 2025 records. They are not live campus sensor or kitchen POS telemetry.')}
          </p>
        </div>

        <div className="h-[310px] min-w-0 border-y border-[#111712]/10 py-5">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthlyChart} margin={{ top: 8, right: 4, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="2 4" vertical={false} stroke="rgba(17,23,18,.10)" />
              <XAxis dataKey="month" tick={{ fontSize: 9, fill: '#717871' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 9, fill: '#717871' }} axisLine={false} tickLine={false} />
              <Tooltip formatter={value => [formatKg(Number(value ?? 0), locale), t('Yemek atığı', 'Food waste')]} />
              <Bar dataKey="wasteKg" fill="#18372b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="border-t border-[#111712]/10 pt-8">
        <div className="grid gap-8 xl:grid-cols-[minmax(0,.88fr)_minmax(0,1.12fr)] xl:gap-14">
          <div>
            <div className="bc-eyebrow">{t('Pilot simülatörü', 'Pilot simulator')}</div>
            <h2 className="mt-2 text-[34px] font-black leading-[1] tracking-[-0.055em] text-[#111712] sm:text-[42px]">
              {t('Hedefi değiştir. İddia değil, test edilecek hipotez üret.', 'Change the target. Produce a testable hypothesis, not a claim.')}
            </h2>
            <p className="mt-4 max-w-lg text-[10px] leading-5 text-[#697169]">
              {t('Bu kontrol gerçek pilot sonucu değildir. 2025 baz çizgisi üzerinde “önleme” ve “geri kazanım” varsayımlarının ne ifade ettiğini gösterir.', 'This control is not a real pilot result. It shows what prevention and recovery assumptions mean against the 2025 baseline.')}
            </p>
          </div>

          <div className="bc-workbench rounded-2xl p-5 sm:p-6">
            <div className="grid gap-6 sm:grid-cols-2">
              <RangeControl
                id="prevention-rate"
                label={t('Kaynakta önleme', 'Prevention at source')}
                value={preventionRate}
                min={0}
                max={30}
                onChange={setPreventionRate}
              />
              <RangeControl
                id="recovery-rate"
                label={t('Geri kazanım oranı', 'Recovery rate')}
                value={recoveryRate}
                min={0}
                max={100}
                onChange={setRecoveryRate}
              />
            </div>

            <div className="mt-6 grid grid-cols-2 border-y border-[#111712]/10 lg:grid-cols-4">
              <ScenarioMetric label={t('Önlenen', 'Prevented')} value={formatKg(scenario.preventedKg, locale)} />
              <ScenarioMetric label={t('Kalan atık', 'Remaining waste')} value={formatKg(scenario.remainingWasteKg, locale)} />
              <ScenarioMetric label={t('Geri kazanılan', 'Recovered')} value={formatKg(scenario.recoveredKg, locale)} />
              <ScenarioMetric label={t('Rezidüel', 'Residual')} value={formatKg(scenario.residualKg, locale)} />
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-[#111712]/10 bg-[#e9e5dc] p-6 sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,.72fr)_minmax(0,1.28fr)] lg:gap-12">
          <div>
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#5f685f]"><Gauge size={11} /> {t('Pilot sözleşmesi', 'Pilot contract')}</div>
            <h2 className="mt-3 text-[31px] font-black leading-[1] tracking-[-0.05em] text-[#111712]">{t('Başarı kriteri demodan önce sabit.', 'Success is defined before the demo result exists.')}</h2>
          </div>
          <div className="divide-y divide-[#111712]/10 border-y border-[#111712]/10">
            <ContractRow label={t('Süre', 'Duration')} value={`${FOOD_WASTE_PILOT_PROTOCOL.durationDays} ${t('gün', 'days')}`} />
            <ContractRow label={t('Minimum kanıt', 'Minimum evidence')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm} ${t('servis / kol', 'services / arm')}`} />
            <ContractRow label={t('Birincil metrik', 'Primary metric')} value={FOOD_WASTE_PILOT_PROTOCOL.primaryMetric.label} />
            <ContractRow label={t('Başarı kapısı', 'Success gate')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}% ${t('normalize atık azalması', 'normalized waste reduction')}`} />
            <ContractRow label={t('Güvenlik', 'Safety')} value={t('Erken tükenme artmayacak; gıda güvenliği süreci bypass edilemez.', 'Early sell-out must not increase; food-safety process cannot be bypassed.')} />
          </div>
        </div>
      </section>
    </div>
  );
}

function ReadinessBadge({ readiness }: { readiness: DecisionReadiness }) {
  if (readiness === 'PILOT_READY') return <StatusBadge label="PILOT_READY" tone="ready" />;
  if (readiness === 'REVIEW_REQUIRED') return <StatusBadge label="REVIEW_REQUIRED" tone="review" />;
  return <StatusBadge label="WITHHOLD" tone="hold" />;
}

function StatusBadge({ label, tone }: { label: string; tone: 'ready' | 'review' | 'hold' | 'neutral' }) {
  const className = {
    ready: 'border-[#66895a]/30 bg-[#edf3e8] text-[#47683d]',
    review: 'border-[#9c7a40]/25 bg-[#f6efdf] text-[#7b5e30]',
    hold: 'border-[#875951]/25 bg-[#f4e8e5] text-[#744840]',
    neutral: 'border-[#111712]/10 bg-[#efede7] text-[#6c736d]',
  }[tone];

  return <span className={`rounded-md border px-2 py-1 font-mono text-[8px] font-black ${className}`}>{label}</span>;
}

function BandMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[8px] font-black uppercase tracking-[0.14em] text-[#858b85]">{label}</div>
      <div className="bc-mono mt-1 text-[20px] font-black tracking-[-0.035em] text-[#111712]">{value}</div>
    </div>
  );
}

function DecisionButton({ active, disabled = false, onClick, label, detail }: { active: boolean; disabled?: boolean; onClick: () => void; label: string; detail: string }) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`bc-focus-ring min-h-[78px] rounded-lg border p-3 text-left transition ${disabled ? 'cursor-not-allowed border-[#111712]/8 bg-[#e8e5de] text-[#9a9f9a]' : active ? 'border-[#18372b] bg-[#18372b] text-white' : 'border-[#111712]/10 bg-white text-[#293129] hover:border-[#18372b]/35'}`}
    >
      <div className="text-[10px] font-black">{label}</div>
      <div className={`mt-1 text-[8px] font-bold leading-4 ${active ? 'text-white/55' : 'text-[#838983]'}`}>{detail}</div>
    </button>
  );
}

function DecisionResult({ decision, t }: { decision: OperatorDecision; t: (tr: string, en: string) => string }) {
  const message = decision === 'PILOT_APPROVED'
    ? t('PILOT_APPROVED · UI-only. Harici üretim komutu gönderilmedi.', 'PILOT_APPROVED · UI-only. No external production command was sent.')
    : decision === 'EDIT_REQUIRED'
      ? t('EDIT_REQUIRED · Öneri operatör revizyonuna döndü.', 'EDIT_REQUIRED · Recommendation returned for operator revision.')
      : t('HOLD · Güvenli varsayılan. Otomatik dispatch kapalı.', 'HOLD · Safe default. Automatic dispatch is disabled.');

  return (
    <div className="mt-3 flex items-start gap-2 rounded-lg border border-[#111712]/10 bg-white px-3.5 py-3 text-[9px] font-bold leading-4 text-[#626a63]">
      <ArrowRight size={11} className="mt-0.5 shrink-0 text-[#315846]" /> {message}
    </div>
  );
}

function DarkMetric({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3 py-4">
      <div>
        <div className="text-[9px] font-bold text-white/48">{label}</div>
        {note && <div className="mt-0.5 text-[7px] font-black uppercase tracking-[0.1em] text-[#b9da72]/70">{note}</div>}
      </div>
      <div className="bc-mono text-[14px] font-black text-white">{value}</div>
    </div>
  );
}

function RangeControl({ id, label, value, min, max, onChange }: { id: string; label: string; value: number; min: number; max: number; onChange: (value: number) => void }) {
  return (
    <label htmlFor={id} className="block">
      <div className="flex items-end justify-between gap-3">
        <span className="text-[9px] font-black uppercase tracking-[0.14em] text-[#747c75]">{label}</span>
        <span className="bc-mono text-[22px] font-black tracking-[-0.04em] text-[#111712]">{value}%</span>
      </div>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={event => onChange(Number(event.target.value))}
        className="mt-3 w-full accent-[#18372b]"
      />
      <div className="mt-1 flex justify-between font-mono text-[7px] font-bold text-[#969b96]"><span>{min}%</span><span>{max}%</span></div>
    </label>
  );
}

function ScenarioMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="border-[#111712]/10 py-4 pr-3 sm:[&:nth-child(even)]:border-l sm:[&:nth-child(even)]:pl-4 lg:border-l lg:px-4 lg:first:border-l-0 lg:first:pl-0">
      <div className="text-[8px] font-black uppercase tracking-[0.14em] text-[#858b85]">{label}</div>
      <div className="bc-mono mt-1.5 text-[17px] font-black tracking-[-0.03em] text-[#111712]">{value}</div>
    </div>
  );
}

function ContractRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1 py-4 sm:grid-cols-[150px_minmax(0,1fr)] sm:gap-5">
      <div className="text-[8px] font-black uppercase tracking-[0.14em] text-[#7a827b]">{label}</div>
      <div className="text-[10px] font-bold leading-5 text-[#303831]">{value}</div>
    </div>
  );
}
