# Contributing to BOUNCAMPUS

BOUNCAMPUS is a fast-moving KREATE for Climate repository. The collaboration model is designed so four humans and supporting agents can work through **five execution roles** without turning `master` into a conflict queue or allowing unsupported claims into the product.

If this is your first session, start with [`docs/ONBOARDING.md`](docs/ONBOARDING.md).

## Non-negotiable rules

1. **Do not build routine features directly on `master`.**
2. **Start from the role branch that owns the outcome.**
3. **Keep one task bounded.** One PR should have one clear outcome and acceptance criteria.
4. **Do not silently overwrite active work.** Check issues, PRs and the target branch before touching shared paths.
5. **Validate before merge.** The exact gates depend on what you changed.
6. **Do not invent evidence.** Interviews, quotes, pilot outcomes, model metrics, institutional facts, savings, hardware performance and climate impact require real evidence or an explicit hypothesis/estimate label.
7. **Final delivery means verified `master`.** A feature merged only into a role branch is still in integration.
8. **EE↔EHB boundary changes require explicit interface coordination and dual review.**

## Pick the owning role

| Role | Integration branch | Primary ownership |
| --- | --- | --- |
| IE | `role/ie-customer-discovery` | PMR, beachhead, persona/buyer, interview evidence |
| EE | `role/ee-physical-systems` | measurement architecture, calibration, uncertainty, field/pilot measurement validity |
| EHB | `role/ehb-embedded-integration` | embedded electronics, PCB, firmware, communications, bring-up, HW↔SW integration |
| CS1 | `role/cs1-decision-intelligence` | decision logic, modeling, uncertainty, evaluation, analytics |
| CS2 | `role/cs2-product-strategy` | product synthesis, evidence integration, application narrative |

These are ownership defaults, not silos. Five execution roles do not imply five humans; the human team remains four people and the PMR target remains 16 interviews.

If a task crosses roles, choose the role that owns the **outcome**, then call out the cross-role dependency in the issue/PR.

For EE↔EHB work, use [`KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`](KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md) when the task changes shared electrical/data/timing/power/fault assumptions.

## Before you start

Fetch current remote state:

```bash
git fetch origin --prune
```

Inspect open work before choosing shared files:

```bash
git branch -r
```

Also check GitHub Issues and Pull Requests. Prefer an existing KREATE task with clear acceptance criteria.

A good first task has one visible result, clear acceptance criteria, bounded paths, no dependency on unavailable private data, no need to fabricate evidence, and a validation method you can run yourself.

## Create your feature branch

Example for EHB:

```bash
git switch role/ehb-embedded-integration
git pull --ff-only origin role/ehb-embedded-integration
git switch -c agent/ehb-firmware/offline-replay
```

Other examples:

```text
agent/customer-discovery/interview-guide
agent/hw-measurement/pilot-measurement-sheet
agent/ehb-hardware/controller-board
agent/ehb-comms/scale-gateway
agent/decision-intelligence/forecast-calibration
agent/product-strategy/evidence-matrix
agent/frontend-ux/pilot-state-empty-screen
```

Use short lowercase slugs. The authoritative branch topology lives in [`docs/development-workflow.md`](docs/development-workflow.md).

## Development loop

```text
issue / question
      ↓
small implementation or evidence artifact
      ↓
run targeted validation
      ↓
self-review diff + truth boundary
      ↓
feature PR → owning role branch
      ↓
review / CI / merge
      ↓
role branch → master integration
      ↓
post-merge verification
```

Do not expand scope simply because nearby code could also be cleaned up.

## Local setup

```bash
cd frontend
npm ci
npm run dev
```

Requirements: Node.js **24.x**. For FastAPI/repository tooling, use Python **3.11+**.

The active frontend includes co-located Next.js `/api/v1` routes, so a separate FastAPI service is not required for normal frontend work.

## Validation

### Frontend change

```bash
cd frontend
npm run typecheck
npm run lint
npm run build
```

