# BOUNCAMPUS Repository Working Policy

## Purpose

BOUNCAMPUS uses a multi-agent execution fabric with **four human-owned parent workstreams** and **five first-class execution roles**. Parallel implementation is encouraged, but durable product truth reaches `master` only through current-base, exact-head-verified merges.

The control plane optimizes for two things at once:

1. let independent work fan out without waiting for unrelated work;
2. prevent path collisions, stale merges, silent feature loss, and evidence-boundary regressions.

## Human parents and execution roles

Human-owned parent workstreams:

- **IE — Customer Discovery & Market**
- **EE — Physical Systems & Measurement**
- **CS1 — Decision Intelligence**
- **CS2 — Product Strategy, Evidence Synthesis & Application**

Durable execution roles:

| Execution role | Long-lived branch | Scope |
| --- | --- | --- |
| IE | `role/ie-customer-discovery` | customer discovery / market evidence |
| EE | `role/ee-physical-systems` | measurement architecture, calibration, uncertainty, field verification |
| EHB | `role/ehb-embedded-integration` | embedded electronics, PCB, firmware, communications, device integration |
| CS1 | `role/cs1-decision-intelligence` | models, inference, decision semantics, software consumer contracts |
| CS2 | `role/cs2-product-strategy` | product strategy, evidence synthesis, application narrative |

Human-team count and execution-role count are intentionally different. The EE human parent may coordinate both EE and EHB child work, but **EHB never collapses into EE**: EHB keeps its own branch, ownership, tests, and integration boundary.

Engineering lanes such as `frontend-ux`, `api-product`, `campus-geo`, `quality-release`, `hw-measurement`, `ehb-firmware`, or `ehb-integration` remain task labels, not ownership substitutes.

## Fabric v2 hierarchy

Schema v2 adds a parent/child coordination layer on top of durable role branches.

```text
human parent workstream
    ├─ child agent task -> execution role A
    ├─ child agent task -> execution role B
    └─ child agent task -> execution role C
                         ↓
                 durable role branch
                         ↓
              one master integration slot
                         ↓
                      master
```

Parent metadata lives under `.agents/coordination/parents/`. Task metadata lives under `.agents/coordination/tasks/`.

Rules:

- Child-agent count is not artificially capped; safety comes from path ownership, dependency, lease, role-target, and integration contracts.
- Every child names one `parent_workstream` and one valid `execution_role`.
- A child that targets EHB must fan in to `role/ehb-embedded-integration`.
- Child work cannot bypass its configured durable role branch merely because its human parent is different.
- Parent fanout may be parallel when child paths do not overlap.
- Batch fanout is rollback-safe: a failed child specification must not leave a partially mutated parent/task store.

## Branch topology

`master` is durable product truth.

Short-lived implementation branches use:

```text
agent/<lane>/<task>
```

Human parent coordination branches may use:

```text
work/<ie|ee|cs1|cs2>/<workstream>
```

Normal product flow:

```text
latest master
    ↓ sync durable role branch
role/<execution-role>
    ↓ child/task branch
agent/<lane>/<task>
    ↓ validated fan-in
role/<execution-role>
    ↓ serialized master integration
master
```

Repository-wide governance/bootstrap work may use `agent/quality-release/<task> -> master` when no single product role owns the change.

`agent-coordination` remains the metadata-only coordination branch.

## Parallelism and integration slot

Parallel draft work is allowed. Final master integration is serialized.

- A durable role branch may have up to **3 open feature PRs**.
- Multiple parent workstreams and child tasks may be ACTIVE concurrently when ownership does not overlap.
- Multiple draft/review PRs may exist concurrently.
- **At most one parent/role/governance workstream may occupy the master integration-ready slot at a time.**
- `READY_FOR_INTEGRATION`, `INTEGRATING`, and `MERGED_VERIFYING` count as occupying that slot for parent-level master integration.
- A master-targeting PR is mergeable only when its head contains the exact current `master` base and all required exact-head checks are green.
- If another PR changes `master`, a previously green but now-stale PR must sync and rerun its checks.
- Direct pushes to `master` are forbidden by process and audited by CI.

Use `python scripts/agent_task.py integration-queue` to inspect the parent integration slot.

## Task ownership and leases

Before implementation:

1. read/claim the task when represented in the coordination store;
2. require hard dependencies to be `MERGED_VERIFIED`;
3. declare realistic `touched_paths`;
4. verify no active task owns an overlapping path;
5. target the correct durable execution role;
6. keep the lease heartbeat fresh during material work.

Two active tasks must not own overlapping product paths. Parent/child relationships do not exempt a task from path ownership.

The default lease TTL comes from `.agents/fabric.json`. Stale lease reclaim is allowed only when repository evidence shows the work is no longer active and there is no active integration ownership.

## Child lifecycle and fan-in

Core lifecycle:

