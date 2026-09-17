import { NextResponse } from 'next/server';

const TARGETS = [
  { id: 'B-SOUTH-TB', aliases: ['Anderson Hall', 'Fen-Edebiyat Binası', 'Temel Bilimler Binası'] },
  { id: 'B-SOUTH-IB', aliases: ['Washburn Hall', 'İdari Bilimler Binası', 'İktisadi ve İdari Bilimler Fakültesi'] },
  { id: 'B-SOUTH-M', aliases: ['Perkins Hall', 'Mühendislik Binası', 'Mühendislik Fakültesi'] },
  { id: 'B-SOUTH-ALH', aliases: ['Albert Long Hall', 'Saatli Bina'] },
  { id: 'B-SOUTH-GH', aliases: ['Gates Hall', 'Genel İdare Binası'] },
  { id: 'B-SOUTH-HH', aliases: ['Hamlin Hall', '1. Erkek Yurdu'] },
  { id: 'B-SOUTH-OFB', aliases: ['Öğrenci Faaliyetleri Binası', 'Student Activities Building', 'Henrietta Washburn Hall'] },
  { id: 'B-SOUTH-NB', aliases: ['Natuk Birkan', 'Natuk Birkan Binası'] },
  { id: 'B-SOUTH-JF', aliases: ['John Freely', 'John Freely Binası', 'John Freely Hall'] },
  { id: 'B-SOUTH-GY', aliases: ['Güney Yemekhanesi', 'Güney Kampüs Yemekhanesi'] },
  { id: 'B-NORTH-KB', aliases: ['Kare Blok', 'Kare Bina', 'Fen ve Mühendislik Binası', 'Science and Technology Building'] },
  { id: 'B-NORTH-NH', aliases: ['New Hall', 'Yeni Bina'] },
  { id: 'B-NORTH-LIB', aliases: ['Aptullah Kuran Kütüphanesi', 'Aptullah Kuran Library'] },
  { id: 'B-NORTH-KY', aliases: ['Kuzey Yemekhanesi', 'Kuzey Kampüs Yemekhanesi'] },
  { id: 'B-NORTH-BM', aliases: ['Bilgisayar Mühendisliği Binası', 'Computer Engineering Building', 'ETA A Blok', 'ETA-A'] },
  { id: 'B-NORTH-EF', aliases: ['Eğitim Fakültesi', 'Faculty of Education'] },
  { id: 'B-NORTH-YD', aliases: ['YADYOK II', 'Kuzey YADYOK', 'School of Foreign Languages', 'New Classroom Building'] },
  { id: 'B-NORTH-ETA', aliases: ['ETA B Blok', 'ETA-B', 'ETA-B Blok', 'Education Technology Building'] },
  { id: 'B-NORTH-KP', aliases: ['Kuzey Park Binası', 'North Park Building', 'KPARK'] },
  { id: 'B-NORTH-SBU', aliases: ['SineBU', 'Mithat Alam Film Center'] },
  { id: 'B-NORTH-Y34', aliases: ['3. Kuzey Yurdu', '4. Kuzey Yurdu', 'Kuzey Yurtları', 'North Campus Dormitory 3', 'North Campus Dormitory 4'] },
] as const;

type OverpassPoint = { lat: number; lon: number };
type OverpassMember = { role?: string; geometry?: OverpassPoint[] };
type OverpassTags = Record<string, string | undefined> & { name?: string; building?: string };
type OverpassElement = {
  id: number;
  type: 'node' | 'way' | 'relation';
  lat?: number;
  lon?: number;
  center?: { lat: number; lon: number };
  geometry?: OverpassPoint[];
  members?: OverpassMember[];
  tags?: OverpassTags;
};

function normalize(value: string) {
  return value.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i').replace(/[^a-z0-9]/g, '');
}

function escapeRegex(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

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
  if (!element.members?.length) return undefined;
  const outerRings = element.members
    .filter(member => (member.role === 'outer' || !member.role) && member.geometry && member.geometry.length >= 3)
    .map(member => member.geometry as OverpassPoint[])
    .sort((a, b) => ringArea(b) - ringArea(a));
  return outerRings[0];
}

