import { ScenarioResult } from '@/lib/types';
import { ArrowRight, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

export default function ComparisonView({ result }: { result: ScenarioResult | null }) {
  if (!result) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400 bg-gray-50 rounded-xl border border-dashed border-gray-300">
        <p>Run a scenario to see the results</p>
      </div>
    );
  }

  const c = result.changes;

  const MetricRow = ({ label, original, modified, change, unit, higherIsWorse = true }: any) => {
    const isIncrease = change > 0;
    const isBad = (isIncrease && higherIsWorse) || (!isIncrease && !higherIsWorse);
    const color = isBad ? 'text-danger' : 'text-primary';
    const Icon = isIncrease ? ArrowUpRight : ArrowDownRight;

    return (
      <div className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
        <span className="text-sm font-medium text-gray-600 w-1/4">{label}</span>
        <div className="w-1/4 text-right font-medium text-gray-400 line-through text-sm">{original} {unit}</div>
        <div className="w-1/12 flex justify-center text-gray-300"><ArrowRight size={16} /></div>
        <div className="w-1/4 text-right font-bold text-gray-800">{modified} {unit}</div>
        <div className={`w-1/6 text-right font-bold flex justify-end items-center ${color}`}>
          {Math.abs(change)}% <Icon size={16} className="ml-1" />
        </div>
      </div>
    );
  };

  const chartData = [
    { name: 'Energy (MWh)', Original: result.original.predicted_energy_mwh, Modified: result.modified.predicted_energy_mwh },
    { name: 'Food (Meals/1000)', Original: result.original.food_demand_meals / 1000, Modified: result.modified.food_demand_meals / 1000 },
    { name: 'CO2 (kg/10)', Original: result.original.co2_avoided_kg / 10, Modified: result.modified.co2_avoided_kg / 10 },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden h-full flex flex-col animate-in slide-in-from-right-4 duration-500">
      <div className="bg-primary text-white p-4">
        <h3 className="font-bold text-lg">Impact Analysis</h3>
      </div>
      
      <div className="p-6 flex-grow">
        <div className="mb-8">
          <MetricRow 
            label="Energy Demand" 
            original={result.original.predicted_energy_mwh} 
            modified={result.modified.predicted_energy_mwh} 
            change={c.energy_change_percent} 
            unit="MWh" 
          />
          <MetricRow 
            label="Food Demand" 
            original={result.original.food_demand_meals} 
            modified={result.modified.food_demand_meals} 
            change={c.food_change_percent} 
            unit="meals" 
          />
          <MetricRow 
            label="CO₂ Output" 
            original={result.original.co2_avoided_kg} 
            modified={result.modified.co2_avoided_kg} 
            change={c.co2_change_percent} 
            unit="kg" 
          />
        </div>

        <div className="h-64 mt-4">
          <h4 className="text-sm font-bold text-gray-700 mb-4 text-center">Visual Comparison</h4>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="Original" fill="#9ca3af" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Modified" fill="#059669" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
