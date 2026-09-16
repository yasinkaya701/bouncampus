import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';
import realCourses from '@/data/real_boun_courses.json';
import type { ActionItem } from '@/lib/types';
import {
  courseScheduleSnapshotSource,
  fetchBounCalendar,
  fetchBounMenu,
  fetchBounShuttle,
  fetchBounWeather,
  type SourceMeta,
} from '@/lib/live-sources';

const DAY_MAP: Record<string, number> = { M: 0, T: 1, W: 2, Th: 3, F: 4, St: 5 };
const SLOT_TO_HOUR: Record<number, number> = {
  1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21,
};
const PREFIX_TO_BUILDING: Record<string, string> = {
  TB: 'B-SOUTH-TB', 'İB': 'B-SOUTH-IB', IB: 'B-SOUTH-IB', M: 'B-SOUTH-M', ALH: 'B-SOUTH-ALH',
  GH: 'B-SOUTH-GH', HH: 'B-SOUTH-HH', OFB: 'B-SOUTH-OFB', 'ÖFB': 'B-SOUTH-OFB', NB: 'B-SOUTH-NB',
  JF: 'B-SOUTH-JF', KB: 'B-NORTH-KB', NH: 'B-NORTH-NH', LIB: 'B-NORTH-LIB', BM: 'B-NORTH-BM',
  EF: 'B-NORTH-EF', YD: 'B-NORTH-YD', ET: 'B-NORTH-ETA', ETA: 'B-NORTH-ETA', KP: 'B-NORTH-KP',
  SBU: 'B-NORTH-SBU', GY: 'B-SOUTH-GY', KY: 'B-NORTH-KY', Y34: 'B-NORTH-Y34',
};

function istanbulHour(): number {
  return Number(new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Istanbul', hour: '2-digit', hour12: false,
  }).format(new Date()));
}

function estimatedStudents(courseCode: string, room: string): number {
  const roomUpper = room.toUpperCase();
  let capacity = 45;
  if (/NH\s*(101|201|301|401)/.test(roomUpper)) capacity = 150;
  else if (/M\s*(1100|2100|2150)/.test(roomUpper)) capacity = 120;
  else if (/KB\s*(001|002)/.test(roomUpper)) capacity = 100;
  else if (/ALH/.test(roomUpper)) capacity = 300;
  else if (/TB\s*130|TB\s*240|İB\s*[12]0[12]|IB\s*[12]0[12]/.test(roomUpper)) capacity = 75;

  const level = Number(courseCode.match(/\b([1-6])\d{2}\b/)?.[1] ?? 3);
  const fill = level === 1 ? 0.88 : level === 2 ? 0.78 : level <= 4 ? 0.65 : 0.45;
  return Math.max(8, Math.round(capacity * fill));
}

function buildSchedule(weekday: number) {
  const hourly: Record<string, Record<number, number>> = {};
  campusConfig.buildings.forEach(building => {
    hourly[building.id] = Object.fromEntries(Array.from({ length: 24 }, (_, h) => [h, 0]));
  });

  const courses = Object.values(realCourses as Record<string, any>);
  for (const course of courses) {
    const days = course.days ?? [];
    const hours = course.hours ?? [];
    const rooms = course.rooms ?? [];
    for (let i = 0; i < Math.min(days.length, hours.length, rooms.length); i += 1) {
      if (DAY_MAP[days[i]] !== weekday) continue;
      const clockHour = SLOT_TO_HOUR[Number(hours[i])] ?? Number(hours[i]);
      const room = String(rooms[i] ?? '').trim();
      const prefix = room.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
      const buildingId = prefix ? PREFIX_TO_BUILDING[prefix] : undefined;
      if (!buildingId || !hourly[buildingId] || clockHour < 0 || clockHour > 23) continue;
      hourly[buildingId][clockHour] += estimatedStudents(String(course.code ?? ''), room);
    }
  }
  return { hourly, courses };
}