function centroid(footprint?: OverpassPoint[]) {
  if (!footprint?.length) return undefined;
  const total = footprint.reduce((acc, point) => ({ lat: acc.lat + point.lat, lon: acc.lon + point.lon }), { lat: 0, lon: 0 });
  return { lat: total.lat / footprint.length, lon: total.lon / footprint.length };
}

function nameScore(name: string, aliases: readonly string[]) {
  const normalizedName = normalize(name);
  let score = -1;
  for (const alias of aliases) {
    const normalizedAlias = normalize(alias);
    if (normalizedName === normalizedAlias) score = Math.max(score, 100);
    else if (normalizedName.includes(normalizedAlias) || normalizedAlias.includes(normalizedName)) score = Math.max(score, 70);
  }
  return score;
}

function elementScore(element: OverpassElement, aliases: readonly string[]) {
  const name = element.tags?.name;
  if (!name) return -1;
  const score = nameScore(name, aliases);
  if (score < 0) return -1;
  const footprint = extractFootprint(element);
  return score + (footprint ? 35 : 0) + (element.tags?.building ? 20 : 0) + (element.type === 'way' ? 5 : 0);
}

export async function GET() {
  const regex = TARGETS.flatMap(target => [...target.aliases]).map(escapeRegex).join('|');
  const query = `[out:json][timeout:22];nwr(around:2600,41.0850,29.0480)["name"~"${regex}",i];out center tags geom;`;

  try {
    const response = await fetch('https://overpass-api.de/api/interpreter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: new URLSearchParams({ data: query }),
      next: { revalidate: 86400 },
    });
    if (!response.ok) throw new Error(`Overpass ${response.status}`);

    const payload = await response.json() as { elements?: OverpassElement[] };
    const elements = payload.elements ?? [];
    const locations = TARGETS.flatMap(target => {
      const matches = elements
        .map(element => ({ element, score: elementScore(element, target.aliases) }))
        .filter(candidate => candidate.score >= 0)
        .sort((a, b) => b.score - a.score);
      const best = matches[0]?.element;
      if (!best?.tags?.name) return [];

      const footprint = extractFootprint(best);
      const footprintCenter = centroid(footprint);
      const lat = best.lat ?? best.center?.lat ?? footprintCenter?.lat;
      const lon = best.lon ?? best.center?.lon ?? footprintCenter?.lon;
      if (lat == null || lon == null) return [];

      const tags = best.tags ?? {};
      const levels = parsePositiveInt(tags['building:levels']);
      const height = parseMeters(tags.height);
      const roofLevels = parsePositiveInt(tags['roof:levels']);
      const roofHeight = parseMeters(tags['roof:height']);
      const minHeight = parseMeters(tags.min_height);

      return [{
        id: target.id,
        coords: [lat, lon] as [number, number],
        matched_name: best.tags.name,
        source: 'OpenStreetMap',
        osm_url: `https://www.openstreetmap.org/${best.type}/${best.id}`,
        geometry_source: footprint ? 'OSM_FOOTPRINT' : 'OSM_CENTER',
        footprint: footprint?.map(point => [point.lat, point.lon] as [number, number]),
        height_m: height,
        min_height_m: minHeight,
        levels,
        roof_levels: roofLevels,
        roof_height_m: roofHeight,
        roof_shape: tags['roof:shape'],
        building_material: tags['building:material'],
        roof_material: tags['roof:material'],
        building_colour: tags['building:colour'],
        roof_colour: tags['roof:colour'],
        start_date: tags.start_date,
      }];
    });

    return NextResponse.json({
      locations,
      source: 'OpenStreetMap / Overpass',
      fetched_at: new Date().toISOString(),
      degraded: false,
      geometry: 'Named OSM building footprints are returned when available; unmatched records retain repository fallback coordinates.',
    });
  } catch (error) {
    return NextResponse.json({
      locations: [],
      source: 'OpenStreetMap / Overpass',
      fetched_at: new Date().toISOString(),
      degraded: true,
      detail: error instanceof Error ? error.message : 'Location source unavailable',
    });
  }
}
