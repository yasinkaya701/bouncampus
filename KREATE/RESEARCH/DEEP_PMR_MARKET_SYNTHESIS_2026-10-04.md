# KREATE Deep PMR & Market Synthesis — 2026-10-04

**Status:** Secondary/public-source research only. **NOT PMR, NOT customer validation, NOT pilot evidence.**

## Executive conclusion

The most defensible KREATE thesis remains:

> **BOUNCAMPUS should be tested as a campus resource decision-and-verification layer, with institutional university dining as the first beachhead and pre-service production quantity as the first named decision.**

The research strengthens the existence, scale, and strategic relevance of the problem class, but it does **not** validate the core causal hypothesis at Boğaziçi. The decisive PMR question remains:

> **Who chooses each service's production/allocation quantity, when does that choice become costly or impossible to change, what information is available before that moment, and who bears the consequence of excess versus shortage?**

This file deliberately separates:

- `PUBLIC SOURCE` — externally inspectable evidence;
- `RESEARCH INFERENCE` — synthesis across sources;
- `HYPOTHESIS` — must be tested through interviews/observation;
- `FORBIDDEN CLAIM` — not supported by current evidence.

---

# 1. Boğaziçi dining is a material multi-campus operation

## PUBLIC SOURCE — waste baseline

Boğaziçi University's official campus food-waste page reports for 2025:

- **48,251 kg total food waste**;
- **33,430 kg delivered to İSTAÇ**;
- **6,305 kg composted**;
- the page states delivered amounts are included in total amounts.

Source: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

### Important semantic caution

This total does not establish how much is:

- preparation waste;
- avoidable pre-consumer surplus;
- plate/post-consumer waste;
- timing/backlog effects in collection reporting;
- other food-related streams.

Therefore:

> **48,251 kg waste != 48,251 kg overproduction.**

## PUBLIC SOURCE — service scale

The 2025 SKS activity report states:

- **6 dining halls**;
- **6,000 daily meals**;
- **2,000 packaged meals** as a separately published figure;
- **2,386 survey participants**;
- meal production, packaged-meal operations, user feedback, and sustainable waste management as Food Services activities.

Source: https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

The exact denominator/time basis for `2,000 packaged meals` is not explicit enough to promote it into a modeling quantity.

## PUBLIC SOURCE — centralized production

Boğaziçi states that all meals served by its dining halls are prepared in the **North Campus kitchen**, with backup kitchens for technical failure/disaster scenarios.

Source: https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314

The same source states that the contractor provides portion weight and nutrition information to the administration with the monthly menu.

### RESEARCH INFERENCE

The operational graph is therefore plausibly closer to:

```text
central production
    -> campus/channel allocation
    -> multi-campus service
    -> unserved surplus / plate waste / other waste streams
```

than to six fully independent cafeterias.

This makes **production quantity + allocation** a plausible control point, but the actual owner and freeze time remain `UNKNOWN`.

---

# 2. Boğaziçi already has multiple digital/feedback signals

## PUBLIC SOURCE — menu preference

Boğaziçi's menu survey allows institutional users to vote through BUCampus on alternatives for Wednesday lunch; voting is authenticated and limited to one vote per user.

Source: https://yemekhane.bogazici.edu.tr/menu-anketi

**Boundary:** preference vote != attendance reservation != meal served.

## PUBLIC SOURCE — dining access metadata clues

The dining FAQ asks users reporting BUCard issues to provide date, time, campus and turnstile information. Users without a physical card may use BUCampus QR at turnstiles.

Source: https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

**Safe inference:** the operational stack supports some event context at turnstile level.

**Forbidden inference:** that the team has access to a historical clean dataset, that events are retained at useful granularity, or that one turnstile event always equals one consumed meal.

## PUBLIC SOURCE — pre-service feedback

Boğaziçi runs a daily volunteer food-tasting process before lunch and dinner, with short evaluation forms.

Source: https://sks.bogazici.edu.tr/en/announcements/food-tasting-event/4165

### RESEARCH INFERENCE

The problem is unlikely to be simply "the university has no data or feedback." A stronger PMR question is:

