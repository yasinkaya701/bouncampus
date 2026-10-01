# BOUNCAMPUS

**Campus food-waste decision intelligence for KREATE for Climate.**

## Team — start here

If you just joined the team, you should be able to clone the repo, understand your lane, run the product, choose a bounded task, and start contributing without reading the entire repository first.

### 5-minute local start

Requirements:

- Git
- Node.js **24.x**
- Python **3.11+** only when you touch backend/repository tooling

```bash
git clone https://github.com/yasinkaya701/bouncampus.git
cd bouncampus/frontend
npm ci
npm run dev
```

Open `http://localhost:3000` and check these first:

1. `/demo`
2. `/food-waste`
3. `/food-waste/pilot`
4. `/data`

Then use:

- **[`docs/ONBOARDING.md`](docs/ONBOARDING.md)** — first 30 minutes in the repo
- **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — branch, issue, validation and PR rules
- **[`docs/development-workflow.md`](docs/development-workflow.md)** — authoritative parallel merge model
- **[`AGENTS.md`](AGENTS.md)** — full human/agent execution policy

### Five execution roles, four human team members

| Role | Owns the question | Long-lived integration branch |
| --- | --- | --- |
| **IE — Customer Discovery & Market Lead** | Who has the problem, who buys, and what does real PMR show? | `role/ie-customer-discovery` |
| **EE — Physical Systems & Measurement Lead** | What should we measure, how accurately, and can we trust it? | `role/ee-physical-systems` |
| **EHB — Embedded Hardware, Communications & Integration Lead** | Can we implement the electronics/firmware/comms path reliably and connect it to software? | `role/ehb-embedded-integration` |
| **CS1 — Decision Intelligence Lead** | Can we make a better operating decision and prove it? | `role/cs1-decision-intelligence` |
| **CS2 — Product Strategy, Evidence Synthesis & Application Lead** | What should we build and what can we credibly claim? | `role/cs2-product-strategy` |

Roles are ownership defaults, not silos. There are still four human team members; execution-role count does not change the PMR target of 16 interviews.

EE owns measurement truth (measurement architecture, calibration, uncertainty, field validity). EHB owns embedded implementation (electronics, PCB, firmware, communications, bring-up, HW↔SW integration). Cross-boundary changes use an explicit EE↔EHB interface contract and dual review.

### Normal development flow

```text
pick one bounded issue
        ↓
choose the owning role branch
        ↓
sync that role branch
        ↓
create agent/<lane>/<task>
        ↓
implement + validate
        ↓
feature PR → role branch
        ↓
role integration PR → master
        ↓
post-merge verification
```

Do not start new work from stale local `master`. Do not commit routine feature work directly to `master`. Final delivery exists only after the change reaches verified `master`.

### Fast validation

Frontend work:

```bash
cd frontend
npm run typecheck
npm run lint
```

Before an integration candidate:

```bash
cd frontend
npm run verify
```

Repository/KREATE checks when relevant:

```bash
python scripts/test_agent_fabric_check.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
```

### Repository map

```text
frontend/      active Next.js product and co-located /api/v1 routes
backend/       FastAPI research/backend service
KREATE/        role docs, PMR, evidence, application and hackathon execution
docs/          maintained product, onboarding and technical documentation
scripts/       validation, coordination and release tooling
.agents/       autonomous multi-agent coordination and policy
legacy/        old experiments/mocks; not the default place for new work
```

---

## Product thesis

BOUNCAMPUS turns a measured institutional food-waste problem into an uncertainty-aware, human-approved operating decision and a falsifiable pilot.

Boğaziçi University publicly reports **48,251 kg** of food waste in 2025. BOUNCAMPUS does not claim live cafeteria telemetry; it combines source-backed context with transparent decision logic, exposes uncertainty, requires operator approval, and measures whether the intervention actually reduces normalized waste.

```text
OFFICIAL BASELINE + CONTEXT
        ↓
SOURCE HEALTH
        ↓
DEMAND / PRODUCTION BAND
        ↓
PILOT_READY / REVIEW_REQUIRED / WITHHOLD
        ↓
HUMAN OPERATOR GATE
        ↓
MATCHED PILOT
        ↓
WASTE KG / 100 SERVED
        ↓
MEASURED SCORECARD
```

