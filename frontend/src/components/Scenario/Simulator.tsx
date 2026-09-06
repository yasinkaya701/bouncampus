'use client';

import { useState } from 'react';
import { ScenarioRequest } from '@/lib/types';
import { Thermometer, BookOpen, Calendar, CloudRain, ShieldAlert, Sun } from 'lucide-react';

interface SimulatorProps {
  onRunScenario: (request: ScenarioRequest) => void;
  isLoading: boolean;
}

export default function Simulator({ onRunScenario, isLoading }: SimulatorProps) {
  const [activeScenario, setActiveScenario] = useState<ScenarioRequest['scenario_type']>('heatwave');
  const [temp, setTemp] = useState(35);
  const [eventSize, setEventSize] = useState(500);

  const scenarios: { id: ScenarioRequest['scenario_type'], title: string, icon: any }[] = [
    { id: 'heatwave', title: 'Heatwave', icon: Thermometer },
    { id: 'exam_week', title: 'Exam Week', icon: BookOpen },
    { id: 'event', title: 'Campus Event', icon: Calendar },
    { id: 'rain', title: 'Rain / Storm', icon: CloudRain },
    { id: 'building_closure', title: 'Closure', icon: ShieldAlert },
    { id: 'summer_school', title: 'Summer Sch.', icon: Sun },
  ];

  const handleRun = () => {
    onRunScenario({
      scenario_type: activeScenario,
      params: { temp, eventSize }
    });
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden h-full flex flex-col">
      <div className="bg-gray-50 border-b border-gray-200 p-4">
        <h3 className="font-bold text-gray-800">Select Scenario</h3>
      </div>
      
      <div className="p-4 flex-grow flex flex-col">
        <div className="grid grid-cols-2 gap-3 mb-6">
          {scenarios.map(s => {
            const Icon = s.icon;
            const isActive = activeScenario === s.id;
            return (
              <button
                key={s.id}
                onClick={() => setActiveScenario(s.id)}
                className={`p-3 rounded-lg border text-left flex items-center space-x-3 transition ${isActive ? 'bg-primary-light border-primary-light text-white' : 'border-gray-200 hover:border-primary-light hover:bg-green-50 text-gray-700'}`}
              >
                <Icon size={18} className={isActive ? 'text-white' : 'text-gray-500'} />
                <span className="font-medium text-sm">{s.title}</span>
              </button>
            );
          })}
        </div>

        <div className="bg-gray-50 rounded-lg p-4 mb-6 flex-grow">
          <h4 className="font-medium text-sm mb-4 text-gray-700">Parameters</h4>
          
          {activeScenario === 'heatwave' && (
            <div>
              <label className="block text-xs text-gray-500 mb-2">Temperature: {temp}°C</label>
              <input 
                type="range" 
                min="20" max="45" 
                value={temp} 
                onChange={(e) => setTemp(Number(e.target.value))}
                className="w-full accent-primary"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>20°C</span><span>45°C</span>
              </div>
            </div>
          )}

          {activeScenario === 'event' && (
            <div>
              <label className="block text-xs text-gray-500 mb-2">Additional Visitors</label>
              <select 
                value={eventSize} 
                onChange={(e) => setEventSize(Number(e.target.value))}
                className="w-full p-2 border border-gray-200 rounded-md text-sm"
              >
                <option value={500}>+500 people</option>
                <option value={1000}>+1000 people</option>
                <option value={2000}>+2000 people</option>
              </select>
            </div>
          )}

          {(activeScenario === 'exam_week' || activeScenario === 'rain' || activeScenario === 'summer_school' || activeScenario === 'building_closure') && (
            <div className="text-sm text-gray-500 italic flex items-center justify-center h-20">
              Standard parameters applied automatically.
            </div>
          )}
        </div>

        <button
          onClick={handleRun}
          disabled={isLoading}
          className="w-full bg-primary hover:bg-primary-medium text-white font-bold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          {isLoading ? 'Running Simulation...' : 'Run Scenario'}
        </button>
      </div>
    </div>
  );
}
