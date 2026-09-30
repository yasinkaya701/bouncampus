# Boğaziçi Food Operations Deep Dive — Decision, Governance & Data-Signal Map

**Research date:** 2026-10-01  
**Purpose:** Extend the Sustainability 2025 research pack with operational, governance, digital-signal, service-regime and model-design evidence for the current institutional food-waste thesis.  
**Status:** Secondary/public-source research only. **NOT PMR. NOT customer validation. NOT pilot evidence.**

Related pack: [`BOGAZICI_SUSTAINABILITY_2025.md`](./BOGAZICI_SUSTAINABILITY_2025.md)

---

# 0. Claim firewall

This document is intentionally conservative.

- Public evidence can establish that a system, role, process or published metric exists.
- It cannot establish that the team can access private operational data.
- It cannot establish that a public digital signal is actually used in production planning.
- It cannot establish that forecast error causes a particular share of the 48,251 kg 2025 food-waste total.
- Literature benchmarks are design references, not expected Boğaziçi results.
- `likely`, `plausible`, `candidate`, and `ask PMR` are not synonyms for `FACT`.

---

# 1. Executive findings

## FOD-01 — The system is materially larger than a single cafeteria and now has multiple service channels

`PUBLIC SOURCE`

The 2025 SKS activity report states:

- **6 dining halls**;
- **6,000 daily meals**;
- **2,000 packaged meals** listed in the Food Services section;
- **2,386 satisfaction-survey participants**;
- a virtual-card system for guest dining;
- packaged-meal distribution;
- a North Campus kiosk;
- a two-year meal-service tender;
- student menu selection through BUCampus.

The report does not provide a definition precise enough to treat `2,000 packaged meals` as a daily average, annual total, capacity or another denominator. Do not infer a unit beyond the source label without owner confirmation.

Source:  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

### Implication

The product problem is not simply `forecast how many people enter a cafeteria`. The operation may contain at least:

```text
central production
    ↓
regular dine-in allocation by campus / meal
    ↓
packaged-meal allocation
    ↓
kiosk / special-channel allocation
    ↓
service + leftovers + waste destinations
```

A pilot should identify which channel creates the actual controllable production decision.

---

## FOD-02 — Official governance identifies a much sharper administrative persona

`PUBLIC SOURCE`

The **Food Services Branch Directorate (Yemek Hizmetleri Şube Müdürlüğü)** is formally assigned to:

1. prepare tender work for student/staff/guest food services;
2. prepare technical specifications for dining halls;
3. monitor and control food service supplied by the contractor;
4. determine staff meal prices for board approval;
5. determine student meal prices and meal-scholarship pricing for board approval;
6. prepare and publish menus;
7. check compliance with the contract and technical specification;
8. perform secretariat duties for the Food Services Executive Board.

Official directive, Article 12:  
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/2106-bogazici-universitesi-saglik-kultur-ve-spor-d-20260521-143342.pdf

### What this establishes

- Food Services is not merely a communications or serving unit.
- It owns or participates in several high-consequence administrative decisions around the service.
- It is a high-priority PMR persona for workflow, incentives and contract constraints.

### What this does **not** establish

The directive does **not** say:

- who chooses the number of portions;
- whether that decision is made by the university, contractor, kitchen manager or jointly;
- when quantity becomes locked;
- whether quantity can be changed during service;
- who bears the financial cost of excess or shortage.

These remain PMR-critical unknowns.

---

## FOD-03 — Contractor incentives and procurement constraints may be first-order product variables

`PUBLIC SOURCE`

The university's 2025 administration activity report describes a contracted service covering **breakfast and meal preparation, distribution and post-distribution cleaning**. It states that these recurring contracted services are monitored through the university's Control Organization and that contractor service is carried out under this oversight.

Relevant section of the 2025 Administration Activity Report:  
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf

The 2025 SKS activity page separately reports that a **two-year meal tender** was conducted.

Source:  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

### Product implication

Forecast quality alone may be insufficient. The intervention must fit the contract.

PMR must resolve:

- Is the contractor paid per produced portion, served portion, fixed service capacity, ingredient input, or another basis?
- Who pays for unused ingredients or unserved cooked food?
- Are minimum quantities or service-level guarantees specified?
- Does the contract permit same-day quantity adjustment?
- Does reducing waste financially help the university, the contractor, both, or neither?