function modelSource(id: string, label: string, detail: string): SourceMeta {
  return {
    id,
    label,
    url: '/',
    provenance: 'MODEL_ESTIMATE',
    fetched_at: new Date().toISOString(),
    ok: true,
    detail,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const dateVal = searchParams.get('date_val') || new Date().toISOString().slice(0, 10);
  const dt = new Date(`${dateVal}T12:00:00+03:00`);
  const weekday = (dt.getDay() + 6) % 7;

  const [weather, menu, shuttle, calendar] = await Promise.all([
    fetchBounWeather(),
    fetchBounMenu(),
    fetchBounShuttle(),
    fetchBounCalendar(),
  ]);

  const { hourly: scheduleHourly, courses } = buildSchedule(weekday);
  const scheduleSource = courseScheduleSnapshotSource(courses.length);
  const evalHour = Math.min(21, Math.max(8, istanbulHour()));

  let totalCurrent = 0;
  let totalCapacity = 0;
  const buildings = campusConfig.buildings.map(building => {
    const current = scheduleHourly[building.id]?.[evalHour] ?? 0;
    totalCurrent += current;
    totalCapacity += building.total_capacity;
    return {
      ...building,
      campus: building.campus as 'south' | 'north',
      current_occupancy: current,
      occupancy_ratio: Math.min(1, current / Math.max(1, building.total_capacity)),
    };
  });

  const temperature = weather.temperature ?? 22;
  const buildingEnergy = campusConfig.buildings.map(building => {
    const profile = building.energy_profile;
    let baselineKwh = 0;
    let optimizedKwh = 0;
    for (let hour = 7; hour <= 22; hour += 1) {
      const occ = scheduleHourly[building.id]?.[hour] ?? 0;
      const ratio = Math.min(1, occ / Math.max(1, building.total_capacity));
      const base = profile.base_load_kw;
      const hvac = profile.hvac_coefficient * Math.abs(temperature - profile.t_target) * (0.3 + 0.7 * ratio);
      const lighting = profile.lighting_max_kw * (0.1 + 0.9 * ratio);
      baselineKwh += base + hvac + lighting;

      const lowUse = ratio < 0.08;
      optimizedKwh += base + hvac * (lowUse ? 0.5 : 0.92) + lighting * (lowUse ? 0.3 : 0.92);
    }
    const eveningOcc = [18, 19, 20, 21].reduce((sum, h) => sum + (scheduleHourly[building.id]?.[h] ?? 0), 0);
    return {
      id: building.id,
      name: building.name,
      baselineKwh,
      optimizedKwh,
      savedKwh: Math.max(0, baselineKwh - optimizedKwh),
      eveningOcc,
    };
  });

  const baselineEnergyKwh = buildingEnergy.reduce((sum, item) => sum + item.baselineKwh, 0);
  const optimizedEnergyKwh = buildingEnergy.reduce((sum, item) => sum + item.optimizedKwh, 0);
  const savedKwh = Math.max(0, baselineEnergyKwh - optimizedEnergyKwh);

  const lunchClassFlow = campusConfig.buildings.reduce((sum, building) => {
    const hours = scheduleHourly[building.id];
    return sum + (hours?.[11] ?? 0) + (hours?.[12] ?? 0) + (hours?.[13] ?? 0);
  }, 0) / 3;
  const rainFactor = weather.rain ? 1.08 : 1;
  const foodDemandMeals = Math.round(lunchClassFlow * 0.72 * rainFactor);

  const energyModelSource = modelSource(
    'campus-energy-model',
    'BOUNCAMPUS physics-lite energy model',
    'BMS/utility meter erişimi olmadığı için bina profili + ders programı + dış sıcaklıktan hesaplanan tahmindir.',
  );
  const occupancyModelSource = modelSource(
    'campus-occupancy-model',
    'BOUNCAMPUS timetable occupancy model',
    'Kart/geçiş sensörü değildir. Resmî ders programındaki oda ve saatlerden oda kapasitesi temelli öğrenci tahmini üretir.',
  );
  const foodModelSource = modelSource(
    'cafeteria-demand-model',
    'BOUNCAMPUS cafeteria demand model',
    'POS verisi olmadığı için öğle ders akışı + hava koşulundan talep tahmini üretir.',
  );

  const candidates = [...buildingEnergy]
    .filter(item => item.eveningOcc < 30 && item.savedKwh > 1)
    .sort((a, b) => b.savedKwh - a.savedKwh)
    .slice(0, 2);

  const actions: ActionItem[] = candidates.map((item, index) => ({
    id: `energy-${item.id}`,
    priority: index === 0 ? 'HIGH' : 'MEDIUM',
    type: 'energy',
    title: `${item.name}: düşük kullanım konsolidasyonu`,
    time: '18:00 - 22:00',
    location: item.name,
    description: `Resmî ders programı snapshot'ında akşam yükü düşük. Boş katların HVAC/aydınlatmasını eko moda almak modelde yaklaşık ${Math.round(item.savedKwh)} kWh/gün potansiyel gösteriyor. BMS komutu uygulanmadan önce saha doğrulaması gerekir.`,
    impact_value: Math.round(item.savedKwh),
    impact_unit: 'kWh model potansiyeli',
    icon: 'Zap',
    provenance: 'MODEL_ESTIMATE',
  }));

  if (foodDemandMeals > 0) {
    actions.push({
      id: 'food-demand-plan',
      priority: 'MEDIUM',
      type: 'food',
      title: menu.main_dish ? `${menu.main_dish}: üretim planını talep tahminiyle doğrula` : 'Yemekhane üretim planını talep tahminiyle doğrula',
      time: '10:30 - 13:30',
      location: 'Kuzey + Güney Yemekhaneleri',
      description: `Ders çıkış akışı ve hava koşuluna göre öğle talebi yaklaşık ${foodDemandMeals.toLocaleString('tr-TR')} porsiyon. Bu sayı POS verisi değildir; mutfak üretim kararı için gerçek satış verisiyle kalibre edilmelidir.`,
      impact_value: foodDemandMeals,
      impact_unit: 'porsiyon talep tahmini',
      icon: 'Utensils',
      provenance: 'MODEL_ESTIMATE',
    });
  }

  const sources = [weather.source, menu.source, shuttle.source, calendar.source, scheduleSource, occupancyModelSource, energyModelSource, foodModelSource];
  const unavailable = sources.filter(item => !item.ok).map(item => item.label);
  const officialLive = sources.filter(item => item.provenance === 'OFFICIAL_LIVE' && item.ok).length;
  const externalLive = sources.filter(item => item.provenance === 'EXTERNAL_LIVE' && item.ok).length;

  return NextResponse.json({
    date: dateVal,
    campus_occupancy: totalCurrent / Math.max(1, totalCapacity),
    predicted_energy_mwh: Math.round((baselineEnergyKwh / 1000) * 10) / 10,
    food_demand_meals: foodDemandMeals,
    potential_saving_tl: Math.round(savedKwh * 2.8),
    co2_avoided_kg: Math.round(savedKwh * 0.47),
    buildings,
    actions,
    live_weather: {
      source: weather.source.label,
      temperature: weather.temperature,
      humidity: weather.humidity,
      rain: weather.rain,
      wind_speed: weather.wind_speed_kmh,
      provenance: weather.source,
    },
    live_menu: {
      source: menu.source.label,
      date: menu.date ?? dateVal,
      soup: menu.soup,
      main_dish: menu.main_dish,
      calories: menu.calories,
      vegan_dish: menu.vegan_dish,
      sides: [],
      options: [],
      popularity_multiplier: 1,
      provenance: menu.source,
    },
    live_shuttle: {
      route: shuttle.route,
      departure_times: shuttle.departure_times,
      next_departure: shuttle.next_departure,
      provenance: shuttle.source,
    },
    academic_calendar: calendar.upcoming,
    today_events: [],
    real_courses_loaded: courses.length,
    sources,
    data_quality: {
      mode: unavailable.length ? 'DEGRADED' : 'LIVE_WITH_MODELS',
      official_live_sources: officialLive,
      external_live_sources: externalLive,
      model_estimates: ['occupancy', 'energy', 'food demand', 'savings', 'CO₂ avoided'],
      unavailable_sources: unavailable,
      note: 'BOUNCAMPUS hiçbir model tahminini kampüs sensörü ölçümü olarak sunmaz. Canlı ve tahmin veri sınıfları API cevabında ayrı provenance taşır.',
    },
  });
}
