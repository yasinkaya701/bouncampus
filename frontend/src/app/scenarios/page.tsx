'use client';

import { useState } from 'react';
import { AlertTriangle, Play } from 'lucide-react';
import { simulateScenario } from '@/lib/api';
import type { ScenarioRequest, ScenarioResult } from '@/lib/types';
import { useLocale } from '@/lib/i18n';

const SCENARIOS: Array<{ type: ScenarioRequest['scenario_type']; tr: string; en: string; trn: string; enn: string }> = [
  { type: 'heatwave', tr: 'Sıcak hava dalgası', en: 'Heatwave', trn: 'Soğutma yükü ve kullanım davranışı şoku', enn: 'Cooling-load and usage shock' },
  { type: 'exam_week', tr: 'Sınav haftası', en: 'Exam week', trn: 'Daha uzun bina ve çalışma alanı kullanımı', enn: 'Longer building and study-space use' },
  { type: 'event', tr: 'Büyük etkinlik', en: 'Large event', trn: 'Yerel talep ve yaya akışı artışı', enn: 'Local demand and footfall increase' },
  { type: 'rain', tr: 'Yağış', en: 'Rain', trn: 'İç mekân talebi ve ulaşım etkisi', enn: 'Indoor-demand and mobility effect' },
  { type: 'building_closure', tr: 'Bina kapanışı', en: 'Building closure', trn: 'Talebin diğer alanlara kayması', enn: 'Demand displaced to other spaces' },
  { type: 'summer_school', tr: 'Yaz okulu', en: 'Summer school', trn: 'Düşük yoğunluklu dönem senaryosu', enn: 'Lower-density term scenario' },
];

export default function ScenariosPage() {
  const { locale, t } = useLocale();
  const [selected, setSelected] = useState<ScenarioRequest['scenario_type']>('heatwave');
  const [result, setResult] = useState<ScenarioResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    setLoading(true); setError(null);
    try { setResult(await simulateScenario({ scenario_type: selected, params: {} })); }
    catch { setResult(null); setError(t('Senaryo servisine ulaşılamadı; demo sonucu uydurulmadı.', 'Scenario service is unavailable; no demo result was substituted.')); }
    finally { setLoading(false); }
  }

  return (
    <div className="space-y-7">
      <section className="border-b border-slate-900/10 pb-7"><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('Karşı-olgusal model', 'Counterfactual model')}</div><h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Senaryolar', 'Scenarios')}</h1><p className="mt-3 max-w-2xl text-[12px] leading-6 text-slate-500">{t('Kampüs davranışını değiştirmeden önce “ne olurdu?” sorusunu model alanında test et. Sonuçlar operasyon gerçeği değil karar desteğidir.', 'Test “what if?” questions in a model space before changing campus operations. Results are decision support, not observed operational truth.')}</p></section>

      {error && <div className="flex items-start gap-2 border border-amber-200 bg-amber-50 p-3 text-[10px] text-amber-900"><AlertTriangle size={14} /> {error}</div>}

      <section className="grid gap-6 lg:grid-cols-[380px_minmax(0,1fr)]">
        <div><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Senaryo seç', 'Choose scenario')}</div><div className="mt-3 divide-y divide-slate-900/8 border-y border-slate-900/10 bg-white">{SCENARIOS.map(item => <button key={item.type} type="button" onClick={() => setSelected(item.type)} className={`block w-full px-4 py-3 text-left ${selected === item.type ? 'bg-slate-50' : ''}`}><div className="flex items-center justify-between gap-3"><span className="text-[12px] font-black text-slate-900">{locale === 'tr' ? item.tr : item.en}</span>{selected === item.type && <span className="h-2 w-2 rounded-full bg-[#173f67]" />}</div><div className="mt-1 text-[9px] text-slate-500">{locale === 'tr' ? item.trn : item.enn}</div></button>)}</div><button type="button" disabled={loading} onClick={run} className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#102a43] px-4 py-3 text-[11px] font-black text-white disabled:opacity-50"><Play size={12} fill="currentColor" /> {loading ? t('Hesaplanıyor…', 'Running…') : t('Senaryoyu çalıştır', 'Run scenario')}</button></div>

        <div className="border-t border-slate-900/10 pt-4 lg:border-l lg:border-t-0 lg:pl-6"><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Karşılaştırma', 'Comparison')}</div>{result ? <div className="mt-4 grid gap-3 sm:grid-cols-2"><Metric label={t('Enerji değişimi', 'Energy change')} value={`${result.changes.energy_change_percent > 0 ? '+' : ''}${result.changes.energy_change_percent.toFixed(1)}%`} /><Metric label={t('Yemek talebi', 'Food demand')} value={`${result.changes.food_change_percent > 0 ? '+' : ''}${result.changes.food_change_percent.toFixed(1)}%`} /><Metric label={t('CO₂ değişimi', 'CO₂ change')} value={`${result.changes.co2_change_percent > 0 ? '+' : ''}${result.changes.co2_change_percent.toFixed(1)}%`} /><Metric label={t('Maliyet farkı', 'Cost delta')} value={`${result.changes.cost_change_tl.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} TL`} /></div> : <div className="mt-4 grid min-h-[260px] place-items-center border border-dashed border-slate-300 bg-white p-6 text-center text-[11px] leading-5 text-slate-400">{t('Bir senaryo seçip çalıştırdığında değişimler burada görünür.', 'Run a scenario to see the modeled deltas here.')}</div>}<p className="mt-4 text-[9px] leading-4 text-slate-400">{t('Bu değerler model çıktısıdır; gerçek sayaç, POS veya sensör ölçümü değildir.', 'These values are model outputs, not meter, POS or sensor measurements.')}</p></div>
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="border-t border-slate-900/10 py-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{label}</div><div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em] text-slate-900">{value}</div></div>;
}
