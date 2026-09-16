import { NextResponse } from 'next/server';
import campusConfig from '@/data/campus_config.json';

export async function GET(request: Request) {
  try {
    const dashboardUrl = new URL('/api/v1/dashboard', request.url);
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (!response.ok) throw new Error(`dashboard ${response.status}`);
    const dashboard = await response.json();
    return NextResponse.json(dashboard.buildings ?? []);
  } catch {
    const unavailable = campusConfig.buildings.map(building => ({
      ...building,
      campus: building.campus as 'south' | 'north',
      occupancy_ratio: 0,
      current_occupancy: 0,
    }));
    return NextResponse.json(unavailable);
  }
}