If incentives are misaligned, the buyer, user and beneficiary may be different personas.

---

## FOD-04 — Boğaziçi already has a digital preference signal through BUCampus

`PUBLIC SOURCE`

Boğaziçi's menu survey states that:

- **Wednesday lunch** is subject to a menu vote;
- users choose among three alternatives in each group;
- the most preferred options determine the menu;
- access is via BUCampus with institutional identity;
- each user can vote once;
- voting runs from Friday to Monday for the next week's menu.

Source:  
https://yemekhane.bogazici.edu.tr/menu-anketi

The BUCampus v1.1.2 announcement states that users can see packaged-meal menus, vote in the food survey, see survey results immediately, view the activity calendar, and access the academic calendar.

Source:  
https://bilgiislem.bogazici.edu.tr/tr/news/kampus/2/bucampusun-yeni-versiyonu-yayinda/3351

### Important distinction

**Preference votes are not attendance reservations.**

A menu vote may help estimate relative appeal, but it does not directly imply:

- the voter will attend;
- which campus the voter will use;
- whether they choose regular vs packaged service;
- how many portions should be produced.

Therefore menu votes are a **candidate feature**, not a demand label.

---

## FOD-05 — There is public evidence of transaction/entry metadata structure, but no evidence of team access

`PUBLIC SOURCE`

The dining FAQ says that for BUCard overcharge incidents, users should report:

- identity;
- **date**;
- **time**;
- **campus**;
- **turnstile** information.

It also says users without a physical card can enter by scanning the QR code on the turnstile using BUCampus.

Source:  
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

### Safe inference

This strongly suggests the operational payment/access stack is capable of identifying at least some dining-entry events with time/campus/turnstile context.

### Forbidden inference

Do **not** claim:

- that historical turnstile data are retained for modeling;
- that the team can access them;
- that a single turnstile event equals a consumed meal in all cases;
- that transaction logs have clean campus/meal labels;
- that QR and BUCard histories are joined in one export.

### PMR question

> Can Food Services or IT export privacy-safe aggregate counts by date × campus × meal/service channel, and what retention period exists?

This may be the single highest-value data-access question for CS1.

---

## FOD-06 — Academic calendar and service-regime changes are not optional modeling details

`PUBLIC SOURCE`

Public dining announcements show structural changes in service rather than ordinary noise.

Example: during the **18 August–19 September 2025 summer break**, Boğaziçi announced that across the listed campuses:

- weekday breakfast and dinner would not be served;
- weekend breakfast, lunch and dinner would not be served.

Source:  
https://yemekhane.bogazici.edu.tr/yaz-donemi-yemek-hizmeti-hakkinda

Another 2025 announcement changed Sarıtepe/Kilyos service for the summer period, pausing breakfast and dinner and weekend service while retaining weekday lunch.

Source:  
https://yemekhane.bogazici.edu.tr/saritepe-kilyos-kampus-yemek-hizmeti-hakkinda

The university maintains a structured academic calendar:

https://akademiktakvim.bogazici.edu.tr/

### Model implication

A model that treats `month` or `weekday` as sufficient calendar context will conflate demand changes with **service availability changes**.

Required concept:

```text
service_regime = {
  normal_term,
  exam_period,
  registration/orientation,
  summer_reduced_service,
  holiday,
  ramadan_special_hours,
  campus-specific closure,
  special package-only / kiosk mode,
  other announced exception
}
```

Historical training/evaluation must distinguish `zero demand because service was closed` from `low demand while service was available`.

---

## FOD-07 — The public menu itself is a useful structured exogenous dataset

`PUBLIC SOURCE`

The public dining website exposes historical/current menus by month and meal type, including regular, breakfast and packaged menus. Individual current menu pages can include kcal and cooked portion gram weights for dishes.

Examples:

- Regular menu archive: https://yemekhane.bogazici.edu.tr/aylik-menu
- Breakfast archive: https://yemekhane.bogazici.edu.tr/kahvalti-menu/2026-06
- Packaged menu archive: https://yemekhane.bogazici.edu.tr/paket-menu

### Data-engineering implication

Even before private data access, CS1 can define a parser/schema for:

```text
date
meal_type
main_course
vegetarian_or_vegan_option
side_options
selectable_items
published_kcal
published_portion_grams
package_vs_dine_in
```

This can later join against aggregate served counts if permission is obtained.

