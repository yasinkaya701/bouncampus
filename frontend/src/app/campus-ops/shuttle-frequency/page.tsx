import Link from 'next/link';
import { ArrowLeft, BusFront } from 'lucide-react';
import ShuttleFrequencyPlanner from '@/components/CampusOps/ShuttleFrequencyPlanner';

export default function ShuttleFrequencyPage() {
  return (
    <div className="space-y-5 sm:space-y-6">
      <section className="overflow-hidden rounded-[30px] border border-white/10 bg-[#07131f] p-6 text-white shadow-[0_28px_80px_rgba(7,19,31,.16)] sm:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#b8e467]"><BusFront size={12} /> CS1 · SHUTTLE FREQUENCY</div>
            <h1 className="mt-4 max-w-4xl text-[40px] font-black leading-[0.95] tracking-[-0.06em] sm:text-[56px]">Schedule-aware shuttle frequency planning</h1>
            <p className="mt-4 max-w-3xl text-[11px] leading-6 text-white/55">Course start/end waves become advisory headway bands. External weather and operator-supplied event/queue context can increase service pressure, while missing route coverage fails closed.</p>
          </div>
          <Link href="/campus-ops" className="bc-focus-ring inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.06] px-4 py-2.5 text-[10px] font-black text-white/75 hover:bg-white/[0.1]"><ArrowLeft size={12} /> Campus Ops</Link>
        </div>
      </section>
      <ShuttleFrequencyPlanner />
    </div>
  );
}