> **Which of the signals that already exist reach the production/allocation decision before its freeze point, and which do not?**

A generic new survey/feedback app is therefore a weak primary wedge.

---

# 3. Current Boğaziçi procurement is economically material, but settlement semantics remain unknown

## PUBLIC SOURCE — 2026–2027 procurement

Current public procurement mirrors reproducing EKAP information show:

- IKN `2025/1727143`;
- six campuses;
- **2,500,000 student meal units**;
- **380,000 breakfast/sahur units**;
- **250,000 staff meal units**;
- **3,130,000 total listed meal units**;
- contract period 01.01.2026–31.12.2027;
- contractor **TEMAŞ Gıda Sanayi ve Ticaret A.Ş.**;
- contract value **759,537,563.59 TRY**.

Sources reproducing EKAP records:

- https://www.ihaledetay.com/2025-1727143
- https://ekapveri.com/ihale/ekap-2025-1727143/

### What this establishes

- quantity is a material contract unit;
- the operation is formal and large enough that planning errors can be operationally important;
- contractor incentives must be part of persona/buyer research.

### What this does NOT establish

The public result notice does not resolve which quantity is used for daily acceptance/payment:

- forecast/requested;
- produced;
- delivered;
- turnstile-served;
- another contract-defined quantity.

It also does not establish who bears ingredient/labor cost for excess production or shortage penalties under the actual Boğaziçi contract.

### Highest-value PMR contract question

> **If 100 unnecessary portions are prevented tomorrow, who financially benefits: Boğaziçi, TEMAŞ, both, or neither?**

This can change the economic buyer and product route.

---

# 4. Comparable Turkish university procurement proves multiple real decision structures exist

This section supports **market-mechanism plausibility and segmentation**, not Boğaziçi-specific claims.

## Case A — İzmir Katip Çelebi University: administration-defined daily production using reservation + expected walk-ins

A 2025 Public Procurement Board decision reproduces a technical specification in which daily production quantity is calculated from:

- university information-system reservation count;
- expected guests;
- estimated students/personnel arriving without reservation.

The administration determines the quantity and the contractor produces that amount. The same specification says:

- the contractor must avoid shortages;
- the administration is not responsible for excess production/unsold meals;
- daily diner count is calculated from electronic-card/turnstile passages;
- payment is based on that count.

Public decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2025UH.II-2367-kamu-ihale-karari-kik

Decision: `2025/UH.II-2367`, İzmir Katip Çelebi University.

### Implication

At least one Turkish university contract contains the exact structure relevant to BOUNCAMPUS:

```text
forecast / reservation signal
    -> production quantity
    -> shortage guardrail
    -> turnstile-realized demand
    -> payment / excess-risk consequence
```

This does not prove Boğaziçi uses the same structure.

## Case B — Kırıkkale University: contractor forecasts quantity and bears excess-risk exposure

An official Public Procurement Board decision dated 26.08.2026 states the technical specification required daily meal quantities to be set by the contractor using previous meal counts. It also states:

- insufficient production can trigger penalties;
- payments are based on meals actually eaten;
- the administration is not responsible for leftover food;
- demand can vary with academic calendar and menu.

Official KIK decision:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

Decision: `2026/UH.I-2269`, Kırıkkale University.

### Implication

The economic pain of forecast error can sit on the **contractor**, not necessarily the university.

That creates at least two plausible B2B structures:

1. university-owned production decision support;
2. contractor-owned production planning software.

## Case C — Gebze Technical University: forecast responsibility without reference data became a procurement issue

A 2026 Public Procurement Board decision concerning Gebze Technical University reproduces a clause that the administration would not pre-notify daily student meal counts and the contractor would forecast meal quantities. The Board concluded that the absence of daily distribution/reference information created material uncertainty for healthy bid preparation.

Public decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-962-kamu-ihale-karari-kik

Decision: `2026/UH.II-962`, Gebze Technical University.

### Strategic implication

This is strong secondary evidence that **demand uncertainty + missing reference information can be contractually material**, not merely a machine-learning demo problem.

It still does not prove an operator will buy BOUNCAMPUS.

---

# 5. Beachhead should be segmented by workflow, not institution label

