# BOUNCAMPUS

**Campus food-waste decision intelligence for KREATE for Climate.**

BOUNCAMPUS turns a measured institutional food-waste problem into an uncertainty-aware, human-approved operating decision and a falsifiable pilot.

## Product thesis

Boğaziçi University publicly reports 48,251 kg of food waste in 2025. BOUNCAMPUS does not claim live cafeteria telemetry; it combines source-backed context with transparent decision logic, exposes uncertainty, requires operator approval, and measures whether the intervention actually reduces normalized waste.

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

The pre-registered target is at least 10% lower normalized waste versus matched control without increasing early sell-outs. This is a target, not an achieved result.

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

## Validation

```bash
cd frontend
npm ci --no-audit --no-fund
npm run typecheck
npm run lint
npm run build
```

Repository-level validation:

```bash
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
```

## Team development model

The repository supports parallel work by all four KREATE roles.

Long-lived integration branches:

| Role | Branch |
| --- | --- |
| IE | `role/ie-customer-discovery` |
| EE | `role/ee-physical-systems` |
| CS1 | `role/cs1-decision-intelligence` |
| CS2 | `role/cs2-product-strategy` |

Create short-lived `agent/<lane>/<task>` branches from the owning role branch and open feature PRs back into that role branch.

Multiple PRs may be open concurrently. Up to 3 feature PRs may target one role branch, and each role may have one role-to-`master` integration PR open. A `master` PR must contain current `master` and pass exact-head CI; if another PR merges first, stale PRs must sync and revalidate.

Final delivery exists only on verified `master`.

Detailed rules:

- [`AGENTS.md`](AGENTS.md)
- [`.agents/FABRIC.md`](.agents/FABRIC.md)
- [`docs/development-workflow.md`](docs/development-workflow.md)

## KREATE role system

- IE — Customer Discovery & Market Lead
- EE — Physical Systems & Measurement Lead
- CS1 — Decision Intelligence Lead
- CS2 — Product Strategy, Evidence Synthesis & Application Lead

Role documents live under [`KREATE/ROLES/`](KREATE/ROLES/).

## Key documentation

- [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)
- [`docs/kreate-winning-product.md`](docs/kreate-winning-product.md)
- [`docs/jury-demo-script.md`](docs/jury-demo-script.md)
- [`docs/pitch.md`](docs/pitch.md)
- [`docs/jury-q-and-a.md`](docs/jury-q-and-a.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/assumptions.md`](docs/assumptions.md)

## KREATE timeline

- Application / evidence stage: optimize for PMR, problem clarity, beachhead/persona quality, measurement feasibility, decision-intelligence credibility, and coherent application claims.
- Hackathon: 15 October 2026, İstanbul.
