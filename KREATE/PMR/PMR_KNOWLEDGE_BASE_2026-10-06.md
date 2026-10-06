# PMR Knowledge Base — Institutional Dining / Boğaziçi

**Snapshot:** 2026-10-06  
**Scope:** Primary Market Research preparation and cumulative evidence context for the KREATE institutional-dining wedge.  
**Important:** Everything in this document is public/secondary research unless explicitly linked to a real interview evidence ID. It must not be described as customer validation.

## 1. What PMR means here

Primary Market Research is direct learning from target customers/users through interviews, observation, immersion, tests, or similar direct interaction. It is iterative: form a hypothesis, seek behavioral evidence and contradictions, revise, and repeat. Public university pages, procurement documents, academic papers, standards, and competitor pages are valuable preparation, but they are not PMR.

Method anchors:
- `SRC-METHOD-DE-PMR-2019` — Disciplined Entrepreneurship practical PMR guide.
- `SRC-METHOD-DE-STEP1A` — Disciplined Entrepreneurship Step 1A PMR resources.
- `SRC-METHOD-MIT-ORBIT-PMR` — MIT Orbit explanation of primary market research.

### Interview behavior standard

Prefer:
- “Walk me through the last time this happened.”
- “Who made the decision?”
- “What did you know at that moment?”
- “What changed the quantity?”
- “What happened when you were wrong?”
- “Show me the report/screen/form if you are allowed.”
- “Who else sees this problem from a different side?”

Avoid treating these as evidence:
- “Would you use an AI tool?”
- “Does this sound useful?”
- “Would sustainability be valuable?”
- “Would you buy this?”

A concrete recent incident is stronger than a future-facing opinion.

---

## 2. Current product hypothesis

The active hypothesis is not simply demand forecasting. The testable operational chain is:

```text
pre-service intent/context signals
→ quantity/service decision
→ decision freeze point
→ human approval
→ production/service execution
→ accepted/served demand
→ surplus / shortage / discard outcome
→ evidence and learning
```

A model matters only if there is a reachable decision before a freeze point and the recommendation beats a transparent baseline without violating service, food-safety, contract, or workflow constraints.

### Current wedge hypothesis

> A university/institutional dining operator has a pre-service quantity or allocation decision that remains adjustable after useful demand signals arrive, and reducing decision error can reduce avoidable surplus without unacceptable shortage risk.

This is a hypothesis. Current public sources establish that dining is a real, material, multi-site operation; they do **not** establish the causal chain above.

---

## 3. Boğaziçi public operating facts

### 3.1 Scale and service surface

The official 2025 campus food-waste page states approximately:
- 13,000 students;
- 2,000 staff;
- three meals per day;
- five alternatives per meal, including vegetarian/vegan options.

The same page lists dining-hall capacities:

| Dining hall | Publicly listed capacity |
| --- | ---: |
| North Campus | 660 |
| South Campus | 159 |
| Kilyos | 118 |
| Kandilli | 200 |
| Hisar | 124 |
| Anadolu Hisarı | 473 |
| **Total** | **1,734** |

Source: `SRC-BOUN-FOODWASTE-2025`.

**PMR implication:** the decision context is likely not one scalar “campus demand” number. Site, meal, service regime, capacity, menu, and possibly channel/allocation may matter. Do not choose the model target before identifying the real decision object.

### 3.2 Food-waste public series

The same official page publishes the following 2025 monthly “Total Food Waste” values in kg:

| Month | kg |
| --- | ---: |
| Jan | 3,992 |
| Feb | 7,811 |
| Mar | 7,004 |
| Apr | 4,772 |
| May | 3,832 |
| Jun | 2,777 |
| Jul | 1,923 |
| Aug | 1,502 |
| Sep | 2,072 |
| Oct | 1,334 |
| Nov | 4,784 |
| Dec | 6,448 |
| **2025 total** | **48,251** |

The page also reports annual totals of 33,430 kg “delivered to İSTAÇ” and 6,305 kg waste oil. Source: `SRC-BOUN-FOODWASTE-2025`.

The older official 2024 reporting page reports 50,993 kg total food waste, 29,776 kg delivered to İSTAÇ, and 5,710 kg waste oil. Source: `SRC-BOUN-FOODWASTE-2024`.

**Do not infer** that 48,251 kg is caused by demand forecast error. It may include preparation, unserved surplus, plate waste, food-safety discard, or other boundaries. The causal split is a PMR/measurement question.

### 3.3 Public-data contradiction worth investigating

The 2025 page contains at least two apparent semantic/arithmetic conflicts:
- August: “Total Food Waste” = 1,502 kg while “Delivered to İSTAÇ” = 3,550 kg.
- October: “Total Food Waste” = 1,334 kg while “Delivered to İSTAÇ” = 4,850 kg.

