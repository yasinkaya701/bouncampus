export type FoodWasteMonth = {
  month: string;
  monthTr: string;
  wasteKg: number;
  recoveredKg: number;
  wasteOilKg: number;
};

export type FoodWasteScenario = {
  preventionRatePct: number;
  recoveryRatePct: number;
  preventedKg: number;
  remainingWasteKg: number;
  recoveredKg: number;
  residualKg: number;
  residualReductionKg: number;
};

export const FOOD_WASTE_SOURCE = {
  title: 'Boğaziçi University — Campus food waste tracking',
  url: 'https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310',
  provenance: 'OFFICIAL_PUBLIC' as const,
};

export const SKS_ACTIVITY_SOURCE = {
  title: 'Boğaziçi University SKS — Faaliyet Raporu',
  url: 'https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096',
  provenance: 'OFFICIAL_PUBLIC' as const,
};

export const FOOD_WASTE_2025: FoodWasteMonth[] = [
  { month: 'Jan', monthTr: 'Oca', wasteKg: 3992, recoveredKg: 2250, wasteOilKg: 475 },
  { month: 'Feb', monthTr: 'Şub', wasteKg: 7811, recoveredKg: 1555, wasteOilKg: 250 },
  { month: 'Mar', monthTr: 'Mar', wasteKg: 7004, recoveredKg: 2285, wasteOilKg: 900 },
  { month: 'Apr', monthTr: 'Nis', wasteKg: 4772, recoveredKg: 3090, wasteOilKg: 825 },
  { month: 'May', monthTr: 'May', wasteKg: 3832, recoveredKg: 2900, wasteOilKg: 450 },
  { month: 'Jun', monthTr: 'Haz', wasteKg: 2777, recoveredKg: 1450, wasteOilKg: 550 },
  { month: 'Jul', monthTr: 'Tem', wasteKg: 1923, recoveredKg: 1850, wasteOilKg: 150 },
  { month: 'Aug', monthTr: 'Ağu', wasteKg: 1502, recoveredKg: 3550, wasteOilKg: 350 },
  { month: 'Sep', monthTr: 'Eyl', wasteKg: 2072, recoveredKg: 1450, wasteOilKg: 830 },
  { month: 'Oct', monthTr: 'Eki', wasteKg: 1334, recoveredKg: 4850, wasteOilKg: 600 },
  { month: 'Nov', monthTr: 'Kas', wasteKg: 4784, recoveredKg: 3300, wasteOilKg: 550 },
  { month: 'Dec', monthTr: 'Ara', wasteKg: 6448, recoveredKg: 4900, wasteOilKg: 375 },
];

export const FOOD_WASTE_BASELINE = {
  year2024WasteKg: 50993,
  year2025WasteKg: 48251,
  year2025RecoveredKg: 33430,
  year2025WasteOilKg: 6305,
  communityStudents: 13000,
  communityStaff: 2000,
  diningHallCapacity: 1734,
  campusesWithDining: 6,
};

export const CURRENT_RECOVERY_RATE_PCT =
  (FOOD_WASTE_BASELINE.year2025RecoveredKg / FOOD_WASTE_BASELINE.year2025WasteKg) * 100;

export const YEAR_OVER_YEAR_REDUCTION_PCT =
  ((FOOD_WASTE_BASELINE.year2024WasteKg - FOOD_WASTE_BASELINE.year2025WasteKg) /
    FOOD_WASTE_BASELINE.year2024WasteKg) *
  100;

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

export function simulateFoodWasteScenario(
  preventionRatePct: number,
  recoveryRatePct: number,
): FoodWasteScenario {
  const prevention = clamp(preventionRatePct, 0, 60);
  const recovery = clamp(recoveryRatePct, 0, 100);
  const baseline = FOOD_WASTE_BASELINE.year2025WasteKg;
  const preventedKg = baseline * (prevention / 100);
  const remainingWasteKg = Math.max(0, baseline - preventedKg);
  const recoveredKg = remainingWasteKg * (recovery / 100);
  const residualKg = Math.max(0, remainingWasteKg - recoveredKg);
  const baselineResidual = baseline - FOOD_WASTE_BASELINE.year2025RecoveredKg;

  return {
    preventionRatePct: prevention,
    recoveryRatePct: recovery,
    preventedKg: Math.round(preventedKg),
    remainingWasteKg: Math.round(remainingWasteKg),
    recoveredKg: Math.round(recoveredKg),
    residualKg: Math.round(residualKg),
    residualReductionKg: Math.round(Math.max(0, baselineResidual - residualKg)),
  };
}

export function buildProductionBand(predictedMeals: number) {
  const demand = Math.max(0, Math.round(predictedMeals));
  if (!demand) return null;

  // Deliberately conservative: this is a planning band, not a claim about actual production.
  // The band should be calibrated against measured produced/served/leftover data in a pilot.
  return {
    predictedMeals: demand,
    lowerBound: Math.max(0, Math.round(demand * 0.97)),
    upperBound: Math.round(demand * 1.05),
    provenance: 'MODEL_ESTIMATE' as const,
  };
}
