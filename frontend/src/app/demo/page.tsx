'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Download,
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
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  simulateFoodWasteScenario,
  YEAR_OVER_YEAR_REDUCTION_PCT,
  type DecisionReadiness,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type FoodApi = {
  demandContext: {
    available: boolean;
    productionBand: null | {
      predictedMeals: number;
      lowerBound: number;
      recommendedTarget: number;
      upperBound: number;
      signalCoveragePct: number;
      decisionReadiness: DecisionReadiness;
      signals: Array<{ id: string; label: string; available: boolean; weightPct: number }>;
      provenance: 'MODEL_ESTIMATE';
    };
  };
};

export default function DemoPage() {
  const { locale, t } = useLocale();
  const [food, setFood] = useState<FoodApi | null>(null);
  const [prevention, setPrevention] = useState(15);
  const [recovery, setRecovery] = useState(85);
  const [operatorGate, setOperatorGate] = useState<'HOLD' | 'PILOT_APPROVED'>('HOLD');
  const scenario = useMemo(() => simulateFoodWasteScenario(prevention, recovery), [prevention, recovery]);

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then(setFood)
      .catch(() => setFood(null));
  }, []);

  const nf = (value: number) => Math.round(value).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US');
  const band = food?.demandContext.productionBand;
  const canPilot = band?.decisionReadiness === 'PILOT_READY';

  return (
    <div className="space-y-8">
      <section className="bc-panel-dark bc-grid-bg rounded-[28px] p-6 text-white sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_.8fr] lg:items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.18em] text-[#b8e467]"><Sparkles size={12} /> {t('KREATE jüri akışı · 90 saniye', 'KREATE jury flow · 90 seconds')}</div>
            <h1 className="mt-4 max-w-4xl text-[42px] font-black leading-[.98] tracking-[-0.06em] sm:text-[58px]">{t('Problemi kanıtla. Kararı üret. İnsanla sınırla. Pilotta yanlışlanabilir hale getir.', 'Prove the problem. Produce the decision. Bound it with a human. Make it falsifiable in a pilot.')}</h1>
            <p className="mt-4 max-w-3xl text-[12px] leading-6 text-white/58">{t('Jürinin görmesi gereken şey “AI dashboard” değil: gerçek problemden güvenli operasyona ve ölçülebilir iklim sonucuna giden kapalı döngü.', 'The jury should not see another “AI dashboard”; they should see a closed loop from a real problem to safe operations and a measurable climate outcome.')}</p>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <TopMetric label={t('2025 atık', '2025 waste')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg)} kg`} />
            <TopMetric label={t('Yıllık değişim', 'YoY change')} value={`−${YEAR_OVER_YEAR_REDUCTION_PCT.toFixed(1)}%`} />
            <TopMetric label={t('Pilot hedefi', 'Pilot target')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} />
          </div>
        </div>
      </section>

      <JuryStep number="01" kicker={t('PROBLEM', 'PROBLEM')} title={t('İlk sayı model çıktısı değil.', 'The first number is not a model output.')} body={t('Boğaziçi Üniversitesi 2025 için 48.251 kg yemek atığı yayımlıyor. Ürün bu resmi baz çizgiden başlıyor; “sorun var” demek için yapay veri üretmiyor.', 'Boğaziçi University publishes 48,251 kg of food waste for 2025. The product begins from that official baseline; it does not fabricate data to prove a problem exists.')}>
        <div className="grid gap-3 sm:grid-cols-3">
          <ProofCard label={t('2025 toplam atık', '2025 total waste')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg)} kg`} provenance="OFFICIAL_PUBLIC" />
          <ProofCard label={t('İSTAÇ geri kazanımı', 'İSTAÇ recovery')} value={`${nf(FOOD_WASTE_BASELINE.year2025RecoveredKg)} kg`} provenance="OFFICIAL_PUBLIC" />
          <ProofCard label={t('Mevcut artık yük', 'Current residual load')} value={`${nf(FOOD_WASTE_BASELINE.year2025WasteKg - FOOD_WASTE_BASELINE.year2025RecoveredKg)} kg`} provenance="DERIVED_FROM_OFFICIAL" />
        </div>
        <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="mt-3 inline-flex items-center gap-1 text-[9px] font-black text-[#173f67]">{t('Resmi kaynağı aç', 'Open official source')} <ExternalLink size={10} /></a>
      </JuryStep>

      <JuryStep number="02" kicker={t('DECISION', 'DECISION')} title={t('Tahminin yanında karar kalitesini de göster.', 'Show decision quality next to the forecast.')} body={t('Model ders programını omurga sinyali kabul eder; hava, menü ve akademik takvim bağlamı arttıkça belirsizlik bandı daralır. Kritik bağlam yoksa karar WITHHOLD olur.', 'The model treats course schedules as the backbone signal; weather, menu and academic-calendar context narrow uncertainty. If critical context is missing, the decision is WITHHOLD.')}>
        {band ? (
          <div className="rounded-[22px] border border-slate-900/10 bg-white p-5">
            <div className="grid gap-3 sm:grid-cols-4">
              <BandMetric label={t('Talep tahmini', 'Demand forecast')} value={nf(band.predictedMeals)} />
              <BandMetric label={t('Alt bant', 'Lower band')} value={nf(band.lowerBound)} />
              <BandMetric label={t('Başlangıç', 'Starting point')} value={nf(band.recommendedTarget)} />
              <BandMetric label={t('Üst bant', 'Upper band')} value={nf(band.upperBound)} />
            </div>
            <div className="mt-4 grid gap-3 lg:grid-cols-[.4fr_.6fr]">
              <div className="rounded-xl bg-[#f7f9f6] p-4">
                <div className="text-[8px] font-black uppercase tracking-[0.11em] text-slate-400">{t('Karar durumu', 'Decision readiness')}</div>
                <div className="mt-2 flex items-center gap-2"><Readiness readiness={band.decisionReadiness} /><span className="font-mono text-[9px] font-black text-slate-500">{band.signalCoveragePct}%</span></div>
              </div>
              <div className="grid grid-cols-2 gap-2">
                {band.signals.map(signal => <SignalPill key={signal.id} label={signal.label} available={signal.available} />)}
              </div>
            </div>
            <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-[9px] leading-4 text-amber-900"><strong>MODEL_ESTIMATE.</strong> {t('Bu sayı POS ya da gerçek üretim telemetrisi değildir.', 'This is not POS or actual production telemetry.')}</div>
          </div>
        ) : <EmptyDecision text={t('Bağlam yoksa sistem sayı uydurmaz; öneri bekletilir.', 'If context is unavailable, the system does not invent a number; advice is withheld.')} />}
      </JuryStep>

      <JuryStep number="03" kicker={t('HUMAN GATE', 'HUMAN GATE')} title={t('AI hiçbir zaman tek başına mutfağa komut vermez.', 'AI never dispatches to the kitchen on its own.')} body={t('Jüride burada butona bas: sadece PILOT_READY durumda kontrollü pilot onayı verilebilir. Bu ekranın kendisi bile harici sisteme komut göndermez.', 'During the jury demo, press the button here: controlled pilot approval is possible only in PILOT_READY. Even this screen does not send a command to an external system.')}>
        <div className="grid gap-3 sm:grid-cols-[1fr_1fr]">
          <button type="button" disabled={!canPilot} onClick={() => setOperatorGate('PILOT_APPROVED')} className={`rounded-[20px] border p-5 text-left transition ${operatorGate === 'PILOT_APPROVED' ? 'border-emerald-700 bg-emerald-700 text-white' : 'border-slate-900/10 bg-white text-slate-900'} ${!canPilot ? 'cursor-not-allowed opacity-40' : 'hover:-translate-y-0.5'}`}>
            <CheckCircle2 size={16} /><div className="mt-5 text-[12px] font-black">{t('Kontrollü pilotu onayla', 'Approve controlled pilot')}</div><div className="mt-1 text-[9px] opacity-60">{t('Harici dispatch yok', 'No external dispatch')}</div>
          </button>
          <button type="button" onClick={() => setOperatorGate('HOLD')} className={`rounded-[20px] border p-5 text-left transition ${operatorGate === 'HOLD' ? 'border-slate-950 bg-slate-950 text-white' : 'border-slate-900/10 bg-white text-slate-900'} hover:-translate-y-0.5`}>
            <ShieldCheck size={16} /><div className="mt-5 text-[12px] font-black">{t('Beklet / gözden geçir', 'Hold / review')}</div><div className="mt-1 text-[9px] opacity-60">{t('Varsayılan güvenli durum', 'Safe default state')}</div>
          </button>
        </div>
        <div className="mt-3 rounded-xl bg-[#f7f9f6] px-4 py-3 font-mono text-[9px] font-black text-slate-600">{operatorGate} · AUTO_DISPATCH=false</div>
      </JuryStep>

      <section className="bc-panel-dark rounded-[26px] p-6 text-white sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[.72fr_1.28fr]">
          <div>
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-[#b8e467]"><Play size={11} /> {t('04 · SENARYO', '04 · SCENARIO')}</div>
            <h2 className="mt-3 text-[30px] font-black tracking-[-0.05em]">{t('Hedefi stres-test et; sonucu “gerçekleşti” diye sunma.', 'Stress-test the target; never present it as achieved.')}</h2>
            <p className="mt-3 text-[10px] leading-5 text-white/52">{t('Bu bölüm 2025 resmi baz çizgisine uygulanan senaryodur. Pilot sonucu değildir.', 'This section is a scenario applied to the official 2025 baseline. It is not a pilot result.')}</p>
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

      <JuryStep number="05" kicker={t('EVIDENCE', 'EVIDENCE')} title={t('Başarısız olabileceğimiz koşulu önceden yazıyoruz.', 'We define the condition under which we fail before the pilot.')} body={t('Ana KPI kg / 100 servis edilen öğün. Hedef kontrole göre en az %10 azalma; erken tükenme artarsa veya gıda güvenliği süreci bozulursa “kazandık” demiyoruz.', 'Primary KPI is kg / 100 served meals. The target is at least 10% reduction versus control; if early sell-out increases or food-safety process is compromised, we do not call the pilot a success.')}>
        <div className="grid gap-3 sm:grid-cols-3">
          <ProofCard label={t('Ana KPI', 'Primary KPI')} value={t('kg / 100 öğün', 'kg / 100 meals')} provenance="PRE_REGISTERED" />
          <ProofCard label={t('Başarı hedefi', 'Success target')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} provenance="TARGET_NOT_RESULT" />
          <ProofCard label={t('Minimum kanıt', 'Minimum evidence')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}+${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} provenance="CONTROL+INTERVENTION" />
        </div>
        <a href="/api/v1/food/pilot-template" className="mt-4 inline-flex items-center gap-2 rounded-xl bg-[#173f67] px-4 py-2.5 text-[9px] font-black text-white"><Download size={12} /> {t('Ölçüm CSV’sini aç', 'Open measurement CSV')}</a>
      </JuryStep>

      <section className="rounded-[24px] border border-emerald-900/10 bg-emerald-50/70 p-5 sm:p-6">
        <div className="flex items-start gap-3"><Utensils size={18} className="mt-0.5 shrink-0 text-emerald-700" /><div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-emerald-800">{t('Kapanış cümlesi', 'Closing line')}</div><p className="mt-2 max-w-5xl text-[18px] font-black leading-7 tracking-[-0.03em] text-slate-950">{t('“48 tonluk problemi raporlamıyoruz; bir sonraki öğünde önlemeye çalışıyoruz. Ama başarıyı model söylemiyor — kontrollü pilot söylüyor.”', '“We are not reporting the 48-ton problem; we are trying to prevent the next kilogram. But the model does not declare success — the controlled pilot does.”')}</p><Link href="/food-waste" className="mt-4 inline-flex items-center gap-1.5 text-[10px] font-black text-[#173f67]">{t('Tam ürün çalışma alanını aç', 'Open the full product workspace')} <ArrowRight size={10} /></Link></div></div>
      </section>
    </div>
  );
}

