# BOUNCAMPUS Repository Working Policy

## Mandatory multi-agent architecture

BOUNCAMPUS is a multi-agent repository. Parallel implementation is encouraged when ownership is explicit and integration is serialized.

### Roles

- **Dispatcher**: decomposes goals into independently executable tasks, resolves dependencies, and exposes ready work.
- **Workstream Agent**: claims one task/lane and owns it end-to-end: implementation, tests, integration, merge, and post-merge verification.
- **Verifier / Red Team**: independently checks risky diffs, acceptance criteria, evidence boundaries, or failure modes when useful.
- **Integration Owner / temporary Merge Coordinator**: the Workstream Agent whose batch currently holds the repository's single integration slot. This is not a handoff role.
- **Frontend / UX lane**: UI, accessibility, responsive behavior, visual system, client interactions.
- **Campus Data / Geo lane**: building metadata, coordinates, geometry, map/3D assets, source provenance.
- **API / Product lane**: Next.js API routes, backend data contracts, product logic, integrations.
- **Quality / Release lane**: typecheck, lint, build, backend validation, deployment/release evidence.

An agent may own more than one lane only when the touched file sets do not overlap with another active task.

## Autonomous control plane

**Default mode is AUTONOMOUS. Human involvement is exception-only inside an accepted work package.**

The machine-readable contract lives in `.agents/fabric.json`; the execution protocol lives in `.agents/FABRIC.md`.

- Repository/product truth lives on `master`.
- Parallel task state lives on the long-lived `agent-coordination` branch under `.agents/coordination/tasks/`.
- Each task is one JSON file based on `.agents/TASK_TEMPLATE.json`.
- Claims/heartbeats update only that task file. GitHub blob-SHA preconditions serialize competing claims without a human dispatcher.
- Product implementation stays on short-lived `agent/<lane>/<task>` branches.
- At most one integration PR may be open; that PR remains the repository-wide integration lock.
- `.agents/WORKSTREAMS.md` is a compatibility/history view, not the high-frequency coordination database. Do not make all parallel agents contend on that single markdown file for routine claims/heartbeats.

The `agent-coordination` branch is a deliberate policy exception: agents may write **coordination metadata only** under `.agents/coordination/**` directly to that branch. They may not put product code, application claims, secrets, binaries, or release artifacts there.

## Human-by-exception policy

Agents MUST NOT ask a human for routine engineering judgment that can be resolved by repository inspection, testing, a reversible implementation choice, or a bounded experiment **while executing the currently accepted work package**.

Human input is required only for these gate kinds:

1. `EVIDENCE_ATTESTATION` — a person must attest real-world evidence such as an interview, quote, private institutional fact, or final claim sign-off.
2. `IRREVERSIBLE_ACTION` — destructive/difficult-to-reverse external actions such as deleting production data, credential revocation/rotation, or repository/account administration.
3. `PHYSICAL_SAFETY` — real hardware energization, actuator movement, mains/high-current work, field deployment, or another physical-risk action.
4. `EXTERNAL_COMMITMENT` — final submission, purchase/payment, contract/legal acceptance, consequential external message, or committing to a pilot/date on behalf of the team.
5. `PRODUCT_DIRECTION` — a material pivot to the agreed beachhead, primary problem, or core product direction when evidence supports materially different choices.

Everything else is autonomous by default **inside the accepted work package**, including decomposition, branch creation, code edits, tests, reversible refactors, dependency updates, ordinary documentation, routine feature prioritization, conflict resolution, PR creation, merge execution, rollback/revert, and post-merge verification.

`WAITING_HUMAN` is valid only when the task has a non-`NONE` human gate, asks one concrete decision, and all work independent of that decision is already complete. Uncertainty alone is not a human gate.

## Post-work user decision checkpoint

Autonomy inside a work package does **not** authorize an agent to finish one meaningful task and then blindly select the next strategic workstream.

The required lifecycle is:

> **Accept work → finish it end-to-end → merge and verify → explain the result → surface real next options → recommend one → ask the user to choose the next meaningful direction when a material branch exists.**

After a work package reaches `MERGED_VERIFIED`, or after a bounded research/PMR/experiment package reaches its accepted Definition of Done, the agent MUST evaluate whether the next step is merely completion of the same direction or a new meaningful branch.

### Continue autonomously when

The next action is:

- required to finish the same accepted acceptance criteria;
- a routine integration or verification step;
- low-risk and reversible;
- an obvious sequential subtask with no material strategic alternative;
- a small technical choice that can be resolved by tests or inspection.

