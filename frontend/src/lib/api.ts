import { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioRequest, ScenarioResult } from './types';
import { realBuildings, realActions, realOccupancy, realEnergy, realFood, realScenarioResult } from './realData';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

async function fetchJson<T>(endpoint: string): Promise<T> {
  const url = API_URL ? `${API_URL}${endpoint}` : endpoint;
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`API ${res.status}: ${endpoint}`);
  return res.json();
}

async function fetchWithFallback<T>(endpoint: string, fallback: T): Promise<T> {
  try {
    return await fetchJson<T>(endpoint);
  } catch {
    return fallback;
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
    buildings: realBuildings.map(building => ({
      ...building,
      current_occupancy: 0,
      occupancy_ratio: 0,
    })),
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

export async function getOccupancy(date?: string, buildingId?: string): Promise<OccupancyForecast[]> {
  const endpoint = buildingId ? `/api/v1/occupancy/${buildingId}` : '/api/v1/occupancy';
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<OccupancyForecast[]>(`${endpoint}${query}`, realOccupancy);
}

export async function getEnergy(date?: string): Promise<EnergyForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<EnergyForecast[]>(`/api/v1/energy${query}`, realEnergy);
}

export async function getFood(date?: string): Promise<FoodForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<FoodForecast[]>(`/api/v1/food${query}`, realFood);
}

export async function getActions(date?: string): Promise<ActionItem[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<ActionItem[]>(`/api/v1/actions${query}`, realActions);
}

export async function simulateScenario(scenario: ScenarioRequest): Promise<ScenarioResult> {
  try {
    const res = await fetch(`${API_URL}/api/v1/scenarios/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(scenario),
    });
    if (!res.ok) throw new Error('API failed');
    return await res.json();
  } catch {
    return realScenarioResult;
  }
}

export async function getBuildings(): Promise<Building[]> {
  return fetchWithFallback<Building[]>('/api/v1/buildings', realBuildings);
}
