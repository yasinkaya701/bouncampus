import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const header = readFileSync(resolve(here, '../src/components/shared/Header.tsx'), 'utf8');

assert.match(header, /href:\s*['"]\/campus-ops\/shuttle-frequency['"]/);
assert.match(header, /Mekik planı/);
assert.match(header, /Shuttle plan/);
assert.match(header, /function isNavActive\(/);
assert.match(header, /href === ['"]\/campus-ops['"]\) return pathname === ['"]\/campus-ops['"]/);

console.log('shuttle navigation tests passed');
