# BOUNCAMPUS Repository Working Policy

## Purpose

BOUNCAMPUS is a **four-human, many-agent** KREATE repository.

Each human owns exactly one persistent parent workstream. Any number of autonomous child agents may work beneath that parent when dependencies and path ownership allow it. The repository deliberately avoids an arbitrary agent-count cap; 50+ child agents are valid when their work is independent.

The operating goals are:

1. maximize parallel execution without turning humans into dispatchers;
2. prevent path collisions, stale merges, evidence fabrication, and silent feature loss;
3. keep `master` as durable product truth;
4. require humans only for genuinely critical real-world decisions.

The machine-readable contract lives in `.agents/fabric.json`; detailed execution semantics live in `.agents/FABRIC.md`.

## Four persistent human parent workstreams

| Parent | Role | Parent branch pattern |
| --- | --- | --- |
| `HUMAN-IE` | Customer Discovery & Market Lead | `work/ie/<slug>` |
| `HUMAN-EE` | Physical Systems & Measurement Lead | `work/ee/<slug>` |
| `HUMAN-CS1` | Decision Intelligence Lead | `work/cs1/<slug>` |
| `HUMAN-CS2` | Product Strategy, Evidence Synthesis & Application Lead | `work/cs2/<slug>` |

Exactly one parent workstream exists per role, and one human may not own several active parent workstreams.

Parent workstreams are long-lived accountability boundaries. A verified integration batch does not finish the human's whole role; its audit evidence is appended to `integration_history`, then the parent returns to `ACTIVE` for the next child-agent wave.

## Child-agent model

Normal execution happens on short-lived child branches:

```text
HUMAN-CS1 / work/cs1/kreate
├── agent/api-product/baseline
├── agent/api-product/data-quality
├── agent/api-product/uncertainty
├── agent/quality-release/red-team
└── ... 50+ siblings when safe
```

A child task:

- belongs to exactly one parent via `parent_id`;
- has one leased `owner_agent` using `agent:<identity>`;
- declares `depends_on`, `touched_paths`, acceptance criteria, and validation commands;
- may declare `produces` / `consumes` artifact contracts;
- may be required or optional for the current parent integration batch;
- integrates only into its owning parent branch.

**A child agent never integrates directly to `master`.**

## Branch topology

```text
master
  ↑ normal merge commit, exact-head CI, post-merge verification
work/<role>/<parent>
  ↑ child fan-in
agent/<lane>/<task>
```

`agent-coordination` is the long-lived **metadata-only** coordination branch. Product code, application claims, secrets, and binary release artifacts do not belong there.

Repository-wide governance/bootstrap work that cannot belong to one KREATE parent may use `agent/quality-release/<task>` directly against `master`, but it must still pass the full integration contract.

## Concurrency and ownership

Agent count is not the concurrency limit. Contracts are.

Before a child becomes active:

1. its parent exists and is not complete;
2. hard dependencies are `MERGED_VERIFIED`;
3. any in-fabric producer of a consumed artifact is verified;
4. `touched_paths` do not overlap another active child;
5. no pending/rejected critical human gate blocks the work;
6. the agent owns a valid lease and heartbeat.

Parent/child path overlap counts as conflict. Cross-parent conflicts count exactly the same as same-parent conflicts.

If a newly discovered necessary path overlaps another active child, re-scope, wait, or explicitly coordinate ownership. Do not silently edit the conflicting path.

## Child integration: agent -> parent

Child lifecycle:

```text
BACKLOG -> READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION
        -> INTEGRATING(parent branch) -> MERGED_VERIFIED(parent-contained)
```

Before a child becomes `MERGED_VERIFIED`:

- targeted validation passes;
- the validated child head is recorded;
- child work is integrated into the exact owning parent branch;
- the integrated parent commit is recorded;
- the task's path/dependency/evidence contracts still hold.

A child `MERGED_VERIFIED` means verified inside its parent. Final `master` provenance is recorded by the later parent integration batch.

## Parent readiness and fan-in

A parent batch becomes ready only when:

- at least one new child is verified into the parent;
- all pending `required_for_parent=true` children are `MERGED_VERIFIED`;
- incomplete optional children are explicitly optional;
- the current parent branch represents the combined validated batch.

Previously promoted children recorded in `integration_history` do not make a new empty batch ready.

## Parallel parent PRs, one master integration slot

Up to **4** parent/master PRs may be open concurrently, normally one per human parent.

- At most **1** parent/master PR may be non-draft.
- The non-draft PR owns the master integration slot.
- Other parent PRs remain draft and may receive advisory CI/review.
- Green draft CI is not merge evidence after `master` changes.
- When a parent acquires the integration slot, its branch must contain current `master` and receive fresh exact-head CI.
- Merge uses a normal merge commit.
- Post-merge verification is mandatory.

Parent queue order is deterministic:

1. P0 before P1 before P2;
2. larger dependency-unblocking value;
3. oldest ready timestamp;
4. parent ID tie-break.

## Master integration contract

A parent/master integration is valid only when:

1. parent is first in the queue and owns the sole integration slot;
2. required child work is verified into the parent;
3. parent head contains current `master`;
4. `python scripts/verify_feature_preservation.py --base-ref <master-sha>` passes;
5. `python scripts/test_agent_fabric_check.py` passes;
6. `python scripts/test_agent_task.py` passes;
7. `python scripts/agent_fabric_check.py` passes;
8. `python scripts/kreate_check.py` passes;
9. repository Python/data validation passes;
10. frontend install/typecheck/lint/build passes while those checks remain in CI;
11. exact-head CI is green;
12. merge uses a normal merge commit;
13. resulting `master` passes post-merge audit;
14. `scripts/agent_exit_gate.py` proves integrated-head containment.

