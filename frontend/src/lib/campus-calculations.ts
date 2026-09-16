import campusConfig from '@/data/campus_config.json';
import realCourses from '@/data/real_boun_courses.json';

export const DAY_MAP: Record<string, number> = { M: 0, T: 1, W: 2, Th: 3, F: 4, St: 5 };
export const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };
export const PREFIX_TO_BUILDING: Record<string, string> = {
  TB: 'B-SOUTH-TB', 'İB': 'B-SOUTH-IB', IB: 'B-SOUTH-IB', M: 'B-SOUTH-M',
  ALH: 'B-SOUTH-ALH', GH: 'B-SOUTH-GH', HH: 'B-SOUTH-HH', OFB: 'B-SOUTH-OFB',
  'ÖFB': 'B-SOUTH-OFB', NB: 'B-SOUTH-NB', JF: 'B-SOUTH-JF', KB: 'B-NORTH-KB',
  NH: 'B-NORTH-NH', LIB: 'B-NORTH-LIB', BM: 'B-NORTH-BM', EF: 'B-NORTH-EF',
  YD: 'B-NORTH-YD', ET: 'B-NORTH-ETA', ETA: 'B-NORTH-ETA', KP: 'B-NORTH-KP',
  SBU: 'B-NORTH-SBU', GY: 'B-SOUTH-GY', KY: 'B-NORTH-KY', Y34: 'B-NORTH-Y34',
};

function estimatedStudents(courseCode: string, room: string): number {
  const normalized = room.toUpperCase();
  let capacity = 45;
  if (/NH\s*(101|201|301|401)/.test(normalized)) capacity = 150;
  else if (/M\s*(1100|2100|2150)/.test(normalized)) capacity = 120;
  else if (/KB\s*(001|002)/.test(normalized)) capacity = 100;
  else if (/ALH/.test(normalized)) capacity = 300;
  else if (/TB\s*130|TB\s*240|İB\s*[12]0[12]|IB\s*[12]0[12]/.test(normalized)) capacity = 75;

  const level = Number(courseCode.match(/\b([1-6])\d{2}\b/)?.[1] ?? 3);
  const fill = level === 1 ? 0.88 : level === 2 ? 0.78 : level <= 4 ? 0.65 : 0.45;
  return Math.max(8, Math.round(capacity * fill));
}

function roomFloor(room: string, floorCount: number): number | null {
  const match = room.match(/(\d{3,4})/);
  if (!match) return null;
  const firstDigit = Number(match[1][0]);
  if (!Number.isFinite(firstDigit)) return null;
  if (firstDigit === 0) return 1;
  return Math.min(floorCount, Math.max(1, firstDigit));
}

export function computeBuildingOccupancy(buildingId: string, weekday: number) {
  const building = campusConfig.buildings.find(item => item.id === buildingId);
  if (!building) {
    return { building_id: buildingId, building_name: buildingId, total_hourly: [], by_floor: [] };
  }

  const floors = building.floors;
  const totalCapacity = Math.max(1, building.total_capacity);
  const hourCounts = Object.fromEntries(Array.from({ length: 24 }, (_, hour) => [hour, 0])) as Record<number, number>;
  const floorHourCounts: Record<number, Record<number, number>> = {};
  for (let floor = 1; floor <= floors; floor += 1) {
    floorHourCounts[floor] = Object.fromEntries(Array.from({ length: 24 }, (_, hour) => [hour, 0]));
  }

  const courses = Object.values(realCourses as Record<string, any>);
  for (const course of courses) {
    const days = course.days ?? [];
    const hours = course.hours ?? [];
    const rooms = course.rooms ?? [];
    for (let index = 0; index < Math.min(days.length, hours.length, rooms.length); index += 1) {
      if (DAY_MAP[days[index]] !== weekday) continue;
      const hour = SLOT_TO_HOUR[Number(hours[index])] ?? Number(hours[index]);
      if (hour < 0 || hour > 23) continue;

      const room = String(rooms[index] ?? '').trim();
      const prefix = room.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
      if (!prefix || PREFIX_TO_BUILDING[prefix] !== buildingId) continue;

      const count = estimatedStudents(String(course.code ?? ''), room);
      hourCounts[hour] += count;

      const parsedFloor = roomFloor(room, floors);
      if (parsedFloor) {
        floorHourCounts[parsedFloor][hour] += count;
      } else {
        const perFloor = Math.max(1, Math.round(count / floors));
        for (let floor = 1; floor <= floors; floor += 1) floorHourCounts[floor][hour] += perFloor;
      }
    }
  }

  const totalHourly = Array.from({ length: 24 }, (_, hour) => {
    const count = hourCounts[hour] ?? 0;
    return {
      hour,
      occupancy_count: count,
      occupancy_ratio: Math.min(1, count / totalCapacity),
    };
  });

  const byFloor = Array.from({ length: floors }, (_, index) => {
    const floor = index + 1;
    const floorCapacity = Math.max(1, (building.floor_capacities?.[index] ?? totalCapacity / floors));
    return {
      floor,
      hourly_occupancy: Array.from({ length: 24 }, (_, hour) => {
        const count = floorHourCounts[floor][hour] ?? 0;
        return { hour, occupancy_count: count, occupancy_ratio: Math.min(1, count / floorCapacity) };
      }),
    };
  });

  return {
    date: undefined,
    building_id: buildingId,
    building_name: building.name,
    total_hourly: totalHourly,
    by_floor: byFloor,
  };
}

