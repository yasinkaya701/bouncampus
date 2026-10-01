# Boğaziçi PMR Pre-Interview Evidence Pack — Dining Decision & Contract Control

**Research date:** 2026-10-01  
**Purpose:** Convert the strongest current public-source findings into interview-ready PMR questions, owner routing and falsification tests.  
**Status:** Secondary/public-source research only. **This is NOT PMR, interview evidence, customer validation, endorsement or proof of data access.**

---

# 0. Executive conclusion

The existing research already establishes the broad food-waste, procurement, Türkiye benchmark and academic context. The remaining PMR bottleneck is narrower:

> **Who controls the contract-relevant dining quantity/allocation decision, when does it become costly to change, which signals exist before that point, and which physical/contract record defines success or failure?**

New public-source work sharpens that path in three ways:

1. Boğaziçi publicly lists an active **“Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı”**. This creates a more direct route for questions about outsourced-service control, acceptance records, compliance and service failures than treating sustainability staff as the contract-workflow owner.
2. A current university page lists **two Food Engineers inside the Food Services Branch — Barış Pancar and Gül Güler**. Barış Pancar is also listed as a member of the dining control organization. These roles are high-value candidates for reconstructing menu/grammage, service constraints, production timing and operational records.
3. The 2025 SKS activity report describes a multi-channel dining operation: **6,000 daily meals, 2,000 packaged meals, a North Campus kiosk, BUCampus menu selection, tasting/feedback activities and planned daily BUCampus meal rating**. PMR must therefore test **allocation by campus/meal/service channel**, not only one university-wide demand number.

The web research did **not** establish the successful 2026–2027 tender's exact daily call-off, hakediş/acceptance, excess-payment or shortage-penalty mechanics. Those must move to primary research or verified tender-document access rather than being inferred.

---

# 1. Claim firewall

Use this pack to prepare interviews, not to claim customer validation.

- A public role listing proves only that a role/person is publicly associated with the listed unit or control organization.
- Membership in the control organization does **not** by itself prove which member owns daily quantity approval, hakediş or acceptance.
- “Food Engineer” is a useful role signal, not proof that the person sets production quantity.
- Publicly reported daily/packaged meal figures do not establish how quantities are forecast, ordered, produced or paid.
- BUCampus menu selection/ratings are evidence that digital feedback/preference mechanisms exist; they do **not** prove these signals are used for production planning.
- BUCard/BUCampus service ownership does not prove historical event retention or export access.
- The 48,251 kg 2025 food-waste figure is a university-reported total; it does not identify the share caused by overproduction, preparation loss or plate waste.
- No public-source finding in this file may be promoted to `INTERVIEW EVIDENCE`.

---

# 2. P0 source register

## PMR-S01 — Dining control organization

**Source:** Boğaziçi University, University Executive Board Committees and Commissions  
https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

**Publicly listed organization:** `Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı`

**Principal members listed at research date:**

- Ayhan Soylu — President
- Barış Pancar
- Aygül Demir
- Ahmed Musab Taş
- Mustafa Tunç

**Alternates listed at research date:**

- Mustafa Melep — President
- Niyazi Şahin
- Ali Kaplan
- Mesut Okur
- Aylin Koç

**What this supports:** there is a formally named current control organization for dining/cooking/distribution.

**What remains unknown:** exact decision rights, inspection cadence, acceptance/hakediş fields, shortage/excess reporting, and whether this group sees daily quantity decisions before production.

**PMR questions created:**

1. Which records does the control organization review to accept/verify the contractor's service?
2. Which quantity fields appear in daily/monthly control or acceptance records?
3. Are ordered, produced, delivered and served quantities distinguished?
4. How are shortages, substitutions, leftovers and service failures documented?
5. Who can approve a quantity/allocation change and until what time?
6. Which control-organization member is the best owner for contract-execution data semantics?

---

## PMR-S02 — Food Services technical staff and service topology

**Source:** Boğaziçi University Institutional Data, Sustainable Food Choices on Campus  
https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313

**Publicly listed Food Services roles:**

