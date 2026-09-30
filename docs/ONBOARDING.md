# BOUNCAMPUS Team Onboarding

This guide is for a teammate entering the repository for the first time. The goal is to get you from zero context to a useful, bounded contribution in roughly one focused session.

## First 30 minutes

### 0–5 min — Clone and run the product

```bash
git clone https://github.com/yasinkaya701/bouncampus.git
cd bouncampus
cd frontend
npm ci
npm run dev
```

Open:

```text
http://localhost:3000
```

Requirements:

- Git
- Node.js **24.x**
- Python **3.11+** only for backend/scripts/repository tooling

Optional frontend environment file:

```bash
cp .env.example .env.local
```

A separate FastAPI process is not required for normal frontend work because the active Next.js application has co-located `/api/v1` routes.

### 5–10 min — Understand what we are actually building

Visit in this order:

1. `/demo` — short jury/product story.
2. `/food-waste` — core decision workspace.
3. `/food-waste/pilot` — measured pilot evidence workflow.
4. `/data` — provenance and truth boundary.
5. `/decisions` — human review / outcome loop.

Then read the top section of [`README.md`](../README.md).

The current wedge is **institutional food-waste prevention**. The product should help an operator make a better production decision without pretending estimates are live university telemetry.

Do not begin by exploring `legacy/`.

### 10–15 min — Find your role branch

| Role | Core question | Integration branch |
| --- | --- | --- |
| IE | Who has the problem, who buys, and what does real PMR show? | `role/ie-customer-discovery` |
| EE | What can we reliably measure and validate in the physical operation? | `role/ee-physical-systems` |
| CS1 | Can we make a better decision and prove it with realistic evaluation? | `role/cs1-decision-intelligence` |
| CS2 | What should we build and what can we credibly claim? | `role/cs2-product-strategy` |

Roles are ownership, not permission boundaries. If you identify useful work outside your nominal role, move it forward while keeping the outcome owner visible.

Detailed role documents are under [`KREATE/ROLES/`](../KREATE/ROLES/).

### 15–20 min — Pick one bounded task

Check GitHub Issues and current Pull Requests.

Prefer work with:

- one clear outcome;
- explicit acceptance criteria;
- a small file/area scope;
- a validation method;
- no dependency on unavailable private data;
- no need to fabricate interview/pilot evidence;
- no active overlapping change in the same shared files.

Bad first tasks:

```text
improve the app
redo the architecture
make everything production-ready
make the pitch better
add AI everywhere
```

Better first tasks:

```text
add empty-state copy for the pilot table
validate a demand-baseline edge case
write a measurement checklist for one pilot field
prepare one interview guide for one stakeholder type
trace one application claim back to its evidence ID
```

### 20–25 min — Create a feature branch from the owning role

Fetch current state:

```bash
git fetch origin --prune
```

Example — CS1 task:

```bash
git switch role/cs1-decision-intelligence
git pull --ff-only origin role/cs1-decision-intelligence
git switch -c agent/decision-intelligence/demand-baseline
```

Examples for each role:

```text
agent/customer-discovery/interview-guide
agent/physical-systems/pilot-measurement-sheet
agent/decision-intelligence/forecast-calibration
agent/product-strategy/evidence-matrix
```

Feature PRs go back to the role branch they came from. Role branches later integrate to `master`.

Read [`development-workflow.md`](development-workflow.md) before changing branch topology or shared policy files.

### 25–30 min — Make one change and prove it works

For frontend work:

```bash
cd frontend
npm run typecheck
npm run lint
```

Before integration:

```bash
npm run build
```

Or:

```bash
npm run verify
```

For Python/repository work, from repo root:

```bash
python -m compileall -q backend/app scripts
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
```

Run only the checks relevant to your work during development, but use the full required gates before integration.

## Repository map

### `frontend/`

The active Next.js product.

Typical work:

- pages and components;
- product states;
- visualizations;
- client interactions;
- co-located API routes;
- frontend data contracts.

### `backend/`

FastAPI research/backend service and supporting datasets.

Use it when the task actually belongs in the Python service; do not duplicate logic simply because both stacks exist.

### `KREATE/`

Hackathon/application operating system:

- role definitions;
- PMR/evidence artifacts;
- measurement plans;
- application strategy;
- hardware/pilot material;
- evidence policy.

This area contains claim-bearing material. Evidence quality matters more than polished prose.

### `docs/`

Maintained technical/product documentation. Start with:

- `ONBOARDING.md`
- `development-workflow.md`
- `food-waste-pilot-protocol.md`
- `architecture.md`

### `scripts/`

