# BOUNCAMPUS Repository Working Policy

## Purpose

BOUNCAMPUS is a multi-agent, five-execution-role KREATE repository. Parallel development is encouraged. Integration is controlled by role branches, explicit path ownership, CI gates, and verified merges to `master`.

The repository optimizes for two things at the same time:

1. let IE, EE, EHB, CS1, and CS2 move independently without waiting for a repository-wide PR lock;
2. prevent stale branches, silent feature loss, weak evidence, and conflict-heavy merges from reaching `master`.

Five execution roles do **not** imply five humans. The human team remains four people; PMR tracking remains person-based, not role-count-based.

## Core roles

KREATE execution roles:

- **IE — Customer Discovery & Market Lead**
- **EE — Physical Systems & Measurement Lead**
- **EHB — Embedded Hardware, Communications & Integration Lead**
- **CS1 — Decision Intelligence Lead**
- **CS2 — Product Strategy, Evidence Synthesis & Application Lead**

Engineering lanes such as `frontend-ux`, `api-product`, `campus-geo`, and `quality-release` remain valid task lanes. A lane may be executed under whichever KREATE role owns the outcome.

Hardware is intentionally split:

- EE owns measurement architecture, measurement-method/sensor selection, calibration, uncertainty, and field validity.
- EHB owns embedded electronics, PCB, firmware, communications, controller-side power/interface implementation, bring-up, and HW↔SW integration.
- System verification and the EE↔EHB interface contract are shared.

## Branch topology

`master` is durable product truth.

Each execution role has a long-lived integration branch:

| Role | Long-lived branch |
| --- | --- |
| IE | `role/ie-customer-discovery` |
| EE | `role/ee-physical-systems` |
| EHB | `role/ehb-embedded-integration` |
| CS1 | `role/cs1-decision-intelligence` |
| CS2 | `role/cs2-product-strategy` |

Normal implementation uses short-lived task branches:

```text
role/<role>
  ├─ agent/<lane>/<task-a>
  ├─ agent/<lane>/<task-b>
  └─ agent/<lane>/<task-c>
```

Recommended EHB lanes:

