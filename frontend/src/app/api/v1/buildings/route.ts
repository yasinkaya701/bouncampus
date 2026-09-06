import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';

export async function GET() {
  const buildings = campusConfig.buildings.map(b => ({
    ...b,
    campus: b.campus as 'south' | 'north',
    occupancy_ratio: 0.45,
    current_occupancy: Math.round(b.total_capacity * 0.45)
  }));
  return NextResponse.json(buildings);
}
