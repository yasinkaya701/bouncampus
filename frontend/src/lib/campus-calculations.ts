import campusConfig from '@/data/campus_config.json';
import realCourses from '@/data/real_boun_courses.json';

export const DAY_MAP: Record<string, number> = { 'M': 0, 'T': 1, 'W': 2, 'Th': 3, 'F': 4, 'St': 5 };
export const SLOT_TO_HOUR: Record<number, number> = { 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18, 11: 19, 12: 20, 13: 21 };
export const PREFIX_TO_BUILDING: Record<string, string> = {
  'TB': 'B-SOUTH-TB', 'İB': 'B-SOUTH-IB', 'IB': 'B-SOUTH-IB', 'M': 'B-SOUTH-M',
  'ALH': 'B-SOUTH-ALH', 'GH': 'B-SOUTH-GH', 'HH': 'B-SOUTH-HH', 'OFB': 'B-SOUTH-OFB',
  'ÖFB': 'B-SOUTH-OFB', 'NB': 'B-SOUTH-NB', 'JF': 'B-SOUTH-JF', 'KB': 'B-NORTH-KB',
  'NH': 'B-NORTH-NH', 'LIB': 'B-NORTH-LIB', 'BM': 'B-NORTH-BM', 'EF': 'B-NORTH-EF',
  'YD': 'B-NORTH-YD', 'ET': 'B-NORTH-ETA', 'ETA': 'B-NORTH-ETA', 'KP': 'B-NORTH-KP',
  'SBU': 'B-NORTH-SBU', 'GY': 'B-SOUTH-GY', 'KY': 'B-NORTH-KY', 'Y34': 'B-NORTH-Y34'
};

export function computeBuildingOccupancy(buildingId: string, weekday: number) {
  const b = campusConfig.buildings.find(x => x.id === buildingId);
  const floors = b ? b.floors : 4;
  const totalCap = b ? b.total_capacity : 500;

  const totalHourly: { hour: number; occupancy_count: number; occupancy_ratio: number }[] = [];
  const floorMap: Record<number, { hour: number; occupancy_count: number; occupancy_ratio: number }[]> = {};

  for (let f = 1; f <= floors; f++) floorMap[f] = [];

  const hourCounts: Record<number, number> = {};
  for (let h = 0; h < 24; h++) hourCounts[h] = 0;

  // Real OBIKAS Schedule
  const coursesList = Object.values(realCourses as Record<string, any>);
  coursesList.forEach(course => {
    const days = course.days || [];
    const hours = course.hours || [];
    const rooms = course.rooms || [];
    for (let i = 0; i < Math.min(days.length, hours.length, rooms.length); i++) {
      if (DAY_MAP[days[i]] !== weekday) continue;
      const slot = hours[i];
      const h = SLOT_TO_HOUR[slot] || slot;
      if (h < 0 || h >= 24) continue;
      const r = rooms[i].trim();
      const m = r.match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/);
      if (m && PREFIX_TO_BUILDING[m[1].toUpperCase()] === buildingId) {
        hourCounts[h] += (r.includes('401') || r.includes('101') ? 140 : 60);
      }
    }
  });

  // Dining rush override
  if (weekday < 5) {
    if (buildingId === 'B-NORTH-KY') {
      hourCounts[12] = 633; hourCounts[13] = 579; hourCounts[18] = 459; hourCounts[11] = 378; hourCounts[14] = 378;
    } else if (buildingId === 'B-SOUTH-GY') {
      hourCounts[12] = 152; hourCounts[13] = 145; hourCounts[18] = 85;
    } else if (buildingId === 'B-NORTH-LIB') {
      hourCounts[16] = 425; hourCounts[18] = 430; hourCounts[20] = 360;
    }
  }

  for (let h = 0; h < 24; h++) {
    const count = hourCounts[h] || 0;
    const ratio = Math.min(1.0, Math.round((count / totalCap) * 100) / 100);
    totalHourly.push({ hour: h, occupancy_count: count, occupancy_ratio: ratio });

    for (let f = 1; f <= floors; f++) {
      const fCount = Math.round(count / floors);
      const fRatio = Math.min(1.0, Math.round((fCount / (totalCap / floors)) * 100) / 100);
      floorMap[f].push({ hour: h, occupancy_count: fCount, occupancy_ratio: fRatio });
    }
  }

  return { building_id: buildingId, total_hourly: totalHourly, floor_hourly: floorMap };
}

