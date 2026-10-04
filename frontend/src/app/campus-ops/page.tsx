'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BookOpenCheck,
  Building2,
  BusFront,
  CheckCircle2,
  CircleAlert,
  Compass,
  Database,
  Loader2,
  MapPinned,
  ShieldCheck,
  Utensils,
} from 'lucide-react';
import { useLocale } from '@/lib/i18n';

type Readiness = 'READY' | 'REVIEW_REQUIRED' | 'WITHHOLD';

type ShuttleStop = {
  id: string;
  nameTr: string;
  nameEn: string;
  campus: string;
};

type ShuttleNetworkResponse = {
  source: { name: string; url: string; provenance: string };
  stops: ShuttleStop[];
  routes: Array<{ id: string; nameTr: string; nameEn: string; stopIds: string[] }>;
  truthBoundary: { tr: string; en: string };
};

type ShuttleRecommendation = {
  originStopId: string;
  destinationStopId: string;
  routeIds: string[];
  transferStopIds: string[];
  transfers: number;
  estimatedDistanceKm: number;
  policyScore: number;
  officialScheduleUrl: string | null;
  timingStatus: string;
  telemetryStatus: string;
};

type ShuttleDecisionResponse = {
  decision: {
    readiness: Readiness;
    abstained: boolean;
    operatorApprovalRequired: true;
    automaticDispatchAllowed: false;
    reasonCodes: string[];
    limitations: string[];
    recommendation: ShuttleRecommendation | null;
  };
  privateCarReplacementScenario: {
    passengerTrips: number;
    avoidedVehicleKmEstimate: number;
    avoidedCarKgCo2eEstimate: number;
    achievedImpact: false;
  } | null;
  truthBoundary: {
    liveGpsConnected: false;
    liveOccupancyConnected: false;
    verifiedVehicleCapacityConnected: false;
    departureTimes: string;
  };
};

type SpaceInventoryResponse = {
  source: {
    term: string;
    capturedAt: string;
    sourceUrl: string;
    sourceClass: string;
    refreshRequiredAfter: string;
  };
  inventory: {
    roomsObservedInScheduleSnapshot: number;
    roomIds: string[];
    roomCapacitySource: string;
  };
  readiness: Readiness;
  reasonCodes: string[];
  truthBoundary: {
    liveRoomOccupancyConnected: false;
    accessControlConnected: false;
    bmsConnected: false;
    universityVerifiedRoomCapacityConnected: false;
    automaticRoomBooking: false;
    note: string;
  };
};

type SpaceAllocationResponse = {
  decisions: Array<{
    readiness: Readiness;
    abstained: boolean;
    reasonCodes: string[];
    limitations: string[];
    operatorApprovalRequired: true;
    automaticDispatchAllowed: false;
    recommendation: {
      requestId: string;
      roomId: string;
      day: string;
      startHour: number;
      durationHours: number;
      occupiedHours: number[];
      capacityStatus: string;
      verifiedCapacity: number | null;
    } | null;
  }>;
  assignedRequestIds: string[];
  unassignedRequestIds: string[];
  source: SpaceInventoryResponse['source'];
  truthBoundary: SpaceInventoryResponse['truthBoundary'];
};

const dayOptions = [
  { id: 'M', tr: 'Pazartesi', en: 'Monday' },
  { id: 'T', tr: 'Salı', en: 'Tuesday' },
  { id: 'W', tr: 'Çarşamba', en: 'Wednesday' },
  { id: 'Th', tr: 'Perşembe', en: 'Thursday' },
  { id: 'F', tr: 'Cuma', en: 'Friday' },
];

function readinessClass(readiness: Readiness) {
  if (readiness === 'READY') return 'border-emerald-200 bg-emerald-50 text-emerald-800';
  if (readiness === 'REVIEW_REQUIRED') return 'border-amber-200 bg-amber-50 text-amber-800';
  return 'border-rose-200 bg-rose-50 text-rose-800';
}