export function computeBuildingEnergy(buildingId: string, weekday: number, ambientTemperature = 22) {
  const building = campusConfig.buildings.find(item => item.id === buildingId);
  if (!building) {
    return {
      building_id: buildingId,
      building_name: buildingId,
      baseline_kwh: 0,
      optimized_kwh: 0,
      saving_kwh: 0,
      saving_percent: 0,
      savings: { kwh_saved: 0, cost_saved_tl: 0, co2_avoided_kg: 0 },
      hourly_forecast: [],
      recommendations: [],
    };
  }

  const { floors, energy_profile: profile } = building;
  const historicFactor = ['Anderson', 'Washburn', 'Perkins', 'Albert Long'].some(name => building.name.includes(name)) ? 1.35 : 1;
  const occupancy = computeBuildingOccupancy(buildingId, weekday);
  const hourlyForecast: Array<{ hour: number; total_kwh: number; floor_details: Array<{ floor: number; energy_kwh: number; hvac_kwh: number; lighting_kwh: number; is_active: boolean }> }> = [];
  let baseline = 0;
  let optimized = 0;

  for (let hour = 0; hour < 24; hour += 1) {
    const occupancyRatio = occupancy.total_hourly[hour]?.occupancy_ratio ?? 0;
    const temperatureDelta = Math.abs(ambientTemperature - profile.t_target);
    const baselineHvac = profile.hvac_coefficient * historicFactor * temperatureDelta;
    const baselineLighting = profile.lighting_max_kw * (hour >= 8 && hour <= 20 ? 0.8 : 0.15);
    baseline += profile.base_load_kw + baselineHvac + baselineLighting;

    const floorDetails = [];
    let optimizedHour = 0;
    for (let floor = 1; floor <= floors; floor += 1) {
      const floorRatio = occupancy.by_floor.find(item => item.floor === floor)?.hourly_occupancy[hour]?.occupancy_ratio ?? occupancyRatio;
      const lowUse = floorRatio < 0.08;
      const base = profile.base_load_kw / floors;
      const hvac = (profile.hvac_coefficient * historicFactor * temperatureDelta * (lowUse ? 0.2 : 0.35 + 0.65 * floorRatio)) / floors;
      const lighting = (profile.lighting_max_kw * (lowUse ? 0.08 : 0.12 + 0.88 * floorRatio)) / floors;
      const total = base + hvac + lighting;
      optimizedHour += total;
      floorDetails.push({
        floor,
        energy_kwh: Math.round(total * 100) / 100,
        hvac_kwh: Math.round(hvac * 100) / 100,
        lighting_kwh: Math.round(lighting * 100) / 100,
        is_active: !lowUse,
      });
    }

    optimized += optimizedHour;
    hourlyForecast.push({ hour, total_kwh: Math.round(optimizedHour * 100) / 100, floor_details: floorDetails });
  }

  const savingKwh = Math.max(0, Math.round((baseline - optimized) * 10) / 10);
  const savingPercent = baseline > 0 ? Math.round((savingKwh / baseline) * 100) : 0;

  return {
    building_id: buildingId,
    building_name: building.name,
    baseline_kwh: Math.round(baseline),
    optimized_kwh: Math.round(optimized),
    saving_kwh: savingKwh,
    saving_percent: savingPercent,
    savings: {
      kwh_saved: savingKwh,
      cost_saved_tl: Math.round(savingKwh * 2.8),
      co2_avoided_kg: Math.round(savingKwh * 0.47),
    },
    hourly_forecast: hourlyForecast,
    recommendations: [
      'Model candidate: review low-use floors for manual HVAC and lighting consolidation.',
      `Model input: ${ambientTemperature.toFixed(1)}°C ambient temperature; validate against building controls before action.`,
      historicFactor > 1 ? 'Assumption: historic-building envelope penalty is applied and should be calibrated with meter data.' : 'Assumption: generic building envelope profile; calibrate with meter data when available.',
    ],
  };
}
