import type { Building } from './types';

export type BuildingFootprintLocation = {
  id: string;
  coords: [number, number];
  matched_name: string;
  osm_url: string;
  source: string;
  geometry_source?: 'OSM_FOOTPRINT' | 'OSM_CENTER';
  footprint?: [number, number][];
  height_m?: number;
  min_height_m?: number;
  levels?: number;
  roof_levels?: number;
  roof_height_m?: number;
  roof_shape?: string;
  building_material?: string;
  roof_material?: string;
  building_colour?: string;
  roof_colour?: string;
  start_date?: string;
};

export type BuildingLocationPayload = {
  locations?: BuildingFootprintLocation[];
  source?: string;
  fetched_at?: string;
  degraded?: boolean;
  detail?: string;
};

export type ArchitectureStyle = 'historic-stone' | 'historic-ivy' | 'brutalist' | 'modern' | 'utility';
export type LandmarkFeature = 'clock-tower' | 'arched-center' | 'cantilever-bands' | 'none';

export type BuildingModelProfile = {
  style: ArchitectureStyle;
  facade: number;
  facadeNight: number;
  roof: number;
  window: number;
  trim: number;
  defaultRoofShape: 'flat' | 'hipped' | 'gabled';
  landmark: LandmarkFeature;
};

const PROFILES: Partial<Record<string, BuildingModelProfile>> = {
  'B-SOUTH-TB': { style: 'historic-stone', facade: 0xcfc3ae, facadeNight: 0x4a4038, roof: 0x8b3f32, window: 0x324b58, trim: 0xe7ded0, defaultRoofShape: 'hipped', landmark: 'arched-center' },
  'B-SOUTH-IB': { style: 'historic-stone', facade: 0xc8baa1, facadeNight: 0x463b33, roof: 0x8a3b2f, window: 0x314755, trim: 0xe2d8c7, defaultRoofShape: 'hipped', landmark: 'arched-center' },
  'B-SOUTH-M': { style: 'historic-ivy', facade: 0x6f775d, facadeNight: 0x2f382d, roof: 0x6c3c2e, window: 0x273e4c, trim: 0xb8b69f, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-SOUTH-ALH': { style: 'historic-stone', facade: 0xc8baa4, facadeNight: 0x443a33, roof: 0x8c3c31, window: 0x2f4854, trim: 0xe6dccb, defaultRoofShape: 'hipped', landmark: 'clock-tower' },
  'B-SOUTH-GH': { style: 'historic-stone', facade: 0xc7b9a1, facadeNight: 0x433931, roof: 0x74423a, window: 0x304652, trim: 0xdfd5c5, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-SOUTH-HH': { style: 'historic-stone', facade: 0xc4b79f, facadeNight: 0x443a32, roof: 0x844134, window: 0x314854, trim: 0xe0d6c5, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-SOUTH-OFB': { style: 'historic-stone', facade: 0xc9bda7, facadeNight: 0x443b34, roof: 0x864137, window: 0x314955, trim: 0xe2d8c8, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-SOUTH-NB': { style: 'historic-stone', facade: 0xc5b8a1, facadeNight: 0x433a32, roof: 0x7d4135, window: 0x304753, trim: 0xddd4c4, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-SOUTH-JF': { style: 'historic-stone', facade: 0xc4b79f, facadeNight: 0x433a33, roof: 0x784035, window: 0x304753, trim: 0xddd3c2, defaultRoofShape: 'hipped', landmark: 'none' },
  'B-NORTH-LIB': { style: 'brutalist', facade: 0xb8b5aa, facadeNight: 0x3d4144, roof: 0x8d8b84, window: 0x24495c, trim: 0xd0cdc2, defaultRoofShape: 'flat', landmark: 'cantilever-bands' },
};

const DEFAULT_PROFILE: BuildingModelProfile = {
  style: 'modern',
  facade: 0xc9d0d4,
  facadeNight: 0x33404a,
  roof: 0x646d74,
  window: 0x26566c,
  trim: 0xe2e8eb,
  defaultRoofShape: 'flat',
  landmark: 'none',
};

const UTILITY_PROFILE: BuildingModelProfile = {
  style: 'utility',
  facade: 0xbfc4c5,
  facadeNight: 0x353e43,
  roof: 0x697176,
  window: 0x2b5263,
  trim: 0xe1e5e5,
  defaultRoofShape: 'flat',
  landmark: 'none',
};

export function modelProfileFor(building: Building): BuildingModelProfile {
  const exact = PROFILES[building.id];
  if (exact) return exact;
  if (building.type === 'Dining' || building.type === 'Research') return UTILITY_PROFILE;
  return DEFAULT_PROFILE;
}

export function effectiveLevels(building: Building, location?: BuildingFootprintLocation) {
  return location?.levels ?? Math.max(1, building.floors || 1);
}

export function effectiveHeightMeters(building: Building, location?: BuildingFootprintLocation) {
  if (location?.height_m && location.height_m > 2) return location.height_m;
  const levels = effectiveLevels(building, location);
  const floorHeight = modelProfileFor(building).style === 'historic-stone' ? 3.8 : modelProfileFor(building).style === 'brutalist' ? 3.6 : 3.35;
  return Math.max(4.5, levels * floorHeight);
}

export function roofShapeFor(building: Building, location?: BuildingFootprintLocation) {
  const raw = location?.roof_shape?.toLowerCase();
  if (raw?.includes('gabled')) return 'gabled' as const;
  if (raw?.includes('hipped') || raw?.includes('pyramidal')) return 'hipped' as const;
  if (raw?.includes('flat')) return 'flat' as const;
  return modelProfileFor(building).defaultRoofShape;
}

export function roofHeightMeters(building: Building, location?: BuildingFootprintLocation) {
  if (location?.roof_height_m && location.roof_height_m > 0) return location.roof_height_m;
  const shape = roofShapeFor(building, location);
  if (shape === 'flat') return 0.65;
  return modelProfileFor(building).style === 'historic-stone' ? 3.8 : 2.5;
}

export function isUsableFootprint(location?: BuildingFootprintLocation) {
  return Boolean(location?.footprint && location.footprint.length >= 4);
}
