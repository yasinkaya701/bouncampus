# BOUNCAMPUS Repository Working Policy

## Purpose

BOUNCAMPUS is a multi-agent, four-role KREATE repository. Parallel development is encouraged. Integration is controlled by role branches, explicit path ownership, CI gates, and verified merges to `master`.

The repository optimizes for two things at the same time:

1. let IE, EE, CS1, and CS2 move independently without waiting for a repository-wide PR lock;
2. prevent stale branches, silent feature loss, and conflict-heavy merges from reaching `master`.

## Core roles

KREATE roles:

- **IE — Customer Discovery & Market Lead**
- **EE — Physical Systems & Measurement Lead**
- **CS1 — Decision Intelligence Lead**
- **CS2 — Product Strategy, Evidence Synthesis & Application Lead**

Engineering lanes such as `frontend-ux`, `api-product`, `campus-geo`, and `quality-release` remain valid task lanes. A lane may be executed under whichever KREATE role owns the outcome.

## Branch topology

`master` is durable product truth.

Each KREATE role has a long-lived integration branch:

| Role | Long-lived branch |
| --- | --- |
| IE | `role/ie-customer-discovery` |
| EE | `role/ee-physical-systems` |
| CS1 | `role/cs1-decision-intelligence` |
| CS2 | `role/cs2-product-strategy` |

Normal implementation uses short-lived task branches:

```text
role/<role>
  ├─ agent/<lane>/<task-a>
  ├─ agent/<lane>/<task-b>
  └─ agent/<lane>/<task-c>
```

Default flow:

```text
latest master
    ↓ sync
role/<role>
    ↓ branch
agent/<lane>/<task>
    ↓ PR
role/<role>
    ↓ integration PR
master
```

The long-lived role branch is a staging/integration surface, not a place to bypass review.

`agent-coordination` remains the long-lived metadata-only coordination branch under `.agents/coordination/**`.

## Parallel PR policy

The old repository-wide single-PR rule is removed.

Parallelism is allowed under these rules:

- Multiple open PRs may exist at the same time.
- A role branch may have up to **3 open feature PRs** targeting it.
- Each role may have at most **1 open role-to-`master` integration PR** at a time.
- Different roles may have integration PRs open concurrently.
- A `master` integration PR is mergeable only when its head contains the current `master` base SHA and all required checks are green.
- When one PR merges to `master`, any other open `master` PR that became stale must sync the new `master` before it can merge.
- Repository-wide governance/bootstrap work may use `agent/quality-release/<task>` directly against `master` when it cannot reasonably live under one role branch.
- Direct pushes to `master` are forbidden by process and audited by CI.

This gives parallel review without permitting stale concurrent merges.

## Task ownership and conflict prevention

Before implementation, a Workstream Agent must:

1. read/claim the task using the `agent-coordination` task store when the work is represented there;
2. verify hard dependencies are `MERGED_VERIFIED`;
3. declare realistic `touched_paths`;
4. verify no active task owns overlapping product paths;
5. create a short-lived `agent/<lane>/<task>` branch from the correct role branch;
6. keep the task lease alive while the work is active.

Two active tasks must not own overlapping product paths. Parent/child ownership counts as overlap.

If work must cross role boundaries, choose one primary role branch and document the cross-role impact. If the change is genuinely repository-wide, use the quality/release governance path rather than silently editing several role branches.

## Feature PR requirements: task branch -> role branch

A feature PR is not final delivery. It stages validated work into a role branch.

Before merging a feature PR into a role branch:

1. the PR head contains the latest target role-branch base SHA;
2. declared ownership does not overlap an active incompatible task;
3. targeted tests pass;
4. repository CI required for the touched surfaces passes on the exact PR head;
5. deletions/renames are intentional;
6. conflicts are resolved by reviewing both sides, never by blind whole-file `ours`/`theirs`;
7. the PR is small enough to understand and revert independently.

A task merged only into a role branch is **not** `MERGED_VERIFIED` and is not yet present in durable product truth.

## Role integration PR requirements: role branch -> master

A role integration PR may contain one or more compatible, already-reviewed workstreams from that role.

It may merge only when all of the following are true:

