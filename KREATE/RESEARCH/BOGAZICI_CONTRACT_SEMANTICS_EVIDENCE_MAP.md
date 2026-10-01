# Boğaziçi Dining Contract Semantics — Evidence Map

**Research date:** 2026-10-01  
**Purpose:** Separate what the current Boğaziçi–TEMAŞ procurement publicly establishes from the quantity/payment semantics that remain unknown, and turn those gaps into an executable PMR/data-acquisition and decision-model plan.  
**Status:** Secondary/public-source research only. **NOT legal advice. NOT signed-contract interpretation. NOT PMR.**

Related packs:

- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md`](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md)
- [`BOGAZICI_PMR_TARGET_MAP.md`](./BOGAZICI_PMR_TARGET_MAP.md)

---

# 0. Executive conclusion

The public record now establishes a large, formal, quantity-based operating environment:

```text
3,130,000 listed meal units / 2026–2027
6 campuses
unit-price service contract
price adjustment provided
10,000-meal/day procurement design requirement
Food Services Branch prepares specifications and monitors contractor compliance
current contractor = TEMAŞ Gıda
```

But the economically decisive variable remains unresolved:

> **Which daily quantity becomes the contract-accepted / payable quantity, and who can change it before service?**

A forecast can be statistically excellent and still have little value if it predicts a quantity that is not connected to the real contractual decision. Therefore the next product gate is **contract semantics**, not model sophistication.

---

# 1. Evidence hierarchy for contract claims

Agents must not blend evidence tiers.

| Tier | Source class | What it may establish | What it must not be used for |
| --- | --- | --- | --- |
| C1 | Signed current contract + current technical/admin specification | Actual 2026–2027 payment, ordering, penalty, adjustment and acceptance clauses | — |
| C2 | Current successful tender notice/result, İKN `2025/1727143` | Procurement quantities, unit-price structure, contractor, campuses, capacity requirement, approximate cost/contract value | Daily call-off, hakediş basis or excess/shortage allocation unless explicitly stated |
| C3 | Current Boğaziçi governance/activity documents | Organizational responsibilities, monitoring/control, service context | Signed-contract economics not stated there |
| C4 | Cancelled predecessor, İKN `2025/1335958` | Procurement provenance and evidence that documentation changed after objections | Current contract clause evidence |
| C5 | Other universities' KİK decisions/specifications | Sector precedents and questions worth testing | Boğaziçi-specific contract facts |
| C6 | Academic literature | Decision-model design references | Local workflow, savings or contract facts |

**Promotion rule:** Boğaziçi payment/penalty/order claims require C1 evidence or direct owner confirmation tied to a current artifact.

---

# 2. Current successful procurement — what is actually established

## CSEM-01 — Quantity is explicitly represented in the procurement

`PUBLIC SOURCE / C2`

Current successful procedure:

- **İKN:** `2025/1727143`
- student meal: **2,500,000** meal units;
- breakfast including sahur: **380,000** meal units;
- staff meal: **250,000** meal units;
- total listed quantity: **3,130,000** meal units;
- period: **01.01.2026–31.12.2027**;
- six campuses: North, South, Kilyos, Kandilli, Hisar, Anadolu Hisarı.

Source reproducing official EKAP notice/result:  
https://www.ihaledetay.com/2025-1727143

EKAP-derived record:  
https://ekapveri.com/ihale/ekap-2025-1727143/

## CSEM-02 — It is explicitly a unit-price contract

`PUBLIC SOURCE / C2`

The successful tender notice states that bids are formed by multiplying each line-item quantity by the offered unit price and that the successful bidder signs a **unit-price contract**.

This establishes that quantity is contractually meaningful at least at procurement-line level.

It does **not** establish which realized daily quantity is invoiced or accepted.

## CSEM-03 — Current procurement economics are large but cannot be treated as waste economics

`PUBLIC SOURCE / C2`

- approximate cost: **873,226,063.59 TRY**;
- contract value: **759,537,563.59 TRY**;
- bids received: **14**;
- valid bids: **7**;
- contractor: **TEMAŞ Gıda Sanayi ve Ticaret A.Ş.**;
- contract date: **25.12.2025**;
- price adjustment is indicated as provided (`Fiyat Farkı Verilecek`).

The contract value is **not** a food-waste cost pool. A saved physical portion cannot be converted to TRY from this total without line-item unit prices and verified payment/acceptance semantics.

---

# 3. Capacity wording reveals a peak/design scale, not observed demand

## CSEM-04 — 5,000 meals is defined as half of the administration's daily requirement

`PUBLIC SOURCE / C2`

The successful notice requires a bidder capacity report covering **5,000 meals**, explicitly described as **one-half of the administration's daily meal requirement**.

Therefore the procurement wording implies a **10,000-meal daily design requirement**.

Source:  
https://ekapveri.com/ihale/ekap-2025-1727143/

### Critical semantics warning

Do not label `10,000` as average daily attendance or measured demand.

The listed two-year contract volume is 3.13 million meal units. At 10,000 meals/day, that volume corresponds to only **313 equivalent full-load days across the two-year contract**. This is a derived scale comparison, not evidence of the actual service-day calendar.

Other Boğaziçi public reports also use different operational figures (for example, a 6,000-daily-meal figure). Treat these as separate source-defined metrics until the owner supplies a data dictionary.

### Product implication

Capacity and demand are different variables:

```text
available production capacity != planned production != actual served demand
```

The product should never infer demand from capacity.

---

# 4. Governance map reveals where the missing contract semantics may live

## CSEM-05 — Food Services owns specification and contractor-control duties

`PUBLIC SOURCE / C3`

Boğaziçi University's current SKS directive gives the Food Services Branch duties including:

- preparing food-service tender work;
- preparing technical specifications;
- monitoring and controlling contractor-provided food service;
- preparing/publishing menus;
- checking service compliance with the contract and technical specification;
- secretariat duties for the Food Services Executive Board.

Official directive, Article 12:  
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/2106-bogazici-universitesi-saglik-kultur-ve-spor-d-20260521-143342.pdf

The same directive assigns the SKS Coordination Branch responsibilities including annual budgeting, procurement transactions and examination of accounting records.

### Operational inference — do not overstate

The current contract semantics may be distributed across more than one institutional owner:

```text
Food Services Branch
    -> technical specification / operational acceptance / contractor control

