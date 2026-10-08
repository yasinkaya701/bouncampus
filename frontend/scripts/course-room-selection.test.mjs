import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { roomBuilding, selectCourseRoom } from '../src/lib/course-room-selection.ts';

const catalog = JSON.parse(readFileSync(
  new URL('../src/data/real_boun_courses.json', import.meta.url),
  'utf8',
));
const courses = Object.values(catalog);
const mixedCampus = courses.filter(course => {
  const campuses = new Set((course.rooms ?? []).map(room => roomBuilding(room)?.campus).filter(Boolean));
  return campuses.size === 2;
});
assert.ok(mixedCampus.length > 0, 'source catalog must contain cross-campus courses for regression');

for (const course of mixedCampus) {
  assert.equal(roomBuilding(selectCourseRoom(course.rooms, 'south'))?.campus, 'south',
    `${course.code}: south filter must link to a south-campus room`);
  assert.equal(roomBuilding(selectCourseRoom(course.rooms, 'north'))?.campus, 'north',
    `${course.code}: north filter must link to a north-campus room`);
  assert.equal(selectCourseRoom(course.rooms, 'ALL'), course.rooms[0],
    'unfiltered view must preserve first-room linking');
}
assert.equal(selectCourseRoom([], 'north'), undefined, 'missing rooms stay unavailable');
assert.equal(selectCourseRoom(['Unknown room'], 'north'), 'Unknown room',
  'unknown building cannot be fabricated as a matching campus location');

console.log(`course building-link selection passed (${mixedCampus.length} cross-campus records)`);