```text
agent/ehb-hardware/<task>
agent/ehb-firmware/<task>
agent/ehb-comms/<task>
agent/ehb-integration/<task>
agent/ehb-verification/<task>
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

If work crosses role boundaries, choose one primary role branch and document the cross-role impact. If the change is genuinely repository-wide, use the quality/release governance path rather than silently editing several role branches.

## EE ↔ EHB coordination contract

EE and EHB are independent roles with a mandatory interface contract whenever work crosses the measurement/electronics boundary.

The relevant subset must be explicit before deep parallel implementation:

- sensor/interface electrical requirements;
- supply voltage/current limits;
- connector/pinout;
- ADC/interface expectations;
- sampling rate/timing;
- calibration-data ownership/persistence;
- protocol and packet/event schema;
- units/scaling;
- quality/status/error flags;
- power budget;
- startup/shutdown behavior;
- offline/fault/retry behavior;
- test points and validation method.

Decision rights:

- measurement correctness → EE final owner;
- embedded/comms/interface implementation → EHB final owner;
- shared interface change → dual EE+EHB review;
- model/decision semantics → CS1 final owner;
- product/application framing → CS2 final owner.

No silent voltage, pinout, sampling, schema, protocol, calibration-persistence, or power-budget change is allowed.

## EHB ↔ CS1 coordination contract

EHB owns reliable device-side representation/transport; CS1 owns decision/model semantics.

Cross-role data work must align on timestamps/order, missing/invalid readings, quality flags, device metadata, duplicate handling, offline replay, schema versions, and API expectations that affect firmware behavior.

A payload reaching the backend is not considered integrated if its semantics cannot be interpreted reliably.

## Feature PR requirements: task branch -> role branch

A feature PR is not final delivery. It stages validated work into a role branch.

Before merging a feature PR into a role branch:

1. the PR head contains the latest target role-branch base SHA;
2. declared ownership does not overlap an active incompatible task;
3. targeted tests pass;
4. repository CI required for the touched surfaces passes on the exact PR head;
5. deletions/renames are intentional;
6. conflicts are resolved by reviewing both sides, never by blind whole-file `ours`/`theirs`;
7. the PR is small enough to understand and revert independently;
8. any EE↔EHB interface changes have the required dual review.

A task merged only into a role branch is **not** `MERGED_VERIFIED` and is not yet present in durable product truth.

## Role integration PR requirements: role branch -> master

A role integration PR may contain one or more compatible, already-reviewed workstreams from that role.

It may merge only when all of the following are true:

1. the role branch has been synchronized with current `master`;
2. the PR head contains the exact current `master` base commit;
3. `python scripts/verify_feature_preservation.py --base-ref <master-sha>` passes;
4. `python scripts/agent_fabric_check.py` passes;
5. `python scripts/test_agent_fabric_check.py` passes;
6. `python scripts/kreate_check.py` passes;
7. repository Python compilation/data validation passes;
8. frontend `npm ci`, typecheck, lint, and build pass when the frontend is in CI;
9. every deletion or rename is accounted for;
10. cross-role/shared-file changes are explicitly called out in the PR checklist;
11. CI is green on the exact PR head SHA;
12. merge uses a normal merge commit;
13. merged `master` is verified after merge.

If another PR lands first, the role PR becomes stale and must re-sync before merge. It does not get grandfathered through on previously green CI.

## Shared and high-conflict surfaces

Treat these as shared/high-conflict surfaces:

- `AGENTS.md`
- `.agents/**`
- `.github/**`
- root build/deployment configuration
- dependency lockfiles
- shared API/data contracts
- EE↔EHB interface contracts
- feature registry
- KREATE claim/evidence policy files

A PR touching a shared/high-conflict surface must:

- identify the owning role or governance owner;
- list other active workstreams that could be affected;
- preserve both valid sides during conflict resolution;
- run the broad repository validation gates, not only a narrow unit test.

## Hardware engineering policy

Hardware work is first-class engineering work, not presentation polish. The detailed execution contract lives in `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`.

Hardware work should be decomposed by ownership rather than forcing all work under EE:

**EE measurement work:** measurement requirement, measurement-method/sensor choice, calibration, uncertainty, field/pilot validation.

**EHB implementation work:** controller/MCU, electronics, power/interface implementation, firmware, communications, PCB/interconnect, bring-up, protocol, backend-device integration.

**Shared:** system verification and interface contract.

Hardware agents MUST preserve the distinction between:

- `ASSUMPTION`
- `DATASHEET`
- `CALCULATION`
- `SIMULATION`
- `BENCH_TEST`
- `FIELD_TEST`
- `PRODUCTION_EVIDENCE`

A simulation, CAD render, datasheet value, or AI-generated schematic is not bench evidence.

Physical actions that can create real risk remain subject to the `PHYSICAL_SAFETY` gate. Designing, simulating, calculating, coding firmware, and non-energized review are autonomous; dangerous energization, high-current/high-voltage testing, unsafe battery work, destructive testing, hazardous actuator motion, or consequential field installation require appropriate human approval/supervision.

## Merge-before-completion contract

`PR opened`, `feature PR merged to role branch`, `review ready`, or `tests green on a feature branch` are not final completion states.

For an accepted task to become `MERGED_VERIFIED`:

1. its implementation must be contained in the role branch that will integrate it;
2. the role-to-`master` integration PR must pass exact-head CI;
3. the integration PR must merge to `master` using a normal merge commit;
4. the resulting `master` commit must pass post-merge verification;
5. `python scripts/agent_exit_gate.py --branch-head <task-or-integration-head>` must prove the validated work is contained in `master`;
6. integration evidence must be recorded in coordination state.

Several compatible tasks may share one role-to-`master` integration PR. They may also integrate independently.

## Human-by-exception policy

Default mode is autonomous inside accepted work.

Human input is required only for:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

Routine branch creation, PR creation, conflict resolution, reversible refactors, tests, technical architecture selection, and merge execution are not human gates.

## Role-specific post-work checkpoint

The strategic checkpoint remains role scoped:

- **IE: CHECKPOINT ON**
- **CS2: CHECKPOINT ON**
- **EE: CHECKPOINT OFF**
- **EHB: CHECKPOINT OFF**
- **CS1: CHECKPOINT OFF**

Detailed behavior lives in `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`.

IE/CS2 should surface a user decision after completing a package when the next step is a genuine strategic branch such as a different beachhead, buyer, major product thesis, or application narrative.

EE/EHB/CS1 should continue to the next highest-value aligned technical task unless one of the explicit human gates applies.

## PMR count and role count

PMR remains a four-human responsibility. The current tracker target stays at **16 interviews**, approximately four lead interviews per human team member.

Do not create EHB-01..04 interview slots merely because EHB exists as a fifth execution role. EHB may support or conduct interviews as staffed, but interview accounting follows real people and actual interviews, not execution-role count.

## Feature preservation

A merge is invalid if an existing feature, route, data source, asset, validation gate, or evidence boundary disappears unintentionally.

Before a `master` merge:

- start from latest `master`;
- account for deletions and renames;
- update `.github/feature-registry.json` for new durable product features when applicable;
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

See `.agents/FABRIC.md`, `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`, and `docs/development-workflow.md` for the operational protocol.