Do not scrape or operationalize in a production system without checking the site's terms and team access policy; for the hackathon, the public pages are enough to validate the **availability of menu context**, not the right to bulk-harvest indefinitely.

---

## FOD-08 — 2024 operational counts provide a useful scale benchmark but definitions differ across reports

`PUBLIC SOURCE`

The 2024 SKS activity report says that in 2024:

- **16,863 students** received **157,697 breakfast servings**;
- students received **1,157,911 meal servings**;
- **2,227 staff** received **96,838 meal servings**.

This sums to **1,412,446 reported breakfast/meal servings** across the listed categories for 2024.

Source:  
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/303-2024-yili-faaliyet-raporu-yayin-20251205-150840.pdf

The 2025 University Administration Activity Report separately lists **17,466 students** and **2,478 staff** under people benefiting from meal services, total **19,944**. This appears to be a beneficiary-count table, not a meal-count table.

Source:  
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf

### Data-quality lesson

Do not join similarly named `meal count`, `beneficiary count`, `daily meal`, `packaged meal`, and `food waste` fields until their units and counting rules are explicitly defined.

The first pilot data artifact should contain a **data dictionary**, not just CSV files.

---

## FOD-09 — A demand model should account for food-access policy and subsidized cohorts

`PUBLIC SOURCE`

Boğaziçi supports meal access through food scholarships. The 2025 SKS activity report lists **1,091 meal-scholarship recipients** and states that meal support was converted to in-kind support so recipients can use meals directly.

Source:  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

The university also operates BUCard/QR access and affordability policies.

### Implication

Demand is not purely a consumer-choice function. It may be influenced by:

- scholarship eligibility;
- pricing changes;
- campaign/free-meal incentives;
- package availability;
- special service modes.

No model should ingest personally identifying scholarship status. If access is granted, only privacy-safe aggregate cohort/event effects should be considered, and only if operationally necessary.

---

# 2. The likely operational decision graph

This is a **research model**, not a verified workflow.

```text
University / Food Services Branch
    ├─ menu design / publication
    ├─ technical specification / contract oversight
    ├─ prices / policy / service rules
    └─ possibly demand guidance  ← UNKNOWN

Contractor / central kitchen operations
    ├─ ingredient procurement / preparation
    ├─ production-batch planning  ← OWNER UNKNOWN
    ├─ campus allocation           ← OWNER UNKNOWN
    └─ distribution to campuses

Campus / channel service
    ├─ dine-in turnstile / BUCard / QR
    ├─ packaged meal
    ├─ kiosk / special service
    └─ campus-specific service windows

Post-service
    ├─ served portions
    ├─ unserved edible surplus
    ├─ preparation waste
    ├─ plate waste
    ├─ donation / animal shelter
    ├─ compost
    └─ İSTAÇ / licensed recovery
```

### PMR objective

Convert every `UNKNOWN` ownership arrow into:

```text
role → input → decision → deadline → allowed adjustment → consequence → stored data
```

---

# 3. Data availability map

## 3.1 Publicly available / externally observable context

| Signal | Public evidence | Potential role | Main caveat |
| --- | --- | --- | --- |
| Menu by date/meal | Yemekhane menu site | Menu-demand context | Not a demand label |
| Menu kcal / portion grams | Menu + sustainability pages | Portion/menu features | Completeness varies by item/page |
| Academic calendar | Official academic calendar | Regime/calendar features | Must map events to operational impact |
| Service hours | Sustainability / dining pages | Availability mask | Special announcements override defaults |
| Service-change announcements | Dining announcements | Structural-break flags | Requires historical normalization |
| Menu poll structure | BUCampus/menu survey | Preference feature | Votes ≠ attendance |
| Campus capacity | Sustainability/admin reports | Capacity/constraint context | Published capacities differ across documents/years |
| Monthly university food waste | Sustainability page | Problem-scale context | Too coarse for production modeling; semantic anomalies |

## 3.2 Plausibly existing internal signals — **access unknown**