SKS Coordination / financial process
    -> procurement / budget / accounting records

TEMAŞ operations
    -> production execution / internal planning records
```

This is a routing hypothesis. PMR must identify who actually holds daily quantity, progress-payment and acceptance records.

---

# 5. Procurement history proves document instability — not specific current clauses

## CSEM-06 — The first 2026–2027 procedure was cancelled because specification changes were required

`PUBLIC SOURCE / C4`

Cancelled predecessor:

- İKN `2025/1335958`;
- same headline quantities and six-campus scope;
- cancelled on **07.10.2025**;
- stated reason: objections to tender documents were evaluated, changes to specification provisions were deemed necessary, but amendment was not possible at that stage.

Source:  
https://ekapveri.com/ihale/ekap-2025-1335958/

The successful procedure `2025/1727143` was then advertised on **17.10.2025** and its public record also indicates that a correction notice existed.

### Why this matters

The procurement lineage is not a stable single document.

Agent rule:

```text
NEVER:
clause from 2025/1335958 -> assume current 2025/1727143 clause

ALWAYS:
attach IKN + document version + publication date to every procurement-derived statement
```

The cancellation itself is useful provenance evidence, but it makes cancelled tender documents **less**, not more, suitable as current-contract proof.

---

# 6. The missing quantity state machine

Current public evidence does not resolve the following state transitions.

```text
expected demand
    ↓
university forecast / request?          UNKNOWN
    ↓
contractor plan?                        UNKNOWN
    ↓
