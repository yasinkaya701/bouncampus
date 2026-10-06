'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  CircleAlert,
  Database,
  Gauge,
  ShieldCheck,
  TimerReset,
  Utensils,
} from 'lucide-react';
import {
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  type DecisionReadiness,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type ProductionBand = {
  policyVersion: string;
  predictedMeals: number;
  lowerBound: number;
  recommendedTarget: number;
  upperBound: number;
  signalCoveragePct: number;
  decisionReadiness: DecisionReadiness;
  provenance: 'MODEL_ESTIMATE';
  decisionProvenance: 'POLICY_HEURISTIC';
  bandSemantics: 'PLANNING_RANGE_NOT_CALIBRATED_INTERVAL';
  calibrationStatus: 'NOT_CALIBRATED';
  signals: Array<{
    id: string;
    label: string;
    available: boolean;
    weightPct: number;
    weightBasis: 'POLICY_HEURISTIC';
  }>;
  reasonCodes?: string[];
};

type FoodApi = {
  demandContext?: {
    available?: boolean;
    actionable?: boolean;
    productionBand?: ProductionBand | null;
  };
};

type DemoHealth = 'LOADING' | 'LIVE' | 'PARTIAL' | 'FALLBACK';

const STEP_SECONDS = [16, 20, 18, 22, 14];

export default function JuryModePage() {
  const { locale, t } = useLocale();
  const [step, setStep] = useState(0);
  const [food, setFood] = useState<FoodApi | null>(null);
  const [health, setHealth] = useState<DemoHealth>('LOADING');
  const [operatorGate, setOperatorGate] = useState<'HOLD' | 'PILOT_APPROVED'>('HOLD');

  useEffect(() => {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 2500);

    fetch('/api/v1/food', { cache: 'no-store', signal: controller.signal })
      .then(async response => {
        if (!response.ok) throw new Error('food api unavailable');
        const payload = await response.json() as FoodApi;
        setFood(payload);
        const productionBand = payload.demandContext?.productionBand;
        setHealth(payload.demandContext?.available && payload.demandContext?.actionable && productionBand ? 'LIVE' : 'PARTIAL');
      })
      .catch(() => {
        setFood(null);
        setHealth('FALLBACK');
      })
      .finally(() => window.clearTimeout(timeout));

    return () => {
      window.clearTimeout(timeout);
      controller.abort();
    };
  }, []);

  const band = food?.demandContext?.productionBand ?? null;
  const canPilot = health === 'LIVE' && band?.decisionReadiness === 'PILOT_READY';
  const elapsed = useMemo(() => STEP_SECONDS.slice(0, step).reduce((sum, value) => sum + value, 0), [step]);
  const nf = (value: number) => Math.round(value).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US');

  const next = () => setStep(current => Math.min(STEP_SECONDS.length - 1, current + 1));
  const previous = () => setStep(current => Math.max(0, current - 1));

  return (
    <div className="space-y-5">
      <section className="bc-panel-dark bc-grid-bg rounded-[28px] p-5 text-white sm:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <Link href="/food-waste" className="inline-flex items-center gap-1.5 text-[9px] font-black text-white/50 hover:text-white"><ArrowLeft size={11} /> {t('Operasyon ekranı', 'Operations workspace')}</Link>
            <div className="mt-4 inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]"><TimerReset size={12} /> {t('Jury Mode v3 · 90 saniye', 'Jury Mode v3 · 90 seconds')}</div>
            <h1 className="mt-3 max-w-4xl text-[38px] font-black leading-[.98] tracking-[-0.06em] sm:text-[52px]">{t('Tek problem. Tek karar. Tek pilot. Sıfır sahte sonuç.', 'One problem. One decision. One pilot. Zero fabricated outcomes.')}</h1>
          </div>
          <HealthBadge health={health} t={t} />
        </div>

        <div className="mt-6 grid grid-cols-5 gap-1.5">
          {STEP_SECONDS.map((seconds, index) => (
            <button key={seconds} type="button" onClick={() => setStep(index)} className={`rounded-xl border px-2 py-2 text-left transition ${index === step ? 'border-[#b8e467] bg-[#b8e467] text-[#071c33]' : 'border-white/10 bg-white/[0.04] text-white/55'}`}>
              <div className="font-mono text-[7px] font-black">0{index + 1}</div>
              <div className="mt-1 hidden text-[8px] font-black sm:block">{stepLabel(index, t)}</div>
              <div className="mt-1 font-mono text-[7px] opacity-55">~{seconds}s</div>
            </button>
          ))}
        </div>
      </section>

      <section className="rounded-[26px] border border-slate-900/10 bg-white p-5 sm:p-7">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3 border-b border-slate-900/8 pb-4">
          <div>
            <div className="bc-eyebrow">{t('Sunucu notu', 'Presenter cue')} · {elapsed}–{elapsed + STEP_SECONDS[step]}s</div>
            <div className="mt-1 text-[10px] font-black text-slate-600">{presenterCue(step, t)}</div>
          </div>
          <div className="font-mono text-[9px] font-black text-slate-400">STEP {step + 1}/5</div>
        </div>

        {step === 0 ? <ProblemStep nf={nf} t={t} /> : null}
        {step === 1 ? <DecisionStep band={band} health={health} nf={nf} t={t} /> : null}
        {step === 2 ? <HumanGateStep canPilot={canPilot} operatorGate={operatorGate} setOperatorGate={setOperatorGate} band={band} t={t} /> : null}
        {step === 3 ? <EvidenceStep t={t} /> : null}
        {step === 4 ? <CloseStep t={t} /> : null}
      </section>

      <section className="grid gap-3 lg:grid-cols-[1fr_auto] lg:items-center">
        <DemoHealthPanel health={health} band={band} t={t} />
        <div className="flex justify-end gap-2">
          <button type="button" disabled={step === 0} onClick={previous} className="rounded-xl border border-slate-900/10 bg-white px-4 py-3 text-[9px] font-black text-slate-600 disabled:opacity-30">{t('Geri', 'Back')}</button>
          {step < 4 ? (
            <button type="button" onClick={next} className="inline-flex items-center gap-2 rounded-xl bg-[#071c33] px-5 py-3 text-[9px] font-black text-white">{t('Sonraki kanıt', 'Next proof')} <ArrowRight size={12} /></button>
          ) : (
            <button type="button" onClick={() => setStep(0)} className="rounded-xl bg-[#173f67] px-5 py-3 text-[9px] font-black text-white">{t('90 saniyeyi sıfırla', 'Reset 90 seconds')}</button>
          )}
        </div>
      </section>
    </div>
  );
}

