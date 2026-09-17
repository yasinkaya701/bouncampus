# Active Workstreams

This file is the coordination ledger for parallel agents.

## Hard lifecycle rule

A workstream owner keeps ownership from first edit through merge and post-merge verification. There is no `DONE` state before verified `master`.

Allowed lifecycle states:

- `ACTIVE` — implementation/testing in progress on the agent branch.
- `READY_FOR_INTEGRATION` — branch validation complete, but work is still unmerged and the agent must remain responsible.
- `INTEGRATING` — the same owning agent holds the Merge Coordinator lock and is driving the single PR.
- `MERGED_VERIFYING` — PR merged; the same owning agent is checking the resulting `master` commit.
- `MERGED_VERIFIED` — work exists on verified `master`; only now may ownership be released and the row archived/removed.
- `BLOCKED` — only for a hard external blocker the agent cannot resolve with repository access. This is not completion.

`HANDOFF`, `PR_READY`, `AWAITING_MERGE`, and branch-only `DONE` are invalid terminal states.

## Rules

- Every active workstream must declare a lane, branch, owner role, scope, and touched paths before implementation begins.
- File ownership is exclusive while a workstream is active.
- The agent that accepts a workstream owns implementation, validation, integration, conflict resolution, merge, and post-merge verification.
- The Merge Coordinator is a repository-wide lock acquired temporarily by the ready workstream owner; it is not a separate agent handoff.
- Only the lock holder may own the repository's single open integration PR.
- Other agents may keep implementing non-overlapping work while the lock is occupied, but may not exit or declare success with unmerged accepted work.
- Ownership is released only after the workstream reaches `MERGED_VERIFIED`.
- Remove or archive a row immediately after `MERGED_VERIFIED` so stale ownership does not block future work.

## Active

| State | Lane | Branch | Owner role | Scope | Touched paths |
| --- | --- | --- | --- | --- | --- |
| `READY_FOR_INTEGRATION` | `quality-release` | `agent/quality-release/multi-agent-runtime` | Workstream Agent / temporary Merge Coordinator | Build executable multi-agent coordination, branch-independent inter-agent messaging, ownership validation, handoff/ack/retry semantics and CI enforcement. Branch Agent Coordination run #5 passed. | `.agents/**`, `scripts/agent_bus.py`, `scripts/test_agent_bus.py`, `.github/workflows/agent-coordination.yml`, `.github/feature-registry.json`, `AGENTS.md` |

_Previous `frontend-ux/asset-wow-v2` workstream was merged in PR #12 and verified by successful `master` CI run #186; its stale integration ownership is released. Photogrammetry work from PR #13 is preserved in this branch; its separate ownership cleanup is serialized through the repository's single-PR rule._

## Suggested lanes

- `frontend-ux`: pages, components, styles, accessibility, responsive UI.
- `campus-geo`: campus directory, building locations, geometry, maps, 3D/assets.
- `api-product`: Next.js API routes, product logic, data contracts, live-source adapters.
- `quality-release`: CI, tests, build gates, deployment verification.
- `integration`: temporary lock state used by whichever workstream owner is actively merging.
