import courseSnapshotMeta from '@/data/course_snapshot_meta.json';
import publicSourceSnapshot from '@/data/public_source_snapshot.json';

export type DataProvenance =
  | 'OFFICIAL_LIVE'
  | 'OFFICIAL_SNAPSHOT'
  | 'EXTERNAL_LIVE'
  | 'MODEL_ESTIMATE'
  | 'FALLBACK';

export interface SourceMeta {
  id: string;
  label: string;
  url: string;
  provenance: DataProvenance;
  fetched_at: string;
  ok: boolean;
  detail?: string;
}

export interface WeatherFeed {
  temperature: number | null;
  humidity: number | null;
  rain: boolean | null;
  wind_speed_kmh: number | null;
  source: SourceMeta;
}

export interface MenuFeed {
  date: string | null;
  soup: string | null;
  main_dish: string | null;
  vegan_dish: string | null;
  calories: number | null;
  source: SourceMeta;
}

export interface ShuttleFeed {
  route: string;
  departure_times: string[];
  next_departure: string | null;
  source: SourceMeta;
}

export interface CalendarFeed {
  upcoming: string[];
  source: SourceMeta;
}

const BOUN_MENU_URL = 'https://yemekhane.bogazici.edu.tr';
const BOUN_CALENDAR_URL = 'https://akademiktakvim.bogazici.edu.tr/';
const BOUN_SHUTTLE_URL = 'https://mekik.bogazici.edu.tr/route.php?id=12&lang=tr';
const OPEN_METEO_URL =
  'https://api.open-meteo.com/v1/forecast?latitude=41.0833&longitude=29.0508&current=temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m&timezone=Europe%2FIstanbul';

function nowIso() {
  return new Date().toISOString();
}

function source(
  id: string,
  label: string,
  url: string,
  provenance: DataProvenance,
  ok: boolean,
  detail?: string,
): SourceMeta {
  return { id, label, url, provenance, fetched_at: nowIso(), ok, detail };
}

function staleSnapshotSource(id: string, label: string, url: string, reason: string): SourceMeta {
  return {
    id,
    label,
    url,
    provenance: 'OFFICIAL_SNAPSHOT',
    fetched_at: publicSourceSnapshot.captured_at,
    ok: false,
    detail: `Canlı upstream şu anda doğrulanamadı (${reason}). Ürün devamlılığı için ${publicSourceSnapshot.captured_at} tarihli son doğrulanmış resmî public snapshot gösteriliyor; bu veri canlı kabul edilmemelidir.`,
  };
}

async function fetchWithTimeout(url: string, revalidateSeconds: number): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5500);
  try {
    return await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'BOUNCAMPUS-Hackathon/1.0 (+public-data)' },
      next: { revalidate: revalidateSeconds },
    });
  } finally {
    clearTimeout(timer);
  }
}

function cleanHtml(value: string): string {
  return value
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&#039;/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/\s+/g, ' ')
    .trim();
}

function fieldValue(html: string, fieldName: string): string | null {
  const re = new RegExp(`${fieldName}[\\s\\S]{0,500}?<a[^>]*>([^<]+)<\\/a>`, 'i');
  const match = html.match(re);
  return match ? cleanHtml(match[1]) : null;
}

function istanbulDate(): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(new Date());
}

export async function fetchBounWeather(): Promise<WeatherFeed> {
  try {
    const res = await fetchWithTimeout(OPEN_METEO_URL, 300);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    const current = json.current ?? {};
    const temperature = Number.isFinite(current.temperature_2m) ? current.temperature_2m : null;
    const humidity = Number.isFinite(current.relative_humidity_2m) ? current.relative_humidity_2m : null;
    const windSpeed = Number.isFinite(current.wind_speed_10m) ? current.wind_speed_10m : null;
    const parsed = temperature !== null && humidity !== null && windSpeed !== null;

    return {
      temperature,
      humidity,
      rain: typeof current.rain === 'number' || typeof current.precipitation === 'number'
        ? (current.rain ?? 0) > 0.1 || (current.precipitation ?? 0) > 0.1
        : null,
      wind_speed_kmh: windSpeed,
      source: source(
        'weather-bebek',
        'Open-Meteo — Boğaziçi Bebek koordinatları',
        OPEN_METEO_URL,
        'EXTERNAL_LIVE',
        parsed,
        parsed
          ? 'Üniversite sensörü değildir; kampüs koordinatına ait haricî meteoroloji verisidir.'
          : 'Haricî kaynak erişildi ancak beklenen current hava alanları ayrıştırılamadı.',
      ),
    };
  } catch (error) {
    return {
      temperature: null,
      humidity: null,
      rain: null,
      wind_speed_kmh: null,
      source: source('weather-bebek', 'Open-Meteo', OPEN_METEO_URL, 'FALLBACK', false, String(error)),
    };
  }
}

function menuSnapshot(reason: string): MenuFeed {
  return {
    date: publicSourceSnapshot.menu.date,
    soup: publicSourceSnapshot.menu.soup,
    main_dish: publicSourceSnapshot.menu.main_dish,
    vegan_dish: publicSourceSnapshot.menu.vegan_dish,
    calories: publicSourceSnapshot.menu.calories,
    source: staleSnapshotSource('boun-sks-menu', 'Boğaziçi Üniversitesi SKS Yemekhane', BOUN_MENU_URL, reason),
  };
}

