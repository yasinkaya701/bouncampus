import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const tscPath = resolve(process.cwd(), 'node_modules/typescript/bin/tsc');
const result = spawnSync(process.execPath, [tscPath, '--noEmit', '--pretty', 'false'], {
  cwd: process.cwd(), env: process.env, encoding: 'utf8',
});
const output = [result.stdout, result.stderr].filter(Boolean).join('\n').trim();
mkdirSync(resolve(process.cwd(), 'public'), { recursive: true });
writeFileSync(resolve(process.cwd(), 'public/typecheck.txt'), output || 'TypeScript reported no diagnostics.', 'utf8');
const matched = output.split(/\r?\n/).some(line => {
  if (!/error TS\d+/.test(line)) return false;
  return !line.includes('src/app/') && !line.includes('src/components/') && !line.includes('src/lib/');
});
console.log(`DIAG_GROUP=other matched=${matched}`);
process.exit(matched ? 1 : 0);
