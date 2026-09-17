'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, CheckCircle2, CloudRain, Database, ExternalLink, Play, ShieldCheck, ThermometerSun } from 'lucide-react';
import { getMissionBrief, simulateScenario } from '@/lib/api';
import type { MissionBrief } from '@/lib/mission-types';
import type { ScenarioResult } from '@/lib/types';
import { useLocale } from '@/lib/i18n';

export default function DemoPage() {
  const { locale, t } = useLocale();
  const [brief, setBrief] = useState<MissionBrief | null>(null);
  const [scenario, setScenario] = useState<ScenarioResult | null>(null);
  const [scenarioName, setScenarioName] = useState('');
  const [running, setRunning] = useState(false);

  useEffect(() => { getMissionBrief().then(setBrief); }, []);

  const sourceScore = useMemo(() => {
    if (!brief?.source_health.total) return 0;
    return Math.round((brief.source_health.passing / brief.source_health.total) * 100);
  }, [brief]);

  async function runScenario(type: 'rain' | 'heatwave') {
    setRunning(true);
    setScenarioName(type === 'rain' ? t('Yoğun yağış', 'Heavy rain') : t('38°C sıcak hava', '38°C heatwave'));
    try {
      setScenario(await simulateScenario({ scenario_type: type, params: type === 'heatwave' ? { temp: 38 } : {} }));
    } finally {
      setRunning(false);
    }
  }

  if (!brief) return <div className="grid min-h-[58vh] place-items-center text-sm font-semibold text-slate-400">{t('Demo verisi hazırlanıyor…', 'Preparing demo data…')}</div>;

  return <div className="space-y-8">
    <section className="grid gap-7 border-b border-slate-900/10 pb-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-end">
      <div><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">{t('90 saniyelik ürün akışı', '90-second product flow')}</div><h1 className="mt-3 max-w-4xl text-[40px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950 sm:text-[52px]">{t('Sinyalden karara, kaynağı saklamadan.', 'From signal to decision, without hiding the source.')}</h1><p className="mt-4 max-w-2xl text-[13px] leading-6 text-slate-500">{t('Bu demo kamuya açık kampüs verisini, program tabanlı modeli ve insan onayını tek akışta gösterir. Bağlı olmayan sensör veya otomasyon sistemi varmış gibi davranmaz.', 'This demo connects public campus data, schedule-derived models and human review in one flow. It does not pretend that unconnected sensors or automation systems exist.')}</p></div>
      <div className="grid grid-cols-3 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4"><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Kaynak', 'Sources')}</div><div className="mt-1 font-mono text-xl font-black">{brief.source_health.passing}/{brief.source_health.total}</div></div><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Hazırlık', 'Readiness')}</div><div className="mt-1 font-mono text-xl font-black text-emerald-700">{sourceScore}%</div></div><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Aday', 'Candidates')}</div><div className="mt-1 font-mono text-xl font-black text-[#173f67]">{brief.dashboard.actions.length}</div></div></div>
    </section>

    <section className="grid gap-7 lg:grid-cols-[0.8fr_1.2fr]">
      <div className="border-t border-slate-900/10 pt-5"><div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><Database size={12} /> {t('1 · Kaynakları oku', '1 · Read the sources')}</div><h2 className="mt-2 text-xl font-black tracking-[-0.035em]">{t('Her sinyal kendi statüsüyle görünür', 'Every signal keeps its own status')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Canlı, snapshot ve model verisi tek etikete sıkıştırılmaz.', 'Live feeds, snapshots and model outputs are not collapsed into one label.')}</p></div>
      <div className="divide-y divide-slate-900/10 border-y border-slate-900/10 bg-white">{brief.evidence.map(item => <article key={item.id} className="grid gap-2 px-4 py-4 sm:grid-cols-[170px_minmax(0,1fr)_130px] sm:items-center"><div><div className="text-[10px] font-black text-slate-900">{item.label}</div><div className={`mt-1 text-[8px] font-bold ${item.source?.ok ? 'text-emerald-700' : 'text-amber-700'}`}>{item.source?.ok ? item.source.provenance : t('KULLANILAMIYOR', 'UNAVAILABLE')}</div></div><div className="text-[10px] leading-5 text-slate-500">{item.interpretation}</div><div className="text-right"><div className="text-[11px] font-black text-slate-800">{item.value}</div>{item.source?.url && item.source.url !== '/' ? <a href={item.source.url} target="_blank" rel="noreferrer" className="mt-1 inline-flex items-center gap-1 text-[8px] font-bold text-[#173f67]">{t('Kaynağı aç', 'Open source')} <ExternalLink size={8} /></a> : null}</div></article>)}</div>
    </section>

    <section className="grid gap-7 lg:grid-cols-2"><div className="border-t border-slate-900/10 pt-5"><div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><ShieldCheck size={12} /> {t('2 · Kararı incele', '2 · Review the decision')}</div><h2 className="mt-2 text-2xl font-black tracking-[-0.04em]">{brief.title}</h2><p className="mt-3 text-[11px] leading-5 text-slate-500">{brief.one_liner}</p><div className="mt-5 grid grid-cols-2 gap-3"><div className="border-t border-slate-900/10 pt-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Güven', 'Confidence')}</div><div className="mt-1 font-mono text-2xl font-black">{brief.confidence}%</div></div><div className="border-t border-slate-900/10 pt-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Pencere', 'Window')}</div><div className="mt-1 text-[11px] font-black">{brief.operating_window}</div></div></div><div className="mt-5 flex items-start gap-2 border border-amber-200 bg-amber-50 p-3 text-[9px] leading-4 text-amber-900"><CheckCircle2 size={12} className="mt-0.5 shrink-0" /> {brief.guardrail}</div><Link href="/decisions" className="mt-4 inline-flex items-center gap-1 text-[10px] font-bold text-[#173f67]">{t('Karar kayıtlarını aç', 'Open decision records')} <ArrowRight size={10} /></Link></div>

      <div className="border-t border-slate-900/10 pt-5"><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('3 · Stres testi', '3 · Stress test')}</div><h2 className="mt-2 text-xl font-black tracking-[-0.035em]">{t('Karar koşullar değişince ne oluyor?', 'What happens when conditions change?')}</h2><div className="mt-4 flex gap-2"><button type="button" disabled={running} onClick={() => runScenario('rain')} className="inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-3 py-2 text-[10px] font-bold disabled:opacity-50"><CloudRain size={12} /> {t('Yoğun yağış', 'Heavy rain')}</button><button type="button" disabled={running} onClick={() => runScenario('heatwave')} className="inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-3 py-2 text-[10px] font-bold disabled:opacity-50"><ThermometerSun size={12} /> {t('38°C sıcak hava', '38°C heatwave')}</button></div>{scenario ? <div className="mt-5"><div className="flex items-center gap-2 text-[10px] font-black text-slate-900"><Play size={10} fill="currentColor" /> {scenarioName}</div><div className="mt-3 grid grid-cols-2 gap-3"><Metric label={t('Enerji', 'Energy')} value={`${scenario.changes.energy_change_percent > 0 ? '+' : ''}${scenario.changes.energy_change_percent.toFixed(1)}%`} /><Metric label={t('Yemek talebi', 'Food demand')} value={`${scenario.changes.food_change_percent > 0 ? '+' : ''}${scenario.changes.food_change_percent.toFixed(1)}%`} /><Metric label={t('CO₂', 'CO₂')} value={`${scenario.changes.co2_change_percent > 0 ? '+' : ''}${scenario.changes.co2_change_percent.toFixed(1)}%`} /><Metric label={t('Maliyet', 'Cost')} value={`${scenario.changes.cost_change_tl.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} TL`} /></div><p className="mt-3 text-[9px] leading-4 text-slate-400">{t('Senaryo çıktısı model sonucudur; gerçek saha ölçümü değildir.', 'Scenario output is a model result, not a field measurement.')}</p></div> : <div className="mt-5 grid min-h-[180px] place-items-center border border-dashed border-slate-300 bg-white p-5 text-center text-[10px] leading-5 text-slate-400">{running ? t('Senaryo hesaplanıyor…', 'Running scenario…') : t('Bir stres testi seç.', 'Choose a stress test.')}</div>}</div></section>
  </div>;
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="border-t border-slate-900/10 py-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{label}</div><div className="mt-1 font-mono text-lg font-black text-slate-900">{value}</div></div>;
}