function ProblemStep({ nf, t }: { nf: (value: number) => string; t: (tr: string, en: string) => string }) {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_.9fr] lg:items-center">
      <div>
        <div className="bc-eyebrow">01 · {t('GERÇEK PROBLEM', 'REAL PROBLEM')}</div>
        <h2 className="mt-3 text-[34px] font-black leading-none tracking-[-0.05em] text-slate-950">{t('İlk sayı model çıktısı değil.', 'The first number is not a model output.')}</h2>
        <p className="mt-4 max-w-2xl text-[11px] leading-6 text-slate-500">{t('Boğaziçi’nin yayımladığı 2025 yemek atığı baz çizgisiyle başlıyoruz. Ürün problemi kanıtlamak için sentetik veri üretmiyor.', 'We start from Boğaziçi University’s published 2025 food-waste baseline. The product does not fabricate synthetic data to prove the problem exists.')}</p>
        <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-2 text-[9px] font-black text-[#173f67]"><Database size={12} /> {t('Resmi kaynak', 'Official source')}</a>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <BigMetric label={t('2025 atık', '2025 waste')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg)} kg`} tag="OFFICIAL_PUBLIC" />
        <BigMetric label={t('Geri kazanım', 'Recovery')} value={`${nf(FOOD_WASTE_BASELINE.year2025RecoveredKg)} kg`} tag="OFFICIAL_PUBLIC" />
        <BigMetric label={t('Yemekhane kapasitesi', 'Dining capacity')} value={nf(FOOD_WASTE_BASELINE.diningHallCapacity)} tag="OFFICIAL_PUBLIC" />
        <BigMetric label={t('Yemekhaneli kampüs', 'Campuses with dining')} value={`${FOOD_WASTE_BASELINE.campusesWithDining}`} tag="OFFICIAL_PUBLIC" />
      </div>
    </div>
  );
}

