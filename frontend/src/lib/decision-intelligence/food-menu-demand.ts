export type MenuPopularityDish = {
  name: string;
  popularity_score: number;
};

export type MenuDemandInput = {
  mainDish?: string | null;
  soup?: string | null;
  veganDish?: string | null;
};

export type MenuDemandAdjustment = {
  factor: number;
  popularityScore: number | null;
  matchedWeight: number;
  matchedItems: string[];
  unmatchedItems: string[];
  provenance:
    | 'POLICY_HEURISTIC_CATALOG'
    | 'POLICY_HEURISTIC_NEUTRAL'
    | 'UNAVAILABLE';
  reasonCodes: string[];
};

export const MENU_DEMAND_POLICY = {
  neutralPopularityScore: 0.8,
  minFactor: 0.9,
  maxFactor: 1.12,
  popularityToFactorSlope: 0.8,
  componentWeights: {
    mainDish: 0.6,
    soup: 0.15,
    veganDish: 0.1,
  },
  unobservedComponentWeight: 0.15,
  semantics: 'BOUNDED_POLICY_HEURISTIC_NOT_MEASURED_ELASTICITY' as const,
};

const DEFAULT_CATALOG: MenuPopularityDish[] = [
  { name: 'Köfte', popularity_score: 0.85 },
  { name: 'Mercimek Çorbası', popularity_score: 0.9 },
  { name: 'Nohut', popularity_score: 0.75 },
  { name: 'Kuru Fasulye', popularity_score: 0.75 },
];

const TURKISH_ASCII: Record<string, string> = {
  'ı': 'i',
  'ş': 's',
  'ğ': 'g',
  'ç': 'c',
  'ö': 'o',
  'ü': 'u',
};

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function normalizeName(value: unknown) {
  return String(value ?? '')
    .trim()
    .toLocaleLowerCase('tr-TR')
    .split('')
    .map(char => TURKISH_ASCII[char] ?? char)
    .join('')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');
}

function catalogEntries(catalog: readonly MenuPopularityDish[]) {
  return catalog
    .map(dish => ({
      normalized: normalizeName(dish.name),
      score: Number(dish.popularity_score),
    }))
    .filter(entry => entry.normalized && Number.isFinite(entry.score))
    .map(entry => ({ ...entry, score: clamp(entry.score, 0, 1) }));
}

function matchScore(
  value: string,
  entries: ReturnType<typeof catalogEntries>,
): number | null {
  const needle = normalizeName(value);
  if (!needle) return null;

  const exact = entries.find(entry => entry.normalized === needle);
  if (exact) return exact.score;

  const partial = entries
    .filter(entry => entry.normalized.length >= 4)
    .filter(entry => entry.normalized.includes(needle) || needle.includes(entry.normalized))
    .sort((a, b) => b.normalized.length - a.normalized.length)[0];
  return partial?.score ?? null;
}

export function buildMenuDemandAdjustment(
  menu: MenuDemandInput,
  verifiedOfficialMenu: boolean,
  catalog: readonly MenuPopularityDish[] = DEFAULT_CATALOG,
): MenuDemandAdjustment {
  if (!verifiedOfficialMenu) {
    return {
      factor: 1,
      popularityScore: null,
      matchedWeight: 0,
      matchedItems: [],
      unmatchedItems: [],
      provenance: 'UNAVAILABLE',
      reasonCodes: ['MENU_SOURCE_NOT_VERIFIED_LIVE'],
    };
  }

  const entries = catalogEntries(catalog);
  const components = [
    { value: menu.mainDish, weight: MENU_DEMAND_POLICY.componentWeights.mainDish },
    { value: menu.soup, weight: MENU_DEMAND_POLICY.componentWeights.soup },
    { value: menu.veganDish, weight: MENU_DEMAND_POLICY.componentWeights.veganDish },
  ];

  let weightedScore = MENU_DEMAND_POLICY.neutralPopularityScore
    * MENU_DEMAND_POLICY.unobservedComponentWeight;
  let matchedWeight = 0;
  let presentWeight = MENU_DEMAND_POLICY.unobservedComponentWeight;
  const matchedItems: string[] = [];
  const unmatchedItems: string[] = [];

  for (const component of components) {
    if (!component.value) continue;
    presentWeight += component.weight;
    const score = matchScore(component.value, entries);
    if (score == null) {
      weightedScore += MENU_DEMAND_POLICY.neutralPopularityScore * component.weight;
      unmatchedItems.push(component.value);
    } else {
      weightedScore += score * component.weight;
      matchedWeight += component.weight;
      matchedItems.push(component.value);
    }
  }

  const missingWeight = Math.max(0, 1 - presentWeight);
  weightedScore += MENU_DEMAND_POLICY.neutralPopularityScore * missingWeight;

  if (matchedWeight <= 0) {
    return {
      factor: 1,
      popularityScore: Number(weightedScore.toFixed(4)),
      matchedWeight: 0,
      matchedItems,
      unmatchedItems,
      provenance: 'POLICY_HEURISTIC_NEUTRAL',
      reasonCodes: ['NO_MATCHED_MENU_POPULARITY_SIGNAL'],
    };
  }

  const factor = clamp(
    1 + (weightedScore - MENU_DEMAND_POLICY.neutralPopularityScore)
      * MENU_DEMAND_POLICY.popularityToFactorSlope,
    MENU_DEMAND_POLICY.minFactor,
    MENU_DEMAND_POLICY.maxFactor,
  );

  return {
    factor: Number(factor.toFixed(4)),
    popularityScore: Number(weightedScore.toFixed(4)),
    matchedWeight: Number(matchedWeight.toFixed(4)),
    matchedItems,
    unmatchedItems,
    provenance: 'POLICY_HEURISTIC_CATALOG',
    reasonCodes: ['MENU_POPULARITY_HEURISTIC_APPLIED'],
  };
}

export function applyMenuDemandAdjustment(baselineDemand: number, factor: number) {
  if (!Number.isFinite(baselineDemand) || baselineDemand <= 0) return 0;
  const safeFactor = Number.isFinite(factor)
    ? clamp(factor, MENU_DEMAND_POLICY.minFactor, MENU_DEMAND_POLICY.maxFactor)
    : 1;
  return Math.max(0, Math.round(baselineDemand * safeFactor));
}
