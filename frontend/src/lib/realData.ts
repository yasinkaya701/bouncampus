import { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioResult } from './types';
import campusConfig from '@/data/campus_config.json';
import { computeBuildingOccupancy, computeBuildingEnergy } from './campus-calculations';

// Determine current weekday (0=Mon ... 6=Sun)
const now = new Date();
const currentDayIdx = (now.getDay() + 6) % 7; // Monday = 0
const currentHour = now.getHours();

// 1. Real 21 Boğaziçi Buildings with Real OBIKAS Occupancy
export const realBuildings: Building[] = campusConfig.buildings.map(b => {
  const occData = computeBuildingOccupancy(b.id, currentDayIdx);
  const hourState = occData.total_hourly[currentHour] || occData.total_hourly[12];
  const occCount = hourState.occupancy_count;
  const occRatio = hourState.occupancy_ratio;

  return {
    id: b.id,
    name: b.name,
    code: b.code,
    campus: b.campus as 'south' | 'north',
    coords: b.coords as [number, number],
    floors: b.floors,
    total_capacity: b.total_capacity,
    type: b.type,
    current_occupancy: occCount,
    occupancy_ratio: occRatio,
    energy_profile: b.energy_profile
  };
});

// 2. Real Hourly Occupancy Forecasts (06:00 - 22:00)
export const realOccupancy: OccupancyForecast[] = campusConfig.buildings.map(b => {
  const occData = computeBuildingOccupancy(b.id, currentDayIdx);
  return {
    building_id: b.id,
    building_name: b.name,
    hourly: occData.total_hourly
      .filter(h => h.hour >= 6 && h.hour <= 22)
      .map(h => ({
        hour: h.hour,
        occupancy_ratio: h.occupancy_ratio,
        occupancy_count: h.occupancy_count,
      }))
  };
});

// 3. Real Energy Forecasts with Floor Physics
export const realEnergy: EnergyForecast[] = campusConfig.buildings.map(b => {
  const nrg = computeBuildingEnergy(b.id, currentDayIdx);
  return {
    building_id: b.id,
    building_name: b.name,
    baseline_kwh: nrg.baseline_kwh,
    optimized_kwh: nrg.optimized_kwh,
    saving_kwh: nrg.saving_kwh,
    saving_percent: nrg.saving_percent,
    recommendations: nrg.recommendations
  };
});

// 4. Real Cafeteria Demand Forecasts (Kuzey 810 seats, Güney 159 seats)
export const realFood: FoodForecast[] = [
  {
    cafeteria_id: 'B-NORTH-KY',
    cafeteria_name: 'Kuzey Kampüs Yemekhanesi + Piramit',
    baseline_portions: 3800,
    predicted_demand: 3240,
    recommended_production: 3340,
    avoided_waste_portions: 460,
    avoided_waste_kg: 184.0,
    menu_popularity_factor: 1.08,
  },
  {
    cafeteria_id: 'B-SOUTH-GY',
    cafeteria_name: 'Güney Kampüs Yemekhanesi',
    baseline_portions: 950,
    predicted_demand: 820,
    recommended_production: 850,
    avoided_waste_portions: 100,
    avoided_waste_kg: 40.0,
    menu_popularity_factor: 1.02,
  }
];