function JuryStep({ number, kicker, title, body, children }: { number: string; kicker: string; title: string; body: string; children: React.ReactNode }) {
  return <section className="grid gap-5 border-t border-slate-900/10 pt-6 lg:grid-cols-[.72fr_1.28fr]"><div><div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.15em] text-slate-400"><span className="font-mono text-emerald-700">{number}</span>{kicker}</div><h2 className="mt-2 text-[27px] font-black tracking-[-0.05em] text-slate-950">{title}</h2><p className="mt-3 text-[10px] leading-5 text-slate-500">{body}</p></div><div>{children}</div></section>;
}

function TopMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-white/10 bg-white/[0.06] p-3"><div className="text-[7px] font-black uppercase tracking-[0.1em] text-white/40">{label}</div><div className="mt-2 font-mono text-[17px] font-black">{value}</div></div>;
}

function ProofCard({ label, value, provenance }: { label: string; value: string; provenance: string }) {
  return <div className="rounded-[20px] border border-slate-900/10 bg-white p-5"><div className="text-[8px] font-black uppercase tracking-[0.11em] text-slate-400">{label}</div><div className="mt-4 font-mono text-[24px] font-black tracking-[-0.05em] text-slate-950">{value}</div><div className="mt-3 text-[7px] font-black uppercase tracking-[0.1em] text-emerald-700">{provenance}</div></div>;
}

function BandMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl bg-[#f7f9f6] p-4"><div className="text-[8px] font-black uppercase tracking-[0.1em] text-slate-400">{label}</div><div className="mt-2 font-mono text-[20px] font-black text-slate-950">{value}</div></div>;
}

function Readiness({ readiness }: { readiness: DecisionReadiness }) {
  const cls = readiness === 'PILOT_READY' ? 'bg-emerald-100 text-emerald-800' : readiness === 'REVIEW_REQUIRED' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800';
  return <span className={`rounded-full px-2.5 py-1 font-mono text-[8px] font-black ${cls}`}>{readiness}</span>;
}

function SignalPill({ label, available }: { label: string; available: boolean }) {
  return <div className="flex items-center gap-2 rounded-xl border border-slate-900/[0.07] bg-[#f7f9f6] px-3 py-2 text-[8px] font-black text-slate-600">{available ? <CheckCircle2 size={11} className="text-emerald-600" /> : <AlertTriangle size={11} className="text-amber-600" />}{label}</div>;
}

function EmptyDecision({ text }: { text: string }) {
  return <div className="grid min-h-[150px] place-items-center rounded-[22px] border border-dashed border-slate-300 bg-white p-5 text-center text-[10px] leading-5 text-slate-400"><Gauge size={18} className="mb-2" />{text}</div>;
}

function DemoSlider({ label, value, min, max, onChange }: { label: string; value: number; min: number; max: number; onChange: (value: number) => void }) {
  return <label className="mt-6 block"><div className="flex items-center justify-between text-[9px] font-black uppercase tracking-[0.1em] text-white/60"><span>{label}</span><span className="font-mono text-[#b8e467]">{value}%</span></div><input className="mt-3 w-full accent-[#b8e467]" type="range" min={min} max={max} value={value} onChange={event => onChange(Number(event.target.value))} /></label>;
}

function ScenarioMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-2xl border border-white/10 bg-white/[0.06] p-5"><div className="text-[8px] font-black uppercase tracking-[0.11em] text-white/40">{label}</div><div className="mt-4 font-mono text-[28px] font-black tracking-[-0.05em]">{value}</div><div className="mt-2 text-[8px] font-black uppercase tracking-[0.1em] text-amber-300">SCENARIO_NOT_RESULT</div></div>;
}
