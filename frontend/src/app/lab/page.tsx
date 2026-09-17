'use client';

import Link from 'next/link';
import { ArrowRight, Droplets, FlaskConical, MapPinned, ShieldAlert, Utensils } from 'lucide-react';
import { useLocale } from '@/lib/i18n';

export default function LabPage() {
  const { t } = useLocale();

  return <div className="space-y-8">
    <section className="border-b border-slate-900/10 pb-8">
      <div className="text-[10px] font-black uppercase tracking-[0.16em] text-amber-700">{t('Ürün yol haritası · jüri demosu değil', 'Product roadmap · not the jury demo')}</div>
      <h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Genişleme alanları', 'Expansion areas')}</h1>
      <p className="mt-3 max-w-3xl text-[12px] leading-6 text-slate-500">{t('KREATE için ana ürün tek probleme odaklanır: doluluk ve hava bağlamıyla bina enerjisi / karbon optimizasyonu. Aşağıdaki alanlar ancak güvenilir veri entegrasyonu ve ölçümlü pilot kanıtı olduğunda ürünleşir.', 'For KREATE, the core product owns one problem: building energy / carbon optimization using occupancy and weather context. The areas below become product surfaces only after trustworthy data integration and measured pilot evidence exist.')}</p>
    </section>

    <div className="flex items-start gap-2 border border-amber-200 bg-amber-50 p-3 text-[10px] leading-5 text-amber-900"><ShieldAlert size={14} className="mt-0.5 shrink-0" /> {t('Eski mock-heavy deney ekranları ana üründen kaldırıldı. Bağlı olmayan BMS, su sayacı, IoT sensörü, POS veya GPS varmış gibi operasyon rakamı gösterilmez.', 'Legacy mock-heavy experiment screens were removed from the primary product. We do not display operational numbers as if unconnected BMS, water meters, IoT sensors, POS or GPS feeds existed.')}</div>

    <section className="grid gap-4 lg:grid-cols-3">
      <article className="rounded-xl border border-slate-900/10 bg-white p-5"><Utensils size={18} className="text-slate-500" /><div className="mt-4 text-[10px] font-black uppercase tracking-[0.12em] text-slate-400">{t('İkinci kullanım alanı', 'Secondary use case')}</div><h2 className="mt-1 text-lg font-black tracking-[-0.03em]">{t('Gıda israfı', 'Food waste')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Ders programı + hava + menü ile talep tahmini. Gerçek doğrulama için anonim zaman dilimi POS toplamları gerekir.', 'Demand forecasting from schedule + weather + menu. Real validation requires anonymous time-bucket POS totals.')}</p><Link href="/food-waste" className="mt-4 inline-flex items-center gap-1 text-[10px] font-bold text-[#173f67]">{t('İkincil modeli gör', 'View secondary model')} <ArrowRight size={10} /></Link></article>

      <article className="rounded-xl border border-slate-900/10 bg-white p-5"><Droplets size={18} className="text-slate-500" /><div className="mt-4 text-[10px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Gelecek', 'Future')}</div><h2 className="mt-1 text-lg font-black tracking-[-0.03em]">{t('Su yönetimi', 'Water management')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Şimdilik ürün ekranı yok. Su sayacı / bina alt-sayaç verisi ve saha baz çizgisi olmadan tasarruf, sızıntı veya greywater iddiası yapılmaz.', 'There is no product screen yet. Savings, leak or greywater claims require water-meter / sub-meter data and a field baseline.')}</p></article>

      <article className="rounded-xl border border-slate-900/10 bg-white p-5"><MapPinned size={18} className="text-slate-500" /><div className="mt-4 text-[10px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Gelecek', 'Future')}</div><h2 className="mt-1 text-lg font-black tracking-[-0.03em]">{t('Mobilite', 'Mobility')}</h2><p className="mt-2 text-[10px] leading-5 text-slate-500">{t('Yayınlanmış mekik tarifesi bağlam olarak kullanılabilir; rota optimizasyonu veya gerçek zamanlı filo kararı için AVL/GPS gerekir.', 'Published shuttle timetables may be context; route optimization or real-time fleet decisions require AVL/GPS.')}</p></article>
    </section>

    <section className="border-t border-slate-900/10 pt-6"><div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.14em] text-slate-400"><FlaskConical size={12} /> {t('Ürün kuralı', 'Product rule')}</div><p className="mt-2 max-w-3xl text-[12px] leading-6 text-slate-600">{t('Önce bir problemi ölçülebilir biçimde çöz. Sonra aynı SENSE → DECIDE → STRESS-TEST → APPROVE → PILOT → LEARN altyapısını yeni kaynak alanlarına genişlet.', 'Solve one problem measurably first. Then extend the same SENSE → DECIDE → STRESS-TEST → APPROVE → PILOT → LEARN infrastructure to new resource domains.')}</p></section>
  </div>;
}