- Aygül Demir Yolasığmazoğlu — Branch Manager
- Barış Pancar — Food Engineer
- Gül Güler — Food Engineer
- Hakan Deniz — Office Personnel
- İsmet Gündoğan — Office Personnel

The same source publishes campus-specific breakfast/lunch/dinner service windows and states that meals are prepared in the North Campus cafeteria kitchen while procurement-to-service stages are performed by the contractor under an SKS technical specification.

**What this supports:** Food Services has named technical food-engineering roles and a multi-campus/multi-meal operational structure.

**What remains unknown:** who determines production quantity, whether Food Services or the contractor owns forecasting, batch timing, campus allocation, and which internal records each role sees.

**PMR questions created for Food Engineers:**

1. Walk through the most recent normal lunch from menu approval to final service quantity.
2. Which gram/portion/menu constraints are fixed before quantity is decided?
3. When are ingredients committed and when does cooking become costly to change?
4. Is production one batch or multiple adjustable batches?
5. Is allocation decided by campus and service channel separately?
6. What do you record for produced, delivered, served, returned, leftover and discarded food?
7. Which part of observed food waste is actually preventable production surplus?
8. Which shortage/service guardrail would make a lower production recommendation unacceptable?

---

## PMR-S03 — Current operating channels and feedback mechanisms

**Source:** SKS 2025 Activity Report / 2026–2027 Goals  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

**Publicly reported current/2025 operating signals include:**

- 6 dining halls;
- 6,000 daily meals;
- 2,000 packaged meals;
- packaged-meal distribution introduced;
- North Campus kiosk established;
- 2,386-person satisfaction survey;
- food-tasting activity;
- instant web request/complaint area;
- BUCampus menu-selection process;
- planned daily meal rating through BUCampus for 2026–2027.

**Important semantic caution:** the report displays several activity counts (including `BUBizden`) with different meanings. Do not add them together or treat them as one demand denominator without owner confirmation.

**PMR implication:** the controllable decision may be a vector rather than a scalar:

```text
quantity(date, meal_type, campus, service_channel)
```

Candidate `service_channel` values should be discovered from the operator rather than hard-coded, but public sources justify explicitly asking about dining-hall, packaged-meal and kiosk flows.

**Questions created:**

1. Are packaged meals planned from the same production pool as dining-hall service?
2. At what point is quantity split across campuses/channels?
3. Can surplus be reallocated between channels or campuses after production?
4. Are BUCampus menu-selection or rating data consulted before quantity decisions?
5. Is any existing digital signal closer to purchase/attendance intent than a menu preference vote?
6. What is the current operational use of complaints, tasting and satisfaction data?

---

## PMR-S04 — Food-waste measurement boundary

**Source:** Boğaziçi University Institutional Data, Campus Food Waste Tracking  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

**Publicly reported 2025 total:** 48,251 kg food waste. The page also reports monthly values and amounts delivered to İSTAÇ for recycling.

**What this supports:** a material, recurring and publicly tracked food-waste stream exists.

**What it does not resolve:** pre-consumer vs post-consumer share, edible surplus vs preparation waste, campus/meal attribution, collection-time vs generation-time semantics, and causal link to demand mismatch.

**PMR questions created:**

1. What physical material enters the published `food waste` total?
2. Is it weighed at kitchen, dining hall, collection point or transporter handoff?
3. Can pre-consumer surplus, preparation loss and plate waste be separated?
4. Can records be attributed by campus, meal or date of service?
5. Is the date the generation date or collection date?
6. Which source record is authoritative for a prospective pilot?

---

## PMR-S05 — BUCard / BUCampus system ownership boundary

**Sources:** Boğaziçi University Information Technology Department  
https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513  
https://bilgiislem.bogazici.edu.tr/

The public service inventory identifies BUCard dining-related services and the IT department publicly lists BUCAMPUS among university digital products/services.

**What this supports:** BİD is a relevant technical/data owner to ask about aggregate historical records and system boundaries.

**What remains unknown:** event retention, table/schema ownership, timestamps, duplicate/refund semantics, historical exportability, pre-decision latency, and approvals required for a pilot.

