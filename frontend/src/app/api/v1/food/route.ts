import { NextResponse } from 'next/server';
import { buildFoodOperationsModel } from '@/lib/food-waste';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const dateVal = requestUrl.searchParams.get('date_val') || new Date().toISOString().slice(0, 10);
  dashboardUrl.searchParams.set('date_val', dateVal);

  const planningBufferPct = Number(requestUrl.searchParams.get('planning_buffer_pct') ?? 12);
  const targetReductionPct = Number(requestUrl.searchParams.get('target_reduction_pct') ?? 10);

  try {
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (!response.ok) throw new Error(`dashboard ${response.status}`);

    const dashboard = await response.json();
    const model = buildFoodOperationsModel({
      date: dateVal,
      predictedDemand: Number(dashboard.food_demand_meals ?? 0),
      planningBufferPct,
      targetReductionPct,
      menu: dashboard.live_menu
        ? {
            main_dish: dashboard.live_menu.main_dish,
            vegan_dish: dashboard.live_menu.vegan_dish,
            soup: dashboard.live_menu.soup,
            popularity_multiplier: dashboard.live_menu.popularity_multiplier,
          }
        : null,
      weather: dashboard.live_weather
        ? {
            rain: dashboard.live_weather.rain,
            temperature: dashboard.live_weather.temperature,
          }
        : null,
    });

    return NextResponse.json(model);
  } catch (error) {
    return NextResponse.json(
      {
        error: 'food_operations_unavailable',
        detail: error instanceof Error ? error.message : 'unknown error',
        mode: 'DEGRADED',
      },
      { status: 503 },
    );
  }
}