After verification, append PR/base/head/merge/timestamp/child IDs to the parent's `integration_history`, clear the current integration slot metadata, and return the parent to `ACTIVE`.

## Shared / high-conflict surfaces

Treat these as shared:

- `AGENTS.md`
- `.agents/**`
- `.github/**`
- root build/deployment configuration
- dependency lockfiles
- shared API/data contracts
- `.github/feature-registry.json`
- KREATE claim/evidence policy files

Changes to these surfaces require broad repository validation and explicit cross-parent impact review.

## Human-by-exception policy

All four roles are autonomous by default. IE and CS2 do **not** have a routine post-task checkpoint anymore.

Human input is required only for:

1. `EVIDENCE_ATTESTATION` — attest a real interview, exact quote, private institutional fact, measured result, or other real-world evidence.
2. `IRREVERSIBLE_ACTION` — destructive/difficult-to-reverse external action, credential revocation/rotation, or repository/account administration.
3. `PHYSICAL_SAFETY` — dangerous hardware energization, actuator motion, mains/high-current work, or consequential field deployment.
4. `EXTERNAL_COMMITMENT` — final submission, purchase/payment, contract/legal acceptance, consequential external message, or binding pilot/date commitment.
5. `PRODUCT_DIRECTION` — material pivot to the agreed beachhead, primary problem, or core product thesis.

Routine architecture, research, PMR planning, model choice, sensor comparison, coding, drafting, testing, documentation, plugin discovery, branch/PR creation, conflict resolution, and merge execution are not human gates.

`WAITING_HUMAN` is reserved for a pending critical gate with one concrete question after all independent work is complete.

## Product truth and KREATE evidence boundary

Parallel autonomy never authorizes fabricated evidence.

Do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT telemetry unless actually integrated and verified.

Do not invent:

- interviews or customer names;
- exact quotes;
- pilot outcomes;
- model accuracy;
- hardware performance;
- live telemetry;
- carbon/water/food savings.

Real-world evidence and application claims remain governed by the stricter evidence system under `KREATE/`.

## Hardware engineering policy

Hardware is first-class engineering work, not demo decoration. The detailed contract lives in `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`.

EE may fan out hardware children into lanes such as:

- `hw-measurement`
- `hw-sensors`
- `hw-power`
- `hw-firmware`
- `hw-pcb`
- `hw-mechanical`
- `hw-calibration`
- `hw-verification`

Hardware evidence must preserve maturity labels:

- `ASSUMPTION`
- `DATASHEET`
- `CALCULATION`
- `SIMULATION`
- `BENCH_TEST`
- `FIELD_TEST`
- `PRODUCTION_EVIDENCE`

A CAD render, schematic, datasheet value, or simulation is not bench evidence.

When custom electronics are justified, agents should create the relevant subset of measurement requirements, block/interface diagrams, error budget, power tree/budget, schematic/PCB constraints, firmware state/failure behavior, data contract, BOM, calibration plan, verification matrix, safety/failure notes, debug/test-point strategy, and DFM/DFT evidence.

Dangerous physical actions remain subject to `PHYSICAL_SAFETY`; design, calculation, CAD, simulation, firmware development, and non-energized review remain autonomous.

## Plugins and specialized tools

Agents may proactively use installed/connected plugins and specialized tools when they materially improve execution or verification.

- Prefer an available specialized capability over a weaker invented workaround.
- Never pretend a plugin/tool exists or was used when it was not discovered/available.
- An agent may ask the user to install/connect/authorize a capability when genuinely needed.
- Optional plugin requests are **not** human-gate blockers; useful work should continue.
- If a missing capability is truly required for acceptance criteria, record the exact blocker.
- Never ask users to paste secrets into repository files/chat when a normal authorization flow exists.
- Tool output keeps its real evidence class: simulation is simulation, CAD is design verification, and remote physical measurements count as physical evidence only with recorded provenance/conditions.

See `.agents/PLUGIN_POLICY.md` for the detailed capability policy.

## Feature preservation

A merge is invalid if an existing feature, route, data source, asset, validation gate, or evidence boundary disappears unintentionally.

Before integration:

- account for every deletion/rename;
- preserve valid work from concurrent parents;
- update the feature registry for new durable capabilities when applicable;
- never resolve product conflicts with blind whole-file `ours`/`theirs`;
- run the full relevant validation gates.

Intentional removal of a registered durable feature requires explicit repository-owner direction.

## Practical execution loop

1. Parent objective exposes bounded child work.
2. Agents fan out non-overlapping child tasks.
3. Agents claim, execute, test, review, and heartbeat independently.
4. Verified children fan into their owning parent.
5. Parent readiness is computed from required pending children.
6. Up to four parent PRs may stay open as drafts.
7. One parent acquires the master integration slot.
8. Sync current `master`, rerun exact-head CI, merge normally.
9. Verify merged `master` and record the immutable batch.
10. Parent returns to `ACTIVE` and starts the next child wave.

See `.agents/FABRIC.md`, `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`, `KREATE/HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`, and `docs/development-workflow.md` for operational details.
