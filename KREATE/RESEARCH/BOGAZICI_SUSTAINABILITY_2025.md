# Boğaziçi University Sustainability 2025 — Agent Research Pack

**Research date:** 2026-09-30  
**Purpose:** Convert Boğaziçi University public sustainability material and relevant peer-reviewed research into an agent-ready secondary-research packet for the KREATE application.  
**Status:** Secondary/public-source research only. **NOT PMR. NOT customer validation. NOT pilot evidence.**

## 0. Claim firewall

This document intentionally separates what is publicly documented from what the team still has to learn.

- `PUBLIC SOURCE` below means an official university page/report or a cited peer-reviewed paper.
- A public waste total proves that waste was reported; it does **not** prove that demand-forecast error caused the waste.
- A university elsewhere reducing waste with forecasting does **not** prove Boğaziçi has the same workflow, data, incentives, or constraints.
- Repository agents must not describe estimated savings, model outputs, or literature case-study reductions as achieved Boğaziçi impact.
- Interview-only questions are explicitly listed as unknowns. They belong in PMR.

---

# 1. Agent-critical takeaways

## Finding R-01 — Boğaziçi publicly reports a material, measured food-waste stream

`PUBLIC SOURCE`

Boğaziçi reports **48,251 kg total food waste in 2025**. The same official page reports **33,430 kg delivered to İSTAÇ for recycling** and **6,305 kg waste oil**, all of the waste oil reported as recycled.

Why this matters:

- The current KREATE food-waste wedge is anchored to a real, university-published campus metric rather than a generic global problem statement.
- The number is appropriate for a **problem-scale public-source claim**.
- It is **not** evidence that the waste is avoidable, that it is caused by overproduction, or that a forecasting product would reduce it.

Primary source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## Finding R-02 — The food-service system is large, multi-campus, and operationally structured

`PUBLIC SOURCE`

The university says it provides catering for approximately **13,000 students and 2,000 staff**, with three meals per day across its campuses and multiple menu options including vegan/vegetarian alternatives. The food-waste page lists six dining halls with a combined listed capacity of **1,734 people**:

| Campus | Listed capacity |
| --- | ---: |
| North | 660 |
| South | 159 |
| Kilyos | 118 |
| Kandilli | 200 |
| Hisar | 124 |
| Anadolu Hisarı | 473 |
| **Total** | **1,734** |

The university publishes campus-specific service windows. Hisar is structurally different: the cited page lists lunch only on weekdays, while the other listed campuses have breakfast, lunch and dinner windows.

Implication: demand should not be assumed to be a single university-wide scalar. A future pilot/model may need at least **campus × meal × day** segmentation.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## Finding R-03 — Public sources indicate centralized production, making the production decision a plausible control point

`PUBLIC SOURCE`

Boğaziçi's sustainable-food page states that **all meals served by the dining halls are prepared in the North Campus kitchen**, with backup kitchens used for technical failure/disaster. It also states that the contractor provides portion-level nutritional values and updated meal/breakfast lists to the administration. Another official page describes the North Campus cafeteria kitchen and a contractor operating under a comprehensive technical specification prepared by the Health, Culture and Sports unit.

This does **not** identify who chooses the production quantity or when it is locked. It does, however, make the current product thesis more specific: instead of a generic "campus sustainability dashboard," the most valuable PMR target is the **central planning/production decision chain**.

Sources:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314  
https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313

## Finding R-04 — Boğaziçi already uses several downstream waste-reduction measures

`PUBLIC SOURCE`

The university says it already uses or promotes:

- portion control;
- removal of unpopular dishes from menus;
- composting of suitable leftovers/organic waste;
- donation or transfer of surplus food;
- recycling streams, including waste oil;
- advance publication of menus and nutrition/calorie information;
- waste separation and Zero Waste practices.

Product implication: a pitch based only on "track waste," "show sustainability," or "compost leftovers" is weak because those actions are already present publicly. The differentiated hypothesis should be **preventing avoidable overproduction before cooking/service**, while respecting shortage and service-level risk.

Sources:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310  
https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1225-policy-for-minimisation-of-plastic-use/1419

## Finding R-05 — 2025 monthly food-waste totals vary substantially, but the cause is unknown

The university reports the following monthly totals:

