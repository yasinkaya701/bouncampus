import { ActionItem } from '@/lib/types';
import { Zap, Utensils, Building2 } from 'lucide-react';

export default function Timeline({ actions }: { actions: ActionItem[] }) {
  const sortedActions = [...actions].sort((a, b) => a.time.localeCompare(b.time));

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative w-full overflow-x-auto">
      <div className="min-w-[600px] py-4 relative">
        {/* Timeline line */}
        <div className="absolute top-1/2 left-0 right-0 h-1 bg-gray-200 -translate-y-1/2 z-0 rounded-full"></div>
        
        {/* Hours markings */}
        <div className="flex justify-between absolute top-0 left-0 right-0 px-2">
          {['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'].map(hour => (
            <div key={hour} className="flex flex-col items-center">
              <span className="text-xs text-gray-400 font-medium">{hour}</span>
              <div className="w-px h-2 bg-gray-300 mt-1"></div>
            </div>
          ))}
        </div>

        {/* Action items */}
        <div className="relative h-24 mt-8">
          {sortedActions.map((action, i) => {
            // Rough calculation of horizontal position based on time string 'HH:MM'
            const [hours, minutes] = action.time.split(':').map(Number);
            const totalMinutesFrom8 = (hours - 8) * 60 + minutes;
            const totalMinutesInTimeline = (20 - 8) * 60; // 08:00 to 20:00
            const percentage = Math.max(5, Math.min(95, (totalMinutesFrom8 / totalMinutesInTimeline) * 100));
            
            const isTop = i % 2 === 0;

            const getColor = (p: string) => {
              if (p === 'HIGH') return 'bg-danger text-white border-danger';
              if (p === 'MEDIUM') return 'bg-warning text-white border-warning';
              return 'bg-primary-light text-white border-primary-light';
            };

            const getIcon = (type: string) => {
              switch (type) {
                case 'energy': return <Zap size={14} />;
                case 'food': return <Utensils size={14} />;
                case 'space': return <Building2 size={14} />;
                default: return <Zap size={14} />;
              }
            };

            return (
              <div 
                key={action.id} 
                className={`absolute flex flex-col items-center ${isTop ? 'bottom-1/2 mb-2' : 'top-1/2 mt-2'}`}
                style={{ left: `${percentage}%`, transform: 'translateX(-50%)' }}
              >
                {isTop && (
                  <div className="bg-white p-2 rounded shadow-md border text-xs w-32 text-center mb-1 z-10 hover:scale-105 transition">
                    <div className="font-bold truncate">{action.title}</div>
                    <div className="text-gray-500">{action.time}</div>
                  </div>
                )}
                
                <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 z-20 ${getColor(action.priority)}`} title={action.title}>
                  {getIcon(action.type)}
                </div>

                {!isTop && (
                  <div className="bg-white p-2 rounded shadow-md border text-xs w-32 text-center mt-1 z-10 hover:scale-105 transition">
                    <div className="font-bold truncate">{action.title}</div>
                    <div className="text-gray-500">{action.time}</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
