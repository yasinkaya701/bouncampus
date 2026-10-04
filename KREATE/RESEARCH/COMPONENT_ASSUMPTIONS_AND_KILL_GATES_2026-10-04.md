# Component Assumptions & Kill Gates — 2026-10-04

**Purpose:** decompose the three application PMR hypotheses into narrow assumptions that can fail independently.  
**Method:** Disciplined Entrepreneurship Step 20 — https://www.d-eship.com/step20/  
**Status:** research design only; no assumption below is validated unless linked later to admissible evidence.

## Why this exists

The form asks for three hypotheses. A good application can present three concise hypotheses, but execution needs a more granular register.

Example:

> `A controllable production decision exists`

actually contains several separate assumptions:

```text
actual demand unknown at commitment
+ decision owner exists
+ decision has an adjustment window
+ useful information exists before freeze
```

If one fails, the intervention may need to move even if the other three are true.

---

# Family A — control point

## KA-01 — actual demand is incomplete at initial commitment

**Hypothesis:** production/allocation is committed before final realized demand is known.

**Evidence:** recent service timeline from operator/contractor.

**Reject if:** actual demand is effectively known through binding reservations/orders before meaningful commitment.

**Consequence:** forecasting uncertainty may be a weak wedge; focus may shift to item mix/portion/other decisions.

## KA-02 — a named decision owner exists

**Hypothesis:** a real role/person determines or approves quantity.

**Reject if:** quantity is mechanically fixed by contract/system with no meaningful human/operator discretion.

**Consequence:** find nearest controllable downstream/upstream decision.

## KA-03 — quantity has a reachable adjustment window

**Hypothesis:** quantity can change after first estimate and before change becomes prohibitively costly/impossible.

**Reject if:** freeze point occurs before any useful signal or operator cannot change it.

**Consequence:** move to longer-horizon planning or downstream batch/allocation decision.

## KA-04 — decision-time information can improve the choice

**Hypothesis:** information available before freeze contains signal beyond current plan.

Candidate sources:

- recent served history;
- reservation/aggregate access;
- academic/service regime;
- menu;
- known events;
- operator knowledge.

**Reject if:** no useful incremental information exists before freeze.

---

# Family B — problem mechanism

## KA-05 — meaningful mismatch incidents recur

**Hypothesis:** actual demand repeatedly differs enough from plan to matter operationally.

**Reject if:** deviations are rare/trivial.

## KA-06 — production planning causes material avoidable edible surplus

**Hypothesis:** a meaningful component of avoidable waste is cooked/prepared but unserved because quantity was too high.

**Reject if:** dominant waste is prep loss, plate waste, spoilage, quality or another process unrelated to quantity.

## KA-07 — shortage/early sell-out is a meaningful counter-risk

**Hypothesis:** lowering production can materially harm service availability.

**Reject if:** replenishment is near-costless or shortages are operationally irrelevant.

## KA-08 — the problem is large enough for action

**Hypothesis:** frequency × consequence is sufficient to justify workflow change.

**Reject if:** operators accept current error as economically/operationally immaterial.

---

# Family C — status quo / alternatives

## KA-09 — current planning leaves a material residual gap

**Hypothesis:** staff experience, historical counts, reservation, spreadsheets and existing systems do not already solve the decision sufficiently.

**Reject if:** current process is consistently accurate enough with low waste/shortage pain.

## KA-10 — specialist incumbents are absent or insufficient in the first target

**Hypothesis:** Winnow/Leanpath/other production/waste systems do not already provide adequate decision support at the site.

**Reject if:** incumbent already solves the exact problem with acceptable workflow/cost.

**Consequence:** narrow differentiation or choose another segment.

---

# Family D — adoption / workflow

## KA-11 — recommendation can fit daily operations

**Hypothesis:** user can review and act without unacceptable extra work.

**Measure:** real daily burden, workflow steps, operator objections.

**Reject if:** integration/data entry/review burden exceeds perceived value.

