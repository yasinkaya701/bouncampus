# Agent Coordination Task Store

This directory exists only on the long-lived `agent-coordination` control branch.

- One JSON file = one autonomous task/lease.
- Use `.agents/TASK_TEMPLATE.json` from `master` as the schema source.
- Claims and heartbeats update only the corresponding task file and must use the current blob SHA.
- Do not place product code, application evidence, secrets, binaries, or release artifacts on this branch.
- Product changes still execute on short-lived `agent/<lane>/<task>` branches and integrate through the repository's single PR slot.
- Human involvement is exception-only under the gate kinds defined in `AGENTS.md` and `.agents/FABRIC.md`.

The task store begins empty except for explicit real blockers/critical human gates. Do not create fake example tasks.
