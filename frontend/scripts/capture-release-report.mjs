import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = process.cwd();
const run = (script, args) => spawnSync(process.execPath, [resolve(root, script), ...args], {
  cwd: root,
  env: process.env,
  encoding: 'utf8',
});

const tsc = run('node_modules/typescript/bin/tsc', ['-p', 'tsconfig.full.json', '--noEmit', '--pretty', 'false']);
const eslint = run('node_modules/eslint/bin/eslint.js', ['src', '--ext', '.ts,.tsx', '--no-ignore', '--format', 'stylish']);

const format = (name, result) => [
  `${name}_exit_code=${result.status ?? 'unknown'}`,
  `${name}_signal=${result.signal ?? 'none'}`,
  '',
  result.stdout || '',
  result.stderr || '',
].join('\n').trim() + '\n';

mkdirSync(resolve(root, 'public'), { recursive: true });
writeFileSync(resolve(root, 'public/typecheck.txt'), format('typecheck', tsc), 'utf8');
writeFileSync(resolve(root, 'public/lint.txt'), format('lint', eslint), 'utf8');
console.log(`release diagnostics captured: typecheck=${tsc.status} lint=${eslint.status}`);
process.exit(0);
