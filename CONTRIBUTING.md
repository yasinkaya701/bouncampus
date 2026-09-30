# Contributing to BOUNCAMPUS

BOUNCAMPUS is a fast-moving KREATE for Climate repository. The collaboration model is designed so four humans and supporting agents can work in parallel without turning `master` into a conflict queue or allowing unsupported claims into the product.

If this is your first session, start with [`docs/ONBOARDING.md`](docs/ONBOARDING.md).

## Non-negotiable rules

1. **Do not build routine features directly on `master`.**
2. **Start from the role branch that owns the outcome.**
3. **Keep one task bounded.** One PR should have one clear outcome and acceptance criteria.
4. **Do not silently overwrite active work.** Check issues, PRs and the target branch before touching shared paths.
5. **Validate before merge.** The exact gates depend on what you changed.
6. **Do not invent evidence.** Interviews, quotes, pilot outcomes, model metrics, institutional facts, savings, hardware performance and climate impact require real evidence or an explicit hypothesis/estimate label.
7. **Final delivery means verified `master`.** A feature merged only into a role branch is still in integration.

## Pick the owning role

| Role | Integration branch | Primary ownership |
| --- | --- | --- |
| IE | `role/ie-customer-discovery` | PMR, beachhead, persona/buyer, interview evidence |
| EE | `role/ee-physical-systems` | measurement, instrumentation, physical feasibility, pilot collection |
| CS1 | `role/cs1-decision-intelligence` | decision logic, modeling, uncertainty, evaluation, analytics |
| CS2 | `role/cs2-product-strategy` | product synthesis, evidence integration, application narrative |

These are ownership defaults, not silos. If a task crosses roles, choose the role that owns the **outcome**, then call out the cross-role dependency in the issue/PR.

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

A good first task has:

- one visible result;
- clear acceptance criteria;
- a bounded file set;
- no dependency on unavailable private data;
- no need to fabricate PMR/pilot evidence;
- a validation method you can run yourself.

Avoid starting with goals such as “improve the whole app,” “redo the architecture,” or “make the pitch better.” Split broad goals into testable work packages.

## Create your feature branch

Example for CS1:

```bash
git switch role/cs1-decision-intelligence
git pull --ff-only origin role/cs1-decision-intelligence
git switch -c agent/decision-intelligence/demand-baseline
```

Other examples:

```text
agent/customer-discovery/interview-guide
agent/physical-systems/pilot-measurement-sheet
agent/decision-intelligence/forecast-calibration
agent/product-strategy/evidence-matrix
agent/frontend-ux/pilot-state-empty-screen
```

Use short lowercase slugs. The authoritative branch topology lives in [`docs/development-workflow.md`](docs/development-workflow.md).

## Development loop

Use this loop:

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

Do not expand scope simply because nearby code could also be cleaned up. Open a separate task when work has a separate reason to exist.

## Local setup

Primary product:

```bash
cd frontend
npm ci
npm run dev
```

Requirements: Node.js **24.x**.

Optional environment file:

```bash
cp .env.example .env.local
```

The active frontend includes co-located Next.js `/api/v1` routes, so a separate FastAPI service is not required for normal frontend work.

For FastAPI/repository tooling, use Python **3.11+**.

## Validation

### Frontend change

At minimum:

```bash
cd frontend
npm run typecheck
npm run lint
```

Before integration:

```bash
npm run build
```

Or run the bundled gate:

```bash
npm run verify
```

### Python/backend/scripts change

From repository root:

```bash
python -m compileall -q backend/app scripts
```

Run the relevant targeted tests/scripts for the area you changed.

### KREATE / evidence / repository policy change

```bash
python scripts/kreate_check.py
python scripts/agent_fabric_check.py
```

For a `master` integration candidate, follow the full gates defined by CI and [`AGENTS.md`](AGENTS.md).

## Evidence and anti-slop policy

AI can help research, synthesize, code, test and draft. It cannot create real-world evidence.

Treat material statements as one of:

- public/source-backed fact;
- measured evidence;
- model estimate;
- policy heuristic;
- interpretation;
- hypothesis;
- unknown.

Never silently upgrade a hypothesis to a fact.

Do not fabricate:

- interviews or interview quotes;
- persona validation;
- pilot measurements;
- model accuracy;
- food/water/CO2/cost savings;
- live university telemetry;
- hardware performance;
- user demand or buyer intent.

If evidence is not available, say so and keep the claim bounded.

## Shared / high-conflict files

Treat these as integration-sensitive:

```text
AGENTS.md
.agents/**
.github/**
package-lock files
root configuration
shared API/data contracts
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

agent/physical-systems/measurement-protocol
  → role/ee-physical-systems
```

The repository permits up to three open feature PRs per role branch.

A useful PR explains:

- **What** changed;
- **Why** this task matters;
- **Scope** / touched paths;
- **Validation** run and results;
- **Evidence / truth-boundary impact** when applicable;
- screenshots for meaningful UI changes;
- known limitations.

### Role integration PR

A role branch reaches `master` through its integration PR. Before merging, it must contain current `master`; another master merge may make it stale and require a sync/revalidation.

Use a normal merge commit as required by repository policy.

## Commit messages

Prefer compact, descriptive commits:

```text
feat(food): expose decision readiness reasons
fix(pilot): reject zero served portions
docs(onboarding): add CS1 first-task path
research(pmr): add interview synthesis template
test(food): cover WITHHOLD source-health state
```

Do not use vague messages such as `update`, `changes`, or `fix stuff`.

## Before asking for merge

Check all of these:

- the diff contains only intended work;
- the target branch is correct;
- no unrelated feature disappeared;
- relevant tests/checks pass;
- evidence claims are correctly classified;
- limitations are visible;
- shared-file conflicts are reconciled;
- the PR is small enough for another teammate to review.

## Human decision gates

Routine engineering is not a reason to block on another person. Human input is required for genuinely consequential gates such as:

- real-world evidence attestation;
- irreversible/destructive external actions;
- physical-safety actions;
- purchases, submissions or external commitments;
- genuine product-direction pivots.

See [`AGENTS.md`](AGENTS.md) for the exact contract.

## When in doubt

Use this priority order:

1. preserve evidence integrity;
2. avoid breaking verified product behavior;
3. keep work mergeable and bounded;
4. prefer reversible implementation choices;
5. escalate only decisions that genuinely need a human.
