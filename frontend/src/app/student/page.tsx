'use client';

import React, { useState } from 'react';
import { BookOpen, Utensils, Award, Footprints, Clock, Zap, MapPin, CheckCircle, Heart, Star, Sparkles, Navigation } from 'lucide-react';

export default function StudentPortalPage() {
  const [activeTab, setActiveTab] = useState<'study' | 'dining' | 'badges' | 'commute'>('study');
  const [ratedMeal, setRatedMeal] = useState(false);

  return (
    <div className="space-y-8 max-w-4xl mx-auto pb-16">
      {/* Header */}
      <div className="text-center space-y-2">
        <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full uppercase tracking-wider">
          Öğrenci Deneyim Portalı
        </span>
        <h1 className="text-3xl font-black text-gray-900 tracking-tight">BOUNCAMPUS Öğrenci Rehberi</h1>
        <p className="text-xs text-gray-500 max-w-md mx-auto">
          En sakin çalışma alanları, anlık yemekhane bekleme süresi ve kişisel yeşil kampüs puanın.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center justify-center gap-2 bg-gray-100 p-1.5 rounded-2xl text-xs font-bold max-w-lg mx-auto">
        <button
          onClick={() => setActiveTab('study')}
          className={`flex-1 py-2 rounded-xl transition flex items-center justify-center gap-1.5 ${activeTab === 'study' ? 'bg-white text-emerald-900 shadow-xs' : 'text-gray-600'}`}
        >
          <BookOpen size={15} />
          <span>Sakin Çalışma Alanı</span>
        </button>
        <button
          onClick={() => setActiveTab('dining')}
          className={`flex-1 py-2 rounded-xl transition flex items-center justify-center gap-1.5 ${activeTab === 'dining' ? 'bg-white text-emerald-900 shadow-xs' : 'text-gray-600'}`}
        >
          <Utensils size={15} />
          <span>Yemekhane & Sıra</span>
        </button>
        <button
          onClick={() => setActiveTab('badges')}
          className={`flex-1 py-2 rounded-xl transition flex items-center justify-center gap-1.5 ${activeTab === 'badges' ? 'bg-white text-emerald-900 shadow-xs' : 'text-gray-600'}`}
        >
          <Award size={15} />
          <span>Karbon Rozetlerim</span>
        </button>
      </div>

      {/* TAB 1: STUDY SPACES */}
      {activeTab === 'study' && (
        <div className="space-y-4">
          <h3 className="font-bold text-sm text-gray-700 uppercase tracking-wider">Önerilen Sakin Çalışma Noktaları</h3>

          <div className="space-y-3">
            <div className="bg-white rounded-2xl border border-emerald-200 p-5 shadow-xs hover:border-emerald-400 transition">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full mb-1 inline-block">
                    En Yüksek Puanlı & En Sakin
                  </span>
                  <h4 className="font-bold text-gray-900 text-base">Aptullah Kuran Kütüphanesi — 2. Kat Sessiz Salon</h4>
                  <p className="text-xs text-gray-500">Kuzey Kampüs • Bireysel Çalışma Masaları</p>
                </div>
                <div className="text-right">
                  <span className="text-lg font-black text-emerald-700">46 Boş Yer</span>
                  <span className="block text-[10px] text-gray-400">Priz & Wi-Fi %100</span>
                </div>
              </div>
              <div className="mt-3 pt-3 border-t border-gray-100 flex items-center gap-4 text-xs text-gray-600">
                <span>🌡️ Sıcaklık: <strong>22.0°C</strong></span>
                <span>🔊 Ses Seviyesi: <strong>28 dB (Çok Sessiz)</strong></span>
                <span>💡 Doğal Işık: <strong>Yüksek</strong></span>
              </div>
            </div>

            <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-xs hover:border-gray-300 transition">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-bold text-gray-900 text-base">Perkins Hall (M) — 2. Kat Koridor Çalışma Masaları</h4>
                  <p className="text-xs text-gray-500">Güney Kampüs • Boğaz Manzaralı Çalışma Alanı</p>
                </div>
                <div className="text-right">
                  <span className="text-lg font-black text-amber-600">14 Boş Yer</span>
                  <span className="block text-[10px] text-gray-400">Tarihi Doku</span>
                </div>
              </div>
              <div className="mt-3 pt-3 border-t border-gray-100 flex items-center gap-4 text-xs text-gray-600">
                <span>🌡️ Sıcaklık: <strong>21.5°C</strong></span>
                <span>🔊 Ses Seviyesi: <strong>42 dB (Düşük)</strong></span>
                <span>⚡ Priz Durumu: <strong>Orta</strong></span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: DINING & QUEUE */}
      {activeTab === 'dining' && (
        <div className="space-y-4">
          <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div>
                <h3 className="font-bold text-lg text-gray-900">Günün Resmi SKS Menüsü</h3>
                <p className="text-xs text-gray-500">Öğle & Akşam Servisi</p>
              </div>
              <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full">
                317 kcal
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="bg-gray-50 p-3 rounded-xl">
                <span className="text-[10px] text-gray-400 block mb-1">Çorba</span>
                <span className="font-bold text-xs text-gray-800">Bamya Çorbası</span>
              </div>
              <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-xl">
                <span className="text-[10px] text-emerald-700 font-bold block mb-1">Ana Yemek</span>
                <span className="font-bold text-xs text-emerald-950">Etli Nohut Yemeği</span>
              </div>
              <div className="bg-gray-50 p-3 rounded-xl">
                <span className="text-[10px] text-gray-400 block mb-1">Yan Yemek</span>
                <span className="font-bold text-xs text-gray-800">Melek Pilavı</span>
              </div>
              <div className="bg-gray-50 p-3 rounded-xl">
                <span className="text-[10px] text-gray-400 block mb-1">Tatlı / Meyve</span>
                <span className="font-bold text-xs text-gray-800">Dubai Magnolia</span>
              </div>
            </div>

            {/* Menu rating */}
            <div className="pt-2 flex items-center justify-between">
              <span className="text-xs text-gray-600">Bugünkü menüyü oyla:</span>
              <button
                onClick={() => setRatedMeal(true)}
                disabled={ratedMeal}
                className="px-4 py-1.5 bg-gray-100 hover:bg-emerald-50 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 text-gray-800"
              >
                <Star size={14} className={ratedMeal ? 'text-amber-500 fill-amber-500' : 'text-gray-400'} />
                <span>{ratedMeal ? 'Oyun Kaydedildi (+10 Puan)' : '4.8 ★ Oyla'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: BADGES & GAMIFICATION */}
      {activeTab === 'badges' && (
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-emerald-800 to-teal-800 text-white rounded-2xl p-6 shadow-md flex items-center justify-between">
            <div>
              <span className="text-xs text-emerald-200 font-bold uppercase tracking-wider block mb-1">Toplam Yeşil Skorun</span>
              <div className="text-4xl font-black">1,420 Puan</div>
              <p className="text-xs text-emerald-100 mt-1">Son 30 günde 42 kg CO₂ tasarrufu sağladın.</p>
            </div>
            <div className="w-16 h-16 rounded-2xl bg-white/20 flex items-center justify-center">
              <Award size={32} className="text-amber-300 animate-pulse" />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-xl border border-gray-200 text-center space-y-2">
              <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-800 mx-auto flex items-center justify-center font-bold">
                🚶
              </div>
              <h4 className="font-bold text-xs text-gray-900">Yürüyüş Şampiyonu</h4>
              <p className="text-[10px] text-gray-500">Ring yerine Bebek yokuşunu 10 kez yürüdün.</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 text-center space-y-2">
              <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-800 mx-auto flex items-center justify-center font-bold">
                🍽️
              </div>
              <h4 className="font-bold text-xs text-gray-900">Temiz Tabak</h4>
              <p className="text-[10px] text-gray-500">Yemekhanede tabakta hiç gıda bırakmadın.</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 text-center space-y-2">
              <div className="w-10 h-10 rounded-full bg-amber-100 text-amber-800 mx-auto flex items-center justify-center font-bold">
                💡
              </div>
              <h4 className="font-bold text-xs text-gray-900">Işık Söndürücü</h4>
              <p className="text-[10px] text-gray-500">Boş etüt odası ışığını bildirdin.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
