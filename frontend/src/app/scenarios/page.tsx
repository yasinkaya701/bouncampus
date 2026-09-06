'use client';

import { useState } from 'react';
import Simulator from '@/components/Scenario/Simulator';
import ComparisonView from '@/components/Scenario/ComparisonView';
import { simulateScenario } from '@/lib/api';
import { ScenarioRequest, ScenarioResult } from '@/lib/types';

export default function ScenariosPage() {
  const [result, setResult] = useState<ScenarioResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleRun = async (request: ScenarioRequest) => {
    setIsLoading(true);
    // Add small artificial delay for dramatic effect in demo
    await new Promise(r => setTimeout(r, 800));
    const res = await simulateScenario(request);
    setResult(res);
    setIsLoading(false);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Scenario Simulator</h1>
        <p className="text-gray-500 mt-2">Test &quot;what-if&quot; scenarios to see how campus dynamics and resource demands shift.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[700px]">
        <div className="lg:col-span-1 h-full">
          <Simulator onRunScenario={handleRun} isLoading={isLoading} />
        </div>
        <div className="lg:col-span-2 h-full">
          <ComparisonView result={result} />
        </div>
      </div>
    </div>
  );
}
