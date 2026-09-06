'use client';

import React, { useState } from 'react';
import { Utensils, HeartHandshake, Trash2, Droplets, Leaf, CheckCircle2, TrendingDown, Clock, ShieldCheck, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const MENU_FOOTPRINT_DATA = [
  { item: 'Etli Nohut Yemeği', SuLitre: 1840, KarbonGram: 920, Kalori: 317, KalanPorsiyon: 45 },
  { item: 'Melek Pilavı', SuLitre: 320, KarbonGram: 210, Kalori: 240, KalanPorsiyon: 30 },
  { item: 'Bamya Çorbası', SuLitre: 140, KarbonGram: 85, Kalori: 110, KalanPorsiyon: 20 },
  { item: 'Dubai Magnolia', SuLitre: 450, KarbonGram: 380, Kalori: 380, KalanPorsiyon: 15 },
];

export default function FoodWastePage() {
  const [redistributeDone, setRedistributeDone] = useState(false);

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-orange-50 text-orange-700 rounded-lg">
              <Utensils size={24} />
            </span>
            <h1 className="text-3xl font-black text-gray-900 tracking-tight">Sıfır Atık Mutfak & SKS Yemekhane AI</h1>
          </div>
          <p className="text-sm text-gray-500 mt-1">
            Resmi menü karbon/su ayak izi takibi, talep bazlı porsiyon optimizasyonu ve yurtlara fazla yemek paylaşım ağı.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-xl text-xs font-bold text-amber-800">
          <Leaf size={16} className="text-amber-600" />
          <span>Sıfır Atık Kampüs (Zero Waste Campus)</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">AI Önerilen Üretim</span>
          <div className="text-3xl font-black text-gray-900">3,584</div>
          <div className="text-xs text-emerald-700 font-semibold mt-1">Standart 4,200 yerine -%14.7</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Önlenen Fazla Porsiyon:</span>
            <span className="font-bold text-emerald-700">616 Porsiyon</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Engellenen Gıda İsrafı</span>
          <div className="text-3xl font-black text-emerald-700">246 kg</div>
          <div className="text-xs text-gray-500 mt-1">Porsiyon başı 0.40 kg bertaraf tasarrufu</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Ekonomik Tasarruf:</span>
            <span className="font-bold text-emerald-800">₺27,720</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Tasarruf Edilen Su</span>
          <div className="text-3xl font-black text-blue-700">1.13 Milyon L</div>
          <div className="text-xs text-gray-500 mt-1">Gıda üretiminde sanal su ayak izi</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Eşdeğer:</span>
            <span className="font-bold text-blue-800">452 Olimpik Havuz</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">Engellenen Sera Gazı</span>
          <div className="text-3xl font-black text-teal-700">566 kg CO₂e</div>
          <div className="text-xs text-gray-500 mt-1">Metan & Lojistik kaynaklı salınım</div>
          <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs">
            <span className="text-gray-500">Ağaç Eşdeğeri:</span>
            <span className="font-bold text-teal-800">28 Yetişkin Çam</span>
          </div>
        </div>
      </div>

      {/* Campus Food Rescue Card */}
      <div className="bg-gradient-to-r from-emerald-800 to-teal-800 text-white rounded-2xl p-6 shadow-md flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="p-2 bg-white/20 rounded-xl">
              <HeartHandshake size={24} />
            </span>
            <h3 className="font-bold text-xl">Boğaziçi Kampüs Gıda Kurtarma & Dağıtım Ağı (Food Rescue)</h3>
          </div>
          <p className="text-xs text-emerald-100 max-w-2xl leading-relaxed">
            Öğle ve akşam servislerinden kalan taze, hijyenik porsiyonlar çöpe atılmak yerine otomatik olarak
            <strong> Kuzey 3. ve 4. Yurt etüt odalarına</strong> ve <strong>Belediye Aşevi Soğuk Zincirine</strong> transfer edilir.
          </p>
        </div>

        <div className="shrink-0">
          <button
            onClick={() => setRedistributeDone(true)}
            disabled={redistributeDone}
            className={`px-5 py-3 rounded-xl text-xs font-bold transition shadow-md flex items-center gap-2 ${
              redistributeDone
                ? 'bg-emerald-600 text-white cursor-default'
                : 'bg-white text-emerald-900 hover:bg-emerald-50 active:scale-95'
            }`}
          >
            {redistributeDone ? (
              <>
                <CheckCircle2 size={16} />
                <span>Yurt Transfer Emri Gönderildi!</span>
              </>
            ) : (
              <>
                <HeartHandshake size={16} />
                <span>Kalan 110 Porsiyonu Yurtlara Aktar</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Menu Footprint Breakdown */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h3 className="font-bold text-xl text-gray-900">Bugünün Resmi Menüsü — Sanal Su & Karbon Ayak İzi</h3>
            <p className="text-xs text-gray-500">
              SKS resmi menüsündeki her yemeğin hazırlanmasında harcanan su ve oluşan karbon yükü
            </p>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={MENU_FOOTPRINT_DATA} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="item" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="SuLitre" fill="#0284c7" name="Su Ayak İzi (Litre)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="KarbonGram" fill="#10b981" name="Karbon (Gram CO₂)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