Disciplined Entrepreneurship Step 2 requires a beachhead whose end users:

1. use the same product;
2. share the same sales process/value proposition;
3. have strong word-of-mouth/community connection.

Source: https://www.d-eship.com/step2/

The Turkish procurement examples show that "universities" are **not operationally homogeneous**.

A more defensible candidate beachhead is:

> **Medium-to-large Turkish universities with centrally coordinated or institution-governed dining, repeated high-volume meal services, an identifiable production-quantity decision point, and enough service-level measurement to run a bounded pilot.**

### Suggested segmentation variables

- quantity owner: university / contractor / joint;
- settlement basis: produced / delivered / served / other;
- reservation model: none / partial / mandatory;
- production architecture: central / distributed;
- measurement maturity: spreadsheet / turnstile-POS / service-level waste / specialist system;
- adjustment horizon: prior-day / same-day / batch-reactive;
- shortage consequence: complaint / penalty / emergency substitution / service delay;
- excess consequence: contractor cost / university cost / shared / unclear.

### Outside initial beachhead

- fragmented independent food courts with no central quantity decision;
- very low-volume operations;
- operations where production quantity is fixed outside any reachable decision window;
- sites where outcome cannot be measured at reasonable effort.

---

# 6. Persona must follow the decision, not the organizational chart

Disciplined Entrepreneurship Step 5 says the persona must be a **real person**, not a generic profile, and purchasing criteria should be prioritized.

Source: https://www.d-eship.com/step5/

## PUBLIC SOURCE — Boğaziçi governance anchor

The current SKS staff page lists **Aygül Demir Yolasığmazoğlu — Yemek Hizmetleri Şube Müdürü**.

Source: https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

This makes Food Services a strong first PMR route.

### Boundary

The public title does not prove that this person sets daily production quantity.

The persona remains a **working hypothesis** until PMR identifies the actual operator:

> **Food Services Operations Manager / Production Quantity Decision Owner**

Possible real owner variants:

- Food Services Branch manager;
- food engineer;
- contractor project manager;
- central-kitchen production manager;
- joint university-contractor workflow.

### Persona adoption criteria to test

Likely purchasing/use criteria, in proposed priority order:

1. service continuity / no unacceptable sell-out risk;
2. recommendation arrives before freeze point;
3. operational reliability and low staff burden;
4. explainable reasons / uncertainty;
5. fit with contractor and current systems;
6. measurable waste/cost effect;
7. procurement/integration burden.

These are `HYPOTHESIS` until interviews.

---

# 7. Final three PMR hypotheses for the application

Disciplined Entrepreneurship Step 20 says key assumptions should be narrow, specific and empirically testable.

Source: https://www.d-eship.com/step20/

## H-A — controllable decision

> **In large, centrally coordinated university dining operations, an identifiable operational role determines or approves meal-production quantities before actual demand is known, and that quantity remains adjustable until a defined operational freeze point.**

### Falsifier

Repeated interviews show quantity is fixed outside the reachable workflow, legally/contractually non-adjustable, or the decision occurs too late/early for usable information.

## H-B — material decision-linked mismatch

> **Demand uncertainty and the current production-planning process repeatedly create meaningful mismatches between food prepared and food actually needed, producing avoidable edible surplus and/or shortages that can be affected by changing the production decision.**

### Falsifier

Waste is primarily driven by plate waste, preparation loss, quality/palatability, food-safety constraints, procurement rules, or other causes that are not materially affected by quantity planning.

## H-C — asymmetric risk / safety buffer

> **Food-service operators intentionally maintain a production safety buffer because shortages create a more immediate operational risk than surplus, and this buffer is determined mainly through historical experience and fragmented information rather than a consistently integrated decision process.**

### Falsifier

Operators already have a sufficiently integrated process with no meaningful buffer/shortage asymmetry, or shortage is not a material constraint.

---

# 8. PMR method: reconstruct incidents, do not pitch the product

Disciplined Entrepreneurship Step 1a describes PMR as foundational and explicitly points to `The Mom Test`; the core lesson is not to ask whether someone likes the business idea.

Source: https://www.d-eship.com/step1a/

The interview should reconstruct the **last real mismatch**:

