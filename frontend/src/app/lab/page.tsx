import Link from 'next/link';
import { ArrowUpRight, FlaskConical, Waves, Zap, Network, Leaf, Users, ShieldAlert, Cpu, Sun, Wrench, Volume2, Droplets, Bus, Utensils, Shuffle, GraduationCap, FileText } from 'lucide-react';

const groups = [
  {
    title: 'Campus operations',
    note: 'Space, flow and student-service experiments.',
    items: [
      ['/flow', 'Flow model', 'Synthetic campus movement and congestion exploration.', Users],
      ['/rescheduler', 'Room consolidation', 'What-if timetable and space consolidation workflow.', Shuffle],
      ['/agent-simulation', 'Agent simulation', 'Synthetic student-agent movement experiment.', FlaskConical],
      ['/student', 'Student decision support', 'Prototype study-space and campus recommendation surface.', GraduationCap],
    ],
  },
  {
    title: 'Energy systems',
    note: 'Future control and generation workflows.',
    items: [
      ['/microgrid', 'Energy scenario', 'Wind, storage and demand scenario visualization.', Zap],
      ['/control-room', 'Control room', 'BMS/SCADA integration concept; no live BMS is connected.', Cpu],
      ['/solar', 'Rooftop solar', 'Solar potential and shading scenario prototype.', Sun],
      ['/maintenance', 'Predictive maintenance', 'Synthetic equipment condition and maintenance workflow.', Wrench],
    ],
  },
  {
    title: 'Sensing & integration',
    note: 'Concepts that require future authorized telemetry.',
    items: [
      ['/anomalies', 'Anomaly radar', 'Water and energy anomaly-detection concept.', ShieldAlert],
      ['/acoustic', 'Acoustic map', 'Sound-environment concept without a live microphone network.', Volume2],
      ['/iot-registry', 'IoT registry', 'Future device inventory and protocol model.', Network],
      ['/integrations', 'Protocol gateway', 'BACnet, Modbus and LoRaWAN integration concept.', Waves],
    ],
  },
  {
    title: 'Sustainability',
    note: 'Decision concepts for resource efficiency.',
    items: [
      ['/food-waste', 'Food waste', 'Cafeteria demand and waste-reduction prototype.', Utensils],
      ['/water', 'Water management', 'Rainwater and water-use optimization scenario.', Droplets],
      ['/transit', 'Mobility', 'Published shuttle schedule plus modeled demand workflow.', Bus],
      ['/esg-reports', 'Carbon reporting', 'Reporting template; not a certified audit.', FileText],
    ],
  },
] as const;

export default function LabPage() {
  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[30px] bg-[#0b1226] p-6 text-white sm:p-8">
        <div className="flex flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <span className="bc-chip border-amber-300/20 bg-amber-300/10 text-amber-200"><FlaskConical size={11} /> PROTOTYPE LAB</span>
            <h1 className="mt-5 max-w-3xl text-3xl font-black leading-[1.04] tracking-[-0.055em] sm:text-4xl">Explore future workflows without pretending they are live infrastructure.</h1>
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-slate-400">These experiments are intentionally separated from the production-facing campus intelligence workflow. They demonstrate what becomes possible when authorized telemetry, BMS, POS or sensor integrations arrive.</p>
          </div>
          <div className="rounded-[20px] border border-white/10 bg-white/[0.04] p-4 text-[11px] leading-relaxed text-slate-400 lg:max-w-xs">
            <div className="flex items-center gap-2 font-black text-white"><ShieldAlert size={14} className="text-amber-300" /> Truth boundary</div>
            <p className="mt-2">Values inside Lab modules may be synthetic, scenario-based or illustrative. The global prototype banner remains visible on every Lab route.</p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        {groups.map(group => (
          <div key={group.title} className="bc-surface rounded-[28px] p-5 sm:p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="bc-eyebrow">{group.title}</div>
                <p className="mt-1 text-[11px] text-slate-500">{group.note}</p>
              </div>
              <FlaskConical size={17} className="text-slate-300" />
            </div>
            <div className="mt-5 grid gap-2 sm:grid-cols-2">
              {group.items.map(([href, title, note, Icon]) => (
                <Link key={href} href={href} className="group rounded-[18px] border border-slate-950/8 bg-[#fafaf8] p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-sm">
                  <div className="flex items-center justify-between gap-3">
                    <div className="grid h-8 w-8 place-items-center rounded-xl bg-[#0b1226] text-white"><Icon size={14} /></div>
                    <ArrowUpRight size={12} className="text-slate-300 transition group-hover:text-blue-600" />
                  </div>
                  <h2 className="mt-4 text-xs font-black text-[#0a1020]">{title}</h2>
                  <p className="mt-1 text-[10px] leading-relaxed text-slate-500">{note}</p>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </section>

      <section className="rounded-[24px] border border-blue-200 bg-blue-50 p-5">
        <div className="flex gap-3">
          <Leaf size={17} className="mt-0.5 shrink-0 text-blue-700" />
          <div>
            <h2 className="text-xs font-black text-blue-950">Product rule</h2>
            <p className="mt-1 text-[11px] leading-relaxed text-blue-900/70">A Lab module can graduate into the main product only after its data source is authorized, provenance is explicit, failure states are truthful and the workflow produces a decision that a real campus operator can validate.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