Do not interrupt the user for those cases.

### Stop and request direction when

The current work is complete and the next action would commit substantial effort to one of multiple credible directions, for example:

- a new major feature stream;
- a new PMR segment;
- a different beachhead or persona;
- hardware versus hardware-free direction;
- a new hardware architecture;
- a materially different model/data strategy;
- a substantial application narrative change;
- a new campus domain expansion;
- a large polish/demo workstream before the application deadline;
- any other next workstream where choosing one path meaningfully delays or excludes another.

### Required decision package

Before asking the user for direction, the agent MUST provide enough information to support an informed choice:

1. **Completed** — what was actually delivered;
2. **Evidence / result** — tests, commits, measurements, interview findings, benchmark results, or evidence IDs;
3. **What changed** — assumptions, risks, product requirements, feature priority, or KREATE claims affected;
4. **Options** — normally 2–4 materially different next paths, without fake alternatives;
5. for each option: **expected result, effort/cost, main risk, dependencies, and KREATE impact**;
6. **Recommendation** — which option the agent prefers and why;
7. **Decision needed** — one concise user choice.

The agent MUST take a position. “All options are equally good” is not useful unless the evidence genuinely supports that conclusion.

Do not ask vague questions such as “What should I do next?” or “Should I continue?” without first supplying the result and decision context.

A good checkpoint ends with something like:

> **Recommended:** Option B because it produces the highest PMR/evidence value before October 8 with lower dependency risk.  
> **Decision needed:** choose A, B, or C for the next workstream.

For KREATE-specific work, follow the detailed protocol in `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`.

This checkpoint occurs **after the current work package is complete**. It does not weaken the merge-before-exit contract and must not be used as an excuse to stop with accepted code unmerged or unverified.

## Task claim and lease rules

New autonomous workstreams use task files on `agent-coordination` rather than editing a central shared ledger for every state change.

Before implementation, a Workstream Agent must:

1. read the task and current blob SHA from `agent-coordination`;
2. require `READY` state or satisfy the stale-reclaim rules in `.agents/FABRIC.md`;
3. verify all hard dependencies are `MERGED_VERIFIED`;
4. verify its declared `touched_paths` do not overlap another active task;
5. atomically update the task to `CLAIMED` with `owner_agent`, branch, claim timestamp, and heartbeat using the current blob SHA;
6. create/use the declared `agent/<lane>/<task>` branch and move to `ACTIVE`.

A material commit or meaningful validation checkpoint refreshes the heartbeat. An expired lease may be reclaimed autonomously only under the evidence requirements in `.agents/FABRIC.md`; a human is not required merely because an agent disappeared.

Two active agents must not own overlapping product paths. Parent/child ownership counts as overlap. If a newly discovered necessary path overlaps another active task, re-scope, wait, or explicitly coordinate; do not silently edit the overlapping path.

## HARD EXIT CONTRACT — MERGE BEFORE EXIT

**An agent MUST NOT finish, report success, relinquish ownership, or exit while its accepted work exists only on an agent branch or open PR.**

For every workstream an agent accepts, the same owning Workstream Agent MUST continue until all of the following are true:

1. implementation is complete on its short-lived branch;
2. targeted validation passes;
3. the task reaches `READY_FOR_INTEGRATION`;
4. the agent acquires the single integration slot when no other PR is open;
5. its branch is updated with the latest `master`;
6. feature-preservation and agent-fabric checks pass;
7. the repository's single integration PR is opened or updated by that same agent;
8. all PR CI checks pass on the exact head SHA;
9. the same agent resolves every merge conflict and CI failure caused by the batch;
10. the same agent performs a normal merge into `master`;
11. the merged `master` commit is verified with the required post-merge checks;
12. `python scripts/agent_exit_gate.py --branch-head <merged-agent-head>` passes;
13. the coordination task is updated to `MERGED_VERIFIED` with PR/head/merge/post-merge evidence;
14. only then may the lease be released and the agent report completion.

`PR opened`, `PR ready`, `tests green on branch`, `handoff written`, or `awaiting merge` are **not completion states**.

If merge is blocked by conflicts, stale base, failing CI, or integration regressions, the agent keeps working on the same workstream and fixes them. It may not stop merely because integration became difficult.

The only permitted non-merged exit is a **hard external blocker** that the agent cannot resolve with available repository/tool access, such as unavailable credentials/permissions, an unavailable required external service, or an explicit repository-owner decision. In that case the task remains `BLOCKED`, never `DONE`, and must contain exact blocker evidence and the next executable action.

