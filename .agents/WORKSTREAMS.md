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
| integration | `agent/integration/kreate-climate-focus` | Merge Coordinator | `frontend/src/app/page.tsx`, `frontend/src/app/demo/page.tsx`, `frontend/src/app/lab/page.tsx`, `frontend/src/components/shared/Header.tsx`, `frontend/src/app/{acoustic,agent-simulation,anomalies,control-room,esg-reports,integrations,iot-registry,league,maintenance,microgrid,rescheduler,solar,student,transit,water}/**`, `docs/pitch.md`, `docs/jury-demo-script.md`, `.agents/WORKSTREAMS.md` | active | KREATE focus pass: preserve 3D/campus geometry, promote occupancy/weather-aware energy-carbon decision flow, remove unfinished/mock-heavy first-class surfaces. |

## Suggested lanes

- `frontend-ux`: pages, components, styles, accessibility, responsive UI.
- `campus-geo`: campus directory, building locations, geometry, maps, 3D/assets.
- `api-product`: API routes, product logic, data contracts, live-source adapters.
- `quality-release`: CI, tests, build gates, deployment verification.
- `integration`: conflict resolution, preservation verification, final PR and merge.
