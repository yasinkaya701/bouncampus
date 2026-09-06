import { DashboardData, ActionItem, Building, EnergyForecast, FoodForecast, OccupancyForecast, ScenarioRequest, ScenarioResult } from './types';
import { mockDashboardData, mockBuildings, mockActions, mockOccupancy, mockEnergy, mockFood, mockScenarioResult } from './mockData';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

async function fetchWithFallback<T>(endpoint: string, fallback: T): Promise<T> {
  try {
    const url = API_URL ? `${API_URL}${endpoint}` : endpoint;
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error('API failed');
    return await res.json();
  } catch (err) {
    console.warn(`API call to ${endpoint} failed, using mock data. Error:`, err);
    return fallback;
  }
}

export async function getDashboard(date?: string): Promise<DashboardData> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<DashboardData>(`/api/v1/dashboard${query}`, mockDashboardData);
}

export async function getOccupancy(date?: string, buildingId?: string): Promise<OccupancyForecast[]> {
  const endpoint = buildingId ? `/api/v1/occupancy/${buildingId}` : '/api/v1/occupancy';
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<OccupancyForecast[]>(`${endpoint}${query}`, mockOccupancy);
}

export async function getEnergy(date?: string): Promise<EnergyForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<EnergyForecast[]>(`/api/v1/energy${query}`, mockEnergy);
}

export async function getFood(date?: string): Promise<FoodForecast[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<FoodForecast[]>(`/api/v1/food${query}`, mockFood);
}

export async function getActions(date?: string): Promise<ActionItem[]> {
  const query = date ? `?date_val=${date}` : '';
  return fetchWithFallback<ActionItem[]>(`/api/v1/actions${query}`, mockActions);
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
  } catch (err) {
    console.warn('API call to /api/v1/scenarios/simulate failed, using mock data. Error:', err);
    return mockScenarioResult;
  }
}

export async function getBuildings(): Promise<Building[]> {
  return fetchWithFallback<Building[]>('/api/v1/buildings', mockBuildings);
}
