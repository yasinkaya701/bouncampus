import { NextResponse } from 'next/server';
import type { FoodForecast } from '@/lib/types';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const dateVal = requestUrl.searchParams.get('date_val');
  if (dateVal) dashboardUrl.searchParams.set('date_val', dateVal);

  try {
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (!response.ok) throw new Error(`dashboard ${response.status}`);
    const dashboard = await response.json();
    const predicted = Number(dashboard.food_demand_meals ?? 0);

    const forecast: FoodForecast = {
      cafeteria_id: 'BOUN-DINING-COMBINED',
      cafeteria_name: 'Kuzey + Güney Yemekhaneleri',
      baseline_portions: predicted,
      predicted_demand: predicted,
      recommended_production: predicted,
      avoided_waste_portions: 0,
      avoided_waste_kg: 0,
      menu_popularity_factor: 1,
    };

    return NextResponse.json(predicted > 0 ? [forecast] : []);
  } catch {
    return NextResponse.json([]);
  }
}
