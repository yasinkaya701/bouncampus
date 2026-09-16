'use client';

import { useEffect, useRef, useState } from 'react';
import { ArrowUp, Bot, Database, RefreshCw, Sparkles, X } from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
}

const QUICK_PROMPTS = [
  'Bugünün en güçlü aksiyonu?',
  'Doluluk gerçekten canlı mı?',
  'Yemekhane tahmini neye dayanıyor?',
  'Mekik verisi ne kadar gerçek zamanlı?',
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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm-init',
      sender: 'bot',
      text: 'Ben BOUNCAMPUS karar destek copilot’uyum. Public kaynakları model tahminlerinden ayırırım; bağlı olmayan BMS, POS, sensör veya GPS verisini varmış gibi göstermem.',
      timestamp: clock(),
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen || dashboard) return;
    getDashboard().then(setDashboard).catch(() => setDashboard(null));
  }, [isOpen, dashboard]);

  useEffect(() => {
    if (isOpen) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isOpen]);

  function answer(query: string): string {
    const lower = query.toLocaleLowerCase('tr-TR');
    const data = dashboard;

    if (!data || data.data_quality?.mode === 'DEGRADED') {
      return 'Canlı dashboard kaynağı şu anda kısmi veya erişilemiyor. Eski demo değerlerini canlı veri gibi kullanmayacağım. Kaynak durumunu /api/v1/health üzerinden kontrol edebilirsin.';
    }

    if (lower.includes('aksiyon')) {
      const best = data.actions[0];
      return best
        ? `${best.title}. Model etkisi: ${fmt(best.impact_value)} ${best.impact_unit}. Bu bir karar adayıdır; sahada uygulanmadan önce operasyon/BMS doğrulaması gerekir.`
        : 'Şu anda model eşik değerini geçen bir aksiyon adayı yok.';
    }

    if (lower.includes('enerji') || lower.includes('tasarruf') || lower.includes('hvac')) {
      const best = data.actions.find(action => action.type === 'energy');
      return [
        `Bugünkü enerji yükü ${fmt(data.predicted_energy_mwh, ' MWh')} olarak model tahmini.`,
        best ? `Öne çıkan enerji adayı: ${best.title}. Hesaplanan etki ${fmt(best.impact_value)} ${best.impact_unit}.` : 'Şu anda enerji aksiyonu üretilemedi.',
        'Bu değer BMS veya sayaç telemetrisi değildir; ders programı snapshot’ı, bina profili ve dış hava girdisinden hesaplanır.',
      ].join('\n\n');
    }

    if (lower.includes('yemek') || lower.includes('porsiyon') || lower.includes('menü')) {
      return [
        `Resmî SKS sayfasından ayrıştırılan ana yemek: ${data.live_menu?.main_dish ?? 'alan ayrıştırılamadı'}.`,
        `Öğle talebi ${fmt(data.food_demand_meals, ' porsiyon')} ve bu sayı model tahmini; POS satışı değildir.`,
        'Talep modeli ders çıkış akışı ve hava koşullarını kullanıyor. Pilot için en değerli sonraki entegrasyon anonim zaman-dilimli POS toplamları olur.',
      ].join('\n\n');
    }

    if (lower.includes('dolu') || lower.includes('occupancy') || lower.includes('kütüphane') || lower.includes('masa')) {
      const pct = Math.round(data.campus_occupancy * 100);
      return [
        `Gösterilen kampüs kullanım oranı yaklaşık %${pct}; bu canlı sensör ölçümü değil.`,
        `Kaynak: ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} derslik BUIS/ÖBİKAS schedule snapshot’ı ve oda kapasitesi varsayımları.`,
        'Gerçek zamanlı doluluk için izinli anonim Wi‑Fi/AP, turnike veya oda sensörü agregaları gerekir.',
      ].join('\n\n');
    }

    if (lower.includes('mekik') || lower.includes('ring') || lower.includes('otobüs') || lower.includes('servis')) {
      return [
        `Mekik Bilgi Sistemi’nden ayrıştırılan bir sonraki Güney → Kuzey hareketi: ${data.live_shuttle?.next_departure ?? 'şu anda ayrıştırılamadı'}.`,
        'Bu resmî tarife verisidir; araç GPS konumu veya anlık yolcu sayısı değildir.',
      ].join('\n\n');
    }

    if (lower.includes('kaynak') || lower.includes('canlı') || lower.includes('gerçek')) {
      const official = data.data_quality?.official_live_sources ?? 0;
      const external = data.data_quality?.external_live_sources ?? 0;
      return [
        `${official} resmî canlı Boğaziçi kaynağı ve ${external} haricî canlı kaynak şu anda sağlıklı görünüyor.`,
        'Resmî canlı: SKS, Mekik, Akademik Takvim. Resmî snapshot: BUIS/ÖBİKAS. Haricî canlı: Open‑Meteo.',
        'Doluluk, enerji, yemek talebi, tasarruf ve CO₂ model tahmini olarak etiketlenir.',
      ].join('\n\n');
    }

    return [
      `Aktif resmî canlı kaynak sayısı: ${data.data_quality?.official_live_sources ?? 0}.`,
      `Ders snapshot’ında ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} kayıt var.`,
      'Bir sonucu canlı sensör verisi olarak adlandırmadan önce provenance katmanındaki kaynağı kontrol ederim.',
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
    }, 220);
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setIsOpen(value => !value)}
        className="bc-focus-ring fixed bottom-5 right-4 z-50 flex items-center gap-2 rounded-full border border-white/10 bg-[#0b1226] px-3.5 py-3 text-white shadow-[0_18px_50px_rgba(11,18,38,0.25)] transition hover:-translate-y-0.5 hover:bg-[#111a32] sm:bottom-6 sm:right-6 sm:px-4"
        title="Open BOUNCAMPUS Copilot"
      >
        <span className="relative grid h-5 w-5 place-items-center">
          <span className="absolute h-2.5 w-2.5 animate-ping rounded-full bg-blue-400/40" />
          <Sparkles size={16} className="relative text-blue-300" />
        </span>
        <span className="hidden text-[11px] font-black tracking-[-0.01em] sm:inline">Ask BOUNCAMPUS</span>
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
                    <h3 className="text-sm font-black tracking-[-0.02em]">Campus Copilot</h3>
                    <span className="rounded-full border border-violet-400/20 bg-violet-400/10 px-2 py-0.5 font-mono text-[8px] font-black text-violet-200">DECISION SUPPORT</span>
                  </div>
                  <p className="mt-1 text-[10px] leading-relaxed text-slate-400">Source-aware answers. No autonomous field dispatch.</p>
                </div>
              </div>
              <button type="button" onClick={() => setIsOpen(false)} className="bc-focus-ring rounded-xl p-2 text-slate-500 transition hover:bg-white/5 hover:text-white"><X size={16} /></button>
            </div>

            <div className="mt-4 flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.04] px-3 py-2 font-mono text-[9px] text-slate-400">
              <Database size={10} className={dashboard?.data_quality?.mode === 'LIVE_WITH_MODELS' ? 'text-emerald-300' : 'text-amber-300'} />
              {dashboard?.data_quality?.mode === 'LIVE_WITH_MODELS' ? 'PUBLIC SOURCES ONLINE · MODELS LABELED' : 'CHECKING SOURCE HEALTH'}
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
                <RefreshCw size={11} className="animate-spin text-blue-500" /> checking provenance and model outputs
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
                placeholder="Ask about sources, demand or decisions…"
                className="min-w-0 flex-1 bg-transparent px-2 py-2 text-[11px] text-slate-800 outline-none placeholder:text-slate-400"
              />
              <button type="button" onClick={() => handleSend()} className="bc-focus-ring grid h-9 w-9 shrink-0 place-items-center rounded-[12px] bg-[#2f5cff] text-white transition hover:bg-blue-700">
                <ArrowUp size={14} />
              </button>
            </div>
            <p className="px-2 pb-1 pt-2 text-center font-mono text-[8px] text-slate-400">PROVENANCE FIRST · NO FIELD COMMANDS</p>
          </div>
        </div>
      )}
    </>
  );
}
