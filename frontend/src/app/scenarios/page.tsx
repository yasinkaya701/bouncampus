'use client';

import { useState } from 'react';
import { AlertTriangle, FlaskConical, Sparkles } from 'lucide-react';
import Simulator from '@/components/Scenario/Simulator';
import ComparisonView from '@/components/Scenario/ComparisonView';
import { simulateScenario } from '@/lib/api';
import type { ScenarioRequest, ScenarioResult } from '@/lib/types';

export default function ScenariosPage() {
  const [result, setResult] = useState<ScenarioResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async (request: ScenarioRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await simulateScenario(request);
      setResult(response);
    } catch {
      setResult(null);
      setError('Scenario service is unavailable. No cached demo result was substituted.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4 md:space-y-5">
      <section className="bc-surface-dark relative overflow-hidden rounded-[30px] px-5 py-7 text-white sm:px-7 lg:px-9 lg:py-9">
        <div className="pointer-events-none absolute -right-20 -top-28 h-72 w-72 rounded-full bg-violet-500/15 blur-3xl" />
        <div className="relative flex flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <div className="flex flex-wrap items-center gap-2"><span className="bc-chip border-violet-400/20 bg-violet-400/10 text-violet-200"><FlaskConical size={10} /> COUNTERFACTUAL LAB</span><span className="bc-chip border-white/10 bg-white/5 text-slate-300"><Sparkles size={10} /> MODEL OUTPUT</span></div>
            <h1 className="mt-6 text-[38px] font-black leading-[0.98] tracking-[-0.055em] sm:text-[48px]">What if campus<br /><span className="text-violet-300">behaved differently tomorrow?</span></h1>
            <p className="mt-4 max-w-2xl text-[12px] leading-relaxed text-slate-400">Heatwave, exam week, event or closure gibi şokları güvenli bir model alanında test et. Sonuçlar karşılaştırmalı karar desteğidir; canlı operasyon sonucu veya otomatik saha komutu değildir.</p>
          </div>
          <div className="max-w-sm rounded-[20px] border border-white/10 bg-white/5 p-4 text-[10px] leading-relaxed text-slate-400"><strong className="mb-1 block text-[9px] uppercase tracking-[0.15em] text-slate-500">Truth boundary</strong>Scenario service çalışmazsa uygulama eski demo değerine dönmez. Hata görünür kalır ve sonuç paneli boş bırakılır.</div>
        </div>
      </section>

      {error && (
        <div className="flex items-start gap-3 rounded-[18px] border border-amber-200 bg-amber-50 px-4 py-3 text-amber-900"><AlertTriangle size={15} className="mt-0.5 shrink-0" /><div><div className="text-[10px] font-black uppercase tracking-[0.12em]">Scenario unavailable</div><div className="mt-1 text-[10px] leading-relaxed text-amber-800">{error}</div></div></div>
      )}

      <section className="grid gap-4 xl:grid-cols-[minmax(330px,0.68fr)_minmax(0,1.32fr)] xl:items-stretch">
        <Simulator onRunScenario={handleRun} isLoading={isLoading} />
        <ComparisonView result={result} />
      </section>
    </div>
  );
}
