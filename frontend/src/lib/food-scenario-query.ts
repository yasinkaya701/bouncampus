/** A missing scenario rate uses the policy default; an invalid supplied rate never silently becomes zero. */
export function parseFoodScenarioRate(raw: string | null, defaultPct: number): number | null {
  if (raw === null) return defaultPct;
  const trimmed = raw.trim();
  if (trimmed === '') return null;
  const parsed = Number(trimmed);
  return Number.isFinite(parsed) ? parsed : null;
}
