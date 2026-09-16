import { NextResponse } from 'next/server';
import type { DashboardData, ScenarioRequest, ScenarioResult } from '@/lib/types';

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

export async function POST(request: Request) {
  try {
    const scenario = await request.json() as ScenarioRequest;
    const dashboardUrl = new URL('/api/v1/dashboard', request.url);
    const dashboardResponse = await fetch(dashboardUrl, { cache: 'no-store' });
    if (!dashboardResponse.ok) throw new Error(`dashboard ${dashboardResponse.status}`);

    const original = await dashboardResponse.json() as DashboardData;
    const temp = Number(scenario.params?.temp ?? 35);
    const eventSize = Number(scenario.params?.eventSize ?? 500);

    let energyChangePercent = 0;
    let foodChangePercent = 0;
    let occupancyChangePercent = 0;

    switch (scenario.scenario_type) {
      case 'heatwave':
        energyChangePercent = Math.round(Math.max(0, temp - 22) * 3.2);
        foodChangePercent = -5;
        occupancyChangePercent = -8;
        break;
      case 'exam_week':
        energyChangePercent = 16;
        foodChangePercent = 20;
        occupancyChangePercent = 28;
        break;
      case 'event': {
        const eventFactor = clamp(eventSize / 1000, 0.25, 2);
        energyChangePercent = Math.round(8 * eventFactor);
        foodChangePercent = Math.round(16 * eventFactor);
        occupancyChangePercent = Math.round(12 * eventFactor);
        break;
      }
      case 'rain':
        energyChangePercent = 7;
        foodChangePercent = 10;
        occupancyChangePercent = 5;
        break;
      case 'building_closure':
        energyChangePercent = -12;
        foodChangePercent = 0;
        occupancyChangePercent = -8;
        break;
      case 'summer_school':
        energyChangePercent = -42;
        foodChangePercent = -55;
        occupancyChangePercent = -50;
        break;
      default:
        break;
    }

    const modified: DashboardData = {
      ...original,
      campus_occupancy: clamp(original.campus_occupancy * (1 + occupancyChangePercent / 100), 0, 1),
      predicted_energy_mwh: Math.max(0, Math.round(original.predicted_energy_mwh * (1 + energyChangePercent / 100) * 10) / 10),
      food_demand_meals: Math.max(0, Math.round(original.food_demand_meals * (1 + foodChangePercent / 100))),
      potential_saving_tl: Math.max(0, Math.round(original.potential_saving_tl * (1 + Math.max(energyChangePercent, 0) / 100))),
      co2_avoided_kg: Math.max(0, Math.round(original.co2_avoided_kg * (1 + Math.max(energyChangePercent, 0) / 100))),
      data_quality: original.data_quality ? {
        ...original.data_quality,
        model_estimates: Array.from(new Set([...original.data_quality.model_estimates, 'scenario counterfactual'])),
        note: `${original.data_quality.note} Scenario outputs are counterfactual model estimates, not forecasts or live telemetry.`,
      } : original.data_quality,
    };

    const result: ScenarioResult = {
      original,
      modified,
      changes: {
        energy_change_percent: energyChangePercent,
        food_change_percent: foodChangePercent,
        co2_change_percent: energyChangePercent,
        cost_change_tl: modified.potential_saving_tl - original.potential_saving_tl,
      },
    };

    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json({ error: 'Scenario model could not be evaluated', detail: String(error) }, { status: 400 });
  }
}
