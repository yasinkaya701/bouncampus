# Active Workstreams

This file is a human-readable compatibility/history view. High-frequency claims and heartbeats belong in task JSON under `agent-coordination`.

## Lifecycle

A workstream remains non-terminal until its accepted changes exist on verified `master`.

Valid states:

- `ACTIVE`
- `READY_FOR_INTEGRATION`
- `INTEGRATING`
- `MERGED_VERIFYING`
- `MERGED_VERIFIED`
- `BLOCKED`
- `WAITING_HUMAN`
- `CANCELLED`

`HANDOFF`, `PR_READY`, `AWAITING_MERGE`, and branch-only `DONE` are not success states.

## Parallel integration rules

- There is no repository-wide single-PR lock.
- Each execution role has a long-lived `role/*` integration branch.
- The execution-role count is independent of the four-human KREATE team count.
- Short-lived `agent/<lane>/<task>` branches normally PR into the owning role branch.
- Up to 3 feature PRs may be open against one role branch.
- Each role may have at most one open role-to-`master` integration PR.
- Different roles may have `master` PRs open concurrently.
- Any `master` PR that becomes stale after another merge must sync current `master` and rerun required validation before merge.
- Active task path ownership remains exclusive.
- A role-branch merge is staging; only verified `master` is final delivery.
- EE↔EHB cross-boundary hardware changes use the interface contract; device/data-contract changes affecting downstream inference require CS1 consumer review.

## Role branches

| Role | Branch |
| --- | --- |
| IE | `role/ie-customer-discovery` |
| EE | `role/ee-physical-systems` |
| EHB | `role/ehb-embedded-integration` |
| CS1 | `role/cs1-decision-intelligence` |
| CS2 | `role/cs2-product-strategy` |

## Active

| Lane | Feature branch | Role branch | Owner | State | Scope | Touched paths |
| --- | --- | --- | --- | --- | --- | --- |

New work should be represented in `.agents/coordination/tasks/*.json`; this table is for human visibility when useful.

## Historical note

Work completed before the role-branch model may reference the former single integration PR discipline. Those records are historical evidence only and do not define current policy.

Current authoritative policy is `AGENTS.md`, `.agents/FABRIC.md`, and `.agents/fabric.json`.
