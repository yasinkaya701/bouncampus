import { MATCHED_FOOD_WASTE_PILOT_PROTOCOL } from '@/lib/food-pilot-matching';

export async function GET() {
  const headers = [...MATCHED_FOOD_WASTE_PILOT_PROTOCOL.measurementFields];
  const rows = Array.from({ length: MATCHED_FOOD_WASTE_PILOT_PROTOCOL.durationDays }, (_, index) => {
    const pairNumber = Math.floor(index / 2) + 1;
    const pairId = `PAIR_${String(pairNumber).padStart(2, '0')}`;
    const arm = index % 2 === 0 ? 'CONTROL' : 'INTERVENTION';
    const seededValues: Record<string, string> = {
      pair_id: pairId,
      service_id: `${pairId}_${arm}`,
      arm,
    };
    return headers.map(header => seededValues[header] ?? '');
  });

  const csv = [headers, ...rows]
    .map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(','))
    .join('\n');

  return new Response(`\uFEFF${csv}\n`, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': `attachment; filename="bouncampus-food-waste-pilot-${MATCHED_FOOD_WASTE_PILOT_PROTOCOL.version}.csv"`,
      'Cache-Control': 'no-store',
      'X-Pilot-Protocol-Version': MATCHED_FOOD_WASTE_PILOT_PROTOCOL.version,
    },
  });
}
