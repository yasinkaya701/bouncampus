import { NextResponse } from 'next/server';
import { computeBuildingEnergy } from '@/lib/campus-calculations';

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const { searchParams } = new URL(request.url);
  const dateVal = searchParams.get('date_val') || new Date().toISOString().split('T')[0];
  const weekday = (new Date(dateVal).getDay() + 6) % 7;

  const result = computeBuildingEnergy(params.id, weekday);
  return NextResponse.json(result);
}