```text
trigger
-> information available
-> person
-> quantity decision
-> freeze time
-> adjustment rights
-> outcome
-> excess / shortage consequence
-> recorded data
-> next correction
```

## First three target roles

1. **Food Services governance / branch decision route** — identify owner, contract, approval, current signals.
2. **Current contractor local production/project lead** — identify heuristic, freeze point, batch flexibility, excess/shortage economics.
3. **Food engineer / daily production operator** — identify actual workflow, buffer behavior, data and measurement.

Support interviews:

4. IT / BUCard data owner;
5. waste/sustainability measurement owner;
6. same decision role at a second university to test repeatability.

## High-value questions

- Tell me about the most recent service where demand was materially different from expected.
- Who chose the production quantity?
- When did that number become hard to change?
- What information was actually used at that moment?
- What happened when too much was produced?
- What happened when too little was produced?
- When was the last time a planned quantity was changed, and what new information caused the change?
- Which quantity is used for payment/acceptance?
- Who benefits financially if unnecessary production falls?
- Which data exist by campus x meal x date before the freeze point?

Avoid:

- "Would you use our AI?"
- "Do you think this is useful?"
- "Would 10% waste reduction be valuable?"

These invite confirmation rather than behavioral evidence.

---

# 9. Competitor reality: forecasting and waste measurement are not unique

## Winnow

Winnow already sells AI-assisted food-waste measurement to commercial kitchens and university dining contexts. In September 2026 it announced **Winnow Foresight**, a mobile-first production-forecasting product that builds production plans from occupancy and waste data.

Sources:

- https://www.winnowsolutions.com/
- https://www.winnowsolutions.com/resources/news/winnow-and-hilton-announce-winnow-foresight-a-mobile-first-ai-powered-forecasting-tool-designed-to-predict-kitchen-demand-and-prevent-food-waste

### Forbidden differentiation

- "Competitors only measure waste."
- "No existing product forecasts production."

## Leanpath

Leanpath markets college/university food-waste systems around measurement, operational insight, root-cause analysis, and sustainability outcomes.

Source: https://www.leanpath.com/industries/college-university/

## Emissary Campus

Emissary Campus markets a university-specific sustainability platform in Türkiye, including energy, water, waste, transportation, audit/evidence workflows and UI GreenMetric/THE positioning.

Source: https://emissary.com.tr/tr/cozumler/emissary-campus

### Forbidden differentiation

- "No campus sustainability platform exists in Türkiye."
- "Centralizing sustainability data is our moat."

### More defensible differentiation hypothesis

```text
campus-specific context
+ exact decision timing
+ provenance / data semantics
+ uncertainty / WITHHOLD
+ human approval
+ measured post-decision verification
```

This is a hypothesis to test against buyers, not a proven moat.

---

# 10. Why-now: sustainability governance is becoming explicitly digital

## PUBLIC SOURCE — UI GreenMetric 2026

The 2026 UI GreenMetric framework adds **Governance and Digitalization** as an 11% category. Its indicators include:

- ICT use for sustainability planning, implementation, monitoring and evaluation (`GD6`);
- policy/use of advanced digital technologies such as AI/IoT for decision-making, operational efficiency and service delivery (`GD7`).

Official guideline:
https://uigreenmetric.com/resources/university/guidelines/2026/english

Official PDF:
https://uigreenmetric.com/wp-content/uploads/2026/06/2026_Guideline_UI-GreenMetric-SUR-eng-v2.pdf

### Boundary

This is a **why-now / institutional context signal**, not proof that a university will buy BOUNCAMPUS and not a promise of ranking improvement.

## PUBLIC SOURCE — Türkiye higher-education direction

YÖK's 2030 roadmap states that Türkiye had **208 universities** in 2025 and explicitly calls for scaling sustainable/climate-friendly campus practices and increasing Turkish representation in UI GreenMetric's top ranks.

Source:
https://s3-ankara.yok.gov.tr/yokmedia/537cb59e-4949-4c0e-8a59-e3e5cc317a03.pdf

### Boundary

`208 universities` is context, not TAM and not 208 addressable buyers.

---

