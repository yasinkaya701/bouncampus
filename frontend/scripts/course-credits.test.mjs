import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { formatCourseCredit } from '../src/lib/course-credit-display.ts';

const catalog = JSON.parse(readFileSync(
  new URL('../src/data/real_boun_courses.json', import.meta.url),
  'utf8',
));
const courses = Object.values(catalog);
const missingEcts = courses.filter(course => course.ects == null);
const missingCredits = courses.filter(course => course.credits == null);

assert.ok(missingEcts.length > 0, 'catalog should contain missing ECTS values for regression coverage');
assert.ok(missingCredits.length > 0, 'catalog should contain missing credit values for regression coverage');
assert.equal(formatCourseCredit(missingEcts[0].ects, 'ECTS'), '— ECTS',
  'missing ECTS cannot silently become five credits');
assert.equal(formatCourseCredit(missingCredits[0].credits, 'CR'), '— CR',
  'missing course credits must remain visibly unknown');
assert.equal(formatCourseCredit(0, 'ECTS'), '0 ECTS', 'recorded zero is not missing');
assert.equal(formatCourseCredit(4.5, 'ECTS'), '4.5 ECTS');
assert.equal(formatCourseCredit(Number.NaN, 'ECTS'), '— ECTS');
assert.equal(formatCourseCredit(-1, 'CR'), '— CR');
assert.equal(formatCourseCredit(Number.POSITIVE_INFINITY, 'CR'), '— CR');
console.log(`course credit display source-truth passed (${missingEcts.length} missing ECTS, ${missingCredits.length} missing CR)`);
