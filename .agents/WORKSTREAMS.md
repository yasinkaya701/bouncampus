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

| Lane | Branch | Owner role | State | Scope | Touched paths |
| --- | --- | --- | --- | --- | --- |

The `api-product + frontend-ux + quality-release / kreate-winning-v2` workstream was merged through PR #19 and verified on `master` at merge commit `a2fe37c9d3c3507f5f8ae2f56de049707fdbbd1b` by CI run #204 before ownership was released. It delivered readiness-aware food-waste decisions, the operator gate, 14-day falsifiable pilot contract, measurement template, measured pilot scorer, Pilot Evidence Lab, claim firewall, aligned jury/product docs, and repository cleanup.

The `api-product + frontend-ux / food-waste-winning-focus` workstream was merged through PR #17 and verified on `master` at merge commit `573385b7a703ec845021e8fdbfc2546496d70b1b` by CI run #198 before ownership was released.

The `frontend-ux / jury-visual-assets-v3` workstream was merged through PR #15 and verified on `master` at merge commit `a51252e59a6856d7db945ba2d9073defe2645c5e` by CI run #192 before ownership was released.

The `campus-geo / photogrammetry-assets` workstream was merged through PR #13 and verified on `master` at merge commit `4ae611ecf394e3cdf05b21b4eeda0dd998526c54` by CI run #188 before ownership was released.

## Suggested lanes

- `frontend-ux`: pages, components, styles, accessibility, responsive UI.
- `campus-geo`: campus directory, building locations, geometry, maps, 3D/assets.
- `api-product`: Next.js API routes, product logic, data contracts, live-source adapters.
- `quality-release`: CI, tests, build gates, deployment verification.
- `integration`: temporary lock state used by whichever workstream owner is actively merging.