| Candidate internal signal | Public clue | Value if accessible | Must ask |
| --- | --- | --- | --- |
| Dining entry counts | BUCard/QR + date/time/campus/turnstile support workflow | Strong served-demand proxy | Export granularity, retention, duplicate/refund semantics |
| Menu vote counts | BUCampus instant survey results | Menu-appeal signal | Historical export? campus identity? response bias? |
| Production/batch counts | Central kitchen + contractor service | Direct decision/target variable | Recorded where? when? by whom? |
| Campus allocation counts | Central production distributed to campuses | Distribution optimization | Planned vs delivered vs returned? |
| Packaged-meal counts | Package program / kiosk | Separate channel demand | Reserved, produced, collected, uncollected fields? |
| Waste weights | Official monthly reporting | Outcome measurement | Pre/post-consumer split, campus/meal granularity? |
| Complaint / feedback | Website + satisfaction survey | Failure/quality context | Structured history? privacy/legal constraints? |

### Rule

`Public clue that a system exists` must never be promoted to `we have the dataset`.

---

# 4. Model-design consequences for CS1

## 4.1 Start with decision-compatible baselines

The first benchmark should be interpretable and hard to beat:

1. last same-weekday demand;
2. rolling median by campus × meal;
3. term-state × weekday × campus × meal mean;
4. menu-aware nearest historical days;
5. operator forecast if it can be recorded prospectively.

Do not begin with LSTM/Transformer simply because the problem is temporal.

## 4.2 Add features by ablation, not accumulation

Recommended sequence:

```text
B0  historical demand only
B1  + service regime / academic calendar
B2  + menu identity / dish category
B3  + menu-poll preference signal
B4  + package/channel state
B5  + weather, events or other context only if incremental value survives holdout tests
```

## 4.3 Evaluate the decision, not only prediction accuracy

Required metrics should include:

- MAE / WAPE or another stable forecast metric;
- excess portions;
- shortage / sellout events;
- service-level guardrail;
- operator override rate;
- calibration or interval coverage if probabilistic output is used;
- waste outcome only when measured consistently enough to support it.

## 4.4 Use an asymmetric objective

A 50-portion shortage may be operationally worse than 50 excess portions, or vice versa. The loss function must come from operator evidence.

Conceptual objective:

```text
expected_cost(q) =
    C_excess × E[max(q - demand, 0)]
  + C_shortage × E[max(demand - q, 0)]
  + service_guardrails
```

Neither coefficient should be invented by CS1.

## 4.5 Structural breaks must be explicit

Train/test splitting should preserve time order and include regime shifts such as:

- term vs break;
- summer reduced-service periods;
- campus closures;
- Ramadan/special hours;
- introduction of package service;
- pricing/promotion changes;
- new scholarship/access programs.

Random row-wise train/test splitting risks leakage and unrealistic performance.

---

# 5. Literature additions

## L-04 — Calendar effects and meal ingredients can materially improve university refectory demand models

Mehmet Acı (2023), *Tehnički vjesnik / Technical Gazette*, modeled a university refectory without pre-booking and explicitly used **calendar effects and meal ingredients**. The best reported model in that case was a boosted ensemble decision tree with high predictive performance.

Use as: justification for testing calendar/menu context after baseline.  
Do not use as: proof that the same model will work at Boğaziçi.

Consensus record:  
https://consensus.app/papers/demand-forecasting-for-food-production-using-machine-acı/53fc30fe33fe579f8949e9a42a0ecc14/?utm_source=chatgpt

## L-05 — Turnstile entry data have been used for institutional cafeteria forecasting

Aydın, Balcıoğlu & Sezen (2025), *OPUS Journal of Society Research*, studied institutional cafeteria forecasting using **turnstile entry data** and time features. Their analysis highlights recent history, weekly cycles and academic-calendar effects as important predictors.

This makes the Boğaziçi BUCard/QR question particularly valuable: not because we know the data are available, but because an analogous data type has research precedent.

Consensus record:  
https://consensus.app/papers/machine-learning-techniques-for-cafeteria-demand-aydın-balcıoğlu/78329bb2e24e5c06a01d9f73bac74c0f/?utm_source=chatgpt

## L-06 — Short-term catering forecasting should be benchmarked against operator-like baselines

Rodrigues, Miguéis, Freitas & Machado (2023), *Journal of Cleaner Production*, evaluated machine-learning demand forecasting in multiple canteens and explicitly included baseline approaches intended to mimic current food-service forecasting. Reported results showed both waste-reduction and unmet-demand improvements in their case studies.

Design lesson: `ML vs naive` is insufficient if operators already use a stronger heuristic. The real benchmark should include the **current operator process** when possible.