Repository automation, validation, agent-fabric tooling, release checks.

Changes here can affect CI/repository safety. Test them carefully.

### `.agents/`

Machine-readable multi-agent coordination and policy. Do not casually edit this directory for normal product tasks.

### `legacy/`

Historical experiments and old mocks. Preserve when useful, but do not treat them as active architecture by default.

## What should each role do first?

### IE — Customer Discovery & Market Lead

Start with reality, not application prose.

Good first sequence:

1. read current beachhead/persona assumptions;
2. inspect existing PMR/evidence artifacts;
3. identify one highest-value unknown;
4. prepare or conduct a real interview/research task;
5. record evidence separately from interpretation;
6. update product assumptions only when evidence supports it.

Never generate fake interviews or quotes to fill a gap.

### EE — Physical Systems & Measurement Lead

Start with what a real pilot can measure reliably.

Good first sequence:

1. read the food-waste pilot protocol;
2. inspect current measurement assumptions;
3. choose one uncertain field or sensor/process question;
4. define the cheapest credible measurement method;
5. record limitations and calibration needs;
6. feed feasibility constraints back to IE/CS1/CS2.

Do not add hardware simply because hardware looks impressive.

### CS1 — Decision Intelligence Lead

Start with a realistic baseline and decision cost, not model novelty.

Good first sequence:

1. inspect `/food-waste` and the decision contract;
2. identify what input/output drives an operator decision;
3. test one baseline, edge case, source-quality rule or uncertainty behavior;
4. keep estimates labeled as estimates;
5. add evaluation that can falsify the approach;
6. expose technical constraints to product strategy.

A simple transparent baseline with defensible evaluation is more useful than an impressive model with fake data.

### CS2 — Product Strategy, Evidence Synthesis & Application Lead

Start from evidence and contradictions.

Good first sequence:

1. inspect current problem/beachhead/persona claims;
2. trace important application statements to evidence;
3. mark unsupported statements as hypotheses/unknowns;
4. identify the strongest strategic contradiction;
5. convert evidence into product requirements and application narrative;
6. surface genuine product-direction decisions to the team.

Do not optimize application prose around claims the team cannot defend.

## Working with agents

Agents are support capacity, not evidence sources.

Good uses:

- code implementation;
- test generation and debugging;
- source-backed research synthesis;
- data cleaning/analysis;
- documentation maintenance;
- red-team review;
- repetitive validation.

Bad uses:

- inventing PMR;
- inventing pilot results;
- asserting private university data access;
- fabricating model metrics;
- hiding uncertainty behind polished language.

If an agent changes a shared/high-conflict file, inspect the diff before integration.

## Pull-request model

### Feature PR

```text
agent/<lane>/<task>
        ↓
role/<owning-role>
```

Up to three feature PRs may be open per role branch.

### Role integration PR

```text
role/<owning-role>
        ↓
master
```

A role integration PR must contain current `master`. If another master PR merges first, sync/revalidate before merging.

A feature existing on a role branch is not considered final delivery until it reaches verified `master`.

## Shared files — coordinate before editing

High-conflict areas include:

```text
AGENTS.md
.agents/**
.github/**
root configuration
package-lock files
shared API/data contracts
KREATE evidence-policy files
```

If your task needs one of these, check current PRs first and keep the change as small as possible.

## Evidence checklist

Before writing or merging a material claim, ask:

1. Is this a public fact, measured result, estimate, heuristic, interpretation, hypothesis, or unknown?
2. Where is the source/evidence?
3. Does the wording overstate what the evidence proves?
4. Are limitations visible?
5. Would a skeptical judge understand exactly what is measured versus modeled?

If you cannot answer those questions, downgrade the claim rather than polishing it.

## Before opening a feature PR

Check:

- correct target role branch;
- bounded diff;
- relevant validation passed;
- no unrelated deletions;
- evidence/claim boundary preserved;
- screenshots included for meaningful UI changes;
- limitations disclosed;
- shared-file changes explicitly called out.

Use [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the complete contribution rules.

## Fast links

- [`../README.md`](../README.md) — project + team entrypoint
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution rules
- [`development-workflow.md`](development-workflow.md) — branch/merge architecture
- [`../AGENTS.md`](../AGENTS.md) — full execution policy
- [`../KREATE/ROLES/`](../KREATE/ROLES/) — role playbooks
- [`food-waste-pilot-protocol.md`](food-waste-pilot-protocol.md) — pilot evidence contract

## One sentence to remember

**Pick a bounded question, work from the owning role branch, prove your change, preserve the truth boundary, and do not call it delivered until it reaches verified `master`.**