| Month | Food waste kg | Reported food waste delivered to İSTAÇ kg | Waste oil kg |
| --- | ---: | ---: | ---: |
| Jan | 3,992 | 2,250 | 475 |
| Feb | 7,811 | 1,555 | 250 |
| Mar | 7,004 | 2,285 | 900 |
| Apr | 4,772 | 3,090 | 825 |
| May | 3,832 | 2,900 | 450 |
| Jun | 2,777 | 1,450 | 550 |
| Jul | 1,923 | 1,850 | 150 |
| Aug | 1,502 | 3,550 | 350 |
| Sep | 2,072 | 1,450 | 830 |
| Oct | 1,334 | 4,850 | 600 |
| Nov | 4,784 | 3,300 | 550 |
| Dec | 6,448 | 4,900 | 375 |
| **Total** | **48,251** | **33,430** | **6,305** |

Descriptive calculations from the published monthly food-waste series:

- mean monthly food waste: **4,020.9 kg**;
- median: **3,912 kg**;
- minimum: **1,334 kg** (October);
- maximum: **7,811 kg** (February);
- max/min ratio: **5.86×**;
- population standard deviation: about **2,114 kg**;
- coefficient of variation: about **52.6%**.

These calculations describe the published series only. They do **not** establish unpredictable demand. Academic calendar, campus occupancy, summer operations, menu mix, service days, accounting timing, events, or waste-handling cadence could explain much of the variation.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## Finding R-06 — The published waste table contains a semantic/data-quality anomaly that must be resolved before modeling

The same official table says the amount delivered to İSTAÇ is included within total food waste. However:

- August: total food waste = **1,502 kg**, delivered to İSTAÇ = **3,550 kg**;
- October: total food waste = **1,334 kg**, delivered to İSTAÇ = **4,850 kg**.

Those rows cannot both satisfy a same-month simple subset interpretation.

Possible explanations include timing/backlog effects, different accounting periods, transcription, or a different semantic definition of "delivered" versus "generated". **None of these explanations is established by the public source.**

Agent rule: do not derive monthly recycling rates, train a target using these columns, or "clean" the anomaly without an operational data dictionary or owner confirmation.

## Finding R-07 — Important model inputs are publicly plausible but not publicly confirmed

The university publicly indicates:

- next-month menus are announced in advance;
- food engineers prepare menus;
- portion weights/calories/nutritional values are tracked or specified;
- menu popularity is acted upon (unpopular dishes may be removed);
- campuses and service windows differ;
- academic calendar determines service periods.

These are useful **candidate features/context**, but the public sources do not show that historical row-level data are available to the team.

Potential candidate features for CS1 to test only after data access:

- campus;
- meal type;
- weekday/weekend;
- academic-calendar state;
- menu/main-course identity;
- vegetarian/vegan mix;
- planned portions;
- served portions;
- reservation count if it exists;
- show/no-show if it exists;
- special event/holiday;
- weather only if incremental value is measured;
- historical demand at comparable campus/meal/menu contexts.

## Finding R-08 — The key public-source gap is causal and operational, not problem visibility

Public sources answer **"is food waste tracked and non-zero?"**. They do not answer:

1. Who decides how many portions to produce?
2. When is that decision made/frozen?
3. What inputs are used today?
4. Is there a reservation/pre-order system?
5. What is the no-show behavior, if any?
6. What is the split between pre-consumer overproduction, serving loss, preparation loss and post-consumer plate waste?
7. What happens when production is too low — sellout, substitution, waiting, extra batch, service failure?
8. Which errors are operationally more costly: one excess portion or one missing portion?
9. Are planned, produced, served and discarded quantities recorded at the same campus/meal granularity?
10. Can the operator change production after an initial batch?

These are PMR questions, not web-research questions.

---

# 2. Academic benchmark: what the literature supports — and what it does not

## A-01 — Demand forecasting with reservation/show-no-show data has been studied in subsidized university dining

Faezirad, Pooya & Naji-Azimi (2021), *Waste Management & Research*, studied a subsidized university dining setting using meal-booking and presence/absence behavior. Their proposed framework combined demand prediction under uncertainty with a cost formulation balancing waste and shortage penalties. The reported case-study framework achieved up to **79% food-waste reduction** in that setting.

Use this result as:

