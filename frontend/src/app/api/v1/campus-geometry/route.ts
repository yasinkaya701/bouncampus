import { NextRequest, NextResponse } from 'next/server';

type CampusKey = 'main' | 'south' | 'north' | 'hisar' | 'ucaksavar' | 'kandilli' | 'anadolu' | 'kilyos';
type BBox = readonly [south: number, west: number, north: number, east: number];

type OverpassPoint = { lat: number; lon: number };
type OverpassMember = { role?: string; geometry?: OverpassPoint[] };
type OverpassTags = Record<string, string | undefined>;
type OverpassElement = {
  id: number;
  type: 'node' | 'way' | 'relation';
  center?: { lat: number; lon: number };
  geometry?: OverpassPoint[];
  members?: OverpassMember[];
  tags?: OverpassTags;
};

const CAMPUS_BOUNDS: Record<Exclude<CampusKey, 'main'>, BBox> = {
  south: [41.0800, 29.0480, 41.0850, 29.0548],
  north: [41.0842, 29.0415, 41.0885, 29.0478],
  hisar: [41.0874, 29.0480, 41.0912, 29.0527],
  ucaksavar: [41.0845, 29.0378, 41.0870, 29.0422],
  kandilli: [41.0604, 29.0567, 41.0650, 29.0648],
  anadolu: [41.0785, 29.0680, 41.0835, 29.0750],
  kilyos: [41.2378, 29.0045, 41.2460, 29.0175],
};

const MAIN_KEYS = ['south', 'north', 'hisar', 'ucaksavar'] as const;

function parseMeters(value?: string) {
  if (!value) return undefined;
  const normalized = value.trim().toLowerCase().replace(',', '.');
  const numeric = Number.parseFloat(normalized);
  if (!Number.isFinite(numeric) || numeric <= 0) return undefined;
  if (normalized.includes('ft') || normalized.includes("'")) return Math.round(numeric * 0.3048 * 10) / 10;
  return Math.round(numeric * 10) / 10;
}

function parsePositiveInt(value?: string) {
  if (!value) return undefined;
  const numeric = Number.parseFloat(value.replace(',', '.'));
  if (!Number.isFinite(numeric) || numeric <= 0) return undefined;
  return Math.max(1, Math.round(numeric));
}

function ringArea(ring: OverpassPoint[]) {
  if (ring.length < 3) return 0;
  let area = 0;
  for (let index = 0; index < ring.length; index += 1) {
    const current = ring[index];
    const next = ring[(index + 1) % ring.length];
    area += current.lon * next.lat - next.lon * current.lat;
  }
  return Math.abs(area / 2);
}

function extractFootprint(element: OverpassElement): OverpassPoint[] | undefined {
  if (element.geometry && element.geometry.length >= 3) return element.geometry;
  const outerRings = (element.members ?? [])
    .filter(member => (member.role === 'outer' || !member.role) && member.geometry && member.geometry.length >= 3)
    .map(member => member.geometry as OverpassPoint[])
    .sort((a, b) => ringArea(b) - ringArea(a));
  return outerRings[0];
}

function fallbackHeight(tags: OverpassTags) {
  const levels = parsePositiveInt(tags['building:levels']);
  if (levels) return levels * 3.35;
  const kind = (tags.building ?? '').toLowerCase();
  if (kind.includes('dormitory') || kind.includes('apartments')) return 15;
  if (kind.includes('school') || kind.includes('university')) return 13;
  if (kind.includes('sports')) return 9;
  return 10.5;
}

function queryFor(bounds: BBox[]) {
  const selectors = bounds.flatMap(([south, west, north, east]) => [
    `way["building"](${south},${west},${north},${east});`,
    `relation["building"](${south},${west},${north},${east});`,
    `way["building:part"](${south},${west},${north},${east});`,
    `relation["building:part"](${south},${west},${north},${east});`,
  ]).join('');
  return `[out:json][timeout:24];(${selectors});out tags center geom;`;
}

function campusForCenter(lat: number, lon: number): Exclude<CampusKey, 'main'> | 'context' {
  for (const [key, [south, west, north, east]] of Object.entries(CAMPUS_BOUNDS) as [Exclude<CampusKey, 'main'>, BBox][]) {
    if (lat >= south && lat <= north && lon >= west && lon <= east) return key;
  }
  return 'context';
}

