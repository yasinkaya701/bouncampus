# Secondary Research Synthesis for PMR — 2026-10-06

**Status:** secondary/public research synthesis.  
**Not PMR evidence.**  
**Purpose:** convert the cumulative source set into higher-information interviews, falsifiers and cross-role tasks.

Source IDs below resolve through [SOURCE_REGISTRY.md](./SOURCE_REGISTRY.md) and [source_registry.json](./source_registry.json).

---

# Executive result

Secondary research is now sufficient to stop asking generic questions such as:

> “Would AI forecasting be useful in a cafeteria?”

The evidence base shows that forecasting, reservations, turnstile data, historical counts, food-waste measurement and campus sustainability software already exist in many forms. The PMR job is therefore to discover the **specific unresolved decision gap** in a real workflow.

The current food wedge survives only if real interviews establish all of the following:

```text
reachable recurring decision
+ meaningful uncertainty/mismatch
+ consequence that matters
+ current alternative is insufficient
+ usable data / measurable outcome
+ operator can act before freeze
+ buyer/champion/veto path exists
+ same product/workflow can repeat
```

If one of these fails, modify or kill the wedge rather than protecting the current solution.

---

# 1. What is already supported by public/academic evidence

## 1.1 Food waste is a real institutional sustainability problem

Boğaziçi publicly reports campus food-waste data and publishes sustainability reporting artifacts (SRC-BU-001/002/003). This supports using food waste as a legitimate institutional problem space.

It does **not** support:

- demand-forecast error as the dominant cause;
- a service-level overproduction problem;
- an AI intervention;
- willingness to adopt or pay.

### PMR consequence

Ask first about the last concrete waste event and where in the process it arose. Do not begin with forecasting.

---

## 1.2 Forecasting and reservation-based planning are established approaches

Academic studies and university systems already use combinations of:

- historical meal counts;
- turnstile/dining entries;
- reservation/no-show signals;
- calendar/context;
- weather;
- menu/food attributes;
- ML/forecasting;
- explicit reservation cutoffs.

Relevant sources: SRC-ACAD-001/002/003/004/005, SRC-TGT-002/003/004/005.

### What this kills

Do not claim:

- “nobody predicts cafeteria demand”;
- “calendar/weather/menu features are novel”;
- “reservation + AI is a new category”.

### PMR consequence

The question becomes:

> What does the current planning process still fail to know **before the last actionable decision point**?

---

## 1.3 The real control point may not be one prior-day production number

Public university archetypes show that operations may use:

- prior-day reservations;
- weekly reservations;
- same-day/historical planning;
- electronic actual-consumption records;
- replenishment or staged production.

Relevant sources: SRC-TGT-001/002/003/004/005.

### PMR consequence

For the last lunch service, reconstruct:

```text
first estimate
→ reservation/count updates
→ procurement/prep
→ first batch
→ last change point
→ service start
→ replenishment possibility
→ service close
→ leftover/waste handling
```

If later-batch release is the actual controllable decision, pivot the product to that decision rather than forcing a next-day total forecast.

---

## 1.4 Food waste is multi-causal

Academic evidence and measurement standards show that food waste can arise from:

- overproduction / demand mismatch;
- portion size;
- menu preference/taste;
- preparation/process loss;
- post-consumer behavior;
- service interruption/food safety;
- other local factors.

Relevant sources: SRC-ACAD-006/007/008, SRC-MEAS-001/002/005.

### PMR consequence

H2 must be falsifiable. Ask operators to rank recent causes using concrete incidents, not general beliefs.

**Strong supporting evidence:** repeated services where a demand estimate caused avoidable unserved edible surplus/shortage and a pre-freeze action could have changed the outcome.

**Strong contradicting evidence:** the dominant preventable waste is mostly post-consumer, recipe/portion, preparation or safety-related.

---

## 1.5 Shortage and surplus are an asymmetric decision problem

Academic models explicitly treat waste and unmet demand as different costs/risks (SRC-ACAD-002/003). Reservation systems also reveal operational mechanisms designed to reduce uncertainty (SRC-TGT-002/003/004).

This establishes **mechanism plausibility**, not the target operator’s actual loss function.

### PMR consequence

Ask for both extremes:

- last time too much was produced;
- last time food ran out / nearly ran out.

Capture:

```text
what happened
who noticed
who complained
emergency action
extra labor
substitution
contract/penalty issue
reputational effect
amount discarded
who absorbed cost
```

Do not assign numeric shortage-vs-surplus weights until local evidence exists.

---

