'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  BarChart3,
  BookOpen,
  Building2,
  CalendarDays,
  Check,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  ClipboardCheck,
  Clock3,
  Database,
  Gauge,
  History,
  Leaf,
  LineChart,
  Menu,
  Pencil,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  TriangleAlert,
  Users,
  Utensils,
  XCircle,
} from 'lucide-react';
import {
  FOOD_WASTE_BASELINE,
  FOOD_WASTE_PILOT_PROTOCOL,
  FOOD_WASTE_SOURCE,
  type DecisionReadiness,
  type DemandSignal,
  type ProductionDecisionBand,
} from '@/lib/food-waste';
import { useLocale } from '@/lib/i18n';

type FoodApi = {
  demandContext: {
    available: boolean;
    actionable: boolean;
    planningCandidate: {
      portions: number;
      baselinePortions: number;
      lowerBound: number;
      upperBound: number;
      signalCoveragePct: number;
      sourceReadiness: DecisionReadiness;
      semantics: 'ADVISORY_MODEL_ESTIMATE_NOT_AUTHORIZED_KITCHEN_ORDER';
    } | null;
    productionBand: ProductionDecisionBand | null;
    decisionAssessment: ProductionDecisionBand | null;
    provenance: 'MODEL_ESTIMATE';
    note: string;
  };
  decisionPolicy: {
    humanApprovalRequired: boolean;
    automaticKitchenDispatch: boolean;
  };
};

type OperatorDecision = 'HOLD' | 'PILOT_APPROVED' | 'EDIT_REQUIRED';

type SignalView = DemandSignal & {
  source: 'OFFICIAL_SNAPSHOT' | 'EXTERNAL_LIVE';
};

const signalSource: Record<DemandSignal['id'], SignalView['source']> = {
  schedule: 'OFFICIAL_SNAPSHOT',
  weather: 'EXTERNAL_LIVE',
  menu: 'EXTERNAL_LIVE',
  calendar: 'OFFICIAL_SNAPSHOT',
};

const signalIcon: Record<DemandSignal['id'], typeof CalendarDays> = {
  schedule: BookOpen,
  weather: Activity,
  menu: Utensils,
  calendar: CalendarDays,
};

