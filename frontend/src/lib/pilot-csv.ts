import { validateMatchedPilotMeasurement, type MatchedPilotServiceMeasurement } from '@/lib/food-pilot-matching';

export const PILOT_CSV_HEADERS = [
  'pair_id',
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
] as const;

export type PilotCsvParseResult = {
  measurements: MatchedPilotServiceMeasurement[];
  errors: string[];
};

function parseCsvRows(text: string): { rows: string[][]; error: string | null } {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let state: 'start' | 'unquoted' | 'quoted' | 'closed' = 'start';

  const pushCell = () => {
    row.push(cell);
    cell = '';
    state = 'start';
  };
  const pushRow = () => {
    pushCell();
    if (row.some(value => value.trim() !== '')) rows.push(row);
    row = [];
  };

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (state === 'quoted') {
      if (char === '"' && next === '"') {
        cell += '"';
        index += 1;
      } else if (char === '"') {
        state = 'closed';
      } else {
        cell += char;
      }
      continue;
    }

    if (char === '"') {
      if (state !== 'start') {
        return { rows: [], error: 'Malformed CSV: unexpected quote outside a quoted field.' };
      }
      state = 'quoted';
      continue;
    }

    if (char === ',') {
      pushCell();
      continue;
    }

    if (char === '\n' || char === '\r') {
      if (char === '\r' && next === '\n') index += 1;
      pushRow();
      continue;
    }

    if (state === 'closed') {
      return { rows: [], error: 'Malformed CSV: characters after a closing quote.' };
    }
    cell += char;
    state = 'unquoted';
  }

  if (state === 'quoted') {
    return { rows: [], error: 'Malformed CSV: unterminated quoted field.' };
  }
  pushRow();
  return { rows, error: null };
}

function parseNumber(value: string, nullable = false) {
  const trimmed = value.trim();
  if (nullable && trimmed === '') return null;
  if (trimmed === '') return Number.NaN;
  const parsed = Number(trimmed);
  return Number.isFinite(parsed) ? parsed : Number.NaN;
}

function parseBoolean(value: string) {
  const normalized = value.trim().toLowerCase();
  if (['true', '1', 'yes', 'y', 'evet'].includes(normalized)) return true;
  if (['false', '0', 'no', 'n', 'hayır', 'hayir'].includes(normalized)) return false;
  return null;
}

export function parsePilotCsv(text: string): PilotCsvParseResult {
  const parsedCsv = parseCsvRows(text.replace(/^\uFEFF/, ''));
  if (parsedCsv.error) return { measurements: [], errors: [parsedCsv.error] };
  const { rows } = parsedCsv;
  if (!rows.length) return { measurements: [], errors: ['CSV is empty.'] };

  const headers = rows[0].map(value => value.trim().toLowerCase());
  const missingHeaders = PILOT_CSV_HEADERS.filter(header => !headers.includes(header));
  if (missingHeaders.length) {
    return {
      measurements: [],
      errors: [`Missing required CSV headers: ${missingHeaders.join(', ')}`],
    };
  }

  const duplicateHeaders = [...new Set(headers.filter((header, index) => headers.indexOf(header) !== index))];
  if (duplicateHeaders.length) {
    return { measurements: [], errors: [`Duplicate CSV headers: ${duplicateHeaders.join(', ')}`] };
  }

  const indexOf = (name: typeof PILOT_CSV_HEADERS[number]) => headers.indexOf(name);
  const measurements: MatchedPilotServiceMeasurement[] = [];
  const errors: string[] = [];

  rows.slice(1).forEach((values, rowIndex) => {
    if (values.length !== headers.length) {
      errors.push(`Row ${rowIndex + 2}: expected ${headers.length} CSV columns, received ${values.length}.`);
      return;
    }
    const value = (name: typeof PILOT_CSV_HEADERS[number]) => values[indexOf(name)] ?? '';
    const earlySellout = parseBoolean(value('early_sellout'));
    const operatorOverride = parseBoolean(value('operator_override'));
    const armRaw = value('arm').trim().toUpperCase();

    if (earlySellout == null || operatorOverride == null) {
      errors.push(`Row ${rowIndex + 2}: boolean fields must be true/false, yes/no, or 1/0.`);
      return;
    }

    const measurement: MatchedPilotServiceMeasurement = {
      pairId: value('pair_id').trim(),
      date: value('date').trim(),
      serviceId: value('service_id').trim(),
      arm: armRaw as MatchedPilotServiceMeasurement['arm'],
      modelForecastMeals: parseNumber(value('model_forecast_meals'), true),
      producedPortions: parseNumber(value('produced_portions')) as number,
      servedPortions: parseNumber(value('served_portions')) as number,
      edibleSurplusKg: parseNumber(value('edible_surplus_kg')) as number,
      wasteKg: parseNumber(value('waste_kg')) as number,
      earlySellout,
      operatorOverride,
      notes: value('notes').trim(),
    };

    const validationErrors = validateMatchedPilotMeasurement(measurement);
    if (validationErrors.length) {
      errors.push(`Row ${rowIndex + 2}: ${validationErrors.join('; ')}`);
      return;
    }

    measurements.push(measurement);
  });

  return { measurements, errors };
}

function escapeCsv(value: string | number | boolean | null | undefined) {
  const raw = value == null ? '' : String(value);
  return /[",\n\r]/.test(raw) ? `"${raw.replace(/"/g, '""')}"` : raw;
}

export function serializePilotCsv(measurements: MatchedPilotServiceMeasurement[]) {
  const lines = [PILOT_CSV_HEADERS.join(',')];
  measurements.forEach(item => {
    lines.push([
      item.pairId,
      item.date,
      item.serviceId,
      item.arm,
      item.modelForecastMeals,
      item.producedPortions,
      item.servedPortions,
      item.edibleSurplusKg,
      item.wasteKg,
      item.earlySellout,
      item.operatorOverride,
      item.notes ?? '',
    ].map(escapeCsv).join(','));
  });
  return `${lines.join('\n')}\n`;
}