**PMR data questions:**

1. Are dining BUCard/QR events retained historically?
2. Can counts be exported as privacy-safe `date × campus × meal window` aggregates?
3. Which timestamp represents actual service consumption?
4. Are failed, refunded, duplicate or second-meal events distinguishable?
5. Are BUCampus menu-selection/rating events retained as aggregate counts?
6. When are these data available relative to the production freeze time?
7. Which data can be used without individual identifiers?

---

## PMR-S06 — Dietetics/control-role overlap

**Sources:** Boğaziçi University Mediko  
https://mediko.bogazici.edu.tr/tr/announcements/diyetisyenlik-hizmetimiz-baslamistir/2845  
https://mediko.bogazici.edu.tr/tr/pages/diyetisyenler/2664

The Mediko source identifies Ayhan Soylu and Ahmet Musab Taş in dietetics; the current control-organization page lists Ayhan Soylu and a similarly named `Ahmed Musab Taş` in the dining control organization.

**Data-quality note:** the public pages use different spellings (`Ahmet` / `Ahmed`). Do not silently normalize identity in downstream evidence. Treat the overlap as a routing clue to verify, not as an identity assertion beyond the source wording.

**PMR implication:** nutrition/menu constraints may have a formal operational-control interface that should be understood before optimizing quantity.

**Questions:**

1. Which nutrition/grammage constraints are non-negotiable when quantities change?
2. Are special-diet/vegetarian/vegan quantities forecast separately?
3. Which service-quality failures are formally recorded by the control organization?
4. Which food-safety/nutrition requirements must be excluded from automated optimization?

---

## PMR-S07 — Current 2026–2027 procurement

**Existing detailed pack:** `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`

Canonical current procurement identifiers already recorded there:

- İKN `2025/1727143`
- service period `2026–2027`
- unit-price service procurement
- 3.13 million listed meal units across student meal, breakfast and staff meal lines
- current contractor: TEMAŞ Gıda Sanayi ve Ticaret A.Ş.

Useful public mirrors/records:

- https://www.ihaledetay.com/2025-1727143
- https://ekapveri.com/ihale/ekap-2025-1727143/
- Official EKAP access surface: https://ekap.kik.gov.tr/EKAP/

**Critical unresolved contract questions:**

- Is there a daily call-off/requested quantity?
- Can it be revised, and until when?
- Which quantity becomes accepted/payable?
- Is unserved production payable?
- Who bears excess-food cost?
- What shortage/service deductions or penalties apply?
- Which progress-payment/acceptance records hold the cleanest historical quantity field?

### Source-access gap

Normal indexed public-web research did not surface a verified copy of the successful tender's complete technical specification and progress-payment semantics. **Do not fill that gap using clauses from a cancelled Boğaziçi tender or another university.** Route it to verified EKAP/tender-document access and the relevant Boğaziçi contract/control owner.

---

# 3. Evidence-to-interview matrix

| Public-source signal | Research inference | Exact PMR test | Best first owner | Kill/modify condition |
| --- | --- | --- | --- | --- |
| Formal dining control organization exists | Contract execution has an explicit control surface | Which record defines accepted service quantity? | Control organization / Food Services | No quantity-level record or no actionable decision before service |
| Food Services has food engineers | Technical production knowledge is institutionally reachable | Reconstruct last service from menu to batch to leftover | Food Engineer | Role has no visibility into production or contractor workflow |
| 6,000 daily + 2,000 packaged reported | Allocation may be multi-channel | Is channel allocation decided separately and when? | Food Services + contractor | Channels do not share a controllable production pool |
| BUCampus menu selection exists | Preference signal may exist before service | Is it used; does it correlate with actual attendance/choice? | Food Services + BİD | Signal is post-decision, too sparse or semantically unrelated to attendance |
| BUCard dining service exists | Aggregate consumption history may exist | Can privacy-safe historical counts be exported before/after freeze? | BİD | No suitable historical record or access cost is prohibitive |
| 48,251 kg food waste tracked | Outcome stream is measurable at some boundary | What share is edible pre-consumer surplus? | Waste/sustainability owner + Food Services | Overproduction is immaterial in the measured stream |
| Unit-price procurement | Quantity is contractually relevant at some level | What is ordered/accepted/payable and who benefits from accuracy? | Food Services/control org/SKS | Payment/incentives make quantity improvement economically irrelevant |