The primary pilot metric is:

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

The pre-registered target is at least **10% lower normalized waste** versus matched control without increasing early sell-outs. This is a target, not an achieved result.

## Core surfaces

| Surface | Purpose |
| --- | --- |
| `/` | KREATE command center and official problem baseline |
| `/food-waste` | Decision workspace, source health, operator gate, scenario and pilot contract |
| `/food-waste/pilot` | Pilot Evidence Lab |
| `/demo` | 90-second jury flow |
| `/decisions` | Human-review decision ledger |
| `/data` | Source provenance and truth boundary |
| `/lab` | Experimental/future modules |

Important API routes:

```text
GET  /api/v1/food
GET  /api/v1/food/pilot-template
GET  /api/v1/food/pilot-score
POST /api/v1/food/pilot-score
GET  /api/v1/health
```

## Truth boundary

BOUNCAMPUS distinguishes public facts, model estimates, hypotheses, and measured pilot evidence.

Do not claim access to cafeteria POS, actual produced/served portions before a pilot, university BMS/smart meters, turnstiles, Wi-Fi occupancy telemetry, shuttle GPS, or live IoT networks unless the source is explicitly integrated and verified.

Do not state achieved food, CO2, water, cost, or service improvements before measured pilot evidence supports the claim.

## Run locally

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Optional frontend environment file:

```bash
cp .env.example .env.local
```

The active frontend can use co-located Next.js `/api/v1` routes, so a separate FastAPI process is not required for normal frontend development.

## Full validation

```bash
cd frontend
npm ci --no-audit --no-fund
npm run typecheck
npm run lint
npm run build
```

From repository root:

```bash
python scripts/test_agent_fabric_check.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
```

## Parallel development model

The repository uses five long-lived execution-role integration branches:

| Role | Branch |
| --- | --- |
| IE | `role/ie-customer-discovery` |
| EE | `role/ee-physical-systems` |
| EHB | `role/ehb-embedded-integration` |
| CS1 | `role/cs1-decision-intelligence` |
| CS2 | `role/cs2-product-strategy` |

Create short-lived `agent/<lane>/<task>` branches from the role that owns the outcome and open feature PRs back into that role branch.

Typical EHB task lanes are `ehb-hardware`, `ehb-firmware`, `ehb-comms`, `ehb-integration`, and `ehb-verification`.

Multiple PRs may be open concurrently. Up to three feature PRs may target one role branch, and each role may have one role-to-`master` integration PR open. Every `master` integration must contain current `master`; stale integration branches must sync and revalidate.

High-conflict files such as `AGENTS.md`, `.agents/**`, `.github/**`, root configuration, lockfiles, shared contracts, EE↔EHB interface contracts, and evidence-policy files require explicit coordination and broad validation.

See [`docs/development-workflow.md`](docs/development-workflow.md) for the exact merge model.

## KREATE role system

Role documents live under [`KREATE/ROLES/`](KREATE/ROLES/):

- IE — Customer Discovery & Market Lead
- EE — Physical Systems & Measurement Lead
- EHB — Embedded Hardware, Communications & Integration Lead
- CS1 — Decision Intelligence Lead
- CS2 — Product Strategy, Evidence Synthesis & Application Lead

Hardware coordination artifacts live under [`KREATE/HARDWARE/`](KREATE/HARDWARE/), including the EE↔EHB interface-contract template.

## Key documentation

- [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`docs/development-workflow.md`](docs/development-workflow.md)
- [`KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`](KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md)
- [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)
- [`docs/kreate-winning-product.md`](docs/kreate-winning-product.md)
- [`docs/jury-demo-script.md`](docs/jury-demo-script.md)
- [`docs/pitch.md`](docs/pitch.md)
- [`docs/jury-q-and-a.md`](docs/jury-q-and-a.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/assumptions.md`](docs/assumptions.md)

## KREATE timeline

- **Application deadline:** 8 October 2026, 23:59
- **Top-15 selection announcement:** 9 October 2026
- **Hackathon:** 15 October 2026, İstanbul

Until the application deadline, optimize for PMR evidence, problem clarity, beachhead/persona quality, measurement feasibility, embedded/integration credibility, decision-intelligence credibility, and coherent claims. Product polish is valuable only when it supports those priorities.