## KA-12 — human-reviewed uncertainty is usable

**Hypothesis:** band + reasons + readiness/WITHHOLD is more useful/trustworthy than a scalar forecast.

**Reject if:** operators require a different representation or find uncertainty display distracting.

## KA-13 — a reachable champion exists

**Hypothesis:** someone with direct pain/value actively wants a pilot to happen.

**Reject if:** all relevant stakeholders are indifferent even when problem is confirmed.

## KA-14 — a reachable economic buyer captures enough value

**Hypothesis:** a person/unit with budget authority benefits enough from savings/risk reduction to fund adoption.

**Reject if:** value is split or externalized such that no actor has a compelling reason to pay.

## KA-15 — veto barriers can be satisfied in a bounded pilot

Potential vetoes:

- procurement;
- IT/security;
- KVKK/privacy;
- food safety;
- contractor agreement;
- senior administration.

**Reject if:** pilot requires full procurement/integration before any learning can occur.

---

# Family E — measurement / verification

## KA-16 — service-level outcomes can be measured consistently

Minimum useful outcome bundle:

```text
served demand
+ produced quantity or plan
+ decision-relevant surplus/waste
+ sellout/service guardrail
```

**Reject/modify if:** semantics cannot be reconciled or measurement burden is too high.

Possible response:

- reduce scope;
- manual short pilot;
- add minimal sensing;
- change outcome variable.

---

# Market homogeneity gates — separate from product mechanism

Even if KA-01..KA-16 work at one institution, a beachhead is not validated until cross-site PMR tests:

## KM-01 — same product

The same first product package can serve different institutions without material redesign.

## KM-02 — same sales process

Champion/economic-buyer/veto path is similar enough for one GTM motion.

## KM-03 — word of mouth

Operators use credible peer/reference networks that can accelerate adoption.

## KM-04 — speed to win

A bounded pilot can be approved quickly enough to make the segment attractive for a new venture.

## KM-05 — whole product manageable

Integration/measurement/onboarding requirements remain small enough for the team to deliver repeatably.

---

# Evidence coding

For each assumption use only:

```text
UNKNOWN
TESTING
SUPPORTED
REJECTED
CONFLICTING
```

Secondary research can move an assumption from `UNKNOWN` to `TESTING` by improving its plausibility/question design, but market-behavior assumptions should not become `SUPPORTED` without admissible primary evidence.

---

# Interview evidence matrix

Each completed interview should be coded against specific assumptions, not just H-A/H-B/H-C.

Example:

```text
Interview: contractor production lead
KA-01: supports — demand not known at first production commitment
KA-02: supports — interviewee names project manager as quantity approver
KA-03: contradicts — quantity cannot change after 15:00 previous day
KA-04: unknown — no evidence about useful signals before 15:00
KA-07: supports — shortage triggers emergency replacement
KA-14: unknown — interviewee cannot speak to budget ownership
```

This prevents a broadly positive interview from being counted as validation of assumptions it never addressed.

---

# Priority order

Highest existential risk:

1. KA-02 decision owner;
2. KA-03 reachable adjustment window;
3. KA-06 addressable surplus mechanism;
4. KA-08 material pain;
5. KA-14 economic buyer/value capture;
6. KA-16 measurable outcome;
7. KM-02 same sales process;
8. KM-01 same product.

Lower priority technical optimization should remain downstream of these.

---

# Kill logic

## Kill or change the production-quantity wedge immediately if repeated PMR shows:

```text
no controllable quantity decision
OR no material decision-linked surplus/shortage
OR no reachable measurement path
```

## Keep problem, change intervention if:

```text
pain is real
BUT control point is batch allocation / portion / menu / storage rather than total production
```

## Keep product, split market if:

```text
same decision/job
BUT buyer/procurement/sales process differs materially across institution types
```

## Keep current beachhead candidate only if:

```text
problem mechanism
+ user job
+ whole product
+ sales process
+ pilot feasibility
repeat across multiple institutions
```
