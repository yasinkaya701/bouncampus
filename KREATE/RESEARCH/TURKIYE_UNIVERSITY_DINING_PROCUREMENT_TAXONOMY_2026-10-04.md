# Türkiye University Dining Procurement Taxonomy — 2026-10-04

**Purpose:** Understand how daily meal-demand uncertainty, production responsibility, payment and excess/shortage risk vary across Turkish university dining contracts.  
**Status:** Secondary public procurement research. **Other universities' clauses must not be projected onto Boğaziçi.**

---

# Executive conclusion

"University dining" is not one homogeneous commercial workflow.

Public procurement decisions show at least four materially different structures:

1. **administration determines production quantity using reservations + forecast walk-ins**;
2. **contractor forecasts production from historical counts/context**;
3. **administration notifies quantity but contractor bears mismatch risk and payment follows consumption**;
4. **forecast responsibility is assigned without enough reference data, creating procurement-level uncertainty/dispute**.

This strengthens the need to segment the beachhead by **decision/control/payment structure**, not merely by institution size or public/private status.

---

# Case 1 — İzmir Katip Çelebi University: reservation + expected walk-in model

Public Procurement Board decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2025UH.II-2367-kamu-ihale-karari-kik

Decision: `2025/UH.II-2367`  
University: İzmir Katip Çelebi University

## Publicly reproduced clauses

Daily production quantity is calculated using:

- university information-system reservations;
- expected guests;
- estimated non-reserved students/personnel.

The administration determines the production quantity and the contractor produces it.

The specification further states:

- students/personnel should not be turned away when the meal is insufficient;
- contractor must make emergency replacement food where required;
- the administration is not responsible for excess production/unsold meals;
- diner count is calculated using electronic-card / turnstile passages;
- contractor payment uses that count;
- non-reservation sales are separately documented through cash-register records.

## Decision structure

```text
reservation + walk-in estimate
        ↓
administration quantity decision
        ↓
contractor production
        ↓
turnstile-realized diners
        ↓
payment
```

## Product implication

A planning system in this structure may need to support the **university quantity owner**, while the contractor carries some operational excess/shortage exposure.

---

# Case 2 — Kırıkkale University: contractor forecasts using previous meal counts

Official Public Procurement Board decision:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

Decision: `2026/UH.I-2269`

## Publicly reproduced clauses/findings

The technical specification required daily meal quantities to be determined by the contractor taking previous meal counts into account.

The procurement decision also records that:

- actual demand can vary with academic calendar, exam periods, weather and menu;
- payment is based on meals actually consumed/purchased under the contract mechanism;
- excess food does not create liability for the administration;
- insufficient production can expose the contractor to service/penalty consequences.

## Decision structure

```text
historical consumption + context
        ↓
contractor forecast
        ↓
contractor production
        ↓
actual consumption
        ↓
payment / excess-risk exposure
```

## Product implication

Here the **contractor** is a strong candidate user/economic beneficiary.

A university-only SaaS assumption would be wrong without resolving this structure.

---

# Case 3 — Karabük University: historical data + turnstile settlement + contractor planning

Public Procurement Board decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2025UH.I-1089-kamu-ihale-karari-kik

Decision: `2025/UH.I-1089`  
University: Karabük University

## Publicly reproduced clauses/findings

The decision records:

- 700,000-meal service scope;
- daily meal counts to be determined by the contractor using previous meal counts;
- academic calendar, summer/semester breaks, exams, weather and menu as demand-changing context to be considered;
- payments based on meals actually eaten;
- turnstile records / fallback meal tickets as payment evidence;
- administration not responsible for surplus food;
- previous **five years** of consumed-meal counts were included by month in the technical specification.

## Decision structure

```text
historical multi-year consumption
+ calendar/weather/menu context
        ↓
contractor quantity plan
        ↓
turnstile actual consumption
        ↓
payment
```

## Product implication

This is especially relevant to BOUNCAMPUS because the specification itself recognizes several candidate demand features already contemplated in the proposed model.

But this also means:

> calendar/weather/menu features are **not a novel idea by themselves**.

Differentiation must be in evidence quality, modeling/decision utility, workflow and verification.

---

# Case 4 — İstanbul Technical University: electronic consumption records + shortage response

Public Procurement Board decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-740-kamu-ihale-karari-kik

Decision: `2026/UH.II-740`  
University: İstanbul Technical University

## Publicly reproduced clauses/findings

The decision records:

- meals are accessed with university/student/personnel/guest cards via turnstiles;
- after each service, turnstile reports are recorded with contractor acknowledgement;
- contractor payments use these electronic records;
- daily payment quantity is determined from cafeteria automation data;
- where food is about to run out, the contractor must prepare additional equivalent food in consultation with the administration;
- the decision explicitly recognizes meal demand can increase/decrease and payment is based on consumed meal count.

