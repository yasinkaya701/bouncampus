# BOUNCAMPUS Repository Working Policy

## Mandatory multi-agent architecture

BOUNCAMPUS is a multi-agent repository. Parallel work is allowed only when ownership is explicit and integration is serialized.

### Roles

- **Merge Coordinator**: the only role allowed to open the integration pull request into `master`, resolve conflicts, and perform the final merge.
- **Frontend / UX Agent**: UI, accessibility, responsive behavior, visual system, client interactions.
- **Campus Data / Geo Agent**: building metadata, coordinates, geometry, map/3D assets, source provenance.
- **API / Product Agent**: Next.js API routes, backend data contracts, product logic, integrations.
- **Quality / Release Agent**: typecheck, lint, build, backend validation, deployment/release evidence.

An agent may own more than one lane only when the touched file sets do not overlap with another active lane.

## Branch and ownership rules

- `master` is protected by process: normal engineering work MUST NOT be committed directly to `master`.
- Each agent works on a short-lived branch named `agent/<lane>/<task>`.
- Before editing, the agent declares the files/directories it owns for that workstream in `.agents/WORKSTREAMS.md`.
- Two active agents must not edit the same file unless the Merge Coordinator explicitly reassigns ownership.
- Agents do not create independent PRs to `master`.
- Agent branches are handed to the Merge Coordinator after tests and a concrete handoff note are complete.

## One-PR integration rule

BOUNCAMPUS must not accumulate pull requests.

- There may be **at most one open pull request** in the repository.
- That PR is the Merge Coordinator's integration PR targeting `master`.
- Additional agent work remains on branches until the current integration PR is merged or closed.
- The integration PR must be rebased/merged onto the latest `master` before final validation; stale heads are not mergeable.
- A PR is not left open as a parking lot. It must become merge-ready, be merged, or be closed with an explicit blocker/handoff.

## Feature-preservation rule

A merge is invalid if an existing feature, route, data source, UI surface, asset, or validation gate disappears unintentionally.

Before merge, the Merge Coordinator MUST:

1. Start from the latest `master`.
2. Integrate agent branches one at a time.
3. Resolve conflicts manually; never use whole-file `ours`/`theirs` conflict resolution on product files without reviewing both sides.
4. Compare the integration head with `master` and account for every deletion or rename.
5. Update `.github/feature-registry.json` when a new durable feature is introduced.
6. Run `python scripts/verify_feature_preservation.py --base-ref <master-sha>`.
7. Run frontend `npm run typecheck`, `npm run lint`, and `npm run build`.
8. Compile backend Python and validate critical JSON datasets.
9. Merge only after all required CI gates are green.
10. Re-run the release checks on the merged `master` commit.

Existing feature-registry entries may not be removed or weakened in a normal feature PR. Intentional removals require an explicit repository-owner decision documented in the PR.

## Merge semantics

- Merge is mandatory: completed work is not considered delivered while it exists only on an agent branch.
- The Merge Coordinator owns the final conflict resolution and merge commit/squash.
- After a successful merge, merged agent branches should be deleted or treated as disposable.
- No agent may continue dependent work from an unmerged integration branch when the dependency is expected to become repository truth.

## Product truth boundary

BOUNCAMPUS must not present model estimates as live university telemetry. Unless a source is explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT sensor networks.

## Release sequence

1. Agent work completes on owned short-lived branches.
2. Merge Coordinator integrates the work into the single integration PR.
3. Feature-preservation + typecheck + lint + build + repository-data gates pass.
4. Integration PR is merged to `master`.
5. Deploy the `frontend` Next.js application.
6. Validate deployed `/api/v1/health` and core product routes.
7. Refresh the BUIS/ÖBİKAS course snapshot after the 28–30 Sep 2026 add/drop window.

## Bootstrap exception

The commit that introduces this policy may land directly on `master` because the previous repository policy explicitly prohibited PR-based development. After that bootstrap, the mandatory merge workflow above is the repository rule.