approved / called-off quantity?         UNKNOWN
    ↓
produced quantity                       UNKNOWN DATA ACCESS
    ↓
delivered / campus-allocation quantity UNKNOWN DATA ACCESS
    ↓
turnstile / served count                PLAUSIBLE SYSTEM SIGNAL; ACCESS UNKNOWN
    ↓
contract-accepted quantity              CRITICAL UNKNOWN
    ↓
progress-payment (hakediş) quantity     CRITICAL UNKNOWN
    ↓
unserved surplus / waste                PARTIALLY REPORTED; GRANULARITY UNKNOWN
```

The product should not define its target variable until the arrows are verified.

---

# 7. Contract-semantics questions ranked by information value

## P0 — one interview / artifact can change the whole product thesis

1. **Which quantity is multiplied by the contract unit price in monthly hakediş?**
2. What system/report is the source of that quantity?
3. Who approves/signs that quantity?
4. Is a daily expected/requested meal count communicated to TEMAŞ? By whom and at what deadline?
5. Can that count be revised? What is the last operationally useful revision time?
6. Is excess produced but unserved food payable, partly payable or entirely contractor risk?
7. What happens when service demand exceeds the planned quantity?

## P1 — required to design a pilot

8. Are student meal, staff meal and breakfast line items settled independently?
9. Does campus allocation affect payment or only operations?
10. Are BUCard/QR counts reconciled against contractor/service records?
11. Are manual corrections/refunds/guest meals included in the acceptance count?
12. Are minimum guaranteed quantities or tolerance bands defined?
13. Are shortages, menu substitution or late service subject to deductions/penalties?
14. Which quantity is available **before** the production freeze point?

---

# 8. Minimum contract-data request

Do not request full personal transaction logs. Ask for the smallest aggregate fields that identify the decision and settlement mechanics.

For a limited historical window:

```text
DATE
MEAL_CLASS                   # student / staff / breakfast
CAMPUS
SERVICE_REGIME
INITIAL_REQUEST_QTY          # if it exists
FINAL_REQUEST_QTY            # if revisions exist
REQUEST_FREEZE_TIMESTAMP
PRODUCED_QTY                 # if recorded
DELIVERED_QTY                # if recorded
AGGREGATE_ENTRY_COUNT        # privacy-safe BUCard/QR aggregate if available
CONTRACT_ACCEPTED_QTY
HAKEDIS_QTY
UNSERVED_SURPLUS_QTY
SHORTAGE_EVENT
MANUAL_ADJUSTMENT_QTY
ADJUSTMENT_REASON_CODE
```

### Data dictionary requirements

For every field record:

- unit;
- event-time vs reporting-period semantics;
- source system;
- responsible owner;
- correction policy;
- whether values can be backdated;
- whether one event can appear in multiple fields;
- whether the field is contractual or operational only.

---

# 9. Sector precedents define candidate mechanisms — not Boğaziçi facts

Other Turkish university contracts documented in the related precedent pack show mechanisms such as:

- contractor setting production using previous-period demand;
- actual diner/smart-card counts feeding progress payment;
- excess production risk remaining with contractor;
- shortage recovery/penalty exposure;
- historical preference data changing production mix.

These mechanisms make the research question commercially credible, but **none may be attributed to Boğaziçi until current C1 evidence exists**.

Related pack:  
[`TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md`](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md)

---

# 10. Decision model after semantics are verified

Do not optimize `MAE` as the product objective by default.

A useful decision layer needs:

```text
P(D | context)            # demand distribution, not only point forecast
q                         # recommended production/allocation quantity
C_over(q, D)              # excess / waste / non-payable production cost
C_under(q, D)             # shortage / substitution / service-failure cost
contract_constraints      # min/max/tolerance/settlement semantics
operational_constraints   # batch, capacity, campus allocation, freeze time
human_override            # required decision gate
```

Then choose `q` against the actual operational/contract objective.

### Academic design references

- Birişçi & McGarvey (2021), *Socio-Economic Planning Sciences*, study institutional food-service production under forecast uncertainty and explicitly model the frontier between food waste and demand shortfall.  
  https://consensus.app/papers/costversus-environmentallyoptimal-production-in-birişçi-mcgarvey/38f25b4bfef85d84a6b78abece26d125/?utm_source=chatgpt
- Malefors et al. (2020), *Sustainable Production and Consumption*, compare simple and complex attendance forecasting methods in public catering and still require safety margins because demand can exceed forecasts.  
  https://consensus.app/papers/potential-for-using-guest-attendance-forecasting-in-malefors-strid/91eb65a9c8e65f39b6a33ffad04a2d86/?utm_source=chatgpt

### Engineering implication

Mandatory benchmark ladder:

1. current operator heuristic;
2. same-weekday / rolling baseline;
3. contextual point forecast;
4. calibrated predictive distribution if data support it;
5. decision policy using asymmetric costs and service guardrail.

A more accurate model that worsens shortage or contract economics must lose.

---

# 11. Pilot acceptance contract

Before any impact claim, define:

## Primary physical outcome

```text
normalized_excess_or_waste
```

with a precise measurement boundary.

## Service guardrails

```text
shortage_events
sellout_minutes
substitution_events
service_delay
operator_override_rate
```

## Decision metrics

```text
recommended_q
operator_q
actual_demand_proxy
absolute_error
signed_error
excess_portions
shortage_portions
```

## Contract/economic metrics — only after semantics verified

```text
accepted_qty
hakediş_qty
verified unit price by line item
verified deduction/penalty
verified non-payable excess
```

No money-saving claim should precede this verification.

---

# 12. Safe current conclusion

A strong public-source statement is:

> Boğaziçi's current 2026–2027 dining procurement is a 3.13-million-unit, six-campus, unit-price service contract with a 10,000-meal/day procurement design requirement and formal university oversight of contractor compliance. Public documents do not yet reveal which realized daily quantity drives progress payment or how production quantities are revised. The team is therefore treating contract/payment semantics as a P0 validation question before assigning an economic value to forecasting improvements.

This is stronger and more defensible than claiming that food-waste savings equal procurement savings.

---

# 13. Sources

## Current Boğaziçi procurement

- Successful tender `2025/1727143`:  
  https://www.ihaledetay.com/2025-1727143  
  https://ekapveri.com/ihale/ekap-2025-1727143/
- Cancelled predecessor `2025/1335958`:  
  https://ekapveri.com/ihale/ekap-2025-1335958/
- Dining BUCard/QR support semantics:  
  https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
- SKS current duties/authority directive:  
  https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/2106-bogazici-universitesi-saglik-kultur-ve-spor-d-20260521-143342.pdf

## Academic design references

- Birişçi E, McGarvey R. (2021). *Cost-versus environmentally-optimal production in institutional food service operations.* Socio-Economic Planning Sciences.  
  https://consensus.app/papers/costversus-environmentallyoptimal-production-in-birişçi-mcgarvey/38f25b4bfef85d84a6b78abece26d125/?utm_source=chatgpt
- Malefors C, Strid I, Hansson P, Eriksson M. (2020). *Potential for using guest attendance forecasting in Swedish public catering to reduce overcatering.* Sustainable Production and Consumption 25:162–172.  
  https://consensus.app/papers/potential-for-using-guest-attendance-forecasting-in-malefors-strid/91eb65a9c8e65f39b6a33ffad04a2d86/?utm_source=chatgpt

---

# 14. Bottom line for agents

```text
DO NOT ask first: Which ML model predicts meals best?

ASK FIRST:
What exact quantity is decided?
Who decides it?
When does it freeze?
Which data exist before freeze?
Which realized quantity settles the contract?
Who bears excess and shortage?

ONLY THEN:
forecast -> decision policy -> human approval -> prospective verification
```
