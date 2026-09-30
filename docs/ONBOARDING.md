# BOUNCAMPUS Team Onboarding

This guide is for teammates who want to enter the repository and start useful work quickly without reading the entire history first.

## First 30 Minutes

### 0–5 min — Get the repository running

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

The frontend expects Node.js **24.x**.

If you want a local environment file:

```bash
cp .env.example .env.local
```

A separate FastAPI backend is not required for normal frontend work because the active product has co-located Next.js `/api/v1` routes.

### 5–10 min — Understand the current product

Visit these routes in this order:

1. `/demo` — 90-second jury flow.
2. `/food-waste` — core decision workspace.
3. `/food-waste/pilot` — measured pilot evidence workflow.
4. `/data` — source provenance and truth boundary.
5. `/decisions` — human-review decision/outcome loop.

Then read the top-level [`README.md`](../README.md). Do not start by exploring `legacy/`.

### 10–15 min — Know your role

| Role | Mission | Start here |
|---|---|---|
| IE — Customer Discovery & Market Lead | prove who has the problem, who buys, and what evidence supports it | `KREATE/`, PMR issues, interview/evidence artifacts |
| EE — Physical Systems & Measurement Lead | define what can actually be measured and how a pilot would collect it | `KREATE/`, measurement protocol, sensor/instrumentation tasks |
| CS1 — Decision Intelligence Lead | build/test realistic decision logic, uncertainty, evaluation, analytics | `backend/`, `frontend/src`, analytical scripts, model/evaluation issues |
| CS2 — Product Strategy, Evidence Synthesis & Application Lead | turn evidence into a coherent product/application without overclaiming | `KREATE/`, application/product docs, evidence synthesis issues |

You may work outside your default area, but coordinate before touching a path another teammate is actively changing.

### 15–20 min — Find one bounded task

Open GitHub Issues and prefer an existing KREATE task.

Pick work that satisfies all of these:

- one visible outcome;
- clear acceptance criteria;
- small enough to finish and validate;
- no dependency on unavailable private data;
- no overlap with another teammate's current files;
- no requirement to invent interview/pilot evidence.

Do **not** start with “improve the whole app,” “rewrite the architecture,” or “make the pitch better.” Convert broad goals into one measurable work package first.

### 20–25 min — Create your branch

Start from the latest `master`:

```bash
git checkout master
git pull --ff-only origin master
git checkout -b human/<role>/<task>
```

Examples:

```text
human/cs1/demand-baseline
human/ee/pilot-measurement-sheet
human/ie/interview-guide
human/cs2/evidence-matrix
```

Before editing shared files, run:

```bash
git fetch origin --prune
git branch -r
```

Also check the current open PR. This repository intentionally serializes integration: **at most one integration PR should be open**. You can keep developing a non-conflicting branch while that slot is occupied.

### 25–30 min — Make one change and validate it

For frontend work:

```bash
cd frontend
npm run typecheck
npm run lint
```

Before a merge candidate:

```bash
npm run verify
```

For repository/KREATE changes, from repository root:

```bash
python scripts/kreate_check.py
python scripts/agent_fabric_check.py
python -m compileall -q backend/app scripts
```

Use the checks relevant to your task; the integration owner runs the complete merge gate before merge.

At the end of the first 30 minutes you should have:

- the app running locally;
- your role and current product wedge understood;
- one issue selected;
- a short-lived branch;
- the first bounded change underway;
- no fabricated evidence or conflicting file ownership.

---

## Repository Map

```text
bouncampus/
├── frontend/            active Next.js product and co-located API routes
├── backend/             FastAPI research/backend service
├── KREATE/              hackathon execution, roles, PMR, evidence, application material
├── docs/                maintained product/technical documentation
├── scripts/             repository checks and coordination/release tooling
├── .agents/             machine-readable multi-agent coordination system
├── .github/             CI, issue templates, PR template, feature registry
├── legacy/              old experiments/mocks; not the default place for new work
├── AGENTS.md            full autonomous repository policy
├── CONTRIBUTING.md      human contribution workflow
└── README.md             product overview + team start path
```

## What is the active hackathon wedge?

The current primary KREATE story is **campus food-waste decision intelligence**.

The operating loop is:

```text
public / verified context
        ↓
source health
        ↓
demand / production band
        ↓
readiness or WITHHOLD
        ↓
human approval
        ↓
measured pilot
        ↓
normalized waste scorecard
        ↓
calibration
```

The repository also contains energy, mobility, campus, scenario, mapping, and older experimental surfaces. Those are not permission to dilute the primary jury story. Treat them as preserved expansion capability unless a current task explicitly promotes them.

## Product truth boundary

Do not assume the project has live access to:

- cafeteria POS;
- produced/served portion telemetry;
- individual plate waste;
- university BMS/smart meters;
- turnstile or Wi-Fi occupancy;
- shuttle GPS;
- live IoT sensor networks.

Model outputs and scenarios must remain labeled as estimates until measured evidence exists.

The pilot evidence system intentionally starts without synthetic “winning” measurements.

## Role Playbooks

### IE — Customer Discovery & Market Lead

Good first tasks:

- improve the interview guide around one hypothesis;
- structure PMR notes/evidence IDs;
- identify missing evidence for a beachhead/persona claim;
- convert vague customer assumptions into testable interview questions;
- summarize verified interview evidence without adding conclusions not supported by the source.

Avoid:

- writing fictional customer quotes;
- declaring product-market fit from desk research;
- turning an AI-generated persona into `INTERVIEW EVIDENCE`;
- inventing pricing willingness or procurement behavior.

### EE — Physical Systems & Measurement Lead

Good first tasks:

- improve the pilot measurement protocol;
- define sensor-free/manual fallback measurement methods;
- validate what fields can realistically be collected in a cafeteria pilot;
- reduce instrumentation burden;
- define calibration, failure, or data-quality checks.

Avoid:

- assuming hardware access that the team does not have;
- presenting simulated hardware performance as measured;
- introducing physical-risk steps without the required human/safety gate.

### CS1 — Decision Intelligence Lead

Good first tasks:

- create or improve a transparent baseline;
- test signal contribution/ablation;
- improve uncertainty/readiness logic;
- implement data-quality checks;
- improve pilot scoring/evaluation;
- connect model decisions to explicit costs/guardrails.

Prefer interpretable and testable logic over impressive but unverifiable ML. The hackathon value is the decision loop plus evidence, not model complexity by itself.

Avoid:

- training on invented labels;
- presenting synthetic metrics as real performance;
- optimizing only forecast accuracy while ignoring service failure/early-sellout costs.

### CS2 — Product Strategy, Evidence Synthesis & Application Lead

Good first tasks:

- build an evidence matrix for application claims;
- tighten product narrative around verified evidence;
- identify contradictions between product UI, application, pitch, and PMR;
- improve the jury flow without introducing unsupported claims;
- turn IE/EE/CS1 outputs into a coherent application section.

Avoid:

- polishing unsupported claims until they sound factual;
- changing the core beachhead/product direction without the product-direction checkpoint;
- expanding scope just because an old feature exists in the repository.

## Development Paths

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Useful scripts:

```bash
npm run typecheck
npm run lint
npm run build
npm run verify
```

`npm run verify` is the frontend convenience gate for typecheck + lint + production build.

### FastAPI research backend

Only start it when your task needs it:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The Dockerfile uses Python 3.11 and serves `app.main:app` on port 8000.

### Docker Compose

A root `docker-compose.yml` exists for the frontend/backend stack. Local Next.js-only development is usually faster for normal UI/product work; use Compose when your task specifically needs the separate FastAPI service or integrated container behavior.

## Before You Commit

Check your diff:

```bash
git status
git diff
```

Ask:

- Did I touch only files required for this task?
- Did I accidentally copy something from `legacy/`?
- Did I remove a feature or route unintentionally?
- Did I add a factual claim without evidence?
- Did I leave debug data, generated artifacts, secrets, or local environment files?
- Can another teammate understand why this change exists from the commit message?

Example commit messages:

```text
feat(food): add source-health warning state
fix(pilot): guard zero served portions
docs(pmr): clarify interview evidence labeling
test(decision): cover WITHHOLD on missing schedule
```

## Before You Ask for Merge

Read [`CONTRIBUTING.md`](../CONTRIBUTING.md) and use the repository PR template.

Minimum expectations:

- scope is bounded;
- latest `master` has been considered;
- relevant tests/checks pass;
- screenshots are included for material UI changes when useful;
- evidence IDs or assumption labels accompany claim-bearing changes;
- known limitations are stated;
- no second integration PR is opened while the slot is occupied.

## AI / Agent Collaboration

AI agents are implementation accelerators, not evidence sources.

Good delegation:

- “implement this accepted issue and run the checks”;
- “find contradictions between these evidence IDs and UI claims”;
- “write tests for this decision rule”;
- “refactor this bounded component without changing behavior.”

Bad delegation:

- “invent PMR so we can submit”;
- “create realistic interview results”;
- “make the pilot numbers look good”;
- “claim the university has live data access.”

For autonomous agent execution rules, leases, touched paths, merge ownership, and human gates, see [`AGENTS.md`](../AGENTS.md) and `.agents/`.

## Where to Ask a Teammate Instead of Guessing

Ask/coordinate when:

- you are about to edit the same file/feature as another person;
- you need unpublished interview or institutional evidence;
- a change would materially pivot the beachhead or core product;
- an external submission/commitment is involved;
- physical deployment or hardware safety is involved.

Do not wait for approval for routine reversible engineering choices that can be resolved with code inspection, tests, or a bounded experiment.

## Fast Reference

| Need | Read / run |
|---|---|
| Understand product | `README.md`, `/demo`, `/food-waste` |
| Start coding | this file + `CONTRIBUTING.md` |
| See full agent policy | `AGENTS.md` |
| Work on KREATE evidence | `KREATE/` |
| Validate frontend | `cd frontend && npm run verify` |
| Validate KREATE structure | `python scripts/kreate_check.py` |
| Validate agent coordination | `python scripts/agent_fabric_check.py` |
| Avoid old directions | do not start in `legacy/` |

The best first contribution is not the biggest one. It is the smallest change that removes a real blocker, improves evidence quality, or makes the jury-critical decision loop measurably stronger.