'use client';

import { useEffect, useRef, useState } from 'react';
import { Bot, Database, RefreshCw, Send, Sparkles, X } from 'lucide-react';
import { getDashboard } from '@/lib/api';
import type { DashboardData } from '@/lib/types';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
}

const QUICK_PROMPTS = [
  'Enerji için bugün hangi aksiyon daha güçlü?',
  'Yemekhane talebi neye dayanıyor?',
  'Kampüs doluluğu gerçekten canlı mı?',
  'Mekik verisinde ne biliyoruz?',
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
      text: 'BOUNCAMPUS karar destek asistanıyım. Resmî/public kaynakları model tahminlerinden ayırırım; bağlı olmayan BMS, POS, sensör veya GPS verisini varmış gibi göstermem.',
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
      return 'Canlı dashboard kaynağı şu anda kısmi veya erişilemiyor. Eski demo değerlerini canlı veri gibi kullanmayacağım. `/api/v1/health` üzerinden kaynak durumunu kontrol edebilirsin.';
    }

    if (lower.includes('enerji') || lower.includes('tasarruf') || lower.includes('hvac')) {
      const best = data.actions.find(action => action.type === 'energy');
      return [
        `Bugünkü enerji yükü ${fmt(data.predicted_energy_mwh, ' MWh')} olarak **model tahmini**.` ,
        best ? `En yüksek öncelikli öneri: ${best.title}. Hesaplanan etki: ${fmt(best.impact_value)} ${best.impact_unit}.` : 'Şu anda enerji aksiyonu üretilemedi.',
        'Bu değer BMS/sayaç telemetrisi değildir; ders programı snapshot’ı, bina profili ve dış hava girdisinden hesaplanır. Sahaya komut göndermiyorum.',
      ].join('\n\n');
    }

    if (lower.includes('yemek') || lower.includes('porsiyon') || lower.includes('menü')) {
      return [
        `Resmî SKS sayfasından ayrıştırılan ana yemek: ${data.live_menu?.main_dish ?? 'alan ayrıştırılamadı'}.`,
        `Öğle talebi ${fmt(data.food_demand_meals, ' porsiyon')} ve bu sayı **model tahmini**; POS satışı değildir. Model ders çıkış akışı ile hava koşulunu kullanır.`,
        'Hackathon pilotunda en değerli sonraki entegrasyon, anonim 15 dakikalık SKS POS toplamlarıyla bu modeli kalibre etmektir.',
      ].join('\n\n');
    }

    if (lower.includes('dolu') || lower.includes('occupancy') || lower.includes('kütüphane') || lower.includes('masa')) {
      const pct = Math.round(data.campus_occupancy * 100);
      return [
        `Gösterilen kampüs kullanım oranı yaklaşık %${pct} ve **canlı sensör ölçümü değildir**.`,
        `Kaynak: ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} derslik BUIS/ÖBİKAS public schedule snapshot’ı + oda kapasitesi varsayımları.`,
        'Gerçek zamanlı doluluk için üniversite izniyle anonim Wi‑Fi/AP, turnike veya oda sensörü agregaları gerekir.',
      ].join('\n\n');
    }

    if (lower.includes('mekik') || lower.includes('ring') || lower.includes('otobüs') || lower.includes('servis')) {
      return [
        `Mekik Bilgi Sistemi’nden ayrıştırılan bir sonraki Güney → Kuzey hareketi: ${data.live_shuttle?.next_departure ?? 'şu anda ayrıştırılamadı'}.`,
        'Bu **resmî tarife verisidir**, araç GPS konumu veya anlık yolcu sayısı değildir.',
        'Yoğunluk/frekans optimizasyonu ancak talep verisiyle model tahmini olarak yapılabilir; uygulama otomatik olarak filoya komut göndermez.',
      ].join('\n\n');
    }

    if (lower.includes('kaynak') || lower.includes('canlı') || lower.includes('gerçek')) {
      const official = data.data_quality?.official_live_sources ?? 0;
      const external = data.data_quality?.external_live_sources ?? 0;
      return [
        `Şu anda ${official} resmî canlı Boğaziçi kaynağı ve ${external} haricî canlı kaynak sağlıklı görünüyor.`,
        'Resmî canlı: SKS menü, Mekik, Akademik Takvim. Resmî snapshot: BUIS/ÖBİKAS ders programı. Haricî canlı: Open‑Meteo.',
        'Doluluk, enerji, yemek talebi, tasarruf ve CO₂ ise açıkça MODEL TAHMİNİ olarak etiketlenir.',
      ].join('\n\n');
    }

    return [
      'Bu soruyu mevcut veri sözleşmesine göre yanıtlayabilirim.',
      `Aktif resmî canlı kaynak sayısı: ${data.data_quality?.official_live_sources ?? 0}. Ders snapshot’ında ${(data.real_courses_loaded ?? 0).toLocaleString('tr-TR')} kayıt var.`,
      'Bir sonucu “canlı sensör verisi” olarak adlandırmadan önce provenance panelindeki kaynağı kontrol ederim.',
    ].join('\n\n');
  }

  function handleSend(textToSend?: string) {
    const query = (textToSend ?? inputQuery).trim();
    if (!query) return;

    setMessages(prev => [...prev, { id: `u-${Date.now()}`, sender: 'user', text: query, timestamp: clock() }]);
    setInputQuery('');
    setIsTyping(true);

    window.setTimeout(() => {
      setMessages(prev => [...prev, { id: `b-${Date.now()}`, sender: 'bot', text: answer(query), timestamp: clock() }]);
      setIsTyping(false);
    }, 250);
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-4 py-3 rounded-full shadow-2xl hover:bg-slate-800 active:scale-95 transition flex items-center gap-2 border border-slate-700"
        title="BOUNCAMPUS karar destek asistanını aç"
      >
        <Sparkles size={18} className="text-emerald-400" />
        <span className="font-bold text-xs hidden sm:inline">Model Copilot</span>
      </button>

      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-[92vw] sm:w-[420px] h-[580px] max-h-[82vh] bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden">
          <div className="bg-slate-900 text-white px-4 py-3.5 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="bg-slate-800 p-2 rounded-xl border border-slate-700"><Bot size={19} className="text-emerald-400" /></div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-bold text-sm">BOUNCAMPUS Model Copilot</h3>
                  <span className="text-[9px] bg-violet-950 text-violet-300 px-2 py-0.5 rounded font-mono border border-violet-800">KARAR DESTEK</span>
                </div>
                <p className="text-[10px] text-slate-400 mt-0.5">Kaynak doğrulamalı · sahaya komut göndermez</p>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white p-1.5"><X size={18} /></button>
          </div>

          <div className="px-4 py-2 bg-slate-50 border-b border-slate-200 flex items-center gap-2 text-[10px] text-slate-600 font-mono">
            <Database size={12} />
            <span>{dashboard?.data_quality?.mode === 'LIVE_WITH_MODELS' ? 'Canlı kaynaklar + açık model tahminleri' : 'Kaynak durumu kontrol ediliyor / degraded'}</span>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50/50">
            {messages.map(msg => (
              <div key={msg.id} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-[88%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed whitespace-pre-line ${msg.sender === 'user' ? 'bg-slate-900 text-white rounded-br-sm' : 'bg-white border border-slate-200 text-slate-800 rounded-bl-sm'}`}>
                  {msg.text}
                </div>
                <span className="text-[9px] text-slate-400 mt-1 px-1">{msg.timestamp}</span>
              </div>
            ))}
            {isTyping && (
              <div className="flex items-center gap-2 text-slate-400 text-xs pl-2">
                <RefreshCw size={12} className="animate-spin text-emerald-600" />
                <span>Kaynak ve model ayrımı kontrol ediliyor...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="px-3 py-2 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            {QUICK_PROMPTS.map(prompt => (
              <button key={prompt} onClick={() => handleSend(prompt)} className="whitespace-nowrap px-2.5 py-1 rounded-full text-[10px] font-medium bg-slate-100 hover:bg-emerald-50 text-slate-700 border border-slate-200">
                {prompt}
              </button>
            ))}
          </div>

          <div className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input
              type="text"
              value={inputQuery}
              onChange={event => setInputQuery(event.target.value)}
              onKeyDown={event => event.key === 'Enter' && handleSend()}
              placeholder="Veri, enerji, yemekhane, doluluk veya mekik sor..."
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs outline-none focus:border-slate-400"
            />
            <button onClick={() => handleSend()} className="bg-slate-900 hover:bg-slate-800 text-white p-2.5 rounded-xl"><Send size={15} /></button>
          </div>
        </div>
      )}
    </>
  );
}
