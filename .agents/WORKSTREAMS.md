# Active Workstreams

This file is the human-readable coordination overview for parallel agents. The machine-readable source of truth for active ownership is `.agents/tasks/**`, managed through `scripts/agent_bus.py`.

## Hard lifecycle rule

A workstream owner keeps ownership from first edit through merge and post-merge verification. There is no `DONE` state before verified `master`.

Allowed lifecycle states:

- `ACTIVE` — implementation/testing in progress on the agent branch.
- `READY_FOR_INTEGRATION` — branch validation complete, but work is still unmerged and the agent must remain responsible.
- `INTEGRATING` — the same owning agent holds the Merge Coordinator lock and is driving the single PR.
- `MERGED_VERIFYING` — PR merged; the same owning agent is checking the resulting `master` commit.
- `MERGED_VERIFIED` — work exists on verified `master`; only now may ownership be released.
- `BLOCKED` — only for a hard external blocker the agent cannot resolve with repository access. This is not completion.

`HANDOFF`, `PR_READY`, `AWAITING_MERGE`, and branch-only `DONE` are invalid terminal states.

## Machine-readable runtime

Use the agent bus instead of manually editing this file to establish ownership:

```bash
python scripts/agent_bus.py claim --task-id <id> --agent <agent> --lane <lane> --branch agent/<lane>/<task> --scope "<scope>" --paths <path...>
python scripts/agent_bus.py heartbeat --task-id <id> --agent <agent>
python scripts/agent_bus.py inbox --agent <agent> --unread-only
python scripts/agent_bus.py validate
```

See `.agents/PROTOCOL.md` for messaging, handoff, blocker, integration-lock, merge, and verification commands.

## Rules

- Every active workstream must declare a lane, branch, owner, scope, and touched paths with `agent_bus.py claim` before implementation begins.
- File ownership is exclusive while a workstream is active; parent/child path overlaps count as conflicts.
- The agent that accepts a workstream owns implementation, validation, integration, conflict resolution, merge, and post-merge verification.
- The Merge Coordinator is a repository-wide lock acquired temporarily by the ready workstream owner; it is not a separate agent handoff.
- Only the lock holder may own the repository's single open integration PR.
- Other agents may keep implementing non-overlapping work while the lock is occupied, but may not exit or declare success with unmerged accepted work.
- Ownership is released only after the workstream reaches `MERGED_VERIFIED`.
- Cross-agent dependencies and decisions must be sent through `.agents/messages/**` via `agent_bus.py send` when they affect another lane's work.
- Stale ownership must be explicitly reassigned; an expired lease does not authorize silent overwrite.

## Active

Run `python scripts/agent_bus.py validate` and inspect `.agents/tasks/**` for authoritative active state.

_No persistent active workstreams are committed at bootstrap._

## Suggested lanes

- `frontend-ux`: pages, components, styles, accessibility, responsive UI.
- `campus-geo`: campus directory, building locations, geometry, maps, 3D/assets.
- `api-product`: Next.js API routes, product logic, data contracts, live-source adapters.
- `quality-release`: CI, tests, build gates, deployment verification.
- `integration`: temporary lock state used by whichever workstream owner is actively merging.