---

# 4. Revised PMR interview order

Use the smallest owner set needed to close the highest-risk unknowns. Do not shotgun every public contact.

```text
1. Food Services Branch manager + one Food Engineer
   -> reconstruct real workflow, freeze time, records, service-channel allocation

2. Dining Control Organization owner/member
   -> only for unresolved acceptance, inspection, shortage and hakediş semantics

3. TEMAŞ local project / production operator
   -> production heuristic, batch irreversibility, internal fields, excess/shortage economics

4. BİD data owner
   -> privacy-safe BUCard/BUCampus history, timing, granularity and access

5. Waste / sustainability measurement owner
   -> waste boundary, stage split and defensible impact metric

6. SKS senior owner
   -> permissions/escalation only after the workflow and bounded request are concrete
```

### Why Food Engineer moved up

The current public source identifies technical Food Services roles that are likely better positioned than generic office staff to explain menu, gram/portion, production and service constraints. This is a routing hypothesis only; if the branch manager identifies a different direct operator, follow the actual workflow.

---

# 5. Interview modules

## Module A — last real production decision

Ask for the last normal lunch/dinner where demand differed from expectation.

```text
expected quantity
-> who estimated it
-> inputs visible at that time
-> approval
-> freeze time
-> produced quantity
-> campus/channel allocation
-> served quantity
-> excess/shortage
-> response
-> final record used for control/payment
```

Avoid “Would AI forecasting be useful?” until the current process is reconstructed.

## Module B — contract and incentive semantics

Ask:

- What is the operational name of the quantity sent to the contractor?
- What is the operational name of the quantity used for acceptance/hakediş?
- Which quantity can still change after the first request?
- Who loses money/time/reputation when excess occurs?
- Who loses when shortage occurs?
- Does the contract create a reason for either side to prefer overproduction?

## Module C — data timing

For every candidate feature, record:

```text
field
owner
source system
available_at
production_freeze_at
historical_retention
granularity
privacy class
known data-quality issue
```

A feature arriving after `production_freeze_at` is not a valid decision input even if it predicts demand well retrospectively.

## Module D — waste causality

Ask for the most recent measured waste incident and separate:

- preparation/trimming loss;
- edible production surplus;
- plate/post-consumer waste;
- expired/spoiled inventory;
- other categories used locally.

Do not force the university's categories into this taxonomy if the actual operational categories differ.

---

# 6. PMR hypotheses and falsifiers

| ID | Hypothesis to test | Public-source status | Primary falsifier |
| --- | --- | --- | --- |
| PMR-RH-01 | A daily production/allocation decision exists before service and can be changed at a useful time. | UNKNOWN | Owner says quantity is fixed externally/too early or cannot be adjusted materially. |
| PMR-RH-02 | Food Services/contractor retains service-level quantity records usable for retrospective baseline construction. | UNKNOWN | Records are absent, too aggregated, semantically inconsistent or inaccessible. |
| PMR-RH-03 | Edible pre-consumer surplus is a material part of the tracked food-waste problem. | UNKNOWN | Measured waste is dominated by plate/preparation/other streams. |
| PMR-RH-04 | Campus/service-channel allocation is a distinct operational control point. | PLAUSIBLE from multi-channel reporting; unverified. | All channels are operationally fixed or allocation cannot change. |
| PMR-RH-05 | At least one privacy-safe demand/intent signal is available before freeze time. | UNKNOWN | BUCard/BUCampus/calendar/menu signals are unavailable or arrive after the decision. |
| PMR-RH-06 | Improving quantity accuracy creates value for at least one decision owner without unacceptable shortage risk. | UNKNOWN | Contract incentives neutralize savings or service-risk dominates. |
| PMR-RH-07 | Existing feedback/preference mechanisms leave residual uncertainty that justifies forecasting/decision support. | UNKNOWN | Reservation/intent/simple rules already solve the actionable uncertainty. |