Consensus record:  
https://consensus.app/papers/machine-learning-models-for-shortterm-demand-forecasting-rodrigues-miguéis/47d8e2ce5d015189bc052f02df2e3a47/?utm_source=chatgpt

---

# 6. PMR script — upgraded after the deep dive

## 6.1 Food Services Branch / administrative owner

1. Walk me through yesterday's lunch from menu planning to final contractor quantity.
2. Which quantity decisions are written in the tender/technical specification and which are discretionary?
3. When is the contractor first told the expected quantity?
4. Who is allowed to revise it, and until what time?
5. Is payment based on produced, delivered, served or another unit?
6. What happens financially when 300 portions are left over?
7. What happens operationally when 300 additional people arrive?
8. Which reports do you receive from the contractor after each meal/day/month?
9. Which of BUCard/QR counts, BUCampus menu votes, package-meal counts and waste weights can you already see?
10. What decision do you currently wish you could make earlier or with less uncertainty?

## 6.2 Contractor / kitchen operations

1. What was yesterday's planned lunch quantity and what was actually produced?
2. How many batches were produced, and at what times?
3. Can batch 2 be adjusted after seeing early service demand?
4. How are quantities allocated among six campuses and package service?
5. What is the largest recurring source of uncertainty?
6. Which dish types are hardest to forecast?
7. Which leftovers can be reused/donated and which must be discarded?
8. What shortage creates the biggest operational failure?
9. What excess creates the highest economic or waste cost?
10. What recommendation would you trust enough to change tomorrow's production by 5%?

## 6.3 IT / data owner

1. Are dining BUCard and QR entries stored historically?
2. Can counts be aggregated by date × time × campus × turnstile without PII?
3. Can entries be mapped to meal window and package/dine-in channel?
4. Are refunds/failed transactions identifiable?
5. How long are logs retained?
6. Are menu-survey vote totals stored historically and exportable?
7. Are service announcements and academic calendar available through structured feeds or export?
8. Can a pilot use read-only aggregate data without integrating personal identifiers?

---

# 7. Highest-value data request for a pilot

Do **not** ask for every database.

Ask first for a privacy-safe export containing, for 8–12 historical weeks if available:

```text
DATE
CAMPUS
MEAL_TYPE
SERVICE_CHANNEL          # dine_in / package / kiosk if available
PLANNED_PORTIONS          # if recorded
PRODUCED_PORTIONS         # if recorded
SERVED_OR_ENTRY_COUNT     # aggregate only
UNSERVED_SURPLUS          # if recorded
WASTE_KG                  # with category/semantics if recorded
MENU_ID / MAIN_COURSE
SERVICE_REGIME
```

Optional later:

```text
MENU_POLL_COUNT
SPECIAL_EVENT_FLAG
WEATHER
```

### Data rejection rule

If `WASTE_KG` cannot distinguish the measurement boundary, do not use it as the model target. Forecast served demand first and measure pilot waste prospectively.

---

# 8. New research hypotheses

| ID | Hypothesis | Public-source status | Fastest falsifier |
| --- | --- | --- | --- |
| RH-F01 | Food Services Branch is a key administrative decision stakeholder. | **SUPPORTED as governance role**, not yet buyer validation. | Interview reveals quantity planning sits entirely elsewhere and Food Services cannot influence it. |
| RH-F02 | Aggregate BUCard/QR entry data can provide a historical served-demand proxy. | PLAUSIBLE; access and semantics unknown. | IT says logs cannot be exported/retained/mapped to dining demand. |
| RH-F03 | BUCampus menu votes contain predictive information beyond menu identity. | UNKNOWN. | Historical ablation shows no out-of-sample gain or votes are inaccessible. |
| RH-F04 | Service-regime flags materially improve forecast robustness. | STRONGLY PLAUSIBLE from documented closures/schedule changes. | Time-aware benchmark shows no incremental value. |
| RH-F05 | Contractor incentives allow lower production recommendations to create economic value. | UNKNOWN. | Contract structure makes production quantity financially irrelevant or non-discretionary. |
| RH-F06 | Production can be adjusted in multiple batches after partial demand is observed. | UNKNOWN. | Kitchen workflow requires all production to be committed before meaningful demand signal. |
| RH-F07 | Packaged meals are a separate demand channel requiring separate forecasting/allocation. | PLAUSIBLE from separate service and menus. | Operations show packaged meals are drawn from identical unconstrained stock with no separate planning decision. |