function ReadinessBadge({ readiness }: { readiness: Readiness }) {
  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-1 font-mono text-[9px] font-black tracking-[0.08em] ${readinessClass(readiness)}`}>
      {readiness}
    </span>
  );
}

function ReasonCodes({ codes }: { codes: string[] }) {
  if (codes.length === 0) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-1.5">
      {codes.map(code => (
        <span key={code} className="rounded-md border border-slate-900/[0.07] bg-slate-50 px-2 py-1 font-mono text-[8px] font-bold text-slate-500">
          {code}
        </span>
      ))}
    </div>
  );
}

export default function CampusOperationsPage() {
  const { locale, t } = useLocale();
  const [network, setNetwork] = useState<ShuttleNetworkResponse | null>(null);
  const [spaceInventory, setSpaceInventory] = useState<SpaceInventoryResponse | null>(null);
  const [bootstrapError, setBootstrapError] = useState<string | null>(null);

  const [origin, setOrigin] = useState('south-square');
  const [destination, setDestination] = useState('north-campus');
  const [passengerTrips, setPassengerTrips] = useState('');
  const [shuttleLoading, setShuttleLoading] = useState(false);
  const [shuttleError, setShuttleError] = useState<string | null>(null);
  const [shuttleResult, setShuttleResult] = useState<ShuttleDecisionResponse | null>(null);

  const [day, setDay] = useState('M');
  const [startHour, setStartHour] = useState('10');
  const [durationHours, setDurationHours] = useState('1');
  const [preferredRoom, setPreferredRoom] = useState('');
  const [requiredCapacity, setRequiredCapacity] = useState('');
  const [spaceLoading, setSpaceLoading] = useState(false);
  const [spaceError, setSpaceError] = useState<string | null>(null);
  const [spaceResult, setSpaceResult] = useState<SpaceAllocationResponse | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      fetch('/api/v1/shuttles').then(async response => {
        if (!response.ok) throw new Error('shuttle_network_unavailable');
        return response.json() as Promise<ShuttleNetworkResponse>;
      }),
      fetch('/api/v1/spaces/allocate').then(async response => {
        if (!response.ok) throw new Error('space_inventory_unavailable');
        return response.json() as Promise<SpaceInventoryResponse>;
      }),
    ])
      .then(([shuttleNetwork, rooms]) => {
        if (cancelled) return;
        setNetwork(shuttleNetwork);
        setSpaceInventory(rooms);
        setBootstrapError(null);
      })
      .catch(error => {
        if (cancelled) return;
        setBootstrapError(error instanceof Error ? error.message : 'bootstrap_failed');
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const stopName = useMemo(() => {
    const map = new Map<string, string>();
    for (const stop of network?.stops ?? []) {
      map.set(stop.id, locale === 'tr' ? stop.nameTr : stop.nameEn);
    }
    return map;
  }, [network, locale]);

  async function submitShuttle(event: FormEvent) {
    event.preventDefault();
    setShuttleLoading(true);
    setShuttleError(null);
    try {
      const params = new URLSearchParams({ origin, destination });
      if (passengerTrips.trim()) params.set('passengerTrips', passengerTrips.trim());
      const response = await fetch(`/api/v1/shuttles/recommend?${params.toString()}`, { cache: 'no-store' });
      const body = await response.json() as ShuttleDecisionResponse | { error?: string };
      if (!response.ok) throw new Error('error' in body && body.error ? body.error : 'shuttle_recommendation_failed');
      setShuttleResult(body as ShuttleDecisionResponse);
    } catch (error) {
      setShuttleResult(null);
      setShuttleError(error instanceof Error ? error.message : 'shuttle_recommendation_failed');
    } finally {
      setShuttleLoading(false);
    }
  }

  async function submitSpace(event: FormEvent) {
    event.preventDefault();
    setSpaceLoading(true);
    setSpaceError(null);
    try {
      const start = Number(startHour);
      const duration = Number(durationHours);
      const capacity = requiredCapacity.trim() ? Number(requiredCapacity) : undefined;
      const request = {
        requestId: `console-${Date.now()}`,
        day,
        startHour: start,
        durationHours: duration,
        ...(preferredRoom ? { candidateRooms: [preferredRoom] } : {}),
        ...(capacity !== undefined ? { requiredCapacity: capacity } : {}),
      };
      const response = await fetch('/api/v1/spaces/allocate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requests: [request] }),
      });
      const body = await response.json() as SpaceAllocationResponse | { error?: string };
      if (!response.ok) throw new Error('error' in body && body.error ? body.error : 'space_allocation_failed');
      setSpaceResult(body as SpaceAllocationResponse);
    } catch (error) {
      setSpaceResult(null);
      setSpaceError(error instanceof Error ? error.message : 'space_allocation_failed');
    } finally {
      setSpaceLoading(false);
    }
  }

  const selectedSpaceDecision = spaceResult?.decisions[0] ?? null;

  return (
    <div className="space-y-5 sm:space-y-6">
      <section className="overflow-hidden rounded-[32px] border border-white/10 bg-[#07131f] text-white shadow-[0_28px_80px_rgba(7,19,31,.16)]">
        <div className="grid lg:grid-cols-[1.15fr_.85fr]">
          <div className="p-6 sm:p-8 lg:p-10">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full border border-[#b8e467]/20 bg-[#b8e467]/10 px-3 py-1.5 text-[9px] font-black uppercase tracking-[0.15em] text-[#dff6ae]">
                CS1 · CAMPUS OPERATIONS
              </span>
              <span className="rounded-full border border-white/10 bg-white/[0.05] px-3 py-1.5 text-[9px] font-black text-white/55">
                HUMAN APPROVAL REQUIRED
              </span>
            </div>
            <h1 className="mt-7 max-w-4xl text-[42px] font-black leading-[0.95] tracking-[-0.065em] sm:text-[58px]">
              {t('Yemek, mekik ve mekân kararlarını aynı güvenli karar katmanında çalıştır.', 'Run food, shuttle and space decisions through one safe decision layer.')}
            </h1>
            <p className="mt-5 max-w-3xl text-[12px] leading-6 text-white/58">
              {t(
                'Bu ekran canlı veri varmış gibi davranmaz. Resmî kaynak, snapshot, politika sezgiseli ve senaryo çıktıları ayrı provenance sınıflarıyla tutulur; eksik kanıt varsa sistem REVIEW_REQUIRED veya WITHHOLD üretir.',
                'This surface does not pretend live telemetry exists. Official sources, snapshots, policy heuristics and scenarios remain distinct provenance classes; missing evidence degrades the result to REVIEW_REQUIRED or WITHHOLD.',
              )}
            </p>
          </div>
          <div className="grid gap-px border-t border-white/10 bg-white/10 sm:grid-cols-3 lg:grid-cols-1 lg:border-l lg:border-t-0">
            <DomainStatus icon={Utensils} label={t('Yemekhane', 'Food')} state="PRODUCTION DECISION" detail={t('Mevcut food-waste motoru + pilot kapısı', 'Existing food-waste engine + pilot gate')} />
            <DomainStatus icon={BusFront} label={t('Mekik', 'Shuttle')} state="TOPOLOGY DECISION" detail={t('Direkt / transfer rota + resmî sefer kontrolü', 'Direct / transfer routing + official timetable check')} />
            <DomainStatus icon={BookOpenCheck} label={t('Sınıf / alan', 'Class / space')} state="CONSTRAINT DECISION" detail={t('Program çakışması + batch rezervasyonu', 'Schedule conflicts + batch reservation')} />
          </div>
        </div>
      </section>

      {bootstrapError ? (
        <div className="flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-800">
          <CircleAlert className="mt-0.5 shrink-0" size={16} />
          <div className="text-[11px] leading-5">
            <div className="font-black">{t('Kaynak bootstrap hatası', 'Source bootstrap error')}</div>
            <div className="font-mono text-[9px]">{bootstrapError}</div>
          </div>
        </div>
      ) : null}

      <section className="grid gap-4 xl:grid-cols-2">
        <article className="rounded-[28px] border border-slate-900/[0.08] bg-white p-5 shadow-[0_16px_45px_rgba(15,23,42,.045)] sm:p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#173f67]"><BusFront size={12} /> {t('Mekik karar motoru', 'Shuttle decision engine')}</div>
              <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('Güzergâh seç', 'Choose an itinerary')}</h2>
              <p className="mt-2 max-w-xl text-[10px] leading-5 text-slate-500">{t('Rota topolojisini optimize eder; canlı kalkış saati, GPS veya doluluk iddiası üretmez.', 'Optimizes route topology; it does not claim live departure times, GPS or occupancy.')}</p>
            </div>
            <span className="rounded-xl border border-slate-900/[0.07] bg-slate-50 p-2.5 text-slate-500"><MapPinned size={17} /></span>
          </div>

          <form onSubmit={submitShuttle} className="mt-5 grid gap-3 sm:grid-cols-2">
            <Field label={t('Başlangıç', 'Origin')}>
              <select value={origin} onChange={event => setOrigin(event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" disabled={!network}>
                {(network?.stops ?? []).map(stop => <option key={stop.id} value={stop.id}>{locale === 'tr' ? stop.nameTr : stop.nameEn}</option>)}
              </select>
            </Field>
            <Field label={t('Hedef', 'Destination')}>
              <select value={destination} onChange={event => setDestination(event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" disabled={!network}>
                {(network?.stops ?? []).map(stop => <option key={stop.id} value={stop.id}>{locale === 'tr' ? stop.nameTr : stop.nameEn}</option>)}
              </select>
            </Field>
            <Field label={t('Senaryo yolcu yolculuğu · opsiyonel', 'Scenario passenger trips · optional')}>
              <input value={passengerTrips} onChange={event => setPassengerTrips(event.target.value)} inputMode="numeric" min="0" max="100000" type="number" placeholder="120" className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" />
            </Field>
            <div className="flex items-end">
              <button type="submit" disabled={!network || shuttleLoading} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-xl bg-[#071c33] px-4 py-2.5 text-[10px] font-black text-white transition hover:bg-[#0b3153] disabled:cursor-not-allowed disabled:opacity-50">
                {shuttleLoading ? <Loader2 className="animate-spin" size={13} /> : <BusFront size={13} />}
                {t('Rotayı hesapla', 'Compute route')}
              </button>
            </div>
          </form>

          {shuttleError ? <ErrorLine value={shuttleError} /> : null}
          {shuttleResult ? (
            <div className="mt-5 rounded-2xl border border-slate-900/[0.07] bg-[#f7f9f6] p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="text-[10px] font-black text-slate-800">{t('Karar', 'Decision')}</div>
                <ReadinessBadge readiness={shuttleResult.decision.readiness} />
              </div>
              {shuttleResult.decision.recommendation ? (
                <div className="mt-4 grid gap-2 sm:grid-cols-3">
                  <Metric label={t('Rota', 'Route')} value={shuttleResult.decision.recommendation.routeIds.join(' → ')} />
                  <Metric label={t('Transfer', 'Transfers')} value={String(shuttleResult.decision.recommendation.transfers)} />
                  <Metric label={t('Tahmini topoloji mesafesi', 'Topology distance estimate')} value={`${shuttleResult.decision.recommendation.estimatedDistanceKm} km`} />
                  <div className="sm:col-span-3 text-[10px] text-slate-500">
                    {stopName.get(shuttleResult.decision.recommendation.originStopId) ?? shuttleResult.decision.recommendation.originStopId}
                    {' → '}
                    {stopName.get(shuttleResult.decision.recommendation.destinationStopId) ?? shuttleResult.decision.recommendation.destinationStopId}
                  </div>
                </div>
              ) : (
                <p className="mt-3 text-[10px] text-slate-500">{t('Politika uygulanabilir güzergâh önermedi.', 'Policy withheld an itinerary.')}</p>
              )}
              <ReasonCodes codes={shuttleResult.decision.reasonCodes} />
              {shuttleResult.privateCarReplacementScenario ? (
                <div className="mt-3 rounded-xl border border-sky-100 bg-sky-50 p-3 text-[9px] leading-4 text-sky-900">
                  <b>SCENARIO:</b> {shuttleResult.privateCarReplacementScenario.avoidedCarKgCo2eEstimate} kgCO₂e {t('özel araç ikame tahmini; gerçekleşmiş etki değildir.', 'private-car replacement estimate; not achieved impact.')}
                </div>
              ) : null}
            </div>
          ) : null}
        </article>

        <article className="rounded-[28px] border border-slate-900/[0.08] bg-white p-5 shadow-[0_16px_45px_rgba(15,23,42,.045)] sm:p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#173f67]"><BookOpenCheck size={12} /> {t('Sınıf / çalışma alanı tahsisi', 'Class / study-space allocation')}</div>
              <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('Çakışmasız alan seç', 'Allocate a conflict-free room')}</h2>
              <p className="mt-2 max-w-xl text-[10px] leading-5 text-slate-500">{t('Resmî ders programı snapshot’ında çakışmayı engeller. Canlı kapı sensörü veya rezervasyon yetkisi yoktur.', 'Blocks conflicts against the official timetable snapshot. There is no live door sensor or booking authority.')}</p>
            </div>
            {spaceInventory ? <ReadinessBadge readiness={spaceInventory.readiness} /> : <Loader2 className="animate-spin text-slate-300" size={18} />}
          </div>

          {spaceInventory ? (
            <div className="mt-4 flex flex-wrap items-center gap-2 text-[9px] text-slate-500">
              <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1"><b>{spaceInventory.inventory.roomsObservedInScheduleSnapshot}</b> {t('gözlenen oda', 'observed rooms')}</span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1">{spaceInventory.source.term}</span>
              {spaceInventory.reasonCodes.map(code => <span key={code} className="rounded-full border border-amber-200 bg-amber-50 px-2.5 py-1 font-mono text-amber-800">{code}</span>)}
            </div>
          ) : null}

          <form onSubmit={submitSpace} className="mt-5 grid gap-3 sm:grid-cols-2">
            <Field label={t('Gün', 'Day')}>
              <select value={day} onChange={event => setDay(event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800">
                {dayOptions.map(option => <option key={option.id} value={option.id}>{locale === 'tr' ? option.tr : option.en}</option>)}
              </select>
            </Field>
            <Field label={t('Başlangıç saati indeksi', 'Start hour index')}>
              <input value={startHour} onChange={event => setStartHour(event.target.value)} type="number" min="0" max="23" className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" />
            </Field>
            <Field label={t('Süre · saat', 'Duration · hours')}>
              <input value={durationHours} onChange={event => setDurationHours(event.target.value)} type="number" min="1" max="8" className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" />
            </Field>
            <Field label={t('Tercih edilen oda · opsiyonel', 'Preferred room · optional')}>
              <select value={preferredRoom} onChange={event => setPreferredRoom(event.target.value)} className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" disabled={!spaceInventory}>
                <option value="">{t('Motor seçsin', 'Let engine choose')}</option>
                {(spaceInventory?.inventory.roomIds ?? []).map(roomId => <option key={roomId} value={roomId}>{roomId}</option>)}
              </select>
            </Field>
            <Field label={t('Gerekli kapasite · opsiyonel', 'Required capacity · optional')}>
              <input value={requiredCapacity} onChange={event => setRequiredCapacity(event.target.value)} type="number" min="1" placeholder="30" className="bc-focus-ring w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-[11px] font-bold text-slate-800" />
              <div className="mt-1 text-[8px] leading-4 text-slate-400">{t('Doğrulanmış kapasite feed’i yoksa REVIEW_REQUIRED üretir.', 'Without a verified capacity feed this becomes REVIEW_REQUIRED.')}</div>
            </Field>
            <div className="flex items-end">
              <button type="submit" disabled={!spaceInventory || spaceLoading} className="bc-focus-ring flex w-full items-center justify-center gap-2 rounded-xl bg-[#071c33] px-4 py-2.5 text-[10px] font-black text-white transition hover:bg-[#0b3153] disabled:cursor-not-allowed disabled:opacity-50">
                {spaceLoading ? <Loader2 className="animate-spin" size={13} /> : <Building2 size={13} />}
                {t('Alan tahsis et', 'Allocate space')}
              </button>
            </div>
          </form>

          {spaceError ? <ErrorLine value={spaceError} /> : null}
          {selectedSpaceDecision ? (
            <div className="mt-5 rounded-2xl border border-slate-900/[0.07] bg-[#f7f9f6] p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="text-[10px] font-black text-slate-800">{t('Tahsis kararı', 'Allocation decision')}</div>
                <ReadinessBadge readiness={selectedSpaceDecision.readiness} />
              </div>
              {selectedSpaceDecision.recommendation ? (
                <div className="mt-4 grid gap-2 sm:grid-cols-3">
                  <Metric label={t('Oda', 'Room')} value={selectedSpaceDecision.recommendation.roomId} />
                  <Metric label={t('Slot', 'Slots')} value={selectedSpaceDecision.recommendation.occupiedHours.join(', ')} />
                  <Metric label={t('Kapasite durumu', 'Capacity status')} value={selectedSpaceDecision.recommendation.capacityStatus} />
                </div>
              ) : (
                <p className="mt-3 text-[10px] text-slate-500">{t('Hard constraint’ler nedeniyle tahsis yapılmadı.', 'Allocation was withheld by hard constraints.')}</p>
              )}
              <ReasonCodes codes={selectedSpaceDecision.reasonCodes} />
            </div>
          ) : null}
        </article>
      </section>

      <section className="grid gap-4 lg:grid-cols-[.85fr_1.15fr]">
        <article className="rounded-[28px] bg-[#0a1b2a] p-5 text-white sm:p-6">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#b8e467]"><Utensils size={12} /> {t('Yemekhane karar sistemi', 'Food decision system')}</div>
          <h2 className="mt-3 text-[30px] font-black leading-[1] tracking-[-0.055em]">{t('Talep → üretim önerisi → insan onayı → pilot ölçümü', 'Demand → production recommendation → human approval → pilot measurement')}</h2>
          <p className="mt-4 text-[10px] leading-5 text-white/52">{t('Food modülü bu konsolda kısaltılmadı; mevcut kaynak-traceable karar motoru, claim firewall ve pilot akışı korunuyor.', 'The food module is not reduced here; the existing source-traceable decision engine, claim firewall and pilot workflow remain intact.')}</p>
          <Link href="/food-waste" className="mt-5 inline-flex items-center gap-2 rounded-xl bg-[#b8e467] px-4 py-3 text-[10px] font-black text-[#071c33] transition hover:-translate-y-0.5">
            {t('Yemekhane motorunu aç', 'Open food engine')} <ArrowRight size={11} />
          </Link>
        </article>

        <article className="rounded-[28px] border border-slate-900/[0.08] bg-white p-5 sm:p-6">
          <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-[0.14em] text-[#173f67]"><Compass size={12} /> {t('Aynı operasyon ağı', 'Same operations network')}</div>
          <h2 className="mt-2 text-[28px] font-black tracking-[-0.05em] text-slate-950">{t('CS1 karar katmanı diğer kampüs yüzeylerine de bağlanır.', 'The CS1 decision layer connects to the rest of campus operations.')}</h2>
          <div className="mt-5 grid gap-2 sm:grid-cols-2">
            <SystemLink href="/mobility" icon={BusFront} title={t('Mekik ağı', 'Mobility network')} detail={t('Hatlar, resmi kaynak ve climate scenario', 'Routes, official source and climate scenario')} />
            <SystemLink href="/courses" icon={BookOpenCheck} title={t('Ders bağlamı', 'Course context')} detail={t('Resmî dönem programı snapshot’ı', 'Official term schedule snapshot')} />
            <SystemLink href="/buildings" icon={Building2} title={t('Binalar', 'Buildings')} detail={t('Mekânsal operasyon bağlamı', 'Spatial operations context')} />
            <SystemLink href="/scenarios" icon={Compass} title={t('Senaryolar', 'Scenarios')} detail={t('Gerçekleşmiş etki olmayan what-if katmanı', 'What-if layer, not achieved impact')} />
            <SystemLink href="/decisions" icon={CheckCircle2} title={t('Karar kayıtları', 'Decision records')} detail={t('İnsan kapısı ve audit trail', 'Human gate and audit trail')} />
            <SystemLink href="/data" icon={Database} title={t('Kanıt katmanı', 'Evidence layer')} detail={t('Kaynak sınıfı ve provenance görünürlüğü', 'Source class and provenance visibility')} />
          </div>
        </article>
      </section>

      <section className="rounded-[24px] border border-slate-900/[0.07] bg-[#f4f7f2] p-4 sm:p-5">
        <div className="flex items-start gap-3">
          <ShieldCheck className="mt-0.5 shrink-0 text-[#173f67]" size={17} />
          <div>
            <div className="text-[10px] font-black text-slate-800">{t('CS1 truth boundary', 'CS1 truth boundary')}</div>
            <p className="mt-1 text-[9px] leading-5 text-slate-500">
              {t('Hiçbir modül otomatik dispatch yapmaz. Mekikte canlı GPS/doluluk/ETA yok; alan tahsisinde canlı oda doluluğu/BMS/access-control ve doğrulanmış kapasite feed’i yok. Bu eksikler recommendation’ı saklanmadan readiness ve reason code olarak görünür.', 'No module performs automatic dispatch. Shuttle has no live GPS/occupancy/ETA; space allocation has no live room occupancy/BMS/access-control or verified capacity feed. These gaps remain visible through readiness and reason codes instead of being hidden.')}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

function DomainStatus({ icon: Icon, label, state, detail }: { icon: typeof Utensils; label: string; state: string; detail: string }) {
  return (
    <div className="bg-[#0a1b2a] p-5 lg:p-6">
      <div className="flex items-center gap-2 text-[10px] font-black"><Icon size={13} className="text-[#b8e467]" /> {label}</div>
      <div className="mt-3 font-mono text-[8px] font-black tracking-[0.08em] text-[#b8e467]">{state}</div>
      <div className="mt-1 text-[9px] leading-4 text-white/42">{detail}</div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-[9px] font-black uppercase tracking-[0.08em] text-slate-500">{label}</span>
      {children}
    </label>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-900/[0.06] bg-white p-3">
      <div className="text-[8px] font-black uppercase tracking-[0.08em] text-slate-400">{label}</div>
      <div className="mt-1 break-words text-[11px] font-black text-slate-800">{value}</div>
    </div>
  );
}

function ErrorLine({ value }: { value: string }) {
  return (
    <div className="mt-3 flex items-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-[9px] font-bold text-rose-800">
      <CircleAlert size={11} /> {value}
    </div>
  );
}

function SystemLink({ href, icon: Icon, title, detail }: { href: string; icon: typeof BusFront; title: string; detail: string }) {
  return (
    <Link href={href} className="group rounded-2xl border border-slate-900/[0.07] bg-[#f8faf7] p-4 transition hover:-translate-y-0.5 hover:bg-white hover:shadow-[0_12px_30px_rgba(15,23,42,.06)]">
      <div className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-2 text-[10px] font-black text-slate-800"><Icon size={12} className="text-[#173f67]" /> {title}</span>
        <ArrowRight size={11} className="text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-slate-700" />
      </div>
      <div className="mt-2 text-[9px] leading-4 text-slate-450">{detail}</div>
    </Link>
  );
}
