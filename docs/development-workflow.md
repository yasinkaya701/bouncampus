# Parallel Development & Merge Workflow

BOUNCAMPUS uses four long-lived KREATE role branches so the team can develop in parallel without turning `master` into a conflict queue.

## Branch map

```text
master
├─ role/ie-customer-discovery
├─ role/ee-physical-systems
├─ role/cs1-decision-intelligence
└─ role/cs2-product-strategy
```

Create short-lived feature branches from the role that owns the outcome:

```text
git switch role/cs1-decision-intelligence
git pull
git switch -c agent/decision-intelligence/forecast-calibration
```

Feature PR:

```text
agent/decision-intelligence/forecast-calibration
    -> role/cs1-decision-intelligence
```

Role integration PR:

```text
role/cs1-decision-intelligence
    -> master
```

## Why this model

The previous repository-wide one-PR lock prevented merge pileups but also serialized unrelated work. The role model keeps conflict domains separate while preserving a hard gate at `master`.

Multiple PRs can be reviewed at once. They cannot merge stale into `master`.

## Concurrency

- Maximum open feature PRs per role branch: **3**
- Maximum open role-to-`master` integration PRs per role: **1**
- Different roles may have open `master` PRs concurrently.
- There is no repository-wide PR cap.

## Merge gates

Every PR must contain its current target base SHA.

Every `master` PR must additionally:

1. sync current `master`;
2. pass feature-preservation checks;
3. pass agent-fabric and KREATE validators;
4. pass frontend/backend/data gates;
5. reconcile shared-file changes;
6. use a normal merge commit;
7. pass post-merge verification.

If PR A merges to `master`, PR B must sync that merge before PR B is eligible to merge.

## Shared files

Changes to `AGENTS.md`, `.agents/**`, `.github/**`, root configuration, lockfiles, shared contracts, and evidence-policy files are treated as high-conflict work. Call them out explicitly and run the broad validation suite.

## Task completion

Merging a feature PR into a role branch is not final completion.

A task is complete only after the role branch containing it reaches `master` and post-merge verification succeeds.