# 11. Academic evidence — use as mechanism support, not impact claims

## Demand forecasting in catering

Rodrigues, Miguéis, Freitas & Machado (2023), *Journal of Cleaner Production*:

https://consensus.app/papers/machine-learning-models-for-shortterm-demand-forecasting-rodrigues-miguéis/47d8e2ce5d015189bc052f02df2e3a47/

Supports: forecasting is a real institutional-catering problem class and should be compared against simple baselines.

Does not support: a transferable Boğaziçi saving percentage.

## University dining under uncertainty

Faezirad, Pooya & Naji-Azimi (2021), *Waste Management & Research*:

https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/

Supports: reservation/show-no-show uncertainty and waste-vs-shortage cost can be modeled jointly.

Does not support: identical economics/workflow at Boğaziçi.

## University foodservice practices

Musicus, McKenzie, Rimm & Blondin (2022), *International Journal of Environmental Research and Public Health*:

https://consensus.app/papers/food-waste-management-practices-and-barriers-to-progress-musicus-mckenzie/d2ef8eef200855aeb7fd97a088d1cef5/

Supports: forecasting and smaller-batch production are recognized institutional food-waste prevention practices.

## Systematic review

Kaur, Dhir, Talwar & Alrasheedy (2021), *International Journal of Contemporary Hospitality Management*:

https://consensus.app/papers/systematic-literature-review-of-food-waste-in-educational-kaur-dhir/41d44cdd08b7512597ef87b8b9fe942d/

Supports: educational food waste is multi-causal and granular measurement/root-cause analysis matters.

### Central academic inference

> Forecasting is technically plausible, but **forecasting is not the novel claim** and model accuracy alone is not product value.

---

# 12. Product architecture implication

The strongest operating contract is:

```text
observe
-> reconcile semantics/provenance
-> predict / diagnose
-> quantify uncertainty
-> recommend
-> human approve / edit / hold
-> measure outcome
-> learn
```

## Existing data first

Use existing institutional systems before introducing hardware.

Add hardware only if a **decision-critical observation** is missing.

Examples:

- turnstile/POS aggregate exists -> integrate rather than duplicate counting;
- service-level waste already measured -> integrate rather than deploy TrayGate;
- plate/post-consumer waste is a critical missing variable -> bounded TrayGate can close the gap.

### TrayGate role

TrayGate should be positioned as a **measurement gap closer**, not the company thesis.

---

# 13. Minimum pilot evidence boundary

A useful service-level table should distinguish:

```text
service_id
service_date
campus
meal_period
service_channel
planned_portions
produced_portions
served_portions_or_validated_entry_count
edible_surplus_kg
prep_waste_kg
plate_waste_kg
early_sellout_or_substitution
menu_id
service_regime
operator_override
override_reason
measurement_method
source/provenance
```

Primary impact metric should normalize for service volume, e.g. waste kg per 100 served meals, while keeping waste stages separate where feasible.

Do not convert to CO2e/water/cost until:

1. measured physical reduction exists;
2. factor/source is documented;
3. contract/payment semantics are known for monetary claims.

---

# 14. Kill / modify gates

Modify or kill the current food-production wedge if PMR repeatedly shows any of the following:

1. production quantity is not a reachable decision;
2. the quantity is fixed too early/late for useful context;
3. avoidable pre-consumer surplus is not material;
4. shortage/service risk makes quantity reduction operationally unacceptable;
5. the decision owner has no discretion;
6. required outcome data cannot be captured at acceptable effort;
7. existing tools/workflows already solve the decision sufficiently;
8. incentives are structurally misaligned so no reachable sponsor captures value.

A contradictory interview is valuable evidence, not a failed interview.

---

# 15. Research priority after this file

Further web research has declining value relative to PMR. The highest-value unresolved items are now:

1. Boğaziçi/TEMAŞ quantity owner;
2. exact freeze point;
3. settlement/payment quantity;
4. excess-cost owner;
5. shortage consequence;
6. stage breakdown of the published waste stream;
7. privacy-safe aggregate service-level data availability;
8. repeatability of the workflow at a second and third Turkish institution.

No secondary source should be promoted into interview evidence for these items.
