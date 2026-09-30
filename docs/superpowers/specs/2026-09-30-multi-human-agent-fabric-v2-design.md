# Multi-Human Multi-Agent Fabric v2 Design

## Status

Approved conversational design, written specification for review before implementation.

## Goal

Evolve BOUNCAMPUS from a mostly single-integration-agent workflow into a collaboration fabric that supports multiple humans and multiple autonomous agents working in parallel without sacrificing evidence integrity, path ownership, merge safety, or KREATE claim discipline.

The default operating mode is autonomous. Humans should be required only at genuinely critical gates: real-world evidence attestation, physical safety, irreversible external actions, external commitments, and material product-direction pivots.

## Non-goals

- Do not build a large agent framework, chat bus, or permanent agent hierarchy.
- Do not redesign the BOUNCAMPUS product.
- Do not change KREATE claims, PMR findings, or application content as part of this fabric change.
- Do not permit agents to self-attest interviews, quotes, private institutional facts, pilot outcomes, or measured climate impact.
- Do not weaken exact-head CI, feature preservation, post-merge verification, or the normal-merge-commit requirement.
- Do not create one branch per human identity or hard-code team-member names into ownership rules.

## Existing foundation to preserve

The repository already provides:

- `master` as repository/product truth;
- `agent-coordination` as metadata-only coordination state;
- per-task JSON files under `.agents/coordination/tasks/`;
- task leases and heartbeat timestamps;
- `touched_paths` ownership and dependency validation;
- explicit human-gate kinds;
- `MERGED_VERIFIED` as the only successful terminal state;
- exact-head CI and post-merge audit;
- KREATE evidence and anti-fabrication boundaries;
- a task CLI workstream already in progress on PR #35.

Fabric v2 extends these mechanisms rather than replacing them.

## Core model

### Task ownership, not person ownership

A task is the unit of ownership. Humans and agents are contributors to tasks; they do not globally own lanes or files outside task leases.

Each active task has:

- one `owner_actor` responsible for lifecycle progress;
- zero or more `contributors`;
- one `lane`;
- one short-lived work branch;
- declared `touched_paths`;
- dependencies;
- acceptance criteria;
- validation commands;
- optional `produces` and `consumes` artifact contracts;
- an optional critical human gate;
- integration evidence.

`owner_actor` may represent either a human or an autonomous agent. Contributor identity is metadata, not an authorization mechanism.

### Actor identity

Actors use a stable string form:

- `human:<github-login>`
- `agent:<role-or-session-id>`

Task JSON must not require a private identity registry. Unknown actors may contribute as long as the task/path contracts are respected.

### Role lanes

KREATE work uses four logical role lanes:

- `ie`
- `ee`
- `cs1`
- `cs2`

Repository engineering lanes such as `frontend-ux`, `api-product`, `campus-geo`, and `quality-release` remain valid for implementation tasks.

Role lanes describe responsibility and prioritization. They are not exclusive human seats: multiple humans and multiple agents may contribute to the same role over time through separate non-overlapping tasks.

## Branch model

### Short-lived task branches

The canonical implementation branch format remains task-scoped:

`agent/<lane>/<task-slug>`

Human contributors may use either the same task branch or a compatible `human/<lane>/<task-slug>` branch when repository tooling supports it. The integration contract applies equally to both.

No permanent role branch is required. Permanent role branches would accumulate divergence and complicate multi-human contribution. Role identity is therefore metadata on tasks, while work remains short-lived and task-scoped.

### Coordination branch

`agent-coordination` remains long-lived and metadata-only. It contains task state, leases, artifact dependencies, and critical human-gate state. It must never contain product code or application claims.

## Parallel pull-request model

### Rationale

The current single-open-PR rule unnecessarily serializes review and CI even when implementation paths are independent. Fabric v2 separates review parallelism from merge serialization.

### Rules

- Up to 4 open work PRs may exist concurrently.
- At most 1 non-draft PR may hold the integration slot at a time.
- All other work PRs must remain draft.
- Each task may have at most 1 open PR.
- A draft PR may run CI, receive reviews, and collect evidence while another PR integrates.
- Draft CI is advisory for future merge readiness; it is never sufficient for merge after `master` changes.
- Before a task acquires the integration slot, its branch must contain current `master`.
- The integration PR must run fresh exact-head CI after the latest-master update.
- Only the integration-slot PR may merge.
- Integration uses a normal merge commit.
- Post-merge verification and `agent_exit_gate.py` remain mandatory.

### Integration queue

Tasks in `READY_FOR_INTEGRATION` form the queue. Queue order is selected mechanically by:

