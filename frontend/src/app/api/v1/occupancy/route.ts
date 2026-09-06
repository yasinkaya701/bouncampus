import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';
import { computeBuildingOccupancy } from '@/lib/campus-calculations';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const dateVal = searchParams.get('date_val') || new Date().toISOString().split('T')[0];
  const weekday = (new Date(dateVal).getDay() + 6) % 7;

  const result = campusConfig.buildings.map(b => computeBuildingOccupancy(b.id, weekday));
  return NextResponse.json(result);
}