## 1.6 Measurement should follow the decision, not hardware preference

UNEP/EPA guidance supports multiple food-service measurement methods and upstream prevention (SRC-MEAS-001..005). Academic studies use weighing, counts and computer vision under different conditions (SRC-ACAD-008/009).

### PMR consequence

First ask what reliable records already exist:

- planned;
- produced;
- served/turnstile;
- unserved surplus;
- plate waste;
- preparation waste;
- cancellations/no-shows;
- shortages/sell-outs.

Only add sensing for a decision-critical field that cannot be captured reliably with existing records.

---

## 1.7 Competitor capability is broader than “waste measurement”

Current vendor materials show mature tracking/analytics and current AI production-forecasting positioning (SRC-COMP-001..005).

### What this kills

Avoid:

- “competitors only measure waste”;
- “first AI food-waste prevention platform”;
- “first campus sustainability platform”;
- “forecasting is our moat”.

### PMR consequence

Ask every relevant stakeholder:

1. What software/spreadsheet/ERP/reservation system is used now?
2. What does it already do well enough?
3. What manual judgment remains?
4. What information arrives too late?
5. What would have to be materially better to change workflow?
6. Would integration into the current system be preferred to another standalone product?

The strongest competitor may be good-enough human judgment at zero incremental procurement cost.

---

## 1.8 Privacy burden should be minimized upstream

KVKK sources support proportionality/data-minimization considerations (SRC-PRIV-001..004). This is not legal advice and does not approve a deployment.

### PMR / product consequence

The initial workflow should test whether the decision can be made with:

```text
service-level aggregate counts
+ menu/calendar/context
+ production/served/waste fields
+ operator decision record
```

rather than identity histories, biometrics or wide-field cameras.

Ask the institutional data owner what aggregate export is permissible and useful before proposing new sensing.

---

# 2. Highest-information interview sequence

The next interviews should not all be “sustainability” interviews. Sample the decision system.

## Interview A — daily production/operations owner

Goal: H1 + H2 + H3 + H6.

Must reconstruct one recent service end to end.

Questions:

1. Walk us through yesterday’s lunch from first quantity estimate to service close.
2. Who first set the number?
3. Who could change it?
4. What was the last practical change point?
5. What information was available at that exact time?
6. Tell us about the last day actual demand was meaningfully different.
7. What happened to excess food or shortages?
8. What do you currently do to protect against uncertainty?
9. What would make you ignore a new recommendation even if it looked accurate?
10. Who else sees or changes this decision?

**Kill condition:** no reachable/adjustable decision or no material consequence.

## Interview B — food engineer / kitchen technical owner

Goal: separate root cause, production mechanics and safety constraints.

Questions:

- Which waste stages are observed separately?
- How does batch production work?
- What can/cannot change after prep starts?
- Which menu/process factors dominate leftovers?
- What emergency substitutions/replenishments are permitted?
- What records are kept per service?
- Which recommendation could create food-safety or quality risk?

**Kill/modification condition:** forecast decision is not causal enough relative to preparation/portion/menu drivers.

## Interview C — university-side governance / Food Services / SKS

Goal: H5 + buyer/champion/veto + pilot approval.

Questions:

- Who owns the operating target?
- Who supervises contractor quantity/service?
- Who can approve a data export?
- Who can approve a bounded pilot?
- Who evaluates contractor performance?
- Which metric would make a pilot worth continuing?
- What would block procurement or integration even after a successful pilot?

**Kill/modification condition:** no feasible champion/approval path or incentive misalignment dominates.

## Interview D — contractor operations / project manager

Goal: economics, incumbent, shortage/surplus incentive.

Questions:

- What quantity drives payment/hakediş?
- Who bears excess ingredient/labor cost?
- Who bears shortage/recovery/penalty cost?
- Who actually decides quantity?
- Which planning software/worksheet is used?
- If waste drops, whose economics improve?
- Who would authorize integrating a planning tool?

**Kill/modification condition:** value accrues to a party with no decision/purchase influence or current system already solves the control point.

## Interview E — data/system owner

Goal: H4.

Ask for a field-level source map, not vague “we have data” confirmation:

```text
field
definition
system owner
granularity
timestamp semantics
available before/after decision
export format
history depth
missingness
privacy constraint
join key
```

**Kill/modification condition:** the outcome/decision cannot be reconstructed at acceptable operational/privacy burden.

---

# 3. Cross-site sampling plan

A Boğaziçi-only success story is not enough to validate a beachhead.

Use contrasting archetypes from the source registry.

## Site type 1 — mature in-house operation