Do not silently “fix” these rows. Preserve them as a source-semantic problem.

**PMR questions created by this contradiction:**
- What does “Total Food Waste” include?
- Is the İSTAÇ field measured in the same period and boundary?
- Are either values cumulative, delayed collections, mixed waste, or corrections?
- Who owns the source spreadsheet?
- Is there a data dictionary?
- Which field is usable for service-level intervention evaluation?

The official page links a raw 2025 spreadsheet. It is indexed as `SRC-BOUN-FOODWASTE-2025-XLSX`.

### 3.4 Food preparation and menu signals

Official Boğaziçi food-choice pages describe a central-kitchen / institutional dining operation and publish menu/portion information. Current dining pages expose meal menus, energy values and cooked-portion grams. Source IDs: `SRC-BOUN-SUSTAINABLE-FOOD`, `SRC-BOUN-MENU-OCT2026`.

The university also has a menu-vote page describing a BUCampus-authenticated weekly vote used to select a Wednesday lunch menu. Source: `SRC-BOUN-MENU-SURVEY`.

**Boundary:** a preference vote is not automatically a demand count, served-meal count, reservation, payment record, or production quantity. It may become a context feature only after semantics and timing are verified.

### 3.5 Governance/control surface

Boğaziçi publicly lists a “Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı.” Source: `SRC-BOUN-DINING-CONTROL`.

**PMR implication:** production, inspection/control, contractor operations, procurement, payment, and university governance may have distinct roles. The end user, decision owner, approver, data owner, economic buyer and veto holder must be mapped separately.

---

## 4. What public research does NOT tell us

The following remain open despite substantial web/repo research:

| Unknown | Why it matters | Best evidence |
| --- | --- | --- |
| Daily production-quantity owner | Identifies real user/decision owner | Incident interview + workflow artifact |
| Exact freeze time | Determines whether any signal/recommendation is actionable | Incident timeline |
| Revision rights | Separates “forecast” from controllable action | Operator + manager corroboration |
| Actual baseline/heuristic | Required before claiming model value | Operator explanation + past records |
| Settlement/hakediş quantity | Identifies buyer economics and incentives | Procurement/finance owner + contract artifact |
| Excess-cost bearer | Determines economic beneficiary | Buyer/contractor evidence |
| Shortage consequence | Required for asymmetric decision loss | Recent incident + contract/workflow |
| Served-demand ground truth | Required for model/evaluation semantics | Source owner + data dictionary |
| BUCampus/BUCard export semantics | Determines usable pre-service/outcome signals | System owner + schema/export |
| Waste-stage split | Determines causal reachability | Measurement owner + protocol |
| Pre-consumer share | Separates overproduction from plate waste | Direct measurement |
| Adoption threshold | Determines whether operators act on recommendation | Real workflow incident |
| Pilot approval owner | Required for field validation | Governance interview |
| Willingness/budget path | Required for business model | Economic buyer/procurement interview |

No amount of additional secondary research can fully close these items.

---

## 5. High-information PMR sequence

The existing tracker targets 16 interviews (hard minimum 12). Prioritize information value rather than merely filling slots.

### Wave A — close the decision chain

1. **Food Services / Dining Operations manager**
   - last service quantity workflow;
   - owner, inputs, freeze point, revision rights;
   - shortage/surplus consequence;
   - pilot approval path.

2. **Contractor project manager / central-kitchen operations**
   - how tomorrow/today quantity is set;
   - batch/replenishment behavior;
   - safety buffer;
   - who bears operational cost;
   - what counts are recorded.

3. **Food engineer / production planner**
   - current heuristic;
   - timing;
   - menu and portion constraints;
   - what new information can still change production;
   - last mismatch incident.

4. **Dining control / verification role**
   - what is inspected/accepted;
   - actual-count semantics;
   - exception handling;
   - settlement/reconciliation artifacts.

### Wave B — close data and measurement

5. **BUCampus/BUCard/reporting system owner**
   - field names and event semantics;
   - timestamps;
   - aggregation level;
   - export availability;
   - cancellations/duplicates/second meals;
   - privacy-minimized aggregate path.

6. **Waste/sustainability measurement owner**
   - weighing method;
   - preparation vs unserved vs plate-waste boundary;
   - collection timing;
   - 2025 spreadsheet semantics;
   - August/October discrepancy.

7. **Procurement / contract / hakediş owner**
   - payable quantity;
   - risk allocation;
   - who can require a software/pilot process;
   - renewal/specification timing.

### Wave C — test repeatability, not friendliness

8. **Comparable external university/institution**
   - same workflow questions;
   - deliberately test whether the Boğaziçi architecture generalizes.