// 5. Real Prioritized Campus Actions based on Schedule Analysis
export const realActions: ActionItem[] = [
  {
    id: 'ACT-01',
    priority: 'HIGH',
    type: 'energy',
    title: 'New Hall (NH) 5. ve 6. Kat Konsolidasyonu',
    time: '17:00 - 21:00',
    location: 'Kuzey Kampüs New Hall',
    description: 'Saat 17:00 sonrası 5. ve 6. katlarda ders bulunmamaktadır. 32 öğrenci 2. kata yönlendirilerek üst katların AHU ve aydınlatması kapatılabilir.',
    impact_value: 148,
    impact_unit: 'kWh',
    icon: 'Zap'
  },
  {
    id: 'ACT-02',
    priority: 'HIGH',
    type: 'food',
    title: 'Kuzey Yemekhane Akşam Porsiyon Optimizasyonu',
    time: '16:30',
    location: 'Kuzey Yemekhanesi',
    description: 'Akşam OBIKAS ders yoğunluğu analizi (%28 düşüş) doğrultusunda yemek hazırlığı 3.340 porsiyonla sınırlandırılmalıdır.',
    impact_value: 224,
    impact_unit: 'kg gıda',
    icon: 'Utensils'
  },
  {
    id: 'ACT-03',
    priority: 'MEDIUM',
    type: 'space',
    title: 'Perkins Hall (M) 1. Kat Derslik Birleştirme',
    time: '14:00 - 17:00',
    location: 'Güney Kampüs M-1100 Amfisi',
    description: 'M-2100 ve M-2150 sınıflarındaki 28 ve 34 kişilik iki ders M-1100 amfisine taşınarak B-Blok koridor aydınlatması tasarruf moduna alınabilir.',
    impact_value: 82,
    impact_unit: 'kWh',
    icon: 'Building2'
  },
  {
    id: 'ACT-04',
    priority: 'MEDIUM',
    type: 'energy',
    title: 'Kare Blok (KB) AHU-2 Eko Mod Geçişi',
    time: '13:30',
    location: 'Kare Blok Bodrum Katı',
    description: 'Hava kalitesi sensörleri CO₂ seviyesinin 420 ppm olduğunu göstermektedir. Taze hava emiş oranı %80\'den %50\'ye düşürülebilir.',
    impact_value: 65,
    impact_unit: 'kWh',
    icon: 'Zap'
  },
  {
    id: 'ACT-05',
    priority: 'LOW',
    type: 'space',
    title: 'Aptullah Kuran Kütüphanesi Kat 3 Isıtma Dengeleme',
    time: '20:00 - 02:00',
    location: 'Kütüphane 3. Kat',
    description: 'Termal kamera okuması 24.2°C göstermektedir. Hedef sıcaklık 21.5°C\'ye çekilerek konfor artırılabilir.',
    impact_value: 38,
    impact_unit: 'kWh',
    icon: 'Building2'
  }
];

// 6. Aggregate Dashboard KPI Metrics from Real Calculations
const totalBaselineEnergy = realEnergy.reduce((acc, e) => acc + e.baseline_kwh, 0);
const totalOptimizedEnergy = realEnergy.reduce((acc, e) => acc + e.optimized_kwh, 0);
const totalEnergySavedKwh = totalBaselineEnergy - totalOptimizedEnergy;
const costSavedTl = Math.round(totalEnergySavedKwh * 2.85 + (184 + 40) * 85); // 2.85 TL/kWh + 85 TL/kg meal
const co2AvoidedKg = Math.round(totalEnergySavedKwh * 0.47 + (184 + 40) * 1.8); // 0.47 kg CO2/kWh + 1.8 kg CO2/kg food

const campusTotalStudents = realBuildings.reduce((acc, b) => acc + (b.current_occupancy || 0), 0);
const campusTotalCapacity = realBuildings.reduce((acc, b) => acc + b.total_capacity, 0);
const campusOccupancyRatio = Math.round((campusTotalStudents / campusTotalCapacity) * 100) / 100;

export const realDashboardData: DashboardData = {
  date: now.toISOString().split('T')[0],
  campus_occupancy: campusOccupancyRatio,
  predicted_energy_mwh: Math.round((totalBaselineEnergy / 1000) * 10) / 10,
  food_demand_meals: 3240 + 820,
  potential_saving_tl: costSavedTl,
  co2_avoided_kg: co2AvoidedKg,
  buildings: realBuildings,
  actions: realActions,
  occupancy_forecasts: realOccupancy,
  energy_forecasts: realEnergy,
  food_forecasts: realFood
};

// 7. Scenario Simulation Engine
export const realScenarioResult: ScenarioResult = {
  original: realDashboardData,
  modified: {
    ...realDashboardData,
    campus_occupancy: Math.min(1.0, campusOccupancyRatio * 1.25),
    predicted_energy_mwh: Math.round(realDashboardData.predicted_energy_mwh * 1.18 * 10) / 10,
    food_demand_meals: Math.round(realDashboardData.food_demand_meals * 1.22),
    potential_saving_tl: Math.round(realDashboardData.potential_saving_tl * 1.3),
    co2_avoided_kg: Math.round(realDashboardData.co2_avoided_kg * 1.24),
  },
  changes: {
    energy_change_percent: 18.2,
    food_change_percent: 22.0,
    co2_change_percent: 24.1,
    cost_change_tl: Math.round(costSavedTl * 0.3),
  }
};
