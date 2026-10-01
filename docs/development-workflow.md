# Parallel Development & Merge Workflow

BOUNCAMPUS uses five long-lived execution-role branches so work can develop in parallel without turning `master` into a conflict queue.

The human team remains four people. Execution roles are ownership surfaces and do not imply one human per role.

## Branch map

```text
master
├─ role/ie-customer-discovery
├─ role/ee-physical-systems
├─ role/ehb-embedded-integration
├─ role/cs1-decision-intelligence
└─ role/cs2-product-strategy
```

Create short-lived feature branches from the role that owns the outcome:

```text
git switch role/ehb-embedded-integration
git pull
git switch -c agent/ehb-firmware/offline-replay
```

Feature PR:

```text
agent/ehb-firmware/offline-replay
    -> role/ehb-embedded-integration
```

Role integration PR:

```text
role/ehb-embedded-integration
    -> master
```

## Ownership guide

- IE: market/customer evidence.
- EE: measurement architecture, calibration, uncertainty, field validity.
- EHB: embedded electronics, PCB, firmware, communications, bring-up, HW↔SW integration.
- CS1: decision/model/data intelligence.
- CS2: product strategy, evidence synthesis, application.

EE/EHB changes crossing the measurement/electronics boundary require an explicit interface contract and dual review.

## Why this model

The previous repository-wide one-PR lock prevented merge pileups but serialized unrelated work. The role model keeps conflict domains separate while preserving a hard gate at `master`.

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
3. pass agent-fabric unit tests and validator;
4. pass KREATE validation;
5. pass frontend/backend/data gates as applicable;
6. reconcile shared-file changes;
7. reconcile EE↔EHB interface changes when applicable;
8. use a normal merge commit;
9. pass post-merge verification.

If PR A merges to `master`, PR B must sync that merge before PR B is eligible to merge.

## EHB lanes

Recommended lanes:

```text
agent/ehb-hardware/<task>
agent/ehb-firmware/<task>
agent/ehb-comms/<task>
agent/ehb-integration/<task>
agent/ehb-verification/<task>
```

These lanes are not silos. What matters is that the task targets the correct role branch, declares realistic `touched_paths`, and respects cross-role contracts.

## Shared files

Changes to `AGENTS.md`, `.agents/**`, `.github/**`, root configuration, lockfiles, shared API/data contracts, EE↔EHB interface contracts, and evidence-policy files are treated as high-conflict work. Call them out explicitly and run the broad validation suite.

## Task completion

Merging a feature PR into a role branch is not final completion.

A task is complete only after the role branch containing it reaches `master` and post-merge verification succeeds.
