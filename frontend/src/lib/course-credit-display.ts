/** Never synthesize academic credits for records with missing source values. */
export function formatCourseCredit(
  value: number | null | undefined,
  unit: 'CR' | 'ECTS',
): string {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0
    ? `${value} ${unit}`
    : `— ${unit}`;
}
