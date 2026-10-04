import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';
import { computeBuildingEnergy } from '@/lib/campus-calculations';
import { fetchBounWeather } from '@/lib/live-sources';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const dateVal = searchParams.get('date_val') || new Date().toISOString().split('T')[0];
  const weekday = (new Date(`${dateVal}T12:00:00+03:00`).getDay() + 6) % 7;
  const weather = await fetchBounWeather();
  const ambientTemperature = weather.temperature ?? 22;

  const result = campusConfig.buildings.map(building => computeBuildingEnergy(building.id, weekday, ambientTemperature));
  return NextResponse.json(result, {
    headers: {
      'Cache-Control': 'no-store',
      'X-BOUNCAMPUS-Provenance': 'SCENARIO',
      'X-BOUNCAMPUS-Energy-Method': 'COUNTERFACTUAL_MODEL',
      'X-BOUNCAMPUS-Live-Metering': 'false',
      'X-BOUNCAMPUS-BMS-Control': 'false',
      'X-BOUNCAMPUS-Achieved-Savings': 'false',
      'X-BOUNCAMPUS-Weather-Provenance': weather.source.provenance,
    },
  });
}
