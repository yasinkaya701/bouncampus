import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
const tscPath = resolve(process.cwd(), 'node_modules/typescript/bin/tsc');
const result = spawnSync(process.execPath, [tscPath, '--noEmit', '--pretty', 'false'], { cwd: process.cwd(), env: process.env, encoding: 'utf8' });
const output = [result.stdout, result.stderr].filter(Boolean).join('\n').trim();
const matched = output.split(/\r?\n/).some(line => /src\/components\/Dashboard\/(KPICards|ActionCards|MissionSpotlight|Timeline)\.tsx/.test(line));
console.log(`DIAG_GROUP=dashboard-widgets matched=${matched}`);
process.exit(matched ? 1 : 0);