1. the role branch has been synchronized with current `master`;
2. the PR head contains the exact current `master` base commit;
3. `python scripts/verify_feature_preservation.py --base-ref <master-sha>` passes;
4. `python scripts/agent_fabric_check.py` passes;
5. `python scripts/kreate_check.py` passes;
6. repository Python compilation/data validation passes;
7. frontend `npm ci`, typecheck, lint, and build pass when the frontend is in CI;
8. every deletion or rename is accounted for;
9. cross-role/shared-file changes are explicitly called out in the PR checklist;
10. CI is green on the exact PR head SHA;
11. merge uses a normal merge commit;
12. merged `master` is verified after merge.

If another PR lands first, the role PR becomes stale and must re-sync before merge. It does not get grandfathered through on previously green CI.

## Shared and high-conflict surfaces

Treat these as shared/high-conflict surfaces:

- `AGENTS.md`
- `.agents/**`
- `.github/**`
- root build/deployment configuration
- dependency lockfiles
- shared API/data contracts
- feature registry
- KREATE claim/evidence policy files

A PR touching a shared/high-conflict surface must:

- identify the owning role or governance owner;
- list other active workstreams that could be affected;
- preserve both valid sides during conflict resolution;
- run the broad repository validation gates, not only a narrow unit test.

## Merge-before-completion contract

`PR opened`, `feature PR merged to role branch`, `review ready`, or `tests green on a feature branch` are not final completion states.

For an accepted task to become `MERGED_VERIFIED`:

1. its implementation must be contained in the role branch that will integrate it;
2. the role-to-`master` integration PR must pass exact-head CI;
3. the integration PR must merge to `master` using a normal merge commit;
4. the resulting `master` commit must pass post-merge verification;
5. `python scripts/agent_exit_gate.py --branch-head <task-or-integration-head>` must prove the validated work is contained in `master`;
6. integration evidence must be recorded in coordination state.

Several compatible tasks may share one role-to-`master` integration PR. They may also integrate independently. The old repository-wide integration slot no longer exists.

## Human-by-exception policy

Default mode is autonomous inside accepted work.

Human input is required only for:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

Routine branch creation, PR creation, conflict resolution, reversible refactors, tests, and merge execution are not human gates.

## Role-specific post-work checkpoint

The strategic checkpoint remains role scoped:

- **IE: CHECKPOINT ON**
- **CS2: CHECKPOINT ON**
- **EE: CHECKPOINT OFF**
- **CS1: CHECKPOINT OFF**

Detailed behavior lives in `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`.

IE/CS2 should surface a user decision after completing a package when the next step is a genuine strategic branch such as a different beachhead, buyer, major product thesis, or application narrative.

EE/CS1 should continue to the next highest-value aligned technical task unless one of the explicit human gates applies.

## Feature preservation

A merge is invalid if an existing feature, route, data source, asset, validation gate, or evidence boundary disappears unintentionally.

Before a `master` merge:

- start from latest `master`;
- account for deletions and renames;
- update `.github/feature-registry.json` for new durable features when applicable;
- run feature-preservation checks;
- run agent-fabric checks;
- run the full relevant CI suite;
- verify `master` after merge.

Intentional removal of a registered durable feature requires explicit repository-owner direction and PR documentation.

## Product truth and evidence boundary

BOUNCAMPUS must not present estimates as live university telemetry.

Unless explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT sensor networks.

Real-world PMR, interview claims, pilot measurements, and KREATE evidence remain subject to the evidence system under `KREATE/`. Parallel development never authorizes fabricated evidence.

## Practical release sequence

1. Expose/claim independent non-overlapping tasks.
2. Branch from the owning role branch.
3. Implement and validate in parallel.
4. Open feature PRs into the owning role branch.
5. Merge compatible feature PRs after exact-head validation.
6. Periodically sync the role branch from latest `master`.
7. Open one role-to-`master` integration PR for that role.
8. Run full integration gates.
9. Merge with a normal merge commit.
10. Verify merged `master` and record evidence.
11. Mark included tasks `MERGED_VERIFIED`.
12. Delete disposable feature branches when practical.

See `.agents/FABRIC.md` and `docs/development-workflow.md` for the operational protocol.
