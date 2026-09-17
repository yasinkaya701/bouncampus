'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, CheckCircle2, FlaskConical, Plus, ShieldCheck, Trash2 } from 'lucide-react';
import { FOOD_WASTE_PILOT_PROTOCOL, type PilotScorecard } from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type DraftRow = {
  id: string;
  arm: 'CONTROL' | 'INTERVENTION';
  date: string;
  forecast: string;
  produced: string;
  served: string;
  surplusKg: string;
  wasteKg: string;
  earlySellout: boolean;
  operatorOverride: boolean;
  notes: string;
};

type ScoreResponse = {
  scorecard?: PilotScorecard;
  error?: string;
  validationErrors?: Array<{ index: number; message: string }>;
};

function createRow(arm: DraftRow['arm'], index: number): DraftRow {
  return {
    id: `${arm}-${Date.now()}-${index}`,
    arm,
    date: '',
    forecast: '',
    produced: '',
    served: '',
    surplusKg: '',
    wasteKg: '',
    earlySellout: false,
    operatorOverride: false,
    notes: '',
  };
}

export default function FoodWastePilotPage() {
  const { locale, t } = useLocale();
  const [rows, setRows] = useState<DraftRow[]>([
    createRow('CONTROL', 0),
    createRow('INTERVENTION', 1),
  ]);
  const [score, setScore] = useState<PilotScorecard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const counts = useMemo(() => ({
    control: rows.filter(row => row.arm === 'CONTROL').length,
    intervention: rows.filter(row => row.arm === 'INTERVENTION').length,
  }), [rows]);

  const updateRow = <K extends keyof DraftRow>(id: string, key: K, value: DraftRow[K]) => {
    setRows(current => current.map(row => row.id === id ? { ...row, [key]: value } : row));
    setScore(null);
    setError(null);
  };

  const addRow = (arm: DraftRow['arm']) => {
    setRows(current => [...current, createRow(arm, current.length)]);
    setScore(null);
  };

  const removeRow = (id: string) => {
    setRows(current => current.filter(row => row.id !== id));
    setScore(null);
  };

  const scorePilot = async () => {
    setLoading(true);
    setError(null);
    setScore(null);

    const measurements = rows.map((row, index) => ({
      date: row.date,
      serviceId: `${row.arm}-${String(index + 1).padStart(2, '0')}`,
      arm: row.arm,
      modelForecastMeals: row.forecast === '' ? null : Number(row.forecast),
      producedPortions: Number(row.produced),
      servedPortions: Number(row.served),
      edibleSurplusKg: Number(row.surplusKg),
      wasteKg: Number(row.wasteKg),
      earlySellout: row.earlySellout,
      operatorOverride: row.operatorOverride,
      notes: row.notes,
    }));

    try {
      const response = await fetch('/api/v1/food/pilot-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ measurements }),
      });
      const payload = await response.json() as ScoreResponse;
      if (!response.ok || !payload.scorecard) {
        const detail = payload.validationErrors?.map(item => `#${item.index + 1}: ${item.message}`).join(' · ');
        setError(detail || payload.error || t('Ölçümler doğrulanamadı.', 'Measurements could not be validated.'));
      } else {
        setScore(payload.scorecard);
      }
    } catch {
      setError(t('Skorlama servisine ulaşılamadı.', 'Could not reach the scoring service.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <section className="bc-panel-dark bc-grid-bg rounded-[28px] p-6 text-white sm:p-8">
        <Link href="/food-waste" className="inline-flex items-center gap-1.5 text-[9px] font-black text-white/55 hover:text-white"><ArrowLeft size={11} /> {t('Yemek atığı çalışma alanı', 'Food-waste workspace')}</Link>
        <div className="mt-5 grid gap-7 lg:grid-cols-[1.2fr_.8fr] lg:items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.17em] text-[#b8e467]"><FlaskConical size={12} /> {t('Pilot Evidence Lab', 'Pilot Evidence Lab')}</div>
            <h1 className="mt-3 max-w-4xl text-[40px] font-black leading-[.98] tracking-[-0.06em] sm:text-[54px]">{t('Gerçek ölçümü gir. Modelin değil, pilotun hüküm vermesine izin ver.', 'Enter measured outcomes. Let the pilot, not the model, judge the intervention.')}</h1>
            <p className="mt-4 max-w-3xl text-[11px] leading-6 text-white/58">{t('Bu ekran boş başlar ve hiçbir sonuç simüle etmez. Kontrol ve müdahale servislerinin gerçek ölçümlerini girince pre-registered KPI ve guardrail’lerle skorlar.', 'This screen starts empty and simulates no outcomes. Once real control and intervention measurements are entered, it scores them using the pre-registered KPI and guardrails.')}</p>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Metric label={t('Minimum kontrol', 'Minimum control')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} />
            <Metric label={t('Minimum müdahale', 'Minimum intervention')} value={`${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} />
            <Metric label={t('Hedef azalma', 'Target reduction')} value={`≥${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} />
            <Metric label={t('Ana KPI', 'Primary KPI')} value={t('kg / 100 öğün', 'kg / 100 meals')} />
          </div>
        </div>
      </section>

      <section className="rounded-[24px] border border-slate-900/10 bg-amber-50 p-5">
        <div className="flex items-start gap-3"><ShieldCheck size={16} className="mt-0.5 shrink-0 text-amber-700" /><div><div className="text-[9px] font-black uppercase tracking-[0.12em] text-amber-800">{t('Kanıt kuralı', 'Evidence rule')}</div><p className="mt-1 text-[9px] leading-5 text-amber-900/75">{t('PROMISING sonucu bile genellenmiş iklim etkisi kanıtı değildir. Gıda güvenliği manuel olarak incelenir; servis eşleştirmesi ve ölçüm kalitesi operatör tarafından doğrulanır.', 'Even a PROMISING result is not generalized proof of climate impact. Food safety remains a manual review, and service matching plus measurement quality must be verified by the operator.')}</p></div></div>
      </section>

      <section className="space-y-3">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <div className="bc-eyebrow">{t('Ölçülen servisler', 'Measured services')}</div>
            <h2 className="mt-1 text-[25px] font-black tracking-[-0.04em] text-slate-950">{counts.control} CONTROL · {counts.intervention} INTERVENTION</h2>
          </div>
          <div className="flex gap-2">
            <button type="button" onClick={() => addRow('CONTROL')} className="inline-flex items-center gap-1.5 rounded-xl border border-slate-900/10 bg-white px-3 py-2 text-[9px] font-black text-slate-700"><Plus size={11} /> CONTROL</button>
            <button type="button" onClick={() => addRow('INTERVENTION')} className="inline-flex items-center gap-1.5 rounded-xl bg-[#173f67] px-3 py-2 text-[9px] font-black text-white"><Plus size={11} /> INTERVENTION</button>
          </div>
        </div>

        <div className="space-y-3">
          {rows.map((row, index) => (
            <article key={row.id} className="rounded-[22px] border border-slate-900/10 bg-white p-4 sm:p-5">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2"><span className={`rounded-full px-2.5 py-1 font-mono text-[8px] font-black ${row.arm === 'CONTROL' ? 'bg-slate-100 text-slate-700' : 'bg-emerald-100 text-emerald-800'}`}>{row.arm}</span><span className="font-mono text-[8px] text-slate-400">#{index + 1}</span></div>
                <button type="button" onClick={() => removeRow(row.id)} disabled={rows.length <= 2} className="rounded-lg p-2 text-slate-300 transition hover:bg-rose-50 hover:text-rose-600 disabled:cursor-not-allowed disabled:opacity-30"><Trash2 size={13} /></button>
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                <Field label={t('Tarih', 'Date')}><input type="date" value={row.date} onChange={event => updateRow(row.id, 'date', event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-900/10 px-3 py-2 text-[10px]" /></Field>
                <NumberField label={t('Model tahmini', 'Model forecast')} value={row.forecast} onChange={value => updateRow(row.id, 'forecast', value)} />
                <NumberField label={t('Üretilen porsiyon', 'Produced portions')} value={row.produced} onChange={value => updateRow(row.id, 'produced', value)} />
                <NumberField label={t('Servis edilen', 'Served portions')} value={row.served} onChange={value => updateRow(row.id, 'served', value)} />
                <NumberField label={t('Yenilebilir fazla kg', 'Edible surplus kg')} value={row.surplusKg} onChange={value => updateRow(row.id, 'surplusKg', value)} step="0.1" />
                <NumberField label={t('Atık kg', 'Waste kg')} value={row.wasteKg} onChange={value => updateRow(row.id, 'wasteKg', value)} step="0.1" />
                <ToggleField label={t('Erken tükenme', 'Early sell-out')} checked={row.earlySellout} onChange={value => updateRow(row.id, 'earlySellout', value)} />
                <ToggleField label={t('Operatör override', 'Operator override')} checked={row.operatorOverride} onChange={value => updateRow(row.id, 'operatorOverride', value)} />
              </div>
              <Field label={t('Anomali / not', 'Anomaly / note')} className="mt-3"><input value={row.notes} onChange={event => updateRow(row.id, 'notes', event.target.value)} placeholder={t('Etkinlik, menü sorunu, ölçüm notu…', 'Event, menu issue, measurement note…')} className="bc-focus-ring w-full rounded-xl border border-slate-900/10 px-3 py-2 text-[10px]" /></Field>
            </article>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-3 rounded-[22px] border border-slate-900/10 bg-[#f7f9f6] p-5 sm:flex-row sm:items-center sm:justify-between">
        <div><div className="text-[9px] font-black text-slate-800">{t('Ölçüm girişi tamam mı?', 'Measurement entry complete?')}</div><div className="mt-1 text-[8px] text-slate-400">{t('Skor motoru yalnız girdiğiniz ölçümleri değerlendirir; veri uydurmaz.', 'The score engine evaluates only measurements you enter; it does not fabricate data.')}</div></div>
        <button type="button" onClick={scorePilot} disabled={loading} className="rounded-xl bg-[#071c33] px-5 py-3 text-[9px] font-black text-white disabled:opacity-50">{loading ? t('Hesaplanıyor…', 'Scoring…') : t('Pilot skorunu hesapla', 'Score measured pilot')}</button>
      </section>

      {error ? <div className="rounded-[20px] border border-rose-200 bg-rose-50 p-5 text-[9px] leading-5 text-rose-800"><strong>VALIDATION_ERROR:</strong> {error}</div> : null}

      {score ? <ScorecardView score={score} t={t} locale={locale} /> : null}
    </div>
  );
}

function ScorecardView({ score, t, locale }: { score: PilotScorecard; t: (tr: string, en: string) => string; locale: 'tr' | 'en' }) {
  const statusClass = score.status === 'PROMISING' ? 'bg-emerald-100 text-emerald-800' : score.status === 'FAILED' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800';
  const fmt = (value: number | null, suffix = '') => value == null ? '—' : `${value.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US', { maximumFractionDigits: 2 })}${suffix}`;
  return (
    <section className="rounded-[26px] border border-slate-900/10 bg-white p-5 sm:p-7">
      <div className="flex flex-wrap items-start justify-between gap-3"><div><div className="bc-eyebrow">{t('Ölçülmüş pilot skor kartı', 'Measured pilot scorecard')}</div><h2 className="mt-2 text-[29px] font-black tracking-[-0.05em] text-slate-950">{t('Sonuç model tahmini değil, girilen ölçümlerin özeti.', 'This is a summary of entered measurements, not a model projection.')}</h2></div><span className={`rounded-full px-3 py-1.5 font-mono text-[9px] font-black ${statusClass}`}>{score.status}</span></div>
      <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <ResultMetric label={t('Normalize atık değişimi', 'Normalized waste change')} value={fmt(score.normalizedWasteReductionPct, '%')} />
        <ResultMetric label={t('Kontrol kg/100', 'Control kg/100')} value={fmt(score.control.meanWasteKgPer100Served)} />
        <ResultMetric label={t('Müdahale kg/100', 'Intervention kg/100')} value={fmt(score.intervention.meanWasteKgPer100Served)} />
        <ResultMetric label={t('Müdahale override', 'Intervention override')} value={fmt(score.intervention.operatorOverrideRatePct, '%')} />
      </div>
      <div className="mt-5 grid gap-2 sm:grid-cols-3">
        <Gate passed={score.gates.enoughEvidence} label={t('Minimum ölçüm', 'Minimum evidence')} />
        <Gate passed={score.gates.wasteReductionTargetMet} label={t('≥10% hedef', '≥10% target')} />
        <Gate passed={score.gates.earlySelloutGuardrailPassed} label={t('Erken tükenme guardrail', 'Early-sellout guardrail')} />
      </div>
      <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-[9px] leading-5 text-amber-900">{t('Gıda güvenliği manuel operasyon incelemesi gerektirir ve bu sayısal skor tarafından otomatik olarak geçilmiş sayılamaz.', 'Food-safety compliance requires manual operational review and cannot be automatically passed by this numeric scorecard.')}</div>
      <div className="mt-4 space-y-2">{score.notes.map(note => <div key={note} className="flex items-start gap-2 text-[9px] leading-4 text-slate-500"><CheckCircle2 size={11} className="mt-0.5 shrink-0 text-slate-300" />{note}</div>)}</div>
    </section>
  );
}

function Field({ label, children, className = '' }: { label: string; children: React.ReactNode; className?: string }) {
  return <label className={`block ${className}`}><div className="mb-1.5 text-[8px] font-black uppercase tracking-[0.08em] text-slate-400">{label}</div>{children}</label>;
}

function NumberField({ label, value, onChange, step = '1' }: { label: string; value: string; onChange: (value: string) => void; step?: string }) {
  return <Field label={label}><input type="number" min="0" step={step} value={value} onChange={event => onChange(event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-900/10 px-3 py-2 text-[10px]" /></Field>;
}

function ToggleField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (value: boolean) => void }) {
  return <label className="flex items-center justify-between rounded-xl border border-slate-900/10 px-3 py-2"><span className="text-[8px] font-black text-slate-500">{label}</span><input type="checkbox" checked={checked} onChange={event => onChange(event.target.checked)} className="h-4 w-4 accent-[#173f67]" /></label>;
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-white/10 bg-white/[0.06] p-3"><div className="text-[7px] font-black uppercase tracking-[0.1em] text-white/40">{label}</div><div className="mt-2 font-mono text-[18px] font-black">{value}</div></div>;
}

function ResultMetric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl bg-[#f7f9f6] p-4"><div className="text-[8px] font-black uppercase tracking-[0.08em] text-slate-400">{label}</div><div className="mt-2 font-mono text-[20px] font-black text-slate-950">{value}</div></div>;
}

function Gate({ passed, label }: { passed: boolean | null; label: string }) {
  const cls = passed === true ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : passed === false ? 'border-rose-200 bg-rose-50 text-rose-800' : 'border-amber-200 bg-amber-50 text-amber-800';
  const text = passed === true ? 'PASS' : passed === false ? 'FAIL' : 'PENDING';
  return <div className={`flex items-center justify-between rounded-xl border p-3 text-[8px] font-black ${cls}`}><span>{label}</span><span className="font-mono">{text}</span></div>;
}