export default function FoodWastePage() {
  const { locale, t } = useLocale();
  const numberLocale = locale === 'tr' ? 'tr-TR' : 'en-US';
  const [food, setFood] = useState<FoodApi | null>(null);
  const [operatorDecision, setOperatorDecision] = useState<OperatorDecision>('HOLD');
  const [updatedAt, setUpdatedAt] = useState<Date | null>(null);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  useEffect(() => {
    fetch('/api/v1/food', { cache: 'no-store' })
      .then(response => (response.ok ? response.json() : null))
      .then((payload: FoodApi | null) => {
        setFood(payload);
        if (payload) setUpdatedAt(new Date());
      })
      .catch(() => setFood(null));
  }, []);

  const planningCandidate = food?.demandContext.planningCandidate ?? null;
  const assessmentBand = food?.demandContext.productionBand ?? food?.demandContext.decisionAssessment ?? null;
  const planningTarget = planningCandidate?.portions ?? assessmentBand?.recommendedTarget ?? null;
  const band = assessmentBand && planningTarget != null
    ? { ...assessmentBand, recommendedTarget: planningTarget }
    : null;
  const advisoryOnly = Boolean(planningCandidate) && !Boolean(food?.demandContext.actionable);
  const canApprovePilot = Boolean(food?.demandContext.actionable) && band?.decisionReadiness === 'PILOT_READY';
  const signals = useMemo<SignalView[]>(
    () => (band?.signals ?? []).map(signal => ({ ...signal, source: signalSource[signal.id] })),
    [band],
  );
  const healthySignals = signals.filter(signal => signal.available).length;
  const targetPosition = band
    ? Math.min(100, Math.max(0, ((band.recommendedTarget - band.lowerBound) / Math.max(1, band.upperBound - band.lowerBound)) * 100))
    : 50;

  const readinessLabel = band?.decisionReadiness ?? 'WITHHOLD';

  return (
    <div className="fixed inset-0 z-[70] overflow-hidden bg-[#f5f6f5] text-[#111713] antialiased">
      <div className="grid h-full lg:grid-cols-[248px_minmax(0,1fr)]">
        <aside className="hidden h-full flex-col border-r border-white/10 bg-[#071d18] text-white lg:flex">
          <div className="flex h-[72px] items-center gap-3 border-b border-white/10 px-5">
            <div className="grid h-9 w-9 place-items-center rounded-xl bg-white/10 text-[#a9e26d] ring-1 ring-white/10">
              <Leaf size={18} strokeWidth={2.2} />
            </div>
            <div>
              <div className="text-[15px] font-bold tracking-[-0.025em]">BOUNCAMPUS</div>
              <div className="mt-0.5 text-[10px] font-medium text-white/50">Campus Food Systems</div>
            </div>
          </div>

          <nav className="flex-1 px-3 py-5">
            <div className="space-y-1">
              <SidebarItem active icon={ClipboardCheck} label={t('Sonraki servis', 'Next service')} detail={t('Öğle · Bugün', 'Lunch · Today')} />
              <SidebarItem icon={Gauge} label={t('Kontrol paneli', 'Dashboard')} />
              <SidebarItem icon={Activity} label={t('Sinyaller', 'Signals')} detail={t('Veri kaynakları ve sağlık', 'Data sources & health')} />
              <SidebarItem icon={Database} label={t('Kanıt defteri', 'Evidence ledger')} detail={t('Resmi veri ve provenance', 'Official data & provenance')} />
              <SidebarItem icon={ClipboardCheck} label={t('Pilot protokolü', 'Pilot protocol')} detail={t('Tasarım ve başarı kriterleri', 'Design & success criteria')} />
              <SidebarItem icon={History} label={t('Karar geçmişi', 'Decision history')} detail={t('Önceki öneriler', 'Past recommendations')} />
            </div>

            <div className="my-5 border-t border-white/10" />

            <div className="space-y-1">
              <SidebarItem icon={LineChart} label={t('Analitik', 'Analytics')} badge="BETA" />
              <SidebarItem icon={Settings} label={t('Ayarlar', 'Settings')} />
              <SidebarItem icon={CircleHelp} label={t('Yardım ve dokümantasyon', 'Help & documentation')} />
            </div>
          </nav>

          <div className="p-3">
            <div className="flex items-center gap-3 rounded-xl border border-white/15 bg-white/[0.035] px-3.5 py-3">
              <Building2 size={17} className="text-white/70" />
              <div className="min-w-0 flex-1">
                <div className="truncate text-[11px] font-semibold">{t('Kuzey Kampüs', 'North Campus')}</div>
                <div className="mt-0.5 truncate text-[9px] text-white/45">{t('Ana Yemekhane', 'Main Dining Hall')}</div>
              </div>
              <ChevronRight size={14} className="text-white/45" />
            </div>
          </div>
        </aside>

        <div className="flex min-w-0 flex-col overflow-hidden">
          <header className="flex h-[58px] shrink-0 items-center justify-between border-b border-[#dfe3df] bg-white px-4 sm:px-6">
            <div className="flex min-w-0 items-center gap-2.5">
              <button
                type="button"
                aria-label={t('Menüyü aç', 'Open menu')}
                onClick={() => setMobileNavOpen(value => !value)}
                className="grid h-8 w-8 place-items-center rounded-lg border border-[#e1e5e1] text-[#596159] lg:hidden"
              >
                <Menu size={15} />
              </button>
              <div className="hidden h-7 w-7 place-items-center rounded-md bg-[#f0f2f0] text-[#435047] sm:grid">
                <SlidersHorizontal size={13} />
              </div>
              <span className="truncate text-[11px] font-medium text-[#475049]">{t('Sonraki servis', 'Next service')}</span>
              <ChevronRight size={12} className="hidden text-[#a0a6a1] sm:block" />
              <span className="hidden truncate text-[11px] font-medium text-[#475049] sm:block">{t('Öğle kararı', 'Lunch decision')}</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden items-center gap-2 text-[9px] text-[#697169] md:flex">
                <span className={`h-1.5 w-1.5 rounded-full ${food ? 'bg-[#15a34a]' : 'bg-[#c69035]'}`} />
                {food ? t('Veri güncel', 'Data updated') : t('Veri bekleniyor', 'Waiting for data')}
                {updatedAt ? <span>· {updatedAt.toLocaleTimeString(numberLocale, { hour: '2-digit', minute: '2-digit' })}</span> : null}
              </div>
              <button type="button" className="hidden h-8 items-center gap-2 rounded-lg border border-[#dfe3df] bg-white px-3 text-[10px] font-semibold text-[#2b332d] shadow-[0_1px_2px_rgba(14,22,17,0.03)] sm:flex">
                <Users size={13} /> {t('Jüri modu', 'Jury mode')}
              </button>
              <div className="grid h-8 w-8 place-items-center rounded-full bg-[#252a27] text-[10px] font-bold text-white">YK</div>
            </div>
          </header>

          {mobileNavOpen ? (
            <div className="absolute inset-x-3 top-[68px] z-30 rounded-xl border border-[#dce1dc] bg-[#071d18] p-2 text-white shadow-xl lg:hidden">
              <SidebarItem active icon={ClipboardCheck} label={t('Sonraki servis', 'Next service')} detail={t('Öğle · Bugün', 'Lunch · Today')} />
              <SidebarItem icon={Activity} label={t('Sinyaller', 'Signals')} />
              <SidebarItem icon={Database} label={t('Kanıt defteri', 'Evidence ledger')} />
              <SidebarItem icon={History} label={t('Karar geçmişi', 'Decision history')} />
            </div>
          ) : null}

          <main className="min-h-0 flex-1 overflow-y-auto">
            <div className="mx-auto w-full max-w-[1510px] px-4 py-5 sm:px-6 sm:py-6 xl:px-7">
              <section className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <h1 className="text-[26px] font-semibold leading-tight tracking-[-0.04em] text-[#121814] sm:text-[30px]">
                    {t('Sonraki öğle kararı', 'Next lunch decision')}
                  </h1>
                  <p className="mt-1.5 text-[11px] text-[#68716a] sm:text-[12px]">
                    {t('Bugün · Kuzey Kampüs · Ana Yemekhane', 'Today · North Campus · Main Dining Hall')}
                  </p>
                </div>
                <div className="flex items-center gap-3 sm:justify-end">
                  <ReadinessBadge readiness={readinessLabel} />
                  <div className="hidden border-l border-[#dde2dd] pl-3 text-right text-[8px] leading-4 text-[#727a73] sm:block">
                    <div>{t('Son güncelleme', 'Last updated')}</div>
                    <div className="font-medium text-[#384139]">{updatedAt ? updatedAt.toLocaleTimeString(numberLocale, { hour: '2-digit', minute: '2-digit' }) : '—'}</div>
                  </div>
                </div>
              </section>

              <section className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <MetricCard
                  icon={Users}
                  label={advisoryOnly ? t('Planlama adayı', 'Planning candidate') : t('Önerilen', 'Recommended')}
                  value={band ? band.recommendedTarget.toLocaleString(numberLocale) : '—'}
                  unit={t('öğün', 'meals')}
                  footer={band ? (advisoryOnly ? t('ADVISORY · mutfak emri değil', 'ADVISORY · not a kitchen order') : t('MODEL_ESTIMATE · ölçüm değil', 'MODEL_ESTIMATE · not measured')) : t('Karar bağlamı bekleniyor', 'Waiting for decision context')}
                />
                <MetricCard
                  icon={BarChart3}
                  label={t('Karar bandı', 'Decision band')}
                  value={band ? `${band.lowerBound.toLocaleString(numberLocale)} – ${band.upperBound.toLocaleString(numberLocale)}` : '—'}
                  footer={t('Belirsizlik bandı · operatör onayı gerekir', 'Uncertainty band · operator approval required')}
                />
                <MetricCard
                  icon={Gauge}
                  label={t('Sinyal kapsamı', 'Signal coverage')}
                  value={band ? `${band.signalCoveragePct}%` : '—'}
                  footer={signals.length ? `${healthySignals} / ${signals.length} ${t('girdi mevcut', 'inputs available')}` : t('Sinyaller bekleniyor', 'Signals pending')}
                  trend={band ? `+${band.signalCoveragePct} pp` : undefined}
                />
                <MetricCard
                  icon={Leaf}
                  label={t('Pilot başarı eşiği', 'Pilot success gate')}
                  value={`≥ ${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`}
                  footer={t('Ön kayıtlı hedef · gerçekleşmiş sonuç değil', 'Pre-registered target · not achieved result')}
                  trend={t('ölçülecek', 'to be measured')}
                />
              </section>

              <section className="mt-3 grid gap-3 xl:grid-cols-[minmax(0,1fr)_360px]">
                <div className="min-w-0 space-y-3">
                  <article className="rounded-xl border border-[#dfe3df] bg-white shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
                    <div className="flex flex-col gap-2 border-b border-[#e4e7e4] px-4 py-4 sm:flex-row sm:items-start sm:justify-between sm:px-5">
                      <div>
                        <div className="flex flex-wrap items-center gap-2">
                          <h2 className="text-[18px] font-semibold tracking-[-0.025em] text-[#151b17]">{advisoryOnly ? t('Planlama adayı', 'Planning candidate') : t('Üretim önerisi', 'Production recommendation')}</h2>
                          <span className="rounded-md bg-[#e6f5ee] px-2 py-1 text-[8px] font-semibold tracking-[0.04em] text-[#27654d]">MODEL_ESTIMATE</span>
                          <CircleHelp size={12} className="text-[#7d857f]" />
                        </div>
                        <p className="mt-1 max-w-2xl text-[10px] leading-4 text-[#667068]">
                          {t(
                            'Aktif karar sinyallerine dayanır. Belirsizlik model ve veri değişkenliğini yansıtır. Operatör onayı zorunludur; otomatik mutfak dispatch kapalıdır.',
                            'Based on active decision signals. Uncertainty reflects model and data variability. Operator approval is required; automatic kitchen dispatch is disabled.',
                          )}
                        </p>
                      </div>
                      <div className="text-[8px] font-medium text-[#778079]">{band?.provenance ?? 'MODEL_ESTIMATE'}</div>
                    </div>

                    <div className="px-4 py-5 sm:px-5">
                      {band ? (
                        <>
                          <div className="grid grid-cols-3 gap-3 text-center">
                            <BandValue label={t('Alt sınır', 'Lower bound')} value={band.lowerBound.toLocaleString(numberLocale)} note={formatDelta(band.lowerBound, band.recommendedTarget)} />
                            <BandValue label={t('Önerilen', 'Recommended')} value={band.recommendedTarget.toLocaleString(numberLocale)} emphasized />
                            <BandValue label={t('Üst sınır', 'Upper bound')} value={band.upperBound.toLocaleString(numberLocale)} note={formatDelta(band.upperBound, band.recommendedTarget)} />
                          </div>

                          <div className="relative mt-4 h-11">
                            <div className="absolute left-0 right-0 top-4 h-1.5 rounded-full bg-[#edf0ed]" />
                            <div className="absolute left-[18%] right-[18%] top-4 h-1.5 rounded-full bg-[#b7dfcd]" />
                            <div className="absolute left-[18%] top-2.5 h-4 w-px bg-[#426d5b]" />
                            <div className="absolute right-[18%] top-2.5 h-4 w-px bg-[#426d5b]" />
                            <div
                              className="absolute top-[10px] h-4 w-4 -translate-x-1/2 rounded-full border-2 border-white bg-[#064936] shadow-[0_0_0_1px_#064936]"
                              style={{ left: `${18 + targetPosition * 0.64}%` }}
                            />
                            <div className="absolute inset-x-0 top-7 flex justify-between font-mono text-[8px] text-[#7d857f]">
                              <span>{Math.max(0, band.lowerBound - 70).toLocaleString(numberLocale)}</span>
                              <span>{band.lowerBound.toLocaleString(numberLocale)}</span>
                              <span>{band.recommendedTarget.toLocaleString(numberLocale)}</span>
                              <span>{band.upperBound.toLocaleString(numberLocale)}</span>
                              <span>{(band.upperBound + 70).toLocaleString(numberLocale)}</span>
                            </div>
                          </div>

                          <div className="mt-4 border-t border-[#e7eae7] pt-4">
                            <div className="text-[10px] font-semibold text-[#222923]">{t('Ana sürücüler', 'Key drivers')} <span className="font-normal text-[#747d76]">({t('neden kodları', 'reason codes')})</span></div>
                            <div className="mt-3 grid gap-2 md:grid-cols-3">
                              {(band.reasonCodes.length ? band.reasonCodes : ['FULL_CONTEXT_AVAILABLE']).slice(0, 3).map((code, index) => (
                                <ReasonCode key={code} code={code} index={index} />
                              ))}
                            </div>
                          </div>
                        </>
                      ) : (
                        <div className="grid min-h-[190px] place-items-center rounded-lg border border-dashed border-[#d9ded9] bg-[#fafbfa] px-6 text-center">
                          <div>
                            <TriangleAlert size={20} className="mx-auto text-[#a9782f]" />
                            <div className="mt-3 text-[13px] font-semibold">{t('Karar bağlamı bekleniyor', 'Waiting for decision context')}</div>
                            <p className="mx-auto mt-1 max-w-md text-[9px] leading-4 text-[#707970]">{t('Sistem yeterli karar bağlamı olmadan üretim miktarı uydurmaz.', 'The system does not invent a production quantity without sufficient decision context.')}</p>
                          </div>
                        </div>
                      )}

                      <div className="mt-5 grid gap-2 sm:grid-cols-3">
                        <ActionButton
                          icon={CheckCircle2}
                          title={t('Pilot için onayla', 'Approve for pilot')}
                          detail={band ? `${band.recommendedTarget.toLocaleString(numberLocale)} ${t('öğün ile ilerle', 'meals')}` : t('Bağlam bekleniyor', 'Context pending')}
                          active={operatorDecision === 'PILOT_APPROVED'}
                          disabled={!canApprovePilot}
                          onClick={() => setOperatorDecision('PILOT_APPROVED')}
                          tone="approve"
                        />
                        <ActionButton
                          icon={Pencil}
                          title={t('Düzenleme iste', 'Request edit')}
                          detail={t('Miktarı ayarla veya not ekle', 'Adjust quantity or add note')}
                          active={operatorDecision === 'EDIT_REQUIRED'}
                          onClick={() => setOperatorDecision('EDIT_REQUIRED')}
                          tone="edit"
                        />
                        <ActionButton
                          icon={XCircle}
                          title={t('Beklet', 'Hold')}
                          detail={t('İlerleme · güvenli varsayılan', 'Do not proceed · safe default')}
                          active={operatorDecision === 'HOLD'}
                          onClick={() => setOperatorDecision('HOLD')}
                          tone="hold"
                        />
                      </div>
                    </div>
                  </article>

                  <article className="overflow-hidden rounded-xl border border-[#dfe3df] bg-white shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
                    <div className="flex items-center justify-between border-b border-[#e6e9e6] px-4 py-3 sm:px-5">
                      <h2 className="text-[14px] font-semibold tracking-[-0.015em] text-[#171e19]">
                        {t('Sinyal sağlığı', 'Signal health')} {signals.length ? `(${healthySignals} / ${signals.length} ${t('mevcut', 'available')})` : ''}
                      </h2>
                      <span className="flex items-center gap-1 text-[9px] font-medium text-[#2f6b51]">{t('Tüm sinyaller', 'View all signals')} <ArrowRight size={10} /></span>
                    </div>
                    <SignalTable signals={signals} t={t} />
                  </article>
                </div>

                <aside className="space-y-3">
                  <article className="rounded-xl border border-[#dfe3df] bg-white p-4 shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
                    <div className="flex items-center justify-between">
                      <h2 className="text-[14px] font-semibold tracking-[-0.02em]">{t('Kanıt defteri', 'Evidence ledger')}</h2>
                      <a href={FOOD_WASTE_SOURCE.url} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-[9px] font-medium text-[#2d6b50]">
                        {t('Tümünü gör', 'View all')} <ArrowRight size={10} />
                      </a>
                    </div>
                    <div className="mt-3 divide-y divide-[#e7eae7]">
                      <EvidenceRow icon={Database} label={t('2025 yemek atığı', '2025 food waste')} value={`${FOOD_WASTE_BASELINE.year2025WasteKg.toLocaleString(numberLocale)} kg`} provenance="OFFICIAL_PUBLIC" />
                      <EvidenceRow icon={Leaf} label={t('Geri kazanılan gıda', 'Recovered food')} value={`${FOOD_WASTE_BASELINE.year2025RecoveredKg.toLocaleString(numberLocale)} kg`} provenance="OFFICIAL_PUBLIC" />
                      <EvidenceRow icon={Building2} label={t('Yemekhane kapasitesi', 'Dining capacity')} value={`${FOOD_WASTE_BASELINE.diningHallCapacity.toLocaleString(numberLocale)} ${t('koltuk', 'seats')}`} provenance="OFFICIAL_SNAPSHOT" />
                    </div>
                  </article>

                  <article className="rounded-xl border border-[#dfe3df] bg-white p-4 shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
                    <div className="flex items-center justify-between gap-2">
                      <h2 className="text-[14px] font-semibold tracking-[-0.02em]">{t('Pilot sözleşmesi', 'Pilot contract')}</h2>
                      <span className="inline-flex items-center gap-1 rounded-md bg-[#e7f6dc] px-2 py-1 text-[8px] font-semibold text-[#37651d]"><span className="h-1.5 w-1.5 rounded-full bg-[#2f8c28]" /> {t('Ön kayıtlı', 'Pre-registered')}</span>
                    </div>
                    <div className="mt-4 grid grid-cols-3 divide-x divide-[#e5e8e5]">
                      <PilotMetric value={`${FOOD_WASTE_PILOT_PROTOCOL.durationDays} ${t('GÜN', 'DAYS')}`} label={t('Pilot süresi', 'Pilot duration')} />
                      <PilotMetric value={`≥ ${FOOD_WASTE_PILOT_PROTOCOL.successGate.targetWasteReductionPct}%`} label={t('Atık azaltma hedefi', 'Waste reduction target')} />
                      <PilotMetric value={`≥ ${FOOD_WASTE_PILOT_PROTOCOL.successGate.minimumMeasuredServicesPerArm}`} label={t('Kol başına servis', 'Services per arm')} />
                    </div>
                    <div className="mt-4 flex items-start gap-2 border-t border-[#e7eae7] pt-3 text-[9px] leading-4 text-[#5e685f]">
                      <BarChart3 size={13} className="mt-0.5 shrink-0 text-[#326047]" />
                      {t('Erken tükenme insidansında kontrol koluna göre artış olmamalı.', 'No increase in early-sellout incidence versus matched control.')}
                    </div>
                  </article>

                  <article className="rounded-xl border border-[#dfe3df] bg-white p-4 shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
                    <div className="flex items-center justify-between">
                      <h2 className="text-[14px] font-semibold tracking-[-0.02em]">{t('Karar zaman çizgisi', 'Decision timeline')}</h2>
                      <span className="flex items-center gap-1 text-[9px] font-medium text-[#2d6b50]">{t('Geçmiş', 'View history')} <ArrowRight size={10} /></span>
                    </div>
                    <div className="mt-4 space-y-0">
                      <TimelineRow done={Boolean(band)} time={updatedAt ? updatedAt.toLocaleTimeString(numberLocale, { hour: '2-digit', minute: '2-digit' }) : '—'} title={t('Sinyaller yakalandı', 'Signals captured')} detail={signals.length ? `${healthySignals} / ${signals.length} ${t('girdi mevcut', 'inputs available')}` : t('Bekleniyor', 'Pending')} />
                      <TimelineRow done={Boolean(band)} time={updatedAt ? updatedAt.toLocaleTimeString(numberLocale, { hour: '2-digit', minute: '2-digit' }) : '—'} title={t('Model çalışması tamamlandı', 'Model run completed')} detail={band ? `${band.recommendedTarget.toLocaleString(numberLocale)} · ${band.signalCoveragePct}%` : t('Bekleniyor', 'Pending')} />
                      <TimelineRow done={operatorDecision !== 'HOLD'} time={operatorDecision === 'HOLD' ? t('Bekliyor', 'Pending') : '—'} title={t('Operatör incelemesi', 'Operator review')} detail={operatorDecision === 'PILOT_APPROVED' ? t('Pilot onaylandı', 'Pilot approved') : operatorDecision === 'EDIT_REQUIRED' ? t('Düzenleme istendi', 'Edit requested') : t('İlerlemek için onay gerekli', 'Approval required to proceed')} />
                      <TimelineRow last done={false} time="—" title={t('Mutfak dispatch', 'Kitchen dispatch')} detail={t('Pilot boyunca otomatik dispatch kapalı', 'Automatic dispatch disabled during pilot')} />
                    </div>
                  </article>
                </aside>
              </section>

              <div className="h-6" />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

function SidebarItem({
  icon: Icon,
  label,
  detail,
  active = false,
  badge,
}: {
  icon: typeof Gauge;
  label: string;
  detail?: string;
  active?: boolean;
  badge?: string;
}) {
  return (
    <button
      type="button"
      className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left transition ${active ? 'bg-[#103d31] shadow-[inset_2px_0_0_#28c36a]' : 'text-white/75 hover:bg-white/[0.045] hover:text-white'}`}
    >
      <Icon size={16} className={active ? 'text-[#d6f6df]' : 'text-white/65'} />
      <span className="min-w-0 flex-1">
        <span className={`block truncate text-[11px] ${active ? 'font-semibold text-white' : 'font-medium'}`}>{label}</span>
        {detail ? <span className="mt-0.5 block truncate text-[9px] text-white/45">{detail}</span> : null}
      </span>
      {badge ? <span className="rounded bg-[#0e513c] px-1.5 py-0.5 text-[7px] font-semibold text-[#71df9d]">{badge}</span> : null}
    </button>
  );
}

function ReadinessBadge({ readiness }: { readiness: DecisionReadiness }) {
  const styles: Record<DecisionReadiness, string> = {
    PILOT_READY: 'border-[#cce8ae] bg-[#e8f8d9] text-[#285717]',
    REVIEW_REQUIRED: 'border-[#ead8a8] bg-[#fbf3d8] text-[#795923]',
    WITHHOLD: 'border-[#e5c7c4] bg-[#fae7e5] text-[#8b3f38]',
  };
  return (
    <div className={`inline-flex h-7 items-center gap-2 rounded-md border px-3 text-[9px] font-semibold tracking-[0.03em] ${styles[readiness]}`}>
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {readiness.replaceAll('_', ' ')}
    </div>
  );
}

function MetricCard({
  icon: Icon,
  label,
  value,
  unit,
  footer,
  trend,
}: {
  icon: typeof Gauge;
  label: string;
  value: string;
  unit?: string;
  footer: string;
  trend?: string;
}) {
  return (
    <article className="min-h-[132px] rounded-xl border border-[#dfe3df] bg-white p-4 shadow-[0_1px_2px_rgba(15,23,18,0.03)]">
      <div className="flex items-start justify-between gap-3">
        <div className="grid h-9 w-9 place-items-center rounded-lg bg-[#f0f3f1] text-[#1d4938]">
          <Icon size={17} />
        </div>
        <MiniBars />
      </div>
      <div className="mt-3 text-[9px] font-medium text-[#515b53]">{label}</div>
      <div className="mt-0.5 flex items-baseline gap-1.5">
        <span className="text-[23px] font-semibold tracking-[-0.035em] text-[#101612]">{value}</span>
        {unit ? <span className="text-[9px] font-semibold text-[#545e56]">{unit}</span> : null}
      </div>
      <div className="mt-2 flex items-center gap-2 text-[8px] leading-3.5 text-[#707970]">
        {trend ? <span className="font-semibold text-[#21854e]">{trend}</span> : null}
        <span>{footer}</span>
      </div>
    </article>
  );
}

function MiniBars() {
  return (
    <div className="flex h-8 items-end gap-[2px] opacity-45" aria-hidden="true">
      {[9, 15, 12, 20, 25, 18, 29].map((height, index) => (
        <span key={`${height}-${index}`} className="w-[2px] rounded-t bg-[#789589]" style={{ height }} />
      ))}
    </div>
  );
}

function BandValue({ label, value, note, emphasized = false }: { label: string; value: string; note?: string; emphasized?: boolean }) {
  return (
    <div>
      <div className={`text-[17px] font-semibold tracking-[-0.03em] ${emphasized ? 'text-[#0f5d41]' : 'text-[#151b17]'}`}>{value}</div>
      <div className={`mt-0.5 text-[9px] font-medium ${emphasized ? 'text-[#27684e]' : 'text-[#687169]'}`}>{label}</div>
      {note ? <div className="mt-0.5 text-[8px] text-[#7a827c]">{note}</div> : null}
    </div>
  );
}

function ReasonCode({ code, index }: { code: string; index: number }) {
  const Icon = index === 0 ? Activity : index === 1 ? Users : LineChart;
  return (
    <div className="rounded-lg bg-[#f6f7f6] px-3 py-2.5">
      <div className="flex items-center gap-2">
        <Icon size={12} className="text-[#36594a]" />
        <span className="truncate font-mono text-[8px] font-semibold text-[#2d3730]">{code}</span>
      </div>
    </div>
  );
}

function ActionButton({
  icon: Icon,
  title,
  detail,
  active,
  disabled,
  onClick,
  tone,
}: {
  icon: typeof CheckCircle2;
  title: string;
  detail: string;
  active: boolean;
  disabled?: boolean;
  onClick: () => void;
  tone: 'approve' | 'edit' | 'hold';
}) {
  const toneStyles = {
    approve: active ? 'border-[#0c4c38] bg-[#0a422f] text-white' : 'border-[#174d3b] bg-[#0e4634] text-white hover:bg-[#0a3c2d]',
    edit: active ? 'border-[#9ca59d] bg-[#eef1ee] text-[#151b17]' : 'border-[#d8ddd8] bg-white text-[#202721] hover:bg-[#f7f8f7]',
    hold: active ? 'border-[#efaaa4] bg-[#fff0ef] text-[#c6372f]' : 'border-[#f0c5c1] bg-[#fff9f8] text-[#c3463e] hover:bg-[#fff3f2]',
  }[tone];
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`flex min-h-[58px] items-center gap-3 rounded-lg border px-4 text-left transition disabled:cursor-not-allowed disabled:opacity-40 ${toneStyles}`}
    >
      <div className={`grid h-7 w-7 shrink-0 place-items-center rounded-full ${tone === 'approve' ? 'bg-white text-[#174d3b]' : tone === 'hold' ? 'bg-[#fee1de] text-[#cf3931]' : 'bg-[#eef1ee] text-[#234b3b]'}`}>
        <Icon size={14} />
      </div>
      <span className="min-w-0">
        <span className="block truncate text-[10px] font-semibold">{title}</span>
        <span className={`mt-0.5 block truncate text-[8px] ${tone === 'approve' ? 'text-white/70' : 'text-current/60'}`}>{detail}</span>
      </span>
    </button>
  );
}

function SignalTable({ signals, t }: { signals: SignalView[]; t: (tr: string, en: string) => string }) {
  if (!signals.length) {
    return <div className="px-5 py-8 text-center text-[9px] text-[#778078]">{t('Karar sinyalleri henüz yüklenmedi.', 'Decision signals have not loaded yet.')}</div>;
  }
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[680px] border-collapse text-left">
        <thead className="bg-[#f7f8f7] text-[8px] font-medium text-[#667068]">
          <tr>
            <th className="px-5 py-2 font-medium">{t('Sinyal', 'Signal')}</th>
            <th className="px-3 py-2 font-medium">{t('Durum', 'Status')}</th>
            <th className="px-3 py-2 font-medium">{t('Ağırlık', 'Weight')}</th>
            <th className="px-3 py-2 font-medium">{t('Kaynak', 'Source')}</th>
            <th className="px-3 py-2 font-medium">{t('Etkisi', 'Contribution')}</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#edf0ed] text-[9px] text-[#263029]">
          {signals.map(signal => {
            const Icon = signalIcon[signal.id];
            return (
              <tr key={signal.id} className="hover:bg-[#fafbfa]">
                <td className="px-5 py-2.5">
                  <div className="flex items-center gap-2"><Icon size={12} className="text-[#5e7065]" /> <span className="font-medium">{signal.label}</span></div>
                </td>
                <td className="px-3 py-2.5">
                  <span className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-[8px] font-medium ${signal.available ? 'bg-[#e6f5e6] text-[#2c7439]' : 'bg-[#fde8e6] text-[#b94740]'}`}>
                    <span className={`h-1.5 w-1.5 rounded-full ${signal.available ? 'bg-[#36a853]' : 'bg-[#df4d44]'}`} />
                    {signal.available ? t('Mevcut', 'Healthy') : t('Eksik', 'Unavailable')}
                  </span>
                </td>
                <td className="px-3 py-2.5 font-mono text-[#5e685f]">{signal.weightPct}%</td>
                <td className="px-3 py-2.5"><span className="rounded bg-[#eff1ef] px-1.5 py-1 font-mono text-[7px] text-[#646d66]">{signal.source}</span></td>
                <td className="px-3 py-2.5"><SignalSpark healthy={signal.available} /></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function SignalSpark({ healthy }: { healthy: boolean }) {
  const points = healthy ? '0,13 8,8 15,10 22,5 29,8 36,3 44,6 52,2' : '0,11 8,9 16,12 24,8 32,14 40,12 48,5 56,9';
  return (
    <svg width="58" height="18" viewBox="0 0 58 18" aria-hidden="true">
      <polyline points={points} fill="none" stroke={healthy ? '#3b9b56' : '#dc5047'} strokeWidth="1.4" />
    </svg>
  );
}

function EvidenceRow({ icon: Icon, label, value, provenance }: { icon: typeof Database; label: string; value: string; provenance: string }) {
  return (
    <div className="flex items-center gap-3 py-3">
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-[#f2f4f2] text-[#244e3c]"><Icon size={14} /></div>
      <div className="min-w-0 flex-1">
        <div className="truncate text-[9px] text-[#59635b]">{label}</div>
        <div className="mt-0.5 text-[13px] font-semibold tracking-[-0.02em] text-[#151c17]">{value}</div>
      </div>
      <span className="rounded bg-[#e5f1ed] px-1.5 py-1 font-mono text-[7px] text-[#285e49]">{provenance}</span>
    </div>
  );
}

function PilotMetric({ value, label }: { value: string; label: string }) {
  return (
    <div className="px-3 first:pl-0 last:pr-0">
      <div className="text-[11px] font-semibold text-[#182019]">{value}</div>
      <div className="mt-1 text-[8px] leading-3.5 text-[#6e776f]">{label}</div>
    </div>
  );
}

function TimelineRow({ done, time, title, detail, last = false }: { done: boolean; time: string; title: string; detail: string; last?: boolean }) {
  return (
    <div className="grid grid-cols-[14px_48px_minmax(0,1fr)] gap-2">
      <div className="relative flex justify-center">
        <span className={`mt-1 h-2.5 w-2.5 rounded-full border ${done ? 'border-[#249749] bg-[#249749]' : 'border-[#8f9891] bg-white'}`} />
        {!last ? <span className={`absolute bottom-[-3px] top-[13px] w-px ${done ? 'bg-[#4bb263]' : 'bg-[#d5dad5]'}`} /> : null}
      </div>
      <div className="pt-0.5 text-[8px] text-[#677068]">{time}</div>
      <div className="pb-3">
        <div className="text-[9px] font-semibold text-[#222a24]">{title}</div>
        <div className="mt-0.5 text-[8px] leading-3.5 text-[#747d75]">{detail}</div>
      </div>
    </div>
  );
}

function formatDelta(value: number, target: number) {
  const pct = ((value - target) / Math.max(1, target)) * 100;
  return `${pct >= 0 ? '+' : ''}${pct.toFixed(1)}%`;
}
