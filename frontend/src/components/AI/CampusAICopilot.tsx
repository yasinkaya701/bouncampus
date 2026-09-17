'use client';

import { useEffect, useRef, useState } from 'react';
import { ArrowUp, Bot, Database, RefreshCw, Sparkles, X } from 'lucide-react';
import { getDashboard, getMissionBrief } from '@/lib/api';
import type { DashboardData } from '@/lib/types';
import type { MissionBrief } from '@/lib/mission-types';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
}

const QUICK_PROMPTS = [
  'Why this mission?',
  'What is the weakest evidence?',
  'What should I verify before acting?',
  'Which values are actually live?',
];

function clock() {
  return new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
}

function fmt(value: number | null | undefined, suffix = '') {
  return value == null ? 'erişilemiyor' : `${value.toLocaleString('tr-TR')}${suffix}`;
}

export default function CampusAICopilot() {
  const [isOpen, setIsOpen] = useState(false);
  const [inputQuery, setInputQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [mission, setMission] = useState<MissionBrief | null>(null);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm-init',
      sender: 'bot',
      text: 'I explain why BOUNCAMPUS recommends a mission, which evidence supports it, where confidence is weak, and what a human must verify before acting. I never invent telemetry or dispatch a field command.',
      timestamp: clock(),
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen || dashboard || mission) return;
    Promise.all([getDashboard(), getMissionBrief()])
      .then(([nextDashboard, nextMission]) => {
        setDashboard(nextDashboard);
        setMission(nextMission);
      })
      .catch(() => {
        setDashboard(null);
        setMission(null);
      });
  }, [isOpen, dashboard, mission]);

  useEffect(() => {
    if (isOpen) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isOpen]);

  function answer(query: string): string {
    const lower = query.toLocaleLowerCase('tr-TR');
    const data = dashboard;

    if (!data || data.data_quality?.mode === 'DEGRADED') {
      return 'Dashboard inputs are partial or unavailable. I will not substitute old demo values. Check Data Trust or /api/v1/health before using any recommendation.';
    }

    if (lower.includes('why') || lower.includes('neden') || lower.includes('mission') || lower.includes('görev')) {
      if (!mission) return 'Mission Brief is not available right now.';
      return [
        `Mission: ${mission.recommendation}.`,
        `Why now: ${mission.why_now}`,
        `Confidence: ${mission.confidence}% (${mission.confidence_label}).`,
        `Human boundary: ${mission.guardrail}`,
      ].join('\n\n');
    }

    if (lower.includes('weak') || lower.includes('zayıf') || lower.includes('kanıt') || lower.includes('evidence')) {
      if (!mission) return 'Mission evidence is not available right now.';
      const weak = mission.evidence.filter(item => !item.source?.ok);
      if (weak.length) {
        return `Weakest evidence: ${weak.map(item => item.label).join(', ')}. These upstreams are unavailable, so confidence should be treated cautiously.`;
      }
      const snapshot = mission.evidence.find(item => item.source?.provenance === 'OFFICIAL_SNAPSHOT');
      return snapshot
        ? `All current source checks pass. The weakest freshness boundary is ${snapshot.label}: it is an official snapshot, not a live feed. Refreshing it after schedule changes would improve confidence.`
        : 'All current source checks pass. The next weakness is model calibration: occupancy, energy and food demand still need authorized operational telemetry for validation.';
    }

    if (lower.includes('verify') || lower.includes('doğrula') || lower.includes('before acting') || lower.includes('uygula')) {
      return [
        'Before acting, verify four things:',
        '1) the relevant source is healthy and current,',
        '2) the location is actually in the low/high-use condition the model predicts,',
        '3) the model assumption matches the day (weather, schedule, capacity),',
        '4) a responsible operator approves the pilot.',
        'BOUNCAMPUS stops at that human gate.',
      ].join('\n');
    }

    if (lower.includes('aksiyon') || lower.includes('action') || lower.includes('karar')) {
      const best = data.actions[0];
      return best
        ? `${best.title}. Modeled impact: ${fmt(best.impact_value)} ${best.impact_unit}. This is a decision candidate, not an automatic command. Open Jury Mode to inspect evidence and stress-test it.`
        : 'No recommendation currently exceeds the decision threshold.';
    }

    if (lower.includes('enerji') || lower.includes('energy') || lower.includes('tasarruf') || lower.includes('hvac')) {
      const best = data.actions.find(action => action.type === 'energy');
      return [
        `Today’s energy load is ${fmt(data.predicted_energy_mwh, ' MWh')} as a model estimate.`,
        best ? `Top energy candidate: ${best.title}. Modeled potential: ${fmt(best.impact_value)} ${best.impact_unit}.` : 'No energy candidate is above threshold.',
        'This is not BMS or meter telemetry; it is calculated from timetable demand, building profiles and outdoor weather.',
      ].join('\n\n');
    }

    if (lower.includes('yemek') || lower.includes('food') || lower.includes('porsiyon') || lower.includes('menü')) {
      return [
        `Official SKS menu item: ${data.live_menu?.main_dish ?? 'unavailable'}.`,
        `Lunch demand: ${fmt(data.food_demand_meals, ' portions')} as a model estimate, not POS sales.`,
        'The model uses class-release flow and weather. Anonymous time-bucketed POS totals would be the highest-value calibration input for a pilot.',
      ].join('\n\n');
    }

    if (lower.includes('dolu') || lower.includes('occupancy') || lower.includes('kütüphane') || lower.includes('masa')) {
      const pct = Math.round(data.campus_occupancy * 100);
      return [
        `Campus utilization is approximately ${pct}% in the current model window; it is not a live occupancy sensor reading.`,
        `Input: ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} BUIS/ÖBİKAS schedule records plus room-capacity assumptions.`,
        'Authorized anonymous Wi-Fi/AP, turnstile or room-sensor aggregates would convert this from schedule-derived demand into measured occupancy.',
      ].join('\n\n');
    }

    if (lower.includes('mekik') || lower.includes('ring') || lower.includes('otobüs') || lower.includes('servis') || lower.includes('shuttle')) {
      return [
        `Next published Güney → Kuzey departure: ${data.live_shuttle?.next_departure ?? 'unavailable'}.`,
        'This is official timetable data, not live vehicle GPS or passenger load.',
      ].join('\n\n');
    }

    if (lower.includes('kaynak') || lower.includes('canlı') || lower.includes('live') || lower.includes('gerçek') || lower.includes('source')) {
      const official = data.data_quality?.official_live_sources ?? 0;
      const external = data.data_quality?.external_live_sources ?? 0;
      return [
        `${official} official live Boğaziçi source(s) and ${external} external live source(s) are currently healthy.`,
        'Official live: SKS, Mekik, Academic Calendar. Official snapshot: BUIS/ÖBİKAS. External live: Open‑Meteo.',
        'Occupancy, energy, food demand, savings and CO₂ are always labeled model estimates.',
      ].join('\n\n');
    }

    return [
      mission ? `Current mission confidence: ${mission.confidence}% (${mission.confidence_label}).` : 'Mission Brief unavailable.',
      `Healthy official live sources: ${data.data_quality?.official_live_sources ?? 0}.`,
      `Schedule snapshot records: ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')}.`,
      'Ask me why the mission exists, which evidence is weakest, or what must be verified before acting.',
    ].join('\n\n');
  }

  function handleSend(textToSend?: string) {
    const query = (textToSend ?? inputQuery).trim();
    if (!query) return;

    setMessages(previous => [...previous, { id: `u-${Date.now()}`, sender: 'user', text: query, timestamp: clock() }]);
    setInputQuery('');
    setIsTyping(true);

    window.setTimeout(() => {
      setMessages(previous => [...previous, { id: `b-${Date.now()}`, sender: 'bot', text: answer(query), timestamp: clock() }]);
      setIsTyping(false);
    }, 180);
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setIsOpen(value => !value)}
        className="bc-focus-ring fixed bottom-5 right-4 z-50 flex items-center gap-2 rounded-full border border-white/10 bg-[#0b1226] px-3.5 py-3 text-white shadow-[0_18px_50px_rgba(11,18,38,0.25)] transition hover:-translate-y-0.5 hover:bg-[#111a32] sm:bottom-6 sm:right-6 sm:px-4"
        title="Open BOUNCAMPUS Decision Explainer"
      >
        <span className="relative grid h-5 w-5 place-items-center">
          <span className="absolute h-2.5 w-2.5 animate-ping rounded-full bg-blue-400/40" />
          <Sparkles size={16} className="relative text-blue-300" />
        </span>
        <span className="hidden text-[11px] font-black tracking-[-0.01em] sm:inline">Explain this decision</span>
      </button>

      {isOpen && (
        <div className="fixed bottom-20 right-3 z-50 flex h-[min(680px,82vh)] w-[calc(100vw-24px)] flex-col overflow-hidden rounded-[28px] border border-slate-950/10 bg-[#f7f8f5] shadow-[0_28px_90px_rgba(11,18,38,0.28)] sm:bottom-24 sm:right-6 sm:w-[430px]">
          <div className="border-b border-white/10 bg-[#0b1226] px-5 pb-4 pt-5 text-white">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3">
                <div className="grid h-10 w-10 place-items-center rounded-[14px] border border-white/10 bg-white/5">
                  <Bot size={17} className="text-blue-300" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-black tracking-[-0.02em]">Decision Explainer</h3>
                    <span className="rounded-full border border-violet-400/20 bg-violet-400/10 px-2 py-0.5 font-mono text-[8px] font-black text-violet-200">MISSION AWARE</span>
                  </div>
                  <p className="mt-1 text-[10px] leading-relaxed text-slate-400">Evidence, confidence, assumptions and human guardrails.</p>
                </div>
              </div>
              <button type="button" onClick={() => setIsOpen(false)} className="bc-focus-ring rounded-xl p-2 text-slate-500 transition hover:bg-white/5 hover:text-white"><X size={16} /></button>
            </div>

            <div className="mt-4 flex items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/[0.04] px-3 py-2 font-mono text-[9px] text-slate-400">
              <span className="flex items-center gap-2"><Database size={10} className={dashboard?.data_quality?.mode === 'LIVE_PUBLIC_DATA' ? 'text-emerald-300' : 'text-amber-300'} />{dashboard?.data_quality?.mode === 'LIVE_PUBLIC_DATA' ? 'PUBLIC SOURCES ONLINE' : 'CHECKING SOURCES'}</span>
              {mission && <span className="font-black text-blue-300">{mission.confidence}% CONF.</span>}
            </div>
          </div>

          <div className="flex-1 space-y-4 overflow-y-auto p-4 sm:p-5">
            {messages.map(message => (
              <div key={message.id} className={`flex flex-col ${message.sender === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-[88%] whitespace-pre-line rounded-[18px] px-3.5 py-3 text-[11px] leading-relaxed ${message.sender === 'user' ? 'rounded-br-[5px] bg-[#0b1226] text-white' : 'rounded-bl-[5px] border border-slate-950/10 bg-white text-slate-700 shadow-sm'}`}>
                  {message.text}
                </div>
                <span className="mt-1 px-1 font-mono text-[8px] text-slate-400">{message.timestamp}</span>
              </div>
            ))}
            {isTyping && (
              <div className="flex items-center gap-2 px-2 text-[10px] font-semibold text-slate-400">
                <RefreshCw size={11} className="animate-spin text-blue-500" /> checking mission evidence and provenance
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="border-t border-slate-950/8 bg-white/70 px-3 pb-2 pt-3">
            <div className="flex gap-1.5 overflow-x-auto pb-2">
              {QUICK_PROMPTS.map(prompt => (
                <button key={prompt} type="button" onClick={() => handleSend(prompt)} className="bc-focus-ring whitespace-nowrap rounded-full border border-slate-950/10 bg-[#f4f5f2] px-2.5 py-1.5 text-[9px] font-bold text-slate-600 transition hover:bg-white hover:text-slate-900">
                  {prompt}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-2 rounded-[17px] border border-slate-950/10 bg-white p-1.5 shadow-sm">
              <input
                type="text"
                value={inputQuery}
                onChange={event => setInputQuery(event.target.value)}
                onKeyDown={event => event.key === 'Enter' && handleSend()}
                placeholder="Ask why, confidence, evidence, or guardrails…"
                className="min-w-0 flex-1 bg-transparent px-2 py-2 text-[11px] text-slate-800 outline-none placeholder:text-slate-400"
              />
              <button type="button" onClick={() => handleSend()} className="bc-focus-ring grid h-9 w-9 shrink-0 place-items-center rounded-[12px] bg-[#2f5cff] text-white transition hover:bg-blue-700">
                <ArrowUp size={14} />
              </button>
            </div>
            <p className="px-2 pb-1 pt-2 text-center font-mono text-[8px] text-slate-400">MISSION EVIDENCE · NO FIELD COMMANDS</p>
          </div>
        </div>
      )}
    </>
  );
}
