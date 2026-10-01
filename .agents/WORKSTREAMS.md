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
- Each KREATE execution role has a long-lived `role/*` integration branch.
- Short-lived `agent/<lane>/<task>` branches normally PR into the owning role branch.
- Up to 3 feature PRs may be open against one role branch.
- Each role may have at most one open role-to-`master` integration PR.
- Different roles may have `master` PRs open concurrently.
- Any `master` PR that becomes stale after another merge must sync current `master` and rerun required validation before merge.
- Active task path ownership remains exclusive.
- A role-branch merge is staging; only verified `master` is final delivery.

Five execution roles do not imply five humans. The team remains four people; PMR accounting remains tied to real people/interviews rather than role count.

## Role branches

| Role | Branch | Final ownership focus |
| --- | --- | --- |
| IE | `role/ie-customer-discovery` | market/customer evidence |
| EE | `role/ee-physical-systems` | measurement truth, calibration, uncertainty, field validity |
| EHB | `role/ehb-embedded-integration` | embedded electronics, PCB, firmware, communications, HW↔SW integration |
| CS1 | `role/cs1-decision-intelligence` | decision/model/data intelligence |
| CS2 | `role/cs2-product-strategy` | product strategy, evidence synthesis, application |

## EE ↔ EHB shared boundary

The interface contract and system-level hardware verification are shared. Cross-boundary changes require explicit coordination and dual review; neither role may silently change voltage, pinout, sampling, protocol/schema, calibration persistence, power budget, or fault semantics.

## Active

| Lane | Feature branch | Role branch | Owner | State | Scope | Touched paths |
| --- | --- | --- | --- | --- | --- | --- |

New work should be represented in `.agents/coordination/tasks/*.json`; this table is for human visibility when useful.

## Historical note

Work completed before the five-role model may reference the former four-role or single-integration-PR discipline. Those records are historical evidence only and do not define current policy.

Current authoritative policy is `AGENTS.md`, `.agents/FABRIC.md`, `.agents/fabric.json`, and the role documents under `KREATE/ROLES/`.
