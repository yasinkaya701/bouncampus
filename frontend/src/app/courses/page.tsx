'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import realCoursesData from '@/data/real_boun_courses.json';
import { ArrowRight, BookOpen, Building2, ChevronLeft, ChevronRight, Clock3, Database, MapPin, Search, UserRound } from 'lucide-react';

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

const DAY_LABELS: Record<string, string> = { M: 'Pzt', T: 'Sal', W: 'Çar', Th: 'Per', F: 'Cum', St: 'Cmt' };
const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };

const BUILDING_MAP: Record<string, { id: string; name: string; campus: 'south' | 'north' }> = {
  TB: { id: 'B-SOUTH-TB', name: 'Anderson Hall', campus: 'south' },
  'İB': { id: 'B-SOUTH-IB', name: 'Washburn Hall', campus: 'south' },
  IB: { id: 'B-SOUTH-IB', name: 'Washburn Hall', campus: 'south' },
  M: { id: 'B-SOUTH-M', name: 'Perkins Hall', campus: 'south' },
  ALH: { id: 'B-SOUTH-ALH', name: 'Albert Long Hall', campus: 'south' },
  GH: { id: 'B-SOUTH-GH', name: 'Gates Hall', campus: 'south' },
  HH: { id: 'B-SOUTH-HH', name: 'Hamlin Hall', campus: 'south' },
  OFB: { id: 'B-SOUTH-OFB', name: 'Dodge Hall', campus: 'south' },
  'ÖFB': { id: 'B-SOUTH-OFB', name: 'Dodge Hall', campus: 'south' },
  NB: { id: 'B-SOUTH-NB', name: 'Natuk Birkan', campus: 'south' },
  JF: { id: 'B-SOUTH-JF', name: 'John Freely', campus: 'south' },
  KB: { id: 'B-NORTH-KB', name: 'Kare Blok', campus: 'north' },
  NH: { id: 'B-NORTH-NH', name: 'New Hall', campus: 'north' },
  LIB: { id: 'B-NORTH-LIB', name: 'Aptullah Kuran Library', campus: 'north' },
  BM: { id: 'B-NORTH-BM', name: 'Computer Engineering', campus: 'north' },
  EF: { id: 'B-NORTH-EF', name: 'Faculty of Education', campus: 'north' },
  YD: { id: 'B-NORTH-YD', name: 'YADYOK', campus: 'north' },
  ETA: { id: 'B-NORTH-ETA', name: 'ETA-B', campus: 'north' },
  ET: { id: 'B-NORTH-ETA', name: 'ETA-B', campus: 'north' },
  KP: { id: 'B-NORTH-KP', name: 'Kuzey Park', campus: 'north' },
  SBU: { id: 'B-NORTH-SBU', name: 'SineBU', campus: 'north' },
};

function roomBuilding(room?: string) {
  const prefix = room?.trim().match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
  return prefix ? BUILDING_MAP[prefix] : undefined;
}

