import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';
import { computeBuildingEnergy } from '@/lib/campus-calculations';
import { fetchBounWeather } from '@/lib/live-sources';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const dateVal = searchParams.get('date_val') || new Date().toISOString().split('T')[0];
  const weekday = (new Date(`${dateVal}T12:00:00+03:00`).getDay() + 6) % 7;
  const weather = await fetchBounWeather();
  const ambientTemperature = weather.temperature ?? 22;

  const result = campusConfig.buildings.map(building => computeBuildingEnergy(building.id, weekday, ambientTemperature));
  return NextResponse.json(result);
}