## Branch and ownership rules

- `master` is protected by process: normal engineering work MUST NOT be committed directly to `master`.
- Product work uses short-lived branches named `agent/<lane>/<task>`.
- `agent-coordination` is the only long-lived agent branch and is metadata-only as defined above.
- New autonomous work claims ownership in task JSON on `agent-coordination`. `.agents/WORKSTREAMS.md` may continue to record legacy/in-flight work and verified history but is not required for high-frequency lease changes.
- Two active tasks must not edit the same product path unless ownership is explicitly re-scoped.
- An agent does not hand completed code to another agent merely to perform the merge. The owning Workstream Agent becomes the temporary Integration Owner when its task reaches the integration slot.
- Ownership remains active until work is merged to `master`, post-merge verification passes, and the task reaches `MERGED_VERIFIED`.

## One-PR integration rule

BOUNCAMPUS must not accumulate pull requests.

- There may be **at most one open pull request** in the repository.
- That PR is the current Integration Owner's integration PR targeting `master`.
- Other agents may continue non-overlapping implementation on their branches while the slot is occupied.
- They may not mark their work complete or exit with unmerged accepted work.
- When the integration slot becomes free, the next `READY_FOR_INTEGRATION` task updates from latest `master`, acquires the slot, integrates, and merges.
- The integration PR must contain the latest `master` before final validation; stale heads are not mergeable.
- A PR is never a parking lot. Its owner keeps driving it until merged or a genuine hard external blocker is documented.

## Feature-preservation rule

A merge is invalid if an existing feature, route, data source, UI surface, asset, or validation gate disappears unintentionally.

Before merge, the owning agent acting as Integration Owner MUST:

1. start from the latest `master`;
2. resolve conflicts manually; never use whole-file `ours`/`theirs` on product files without reviewing both sides;
3. compare the integration head with `master` and account for every deletion or rename;
4. update `.github/feature-registry.json` when a new durable feature is introduced;
5. run `python scripts/verify_feature_preservation.py --base-ref <master-sha>`;
6. run `python scripts/agent_fabric_check.py`;
7. run frontend `npm run typecheck`, `npm run lint`, and `npm run build` when frontend remains part of repository CI;
8. compile backend/scripts Python and validate critical JSON datasets;
9. merge only after all required CI gates are green on the exact head;
10. re-run release checks on the merged `master` commit;
11. run the agent exit gate before declaring completion.

Existing feature-registry entries may not be removed or weakened in a normal feature PR. Intentional removals require an explicit repository-owner decision documented in the PR.

## Merge semantics

- **Merge is mandatory and owned by the Workstream Agent that accepted the task.**
- Completed work is not delivered while it exists only on a branch or PR.
- Use a normal merge commit so the validated agent head remains an ancestor of `master` and can be verified by the exit gate.
- After successful merge and post-merge verification, merged work branches are disposable and should be deleted when practical.
- No agent may report `DONE` for work that is not present on verified `master` and reflected as `MERGED_VERIFIED` in coordination state.

## Product truth boundary

BOUNCAMPUS must not present model estimates as live university telemetry. Unless a source is explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT sensor networks.

Real-world evidence and KREATE claims remain subject to the stricter evidence system under `KREATE/`; multi-agent autonomy never permits fabricating or self-attesting PMR.

## Release sequence

1. Dispatcher exposes independent `READY` tasks.
2. Workstream Agents atomically claim non-overlapping tasks and execute in parallel.
3. Each agent validates its branch and moves its task to `READY_FOR_INTEGRATION`.
4. One task at a time acquires the integration slot, updates from latest `master`, and opens the single PR.
5. Feature-preservation + agent-fabric + typecheck/lint/build + repository-data gates pass.
6. The same owning agent resolves integration failures and merges to `master`.
7. The same agent verifies the merged `master`, runs the exit gate, and records merge evidence.
8. Only then does the task become `MERGED_VERIFIED` and release its lease.
9. Deploy/verify runtime surfaces when deployment is part of the task scope.
10. If the completed work exposes multiple meaningful next directions, present the user decision checkpoint before claiming a new strategic workstream.

## Bootstrap exception

Policy bootstrap changes that establish or strengthen this execution contract may temporarily use a conservative bootstrap path when the old coordination mechanism itself prevents a valid parallel claim. Bootstrap work must remain non-product, must not overwrite another task's owned product paths, must be explicitly identified in its integration PR, and must still pass exact-head CI, normal merge, and post-merge verification before it is considered delivered.