---

# 9. What this changes for the KREATE application

## Stronger problem wording

Before:

> University cafeterias produce food under uncertain demand and may overproduce.

Better, still evidence-safe:

> `PUBLIC SOURCE` Boğaziçi operates a centralized multi-campus food service with approximately 6,000 daily meals, packaged-meal service, digital dining access, advance menus and a contractor governed by university technical specifications. It also reports 48,251 kg of food waste in 2025. `HYPOTHESIS` The team is testing whether the production/allocation quantity is set before enough demand information is available, and whether existing aggregate signals can support a human-reviewed adjustment without increasing shortages.

## Stronger persona wording

Do not write `cafeteria manager` generically.

Use PMR to distinguish:

- Food Services Branch administrative owner;
- food engineer/menu planner;
- contractor operations / central-kitchen production lead;
- campus service manager;
- IT/data owner;
- waste measurement/Zero Waste owner;
- procurement/control organization.

The buyer/user/approver may not be the same person.

---

# 10. Source inventory added in this deep dive

## Official Boğaziçi sources

1. **2025 SKS Activity Report** — food-service scale, package service, tender, survey, BUCampus menu process:  
   https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
2. **SKS Duties and Working Directive, Article 12** — formal Food Services Branch responsibilities:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/2106-bogazici-universitesi-saglik-kultur-ve-spor-d-20260521-143342.pdf
3. **2025 University Administration Activity Report** — beneficiary table, contract/control structure:  
   https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf
4. **2024 SKS Activity Report** — 2024 annual meal-service counts:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/303-2024-yili-faaliyet-raporu-yayin-20251205-150840.pdf
5. **BUCampus v1.1.2 announcement** — package menus, food poll, events, academic calendar:  
   https://bilgiislem.bogazici.edu.tr/tr/news/kampus/2/bucampusun-yeni-versiyonu-yayinda/3351
6. **Menu survey** — weekly Wednesday lunch voting mechanics:  
   https://yemekhane.bogazici.edu.tr/menu-anketi
7. **Dining FAQ** — BUCard/QR and date/time/campus/turnstile support metadata:  
   https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
8. **Summer 2025 service reduction**:  
   https://yemekhane.bogazici.edu.tr/yaz-donemi-yemek-hizmeti-hakkinda
9. **Sarıtepe/Kilyos summer 2025 service change**:  
   https://yemekhane.bogazici.edu.tr/saritepe-kilyos-kampus-yemek-hizmeti-hakkinda
10. **Academic calendar**:  
    https://akademiktakvim.bogazici.edu.tr/
11. **Dining menus**:  
    https://yemekhane.bogazici.edu.tr/

## Academic literature

1. Mehmet Acı (2023), *Demand Forecasting for Food Production Using Machine Learning Algorithms: A Case Study of University Refectory*, Technical Gazette.  
   https://consensus.app/papers/demand-forecasting-for-food-production-using-machine-acı/53fc30fe33fe579f8949e9a42a0ecc14/?utm_source=chatgpt
2. B. Aydın, Y. S. Balcıoğlu, Bulent Sezen (2025), *Machine Learning Techniques for Cafeteria Demand Forecasting: An Institutional Case*, OPUS Journal of Society Research.  
   https://consensus.app/papers/machine-learning-techniques-for-cafeteria-demand-aydın-balcıoğlu/78329bb2e24e5c06a01d9f73bac74c0f/?utm_source=chatgpt
3. Miguel Rodrigues, V. Miguéis, S. Freitas, T. Machado (2023), *Machine learning models for short-term demand forecasting in food catering services: A solution to reduce food waste*, Journal of Cleaner Production.  
   https://consensus.app/papers/machine-learning-models-for-shortterm-demand-forecasting-rodrigues-miguéis/47d8e2ce5d015189bc052f02df2e3a47/?utm_source=chatgpt

---

# 11. Bottom line

The research has moved the thesis from a broad sustainability idea to a testable operational system:

> **central kitchen + contractor + six campuses + multiple service channels + digital access/preference signals + strong calendar/service-regime effects**

The highest-value unknown is no longer whether Boğaziçi has food waste or digital infrastructure. It is:

> **Who controls the final production/allocation quantity, when is it frozen, which aggregate signals are available before that deadline, and what is the real cost of excess versus shortage?**

That question should drive the next PMR, data request and CS1 baseline.