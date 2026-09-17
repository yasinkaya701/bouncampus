# BOUNCAMPUS Repository Working Policy

## Mandatory multi-agent architecture

BOUNCAMPUS is a multi-agent repository. Parallel work is allowed only when ownership is explicit and integration is serialized.

### Roles

- **Workstream Agent**: owns an assigned lane end-to-end: implementation, tests, integration, merge, and post-merge verification.
- **Merge Coordinator lock**: not a separate handoff role. The workstream agent whose batch is ready acquires the repository's single integration slot and becomes the temporary Merge Coordinator for that batch.
- **Frontend / UX lane**: UI, accessibility, responsive behavior, visual system, client interactions.
- **Campus Data / Geo lane**: building metadata, coordinates, geometry, map/3D assets, source provenance.
- **API / Product lane**: Next.js API routes, backend data contracts, product logic, integrations.
- **Quality / Release lane**: typecheck, lint, build, backend validation, deployment/release evidence.

An agent may own more than one lane only when the touched file sets do not overlap with another active lane.

## Machine-readable coordination runtime

All agents MUST use `scripts/agent_bus.py` and `.agents/PROTOCOL.md` for task ownership and inter-agent communication. Chat context alone is not an ownership record.

Before the first product edit, the agent MUST `claim` the workstream with its agent id, lane, branch, scope, and exact owned paths. The claim is rejected when it overlaps another active workstream. During work, the owner renews its heartbeat/lease and communicates dependencies through durable `REQUEST`, `DECISION`, `BLOCKER`, `HANDOFF`, `REVIEW`, or `INFO` messages.

Runtime state is intentionally split across `.agents/tasks/**`, `.agents/leases/**`, `.agents/heartbeats/**`, `.agents/messages/**`, `.agents/acks/**`, and `.agents/locks/**` so parallel agents do not contend on one shared state file. `.agents/WORKSTREAMS.md` is a human-readable overview; the machine-readable task records are the source of truth for active ownership.

A handoff is allowed only while implementation is `ACTIVE` or `BLOCKED`. Work in `READY_FOR_INTEGRATION`, `INTEGRATING`, or `MERGED_VERIFYING` may not be handed to a separate merge agent. A stale owner may be reassigned only through an explicit recorded reassignment with a reason; expiration is evidence of staleness, not silent permission to overwrite owned paths.

Before an agent reports completion, the runtime lifecycle must reach `MERGED_VERIFIED`. `python scripts/agent_bus.py validate` is a required CI gate and rejects invalid states, overlapping ownership, malformed messages, and inconsistent merge-lock state.

## HARD EXIT CONTRACT — MERGE BEFORE EXIT

**An agent MUST NOT finish, report success, relinquish ownership, or exit while its accepted work exists only on an agent branch or open PR.**

For every workstream an agent accepts, the same agent MUST continue until all of the following are true:

1. implementation is complete on its short-lived branch;
2. targeted validation passes;
3. the agent acquires the single Merge Coordinator lock;
4. its branch is updated with the latest `master`;
5. feature-preservation checks pass;
6. the repository's single integration PR is opened or updated by that same agent;
7. all PR CI checks pass on the exact head SHA;
8. the same agent resolves every merge conflict and CI failure caused by the batch;
9. the same agent performs the merge into `master`;
10. the merged `master` commit is verified with the required post-merge checks;
11. only then may the workstream be marked complete and ownership released.

`PR opened`, `PR ready`, `tests green on branch`, `handoff written`, or `awaiting merge` are **not completion states**.

If merge is blocked by conflicts, stale base, failing CI, or integration regressions, the agent keeps working on the same workstream and fixes them. It may not stop merely because integration became difficult.

The only permitted non-merged exit is a **hard external blocker** that the agent cannot resolve with repository access, such as unavailable credentials/permissions, an unavailable required external service, or an explicit repository-owner decision. In that case the workstream remains `BLOCKED`, never `DONE`, and must contain exact blocker evidence and the next executable action.

## Branch and ownership rules

