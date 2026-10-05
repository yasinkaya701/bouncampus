# Highest-Information-Value Research / PMR Queue

**Updated:** 2026-10-05
**Goal:** prioritize the unknowns whose resolution changes the largest number of application/product decisions.

## Context

Public KREATE framing says a finished product is not required; the strongest selection advantage therefore comes from evidence that the team understands a real climate problem, a credible customer and an executable path to validation.

The repository already has more technical/product material than customer evidence. New feature work has lower selection value than resolving core workflow hypotheses.

## Priority 0 — Quantity owner + freeze point

### Question
Who actually chooses or approves the next meal's quantity, and when does that quantity become difficult/costly to change?

### Why highest value
Resolves or materially affects:
- Problem intervention point;
- Persona;
- H1;
- product timing;
- recommendation delivery time;
- whether forecasting is useful at all;
- whole-product integration.

### Required evidence
Two or more concrete incident accounts from direct workflow participants, ideally university + contractor/production side.

### Kill outcome
No reachable/control point exists.

---

## Priority 1 — Waste-stage causality

### Question
What fraction / type of avoidable waste actually comes from overproduction versus plate waste, preparation loss, quality/menu issues, food-safety discard or other causes?

### Why
Determines whether production quantity is the right problem rather than an attractive technical solution.

### Required evidence
- operator incidents;
- current waste-stage measurement;
- prospective measurement if existing data cannot separate stages.

### Kill/modify
If production surplus is minor, pivot intervention to the dominant stage.

---

## Priority 2 — Shortage asymmetry / safety buffer

### Question
How costly/disruptive is shortage relative to surplus, and is there a deliberate buffer?

### Why
Determines:
- H3;
- decision loss;
- planning range;
- sellout guardrail;
- operator trust/adoption.

### Required evidence
Recent shortage and surplus examples, not stated preferences alone.

---

## Priority 3 — Contract economics

### Question
Who financially benefits if unnecessary production falls, and who pays when shortage or excess occurs?

### Why
Determines:
- economic buyer;
- sales process;
- contractor vs university beachhead;
- value proposition;
- willingness-to-pay logic.

### Required evidence
Boğaziçi/TEMAŞ contract owner + operations confirmation or authoritative contract clauses.

---

## Priority 4 — Existing planning stack

### Question
What system/heuristic is used today and where exactly does the planned quantity originate?

### Why
Competitor research shows mature ERP/food-waste/forecast tools already exist.

Need to distinguish:

```text
ERP computes quantity
vs
human computes quantity and ERP executes it
```

### Required evidence
Screen/workflow description, production sheet, spreadsheet or system demo from operator where possible.

---

## Priority 5 — Service-level data availability

### Question
Can we obtain or prospectively measure:
- planned;
- produced;
- served;
- edible surplus;
- prep waste;
- plate waste;
- sellout/substitution;
- menu/context?

### Why
Without this, neither model nor pilot can become evidence.

### Required evidence
Source owner + semantic definition + granularity + retention + access path.

---

## Priority 6 — Real persona purchasing criteria

### Question
What does the actual decision owner rank first?

Candidate assumptions:
- service continuity;
- food safety;
- operational reliability;
- timing;
- low friction;
- explainability;
- measurable waste/cost impact;
- integration burden;
- price.

### Why
DE Step 5 requires prioritized purchasing criteria, including rational/emotional/social motivation.

### Required evidence
Real named persona interview(s), not team guesses.

---

## Priority 7 — Second-site same-product test

### Question
Can the same product, language and workflow be used at a second university?

Best targets from secondary research:
- GTÜ: explicit historical/user-count planning + unexpected demand;
- ITU: sophisticated calendar/weather/history/manual forecasting;
- one contractor-led site: tests buyer change.

### Why
Validates beachhead homogeneity and prevents Boğaziçi-only solution design.

---

## Priority 8 — Same sales process / word-of-mouth

### Question
Do these users buy/refer through a repeatable university/contractor network?

### Why
Disciplined Entrepreneurship beachhead condition.

### Evidence needed
- procurement route comparison;
- referral behavior;
- professional peer networks;
- contractor multi-site rollout route;
- introductions from interviewees.

Public secondary evidence is currently insufficient to mark this supported.

---

## Priority 9 — Technical model performance

Only after real target data exists.

Start with:
- same weekday baseline;
- rolling mean/median;
- calendar-aware simple model;
- ERP/current operator forecast;
- richer context model.

Evaluate chronological decision utility, not only RMSE.

### Why below PMR
A highly accurate model for a non-actionable decision is worthless.

---

## Priority 10 — TrayGate technical validation

Only if PMR/data discovery proves post-consumer measurement is decision-critical and unavailable.

Validation sequence:
- controlled tray geometry;
- segmentation;
- leftover bins;
- physical ground-truth comparison;
- volume;
- only then mass.

Do not let hardware research outrank the problem hypothesis.

---

# Application-weight lens

Approximate effect on application sections:

| Unknown | Problem | Beachhead | Persona | PMR | Solution |
| --- | ---: | ---: | ---: | ---: | ---: |
| quantity owner/freeze | HIGH | HIGH | HIGH | HIGH | HIGH |
| waste-stage causality | HIGH | MED | MED | HIGH | HIGH |
| shortage asymmetry | HIGH | MED | HIGH | HIGH | HIGH |
| contract economics | MED | HIGH | HIGH | HIGH | MED |
| incumbent workflow | MED | HIGH | HIGH | HIGH | HIGH |
| data availability | MED | MED | MED | HIGH | HIGH |
| persona priorities | LOW | MED | HIGH | HIGH | HIGH |
| second-site repeatability | MED | HIGH | MED | HIGH | MED |

The first five unknowns dominate.

# Stop rule for secondary research

Secondary research is now strong enough that further browsing should only continue when it:
- identifies a new interview target;
- finds authoritative contract mechanics;
- kills a proposed novelty claim;
- clarifies measurement/legal constraints;
- identifies a directly relevant current incumbent.

Everything else should yield to real PMR.
