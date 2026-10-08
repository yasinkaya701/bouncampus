import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const source = readFileSync(
  new URL('../src/app/courses/page.tsx', import.meta.url),
  'utf8',
);
assert.ok(source.includes("aria-label={t('Ders ara', 'Search courses')}"),
  'course search needs a programmatic name beyond placeholder text');
assert.ok(source.includes("aria-label={t('Bölüme göre filtrele', 'Filter by department')}"),
  'department select needs a programmatic name');
assert.ok(source.includes('aria-pressed={selectedCampus === campus}'),
  'campus toggle selection must be exposed to assistive technology');
assert.ok(source.includes("aria-label={t('Önceki sayfa', 'Previous page')}"),
  'icon-only previous-page control needs a name');
assert.ok(source.includes("aria-label={t('Sonraki sayfa', 'Next page')}"),
  'icon-only next-page control needs a name');
assert.ok(source.includes('aria-live="polite"'),
  'pagination changes should be announced without stealing focus');
console.log('course filter and pagination accessibility affordances verified');