export async function GET(request: NextRequest) {
  const requested = request.nextUrl.searchParams.get('campus') as CampusKey | null;
  const campus: CampusKey = requested && (requested === 'main' || requested in CAMPUS_BOUNDS) ? requested : 'main';
  const bounds = campus === 'main' ? MAIN_KEYS.map(key => CAMPUS_BOUNDS[key]) : [CAMPUS_BOUNDS[campus]];
  const query = queryFor(bounds);

  try {
    const response = await fetch('https://overpass-api.de/api/interpreter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: new URLSearchParams({ data: query }),
      next: { revalidate: 86400 },
    });
    if (!response.ok) throw new Error(`Overpass ${response.status}`);

    const payload = await response.json() as { elements?: OverpassElement[] };
    const seen = new Set<string>();
    const buildings = (payload.elements ?? []).flatMap(element => {
      const key = `${element.type}/${element.id}`;
      if (seen.has(key)) return [];
      seen.add(key);
      const footprint = extractFootprint(element);
      if (!footprint || footprint.length < 3) return [];

      const center = footprint.reduce((acc, point) => ({ lat: acc.lat + point.lat, lon: acc.lon + point.lon }), { lat: 0, lon: 0 });
      const lat = center.lat / footprint.length;
      const lon = center.lon / footprint.length;
      const tags = element.tags ?? {};
      const explicitHeight = parseMeters(tags.height);
      const levels = parsePositiveInt(tags['building:levels']);
      const minLevel = parsePositiveInt(tags['building:min_level']);
      const explicitMinHeight = parseMeters(tags.min_height);
      const minHeight = explicitMinHeight ?? (minLevel ? minLevel * 3.35 : 0);
      const height = explicitHeight ?? (levels ? levels * 3.35 : fallbackHeight(tags));
      const heightSource = explicitHeight ? 'OSM_HEIGHT' : levels ? 'OSM_LEVELS' : 'VISUALIZATION_ESTIMATE';
      const roofLevels = parsePositiveInt(tags['roof:levels']);
      const roofHeight = parseMeters(tags['roof:height']) ?? (roofLevels ? roofLevels * 2.6 : 0);
      const isPart = Boolean(tags['building:part']);

      return [{
        osm_id: key,
        name: tags.name ?? null,
        campus: campusForCenter(lat, lon),
        geometry_kind: isPart ? 'BUILDING_PART' : 'BUILDING',
        coords: [lat, lon] as [number, number],
        footprint: footprint.map(point => [point.lat, point.lon] as [number, number]),
        height_m: Math.max(3, height),
        height_source: heightSource,
        levels,
        min_height_m: minHeight,
        min_level: minLevel,
        roof_levels: roofLevels,
        roof_height_m: roofHeight,
        roof_shape: tags['roof:shape'] ?? null,
        roof_orientation: tags['roof:orientation'] ?? null,
        building: tags.building ?? null,
        building_part: tags['building:part'] ?? null,
        building_material: tags['building:material'] ?? null,
        building_colour: tags['building:colour'] ?? null,
        roof_material: tags['roof:material'] ?? null,
        roof_colour: tags['roof:colour'] ?? null,
        start_date: tags.start_date ?? null,
        source: 'OpenStreetMap / Overpass',
        osm_url: `https://www.openstreetmap.org/${element.type}/${element.id}`,
      }];
    });

    return NextResponse.json({
      campus,
      buildings,
      source: 'OpenStreetMap / Overpass',
      fetched_at: new Date().toISOString(),
      degraded: false,
      note: 'Footprints, building parts and explicit height/level tags are source-backed. Missing heights are conservative visualization estimates and are not survey-grade measurements.',
    });
  } catch (error) {
    return NextResponse.json({
      campus,
      buildings: [],
      source: 'OpenStreetMap / Overpass',
      fetched_at: new Date().toISOString(),
      degraded: true,
      detail: error instanceof Error ? error.message : 'Campus geometry source unavailable',
    });
  }
}