function DecisionStep({ band, health, nf, t }: { band: ProductionBand | null; health: DemoHealth; nf: (value: number) => string; t: (tr: string, en: string) => string }) {
  if (!band || health === 'FALLBACK') {
    return (
      <div>
        <div className="bc-eyebrow">02 · {t('KARAR KALİTESİ', 'DECISION QUALITY')}</div>
        <h2 className="mt-3 text-[34px] font-black tracking-[-0.05em] text-slate-950">WITHHOLD</h2>
        <p className="mt-3 max-w-3xl text-[11px] leading-6 text-slate-500">{t('Gerekli bağlam yoksa sistem operasyonel sayı uydurmuyor. Resmi problem kanıtı görünür kalıyor; üretim önerisi güvenli biçimde bekletiliyor.', 'If required context is unavailable, the system does not invent an operational number. Official problem evidence remains visible while the production recommendation is safely withheld.')}</p>
        <div className="mt-5 grid gap-2 sm:grid-cols-4">
          <SignalContract label={t('Ders programı', 'Course schedule')} weight="50% POLICY" />
          <SignalContract label={t('Hava', 'Weather')} weight="20% POLICY" />
          <SignalContract label={t('Menü', 'Menu')} weight="20% POLICY" />
          <SignalContract label={t('Akademik takvim', 'Academic calendar')} weight="10% POLICY" />
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="bc-eyebrow">02 · {t('KARAR KALİTESİ', 'DECISION QUALITY')}</div>
      <div className="mt-3 flex flex-wrap items-center gap-3"><h2 className="text-[34px] font-black tracking-[-0.05em] text-slate-950">{band.decisionReadiness === 'PILOT_READY' ? t('PROTOTİP KAPISI GEÇTİ', 'PROTOTYPE GATE PASS') : band.decisionReadiness}</h2><span className="rounded-full bg-slate-100 px-3 py-1 font-mono text-[8px] font-black text-slate-600">{band.signalCoveragePct}% POLICY COVERAGE</span></div>
      <div className="mt-5 grid gap-3 sm:grid-cols-4">
        <BigMetric label={t('Nokta tahmini', 'Point forecast')} value={nf(band.predictedMeals)} tag="MODEL_ESTIMATE" />
        <BigMetric label={t('Alt planlama sınırı', 'Lower planning bound')} value={nf(band.lowerBound)} tag="POLICY_HEURISTIC" />
        <BigMetric label={t('Operatör başlangıcı', 'Operator starting point')} value={nf(band.recommendedTarget)} tag="POLICY_HEURISTIC" />
        <BigMetric label={t('Üst planlama sınırı', 'Upper planning bound')} value={nf(band.upperBound)} tag="POLICY_HEURISTIC" />
      </div>
      <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-[8px] font-black leading-5 text-amber-900">
        {band.provenance} → {band.decisionProvenance} · {band.calibrationStatus} · {band.bandSemantics}
      </div>
      <div className="mt-5 grid gap-2 sm:grid-cols-4">
        {band.signals.map(signal => <SignalState key={signal.id} label={signal.label} weight={signal.weightPct} available={signal.available} />)}
      </div>
      {band.reasonCodes?.length ? <div className="mt-4 rounded-xl bg-amber-50 p-3 font-mono text-[8px] font-black text-amber-900">WHY: {band.reasonCodes.join(' · ')}</div> : null}
    </div>
  );
}

function HumanGateStep({ canPilot, operatorGate, setOperatorGate, band, t }: { canPilot: boolean; operatorGate: 'HOLD' | 'PILOT_APPROVED'; setOperatorGate: (value: 'HOLD' | 'PILOT_APPROVED') => void; band: ProductionBand | null; t: (tr: string, en: string) => string }) {
  return (
    <div>
      <div className="bc-eyebrow">03 · {t('İNSAN KAPISI', 'HUMAN GATE')}</div>
      <h2 className="mt-3 text-[34px] font-black tracking-[-0.05em] text-slate-950">{t('AI mutfağa tek başına komut vermez.', 'AI never dispatches to the kitchen alone.')}</h2>
      <p className="mt-3 max-w-3xl text-[11px] leading-6 text-slate-500">{t('Prototip senaryo kapısı yalnız gerekli bağlam erişilebilir ve iç politika durumu PILOT_READY iken açılır. Bu, kurumsal pilot onayı değildir; buton harici mutfak sistemine dispatch yapmaz.', 'The prototype scenario gate opens only when required context is available and the internal policy state is PILOT_READY. This is not institutional pilot approval, and the button does not dispatch to an external kitchen system.')}</p>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <button type="button" disabled={!canPilot} onClick={() => setOperatorGate('PILOT_APPROVED')} className={`rounded-[20px] border p-5 text-left ${operatorGate === 'PILOT_APPROVED' ? 'border-emerald-700 bg-emerald-700 text-white' : 'border-slate-900/10 bg-white text-slate-900'} disabled:cursor-not-allowed disabled:opacity-35`}><CheckCircle2 size={17} /><div className="mt-5 text-[12px] font-black">{t('Danışmanlık senaryosunu hazır işaretle', 'Mark advisory scenario ready')}</div><div className="mt-1 text-[9px] opacity-55">{band?.decisionReadiness === 'PILOT_READY' ? t('PROTOTİP KAPISI GEÇTİ', 'PROTOTYPE GATE PASS') : band?.decisionReadiness ?? 'WITHHOLD'} · AUTO_DISPATCH=false</div></button>
        <button type="button" onClick={() => setOperatorGate('HOLD')} className={`rounded-[20px] border p-5 text-left ${operatorGate === 'HOLD' ? 'border-slate-950 bg-slate-950 text-white' : 'border-slate-900/10 bg-white text-slate-900'}`}><ShieldCheck size={17} /><div className="mt-5 text-[12px] font-black">{t('Beklet / gözden geçir', 'Hold / review')}</div><div className="mt-1 text-[9px] opacity-55">{t('Varsayılan güvenli durum', 'Safe default')}</div></button>
      </div>
    </div>
  );
}

function EvidenceStep({ t }: { t: (tr: string, en: string) => string }) {
  return (
    <div>
      <div className="bc-eyebrow">04 · {t('ÖNERİLEN YANLIŞLANABİLİR PİLOT', 'PROPOSED FALSIFIABLE PILOT')}</div>
      <h2 className="mt-3 text-[34px] font-black tracking-[-0.05em] text-slate-950">{t('Başarıyı model değil, gelecekteki ölçüm ilan edebilir.', 'Only prospective measurement can declare success.')}</h2>
      <p className="mt-3 max-w-3xl text-[10px] leading-5 text-slate-500">{t('Bu ekran çalıştırılmış bir pilot sonucu göstermiyor; henüz uygulanmamış, yanlışlanabilir bir ölçüm protokolünü gösteriyor.', 'This screen does not show an executed pilot result; it shows a proposed, falsifiable measurement protocol that has not yet been run.')}</p>
      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        <BigMetric label={t('Ana KPI', 'Primary KPI')} value={t('kg / 100 öğün', 'kg / 100 meals')} tag="PROPOSED_PROTOCOL" />
        <BigMetric label={t('Hedef', 'Target')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} tag="ILLUSTRATIVE_TARGET_NOT_RESULT" />
        <BigMetric label={t('Minimum kanıt', 'Minimum evidence')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}+${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} tag="CONTROL+INTERVENTION" />
      </div>
      <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-[9px] leading-5 text-amber-900">{t('Erken tükenme artarsa, data-quality gate geçmezse veya gıda güvenliği süreci geçmezse PROMISING sonucu verilemez. İklim etkisi ancak gerçek ölçümden sonra ayrıca hesaplanabilir.', 'If early sell-out increases, the data-quality gate fails, or food-safety review fails, the intervention cannot be called PROMISING. Climate impact can only be calculated separately after real measurement.')}</div>
      <Link href="/food-waste/pilot" className="mt-4 inline-flex items-center gap-2 rounded-xl bg-[#173f67] px-4 py-3 text-[9px] font-black text-white"><Gauge size={12} /> {t('Pilot Evidence Lab’i aç', 'Open Pilot Evidence Lab')}</Link>
    </div>
  );
}

function CloseStep({ t }: { t: (tr: string, en: string) => string }) {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.15fr_.85fr] lg:items-center">
      <div>
        <div className="bc-eyebrow">05 · {t('KAPANIŞ', 'CLOSE')}</div>
        <h2 className="mt-3 text-[36px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950">{t('48 tonluk problemi raporlamıyoruz; bir sonraki öğünde oluşmasını azaltabilecek kararı test ediyoruz.', 'We are not merely reporting the 48-ton problem; we are testing a decision that may reduce waste in the next service.')}</h2>
        <p className="mt-4 text-[12px] font-black leading-6 text-[#173f67]">{t('Ama başarıyı AI söylemiyor — ancak gelecekteki doğrulanmış ölçüm söyleyebilir.', 'But AI does not declare victory — only future verified measurement can.')}</p>
      </div>
      <div className="rounded-[22px] bg-[#071c33] p-5 text-white">
        <div className="text-[8px] font-black uppercase tracking-[0.13em] text-[#b8e467]">{t('Ölçekleme kuralı', 'Scaling rule')}</div>
        <div className="mt-3 text-[17px] font-black">{t('Önce kanıt → sonra etki hesabı → sonra kampüs ölçeği.', 'Evidence first → impact accounting second → campus scale third.')}</div>
        <div className="mt-4 flex items-center gap-2 text-[9px] text-white/55"><Utensils size={12} /> {t('Enerji, mobilite ve 3D modüller platform genişlemesidir; pitch’in başlangıcı değildir.', 'Energy, mobility and 3D remain platform expansion modules; they are not the opening pitch.')}</div>
      </div>
    </div>
  );
}