- evidence that the problem class is technically legitimate;
- a design reference for asymmetric cost / uncertainty-aware planning;
- a reason to ask whether Boğaziçi has reservations and no-show data.

Do **not** use it as:

- an expected Boğaziçi reduction percentage;
- a KREATE impact claim;
- proof that an ANN is the correct model for our pilot.

Paper:  
https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/?utm_source=chatgpt

## A-02 — Demand forecasting is already a recognized foodservice waste-prevention practice

Musicus, McKenzie, Rimm & Blondin (2022), *International Journal of Environmental Research and Public Health*, surveyed 57 U.S. university foodservice representatives. Roughly three-quarters reported tracking food waste and viewing reduction as a high/very-high priority; common reduction strategies included **forecasting demand to prevent overproduction** and preparing smaller batches. Donation and composting were common repurposing strategies, with operational barriers around labor, liability, infrastructure and know-how.

Use this to justify asking about forecasting and batch planning as established operational practices, not to claim a particular Boğaziçi workflow.

Paper:  
https://consensus.app/papers/food-waste-management-practices-and-barriers-to-progress-musicus-mckenzie/d2ef8eef200855aeb7fd97a088d1cef5/?utm_source=chatgpt

## A-03 — University food waste is multi-causal; forecasting should not crowd out other causes

Leal et al. (2023), *Environment, Development and Sustainability*, reviewed university food-waste literature and identifies multiple drivers and intervention families, including planning/awareness, preparation/storage, service, and direct reuse. The review reports substantial heterogeneity among university settings.

Product implication: the team should test whether **production mismatch is a dominant addressable cause in the chosen workflow** rather than assuming every kilogram in the official total is forecast-addressable.

Paper:  
https://consensus.app/papers/toward-food-waste-reduction-at-universities-leal-ribeiro/ccb8fe652ec75ed58b6b030afe3423d6/?utm_source=chatgpt

---

# 3. Secondary sustainability context beyond food

These facts are useful to prevent tunnel vision and to help agents compare campus climate opportunities. They are not a recommendation to pivot away from the current food-production wedge.

## Water

Boğaziçi's official water-reuse page documents grey-water and rainwater recovery. It says recovered grey water is used for high-demand non-potable uses such as toilet reservoirs; it reports that **15% of total water consumption in the 1st Men's Dormitory** is supplied by grey water. The current page contains different passages about whether **16 m³/day** is a system-level figure or a per-building figure across multiple dormitories, so that value requires source-owner clarification before reuse in a submission.

It also reports rainwater tanks of **46 m³** at Kandilli UDIM and **20 m³** at the North Campus ETA building, and a designed Hisar-campus potential of **1,747 m³/year**.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/641-water-reuse-policy/1354

Research implication: water is measurable and governed, but public material already describes dedicated infrastructure and a Water Management Commission. A hackathon solution here would need a sharply identified unresolved decision rather than another generic monitoring dashboard.

## Transport

The 2025 sustainable-practices table reports:

- personnel shuttles: **65**;
- campus shuttle services: **7**;
- listed service capacity: **1,429**;
- occupancy rate: **93%**;
- users: **1,332**;
- 2026 user target: **1,350**.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406

Research implication: there is structured transport data, but a 93% reported occupancy rate does not obviously reveal a large optimization gap. Any mobility idea would need PMR around pain points such as peak imbalance, route timing, reliability, deadheading, or access — none are established by this public table.

## Energy / greenhouse gases

Boğaziçi's 2025 Greenhouse Gas Inventory, prepared for January–December 2025 under ISO 14064-1:2018, reports a total footprint of **14,664.76 tCO₂e**. The report attributes **45.61%** to electricity consumption, **34.73%** to natural gas, **3.57%** to stationary/mobile combustion and **16.09%** to Scope 3/value-chain emissions.

Scope totals in the report:

- Scope 1: **5,615.90 tCO₂e**;
- Scope 2: **6,688.69 tCO₂e**;
- Scope 3: **2,360.17 tCO₂e**.

Official report index:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063

2025 GHG report:  
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/566-bogazici-university-greenhouse-gas-inventory--yayin-20260414-160244.pdf

The sustainability material also describes the BÜRES wind turbine as generating approximately **1.7 million kWh/year** and exporting excess generation to the grid.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1241-publication-of-sustainability-report/1424

