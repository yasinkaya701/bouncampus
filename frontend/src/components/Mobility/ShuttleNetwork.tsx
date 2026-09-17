'use client';

import { useMemo, useState } from 'react';
import { ArrowRight, BusFront, ExternalLink, Leaf, MapPin, Radio, Route, Users } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import {
  estimateAvoidedCarImpact,
  OFFICIAL_SHUTTLE_SOURCE,
  shuttleRoutes,
  shuttleStops,
  type ShuttleRoute,
  type ShuttleServiceType,
} from '@/lib/shuttle-network';

type Filter = 'all' | ShuttleServiceType;

const stopById = Object.fromEntries(shuttleStops.map(stop => [stop.id, stop]));

function ServiceBadge({ type }: { type: ShuttleServiceType }) {
  const { t } = useLocale();
  const label = type === 'campus_loop' ? t('Kampüs içi ring', 'Campus loop') : t('Kampüsler arası', 'Inter-campus');
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-[9px] font-black uppercase tracking-[0.08em] ${type === 'campus_loop' ? 'bg-sky-50 text-sky-800 ring-1 ring-sky-200' : 'bg-emerald-50 text-emerald-800 ring-1 ring-emerald-200'}`}>
      <BusFront size={10} /> {label}
    </span>
  );
}

function RouteCard({ route, selected, onSelect }: { route: ShuttleRoute; selected: boolean; onSelect: () => void }) {
  const { locale, t } = useLocale();
  const stops = route.stopIds.map(id => stopById[id]).filter(Boolean);

  return (
    <button
      type="button"
      onClick={onSelect}
      className={`bc-focus-ring w-full rounded-xl border p-4 text-left transition ${selected ? 'border-[#173f67]/35 bg-[#eef4f8] shadow-[0_12px_32px_rgba(16,42,67,0.08)]' : 'border-slate-900/10 bg-white hover:border-slate-900/20'}`}
    >
      <div className="flex items-start justify-between gap-3">
        <ServiceBadge type={route.serviceType} />
        <span className="font-mono text-[9px] font-black tracking-[0.08em] text-slate-400">{route.shortLabel}</span>
      </div>
      <h3 className="mt-4 text-[15px] font-black tracking-[-0.025em] text-slate-950">{locale === 'tr' ? route.nameTr : route.nameEn}</h3>
      <div className="mt-4 flex flex-wrap items-center gap-1.5">
        {stops.map((stop, index) => (
          <span key={stop.id} className="inline-flex items-center gap-1 text-[9px] font-semibold text-slate-500">
            <MapPin size={9} /> {locale === 'tr' ? stop.nameTr : stop.nameEn}
            {index < stops.length - 1 ? <ArrowRight size={9} className="ml-0.5 text-slate-300" /> : null}
          </span>
        ))}
      </div>
      <div className="mt-4 flex items-center justify-between border-t border-slate-900/8 pt-3 text-[9px]">
        <span className="font-semibold text-slate-400">{t('Mesafe: model tahmini', 'Distance: model estimate')}</span>
        <span className="font-mono font-black text-slate-700">~{route.distanceKmEstimate.toFixed(1)} km</span>
      </div>
    </button>
  );
}

export default function ShuttleNetwork() {
  const { locale, t } = useLocale();
  const [filter, setFilter] = useState<Filter>('all');
  const [selectedRouteId, setSelectedRouteId] = useState(shuttleRoutes[0]?.id ?? '');
  const [passengerTrips, setPassengerTrips] = useState(24);

  const filteredRoutes = useMemo(
    () => shuttleRoutes.filter(route => filter === 'all' || route.serviceType === filter),
    [filter],
  );

  const selectedRoute = shuttleRoutes.find(route => route.id === selectedRouteId) ?? filteredRoutes[0] ?? shuttleRoutes[0];
  const selectedStops = selectedRoute?.stopIds.map(id => stopById[id]).filter(Boolean) ?? [];
  const impact = selectedRoute ? estimateAvoidedCarImpact(selectedRoute, passengerTrips) : null;

  function applyFilter(next: Filter) {
    setFilter(next);
    const nextRoute = shuttleRoutes.find(route => next === 'all' || route.serviceType === next);
    if (nextRoute) setSelectedRouteId(nextRoute.id);
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
        <div className="rounded-2xl border border-slate-900/10 bg-[#102a43] p-6 text-white sm:p-7">
          <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.16em] text-sky-200"><Route size={13} /> {t('Mobilite ağı', 'Mobility network')}</div>
          <h2 className="mt-4 max-w-2xl text-[30px] font-black tracking-[-0.05em] sm:text-[38px]">{t('Aynı ürün içinde iki ayrı mekik mantığı.', 'Two shuttle modes, one mobility product.')}</h2>
          <p className="mt-4 max-w-2xl text-[12px] leading-6 text-slate-300">{t('Kampüs içi ring kısa mesafeli ana kampüs hareketini; kampüsler arası mekik ise Hisar, Kandilli, Anadolu Hisarı ve Kilyos gibi yerleşkeler arasındaki planlı ulaşımı temsil ediyor.', 'Campus loop covers short main-campus movement; inter-campus shuttle covers scheduled travel between sites such as Hisar, Kandilli, Anadolu Hisarı and Kilyos.')}</p>
          <div className="mt-6 flex flex-wrap gap-2">
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-[9px] font-bold text-white">{t('Resmî güzergâh kaynağı', 'Official route source')}</span>
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-[9px] font-bold text-white">{t('Canlı GPS iddiası yok', 'No live-GPS claim')}</span>
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-[9px] font-bold text-white">{t('Karbon: senaryo modeli', 'Carbon: scenario model')}</span>
          </div>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.12em] text-amber-800"><Radio size={12} /> {t('Veri sınırı', 'Data boundary')}</div>
          <p className="mt-3 text-[11px] leading-5 text-amber-950/75">{t('BOUNCAMPUS henüz üniversitenin mekik GPS, anlık doluluk veya araç kapasite sistemine bağlı değil. Bu yüzden “3 dk sonra burada” veya “%82 dolu” gibi sahte canlı metrikler göstermiyoruz.', 'BOUNCAMPUS is not connected to university shuttle GPS, real-time occupancy, or vehicle-capacity systems. We therefore do not invent live metrics such as “arrives in 3 min” or “82% full”.')}</p>
          <a href={OFFICIAL_SHUTTLE_SOURCE} target="_blank" rel="noreferrer" className="bc-focus-ring mt-4 inline-flex items-center gap-1.5 rounded-lg bg-amber-900 px-3 py-2 text-[10px] font-black text-white">
            {t('Resmî mekik saatleri', 'Official shuttle times')} <ExternalLink size={11} />
          </a>
        </div>
      </section>

      <section className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="text-[10px] font-black uppercase tracking-[0.14em] text-slate-400">{t('Servis tipi', 'Service type')}</div>
          <p className="mt-1 text-[11px] text-slate-500">{t('Ring ile kampüsler arası servisi birbirine karıştırmadan filtrele.', 'Filter campus loops and inter-campus services without mixing the two concepts.')}</p>
        </div>
        <div className="flex w-fit rounded-lg border border-slate-900/10 bg-white p-1">
          {([
            ['all', t('Tümü', 'All')],
            ['campus_loop', t('Kampüs içi', 'Campus loop')],
            ['inter_campus', t('Kampüsler arası', 'Inter-campus')],
          ] as Array<[Filter, string]>).map(([value, label]) => (
            <button key={value} type="button" onClick={() => applyFilter(value)} className={`bc-focus-ring rounded-md px-3 py-2 text-[9px] font-black ${filter === value ? 'bg-[#102a43] text-white' : 'text-slate-500 hover:text-slate-900'}`}>
              {label}
            </button>
          ))}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.05fr)_minmax(380px,0.95fr)]">
        <div className="grid gap-3 md:grid-cols-2">
          {filteredRoutes.map(route => (
            <RouteCard key={route.id} route={route} selected={route.id === selectedRoute?.id} onSelect={() => setSelectedRouteId(route.id)} />
          ))}
        </div>

        {selectedRoute ? (
          <aside className="self-start rounded-2xl border border-slate-900/10 bg-white p-5 xl:sticky xl:top-24">
            <div className="flex items-start justify-between gap-3">
              <div>
                <ServiceBadge type={selectedRoute.serviceType} />
                <h3 className="mt-3 text-[20px] font-black tracking-[-0.035em] text-slate-950">{locale === 'tr' ? selectedRoute.nameTr : selectedRoute.nameEn}</h3>
              </div>
              <BusFront size={24} className="text-[#173f67]" />
            </div>

            <div className="mt-6 space-y-0">
              {selectedStops.map((stop, index) => (
                <div key={stop.id} className="grid grid-cols-[20px_1fr] gap-3">
                  <div className="flex flex-col items-center">
                    <div className="mt-1 h-2.5 w-2.5 rounded-full bg-[#173f67] ring-4 ring-sky-50" />
                    {index < selectedStops.length - 1 ? <div className="min-h-10 w-px flex-1 bg-slate-200" /> : null}
                  </div>
                  <div className="pb-5">
                    <div className="text-[11px] font-black text-slate-900">{locale === 'tr' ? stop.nameTr : stop.nameEn}</div>
                    <div className="mt-0.5 text-[9px] font-semibold text-slate-400">{stop.campus}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-2 border-t border-slate-900/8 pt-4">
              <div className="rounded-lg bg-slate-50 p-3">
                <div className="flex items-center gap-1 text-[9px] font-black uppercase tracking-[0.08em] text-slate-400"><Users size={10} /> {t('Doluluk', 'Occupancy')}</div>
                <div className="mt-2 text-[12px] font-black text-slate-800">{t('Canlı veri yok', 'No live feed')}</div>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <div className="flex items-center gap-1 text-[9px] font-black uppercase tracking-[0.08em] text-slate-400"><Radio size={10} /> ETA</div>
                <div className="mt-2 text-[12px] font-black text-slate-800">{t('Tarife kaynağı', 'Schedule source')}</div>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4">
              <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.1em] text-emerald-800"><Leaf size={12} /> {t('İklim senaryosu', 'Climate scenario')}</div>
              <label className="mt-4 block text-[9px] font-black uppercase tracking-[0.08em] text-emerald-950/60" htmlFor="passenger-trips">{t('Özel araç yerine mekik kullanan yolculuk', 'Trips shifted from private car to shuttle')}</label>
              <input id="passenger-trips" type="number" min={0} max={5000} value={passengerTrips} onChange={event => setPassengerTrips(Number(event.target.value) || 0)} className="bc-focus-ring mt-2 w-full rounded-lg border border-emerald-900/10 bg-white px-3 py-2.5 font-mono text-sm font-black text-emerald-950" />
              {impact ? (
                <div className="mt-4 grid grid-cols-2 gap-2">
                  <div className="rounded-lg bg-white/80 p-3"><div className="text-[8px] font-black uppercase tracking-[0.08em] text-emerald-800/60">{t('Kaçınılan araç-km', 'Avoided vehicle-km')}</div><div className="mt-1 font-mono text-lg font-black text-emerald-950">{impact.avoidedVehicleKm}</div></div>
                  <div className="rounded-lg bg-white/80 p-3"><div className="text-[8px] font-black uppercase tracking-[0.08em] text-emerald-800/60">{t('Kaçınılan kgCO₂e', 'Avoided kgCO₂e')}</div><div className="mt-1 font-mono text-lg font-black text-emerald-950">{impact.avoidedCarKgCo2eEstimate}</div></div>
                </div>
              ) : null}
              <p className="mt-3 text-[9px] leading-4 text-emerald-950/65">{t('Bu değer ölçüm değil; rota mesafesi, 1,2 kişi/özel araç ve 0,171 kgCO₂e/araç-km varsayımıyla üretilen karşı-olgusal senaryodur. Mekik aracının net emisyonunu temsil etmez.', 'This is not a measurement. It is a counterfactual scenario using route distance, 1.2 people/private car and 0.171 kgCO₂e/vehicle-km assumptions. It does not represent net shuttle emissions.')}</p>
            </div>

            <a href={selectedRoute.officialScheduleUrl} target="_blank" rel="noreferrer" className="bc-focus-ring mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#102a43] px-4 py-3 text-[10px] font-black text-white transition hover:bg-[#173f67]">
              {t('Güncel sefer saatini resmî kaynaktan aç', 'Open current timetable at official source')} <ExternalLink size={11} />
            </a>
          </aside>
        ) : null}
      </section>
    </div>
  );
}