export function computeBuildingEnergy(buildingId: string, weekday: number) {
  const b = campusConfig.buildings.find(x => x.id === buildingId);
  const floors = b ? b.floors : 4;
  const baseLoad = b ? b.energy_profile.base_load_kw : 30;
  const hvacCoeff = b ? b.energy_profile.hvac_coefficient : 2.5;
  const lightMax = b ? b.energy_profile.lighting_max_kw : 15;
  const tTarget = b ? b.energy_profile.t_target : 22;

  const isHistoric = b && ['Anderson', 'Washburn', 'Perkins', 'Albert Long'].some(h => b.name.includes(h));
  const histFactor = isHistoric ? 1.35 : 1.0;

  const occData = computeBuildingOccupancy(buildingId, weekday);
  const hourlyForecast: any[] = [];
  let totalOpt = 0;
  let totalBase = 0;

  for (let h = 0; h < 24; h++) {
    const occRatio = occData.total_hourly[h]?.occupancy_ratio || 0.0;
    const unoptHvac = hvacCoeff * histFactor * Math.abs(21.5 - tTarget);
    const unoptLight = lightMax * (h >= 8 && h <= 20 ? 0.8 : 0.2);
    const hBase = baseLoad + unoptHvac + unoptLight;
    totalBase += hBase;

    const floorDetails: any[] = [];
    let hOpt = 0;

    for (let f = 1; f <= floors; f++) {
      const isEco = (h >= 18 || h < 8) && f > 2 && occRatio < 0.25;
      const fBase = baseLoad / floors;
      let fHvac: number;
      let fLight: number;

      if (isEco) {
        fHvac = (hvacCoeff * histFactor * Math.abs(21.5 - tTarget) * 0.15) / floors;
        fLight = (lightMax * 0.05) / floors;
      } else {
        fHvac = (hvacCoeff * histFactor * Math.abs(21.5 - tTarget) * (0.3 + 0.7 * occRatio)) / floors;
        fLight = (lightMax * (0.1 + 0.9 * occRatio)) / floors;
      }

      const fKwh = Math.round((fBase + fHvac + fLight) * 100) / 100;
      hOpt += fKwh;
      floorDetails.push({
        floor: f,
        energy_kwh: fKwh,
        hvac_kwh: Math.round(fHvac * 100) / 100,
        lighting_kwh: Math.round(fLight * 100) / 100,
        is_active: !isEco
      });
    }

    totalOpt += hOpt;
    hourlyForecast.push({
      hour: h,
      total_kwh: Math.round(hOpt * 100) / 100,
      floor_details: floorDetails
    });
  }

  const savingKwh = Math.max(0, Math.round((totalBase - totalOpt) * 10) / 10);
  const savingPct = Math.round((savingKwh / totalBase) * 100);

  return {
    building_id: buildingId,
    building_name: b ? b.name : buildingId,
    baseline_kwh: Math.round(totalBase),
    optimized_kwh: Math.round(totalOpt),
    saving_kwh: savingKwh,
    saving_percent: savingPct,
    hourly_forecast: hourlyForecast,
    recommendations: [
      `Automate night setback across floor 3+ (${savingKwh} kWh daily reduction)`,
      `Pre-cool building before class rush at 09:00 to reduce grid peak penalty`,
      isHistoric ? 'Historic building envelope: adjust heating buffer by +1.5°C' : 'Smart multi-zone VAV modulation active'
    ]
  };
}