Research implication: buildings/energy are quantitatively important climate areas, but the current food wedge has a clearer application-level decision point accessible through human PMR. Energy should remain a comparison domain unless interviews reveal a better reachable decision owner and data path.

## Waste governance

Boğaziçi publicly documents Zero Waste separation, recycling, organic-waste handling, waste-oil recycling and supplier-facing waste policies. This means "build a campus waste dashboard" is unlikely to be sufficiently differentiated without a concrete unresolved operational decision.

Sources:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1225-policy-for-minimisation-of-plastic-use/1419  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1224-policy-waste-disposal-landfill-policy/1418  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1228-minimisation-policies-extended-to-suppli/1422

---

# 4. Opportunity comparison for KREATE

This table scores only **public-source evidence fit and execution leverage**. It is not market validation.

| Domain | Publicly quantified problem/context | Existing institutional action | Clear decision point from public sources | PMR/access burden | Research conclusion |
| --- | --- | --- | --- | --- | --- |
| Food production / waste | Strong: 48,251 kg 2025 food waste; campus/meal structure | Strong: portion control, compost, donation, menu action, recycling | **Plausible but unverified**: centralized kitchen and planned menus make production quantity a concrete candidate | Medium | **Best current wedge to test** because problem metric + centralized operational system + literature benchmark align; causality still requires PMR. |
| Water | Strong infrastructure metrics | Strong grey/rainwater systems and governance | Weak from public material; unresolved decision not yet identified | Medium–High | Good sustainability domain, but needs a sharper problem than monitoring/recovery already described. |
| Energy/buildings | Very strong GHG magnitude | Strong reporting/efficiency/renewable activity | Potentially many decisions, but access/controls unclear | High | Climate impact is high, but a hackathon MVP risks becoming generic building-energy analytics without facility access. |
| Shuttle/mobility | Structured capacity/occupancy figures | Existing shuttle system | Route/capacity decisions plausible but pain point not established | Medium | Worth PMR only if a stakeholder reveals a concentrated route/timing problem; public 93% occupancy does not itself prove one. |
| Generic recycling/zero waste | Strong process documentation | Very strong existing policy/infrastructure | Mostly downstream | Low–Medium | Weak differentiation unless focused on a specific unserved decision. |

---

# 5. PMR packet generated from the research

The web research narrows the questions; it does not answer them.

## 5.1 Highest-value interview targets

Prioritize roles before names:

1. **Food Services / Health, Culture and Sports operational owner** — understands menu, service and administration.
2. **North Campus central-kitchen production manager / contractor operations lead** — likely closest to production quantities and batches.
3. **Food engineer / menu planner** — understands menu construction, portion specifications and historical demand heuristics.
4. **Campus dining-hall service manager** — sees local demand, sellouts, leftovers and distribution mismatch.
5. **Waste/zero-waste operational owner** — understands weighing semantics and the İSTAÇ accounting anomaly.
6. **Procurement/contract owner** — understands supplier/contract constraints and whether quantity changes are operationally/contractually flexible.

Do not assume any one of these roles is the buyer or final decision owner until PMR confirms it.

## 5.2 Interview questions — production decision

Ask for the **last real incident**, not opinions first.

- "For yesterday's lunch, how was the final number of portions decided?"
- "At what exact time/day did that number become difficult or impossible to change?"
- "Who proposed it, who approved it, and who executed it?"
- "What data did you actually look at?"
- "What happens when demand is 10% lower than planned?"
- "What happens when demand is 10% higher than planned?"
- "Can you cook in smaller batches during service, or must most production be committed before service?"
- "Which is operationally worse: excess portions or a sellout? Why?"
- "What is recorded after service: planned, cooked, served, returned, plate waste, donation, compost, İSTAÇ? At what granularity?"
- "When an unpopular dish is removed, what evidence or threshold drives that decision?"

## 5.3 Interview questions — data semantics

- "Does 'total food waste' combine preparation waste, unserved cooked food and plate waste?"
- "Is İSTAÇ delivery booked by generation month or collection/delivery month?"
- "Can material generated in one month be collected/reported in another?"
- "Why can the published August/October İSTAÇ delivery exceed the same month's total food-waste figure?"
- "Are waste measurements available per campus, per meal, per menu or only monthly university totals?"
- "Are produced and served portion counts recorded anywhere today?"
- "Is there any reservation/pre-order data? If yes, how often do reservations become no-shows?"

