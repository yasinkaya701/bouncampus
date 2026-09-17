'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, CheckCircle2, Database, ExternalLink, Play, ShieldCheck, ThermometerSun, Zap } from 'lucide-react';
import { getMissionBrief, simulateScenario } from '@/lib/api';
import type { MissionBrief } from '@/lib/mission-types';
import type { ScenarioResult } from '@/lib/types';
import { useLocale } from '@/lib/i18n';
import { actionTitle } from '@/lib/action-copy';

export default function DemoPage() {
  const { locale, t } = useLocale();
  const [brief, setBrief] = useState<MissionBrief | null>(null);
  const [scenario, setScenario] = useState<ScenarioResult | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => { getMissionBrief().then(setBrief); }, []);

  const sourceScore = useMemo(() => {
    if (!brief?.source_health.total) return 0;
    return Math.round((brief.source_health.passing / brief.source_health.total) * 100);
  }, [brief]);

  const climateEvidence = useMemo(() => (brief?.evidence ?? []).filter(item => item.id === 'schedule' || item.id === 'weather'), [brief]);
  const energyAction = useMemo(() => brief?.dashboard.actions.find(action => action.type === 'energy'), [brief]);

  async function runHeatwave() {
    setRunning(true);
    try {
      setScenario(await simulateScenario({ scenario_type: 'heatwave', params: { temp: 38 } }));
    } finally {
      setRunning(false);
    }
  }

  if (!brief) return <div className="grid min-h-[58vh] place-items-center text-sm font-semibold text-slate-400">{t('Demo verisi hazırlanıyor…', 'Preparing demo data…')}</div>;

  return <div className="space-y-8">
    <section className="grid gap-7 border-b border-slate-900/10 pb-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-end">
      <div>
        <div className="text-[10px] font-black uppercase tracking-[0.16em] text-emerald-700">{t('KREATE jüri akışı · tek problem', 'KREATE jury flow · one problem')}</div>
        <h1 className="mt-3 max-w-4xl text-[40px] font-black leading-[1.02] tracking-[-0.055em] text-slate-950 sm:text-[52px]">{t('Düşük kullanım penceresini enerji kararına çevir.', 'Turn a low-use window into an energy decision.')}</h1>
        <p className="mt-4 max-w-2xl text-[13px] leading-6 text-slate-500">{t('Bu demo yalnızca bina enerjisi ve karbon hikâyesini anlatır: program + hava + bina bağlamı → müdahale adayı → 38°C stres testi → insan onayı → ölçümlü pilot.', 'This demo tells one building-energy and carbon story: schedule + weather + building context → intervention candidate → 38°C stress test → human approval → measured pilot.')}</p>
      </div>
      <div className="grid grid-cols-3 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4"><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Kaynak', 'Sources')}</div><div className="mt-1 font-mono text-xl font-black">{brief.source_health.passing}/{brief.source_health.total}</div></div><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Hazırlık', 'Readiness')}</div><div className="mt-1 font-mono text-xl font-black text-emerald-700">{sourceScore}%</div></div><div className="px-3"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Enerji adayı', 'Energy candidates')}</div><div className="mt-1 font-mono text-xl font-black text-[#173f67]">{brief.dashboard.actions.filter(action => action.type === 'energy').length}</div></div></div>
    </section>

    <section className="grid gap-7 lg:grid-cols-[0.8fr_1.2fr]">
      <div className="border-t border-slate-900/10 pt-5"><div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><Database size={12} /> {t('1 · İki kanıtı oku', '1 · Read two evidence signals')}</div><h2 className="mt-2 text-xl font-black tracking-[-0.035em]">{t('Talep nerede düşüyor, dış koşul ne söylüyor?', 'Where is demand dropping, and what do outdoor conditions say?')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Ders programı doluluk için model girdisidir; hava verisi HVAC bağlamıdır. Hiçbiri bağlı BMS veya canlı doluluk sensörü olarak sunulmaz.', 'The course schedule is a model input for occupancy; weather provides HVAC context. Neither is presented as a connected BMS or live occupancy sensor.')}</p></div>
      <div className="divide-y divide-slate-900/10 border-y border-slate-900/10 bg-white">{climateEvidence.map(item => <article key={item.id} className="grid gap-2 px-4 py-4 sm:grid-cols-[170px_minmax(0,1fr)_130px] sm:items-center"><div><div className="text-[10px] font-black text-slate-900">{item.label}</div><div className={`mt-1 text-[8px] font-bold ${item.source?.ok ? 'text-emerald-700' : 'text-amber-700'}`}>{item.source?.ok ? item.source.provenance : t('KULLANILAMIYOR', 'UNAVAILABLE')}</div></div><div className="text-[10px] leading-5 text-slate-500">{item.interpretation}</div><div className="text-right"><div className="text-[11px] font-black text-slate-800">{item.value}</div>{item.source?.url && item.source.url !== '/' ? <a href={item.source.url} target="_blank" rel="noreferrer" className="mt-1 inline-flex items-center gap-1 text-[8px] font-bold text-[#173f67]">{t('Kaynağı aç', 'Open source')} <ExternalLink size={8} /></a> : null}</div></article>)}</div>
    </section>

    <section className="grid gap-7 lg:grid-cols-2">
      <div className="border-t border-slate-900/10 pt-5">
        <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><Zap size={12} /> {t('2 · Enerji kararını incele', '2 · Review the energy decision')}</div>
        <h2 className="mt-2 text-2xl font-black tracking-[-0.04em]">{energyAction ? actionTitle(energyAction, locale) : t('Bugün müdahale eşiğinin üzerinde enerji adayı yok.', 'No energy candidate is above the intervention threshold today.')}</h2>
        <p className="mt-3 text-[11px] leading-5 text-slate-500">{energyAction?.description ?? t('BOUNCAMPUS karar üretmek için sayı uydurmaz; eşik aşılmadığında izlemeye devam eder.', 'BOUNCAMPUS does not invent numbers to force a decision; it keeps monitoring when the threshold is not met.')}</p>
        <div className="mt-5 grid grid-cols-2 gap-3"><div className="border-t border-slate-900/10 pt-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Güven', 'Confidence')}</div><div className="mt-1 font-mono text-2xl font-black">{brief.confidence}%</div></div><div className="border-t border-slate-900/10 pt-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Pencere', 'Window')}</div><div className="mt-1 text-[11px] font-black">{energyAction?.time ?? brief.operating_window}</div></div></div>
        <div className="mt-5 flex items-start gap-2 border border-amber-200 bg-amber-50 p-3 text-[9px] leading-4 text-amber-900"><CheckCircle2 size={12} className="mt-0.5 shrink-0" /> {t('Bu değer model potansiyelidir. Operatör sahayı doğrulamadan ve pilotu onaylamadan gerçek sistemde hiçbir komut çalıştırılmaz.', 'This is modeled potential. No real-world command is executed until an operator validates field conditions and approves a pilot.')}</div>
        <Link href="/decisions" className="mt-4 inline-flex items-center gap-1 text-[10px] font-bold text-[#173f67]">{t('Karar kayıtlarını aç', 'Open decision records')} <ArrowRight size={10} /></Link>
      </div>

      <div className="border-t border-slate-900/10 pt-5">
        <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><ShieldCheck size={12} /> {t('3 · 38°C ile stres testi', '3 · Stress-test at 38°C')}</div>
        <h2 className="mt-2 text-xl font-black tracking-[-0.035em]">{t('Aynı müdahale sıcak hava dalgasında hâlâ mantıklı mı?', 'Does the same intervention still make sense during a heatwave?')}</h2>
        <button type="button" disabled={running} onClick={runHeatwave} className="mt-4 inline-flex items-center gap-1.5 rounded-lg border border-slate-900/10 bg-white px-3 py-2 text-[10px] font-bold disabled:opacity-50"><ThermometerSun size={12} /> {running ? t('Hesaplanıyor…', 'Running…') : t('38°C sıcak hava senaryosunu çalıştır', 'Run 38°C heatwave scenario')}</button>
        {scenario ? <div className="mt-5"><div className="flex items-center gap-2 text-[10px] font-black text-slate-900"><Play size={10} fill="currentColor" /> {t('Karşı-olgusal sonuç', 'Counterfactual result')}</div><div className="mt-3 grid grid-cols-3 gap-3"><Metric label={t('Enerji değişimi', 'Energy change')} value={`${scenario.changes.energy_change_percent > 0 ? '+' : ''}${scenario.changes.energy_change_percent.toFixed(1)}%`} /><Metric label={t('CO₂ değişimi', 'CO₂ change')} value={`${scenario.changes.co2_change_percent > 0 ? '+' : ''}${scenario.changes.co2_change_percent.toFixed(1)}%`} /><Metric label={t('Maliyet farkı', 'Cost delta')} value={`${scenario.changes.cost_change_tl.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')} TL`} /></div><p className="mt-3 text-[9px] leading-4 text-slate-400">{t('Bu çıktı gerçek saha ölçümü değil; operatörün öneriyi uygulamadan önce sorgulaması için model karşılaştırmasıdır.', 'This is not a field measurement; it is a model comparison used to challenge the recommendation before action.')}</p></div> : <div className="mt-5 grid min-h-[170px] place-items-center border border-dashed border-slate-300 bg-white p-5 text-center text-[10px] leading-5 text-slate-400">{t('Jüride tek buton: 38°C stres testini çalıştır ve kararın nasıl değiştiğini göster.', 'One jury button: run the 38°C stress test and show how the decision changes.')}</div>}
      </div>
    </section>

    <section className="border-t border-slate-900/10 pt-6"><div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('4 · Pilot ve öğrenme', '4 · Pilot and learn')}</div><div className="mt-2 grid gap-4 lg:grid-cols-[1fr_1fr]"><div><h2 className="text-xl font-black tracking-[-0.035em]">{t('Bugün mimariyi kanıtlıyoruz; etkiyi pilotta ölçeceğiz.', 'Today we prove the decision workflow; the pilot proves impact.')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Pilot girdileri: bina/floor smart-meter toplamları ve anonim toplu doluluk. Çıktı: beklenen kWh ile ölçülen kWh farkı, model hatası ve bir sonraki karar için kalibrasyon.', 'Pilot inputs: building/floor smart-meter totals and anonymous aggregate occupancy. Output: expected versus measured kWh, model error and calibration for the next decision.')}</p></div><div className="grid grid-cols-3 gap-2 text-center"><Step value="SENSE" /><Step value="DECIDE" /><Step value="STRESS-TEST" /><Step value="APPROVE" /><Step value="PILOT" /><Step value="LEARN" /></div></div></section>
  </div>;
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="border-t border-slate-900/10 py-3"><div className="text-[8px] font-black uppercase tracking-[0.12em] text-slate-400">{label}</div><div className="mt-1 font-mono text-lg font-black text-slate-900">{value}</div></div>;
}

function Step({ value }: { value: string }) {
  return <div className="rounded-lg border border-slate-900/10 bg-white px-2 py-3 text-[9px] font-black tracking-[0.08em] text-slate-600">{value}</div>;
}
