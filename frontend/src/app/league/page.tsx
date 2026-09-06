'use client';

import React from 'react';
import { Trophy, Award, TrendingUp, Users, Leaf, Medal, Flame, CheckCircle2 } from 'lucide-react';

const FACULTIES = [
  { rank: 1, name: 'Mühendislik Fakültesi', points: 4850, energySavedMwh: 14.2, zeroWastePct: 88, badge: '🏆 Lider', members: 3200 },
  { rank: 2, name: 'İktisadi ve İdari Bilimler Fakültesi', points: 4120, energySavedMwh: 11.5, zeroWastePct: 82, badge: '🥈 2. Sıra', members: 2400 },
  { rank: 3, name: 'Fen - Edebiyat Fakültesi', points: 3890, energySavedMwh: 10.1, zeroWastePct: 79, badge: '🥉 3. Sıra', members: 2900 },
  { rank: 4, name: 'Eğitim Fakültesi', points: 3450, energySavedMwh: 8.6, zeroWastePct: 75, badge: '4. Sıra', members: 1600 },
  { rank: 5, name: 'Uygulamalı Bilimler Yüksekokulu', points: 2980, energySavedMwh: 6.9, zeroWastePct: 71, badge: '5. Sıra', members: 1100 },
];

export default function GreenLeaguePage() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-amber-50 text-amber-600 rounded-lg">
              <Trophy size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Fakülteler Arası Yeşil Lig</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Derslik kapatma disiplini, sıfır gıda atığı ve sürdürülebilir ulaşım puanlamasıyla aylık şampiyonluk yarışı.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-800">
          <Flame size={15} className="text-amber-500" />
          <span>Mart 2026 Sezonu Aktif</span>
        </div>
      </div>

      {/* Leaderboard Card */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-xs overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg text-gray-900">Genel Klasman Puan Tablosu</h3>
            <p className="text-xs text-gray-500">Her pazartesi 00:00&apos;da güncellenir</p>
          </div>
          <span className="text-xs bg-amber-100 text-amber-800 font-bold px-3 py-1 rounded-full">
            Ödül: Çevre Kulübü Yeşil Bütçesi
          </span>
        </div>

        <div className="divide-y divide-gray-100">
          {FACULTIES.map(fac => (
            <div
              key={fac.rank}
              className={`p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition ${
                fac.rank === 1 ? 'bg-amber-50/30 font-semibold' : 'hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center space-x-4">
                <div
                  className={`w-10 h-10 rounded-2xl flex items-center justify-center font-black text-sm ${
                    fac.rank === 1
                      ? 'bg-amber-500 text-white shadow-md'
                      : fac.rank === 2
                      ? 'bg-slate-300 text-slate-800'
                      : fac.rank === 3
                      ? 'bg-amber-700 text-white'
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {fac.rank}
                </div>

                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold text-sm text-gray-900">{fac.name}</h4>
                    <span className="text-[10px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md font-normal">
                      {fac.members} Öğrenci
                    </span>
                  </div>
                  <div className="text-xs text-gray-500 mt-0.5 flex items-center gap-3">
                    <span>⚡ Tasarruf: <strong>{fac.energySavedMwh} MWh</strong></span>
                    <span>🍽️ Sıfır Atık: <strong>%{fac.zeroWastePct}</strong></span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-xl font-black text-emerald-700">{fac.points} Puan</div>
                  <div className="text-[11px] text-gray-400">{fac.badge}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
