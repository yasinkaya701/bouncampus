'use client';

import Link from 'next/link';
import { ArrowUpRight, Bus, Cpu, Droplets, FileText, FlaskConical, GraduationCap, Network, ShieldAlert, Shuffle, Sun, Users, Utensils, Volume2, Waves, Wrench, Zap } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

const groups = [
  { tr: 'Kampüs operasyonları', en: 'Campus operations', items: [
    ['/flow', 'Akış modeli', 'Flow model', Users], ['/rescheduler', 'Derslik konsolidasyonu', 'Room consolidation', Shuffle], ['/agent-simulation', 'Ajan simülasyonu', 'Agent simulation', FlaskConical], ['/student', 'Öğrenci karar desteği', 'Student decision support', GraduationCap],
  ] },
  { tr: 'Enerji sistemleri', en: 'Energy systems', items: [
    ['/microgrid', 'Enerji senaryosu', 'Energy scenario', Zap], ['/control-room', 'Kontrol odası', 'Control room', Cpu], ['/solar', 'Çatı GES', 'Rooftop solar', Sun], ['/maintenance', 'Kestirimci bakım', 'Predictive maintenance', Wrench],
  ] },
  { tr: 'Algılama ve entegrasyon', en: 'Sensing & integration', items: [
    ['/anomalies', 'Anomali modeli', 'Anomaly model', ShieldAlert], ['/acoustic', 'Akustik harita', 'Acoustic map', Volume2], ['/iot-registry', 'IoT envanteri', 'IoT registry', Network], ['/integrations', 'Protokol geçidi', 'Protocol gateway', Waves],
  ] },
  { tr: 'Sürdürülebilirlik', en: 'Sustainability', items: [
    ['/food-waste', 'Gıda israfı', 'Food waste', Utensils], ['/water', 'Su yönetimi', 'Water management', Droplets], ['/transit', 'Mekik ve mobilite', 'Shuttle & mobility', Bus], ['/esg-reports', 'Karbon raporu', 'Carbon reporting', FileText],
  ] },
] as const;

export default function LabPage() {
  const { locale, t } = useLocale();
  return <div className="space-y-7"><section className="border-b border-slate-900/10 pb-7"><div className="text-[10px] font-black uppercase tracking-[0.16em] text-amber-700">{t('Deneysel alan', 'Experimental area')}</div><h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Deneyler', 'Lab')}</h1><p className="mt-3 max-w-2xl text-[12px] leading-6 text-slate-500">{t('Gerçek altyapı bağlantısı bulunmayan gelecek iş akışları ana üründen ayrı tutulur. Buradaki değerler sentetik, senaryo tabanlı veya açıklayıcı olabilir.', 'Future workflows without authorized infrastructure connections stay outside the core product. Values here may be synthetic, scenario-based or illustrative.')}</p></section><div className="flex items-start gap-2 border border-amber-200 bg-amber-50 p-3 text-[10px] leading-5 text-amber-900"><ShieldAlert size={14} className="mt-0.5 shrink-0" /> {t('Lab modülleri gerçek BMS, sensör, POS veya IoT telemetrisi iddiasında bulunmaz.', 'Lab modules do not claim to be connected BMS, sensor, POS or IoT telemetry.')}</div><section className="grid gap-7 lg:grid-cols-2">{groups.map(group => <div key={group.en} className="border-t border-slate-900/10 pt-4"><h2 className="text-[12px] font-black text-slate-900">{locale === 'tr' ? group.tr : group.en}</h2><div className="mt-3 divide-y divide-slate-900/8 border-y border-slate-900/10 bg-white">{group.items.map(([href, tr, en, Icon]) => <Link key={href} href={href} className="flex items-center justify-between gap-3 px-3 py-3 hover:bg-slate-50"><div className="flex items-center gap-3"><Icon size={14} className="text-slate-400" /><span className="text-[11px] font-bold text-slate-800">{locale === 'tr' ? tr : en}</span></div><ArrowUpRight size={11} className="text-slate-300" /></Link>)}</div></div>)}</section></div>;
}
