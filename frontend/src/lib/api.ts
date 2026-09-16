import type { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioRequest, ScenarioResult } from './types';
import type { MissionBrief } from './mission-types';
import { realBuildings } from './realData';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

async function fetchJson<T>(endpoint: string): Promise<T> {
  const url = API_URL ? `${API_URL}${endpoint}` : endpoint;
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`API ${res.status}: ${endpoint}`);
  return res.json();
}

async function fetchArrayOrEmpty<T>(endpoint: string): Promise<T[]> {
  try {
    return await fetchJson<T[]>(endpoint);
  } catch {
    return [];
  }
}

function degradedDashboard(date?: string): DashboardData {
  return {
    date: date ?? new Date().toISOString().slice(0, 10),
    campus_occupancy: 0,
    predicted_energy_mwh: 0,
    food_demand_meals: 0,
    potential_saving_tl: 0,
    co2_avoided_kg: 0,
    buildings: realBuildings.map(building => ({ ...building, current_occupancy: 0, occupancy_ratio: 0 })),
    actions: [],
    sources: [],
    data_quality: {
      mode: 'DEGRADED',
      official_live_sources: 0,
      external_live_sources: 0,
      model_estimates: [],
      unavailable_sources: ['BOUNCAMPUS dashboard API'],
      note: 'Dashboard API erişilemedi. Eski demo/mock değerleri canlı veri gibi gösterilmedi.',
    },
  };
}

export async function getDashboard(date?: string): Promise<DashboardData> {
  const query = date ? `?date_val=${date}` : '';
  try {
    return await fetchJson<DashboardData>(`/api/v1/dashboard${query}`);
  } catch {
    return degradedDashboard(date);
  }
}

export async function getMissionBrief(date?: string): Promise<MissionBrief | null> {
  const query = date ? `?date_val=${date}` : '';
  try {
    return await fetchJson<MissionBrief>(`/api/v1/brief${query}`);
  } catch {
    return null;
  }
}

export async function getOccupancy(date?: string, buildingId?: string): Promise<OccupancyForecast[]> {
  const endpoint = buildingId ? `/api/v1/occupancy/${buildingId}` : '/api/v1/occupancy';
  const query = date ? `?date_val=${date}` : '';
  return fetchArrayOrEmpty<OccupancyForecast>(`${endpoint}${query}`);
}

export async function getEnergy(date?: string): Promise<EnergyForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchArrayOrEmpty<EnergyForecast>(`/api/v1/energy${query}`);
}

export async function getFood(date?: string): Promise<FoodForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchArrayOrEmpty<FoodForecast>(`/api/v1/food${query}`);
}

export async function getActions(date?: string): Promise<ActionItem[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchArrayOrEmpty<ActionItem>(`/api/v1/actions${query}`);
}

export async function simulateScenario(scenario: ScenarioRequest): Promise<ScenarioResult> {
  const res = await fetch(`${API_URL}/api/v1/scenarios/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(scenario),
  });
  if (!res.ok) throw new Error(`Scenario API ${res.status}`);
  return res.json();
}

export async function getBuildings(): Promise<Building[]> {
  try {
    return await fetchJson<Building[]>('/api/v1/buildings');
  } catch {
    return realBuildings.map(({ current_occupancy, occupancy_ratio, ...building }) => building);
  }
}
