import { FOOD_WASTE_PILOT_PROTOCOL } from '@/lib/food-waste';

export async function GET() {
  const headers = [...FOOD_WASTE_PILOT_PROTOCOL.measurementFields];
  const rows = Array.from({ length: FOOD_WASTE_PILOT_PROTOCOL.durationDays }, (_, index) =>
    headers.map(header => header === 'service_id' ? `DAY_${String(index + 1).padStart(2, '0')}` : ''),
  );

  const csv = [headers, ...rows]
    .map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(','))
    .join('\n');

  return new Response(`\uFEFF${csv}\n`, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': `attachment; filename="bouncampus-food-waste-pilot-${FOOD_WASTE_PILOT_PROTOCOL.version}.csv"`,
      'Cache-Control': 'no-store',
      'X-Pilot-Protocol-Version': FOOD_WASTE_PILOT_PROTOCOL.version,
    },
  });
}