- `master` is protected by process: normal engineering work MUST NOT be committed directly to `master`.
- Each agent works on a short-lived branch named `agent/<lane>/<task>`.
- Before editing, the agent claims the files/directories it owns with `python scripts/agent_bus.py claim ...`; `.agents/WORKSTREAMS.md` may mirror the state for humans but does not replace the claim.
- Two active agents must not edit the same file unless ownership is explicitly reassigned.
- An agent does not hand completed code to another agent just to perform the merge. The owning agent acquires the Merge Coordinator lock and performs its own integration.
- Ownership remains active until the work is merged to `master` and post-merge verification passes.

## One-PR integration rule

BOUNCAMPUS must not accumulate pull requests.

- There may be **at most one open pull request** in the repository.
- That PR is the current Merge Coordinator lock holder's integration PR targeting `master`.
- Other agents may continue non-overlapping implementation on their branches, but they may not mark their work complete or exit with unmerged accepted work.
- When the integration slot becomes free, the next ready workstream agent rebases/merges latest `master`, acquires the lock, integrates its batch, and merges it.
- The integration PR must contain the latest `master` before final validation; stale heads are not mergeable.
- A PR is never a parking lot. The owning agent keeps driving it until merged or until a genuine hard external blocker is documented.

## Feature-preservation rule

A merge is invalid if an existing feature, route, data source, UI surface, asset, or validation gate disappears unintentionally.

Before merge, the owning agent acting as Merge Coordinator MUST:

1. Start from the latest `master`.
2. Integrate included work one branch at a time when the batch contains multiple compatible workstreams.
3. Resolve conflicts manually; never use whole-file `ours`/`theirs` conflict resolution on product files without reviewing both sides.
4. Compare the integration head with `master` and account for every deletion or rename.
5. Update `.github/feature-registry.json` when a new durable feature is introduced.
6. Run `python scripts/verify_feature_preservation.py --base-ref <master-sha>`.
7. Run `python scripts/agent_bus.py validate`.
8. Run frontend `npm run typecheck`, `npm run lint`, and `npm run build`.
9. Compile backend Python and validate critical JSON datasets.
10. Merge only after all required CI gates are green.
11. Re-run the release checks on the merged `master` commit.
12. Run `python scripts/agent_exit_gate.py --branch-head <merged-agent-head>` and require it to pass before declaring completion.

Existing feature-registry entries may not be removed or weakened in a normal feature PR. Intentional removals require an explicit repository-owner decision documented in the PR.

## Merge semantics

- **Merge is mandatory and owned by the agent that accepted the work.**
- Completed work is not considered delivered while it exists only on a branch or PR.
- Use a normal merge commit for agent integration so the merged agent head remains an ancestor of `master` and can be verified by the exit gate.
- The owning agent performs final conflict resolution and the merge after acquiring the Merge Coordinator lock.
- After successful merge and post-merge verification, merged agent branches are disposable and should be deleted when practical.
- No agent may report `DONE` for work that is not present on verified `master`.

## Product truth boundary

BOUNCAMPUS must not present model estimates as live university telemetry. Unless a source is explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT sensor networks.

## Release sequence

1. Workstream agent claims its task/path scope in the agent bus and implements on its owned short-lived branch.
2. The same agent validates the branch and updates it with latest `master`.
3. The same agent marks the task `READY_FOR_INTEGRATION`, acquires the single Merge Coordinator lock, and opens/updates the integration PR.
4. Feature-preservation + agent-bus validation + typecheck + lint + build + repository-data gates pass.
5. The same agent resolves all integration failures and merges the PR to `master`.
6. The same agent records the merge, verifies the merged `master` commit, reaches `MERGED_VERIFIED`, and runs the agent exit gate.
7. Only after step 6 may the agent release ownership or report completion.
8. Deploy the `frontend` Next.js application when the workstream includes release/deployment scope.
9. Validate deployed `/api/v1/health` and core product routes when deployment is in scope.
10. Refresh the BUIS/ÖBİKAS course snapshot after the 28–30 Sep 2026 add/drop window.

## Bootstrap exception

Policy/runtime bootstrap commits that establish or strengthen this execution contract may land directly on `master`. All normal product work must follow the mandatory merge-before-exit workflow above.
