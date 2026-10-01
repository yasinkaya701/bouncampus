# BOUNCAMPUS Team Onboarding

This guide is for a teammate entering the repository for the first time. The goal is to get from zero context to a useful, bounded contribution in one focused session.

The human team has four people, while the repository exposes five execution roles so embedded/integration work does not overload EE.

## First 30 minutes

### 0–5 min — Clone and run the product

```bash
git clone https://github.com/yasinkaya701/bouncampus.git
cd bouncampus/frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Requirements:

- Git
- Node.js **24.x**
- Python **3.11+** only for backend/scripts/repository tooling

A separate FastAPI process is not required for normal frontend work because the active Next.js application has co-located `/api/v1` routes.

### 5–10 min — Understand what we are building

Visit:

1. `/demo`
2. `/food-waste`
3. `/food-waste/pilot`
4. `/data`
5. `/decisions`

Then read the top section of [`README.md`](../README.md).

The current wedge is **institutional food-waste prevention**. The product should help an operator make a better production decision without pretending estimates are live university telemetry.

Do not begin by exploring `legacy/`.

### 10–15 min — Find your execution role branch

| Role | Core question | Integration branch |
| --- | --- | --- |
| IE | Who has the problem, who buys, and what does real PMR show? | `role/ie-customer-discovery` |
| EE | What should we measure, how accurately, and can we trust the measurement? | `role/ee-physical-systems` |
| EHB | Can we implement electronics/firmware/communications reliably and integrate them with software? | `role/ehb-embedded-integration` |
| CS1 | Can we make a better decision and prove it with realistic evaluation? | `role/cs1-decision-intelligence` |
| CS2 | What should we build and what can we credibly claim? | `role/cs2-product-strategy` |

Roles are ownership, not permission boundaries. Five roles do not mean five humans. PMR remains a four-human process with a 16-interview target.

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
implement one offline-buffer/replay test for EHB
prepare one interview guide for one stakeholder type
trace one application claim back to its evidence ID
```

### 20–25 min — Create a feature branch from the owning role

Fetch current state:

```bash
git fetch origin --prune
```

Example — EHB task:

```bash
git switch role/ehb-embedded-integration
git pull --ff-only origin role/ehb-embedded-integration
git switch -c agent/ehb-firmware/offline-replay
```

Examples:

```text
agent/customer-discovery/interview-guide
agent/hw-measurement/pilot-measurement-sheet
agent/ehb-hardware/controller-board
agent/ehb-comms/scale-gateway
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
npm run build
```

For Python/repository work, from repo root:

```bash
python -m compileall -q backend/app scripts
python scripts/test_agent_fabric_check.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
```

Run targeted checks during development and the full required gates before integration.

## Repository map

### `frontend/`

Active Next.js product: pages/components, product states, visualizations, client interactions, co-located API routes and frontend data contracts.

### `backend/`

FastAPI research/backend service and supporting datasets. Do not duplicate logic simply because both stacks exist.

### `KREATE/`

Hackathon/application operating system: role definitions, PMR/evidence artifacts, measurement plans, hardware/integration artifacts, application strategy and evidence policy.

### `KREATE/HARDWARE/`

Shared EE/EHB hardware execution material. Important files include:

- `HARDWARE_AGENT_PLAYBOOK.md`
- `EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`

Use the interface-contract template when EE and EHB need to work independently against one stable boundary.

### `docs/`

Maintained technical/product documentation. Start with `ONBOARDING.md`, `development-workflow.md`, `food-waste-pilot-protocol.md`, and `architecture.md`.

### `scripts/`

Repository automation, validation, agent-fabric tooling and release checks. Changes here can affect CI/repository safety.

### `.agents/`

Machine-readable multi-agent coordination and policy. Do not casually edit this directory for normal product tasks.

### `legacy/`

Historical experiments and old mocks. Preserve when useful, but do not treat them as active architecture by default.

## What should each role do first?

### IE — Customer Discovery & Market Lead

Start with reality, not application prose. Identify a high-value unknown, conduct/source real research, separate evidence from interpretation, and update assumptions only when evidence supports it.

