'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import realCoursesData from '@/data/real_boun_courses.json';
import { ArrowRight, BookOpen, ChevronLeft, ChevronRight, Clock3, MapPin, Search, UserRound } from 'lucide-react';
import { useLocale } from '@/lib/i18n';
import { presentBuilding } from '@/lib/campus-directory';
import { formatCourseCredit } from '@/lib/course-credit-display';
import { roomBuilding, selectCourseRoom } from '@/lib/course-room-selection';

interface CourseItem {
  code: string;
  name: string;
  instructor?: string;
  credits?: number;
  ects?: number;
  days?: string[];
  hours?: number[];
  rooms?: string[];
}

type Campus = 'south' | 'north';
const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };
export default function CoursesPage() {
  const { locale, t } = useLocale();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedCampus, setSelectedCampus] = useState<'ALL' | Campus>('ALL');
  const [page, setPage] = useState(1);
  const pageSize = 24;

  const allCourses = useMemo(() => Object.values(realCoursesData as unknown as Record<string, CourseItem>), []);
  const departments = useMemo(() => Array.from(new Set(allCourses.map(course => course.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase()).filter(Boolean) as string[])).sort(), [allCourses]);
  const filteredCourses = useMemo(() => {
    const term = searchTerm.toLocaleLowerCase(locale === 'tr' ? 'tr-TR' : 'en-US').trim();
    return allCourses.filter(course => {
      const dept = course.code.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
      if (selectedDept !== 'ALL' && dept !== selectedDept) return false;
      if (selectedCampus !== 'ALL' && !(course.rooms ?? []).some(room => roomBuilding(room)?.campus === selectedCampus)) return false;
      if (!term) return true;
      return [course.code, course.name, course.instructor ?? '', ...(course.rooms ?? [])].some(value => value.toLocaleLowerCase(locale === 'tr' ? 'tr-TR' : 'en-US').includes(term));
    });
  }, [allCourses, locale, searchTerm, selectedCampus, selectedDept]);
  const totalPages = Math.max(1, Math.ceil(filteredCourses.length / pageSize));
  const currentPage = Math.min(page, totalPages);
  const paginated = filteredCourses.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const scheduleText = (course: CourseItem) => (course.days ?? []).map((day, index) => {
    const dayNames: Record<string, [string, string]> = { M: ['Pzt', 'Mon'], T: ['Sal', 'Tue'], W: ['Çar', 'Wed'], Th: ['Per', 'Thu'], F: ['Cum', 'Fri'], St: ['Cmt', 'Sat'] };
    const hour = SLOT_TO_HOUR[(course.hours ?? [])[index]];
    const dayLabel = dayNames[day]?.[locale === 'tr' ? 0 : 1] ?? day;
    return `${dayLabel} ${hour ? String(hour).padStart(2, '0') : '—'}:00`;
  }).join(' · ') || t('Program bilgisi yok', 'Schedule unavailable');

  return (
    <div className="space-y-7">
      <section className="grid gap-6 border-b border-slate-900/10 pb-7 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-end">
        <div><div className="text-[10px] font-black uppercase tracking-[0.16em] text-slate-400">BUIS / ÖBİKAS</div><h1 className="mt-3 text-[38px] font-black tracking-[-0.055em] text-slate-950 sm:text-[48px]">{t('Dersler', 'Courses')}</h1><p className="mt-3 max-w-2xl text-[12px] leading-6 text-slate-500">{t('Kamuya açık ders programı snapshot’ında ders, öğretim üyesi ve oda ara. Bu kayıtlar öğrenci doluluğu sensörü değildir.', 'Search courses, instructors and rooms in the public course-schedule snapshot. These records are not live occupancy telemetry.')}</p></div>
        <div className="grid grid-cols-2 divide-x divide-slate-900/10 border-y border-slate-900/10 py-4"><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Toplam kayıt', 'Snapshot')}</div><div className="mt-1 font-mono text-xl font-black">{allCourses.length.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')}</div></div><div className="px-4"><div className="text-[9px] font-black uppercase tracking-[0.12em] text-slate-400">{t('Eşleşen', 'Matching')}</div><div className="mt-1 font-mono text-xl font-black text-[#173f67]">{filteredCourses.length.toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')}</div></div></div>
      </section>

      <section className="grid gap-2 sm:grid-cols-[minmax(260px,1fr)_180px_auto]">
        <label className="relative"><Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input value={searchTerm} onChange={event => { setSearchTerm(event.target.value); setPage(1); }} placeholder={t('CMPE 150, öğretim üyesi, NH 101…', 'CMPE 150, instructor, NH 101…')} aria-label={t('Ders ara', 'Search courses')} className="bc-focus-ring w-full rounded-lg border border-slate-900/10 bg-white py-2.5 pl-9 pr-3 text-[11px] font-semibold" /></label>
        <select value={selectedDept} aria-label={t('Bölüme göre filtrele', 'Filter by department')} onChange={event => { setSelectedDept(event.target.value); setPage(1); }} className="bc-focus-ring rounded-lg border border-slate-900/10 bg-white px-3 text-[10px] font-semibold"><option value="ALL">{t('Tüm bölümler', 'All departments')}</option>{departments.map(dept => <option key={dept}>{dept}</option>)}</select>
        <div className="flex rounded-lg border border-slate-900/10 bg-white p-1">{(['ALL', 'south', 'north'] as const).map(campus => <button key={campus} type="button" aria-pressed={selectedCampus === campus} onClick={() => { setSelectedCampus(campus); setPage(1); }} className={`rounded-md px-3 py-1.5 text-[9px] font-bold ${selectedCampus === campus ? 'bg-[#102a43] text-white' : 'text-slate-500'}`}>{campus === 'ALL' ? t('Tümü', 'All') : campus === 'south' ? t('Güney', 'South') : t('Kuzey', 'North')}</button>)}</div>
      </section>

      <section className="divide-y divide-slate-900/10 border-y border-slate-900/10 bg-white">
        {paginated.length === 0 ? <div className="p-10 text-center text-sm font-semibold text-slate-400">{t('Eşleşen ders bulunamadı.', 'No matching course found.')}</div> : paginated.map((course, index) => {
          const room = selectCourseRoom(course.rooms, selectedCampus);
          const mapped = roomBuilding(room);
          const buildingLabel = mapped ? presentBuilding({ id: mapped.id, name: room ?? '', code: room?.match(/^[A-Za-zÇĞİÖŞÜçğıöşü]+/)?.[0] ?? '' }, locale).name : null;
          return <article key={`${course.code}-${index}`} className="grid gap-4 px-4 py-4 lg:grid-cols-[minmax(0,1fr)_260px_240px] lg:items-center"><div><div className="flex flex-wrap items-center gap-2"><span className="font-mono text-[10px] font-black text-[#173f67]">{course.code}</span><span className="text-[9px] text-slate-400">{formatCourseCredit(course.credits, 'CR')} · {formatCourseCredit(course.ects, 'ECTS')}</span></div><h2 className="mt-1 text-[13px] font-black text-slate-900">{course.name}</h2><div className="mt-1 inline-flex items-center gap-1 text-[10px] text-slate-500"><UserRound size={10} /> {course.instructor || t('Öğretim üyesi belirtilmemiş', 'Instructor not listed')}</div></div><div><div className="flex items-center gap-1 text-[9px] font-bold text-slate-400"><Clock3 size={10} /> {t('Program', 'Schedule')}</div><div className="mt-1 text-[10px] font-semibold text-slate-700">{scheduleText(course)}</div></div><div className="flex items-center justify-between gap-3"><div><div className="flex items-center gap-1 text-[9px] font-bold text-slate-400"><MapPin size={10} /> {t('Oda', 'Room')}</div><div className="mt-1 text-[10px] font-semibold text-slate-700">{(course.rooms ?? []).join(' · ') || '—'}</div></div>{mapped && buildingLabel ? <Link href={`/buildings/${mapped.id}`} className="inline-flex items-center gap-1 text-[9px] font-bold text-[#173f67]">{t('Bina', 'Building')} <ArrowRight size={10} /></Link> : null}</div></article>;
        })}
      </section>

      {totalPages > 1 && <div className="flex items-center justify-between text-[10px] text-slate-500"><span aria-live="polite">{t('Sayfa', 'Page')} {currentPage} / {totalPages}</span><div className="flex gap-1"><button type="button" aria-label={t('Önceki sayfa', 'Previous page')} disabled={currentPage <= 1} onClick={() => setPage(value => Math.max(1, value - 1))} className="rounded-lg border border-slate-900/10 bg-white p-2 disabled:opacity-30"><ChevronLeft size={12} /></button><button type="button" aria-label={t('Sonraki sayfa', 'Next page')} disabled={currentPage >= totalPages} onClick={() => setPage(value => Math.min(totalPages, value + 1))} className="rounded-lg border border-slate-900/10 bg-white p-2 disabled:opacity-30"><ChevronRight size={12} /></button></div></div>}
    </div>
  );
}
