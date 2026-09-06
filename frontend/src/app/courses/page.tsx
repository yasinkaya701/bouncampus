'use client';

import React, { useState, useMemo } from 'react';
import Header from '@/components/shared/Header';
import realCoursesData from '@/data/real_boun_courses.json';
import Link from 'next/link';
import { 
  BookOpen, Search, Filter, Calendar, MapPin, Clock, 
  GraduationCap, Award, Building2, User, ChevronRight, Zap
} from 'lucide-react';

interface CourseItem {
  code: string;
  name: string;
  instructor?: string;
  credits: number;
  ects: number;
  days?: string[];
  hours?: number[];
  rooms?: string[];
}

const DAY_LABELS: Record<string, string> = {
  'M': 'Pazartesi',
  'T': 'Salı',
  'W': 'Çarşamba',
  'Th': 'Perşembe',
  'F': 'Cuma',
  'St': 'Cumartesi'
};

const BUILDING_MAP: Record<string, { id: string; name: string; campus: 'south' | 'north' }> = {
  'TB': { id: 'B-SOUTH-TB', name: 'Anderson Hall', campus: 'south' },
  'İB': { id: 'B-SOUTH-IB', name: 'Washburn Hall', campus: 'south' },
  'IB': { id: 'B-SOUTH-IB', name: 'Washburn Hall', campus: 'south' },
  'M': { id: 'B-SOUTH-M', name: 'Perkins Hall', campus: 'south' },
  'ALH': { id: 'B-SOUTH-ALH', name: 'Albert Long Hall', campus: 'south' },
  'GH': { id: 'B-SOUTH-GH', name: 'Gates Hall', campus: 'south' },
  'HH': { id: 'B-SOUTH-HH', name: 'Hamlin Hall', campus: 'south' },
  'OFB': { id: 'B-SOUTH-OFB', name: 'Dodge Hall (ÖFB)', campus: 'south' },
  'ÖFB': { id: 'B-SOUTH-OFB', name: 'Dodge Hall (ÖFB)', campus: 'south' },
  'NB': { id: 'B-SOUTH-NB', name: 'Natuk Birkan', campus: 'south' },
  'JF': { id: 'B-SOUTH-JF', name: 'John Freely', campus: 'south' },
  'KB': { id: 'B-NORTH-KB', name: 'Kare Blok', campus: 'north' },
  'NH': { id: 'B-NORTH-NH', name: 'New Hall', campus: 'north' },
  'LIB': { id: 'B-NORTH-LIB', name: 'Aptullah Kuran Kütüphanesi', campus: 'north' },
  'BM': { id: 'B-NORTH-BM', name: 'Bilgisayar Müh.', campus: 'north' },
  'EF': { id: 'B-NORTH-EF', name: 'Eğitim Fakültesi', campus: 'north' },
  'YD': { id: 'B-NORTH-YD', name: 'YADYOK', campus: 'north' },
  'ETA': { id: 'B-NORTH-ETA', name: 'ETA-B Blok', campus: 'north' },
  'ET': { id: 'B-NORTH-ETA', name: 'ETA-B Blok', campus: 'north' },
  'KP': { id: 'B-NORTH-KP', name: 'Teknopark', campus: 'north' },
  'SBU': { id: 'B-NORTH-SBU', name: 'SineBU', campus: 'north' },
};

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedDay, setSelectedDay] = useState('ALL');
  const [selectedCampus, setSelectedCampus] = useState<'ALL' | 'south' | 'north'>('ALL');
  const [page, setPage] = useState(1);
  const pageSize = 30;

  // Convert dictionary of courses to array
  const allCourses: CourseItem[] = useMemo(() => {
    return Object.values(realCoursesData as unknown as Record<string, CourseItem>);
  }, []);

  // Extract list of all unique departments from codes (e.g. CMPE from CMPE 150.01)
  const departments = useMemo(() => {
    const set = new Set<string>();
    allCourses.forEach(c => {
      const match = c.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/);
      if (match) set.add(match[1].toUpperCase());
    });
    return Array.from(set).sort();
  }, [allCourses]);

  // Filter courses
  const filteredCourses = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();

    return allCourses.filter(course => {
      // Dept filter
      if (selectedDept !== 'ALL') {
        const match = course.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/);
        if (!match || match[1].toUpperCase() !== selectedDept) return false;
      }

      // Day filter
      if (selectedDay !== 'ALL') {
        if (!course.days || !course.days.includes(selectedDay)) return false;
      }

      // Search term
      if (term) {
        const matchesCode = course.code.toLowerCase().includes(term);
        const matchesName = course.name.toLowerCase().includes(term);
        const matchesInstructor = (course.instructor || '').toLowerCase().includes(term);
        const matchesRoom = (course.rooms || []).some(r => r.toLowerCase().includes(term));
        if (!matchesCode && !matchesName && !matchesInstructor && !matchesRoom) return false;
      }

      // Campus filter
      if (selectedCampus !== 'ALL') {
        const hasCampusRoom = (course.rooms || []).some(r => {
          const m = r.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/);
          if (m && BUILDING_MAP[m[1].toUpperCase()]) {
            return BUILDING_MAP[m[1].toUpperCase()].campus === selectedCampus;
          }
          return false;
        });
        if (!hasCampusRoom) return false;
      }

      return true;
    });
  }, [allCourses, searchTerm, selectedDept, selectedDay, selectedCampus]);

  const totalPages = Math.ceil(filteredCourses.length / pageSize);
  const paginatedCourses = filteredCourses.slice((page - 1) * pageSize, page * pageSize);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8 space-y-6">
        {/* Header Title */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono text-xs font-bold flex items-center gap-1.5 border border-emerald-500/30">
                <BookOpen size={13} className="text-emerald-400" />
                OBIKAS CANLI VERİ TABANI
              </span>
              <span className="text-xs text-slate-400 font-mono">3.238 Gerçek Boğaziçi Dersi & Amfisi</span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
              Boğaziçi Ders, Amfi & Doluluk Arama Motoru
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Ders koduna, amfiye, öğretim üyesine veya bölüme göre canlı arama yapın; derslik doluluk ve enerji yüklerini inceleyin.
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 px-4 py-2.5 rounded-2xl flex items-center gap-4 text-center">
            <div>
              <span className="text-[10px] text-slate-400 font-mono block">Toplam Ders</span>
              <span className="text-xl font-black text-emerald-400 font-mono">{allCourses.length}</span>
            </div>
            <div className="w-px h-8 bg-slate-800"></div>
            <div>
              <span className="text-[10px] text-slate-400 font-mono block">Filtrelenen</span>
              <span className="text-xl font-black text-white font-mono">{filteredCourses.length}</span>
            </div>
          </div>
        </div>

        {/* Search & Filter Bar */}
        <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-2xl shadow-xl space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            {/* Search Input */}
            <div className="flex-1 min-w-[260px] relative">
              <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Ders kodu (CMPE 150), ders adı, hoca veya amfi (NH 101, M 1100)..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setPage(1);
                }}
                className="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 outline-none transition"
              />
            </div>

            {/* Department Selector */}
            <select
              value={selectedDept}
              onChange={(e) => {
                setSelectedDept(e.target.value);
                setPage(1);
              }}
              className="bg-slate-950 border border-slate-800 text-xs text-slate-200 px-3 py-2.5 rounded-xl outline-none focus:border-emerald-500 font-mono"
            >
              <option value="ALL">Tüm Bölümler ({departments.length})</option>
              {departments.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>

            {/* Day Selector */}
            <select
              value={selectedDay}
              onChange={(e) => {
                setSelectedDay(e.target.value);
                setPage(1);
              }}
              className="bg-slate-950 border border-slate-800 text-xs text-slate-200 px-3 py-2.5 rounded-xl outline-none focus:border-emerald-500"
            >
              <option value="ALL">Tüm Günler</option>
              <option value="M">Pazartesi</option>
              <option value="T">Salı</option>
              <option value="W">Çarşamba</option>
              <option value="Th">Perşembe</option>
              <option value="F">Cuma</option>
            </select>

            {/* Campus Selector */}
            <div className="flex items-center space-x-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
              <button
                onClick={() => { setSelectedCampus('ALL'); setPage(1); }}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition ${selectedCampus === 'ALL' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Tümü
              </button>
              <button
                onClick={() => { setSelectedCampus('south'); setPage(1); }}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition ${selectedCampus === 'south' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Güney
              </button>
              <button
                onClick={() => { setSelectedCampus('north'); setPage(1); }}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition ${selectedCampus === 'north' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Kuzey
              </button>
            </div>
          </div>
        </div>

        {/* Results List */}
        <div className="space-y-3">
          {paginatedCourses.length === 0 ? (
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
              <BookOpen size={36} className="mx-auto text-slate-600 mb-3" />
              <p className="font-bold text-base text-white">Aramanızla eşleşen Boğaziçi dersi bulunamadı.</p>
              <p className="text-xs text-slate-500 mt-1">Filtreleri temizleyerek tekrar deneyin.</p>
            </div>
          ) : (
            paginatedCourses.map((c, idx) => {
              const mainRoom = (c.rooms && c.rooms[0]) ? c.rooms[0].trim() : 'Amfi Belirlenmedi';
              const roomPrefix = mainRoom.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/);
              const bldgInfo = roomPrefix ? BUILDING_MAP[roomPrefix[1].toUpperCase()] : null;

              return (
                <div 
                  key={`${c.code}-${idx}`}
                  className="bg-slate-900/60 hover:bg-slate-900/95 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-4 transition shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4 backdrop-blur-md"
                >
                  {/* Left: Code, Title & Instructor */}
                  <div className="space-y-1 md:max-w-[48%]">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-md bg-emerald-950 text-emerald-400 border border-emerald-800/80 font-mono text-xs font-black">
                        {c.code}
                      </span>
                      <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                        {c.credits} Kredi • {c.ects || 5.0} AKTS
                      </span>
                    </div>
                    <h3 className="font-bold text-sm text-white">{c.name}</h3>
                    <p className="text-xs text-slate-400 flex items-center gap-1">
                      <User size={12} className="text-slate-500" />
                      <span>{c.instructor || 'Öğretim Üyesi Belirtilmedi'}</span>
                    </p>
                  </div>

                  {/* Middle: Schedule & Amfi */}
                  <div className="flex flex-wrap items-center gap-4 text-xs">
                    <div className="bg-slate-950 px-3 py-2 rounded-xl border border-slate-800 font-mono">
                      <span className="text-slate-500 text-[10px] block flex items-center gap-1">
                        <Clock size={11} /> Ders Saatleri
                      </span>
                      <span className="text-slate-200 font-bold">
                        {(c.days || []).map((d, i) => `${DAY_LABELS[d] || d} ${(c.hours || [])[i] || ''}:00`).join(', ') || 'Saat Belirtilmedi'}
                      </span>
                    </div>

                    <div className="bg-slate-950 px-3 py-2 rounded-xl border border-slate-800 font-mono">
                      <span className="text-slate-500 text-[10px] block flex items-center gap-1">
                        <MapPin size={11} /> Derslik / Amfi
                      </span>
                      <span className="text-emerald-400 font-bold">
                        {(c.rooms || []).join(', ') || 'Online / Belirtilmedi'}
                      </span>
                    </div>
                  </div>

                  {/* Right: Building Link & Details */}
                  <div>
                    {bldgInfo ? (
                      <Link
                        href={`/buildings/${bldgInfo.id}`}
                        className="bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-bold px-3.5 py-2 rounded-xl transition flex items-center gap-1.5 shadow-xs whitespace-nowrap"
                      >
                        <Building2 size={13} />
                        <span>{bldgInfo.name}</span>
                        <ChevronRight size={13} />
                      </Link>
                    ) : (
                      <span className="text-xs text-slate-500 italic">Genel Kampüs</span>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Pagination Bar */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between pt-4 border-t border-slate-800 text-xs text-slate-400">
            <span>
              Sayfa <strong className="text-white">{page}</strong> / {totalPages} ({filteredCourses.length} ders)
            </span>
            <div className="flex items-center space-x-2">
              <button
                disabled={page === 1}
                onClick={() => setPage(p => Math.max(1, p - 1))}
                className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-800 transition"
              >
                &larr; Önceki
              </button>
              <button
                disabled={page === totalPages}
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-800 transition"
              >
                Sonraki &rarr;
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
