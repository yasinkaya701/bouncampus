import { FOOD_WASTE_PILOT_PROTOCOL } from '@/lib/food-waste';

export async function GET() {
  const headers = [
    'date',
    'service_id',
    'arm',
    'model_forecast_meals',
    'produced_portions',
    'served_portions',
    'edible_surplus_kg',
    'waste_kg',
    'early_sellout',
    'operator_override',
    'notes',
  ];

  const rows = Array.from({ length: FOOD_WASTE_PILOT_PROTOCOL.durationDays }, (_, index) => [
    '',
    `DAY_${String(index + 1).padStart(2, '0')}`,
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
  ]);

  const csv = [headers, ...rows]
    .map(row => row.map(value => `"${String(value).replaceAll('"', '""')}"`).join(','))
    .join('\n');

  return new Response(`\uFEFF${csv}\n`, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': 'attachment; filename="bouncampus-food-waste-pilot-template.csv"',
      'Cache-Control': 'no-store',
    },
  });
}