export async function fetchBounMenu(): Promise<MenuFeed> {
  try {
    const res = await fetchWithTimeout(BOUN_MENU_URL, 900);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    const soup = fieldValue(html, 'field-ccorba');
    const main = fieldValue(html, 'field-anaa-yemek');
    const vegan = fieldValue(html, 'field-vejetarien');
    const calorieMatch = html.match(/field-kalori-miktar-6[\s\S]{0,500}?([0-9]{2,4})\s*kcal/i);
    const calories = calorieMatch ? Number(calorieMatch[1]) : null;
    const parsed = Boolean(soup || main || vegan || calories);

    if (!parsed) return menuSnapshot('menü alanları ayrıştırılamadı');

    return {
      date: istanbulDate(),
      soup,
      main_dish: main,
      vegan_dish: vegan,
      calories,
      source: source(
        'boun-sks-menu',
        'Boğaziçi Üniversitesi SKS Yemekhane',
        BOUN_MENU_URL,
        'OFFICIAL_LIVE',
        true,
        'Resmî SKS sayfasından sunucu tarafında çekildi ve yapılandırılmış menü alanı ayrıştırıldı.',
      ),
    };
  } catch (error) {
    return menuSnapshot(String(error));
  }
}

function minutesFromMidnight(value: string): number {
  const [h, m] = value.split(':').map(Number);
  return h * 60 + m;
}

function nextDepartureFrom(times: string[]): string | null {
  const istanbulClock = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', hour12: false,
  }).format(new Date());
  const nowMinutes = minutesFromMidnight(istanbulClock);
  return times.find(t => minutesFromMidnight(t) >= nowMinutes) ?? null;
}

function shuttleSnapshot(reason: string): ShuttleFeed {
  const times = [...publicSourceSnapshot.shuttle.departure_times];
  return {
    route: publicSourceSnapshot.shuttle.route,
    departure_times: times,
    next_departure: nextDepartureFrom(times),
    source: staleSnapshotSource('boun-shuttle-guney-kuzey', 'Boğaziçi Üniversitesi Mekik Bilgi Sistemi', BOUN_SHUTTLE_URL, reason),
  };
}

export async function fetchBounShuttle(): Promise<ShuttleFeed> {
  const route = 'Güney Meydan → Kuzey Kampüs';
  try {
    const res = await fetchWithTimeout(BOUN_SHUTTLE_URL, 300);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();
    const times = Array.from(new Set(html.match(/\b(?:[01]\d|2[0-3]):[0-5]\d(?!:)/g) ?? []))
      .sort((a, b) => minutesFromMidnight(a) - minutesFromMidnight(b));

    if (!times.length) return shuttleSnapshot('hareket saatleri ayrıştırılamadı');

    return {
      route,
      departure_times: times,
      next_departure: nextDepartureFrom(times),
      source: source(
        'boun-shuttle-guney-kuzey',
        'Boğaziçi Üniversitesi Mekik Bilgi Sistemi',
        BOUN_SHUTTLE_URL,
        'OFFICIAL_LIVE',
        true,
        `${times.length} hareket saati ayrıştırıldı.`,
      ),
    };
  } catch (error) {
    return shuttleSnapshot(String(error));
  }
}

function calendarSnapshot(reason: string): CalendarFeed {
  return {
    upcoming: [...publicSourceSnapshot.calendar.upcoming],
    source: staleSnapshotSource('boun-academic-calendar', 'Boğaziçi Üniversitesi Akademik Takvim', BOUN_CALENDAR_URL, reason),
  };
}

export async function fetchBounCalendar(): Promise<CalendarFeed> {
  try {
    const res = await fetchWithTimeout(BOUN_CALENDAR_URL, 900);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();
    const generic = new Set(['Gelecek Etkinlikler', 'Yakın Zamanda Gerçekleşecek Etkinlikler']);
    const headings = Array.from(html.matchAll(/<h3[^>]*>([\s\S]*?)<\/h3>/gi))
      .map(match => cleanHtml(match[1]))
      .filter(text => text.length >= 8 && text.length <= 220)
      .filter(text => !generic.has(text))
      .filter(text => !/^(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+20\d{2}$/i.test(text))
      .filter((text, index, array) => array.indexOf(text) === index)
      .slice(0, 6);

    if (!headings.length) return calendarSnapshot('yapılandırılmış etkinlik ayrıştırması boş döndü');

    return {
      upcoming: headings,
      source: source(
        'boun-academic-calendar',
        'Boğaziçi Üniversitesi Akademik Takvim',
        BOUN_CALENDAR_URL,
        'OFFICIAL_LIVE',
        true,
        `${headings.length} yaklaşan takvim olayı ayrıştırıldı.`,
      ),
    };
  } catch (error) {
    return calendarSnapshot(String(error));
  }
}

export function courseScheduleSnapshotSource(courseCount: number): SourceMeta {
  const capturedAt = new Date(courseSnapshotMeta.captured_at).getTime();
  const refreshRequiredAfter = new Date(courseSnapshotMeta.refresh_required_after).getTime();
  const now = Date.now();
  const mustHavePostAddDropCapture = now > refreshRequiredAfter;
  const isFreshEnough = !mustHavePostAddDropCapture || capturedAt > refreshRequiredAfter;
  const ok = courseCount > 0 && isFreshEnough;

  return {
    id: 'boun-course-schedule',
    label: `Boğaziçi BUIS/ÖBİKAS public course schedule snapshot (${courseSnapshotMeta.term})`,
    url: courseSnapshotMeta.source_url,
    provenance: 'OFFICIAL_SNAPSHOT',
    fetched_at: courseSnapshotMeta.captured_at,
    ok,
    detail: ok
      ? `${courseCount.toLocaleString('tr-TR')} ders yerel snapshot içinde. Bu kaynak canlı sensör/öğrenci sayımı değildir. Add/drop sonrası yeniden yakalama release gate'idir.`
      : `${courseCount.toLocaleString('tr-TR')} ders var ancak snapshot add/drop sonrasındaki 30 Eylül 2026 tazelik kapısını geçmiyor. Hackathon release öncesi resmî schedule kaynağından yenilenmelidir.`,
  };
}
