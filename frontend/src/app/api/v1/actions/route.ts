import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const dashboardUrl = new URL('/api/v1/dashboard', request.url);
  const dateVal = requestUrl.searchParams.get('date_val');
  if (dateVal) dashboardUrl.searchParams.set('date_val', dateVal);

  try {
    const response = await fetch(dashboardUrl, { cache: 'no-store' });
    if (!response.ok) throw new Error(`dashboard ${response.status}`);
    const dashboard = await response.json();
    return NextResponse.json(dashboard.actions ?? []);
  } catch {
    return NextResponse.json([], { status: 200 });
  }
}
