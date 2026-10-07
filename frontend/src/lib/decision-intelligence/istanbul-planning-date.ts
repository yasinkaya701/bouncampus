/**
 * Strict planning-date interpretation in the campus timezone.
 * A valid ISO-shaped string is not necessarily a real calendar day.
 */
function isRealCalendarDate(value: string): boolean {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (year < 1 || month < 1 || month > 12 || day < 1) return false;
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const daysInMonth = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return day <= daysInMonth[month - 1];
}

export function parseIstanbulPlanningDate(
  supplied: string | null,
  now: Date = new Date(),
): { dateVal: string; weekday: number } | null {
  let dateVal = supplied?.trim() || '';
  if (!dateVal) {
    // Assemble the ISO date from structured parts rather than locale-specific separators.
    const parts = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Istanbul',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).formatToParts(now);
    const year = parts.find(part => part.type === 'year')?.value;
    const month = parts.find(part => part.type === 'month')?.value;
    const day = parts.find(part => part.type === 'day')?.value;
    if (!year || !month || !day) return null;
    dateVal = `${year.padStart(4, '0')}-${month}-${day}`;
  }

  if (!isRealCalendarDate(dateVal)) return null;
  const atNoon = new Date(`${dateVal}T12:00:00+03:00`);
  if (Number.isNaN(atNoon.getTime())) return null;

  // 0 = Monday, 6 = Sunday; 09:00 UTC and 12:00 Istanbul share a calendar day.
  return { dateVal, weekday: (atNoon.getUTCDay() + 6) % 7 };
}
