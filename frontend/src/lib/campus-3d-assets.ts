export type Campus3DAssetMode = 'runtime-derived' | 'embed-only';
export type Campus3DAssetQuality = 'source-backed-footprint' | 'photogrammetry-reference';

export type Campus3DAsset = {
  id: string;
  title: string;
  campus: readonly string[];
  provider: 'OpenStreetMap' | 'Sketchfab';
  author: string;
  quality: Campus3DAssetQuality;
  mode: Campus3DAssetMode;
  sourceUrl: string;
  embedUrl?: string;
  modelUid?: string;
  license: string;
  attribution: string;
  redistribution: 'allowed-with-odbl' | 'not-checked-in-license-unverified';
  notes: string;
};

const sketchfabAsset = (
  id: string,
  title: string,
  campus: readonly string[],
  modelUid: string,
  notes: string,
): Campus3DAsset => ({
  id,
  title,
  campus,
  provider: 'Sketchfab',
  author: 'Havadan Harita / Buğrahan Yeni',
  quality: 'photogrammetry-reference',
  mode: 'embed-only',
  modelUid,
  sourceUrl: `https://sketchfab.com/models/${modelUid}`,
  embedUrl: `https://sketchfab.com/models/${modelUid}/embed?autostart=0&ui_infos=0&ui_watermark=1&ui_controls=1`,
  license: 'Redistribution license not verified by BOUNCAMPUS',
  attribution: '3D model: Havadan Harita / Buğrahan Yeni — hosted by Sketchfab',
  redistribution: 'not-checked-in-license-unverified',
  notes,
});

export const CAMPUS_3D_ASSETS: readonly Campus3DAsset[] = [
  {
    id: 'osm-campus-buildings',
    title: 'Boğaziçi campus building footprints',
    campus: ['south', 'north', 'hisar', 'ucaksavar', 'kandilli', 'anadolu', 'kilyos'],
    provider: 'OpenStreetMap',
    author: 'OpenStreetMap contributors',
    quality: 'source-backed-footprint',
    mode: 'runtime-derived',
    sourceUrl: 'https://www.openstreetmap.org/copyright',
    license: 'ODbL-1.0',
    attribution: '© OpenStreetMap contributors',
    redistribution: 'allowed-with-odbl',
    notes: 'Building footprints, tagged heights/levels, roof metadata and materials are fetched through the repository Overpass adapter. Missing heights are explicitly marked as visualization estimates.',
  },
  sketchfabAsset(
    'sketchfab-north-campus-1-5',
    '1–2–3–4–5 Boğaziçi University North Campus',
    ['north'],
    '7ee0a7f38d434c519be728a3ab493722',
    'High-detail external photogrammetry reference for the North Campus building cluster.',
  ),
  sketchfabAsset(
    'sketchfab-north-campus-dorms-6-7',
    '6–7 Boğaziçi University North Campus Dormitories',
    ['north'],
    'd153dab298bd472787c6896063f9a9b7',
    'High-detail external photogrammetry reference for the North Campus dormitory cluster.',
  ),
  sketchfabAsset(
    'sketchfab-ucaksavar-superdorm-kss',
    'Boğaziçi University Uçaksavar Campus — Superdorm / KSS',
    ['ucaksavar'],
    '58f91e285e0c4a4dafff412ccc553ecf',
    'External photogrammetry reference for Uçaksavar Campus and Superdorm/KSS context.',
  ),
  sketchfabAsset(
    'sketchfab-kandilli-new-geophysics',
    'Boğaziçi University Kandilli — New Geophysics Building',
    ['kandilli'],
    '364f2ef47974416baa046626efae4fa0',
    'External photogrammetry reference for the Kandilli campus New Geophysics building.',
  ),
  sketchfabAsset(
    'sketchfab-kilyos-dormitory',
    'Boğaziçi University Kilyos Campus — Dormitory Building',
    ['kilyos'],
    '39aa2add49de4877bedf68e7d618e097',
    'External 3D scan referenced by a Turkish Ministry seismic-resilience / energy-efficiency project document.',
  ),
  sketchfabAsset(
    'sketchfab-anadolu-hisari-pool',
    'Boğaziçi University Anadolu Hisarı Campus — Indoor Pool',
    ['anadolu'],
    'bc509269e0c747deb58b4a7b369fba0b',
    'External photogrammetry reference for the Anadolu Hisarı indoor pool building.',
  ),
] as const;

export const EMBEDDABLE_CAMPUS_3D_ASSETS = CAMPUS_3D_ASSETS.filter(
  (asset): asset is Campus3DAsset & { embedUrl: string; modelUid: string } => Boolean(asset.embedUrl && asset.modelUid),
);

export function assetsForCampus(campus: string) {
  return CAMPUS_3D_ASSETS.filter(asset => asset.campus.includes(campus));
}
