import { NextResponse } from 'next/server';
import { buildFoodIntelligence, reforecastFoodDecision } from '@/lib/food-intelligence';
import type { DashboardData, FoodIntelligenceResponse, FoodMealType, FoodReforecastRequest } from '@/lib/types';

const VALID_MEALS = new Set<FoodMealType>(['breakfast', 'lunch', 'dinner']);

async function loadDecisionContext(request: Request, date: string): Promise<FoodIntelligenceResponse> {
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  dashboardUrl.searchParams.set('date_val', date);

  const response = await fetch(dashboardUrl, { cache: 'no-store' });
  if (!response.ok) throw new Error(`dashboard ${response.status}`);
  const dashboard = await response.json() as DashboardData;

  return buildFoodIntelligence({
    date,
    northSouthLunchSignal: Number(dashboard.food_demand_meals ?? 0) || null,
    rain: dashboard.live_weather?.rain ?? null,
    temperature: dashboard.live_weather?.temperature ?? null,
    menu: dashboard.live_menu ? {
      main_dish: dashboard.live_menu.main_dish,
      soup: dashboard.live_menu.soup,
      vegan_dish: dashboard.live_menu.vegan_dish,
      source: dashboard.live_menu.source,
      provenance: dashboard.live_menu.provenance ? {
        provenance: dashboard.live_menu.provenance.provenance,
        ok: dashboard.live_menu.provenance.ok,
      } : null,
    } : null,
  });
}

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const date = requestUrl.searchParams.get('date')
    ?? requestUrl.searchParams.get('date_val')
    ?? new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Istanbul' }).format(new Date());

  try {
    const result = await loadDecisionContext(request, date);
    return NextResponse.json(result, {
      headers: { 'Cache-Control': 'no-store' },
    });
  } catch (error) {
    return NextResponse.json({
      error: 'FOOD_INTELLIGENCE_CONTEXT_UNAVAILABLE',
      detail: error instanceof Error ? error.message : 'Unable to build food decision context',
    }, { status: 503 });
  }
}

export async function POST(request: Request) {
  let body: FoodReforecastRequest;
  try {
    body = await request.json() as FoodReforecastRequest;
  } catch {
    return NextResponse.json({ error: 'INVALID_JSON' }, { status: 400 });
  }

  if (!body.cafeteria_id || !VALID_MEALS.has(body.meal_type)) {
    return NextResponse.json({ error: 'cafeteria_id and a valid meal_type are required' }, { status: 400 });
  }
  if (!Number.isFinite(body.served_so_far) || body.served_so_far < 0) {
    return NextResponse.json({ error: 'served_so_far must be a non-negative number' }, { status: 400 });
  }
  if (!Number.isFinite(body.elapsed_fraction) || body.elapsed_fraction <= 0 || body.elapsed_fraction >= 1) {
    return NextResponse.json({ error: 'elapsed_fraction must be between 0 and 1' }, { status: 400 });
  }
  if (body.queue_count != null && (!Number.isFinite(body.queue_count) || body.queue_count < 0)) {
    return NextResponse.json({ error: 'queue_count must be a non-negative number' }, { status: 400 });
  }

  const date = body.date
    ?? new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Istanbul' }).format(new Date());

  try {
    const context = await loadDecisionContext(request, date);
    const prior = context.forecasts.find(item => (
      item.cafeteria_id === body.cafeteria_id && item.meal_type === body.meal_type
    ));
    if (!prior) {
      return NextResponse.json({ error: 'FORECAST_NOT_FOUND_FOR_SERVICE' }, { status: 404 });
    }

    const updated = reforecastFoodDecision(prior, body);
    return NextResponse.json({
      ...context,
      forecasts: context.forecasts.map(item => (
        item.cafeteria_id === updated.cafeteria_id && item.meal_type === updated.meal_type ? updated : item
      )),
      reforecasted_at: new Date().toISOString(),
      reforecast_input_provenance: 'USER_INPUT',
    }, {
      headers: { 'Cache-Control': 'no-store' },
    });
  } catch (error) {
    return NextResponse.json({
      error: 'FOOD_REFORECAST_UNAVAILABLE',
      detail: error instanceof Error ? error.message : 'Unable to reforecast food demand',
    }, { status: 503 });
  }
}
