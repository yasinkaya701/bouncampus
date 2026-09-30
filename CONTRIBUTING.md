# Contributing to BOUNCAMPUS

BOUNCAMPUS is a fast-moving KREATE for Climate repository. The goal is to let four human teammates and supporting agents work in parallel without losing evidence quality, breaking the demo, or creating an unmergeable PR backlog.

If you are new to the repository, read [`docs/ONBOARDING.md`](docs/ONBOARDING.md) first.

## Core rules

1. **Do not work directly on `master`.** Start from the latest `master` and use a short-lived branch.
2. **Keep one task small enough to review and merge.** Avoid mixed feature/refactor/content batches.
3. **Do not silently overwrite another teammate's work.** Check active issues, open branches, and the current integration PR before editing shared paths.
4. **Run the relevant validation before asking for merge.** Frontend work must at least pass typecheck and lint; merge candidates should pass the full repository gates.
5. **Do not invent evidence.** Interviews, quotes, institutional facts, pilot outcomes, model metrics, savings, hardware performance, and climate-impact claims require real evidence or must remain explicitly labeled as hypotheses/estimates.
6. **Human decisions stay human where required.** External commitments, evidence attestation, irreversible actions, physical-safety actions, and genuine product-direction pivots require the appropriate human gate.

The full autonomous/agent policy is in [`AGENTS.md`](AGENTS.md). Humans do not need to memorize it before starting, but work merged to the repository must remain compatible with it.

## Team roles

| Role | Primary ownership | Typical repository areas |
|---|---|---|
| IE — Customer Discovery & Market Lead | PMR, beachhead, buyer/persona, interview evidence | `KREATE/`, PMR/evidence docs, application inputs |
| EE — Physical Systems & Measurement Lead | measurement design, instrumentation, feasibility, field protocol | `KREATE/`, measurement/hardware docs, data-collection interfaces |
| CS1 — Decision Intelligence Lead | modeling, uncertainty, decision logic, evaluation | `backend/`, decision logic, analytical scripts, model/evaluation docs |
| CS2 — Product Strategy, Evidence Synthesis & Application Lead | product synthesis, application narrative, evidence integration | `KREATE/`, product docs, application material, cross-functional synthesis |

Roles are ownership defaults, not silos. Cross-role work is encouraged when the owner of the affected area is visible and conflicts are avoided.

## Before starting work

Update your local copy:

```bash
git checkout master
git pull --ff-only origin master
```

Check what is already in flight:

```bash
git fetch origin --prune
git branch -r
```

Also check GitHub Issues and the currently open pull request. This repository intentionally keeps **at most one integration PR open at a time**. If the integration slot is occupied, you may continue non-conflicting work on your branch, but do not open a second parking-lot PR.

## Branch naming

For human work, use a short descriptive branch:

```text
human/<role>/<task>
```

Examples:

```text
human/cs1/demand-baseline
human/ee/measurement-protocol
human/ie/pmr-interview-guide
human/cs2/application-evidence-pass
```

Agent-owned work continues to use the repository's `agent/<lane>/<task>` convention defined in [`AGENTS.md`](AGENTS.md).

## Pick work from an issue

Prefer an existing KREATE issue before inventing a new task. A good issue has:

- one clear outcome;
- acceptance criteria;
- explicit evidence needs when claims are involved;
- a bounded file/area scope;
- no hidden dependency on another teammate's unmerged work.

If you need a new issue, use the existing **KREATE task** issue template.

## Local setup

The primary product surface is the Next.js application in `frontend/`.

Requirements:

- Node.js **24.x**;
- npm;
- Python **3.11+** only if you are working on the FastAPI research backend/scripts;
- Git.

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Optional environment file:

```bash
cp .env.example .env.local
```

The default frontend can use its co-located Next.js `/api/v1` routes, so a separate backend is not required for normal UI work.

Research backend, when needed:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Development loop

Use this sequence for normal work:

```text
Issue / acceptance criteria
        ↓
latest master
        ↓
short-lived branch
        ↓
small implementation
        ↓
local validation
        ↓
self-review diff
        ↓
integration slot
        ↓
PR
        ↓
CI + review
        ↓
merge
```

Keep changes easy to reason about. If a task starts touching unrelated product surfaces, split it before the diff becomes difficult to merge.

## Validation

### Frontend-only change

```bash
cd frontend
npm run typecheck
npm run lint
```

Before an integration candidate is merged:

```bash
cd frontend
npm run verify
```

`npm run verify` runs typecheck, lint, and production build.

### Repository/KREATE checks

From repository root, the merge path may also require:

```bash
python scripts/kreate_check.py
python scripts/agent_fabric_check.py
python -m compileall -q backend/app scripts
```

Feature-preservation and exit-gate commands are integration-owner responsibilities and are documented in [`AGENTS.md`](AGENTS.md) and the PR template.

## Commit style

Prefer small, descriptive commits:

```text
docs: clarify PMR interview evidence flow
feat(food): expose source-health reason codes
fix(demo): preserve readiness state on refresh
test(pilot): cover early-sellout guardrail
```

Avoid generic messages such as `update`, `stuff`, `changes`, or `final`.

## Pull requests

Before opening a PR:

- rebase/merge the latest `master` into your branch using the repository's current integration policy;
- inspect every changed file;
- remove debug output and accidental generated files;
- run the relevant validation;
- document evidence IDs or limitations for claim-bearing changes;
- confirm the repository does not already have another open integration PR.

The PR description should answer:

1. What changed?
2. Why does it matter for KREATE or the product?
3. What did you test?
4. What evidence or assumptions changed?
5. What is intentionally not solved by this PR?

## Evidence and AI usage

AI tools may help with coding, analysis, drafting, testing, summarization, or repository work. They may **not** manufacture real-world evidence.

Never merge AI-generated content that presents any of the following as real without verification:

- interviews or quotes;
- customer demand;
- institutional/private data;
- pilot measurements;
- model accuracy;
- hardware test results;
- saved kilograms, money, CO2, water, or energy;
- external approvals or commitments.

Use the repository's evidence labels and IDs. If evidence does not exist yet, write `HYPOTHESIS`, `MODEL_ESTIMATE`, `POLICY_HEURISTIC`, or `UNKNOWN` as appropriate instead of making the text sound certain.

## Do not edit legacy by accident

`legacy/` exists to preserve older experiments and mock/product directions. Do not revive or copy legacy behavior into the primary KREATE path unless an issue explicitly requires it.

For current work, prefer:

- `frontend/` for the active product;
- `backend/` for research/backend logic;
- `KREATE/` for competition execution and evidence;
- `docs/` for maintained technical/product documentation;
- `.agents/` and `AGENTS.md` for autonomous coordination policy.

## Need the fast path?

Read [`docs/ONBOARDING.md`](docs/ONBOARDING.md) and complete the **First 30 Minutes** checklist. After that, you should be able to run the product, find your role-specific starting area, select a bounded issue, and begin development without reading the entire repository history.