1. priority (`P0` before `P1` before `P2`);
2. dependency-unblocking value;
3. oldest `ready_for_integration_at` timestamp;
4. stable task ID tie-break.

An agent may not jump the queue merely because its PR is already open. A critical regression or recovery task may preempt by being marked P0 with explicit rationale.

## Multi-human collaboration

### Contributors

A task can record multiple contributors. Contributors may:

- add commits to the task branch when authorized by GitHub;
- review artifacts;
- run tests;
- attach evidence references;
- participate in code review.

Only the `owner_actor` changes lifecycle state unless ownership is explicitly transferred in task metadata.

### Ownership transfer

Ownership transfer is allowed when:

- the current owner intentionally releases responsibility; or
- the lease is stale and reclaim rules are satisfied.

Transfer must record previous owner, new owner, timestamp, and reason in task notes/history. It must not require a human gate unless a critical human-gate condition independently exists.

### Human review versus human gate

Human code review and human-gate approval are different concepts.

- Human review may improve quality but should not block ordinary autonomous work unless repository policy explicitly requires it for a sensitive path.
- A human gate blocks progress only for the five critical gate kinds.

Application-relevant factual claims retain their existing second-human review requirements from the KREATE operating system.

## Human-by-exception policy

All roles — IE, EE, CS1, and CS2 — continue autonomously after completing ordinary work. The previous universal post-work strategic checkpoint for IE/CS2 is removed.

Humans are required only for:

1. `EVIDENCE_ATTESTATION`
   - confirming an interview occurred;
   - confirming exact quotes;
   - attesting private institutional facts;
   - final factual sign-off where KREATE policy requires a person.

2. `IRREVERSIBLE_ACTION`
   - destructive production/data operations;
   - credential revocation/rotation;
   - repository/account administration;
   - equivalent difficult-to-reverse external actions.

3. `PHYSICAL_SAFETY`
   - hardware energization;
   - actuator movement;
   - mains/high-current work;
   - real field deployment.

4. `EXTERNAL_COMMITMENT`
   - final application submission;
   - purchase/payment;
   - contract/legal acceptance;
   - consequential external messages;
   - committing the team to a pilot/date.

5. `PRODUCT_DIRECTION`
   - material change to agreed beachhead;
   - material change to primary problem;
   - material change to core product thesis when evidence supports multiple credible directions.

Routine PMR planning, architecture choices, reversible feature prioritization, model selection, sensor comparison, application drafting, branch operations, testing, conflict resolution, PR creation, and merge execution do not require human approval.

`WAITING_HUMAN` is invalid unless one of these five gates is pending and all independent work is already complete.

## Artifact contracts between agents and humans

Tasks gain optional arrays:

- `produces`: artifact/evidence/task-output identifiers created by the task;
- `consumes`: identifiers required by the task.

Examples:

- IE task produces `E-INT-012` and `H-003-update`.
- CS1 task consumes `E-INT-012` and `H-003-update`.
- EE task produces `TECH_TEST-scale-repeatability-v1`.
- CS2 consumes those outputs when drafting a defensible claim.

Artifact contracts replace synchronous chat relay. A consumer cannot claim an artifact-dependent task until required producer outputs exist or the dependency is explicitly optional.

## Task schema v2

Task metadata should add, minimally:

- `schema_version: 2`
- `owner_actor`
- `contributors: []`
- `role: IE | EE | CS1 | CS2 | NONE`
- `produces: []`
- `consumes: []`
- `ready_for_integration_at`
- `integration.pr_state: DRAFT | READY | MERGED | null`
- `history: []` for ownership/state-transition audit entries

Compatibility: schema-v1 tasks remain readable during migration. Validator/CLI should support v1 read and v2 writes until all active tasks are migrated.

## Path ownership

`touched_paths` remains the hard conflict-prevention contract.

Rules:

- Parent/child path overlap counts as conflict.
- Two active tasks may not own overlapping product paths.
- Read-only consumption does not require ownership.
- Coordination metadata paths do not count as product-path ownership.
- If a task discovers a new required path that conflicts with active ownership, it must re-scope, wait, or explicitly transfer/merge task ownership.
- Draft PR status does not relax path ownership.

Multi-human work on one task is allowed because contributors share the same task/path lease.

## CI and policy enforcement

### Pull-request CI

Mechanical policy checks must enforce:

- no more than 4 open work PRs;
- no more than 1 non-draft integration PR;
- no more than 1 open PR per task ID;
- PR body includes task ID and owner actor;
- task branch is associated with the same task ID;
- integration-ready PR contains latest `master`;
- only the non-draft integration PR can satisfy merge discipline;
- feature-preservation, agent-fabric, KREATE, repository-data, frontend checks remain unchanged.