## 5.4 Falsifiers for the current thesis

The current production-decision wedge should be weakened or killed if PMR shows any of the following:

- production quantity is externally fixed and operators cannot change it;
- the overwhelming majority of waste is plate waste unrelated to overproduction;
- produced/served/waste data cannot be measured at useful granularity without prohibitive burden;
- existing forecasting already performs near the operational ceiling and operators report no costly mismatch incidents;
- shortage risk is so asymmetric that operators cannot act on a lower recommendation;
- contract/procurement rules eliminate the proposed decision discretion.

---

# 6. Role-specific handoffs

## IE — Customer Discovery & Market Lead

**Use now:** R-01, R-03, R-04, R-06, R-08.

Next actions:

1. Target the central-kitchen/food-service decision chain, not generic students first.
2. Test `H-002` (decision timing/discretion), `H-003` (demand mismatch causality) and `H-005` (persona/decision authority) with incident-based interviews.
3. Treat the 48,251 kg figure as problem context only.
4. Resolve the İSTAÇ/month semantic anomaly with an owner before quoting recycling ratios.
5. Ask explicitly whether the contractor or university administration bears the economic/operational cost of excess and shortage.

## EE — Physical Systems & Measurement Lead

**Use now:** R-05, R-06, R-08.

Build a measurement feasibility map before proposing hardware:

```text
planned portions
      ↓
produced portions / batches
      ↓
served portions
      ↓
unserved edible surplus
      ↓
preparation waste + plate waste
      ↓
compost / donation / İSTAÇ / other
```

For each edge, record source, unit, timestamp, campus, meal, owner, collection burden, and auditability.

Minimum pilot measurement should prefer existing logs plus manual weighing/counts before adding sensors. Public sources do not prove access to BMS, POS, turnstiles, smart scales or cafeteria telemetry.

## CS1 — Decision Intelligence Lead

**Use now:** R-02, R-05, R-06, R-07 plus A-01/A-02.

Technical guidance:

1. Do not start with a complex model before a clean baseline dataset exists.
2. Candidate baselines: last comparable day, rolling median, weekday × campus × meal mean, menu-aware historical baseline.
3. Optimize an **asymmetric decision loss**, not forecast MAE alone:
   - cost of excess/waste;
   - cost of shortage/sellout/service failure;
   - override/abstention when source health is poor.
4. Evaluate by campus/meal and calendar regime, not only global averages.
5. Keep policy heuristic bands separate from statistically calibrated uncertainty.
6. Treat the published monthly waste table as context, **not training data** for a production recommendation.
7. If reservation/show-no-show data exist, benchmark them because university literature shows they can be informative; do not assume they exist.

## CS2 — Product Strategy, Evidence Synthesis & Application Lead

**Use now:** all findings, especially the firewall.

Safe application narrative before PMR:

> `PUBLIC SOURCE` — Boğaziçi University reports 48,251 kg of food waste in 2025 and already uses measures including portion control, composting, surplus handling and menu adjustments. `HYPOTHESIS` — a remaining avoidable component may arise before service when production quantities are set under uncertain attendance. The team is testing who makes that decision, what data are available, and whether a human-reviewed recommendation can reduce mismatch without increasing shortages.

Do not write:

- "Boğaziçi wastes 48 tonnes because it cannot predict demand."
- "Our AI will reduce Boğaziçi food waste by 79%."
- "Boğaziçi has real-time cafeteria demand data."
- "69% of food waste is recycled" without first resolving the monthly reporting semantics.

---

# 7. Agent-ready hypotheses created by this pack

These are **research hypotheses**, not promoted evidence-register changes because `KREATE/EVIDENCE.md` and `KREATE/ASSUMPTIONS.md` are currently owned by another active workstream.

