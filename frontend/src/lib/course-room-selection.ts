export type CourseCampus = 'south' | 'north';

const BUILDING_MAP: Record<string, { id: string; campus: CourseCampus }> = {
  TB: { id: 'B-SOUTH-TB', campus: 'south' }, İB: { id: 'B-SOUTH-IB', campus: 'south' }, IB: { id: 'B-SOUTH-IB', campus: 'south' },
  M: { id: 'B-SOUTH-M', campus: 'south' }, HH: { id: 'B-SOUTH-HH', campus: 'south' }, JF: { id: 'B-SOUTH-JF', campus: 'south' }, NB: { id: 'B-SOUTH-NB', campus: 'south' },
  KB: { id: 'B-NORTH-KB', campus: 'north' }, NH: { id: 'B-NORTH-NH', campus: 'north' }, BM: { id: 'B-NORTH-BM', campus: 'north' }, EF: { id: 'B-NORTH-EF', campus: 'north' },
  KYD: { id: 'B-NORTH-YD', campus: 'north' }, ET: { id: 'B-NORTH-ETA', campus: 'north' }, KP: { id: 'B-NORTH-KP', campus: 'north' },
};

export function roomBuilding(room?: string) {
  const prefix = room?.trim().match(/^([A-ZÇĞİÖŞÜa-zçğıöşü]+)/)?.[1]?.toUpperCase();
  return prefix ? BUILDING_MAP[prefix] : undefined;
}

/** When a campus filter is active, link to an actual room on that campus. */
export function selectCourseRoom(
  rooms: readonly string[] | undefined,
  campus: 'ALL' | CourseCampus,
): string | undefined {
  if (campus === 'ALL') return rooms?.[0];
  return rooms?.find(room => roomBuilding(room)?.campus === campus) ?? rooms?.[0];
}