Draft PRs should not fail merely because another draft PR exists. They should fail only on true task/fabric violations.

### Master CI

Continue requiring:

- merge-commit provenance;
- associated merged PR;
- integrated task head contained in master;
- post-merge validators;
- exit-gate verification.

## Task CLI behavior

The existing PR #35 task CLI should remain the primary mutation interface if merged successfully.

Fabric v2 should extend it with commands or equivalent operations for:

- `next`: choose highest-value claimable task for an actor/role;
- `add-contributor` / `remove-contributor`;
- `transfer-owner`;
- `ready`: mark `READY_FOR_INTEGRATION` and timestamp it;
- `queue`: show deterministic integration order;
- `acquire-integration`: require the integration slot to be free and mark the task PR ready/non-draft;
- `release-integration`: only after merge or explicit rollback;
- artifact `produce` / `consume` recording where useful.

Commands must preserve atomic blob-SHA update behavior on `agent-coordination`.

## Autonomous dispatcher

A dispatcher can run without a human relay:

1. read current objective and task graph;
2. identify READY tasks;
3. filter unresolved dependencies and path conflicts;
4. rank by priority and selection impact;
5. assign/claim work for available actors;
6. let tasks execute in parallel;
7. move validated tasks to `READY_FOR_INTEGRATION`;
8. acquire integration slot for one task at a time;
9. keep all other PRs draft;
10. after verified merge, release task lease and expose newly unblocked work.

A dispatcher may create new bounded technical/operational tasks when the need is mechanically implied by current objectives and does not change product direction.

## Failure and recovery behavior

- Stale owner: reclaim by lease rules after checking branch/PR activity.
- Stale draft PR: owner/reclaimer syncs latest master before integration; old CI is not trusted.
- Integration failure: integration owner keeps ownership, fixes or reverts, reruns exact-head CI.
- Conflicting path requirement: block/re-scope one task; do not allow concurrent edits.
- Human-gate pending: finish independent work, set `WAITING_HUMAN`, ask exactly one concrete question.
- Direct push to master: retain existing incident-recovery procedure and audit failure.
- Abandoned task: `CANCELLED` with rationale; never represented as completed.

## Migration plan

1. Allow PR #35 to complete under the current fabric because it modifies the task CLI and CI used by v2.
2. Implement fabric schema-v2 compatibility and tests.
3. Replace single-open-PR enforcement with parallel-draft / single-integration-slot enforcement.
4. Remove IE/CS2 post-work checkpoint requirement while retaining the five explicit human gates.
5. Extend task CLI for contributor ownership, queueing, and integration-slot operations.
6. Update issue/PR templates to carry task ID, owner actor, contributors, role, and draft/integration state.
7. Create/update test fixtures for multiple humans and multiple agents operating concurrently.
8. Merge through exact-head CI and verify master.
9. Migrate active coordination tasks to schema v2 when touched; do not rewrite verified historical tasks unnecessarily.

## Acceptance criteria

Fabric v2 is complete only when all of the following are mechanically demonstrated:

1. Two or more independent tasks can be active concurrently with distinct humans/agents and non-overlapping paths.
2. Up to four work PRs may be open when all but at most one are draft.
3. A second non-draft integration PR is rejected.
4. Two active tasks with overlapping paths are rejected.
5. One task can have multiple contributors without creating a second lease.
6. Ownership can be transferred or stale-reclaimed with an audit record.
7. Integration queue ordering is deterministic.
8. A draft PR with previously green CI must rerun exact-head CI after syncing changed master before merge.
9. `WAITING_HUMAN` is rejected for any non-critical reason.
10. IE/CS2 can autonomously continue ordinary strategic execution without a post-work checkpoint.
11. Real PMR/evidence attestation still cannot be self-approved by an agent.
12. Application claim review rules remain intact.
13. `MERGED_VERIFIED` still requires normal merge, post-merge verification, and exit-gate evidence.
14. Existing product/UI behavior and KREATE evidence truth boundaries are unchanged.

## Security and trust boundary

The fabric coordinates work; it does not grant additional GitHub permissions. Repository permissions remain the enforcement boundary for who can push, merge, or administer settings. Fabric metadata is advisory plus CI-enforced policy and must never contain secrets.

## Design decision summary

Use **task-scoped short-lived branches + multi-contributor leases + parallel draft PRs + one serialized integration slot**.

Do not use permanent role branches and do not revive the old large `agent_bus.py` approach. This keeps parallelism high while minimizing long-lived divergence, merge conflicts, and coordination overhead.