function scheduleText(course: CourseItem) {
  const days = course.days ?? [];
  const hours = course.hours ?? [];
  return days
    .map((day, index) => {
      const slot = hours[index];
      const hour = SLOT_TO_HOUR[slot] ?? slot;
      return `${DAY_LABELS[day] ?? day} ${String(hour ?? '—').padStart(2, '0')}:00`;
    })
    .join(' · ') || 'Schedule unavailable';
}

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedDay, setSelectedDay] = useState('ALL');
  const [selectedCampus, setSelectedCampus] = useState<'ALL' | 'south' | 'north'>('ALL');
  const [page, setPage] = useState(1);
  const pageSize = 24;

  const allCourses = useMemo(() => Object.values(realCoursesData as unknown as Record<string, CourseItem>), []);

  const departments = useMemo(() => {
    const set = new Set<string>();
    allCourses.forEach(course => {
      const prefix = course.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1];
      if (prefix) set.add(prefix.toUpperCase());
    });
    return Array.from(set).sort();
  }, [allCourses]);

  const filteredCourses = useMemo(() => {
    const term = searchTerm.toLocaleLowerCase('tr-TR').trim();
    return allCourses.filter(course => {
      const dept = course.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
      if (selectedDept !== 'ALL' && dept !== selectedDept) return false;
      if (selectedDay !== 'ALL' && !(course.days ?? []).includes(selectedDay)) return false;
      if (selectedCampus !== 'ALL') {
        const match = (course.rooms ?? []).some(room => roomBuilding(room)?.campus === selectedCampus);
        if (!match) return false;
      }
      if (!term) return true;
      return [course.code, course.name, course.instructor ?? '', ...(course.rooms ?? [])]
        .some(value => value.toLocaleLowerCase('tr-TR').includes(term));
    });
  }, [allCourses, searchTerm, selectedDept, selectedDay, selectedCampus]);

  const totalPages = Math.max(1, Math.ceil(filteredCourses.length / pageSize));
  const paginatedCourses = filteredCourses.slice((page - 1) * pageSize, page * pageSize);

  const resetPage = () => setPage(1);

  return (
    <div className="space-y-4 md:space-y-5">
      <section className="bc-surface-dark relative overflow-hidden rounded-[30px] px-5 py-7 text-white sm:px-7 lg:px-9 lg:py-9">
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-blue-500/15 blur-3xl" />
        <div className="relative flex flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="bc-chip border-violet-400/20 bg-violet-400/10 text-violet-200"><Database size={10} /> OFFICIAL SNAPSHOT</span>
              <span className="font-mono text-[9px] font-bold text-slate-500">BUIS / ÖBİKAS PUBLIC COURSE SCHEDULE</span>
            </div>
            <h1 className="mt-6 text-[38px] font-black leading-[0.98] tracking-[-0.055em] sm:text-[48px]">Find any course.<br /><span className="text-blue-300">See where campus demand begins.</span></h1>
            <p className="mt-4 max-w-2xl text-[12px] leading-relaxed text-slate-400">Ders, öğretim üyesi ve oda kayıtlarını resmî kaynaklı schedule snapshot üzerinden ara. Bu sayfa canlı öğrenci sayımı değil; kampüs kullanım modelinin akademik sinyal katmanıdır.</p>
          </div>
          <div className="grid grid-cols-2 gap-2 sm:min-w-[300px]">
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4">
              <div className="text-[9px] font-black uppercase tracking-[0.16em] text-slate-500">Snapshot</div>
              <div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em] text-white">{allCourses.length.toLocaleString('tr-TR')}</div>
              <div className="mt-1 text-[10px] text-slate-500">course records</div>
            </div>
            <div className="rounded-[18px] border border-white/10 bg-white/5 p-4">
              <div className="text-[9px] font-black uppercase tracking-[0.16em] text-slate-500">Current view</div>
              <div className="mt-2 font-mono text-2xl font-black tracking-[-0.04em] text-blue-300">{filteredCourses.length.toLocaleString('tr-TR')}</div>
              <div className="mt-1 text-[10px] text-slate-500">matching records</div>
            </div>
          </div>
        </div>
      </section>

      <section className="bc-surface sticky top-[72px] z-30 rounded-[24px] p-3 sm:p-4">
        <div className="grid gap-2 lg:grid-cols-[minmax(280px,1fr)_170px_160px_auto]">
          <label className="relative block">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={searchTerm}
              onChange={event => { setSearchTerm(event.target.value); resetPage(); }}
              placeholder="CMPE 150, instructor, NH 101…"
              className="bc-focus-ring w-full rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] py-2.5 pl-10 pr-3 text-[11px] font-semibold text-slate-800 placeholder:text-slate-400"
            />
          </label>

          <select value={selectedDept} onChange={event => { setSelectedDept(event.target.value); resetPage(); }} className="bc-focus-ring rounded-[14px] border border-slate-950/10 bg-white px-3 py-2.5 text-[10px] font-bold text-slate-600">
            <option value="ALL">All departments</option>
            {departments.map(dept => <option key={dept} value={dept}>{dept}</option>)}
          </select>

          <select value={selectedDay} onChange={event => { setSelectedDay(event.target.value); resetPage(); }} className="bc-focus-ring rounded-[14px] border border-slate-950/10 bg-white px-3 py-2.5 text-[10px] font-bold text-slate-600">
            <option value="ALL">Any day</option>
            <option value="M">Pazartesi</option><option value="T">Salı</option><option value="W">Çarşamba</option><option value="Th">Perşembe</option><option value="F">Cuma</option>
          </select>

          <div className="flex rounded-[14px] border border-slate-950/10 bg-[#f4f5f2] p-1">
            {(['ALL', 'south', 'north'] as const).map(campus => (
              <button key={campus} type="button" onClick={() => { setSelectedCampus(campus); resetPage(); }} className={`bc-focus-ring rounded-[10px] px-3 py-1.5 text-[9px] font-black transition ${selectedCampus === campus ? 'bg-[#0b1226] text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'}`}>
                {campus === 'ALL' ? 'All' : campus === 'south' ? 'Güney' : 'Kuzey'}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="space-y-2">
        {paginatedCourses.length === 0 ? (
          <div className="bc-surface rounded-[26px] p-12 text-center">
            <BookOpen size={28} className="mx-auto text-slate-300" />
            <h2 className="mt-4 text-sm font-black text-slate-800">No course matches this view.</h2>
            <p className="mt-1 text-[11px] text-slate-500">Search term or filters can be broadened.</p>
          </div>
        ) : paginatedCourses.map((course, index) => {
          const mainRoom = course.rooms?.[0];
          const building = roomBuilding(mainRoom);
          return (
            <article key={`${course.code}-${index}`} className="bc-surface group rounded-[22px] p-4 transition duration-200 hover:-translate-y-0.5 hover:border-slate-950/15 hover:shadow-[0_12px_34px_rgba(10,16,32,0.06)] sm:p-5">
              <div className="grid gap-4 lg:grid-cols-[minmax(0,1.25fr)_minmax(280px,0.8fr)_auto] lg:items-center">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-lg bg-[#0b1226] px-2 py-1 font-mono text-[10px] font-black text-white">{course.code}</span>
                    <span className="font-mono text-[9px] font-bold text-slate-400">{course.credits} CR · {course.ects || 5} ECTS</span>
                  </div>
                  <h2 className="mt-2 text-[14px] font-black leading-snug tracking-[-0.02em] text-[#0a1020]">{course.name}</h2>
                  <div className="mt-2 flex items-center gap-1.5 text-[10px] font-semibold text-slate-500"><UserRound size={11} /> {course.instructor || 'Instructor not listed'}</div>
                </div>

                <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
                  <div className="rounded-[14px] bg-[#f4f5f2] p-3">
                    <div className="flex items-center gap-1 text-[8px] font-black uppercase tracking-[0.14em] text-slate-400"><Clock3 size={9} /> Schedule</div>
                    <div className="mt-1.5 text-[10px] font-bold leading-relaxed text-slate-700">{scheduleText(course)}</div>
                  </div>
                  <div className="rounded-[14px] bg-[#f4f5f2] p-3">
                    <div className="flex items-center gap-1 text-[8px] font-black uppercase tracking-[0.14em] text-slate-400"><MapPin size={9} /> Room</div>
                    <div className="mt-1.5 text-[10px] font-bold leading-relaxed text-slate-700">{(course.rooms ?? []).join(' · ') || 'Room not listed'}</div>
                  </div>
                </div>

                <div className="flex justify-end">
                  {building ? (
                    <Link href={`/buildings/${building.id}`} className="bc-focus-ring inline-flex items-center gap-2 rounded-[13px] border border-slate-950/10 bg-white px-3 py-2 text-[10px] font-black text-slate-700 transition group-hover:bg-[#0b1226] group-hover:text-white">
                      <Building2 size={12} /> {building.name} <ArrowRight size={11} />
                    </Link>
                  ) : <span className="text-[9px] font-bold text-slate-400">No mapped building</span>}
                </div>
              </div>
            </article>
          );
        })}
      </section>

      {totalPages > 1 && (
        <section className="flex flex-col gap-3 rounded-[20px] border border-slate-950/10 bg-white/60 px-4 py-3 text-[10px] sm:flex-row sm:items-center sm:justify-between">
          <span className="font-bold text-slate-500">Page <strong className="text-slate-900">{page}</strong> of {totalPages} · {filteredCourses.length.toLocaleString('tr-TR')} results</span>
          <div className="flex gap-2">
            <button type="button" disabled={page === 1} onClick={() => setPage(value => Math.max(1, value - 1))} className="bc-focus-ring inline-flex items-center gap-1 rounded-xl border border-slate-950/10 bg-white px-3 py-2 font-black text-slate-600 disabled:cursor-not-allowed disabled:opacity-35"><ChevronLeft size={11} /> Previous</button>
            <button type="button" disabled={page === totalPages} onClick={() => setPage(value => Math.min(totalPages, value + 1))} className="bc-focus-ring inline-flex items-center gap-1 rounded-xl bg-[#0b1226] px-3 py-2 font-black text-white disabled:cursor-not-allowed disabled:opacity-35">Next <ChevronRight size={11} /></button>
          </div>
        </section>
      )}
    </div>
  );
}
