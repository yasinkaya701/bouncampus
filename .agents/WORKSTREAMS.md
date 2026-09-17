# Active Workstreams

This file is the coordination ledger for parallel agents.

## Rules

- Every active workstream must declare a lane, branch, owner role, scope, and touched paths before implementation begins.
- File ownership is exclusive while a workstream is active.
- Agents may commit to their own branch, but only the Merge Coordinator opens the repository's single integration PR.
- Completed work is not repository truth until that integration PR is merged to `master`.
- Remove or archive completed rows immediately after merge so stale ownership does not block future work.

## Active

| Lane | Branch | Owner role | Paths owned | Status | Handoff |
| --- | --- | --- | --- | --- | --- |
| integration | `master` bootstrap only | Merge Coordinator | `AGENTS.md`, `.agents/**`, `.github/**`, `scripts/verify_feature_preservation.py` | bootstrapping | Replace this row with the first real integration workstream after this policy lands. |

## Suggested lanes

- `frontend-ux`: pages, components, styles, accessibility, responsive UI.
- `campus-geo`: campus directory, building locations, geometry, maps, 3D/assets.
- `api-product`: API routes, product logic, data contracts, live-source adapters.
- `quality-release`: CI, tests, build gates, deployment verification.
- `integration`: conflict resolution, preservation verification, final PR and merge.