`BACKLOG -> READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

Side states: `BLOCKED`, `WAITING_HUMAN`, `CANCELLED`.

Useful operations:

```bash
python scripts/agent_task.py spawn-child ...
python scripts/agent_task.py fanout <parent-id> --spec-file <children.json>
python scripts/agent_task.py claim ...
python scripts/agent_task.py heartbeat ...
python scripts/agent_task.py parent-status <parent-id>
python scripts/agent_task.py integrate-child ...
python scripts/agent_task.py integration-queue
```

A child merged only into a role branch is staging, not final durable completion. `MERGED_VERIFIED` requires verified containment in `master` and recorded integration evidence.

## Feature PR requirements: child/task branch -> role branch

Before merging a child/feature PR into a role branch:

1. head contains the latest target role-branch base;
2. ownership does not overlap an incompatible active task;
3. execution role matches the configured target role branch;
4. targeted tests pass;
5. required repository checks pass on the exact head;
6. deletions/renames are intentional;
7. conflicts are resolved by reviewing both sides, never blind whole-file `ours`/`theirs`.

## Master integration requirements

A role or governance PR may merge to `master` only when:

1. it owns the single master integration slot;
2. its head contains current `master`;
3. `python scripts/verify_feature_preservation.py --base-ref <master-sha>` passes where applicable;
4. `python scripts/agent_fabric_check.py` passes;
5. `python scripts/kreate_check.py` passes;
6. repository Python/data validation passes;
7. frontend typecheck/lint/build passes when included by CI;
8. cross-role/shared-file changes are reconciled;
9. exact-head required CI is green;
10. merge uses a normal merge commit;
11. resulting `master` passes post-merge verification.

No previously green SHA is grandfathered after the head or base moves.

## Shared/high-conflict surfaces

Treat these as shared:

- `AGENTS.md`
- `.agents/**`
- `.github/**`
- root build/deployment configuration
- dependency lockfiles
- shared API/data contracts
- feature registry
- KREATE claim/evidence policy files

Changes to these surfaces require broad repository validation and explicit preservation of valid concurrent changes.

## Hardware ownership boundary

Hardware work is first-class engineering work. Detailed execution rules live in `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`.

Ownership is split deliberately:

- **EE:** measurement architecture, sensor/measurement selection, calibration, uncertainty, field verification.
- **EHB:** embedded electronics, PCB, firmware, communications, device-side power/interface implementation, bring-up, buffering/recovery, HW/SW integration.
- **Shared:** system verification and `ee-ehb-interface-contract`.
- **CS1 consumer review:** required when device/schema/timing/calibration/quality semantics can alter inference or decision behavior.

The canonical handoff template is `KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`.

Hardware evidence labels are exactly:

- `ASSUMPTION`
- `DATASHEET`
- `CALCULATION`
- `SIMULATION`
- `BENCH_TEST`
- `FIELD_TEST`
- `PRODUCTION_EVIDENCE`

Simulation, CAD, a datasheet value, or AI-generated design output is not bench evidence.

Physical actions that create real risk remain subject to `PHYSICAL_SAFETY`. Design, calculation, simulation, coding, and non-energized review remain autonomous.

## Plugin and specialized-tool policy

Agents may proactively use available plugins, connectors, and specialized tools when they materially improve execution or verification. Detailed policy lives in `.agents/PLUGIN_POLICY.md`.

- Never fabricate plugin availability or plugin-derived evidence.
- Prefer connected specialized tooling over weaker manual imitation when it provides stronger evidence.
- Missing optional tooling is not automatically a human gate; continue safe independent work.
- If a missing capability is genuinely required for acceptance, record the blocker precisely.
- Use least privilege and normal authorization flows; never place secrets in repository files.

Plugin output retains its real evidence class.

## Human-by-exception policy

Default mode is autonomous inside accepted scope.

Human input is required only for:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

Routine branch/PR creation, reversible refactors, conflict resolution, tests, merge execution, child fanout, plugin discovery, and ordinary technical decisions are not human gates.

## Role-specific post-work checkpoint

- **IE: CHECKPOINT ON**
- **CS2: CHECKPOINT ON**
- **EE: CHECKPOINT OFF**
- **EHB: CHECKPOINT OFF**
- **CS1: CHECKPOINT OFF**

The four-human parent model does not invent a fifth human checkpoint owner for EHB. EHB is an independent execution role coordinated through the existing team structure.

## Merge-before-completion contract

`PR opened`, `feature PR merged to role branch`, `review ready`, or `tests green on a feature branch` are not final completion states.

For accepted work to become `MERGED_VERIFIED`:

1. validated implementation reaches its configured durable role/integration surface;
2. the master integration PR passes exact-head CI;
3. the PR merges to `master` using a normal merge commit;
4. resulting `master` passes post-merge verification;
5. `python scripts/agent_exit_gate.py --branch-head <validated-head>` proves containment when applicable;
6. integration evidence is recorded in coordination state.

## Product truth and evidence boundary

BOUNCAMPUS must not present estimates as live university telemetry.

Unless explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT networks.

Real-world PMR, interviews, pilots, model metrics, hardware performance, climate impact, and savings require their actual evidence class and provenance. Parallel execution never authorizes fabricated evidence.

## Practical release sequence

1. Define a human parent objective when coordination spans multiple child tasks.
2. Fan out independent non-overlapping children to explicit execution roles.
3. Claim/execute children and maintain leases.
4. Merge validated children into their configured durable role branches.
5. Check parent readiness and reconcile shared changes.
6. Claim the single master integration slot.
7. Sync exact current `master`.
8. Run broad exact-head gates.
9. Merge with a normal merge commit.
10. Verify merged `master`.
11. Record integration evidence and mark included work `MERGED_VERIFIED`.

See `.agents/FABRIC.md`, `.agents/PLUGIN_POLICY.md`, `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`, and `docs/development-workflow.md` for the operational protocol.