| Research hypothesis | Current status from public sources | Best next evidence |
| --- | --- | --- |
| Centralized production creates a reachable operational control point. | PLAUSIBLE | Interview central-kitchen/contract operations owner; document decision flow. |
| Demand mismatch causes a material share of reported waste. | UNKNOWN | 6+ concrete mismatch incidents + waste category breakdown. |
| Menu identity affects demand materially. | PLAUSIBLE because university says unpopular dishes are removed, but magnitude unknown. | Historical served counts by menu or operator incidents. |
| Campus/meal segmentation matters. | PLAUSIBLE from heterogeneous service schedules/capacities. | Per-campus/per-meal served and production data. |
| Reservation/no-show features exist and are useful. | UNKNOWN at Boğaziçi; supported as a useful pattern elsewhere. | Ask whether reservations/pre-orders exist; quantify no-show if yes. |
| Smaller/dynamic batches are operationally feasible. | UNKNOWN | Kitchen workflow interview and pilot observation. |
| Monthly waste reporting is directly usable for model training. | **NOT SUPPORTED** | Data dictionary + reconciliation of anomalous rows + finer-grained raw data. |

---

# 8. Source inventory and provenance

## Official Boğaziçi sources

1. **Boğaziçi University Sustainability 2025 report** — user-provided report URL:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/183-bogazici-university-sustainability-2025-yayin-20260430-104238.pdf
2. **Official sustainability reports index**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063
3. **Campus food waste tracking / 2025 food-waste table**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
4. **Sustainable food choices on campus**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313
5. **Healthy and affordable food choices**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314
6. **Water reuse policy**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/641-water-reuse-policy/1354
7. **Sustainable practices targets / transportation table**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406
8. **Publication of sustainability report / BÜRES context**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/1241-publication-of-sustainability-report/1424
9. **Plastic-use minimization / Zero Waste practices**:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/1225-policy-for-minimisation-of-plastic-use/1419
10. **Waste disposal / landfill policy**:  
    https://kurumsalveri.bogazici.edu.tr/tr/pages/1224-policy-waste-disposal-landfill-policy/1418
11. **Supplier-facing minimization policy**:  
    https://kurumsalveri.bogazici.edu.tr/tr/pages/1228-minimisation-policies-extended-to-suppli/1422
12. **2025 Greenhouse Gas Inventory**:  
    https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/566-bogazici-university-greenhouse-gas-inventory--yayin-20260414-160244.pdf

## Peer-reviewed literature retrieved via Consensus

1. Faezirad M, Pooya A, Naji-Azimi Z. (2021). *Preventing food waste in subsidy-based university dining systems: An artificial neural network-aided model under uncertainty.* Waste Management & Research.  
   https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/?utm_source=chatgpt
2. Musicus A, McKenzie R, Rimm E, Blondin S. (2022). *Food Waste Management Practices and Barriers to Progress in U.S. University Foodservice.* International Journal of Environmental Research and Public Health.  
   https://consensus.app/papers/food-waste-management-practices-and-barriers-to-progress-musicus-mckenzie/d2ef8eef200855aeb7fd97a088d1cef5/?utm_source=chatgpt
3. Leal W et al. (2023). *Toward food waste reduction at universities.* Environment, Development and Sustainability.  
   https://consensus.app/papers/toward-food-waste-reduction-at-universities-leal-ribeiro/ccb8fe652ec75ed58b6b030afe3423d6/?utm_source=chatgpt

---

# 9. Limitations

- The large Sustainability 2025 PDF is complemented here with the university's indexed SDG pages because those pages expose the underlying tables and current wording more directly.
- Public pages can change after this research date; submission claims must be rechecked.
- Several university pages combine current material with sections labelled as related to the 2024 Sustainability Report. Each numeric claim above is tied to its immediate source wording; do not infer a measurement year where the page does not specify one.
- The water page contains internally different descriptions of the 16 m³/day grey-water figure; this pack intentionally does not resolve that contradiction by assumption.
- The food-waste table has an internal monthly semantic inconsistency discussed in R-06.
- No PMR interview, private cafeteria dataset, contract, POS log, production log, sensor feed, or pilot result was used in this pack.

---

# 10. Bottom line

The strongest public-source story is **not** "Boğaziçi needs sustainability." The university already has extensive sustainability policy, reporting, recycling, water-reuse, renewable-energy and food-service initiatives.

The stronger KREATE hypothesis is narrower:

> Boğaziçi has a real, measured food-waste stream and a centralized, structured dining operation that already performs downstream mitigation. The unresolved opportunity is whether an earlier human-reviewed production-quantity decision can use existing operational context to reduce avoidable mismatch without causing shortages.

That sentence remains partly a `HYPOTHESIS` until IE/EE PMR establishes the decision owner, timing, causality, usable data and operational loss function.