Or:

```bash
npm run verify
```

### Python/backend/scripts change

From repository root:

```bash
python -m compileall -q backend/app scripts
```

Run targeted tests/scripts for the area you changed.

### KREATE / evidence / repository policy change

```bash
python scripts/test_agent_fabric_check.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
```

For a `master` integration candidate, follow the full gates defined by CI and [`AGENTS.md`](AGENTS.md).

## EE ↔ EHB handoff rule

EE defines what must be true about the measurement. EHB implements the embedded path that makes the contract real.

Use a shared interface contract when changing any of:

- voltage/current;
- connector/pinout;
- ADC/reference/excitation;
- sampling/timing;
- calibration storage/semantics;
- protocol/payload schema;
- units/scaling;
- quality/error flags;
- power budget;
- startup/shutdown;
- offline/retry/replay behavior;
- fault semantics;
- verification method.

EE reviews measurement correctness; EHB reviews implementation correctness; CS1 reviews downstream data semantics when affected.

## Evidence and anti-slop policy

AI can help research, synthesize, code, test and draft. It cannot create real-world evidence.

Treat material statements as public/source-backed fact, measured evidence, model estimate, policy heuristic, interpretation, hypothesis, or unknown.

Do not fabricate interviews, pilot measurements, model accuracy, food/water/CO2/cost savings, live university telemetry, hardware performance, or buyer intent.

Hardware evidence must preserve the repository labels: `ASSUMPTION`, `DATASHEET`, `CALCULATION`, `SIMULATION`, `BENCH_TEST`, `FIELD_TEST`, `PRODUCTION_EVIDENCE`.

## Shared / high-conflict files

Treat these as integration-sensitive:

```text
AGENTS.md
.agents/**
.github/**
package-lock files
root configuration
shared API/data contracts
EE↔EHB interface contracts
KREATE evidence-policy files
```

Before changing them, check current PRs and latest target branch. Mention the shared-file change explicitly in the PR and run broad validation.

## Pull requests

### Feature PR

Target the owning role branch, not `master`.

Examples:

```text
agent/decision-intelligence/demand-baseline
  → role/cs1-decision-intelligence

agent/hw-measurement/measurement-protocol
  → role/ee-physical-systems

agent/ehb-firmware/offline-replay
  → role/ehb-embedded-integration
```

The repository permits up to three open feature PRs per role branch.

A useful PR explains what changed, why it matters, touched paths, validation results, truth/evidence impact, cross-role contract impact, screenshots where useful, and known limitations.

### Role integration PR

A role branch reaches `master` through its integration PR. Before merging, it must contain current `master`; another master merge may make it stale and require a sync/revalidation.

Use a normal merge commit as required by repository policy.

## Commit messages

Prefer compact, descriptive commits:

```text
feat(food): expose decision readiness reasons
feat(ehb): add offline telemetry replay
fix(pilot): reject zero served portions
docs(onboarding): add EHB first-task path
test(agents): pin EHB role contract
```

## Before asking for merge

Check all of these:

- intended bounded diff;
- correct target branch;
- no unrelated feature disappeared;
- relevant tests/checks pass;
- evidence claims are correctly classified;
- limitations are visible;
- shared-file conflicts are reconciled;
- EE↔EHB dual review is complete when required;
- the PR is small enough to review.

## Human decision gates

Routine engineering is not a reason to block on another person. Human input is required for real-world evidence attestation, irreversible/destructive actions, physical-safety actions, purchases/submissions/external commitments, and genuine product-direction pivots.

EE, EHB and CS1 are technical checkpoint-OFF roles; ordinary architecture choices are autonomous. See [`AGENTS.md`](AGENTS.md) for the exact contract.

## When in doubt

Use this priority order:

1. preserve evidence integrity;
2. preserve measurement/interface truth;
3. avoid breaking verified product behavior;
4. keep work mergeable and bounded;
5. prefer reversible implementation choices;
6. escalate only decisions that genuinely need a human.
