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

function parseCsvRows(text: string) {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let quoted = false;
  let closedQuote = false;

  const finishCell = () => {
    row.push(cell);
    cell = '';
    closedQuote = false;
  };
  const finishRow = () => {
    finishCell();
    if (row.some(value => value.trim() !== '')) rows.push(row);
    row = [];
  };

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (quoted) {
      if (char === '"') {
        if (next === '"') {
          cell += '"';
          index += 1;
        } else {
          quoted = false;
          closedQuote = true;
        }
      } else {
        cell += char;
      }
      continue;
    }

    if (char === '"') {
      if (cell.length !== 0 || closedQuote) {
        return { rows: [], errors: [`Invalid CSV quote at character ${index + 1}.`] };
      }
      quoted = true;
      continue;
    }
    if (char === ',') {
      finishCell();
      continue;
    }
    if (char === '\n' || char === '\r') {
      if (char === '\r' && next === '\n') index += 1;
      finishRow();
      continue;
    }
    if (closedQuote) {
      return { rows: [], errors: [`Unexpected text after CSV closing quote at character ${index + 1}.`] };
    }
    cell += char;
  }

  if (quoted) {
    return { rows: [], errors: ['Unterminated quoted CSV field.'] };
  }
  finishRow();
  return { rows, errors: [] as string[] };
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
  const parsed = parseCsvRows(text.replace(/^\uFEFF/, ''));
  if (parsed.errors.length) return { measurements: [], errors: parsed.errors };
  const rows = parsed.rows;
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
      errors.push(`Row ${rowIndex + 2}: expected ${headers.length} columns, received ${values.length}.`);
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
