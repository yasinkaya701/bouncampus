import { ActionItem } from '@/lib/types';
import { Zap, Utensils, Building2 } from 'lucide-react';

export default function ActionCards({ actions }: { actions: ActionItem[] }) {
  const getIcon = (type: string) => {
    switch (type) {
      case 'energy': return <Zap size={18} />;
      case 'food': return <Utensils size={18} />;
      case 'space': return <Building2 size={18} />;
      default: return <Zap size={18} />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH': return 'bg-danger text-white';
      case 'MEDIUM': return 'bg-warning text-white';
      case 'LOW': return 'bg-primary-light text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="grid gap-4">
      {actions.map(action => (
        <div key={action.id} className="bg-white border border-gray-100 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-start space-x-4">
            <div className={`p-2 rounded-full ${getPriorityColor(action.priority)} mt-1 sm:mt-0`}>
              {getIcon(action.type)}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h4 className="font-bold text-gray-800">{action.title}</h4>
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${action.priority === 'HIGH' ? 'bg-red-100 text-red-700' : action.priority === 'MEDIUM' ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'}`}>
                  {action.priority}
                </span>
              </div>
              <p className="text-sm text-gray-500 mt-1">{action.description}</p>
              <div className="flex text-xs text-gray-400 mt-2 space-x-3">
                <span className="flex items-center">🕒 {action.time}</span>
                <span className="flex items-center">📍 {action.location}</span>
              </div>
            </div>
          </div>
          <div className="mt-4 sm:mt-0 bg-gray-50 px-4 py-2 rounded-lg text-center min-w-[100px]">
            <div className="text-xs text-gray-500 mb-1">Impact</div>
            <div className="font-bold text-gray-800">{action.impact_value} <span className="text-sm font-normal text-gray-500">{action.impact_unit}</span></div>
          </div>
        </div>
      ))}
    </div>
  );
}