Never generate fake interviews or quotes.

### EE — Physical Systems & Measurement Lead

Start with what a real pilot must measure reliably.

Good sequence:

1. read the pilot protocol;
2. inspect measurement assumptions;
3. choose one uncertain measurand/method question;
4. define the cheapest credible measurement method;
5. define calibration/uncertainty/acceptance needs;
6. write or update the EE↔EHB interface requirement if embedded implementation is needed;
7. feed measurement constraints to EHB/IE/CS1/CS2.

EE owns measurement truth, not every PCB/firmware task.

### EHB — Embedded Hardware, Communications & Integration Lead

Start from an accepted measurement/interface need rather than inventing hardware.

Good sequence:

1. read the EE requirement and interface contract;
2. identify the smallest embedded implementation that closes the loop;
3. choose controller/interface/connectivity with explicit assumptions;
4. define power, firmware, buffering, protocol and fault behavior;
5. implement/verify one bounded path;
6. return feasibility or interface constraints to EE and CS1;
7. keep evidence labeled as simulation/bench/field honestly.

Do not build a custom PCB if an adapter/off-the-shelf path is better.

### CS1 — Decision Intelligence Lead

Start with a realistic baseline and decision cost, not model novelty. Test baselines, edge cases, source-quality rules or uncertainty; keep estimates labeled; expose technical constraints to product strategy.

When consuming EHB data, review timestamps, invalid/missing representation, quality flags, duplicate/replay semantics and schema versioning.

### CS2 — Product Strategy, Evidence Synthesis & Application Lead

Start from evidence and contradictions. Trace claims, mark unsupported statements as hypotheses/unknowns, convert evidence into product requirements and surface genuine strategic decisions.

Do not optimize prose around claims the team cannot defend.

## EE ↔ EHB coordination

The core rule is:

> **EE defines what must be true about the measurement. EHB defines how the embedded system reliably makes that contract real. Neither silently changes the boundary.**

Changes to voltage/current, pinout, sampling/timing, calibration persistence, protocol/schema, units, quality/error flags, power budget, offline/retry behavior, fault semantics or verification method require explicit interface-contract updates and dual review.

## Working with agents

Agents are support capacity, not evidence sources.

Good uses include code implementation, tests/debugging, source-backed research synthesis, data analysis, documentation maintenance, red-team review, firmware/PCB reasoning and repetitive validation.

Bad uses include inventing PMR, pilot results, private data access, hardware performance or model metrics.

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

A feature existing on a role branch is not final delivery until it reaches verified `master`.

## Shared files — coordinate before editing

High-conflict areas include:

```text
AGENTS.md
.agents/**
.github/**
root configuration
package-lock files
shared API/data contracts
EE↔EHB interface contracts
KREATE evidence-policy files
```

If your task needs one of these, check current PRs first and keep the change bounded.

## Evidence checklist

Before writing or merging a material claim, ask:

1. Is this a public fact, measured result, estimate, heuristic, interpretation, hypothesis or unknown?
2. Where is the source/evidence?
3. Does the wording overstate what the evidence proves?
4. Are limitations visible?
5. Would a skeptical judge understand exactly what is measured versus modeled?

Downgrade unsupported claims rather than polishing them.

## Before opening a feature PR

Check:

- correct target role branch;
- bounded diff;
- relevant validation passed;
- no unrelated deletions;
- evidence/claim boundary preserved;
- interface contract updated/reviewed when applicable;
- screenshots included for meaningful UI changes;
- limitations disclosed;
- shared-file changes explicitly called out.

## Fast links

- [`../README.md`](../README.md)
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- [`development-workflow.md`](development-workflow.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../KREATE/ROLES/`](../KREATE/ROLES/)
- [`../KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`](../KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md)
- [`food-waste-pilot-protocol.md`](food-waste-pilot-protocol.md)

## One sentence to remember

**Pick a bounded question, work from the owning role branch, respect EE↔EHB interface ownership, prove your change, preserve the truth boundary, and do not call it delivered until it reaches verified `master`.**
