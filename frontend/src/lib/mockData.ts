import { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioResult } from './types';

export const BUILDINGS_COORDS: Record<string, [number, number]> = {
  'anderson-hall': [41.0836, 29.0506],
  'washburn-hall': [41.0833, 29.0531],
  'perkins-hall': [41.0837, 29.0519],
  'albert-long-hall': [41.0830, 29.0525],
  'gates-hall': [41.0831, 29.0518],
  'hamlin-hall': [41.0838, 29.0538],
  'dodge-hall-ofb': [41.0825, 29.0514],
  'natuk-birkan': [41.0842, 29.0510],
  'john-freely': [41.0844, 29.0505],
  'guney-yemekhane': [41.0836, 29.0528],
  'kare-blok': [41.0865, 29.0438],
  'new-hall': [41.0862, 29.0449],
  'aptullah-kuran-lib': [41.0855, 29.0442],
  'kuzey-yemekhane-piramit': [41.0868, 29.0445],
  'bilgisayar-muh': [41.0860, 29.0432],
  'egitim-fakultesi': [41.0858, 29.0446],
  'yadyok-kuzey': [41.0853, 29.0452],
  'eta-b-blok': [41.0863, 29.0430],
  'kuzey-park': [41.0874, 29.0440],
  'sinebu-idari': [41.0864, 29.0452],
  'kuzey-yurtlar': [41.0870, 29.0455],
};

export const mockBuildings: Building[] = Object.keys(BUILDINGS_COORDS).map((id, index) => ({
  id,
  name: id.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
  code: id.substring(0, 3).toUpperCase(),
  campus: BUILDINGS_COORDS[id][0] < 41.0845 ? 'south' : 'north',
  coords: BUILDINGS_COORDS[id],
  floors: 3 + (index % 3),
  total_capacity: 500 + (index * 50),
  type: index % 4 === 0 ? 'admin' : (index % 4 === 1 ? 'cafeteria' : 'academic'),
  current_occupancy: Math.floor(Math.random() * (500 + (index * 50))),
  occupancy_ratio: index % 4 === 0 ? Math.random() * 0.4 + 0.2 : Math.random() * 0.5 + 0.4, // admin 20-60%, academic 40-90%
}));

export const mockActions: ActionItem[] = [
  { id: '1', priority: 'HIGH', type: 'energy', title: 'Dim Lights in ETA B Blok', time: '14:00', location: 'ETA B Blok', description: 'Occupancy is below 20%.', impact_value: 120, impact_unit: 'kWh', icon: 'Zap' },
  { id: '2', priority: 'HIGH', type: 'food', title: 'Reduce Kuzey Yemekhane Production', time: '11:00', location: 'Kuzey Yemekhane', description: 'Demand is lower than expected due to exams.', impact_value: 300, impact_unit: 'meals', icon: 'Utensils' },
  { id: '3', priority: 'MEDIUM', type: 'space', title: 'Consolidate Study Rooms', time: '18:00', location: 'Aptullah Kuran Library', description: 'Move students to 1st floor to close 2nd floor.', impact_value: 80, impact_unit: 'kWh', icon: 'Building2' },
];

export const mockOccupancy: OccupancyForecast[] = mockBuildings.map(b => ({
  building_id: b.id,
  building_name: b.name,
  hourly: Array.from({ length: 17 }, (_, i) => ({
    hour: i + 6,
    occupancy_ratio: Math.min(1, Math.max(0, (i < 8 || i > 12) ? Math.random() * 0.5 : Math.random() * 0.5 + 0.4)),
    occupancy_count: Math.floor(b.total_capacity * Math.random()),
  }))
}));

export const mockEnergy: EnergyForecast[] = mockBuildings.map(b => ({
  building_id: b.id,
  building_name: b.name,
  baseline_kwh: 500,
  optimized_kwh: 400,
  saving_kwh: 100,
  saving_percent: 20,
  recommendations: ['Turn off lights', 'Adjust HVAC'],
}));

export const mockFood: FoodForecast[] = [
  { cafeteria_id: 'guney-yemekhane', cafeteria_name: 'Guney Yemekhane', baseline_portions: 2000, predicted_demand: 1800, recommended_production: 1850, avoided_waste_portions: 150, avoided_waste_kg: 75, menu_popularity_factor: 0.9 },
  { cafeteria_id: 'kuzey-yemekhane-piramit', cafeteria_name: 'Kuzey Yemekhane', baseline_portions: 2500, predicted_demand: 2400, recommended_production: 2400, avoided_waste_portions: 100, avoided_waste_kg: 50, menu_popularity_factor: 1.1 },
];

export const mockDashboardData: DashboardData = {
  date: new Date().toISOString().split('T')[0],
  campus_occupancy: 62,
  predicted_energy_mwh: 12.1,
  food_demand_meals: 4300,
  potential_saving_tl: 14820,
  co2_avoided_kg: 312,
  buildings: mockBuildings,
  actions: mockActions,
  occupancy_forecasts: mockOccupancy,
  energy_forecasts: mockEnergy,
  food_forecasts: mockFood,
};

export const mockScenarioResult: ScenarioResult = {
  original: mockDashboardData,
  modified: {
    ...mockDashboardData,
    predicted_energy_mwh: 14.3,
    food_demand_meals: 5080,
    potential_saving_tl: 16500,
    co2_avoided_kg: 341,
  },
  changes: {
    energy_change_percent: 18,
    food_change_percent: 21,
    co2_change_percent: 20,
    cost_change_tl: 1680,
  }
};