function DemoHealthPanel({ health, band, t }: { health: DemoHealth; band: ProductionBand | null; t: (tr: string, en: string) => string }) {
  return (
    <div className="grid gap-2 rounded-[20px] border border-slate-900/10 bg-[#f7f9f6] p-4 sm:grid-cols-3">
      <HealthItem label={t('Resmi baz çizgi', 'Official baseline')} value="READY" good />
      <HealthItem label={t('Canlı bağlam', 'Live context')} value={health} good={health === 'LIVE'} />
      <HealthItem label={t('Prototip aksiyon kapısı', 'Prototype action gate')} value={band?.decisionReadiness === 'PILOT_READY' ? t('GEÇTİ', 'PASS') : band?.decisionReadiness ?? 'WITHHOLD'} good={band?.decisionReadiness === 'PILOT_READY'} />
    </div>
  );
}

function HealthBadge({ health, t }: { health: DemoHealth; t: (tr: string, en: string) => string }) {
  const cls = health === 'LIVE' ? 'bg-emerald-400/15 text-emerald-200' : health === 'LOADING' ? 'bg-white/10 text-white/55' : 'bg-amber-400/15 text-amber-200';
  const label = health === 'FALLBACK' ? t('FAIL-SAFE MOD', 'FAIL-SAFE MODE') : health;
  return <div className={`rounded-full px-3 py-2 font-mono text-[8px] font-black ${cls}`}>{label}</div>;
}