---

# 7. Stop-browsing boundary — these now require PMR or verified internal documents

Do not keep turning the following into web-research tasks unless a genuinely new first-party document appears:

1. **Exact daily quantity owner and freeze time.** Public pages do not establish this.
2. **Hakediş/acceptance quantity semantics.** The indexed successful-tender summaries do not resolve this.
3. **Excess vs shortage financial incidence.** Do not infer from contract value or unit-price structure.
4. **Pre-consumer share of 48,251 kg food waste.** Public totals do not provide a causal stage split.
5. **Historical BUCard/BUCampus exportability.** Product/service existence is not data-access evidence.
6. **Operational use of BUCampus menu votes/ratings.** Existence is not evidence of decision use.
7. **TEMAŞ's internal forecasting heuristic.** Requires local project/production PMR.
8. **Real batch/reallocation flexibility.** Requires the operator/food-engineering workflow.

This boundary prevents “more research” from substituting for the KREATE rubric's primary-market-research requirement.

---

# 8. Minimum evidence package after the first three interviews

The PMR program should not claim the dining wedge validated until it can fill this table with real primary evidence:

| Field | Required answer |
| --- | --- |
| quantity_decision_owner | named role, not guessed person |
| production_freeze_time | actual clock/event trigger |
| adjustment_rights | what can change after first estimate |
| service_segmentation | meal × campus × channel semantics |
| current_forecast_method | actual heuristic/system |
| accepted_quantity | field used for operational/contract acceptance |
| excess_consequence | physical + economic + workflow consequence |
| shortage_consequence | service + contractual + reputational consequence |
| historical_data | available fields, horizon, granularity |
| waste_boundary | measured stage/category |
| actionable_signal | available before freeze |
| pilot_owner | person/role able to approve bounded pilot |

Until then, model architecture, saving percentages and commercial ROI remain hypotheses.

---

# 9. Agent handoff

## IE

Use this pack as the pre-interview brief. Prioritize one Food Services conversation that includes a technical operator/food engineer and reconstructs a **specific recent service**.

## CS1

Do not assume one scalar `daily_meals` target. Be ready for `date × meal × campus × service_channel`, but only implement dimensions confirmed by real data semantics. Freeze-time reachability remains a hard gate.

## EE

Do not design new measurement hardware until the Food Services/control interviews identify existing scales, waste records and stage boundaries.

## CS2

Keep public-source facts and PMR evidence separate. The strongest application story is not that public sources prove forecasting works at Boğaziçi; it is that the team used public sources to identify the exact unresolved decision and then tested it with the real owners.

---

# 10. Source checklist before each interview

Read only the sources relevant to that owner:

### Food Services / Food Engineer

- This pack
- `BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`
- `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`
- SKS activity report
- Sustainable Food Choices page

### Control Organization / contract owner

- This pack
- `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`
- `TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md`
- Current Boğaziçi control-organization page

### Contractor

- This pack
- `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`
- `TURKIYE_DINING_RESERVATION_SIGNALS.md`

### BİD

- This pack
- `BOGAZICI_SOURCE_RECONCILIATION.md`
- `METRIC_PROVENANCE_AND_VERIFICATION.md`

### Waste / sustainability owner

- `BOGAZICI_SUSTAINABILITY_2025.md`
- `TURKIYE_ZERO_WASTE_CAMPUS_MEASUREMENT_CONTEXT.md`
- Campus Food Waste Tracking source

---

# Bottom line

Secondary research has now done its job: it has narrowed the first PMR problem from “Does the university have a sustainability/food-waste problem?” to a concrete institutional decision chain.

The next high-value work is **primary evidence**:

> reconstruct one real meal decision from forecast/request -> production -> allocation -> service -> excess/shortage -> acceptance/payment -> waste record, with exact roles and timestamps.

Anything less risks optimizing a metric that the operator cannot act on.