Candidate: İTÜ (SRC-TGT-001).

Test whether sophisticated internal data/processes make a new layer redundant.

## Site type 2 — explicit reservation-before-production

Candidate: RTEÜ (SRC-TGT-002), Kayseri (SRC-TGT-003), AFSÜ (SRC-TGT-004).

Test whether the product problem is really:

- no-show/walk-in estimation;
- reservation compliance;
- allocation;
- batch release;

rather than generic demand forecasting.

## Site type 3 — large operation with reservation/digital workflow

Candidate: Anadolu (SRC-TGT-005).

Test portability at scale.

## Site type 4 — university-developed incumbent

Candidate: Altınbaş MyMeal (SRC-TGT-006).

Test build-vs-buy and integration/whole-product burden.

### Repeatability gate

Do not call the segment a beachhead until at least two/three independent sites show materially similar:

- end-user role;
- decision object;
- decision timing;
- pain/consequence;
- data semantics;
- whole-product requirement;
- buyer/procurement route.

If the technical pain repeats but buyer/process differs, segment again.

---

# 4. Source-to-question matrix

| Public finding | Interview question it should generate | Hypothesis |
| --- | --- | --- |
| Boğaziçi reports annual/monthly food waste | “For the last service with high waste, what stage caused it and what record exists?” | H2/H4 |
| universities use reservations | “When does reservation count freeze and what uncertainty remains afterward?” | H1/H2 |
| studies use turnstile/campus/context features | “Which signals exist before your decision, and which actually change your judgment?” | H1/H4 |
| forecasting already exists academically/vendors | “What does your current forecast/manual process fail at?” | H2/H6 |
| food waste has multiple drivers | “Which three recent events created avoidable waste, and what was the mechanism?” | H2 |
| shortage/unmet demand matters | “Describe the last sell-out/near-sell-out and its consequence.” | H3 |
| measurement methods vary | “What is already weighed/counted per service, by stage?” | H4 |
| competitor systems are broad | “Would you integrate into an existing system or add another tool? Why?” | H6 |
| privacy favors minimization | “Can aggregate service-level data answer the decision without personal histories?” | H4/H6 |

---

# 5. Evidence promotion ladder

```text
PUBLIC/ACADEMIC/VENDOR SOURCE
  ↓
question / target / falsifier
  ↓
real interview record
  ↓
specific quote / incident / artifact
  ↓
E-INT evidence with assumption link
  ↓
independent corroboration / contradiction
  ↓
assumption update
  ↓
product/application decision
```

Do not skip the middle.

A completed conversation that produces no promotable claim is still valid research and should be recorded as:

`NONE — no promotable claim`

---

# 6. What research should happen next vs stop

## Continue immediately

- verify the exact current Boğaziçi/TEMAŞ quantity/settlement mechanics from authoritative tender documents or direct stakeholders;
- identify named role routes for the five interview types above;
- obtain one real service-level field/sample schema;
- inspect the Boğaziçi 2025 waste XLSX only for its actual fields/units, without inferring service-level causality;
- use competitor research to sharpen differentiation questions;
- reverify any useful procurement cases from legacy research before promoting them into the canonical registry.

## Stop / deprioritize

- more generic “AI can reduce waste” papers;
- broad sustainability statistics that do not change an interview or product decision;
- extra feature ideation before control point and causal mechanism are validated;
- scraping contact lists without a hypothesis-specific reason;
- calculating TAM from university counts before workflow/buyer homogeneity is shown;
- quoting vendor outcome percentages as independent evidence.

---

# 7. Current decision posture

### KEEP

- food waste as a serious institutional problem space;
- decision-intelligence framing;
- human-reviewed recommendation;
- baseline-first / uncertainty-aware evaluation;
- service-level pilot with explicit measurement semantics;
- source provenance and claim firewall.

### MODIFY / TEST

- replace “forecasting product” with “decision layer around the real reachable control point”;
- allow the decision object to become total quantity, batch release, campus allocation, reservation correction or another PMR-discovered control;
- position sensing as gap-filling measurement, not product centerpiece;
- treat university-specific context/abstention/provenance as differentiation hypotheses, not established moat.

### KILL if PMR shows

- no reachable quantity/allocation/batch decision;
- waste is mostly driven by other mechanisms;
- shortage/surplus consequence is immaterial;
- existing process/tool already solves the decision adequately;
- outcome cannot be measured;
- no feasible pilot/buyer path;
- cross-site workflow is not repeatable enough for a coherent beachhead.

This is the standard against which the next PMR interviews should be run.
