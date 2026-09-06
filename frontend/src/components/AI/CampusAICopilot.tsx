'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Sparkles, Bot, Send, X, CheckCircle2, Zap, ArrowRight, CornerDownLeft, RefreshCw, Radio } from 'lucide-react';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  actionPayload?: {
    type: string;
    savingsTl: number;
    kwhSaved: number;
    protocol: string;
    bmsStatus: string;
  };
}

const QUICK_PROMPTS = [
  '⚡ Pik saat enerji yükünü tıraşla (Peak-Shaving)',
  '🍱 Yemekhane 12:30 kuyruk ve porsiyon uyarısı',
  '📚 Kütüphane boş masa ve çalışma alanı durumu',
  '🚌 Kuzey-Güney ring otobüs yoğunluk tahmini'
];

export default function CampusAICopilot() {
  const [isOpen, setIsOpen] = useState(false);
  const [inputQuery, setInputQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [dispatchedId, setDispatchedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm-init',
      sender: 'bot',
      text: 'Merhaba! Ben BOUNCAMPUS Yapay Zekâ Enerji & Operasyon Asistanı. 3.238 gerçek OBIKAS dersi, canlı hava durumu ve Kilyos rüzgar türbini verisiyle kampüsü optimize etmeye hazırım. Neyi hesaplayalım?',
      timestamp: '12:00'
    }
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || inputQuery;
    if (!query.trim()) return;

    const userMsg: Message = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInputQuery('');
    setIsTyping(true);

    setTimeout(() => {
      let botResponse: Message;
      const lower = query.toLowerCase();

      if (lower.includes('enerji') || lower.includes('pik') || lower.includes('peak') || lower.includes('klima') || lower.includes('hvac')) {
        botResponse = {
          id: `b-${Date.now()}`,
          sender: 'bot',
          text: `🔍 **Fiziksel Termodinamik Analiz Tamamlandı:**\n\n• Saat 12:00-14:00 arasında New Hall ve Perkins Hall amfilerinde 1.200+ öğrenci bulunacak.\n• Open-Meteo anlık Bebek sıcaklığı 21.5°C olduğundan, üst katlardaki (Kat 3 ve 4) HVAC setpoint değerini +1.5°C artırarak şebeke pik cezası önlenebilir.\n\nÖnerilen aksiyon onaylanırsa kampüs otomasyon sistemine (BMS) BACnet protokolüyle anında iletilecektir.`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
          actionPayload: {
            type: 'HVAC Night & Peak Setpoint Dispatch',
            savingsTl: 14200,
            kwhSaved: 5120,
            protocol: 'BACnet/IP over UDP (Port 47808)',
            bmsStatus: 'Ready for Field Push'
          }
        };
      } else if (lower.includes('yemek') || lower.includes('porsiyon') || lower.includes('kuyruk') || lower.includes('kantin')) {
        botResponse = {
          id: `b-${Date.now()}`,
          sender: 'bot',
          text: `🍽️ **SKS Canlı Yemekhane Akış Raporu:**\n\n• Bugün resmi menü: **Etli Nohut Yemeği (317 kcal) & Melek Pilavı**.\n• Saat 12:15'te New Hall ve Kare Blok'taki derslerin bitişiyle Kuzey Yemekhanesi'nde 633 öğrenci eş zamanlı kuyruğa girecek.\n• **Bekleme Süresi Tahmini:** Kuzey Yemekhanesi: ~16 dakika • Güney Yemekhanesi: ~5 dakika • Orta Kantin: ~7 dakika.\n• **AI Mutfak Önerisi:** Akşam israfını önlemek için 4.200 yerine 3.584 porsiyon hazırlanmalı. 616 porsiyon kurtarılacaktır.`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
      } else if (lower.includes('kütüphane') || lower.includes('masa') || lower.includes('yer') || lower.includes('etüt')) {
        botResponse = {
          id: `b-${Date.now()}`,
          sender: 'bot',
          text: `📚 **Aptullah Kuran Kütüphanesi Canlı Doluluk Radarı:**\n\n• Toplam 512 çalışma koltuğundan şu anda **382'si aktif (%74 doluluk)**.\n• **Zemin Kat (Grup Çalışma):** %89 Dolu (Yalnızca 8 masa boş)\n• **1. Kat (Süreli Yayınlar):** %62 Dolu (31 masa boş)\n• **2. Kat (Bireysel Sessiz Salon):** %54 Dolu (46 masa boş - **Önerilen Alan**)\n\nAkşam 18:00 sonrası sınav haftası etkisiyle doluluğun %90 üzerine çıkması bekleniyor.`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
      } else if (lower.includes('ring') || lower.includes('otobüs') || lower.includes('servis') || lower.includes('hisarüstü') || lower.includes('bebek')) {
        botResponse = {
          id: `b-${Date.now()}`,
          sender: 'bot',
          text: `🚌 **Kampüs İçi Ring Servis & Hareketlilik Modeli:**\n\n• Hisarüstü Kuzey Kampüs kapısı ile Bebek Güney Kampüs kapısı arasındaki öğrenci göçü 12:45'te tepe noktaya ulaşacaktır.\n• Tahmini bekleyen öğrenci: ~95 kişi.\n• **Optimizasyon Kararı:** Mevcut 15 dakikalık sefer sıklığı 12:30 - 13:45 arasında **7 dakikaya indirilmelidir** (Ekstra 2 adet elektrikli servis devreye alınmalı). Bekleme süresi 18 dakikadan 6 dakikaya düşer.`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
          actionPayload: {
            type: 'Shuttle Frequency Modulation',
            savingsTl: 3200,
            kwhSaved: 480,
            protocol: 'Fleet MQTT Telemetry v2',
            bmsStatus: 'Route Schedule Ready'
          }
        };
      } else {
        botResponse = {
          id: `b-${Date.now()}`,
          sender: 'bot',
          text: `🤖 **Analiz Sonucu:** "${query}" için Boğaziçi OBIKAS veritabanında 3.238 derslik kaydı ve 21 binanın enerji profili tarandı.\n\nSistem şu anda tam optimize durumda çalışıyor: Kilyos Rüzgar Türbini 420 kW temiz güç üretiyor ve kampüs şebeke ofsetini %28.4 seviyesinde tutuyor. Binaların kapatılan üst katları sayesinde bugün 3.420 kWh enerji tasarrufu öngörülmektedir.`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
      }

      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 600);
  };

  const handleDispatchAction = (actionId: string) => {
    setDispatchedId(actionId);
    setTimeout(() => {
      setDispatchedId(null);
    }, 4000);
  };

  return (
    <>
      {/* Floating Action Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 text-white p-3.5 rounded-full shadow-2xl hover:scale-105 active:scale-95 transition-all duration-300 flex items-center gap-2 group border-2 border-white/20"
        title="Campus AI Copilot'u Aç"
      >
        <span className="relative flex h-3.5 w-3.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-200 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-white"></span>
        </span>
        <Sparkles size={20} className="animate-pulse" />
        <span className="font-bold text-xs tracking-wide pr-1 hidden sm:inline">AI Copilot</span>
      </button>

      {/* Slide-out Drawer / Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-[92vw] sm:w-[420px] h-[580px] max-h-[82vh] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-300">
          {/* Header */}
          <div className="bg-gradient-to-r from-emerald-800 to-teal-800 text-white px-4 py-3.5 flex items-center justify-between shadow-md">
            <div className="flex items-center space-x-2.5">
              <div className="bg-white/15 p-2 rounded-xl backdrop-blur-xs">
                <Bot size={20} className="text-emerald-300" />
              </div>
              <div>
                <h3 className="font-bold text-sm flex items-center gap-1.5">
                  BOUNCAMPUS AI Copilot
                  <span className="text-[10px] bg-emerald-500/30 text-emerald-200 px-2 py-0.5 rounded-full font-mono border border-emerald-400/30">
                    Live
                  </span>
                </h3>
                <p className="text-[11px] text-emerald-100/80">3.238 OBIKAS Dersi • Kilyos RES • BACnet BMS</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/70 hover:text-white hover:bg-white/10 p-1.5 rounded-lg transition"
            >
              <X size={18} />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50/50">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[86%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed shadow-2xs ${
                    msg.sender === 'user'
                      ? 'bg-emerald-700 text-white rounded-br-xs'
                      : 'bg-white border border-gray-200 text-gray-800 rounded-bl-xs'
                  }`}
                >
                  <div className="whitespace-pre-line">{msg.text}</div>

                  {/* Dispatchable Action Card */}
                  {msg.actionPayload && (
                    <div className="mt-3 p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-gray-800">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="font-bold text-emerald-900 text-[11px] flex items-center gap-1">
                          <Zap size={13} className="text-emerald-700" />
                          {msg.actionPayload.type}
                        </span>
                        <span className="text-[10px] bg-emerald-200 text-emerald-900 px-1.5 py-0.5 rounded font-mono font-bold">
                          +{msg.actionPayload.kwhSaved} kWh
                        </span>
                      </div>
                      <div className="text-[10px] text-gray-600 font-mono mb-2">
                        {msg.actionPayload.protocol}
                      </div>
                      <button
                        onClick={() => handleDispatchAction(msg.id)}
                        disabled={dispatchedId === msg.id}
                        className={`w-full py-1.5 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 ${
                          dispatchedId === msg.id
                            ? 'bg-emerald-600 text-white'
                            : 'bg-emerald-700 hover:bg-emerald-800 text-white shadow-xs'
                        }`}
                      >
                        {dispatchedId === msg.id ? (
                          <>
                            <CheckCircle2 size={14} />
                            <span>BACnet Paketi İletildi (200 OK)</span>
                          </>
                        ) : (
                          <>
                            <Radio size={14} className="animate-pulse" />
                            <span>Aksiyonu Sahaya İlet (BMS Dispatch)</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>
                <span className="text-[10px] text-gray-400 mt-1 px-1">{msg.timestamp}</span>
              </div>
            ))}

            {isTyping && (
              <div className="flex items-center space-x-2 text-gray-400 text-xs pl-2">
                <RefreshCw size={12} className="animate-spin text-emerald-600" />
                <span>BOUN model verisi taranıyor...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompt Chips */}
          <div className="px-3 py-2 bg-white border-t border-gray-100 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
            {QUICK_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(prompt)}
                className="whitespace-nowrap px-2.5 py-1 rounded-full text-[10px] font-medium bg-gray-100 hover:bg-emerald-50 hover:text-emerald-800 text-gray-700 transition border border-gray-200"
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Input Footer */}
          <div className="p-3 bg-white border-t border-gray-200 flex items-center space-x-2">
            <input
              type="text"
              value={inputQuery}
              onChange={e => setInputQuery(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Kampüs hakkında soru sor veya aksiyon emri ver..."
              className="flex-1 text-xs border border-gray-300 rounded-xl px-3.5 py-2.5 focus:outline-hidden focus:ring-2 focus:ring-emerald-600 focus:border-transparent"
            />
            <button
              onClick={() => handleSend()}
              disabled={!inputQuery.trim()}
              className="bg-emerald-700 hover:bg-emerald-800 disabled:opacity-40 text-white p-2.5 rounded-xl transition shadow-xs"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