function BigMetric({ label, value, tag }: { label: string; value: string; tag: string }) {
  return <div className="rounded-[18px] border border-slate-900/10 bg-[#f7f9f6] p-4"><div className="text-[8px] font-black uppercase tracking-[0.09em] text-slate-400">{label}</div><div className="mt-2 font-mono text-[22px] font-black text-slate-950">{value}</div><div className="mt-2 font-mono text-[7px] font-black text-slate-400">{tag}</div></div>;
}

function SignalState({ label, weight, available }: { label: string; weight: number; available: boolean }) {
  return <div className={`rounded-xl border p-3 ${available ? 'border-emerald-200 bg-emerald-50' : 'border-amber-200 bg-amber-50'}`}><div className="text-[8px] font-black text-slate-700">{label}</div><div className="mt-2 flex justify-between font-mono text-[7px] font-black"><span>{weight}% POLICY</span><span>{available ? 'AVAILABLE' : 'MISSING'}</span></div></div>;
}

function SignalContract({ label, weight }: { label: string; weight: string }) {
  return <div className="rounded-xl border border-slate-900/10 bg-[#f7f9f6] p-3"><div className="text-[8px] font-black text-slate-700">{label}</div><div className="mt-2 font-mono text-[8px] font-black text-slate-400">{weight}</div></div>;
}

function HealthItem({ label, value, good }: { label: string; value: string; good: boolean }) {
  return <div className="flex items-center gap-2"><span className={`inline-flex h-6 w-6 items-center justify-center rounded-full ${good ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>{good ? <CheckCircle2 size={12} /> : <CircleAlert size={12} />}</span><div><div className="text-[7px] font-black uppercase tracking-[0.08em] text-slate-400">{label}</div><div className="font-mono text-[8px] font-black text-slate-700">{value}</div></div></div>;
}

function stepLabel(index: number, t: (tr: string, en: string) => string) {
  return [t('Problem', 'Problem'), t('Karar', 'Decision'), t('İnsan kapısı', 'Human gate'), t('Pilot', 'Pilot'), t('Kapanış', 'Close')][index];
}

function presenterCue(index: number, t: (tr: string, en: string) => string) {
  return [
    t('48.251 kg sayısıyla aç. Bunun resmi kaynak olduğunu söyle.', 'Open with 48,251 kg and say it is official public data.'),
    t('Nokta tahmini MODEL_ESTIMATE; bant ve eşikler POLICY_HEURISTIC. Eksik gerekli bağlamda WITHHOLD.', 'Point forecast is MODEL_ESTIMATE; range and thresholds are POLICY_HEURISTIC. Missing required context forces WITHHOLD.'),
    t('Bir kez HOLD’a, yalnız uygunsa bir kez pilot onayına bas.', 'Tap HOLD once, and approve the pilot only if eligible.'),
    t('≥10% hedefin sonuç olmadığını özellikle söyle ve Evidence Lab’i göster.', 'Explicitly say ≥10% is a target, not a result, and show the Evidence Lab.'),
    t('Kapanışta “test ediyoruz” de; başarıyı yalnız ölçümün ilan edeceğini vurgula.', 'Close with “we are testing it” and stress that only measurement can declare success.'),
  ][index];
}
