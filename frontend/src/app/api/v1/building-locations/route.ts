import { NextResponse } from 'next/server';

const TARGETS = [
  { id: 'B-SOUTH-TB', aliases: ['Anderson Hall', 'Fen-Edebiyat Binası'] },
  { id: 'B-SOUTH-IB', aliases: ['Washburn Hall', 'İdari Bilimler Binası'] },
  { id: 'B-SOUTH-M', aliases: ['Perkins Hall', 'Mühendislik Binası'] },
  { id: 'B-SOUTH-ALH', aliases: ['Albert Long Hall'] },
  { id: 'B-SOUTH-GH', aliases: ['Gates Hall', 'Genel İdare Binası'] },
  { id: 'B-SOUTH-HH', aliases: ['Hamlin Hall'] },
  { id: 'B-SOUTH-OFB', aliases: ['Öğrenci Faaliyetleri Binası', 'Student Activities Building', 'Henrietta Washburn Hall'] },
  { id: 'B-SOUTH-NB', aliases: ['Natuk Birkan', 'Natuk Birkan Binası'] },
  { id: 'B-SOUTH-JF', aliases: ['John Freely', 'John Freely Binası', 'John Freely Hall'] },
  { id: 'B-SOUTH-GY', aliases: ['Güney Yemekhanesi', 'Güney Kampüs Yemekhanesi'] },
  { id: 'B-NORTH-KB', aliases: ['Kare Blok', 'Kare Bina', 'Fen ve Mühendislik Binası'] },
  { id: 'B-NORTH-NH', aliases: ['New Hall', 'Yeni Bina'] },
  { id: 'B-NORTH-LIB', aliases: ['Aptullah Kuran Kütüphanesi', 'Aptullah Kuran Library'] },
  { id: 'B-NORTH-KY', aliases: ['Kuzey Yemekhanesi', 'Kuzey Kampüs Yemekhanesi'] },
  { id: 'B-NORTH-BM', aliases: ['Bilgisayar Mühendisliği Binası', 'Computer Engineering Building', 'ETA A Blok', 'ETA-A'] },
  { id: 'B-NORTH-EF', aliases: ['Eğitim Fakültesi', 'Faculty of Education'] },
  { id: 'B-NORTH-YD', aliases: ['YADYOK II', 'Kuzey YADYOK', 'School of Foreign Languages'] },
  { id: 'B-NORTH-ETA', aliases: ['ETA B Blok', 'ETA-B', 'ETA-B Blok'] },
  { id: 'B-NORTH-KP', aliases: ['Kuzey Park Binası', 'North Park Building'] },
  { id: 'B-NORTH-SBU', aliases: ['SineBU'] },
  { id: 'B-NORTH-Y34', aliases: ['3. Kuzey Yurdu', '4. Kuzey Yurdu', 'Kuzey Yurtları'] },
] as const;

type OverpassElement = {
  id: number;
  type: 'node' | 'way' | 'relation';
  lat?: number;
  lon?: number;
  center?: { lat: number; lon: number };
  tags?: { name?: string };
};

function normalize(value: string) {
  return value.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i').replace(/[^a-z0-9]/g, '');
}

function escapeRegex(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export async function GET() {
  const regex = TARGETS.flatMap(target => [...target.aliases]).map(escapeRegex).join('|');
  const query = `[out:json][timeout:18];nwr(around:2600,41.0850,29.0480)["name"~"${regex}",i];out center tags;`;

  try {
    const response = await fetch('https://overpass-api.de/api/interpreter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: new URLSearchParams({ data: query }),
      next: { revalidate: 86400 },
    });
    if (!response.ok) throw new Error(`Overpass ${response.status}`);

    const payload = await response.json() as { elements?: OverpassElement[] };
    const used = new Set<string>();
    const locations = (payload.elements ?? []).flatMap(element => {
      const name = element.tags?.name;
      const lat = element.lat ?? element.center?.lat;
      const lon = element.lon ?? element.center?.lon;
      if (!name || lat == null || lon == null) return [];
      const normalizedName = normalize(name);
      const target = TARGETS.find(candidate => !used.has(candidate.id) && candidate.aliases.some(alias => {
        const normalizedAlias = normalize(alias);
        return normalizedName === normalizedAlias || normalizedName.includes(normalizedAlias) || normalizedAlias.includes(normalizedName);
      }));
      if (!target) return [];
      used.add(target.id);
      return [{ id: target.id, coords: [lat, lon] as [number, number], matched_name: name, source: 'OpenStreetMap', osm_url: `https://www.openstreetmap.org/${element.type}/${element.id}` }];
    });

    return NextResponse.json({ locations, source: 'OpenStreetMap / Overpass', fetched_at: new Date().toISOString(), degraded: false });
  } catch (error) {
    return NextResponse.json({ locations: [], source: 'OpenStreetMap / Overpass', fetched_at: new Date().toISOString(), degraded: true, detail: error instanceof Error ? error.message : 'Location source unavailable' });
  }
}
