import { DashboardData } from '@/lib/types';
import { Users, Zap, Utensils, TrendingDown } from 'lucide-react';

export default function KPICards({ data }: { data: DashboardData }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-500 font-medium text-sm">Campus Occupancy</h3>
          <div className="p-2 bg-blue-50 rounded-lg text-blue-500">
            <Users size={20} />
          </div>
        </div>
        <div className="flex items-end space-x-2">
          <span className="text-3xl font-bold text-gray-800">{data.campus_occupancy}%</span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-500 font-medium text-sm">Predicted Energy</h3>
          <div className="p-2 bg-amber-50 rounded-lg text-accent">
            <Zap size={20} />
          </div>
        </div>
        <div className="flex items-end space-x-2">
          <span className="text-3xl font-bold text-gray-800">{data.predicted_energy_mwh} <span className="text-lg text-gray-500">MWh</span></span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-500 font-medium text-sm">Food Demand</h3>
          <div className="p-2 bg-orange-50 rounded-lg text-warning">
            <Utensils size={20} />
          </div>
        </div>
        <div className="flex items-end space-x-2">
          <span className="text-3xl font-bold text-gray-800">{data.food_demand_meals} <span className="text-lg text-gray-500">meals</span></span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-primary-light flex flex-col justify-between relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-primary-light opacity-10 rounded-bl-full pointer-events-none"></div>
        <div className="flex items-center justify-between mb-4 relative z-10">
          <h3 className="text-primary-medium font-medium text-sm">Potential Saving</h3>
          <div className="p-2 bg-green-50 rounded-lg text-primary">
            <TrendingDown size={20} />
          </div>
        </div>
        <div className="flex flex-col relative z-10">
          <span className="text-3xl font-bold text-primary">₺{data.potential_saving_tl.toLocaleString()}</span>
          <span className="text-xs text-primary-light mt-1 flex items-center"><TrendingDown size={12} className="mr-1"/> {data.co2_avoided_kg} kg CO₂ avoided</span>
        </div>
      </div>
    </div>
  );
}