## Decision structure

```text
planned/communicated demand
        ↓
service
        ↓
possible in-service additional production
        ↓
turnstile / cafeteria automation actual count
        ↓
payment
```

## Product implication

This exposes an important alternative intervention point:

> The best decision may not always be one static prior-day quantity; it can be **batch release / in-service replenishment** if the operation permits it.

PMR at Boğaziçi must therefore ask whether production is split into batches and whether later batches can react to early service information.

---

# Case 5 — Gebze Technical University: forecasting without reference data became a procurement issue

Public Procurement Board decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-962-kamu-ihale-karari-kik

Decision: `2026/UH.II-962`  
University: Gebze Technical University

## Publicly reproduced clause/finding

The technical specification stated that the administration did not have to pre-notify the contractor of daily student diner counts and the contractor would determine them by estimation.

The Board noted that the documents did not provide a useful daily distribution/reference basis and concluded that expecting a bidder to run the service based only on its own estimates created material uncertainty for healthy bid preparation.

## Product implication

This is strong evidence that **reference-data availability and demand uncertainty can be contractually material**, not merely a model-development inconvenience.

It does **not** demonstrate software purchasing demand.

---

# Boğaziçi — what public procurement currently establishes

Current successful procurement:

- IKN: `2025/1727143`;
- period: 01.01.2026–31.12.2027;
- 2,500,000 student meals;
- 380,000 breakfast/sahur units;
- 250,000 staff meals;
- six campuses;
- contractor: TEMAŞ;
- contract value: 759,537,563.59 TRY.

Public mirrors:

- https://www.ihaledetay.com/2025-1727143
- https://ekapveri.com/ihale/ekap-2025-1727143/

The public notice also requires production-capacity evidence at **5,000 meals/day**, described as half the administration's daily need, implying a 10,000-meal/day procurement design scale. This should **not** be substituted for observed daily consumption.

## Still unresolved in publicly indexed material

The publicly indexed notice/result does **not** establish:

- who sets tomorrow's quantity;
- whether a reservation exists;
- exact freeze time;
- whether quantity can change by batch/campus/channel;
- whether payment uses ordered/produced/delivered/served/turnstile quantity;
- whether excess production is paid;
- which side owns ingredient loss;
- shortage penalties/response rules.

The detailed tender documents are referenced as available in EKAP. Until those clauses are inspected or the workflow owner is interviewed, these remain `UNKNOWN`.

---

# Procurement taxonomy for beachhead segmentation

For every target institution, collect:

| Axis | Values to distinguish |
| --- | --- |
| Quantity owner | university / contractor / joint |
| Demand input | reservation / historical consumption / manual estimate / event/calendar / other |
| Production timing | prior-day / same-day / rolling batches |
| Adjustment right | none / before cooking / by campus / in-service replenishment |
| Settlement basis | ordered / produced / delivered / electronic served / other |
| Excess-risk owner | university / contractor / shared / unclear |
| Shortage-risk owner | university / contractor / shared / unclear |
| Actual-demand record | turnstile / POS / tickets / manual / none |
| Historical reference supplied | none / months / years / reservation snapshots |
| Service architecture | central kitchen / distributed / hybrid |
| Channels | dine-in / package / kiosk / other |

---

# Commercial implications

## Structure A — contractor bears forecast error

Likely value path:

> contractor operations software / shared planning tool

because better planning can reduce direct ingredient/production risk.

## Structure B — university bears ordered/produced quantity

Likely value path:

> university food-services decision support

because the institution may capture direct savings.

## Structure C — university chooses quantity, contractor bears excess

Potential incentive conflict:

- university may prioritize availability;
- contractor may prioritize lower excess;
- both need transparent shortage/surplus trade-off.

A shared planning/approval layer may be more valuable than one-sided automation.

## Structure D — payment only actual consumption, but quantity planning still manual

Savings may accrue mainly to contractor, while university benefits from service quality/sustainability.

Economic buyer cannot be inferred from beneficiary alone.

---

# Highest-value PMR question after procurement research

> **"For yesterday's lunch, who chose the number produced, what quantity was recorded for payment, and who lost money or absorbed work when the forecast was wrong?"**

One concrete answer resolves more commercial uncertainty than asking whether the stakeholder wants an AI forecasting platform.

---

# Strategic consequence

The beachhead should not be defined as:

> "all Turkish universities"

or even:

> "large public universities."

A more product-relevant segment is:

> **high-volume institutional university dining operations where a recurring quantity decision exists, forecast error creates a consequence for a reachable operator/buyer, and actual consumption can be measured.**

This definition can include both public and foundation universities if the workflow/economics are similar, while excluding superficially similar institutions whose decision structure is incompatible.
