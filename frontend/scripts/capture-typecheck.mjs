import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const tscPath = resolve(process.cwd(), 'node_modules/typescript/bin/tsc');
const result = spawnSync(process.execPath, [tscPath, '--noEmit', '--pretty', 'false'], {
  cwd: process.cwd(),
  env: process.env,
  encoding: 'utf8',
});

const output = [result.stdout, result.stderr]
  .filter(Boolean)
  .join('\n')
  .trim();

const report = [
  `exit_code=${result.status ?? 'unknown'}`,
  `signal=${result.signal ?? 'none'}`,
  '',
  output || 'TypeScript reported no diagnostics.',
  '',
].join('\n');

mkdirSync(resolve(process.cwd(), 'public'), { recursive: true });
writeFileSync(resolve(process.cwd(), 'public/typecheck.txt'), report, 'utf8');

console.log(output || 'TypeScript reported no diagnostics.');
console.log('TypeScript diagnostics written to /typecheck.txt for this preview build.');

// Diagnostic preview only: preserve the report even when tsc reports errors.
process.exit(0);