9. **Different operating archetype**
   - transported vs on-site, reservation-heavy vs walk-in, multi-site vs single-site;
   - use contradiction to find segmentation boundaries.

Continue through the 12–16 target using referrals from high-information interviews.

---

## 6. Falsification-first interview map

Use [HYPOTHESIS_FALSIFICATION_MATRIX.md](HYPOTHESIS_FALSIFICATION_MATRIX.md) as the canonical question bank.

The key kill/modify gates are:

1. **No reachable decision:** quantity is contractually/practically fixed before useful signals arrive.
2. **Wrong causal target:** dominant avoidable waste is not caused by production/allocation mismatch.
3. **No measurable outcome:** served/surplus/waste cannot be measured with acceptable semantics/effort.
4. **No actionable authority:** the apparent user cannot change the decision.
5. **No workflow fit:** recommendation arrives too late or violates operational/safety constraints.
6. **No incremental value:** transparent heuristic/baseline performs adequately.
7. **No incentive path:** user/buyer/beneficiary structure makes adoption implausible.
8. **Privacy cost too high:** required data would need unjustified person-level tracking.

A rejected hypothesis is useful research; do not rescue the current concept by redefining success after the interview.

---

## 7. Measurement discipline

External measurement standards should guide, not replace, local semantics.

### UNEP Food Waste Index 2024

`SRC-UNEP-FWI-2024` provides food-waste measurement guidance across food service, retail and household sectors.

Use it to:
- define measurement boundaries explicitly;
- separate estimation from measured quantities;
- document methods and reporting scope;
- avoid comparing incompatible waste definitions.

### FLW Standard

`SRC-FLW-STANDARD` and `SRC-FLW-OVERVIEW-PDF` provide a common accounting/reporting framework for food loss and waste.

For a pilot, record at minimum:
- date/service/site;
- measurement boundary;
- unit;
- method;
- stage/destination where known;
- planned quantity;
- produced quantity;
- accepted/served demand;
- unserved surplus;
- discard/waste;
- shortage/sell-out;
- source/provenance;
- operator baseline;
- recommendation;
- final human action.

Do not invent missing stages by subtraction unless source semantics support it.

---

## 8. Academic context — benchmark only

`SRC-ACADEMIC-TURKER-2025` is an open-access university dining paper on demand prediction and food-waste reduction. It supports the general relevance of density/demand information for campus food planning.

It does **not** prove:
- Boğaziçi has the same data;
- Boğaziçi waste has the same cause;
- the same model will work;
- any reduction will transfer;
- any current product metric has been achieved.

Use academic work for candidate features, baselines, measurement design and threat analysis—not as a substitute for local PMR or pilot evidence.

---

## 9. Agent consumption contract

### IE
- Read this file + falsification matrix before outreach.
- Capture recent incidents, not generic preferences.
- Add only real interviews to the tracker.
- Create `E-INT-*` only when evidence is promotable.
- Record contradictions and referrals.

### CS1
- Wait for semantic owner confirmation before treating a count as target truth.
- Benchmark the operator heuristic first.
- Keep recommendation, human action, execution and outcome as separate records.
- Use public/synthetic data only for software plumbing unless provenance permits stronger use.

### CS2
- Keep application wording aligned with evidence class.
- Use public scale facts only as public scale facts.
- Never convert 48,251 kg into “avoidable by our model.”
- Keep economic buyer and user separate until PMR maps them.

### EE / EHB
- Use standards to define measurement boundary.
- Add physical sensing only when a decision-critical field is absent/unreliable.
- Treat datasheet/simulation/bench/field evidence as distinct classes.

---

## 10. Source-driven artifacts available now

See [ASSET_AND_MEDIA_INDEX_2026-10-06.md](ASSET_AND_MEDIA_INDEX_2026-10-06.md) for direct links. The current index includes:
- official 2025 Boğaziçi food-waste page;
- official raw 2025 waste `.xlsx`;
- official Boğaziçi dining/facility photographs;
- Boğaziçi sustainability/SDG PDF;
- Disciplined Entrepreneurship PMR PDF;
- UNEP Food Waste Index 2024 PDF;
- FLW Standard overview PDF;
- current menu/menu-vote pages;
- open-access academic paper link.

Binary mirroring is intentionally avoided when redistribution permission is unclear. Link-first storage keeps provenance intact and repo size small.

---

## 11. Next evidence promotion path

The next meaningful advancement is not another generic market document. It is:

```text
interview → exact incident → owner/freeze/data semantics
→ artifact request → second-role corroboration
→ admitted aggregate dataset
→ transparent baseline
→ shadow recommendation
→ prospective pilot
→ measured outcome
```

Until the first steps are closed, model sophistication and impact claims should remain downstream.
