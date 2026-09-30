# Türkiye University Dining Contract Decision Precedents

**Research date:** 2026-10-01  
**Purpose:** Extract public procurement/KİK precedents showing who bears demand-forecast risk, how daily meal quantity can be set, what operational signals are used, and how payment may be linked to actual consumption in university dining contracts.  
**Status:** Secondary public-source research only. **NOT legal advice. NOT evidence that Boğaziçi uses the same clauses. NOT PMR.**

Related packs:

- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md`](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md)

---

# 0. Why this matters

Desk research previously established that Turkish public universities procure explicit meal quantities through institutional food-service contracts. The missing question was whether `forecasting daily demand` is merely a product idea or can be a real contractual operating responsibility.

The KİK decisions below materially strengthen that point.

They show real university tender documents where:

- daily meal counts are allowed to vary;
- contractors are expected to estimate production from historical demand;
- underproduction can trigger operational/contract consequences;
- overproduction can be left at contractor risk;
- actual diners can be counted by smart-card or similar systems;
- monthly payment can be tied to actual consumption rather than produced quantity;
- universities can reserve the right to introduce reservation systems;
- historical preferences can alter the production mix of menu alternatives.

This is **not** proof that every university uses these mechanics. It is proof that the current product thesis maps to real contract structures already used in the sector.

---

# 1. Uşak University — historical demand forecast + smart-card settlement

## PRECEDENT-U01

**Official source:** Kamu İhale Kurulu decision 2023/UH.II-1466, dated 29.11.2023.  
**Tender:** 2023/1031004 — “Mamul Yemek Alımı, Dağıtımı ve Sonrası Hizmetleri Alımı”  
**Authority:** Uşak University Health, Culture and Sports Department.

Official KİK decision:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=a2f80a616e9c557c0277ada12419f7fe4b56a43f838d580d271ac80b78fc28d7&KararMetni=463e03f9e3aad6ea48bee9aff80678331453bbe55b4fbbbde6250ac09a80c38d

### Contract mechanics reproduced in the KİK decision

The technical specification stated that:

1. **Daily meal counts are determined by the contractor using the previous week's corresponding days**, while education term, break and summer periods are evaluated within their own regimes.
2. If food is insufficient during service, an equivalent meal must be produced under the Control Organization's knowledge so service is not interrupted.
3. The university may move to a **reservation system** for meal counts if needed.
4. Meal service uses an **intelligent/smart card system** across listed service points.
5. If the card system fails, total students/staff eating are recorded daily by the Control Organization through a written record.
6. Contractor progress payments / hakediş are made monthly by summing the **daily number of students and staff who actually ate**.
7. The university is not responsible for excess food left after lunch/dinner.
8. The contractor cannot request payment for meals it produced but had left over.
9. The bid quantity was 800,000 normal meal units; the KİK reasoning explicitly treated this as an estimate because actual user counts naturally vary.

### Decision-system interpretation

This is almost a direct formalization of the KREATE decision problem:

```text
historical demand / regime
        ↓
contractor chooses daily production quantity
        ↓
actual demand measured by card / controlled fallback count
        ↓
shortage => contractor must recover service
excess   => contractor bears leftover risk
        ↓
monthly payment based on actual diners
```

### Product implication

In this contract archetype, forecast quality is potentially a **contractor P&L and operational-risk variable**, not merely a sustainability KPI.

A useful recommendation would need to minimize something like:

```text
excess production cost
+ shortage recovery / service-risk cost
+ contract penalty risk
```

while payment is driven by actual diners.

### Important caveat

This was Uşak University's 2023 procurement for a 2024 service period. It is a sector precedent, not current Boğaziçi contract evidence.

---

# 2. Kırıkkale University — current 2026 precedent with forecast risk on contractor

## PRECEDENT-K01

**Official source:** KİK decision 2026/UH.I-2269, dated 26.08.2026.  
**Tender:** 2026/1174924 — “Malzemeli Yemek Hizmeti”  
**Authority:** Kırıkkale University Rectorate / SKS context.  
**Listed quantity:** 350,000 meal units.

Official KİK decision:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

### Contract mechanics reproduced in the decision

The technical specification included the following operating logic:

1. **Daily meal counts are determined by the contractor considering previous meal counts.**
2. If the contractor fails to prepare enough food, contractual penalty action can apply.
3. Progress payments are based on the **number of meals actually eaten**.
4. The administration is not responsible for excess food.
5. Leftover food may not simply be reused in another meal.
6. Bidders are expected to account for changes in diner counts caused by the **academic calendar and the menu**.
7. The specification says the contractor determines preparation quantity based on the **day's popularity**.
8. The KİK decision concludes that daily consumption can vary according to the administration's actual need and points to payment based on the quantity of meals purchased/consumed.

### Decision-system interpretation

```text
previous demand
+ academic calendar
+ menu / day popularity
        ↓
contractor forecasts daily quantity
        ↓
actual consumption
        ↓
hakediş based on actual consumed/purchased quantity

underproduce → penalty / service risk
overproduce  → administration does not absorb excess
```

### Product implication

This provides unusually strong public-source support for the **asymmetric prediction-loss thesis**:

- overforecast can cost the contractor;
- underforecast can create service failure and penalty risk;
- therefore MAE alone is not the business objective.

The product should support an operator-specific asymmetric objective or guardrail rather than a generic prediction score.

### Strong PMR question derived from Kırıkkale

> In your current contract, when demand differs from production, who financially absorbs the excess and what happens operationally/contractually when meals run out?

That question should be asked at Boğaziçi and contractor interviews even if Boğaziçi's clauses differ.

---

# 3. Sakarya University — historical preference data may change production mix

## PRECEDENT-S01

**Official source:** KİK decision 2026/UH.I-2163, dated 19.08.2026.  
**Tender:** 2026/1002808 — “Sakarya Üniversitesi Servise Hazır Yemek Hizmeti Alım İşi”.

Official KİK decision:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=992c5efa9fa05688b41bc2a9bf9e09c0927c462208d40fa9af7f78f7e2807899

### Demand scale

The tender material described an administration average daily requirement using a total of **1,250,000 meals over 354 days**, approximately 3.5k meals/day for capacity-planning purposes.

Treat this as the tender's calculation basis, not a measured day-by-day demand series.

### Menu-production decision reproduced in the decision

The specification's default production policy for the main-course group was:

- 3% vegetarian main course;
- remaining selectable main courses initially produced 50/50;
- but **if the contractor and university Control Organization jointly decide, using historical-period data on student/staff preference, the preferred selected main course can be produced in a larger quantity than the other**.

Menus are prepared by the Menu Planning Commission and communicated monthly, with controlled mechanisms for menu changes.

### Decision-system interpretation

Sakarya's contract shows that forecasting can operate at more than one level:

```text
Level A — total diners
Level B — demand split among menu alternatives
```

The second level is explicitly adjustable using historical preference data.

### Product implication

The system architecture should distinguish:

```text
total_quantity_forecast
menu_mix_forecast
campus_allocation_forecast
```

rather than treating a meal service as one scalar demand number.

A model may create value even where total production is constrained if it improves **mix allocation** between alternative dishes.

### Important caveat

The public KİK text establishes the contract clause, not that Sakarya currently uses an ML system or that historical data are digitally accessible.

---

# 4. Marmara University — contract line-item segmentation is explicit

## PRECEDENT-M01

Marmara's 2026 transported meal tender (İKN 2026/603458) contains explicit separate unit-price bid items for:

- 220,000 standard transported four-course meals;
- 19,000 vegetarian meals;
- 500 gluten-free meals;
- 500 vegan meals.

Official KİK decision:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=e53bf685cc2908fe76abbf541eec9f9bd19b36dabe0cb1efb72281d2bc429276

### Product implication

Some demand classes are not just analytics features; they can be **contract/bid line items**.

Therefore the data model should retain `meal_class` / `dietary_class` and must not aggregate everything into one generic meal count before contract interpretation.

---

# 5. Cross-precedent patterns

## CP-01 — Daily production can be a forecasting responsibility

Uşak and Kırıkkale public KİK decisions reproduce specifications where the **contractor determines daily production using historical demand signals**.

This materially changes the candidate user map:

- university/SKS may be buyer, contract owner and control authority;
- **contractor operations may be the direct daily user** of the recommendation.

The product should not assume the university's Food Services Branch is always the keyboard-level user.

---

## CP-02 — Excess and shortage are asymmetric risks

The sampled contract precedents show mechanics where:

- excess output may be unpaid / administration bears no responsibility;
- shortages require rapid replacement and can create penalty/service risk.

This validates the need for a decision objective such as:

```text
ExpectedDecisionLoss(q) =
    C_excess × E[max(q - D, 0)]
  + C_shortage × E[max(D - q, 0)]
  + service_failure_penalty(q)
```

But `C_excess` and `C_shortage` must come from each contract/operator, not from generic assumptions.

---

## CP-03 — Actual consumption can be the settlement signal

Uşak provides the clearest public precedent:

- smart-card service measurement;
- controlled daily fallback counts;
- monthly progress payment calculated from daily actual diner totals.

Kırıkkale similarly links progress payment to actually eaten/purchased meals.

### Product implication

Where this contract model applies, the following table is especially valuable:

```text
FORECAST_QTY
PRODUCED_QTY
ACTUAL_CARD_OR_VALIDATED_DINERS
EXCESS_QTY
SHORTAGE_EVENT
CONTRACT_SETTLED_QTY
```

This provides both model evaluation and economic reconciliation without needing personally identifiable diner data.

---

## CP-04 — Academic calendar and menu are contract-recognized demand drivers

Kırıkkale explicitly says bidders should account for changes based on academic calendar and menu. Uşak separates education, break and summer periods when using historical weeks.

This makes calendar/service-regime features more than academic-literature ideas: they appear directly in procurement operating logic.

### CS1 implication

A minimum serious baseline should be:

```text
same_weekday_recent_history
+ academic/service regime
+ menu context
```

before complex models are tested.

---

## CP-05 — Reservation is a plausible institutional pathway

Uşak's tender reserved the administration's right to introduce a meal reservation system.

This matters because the product should support more than passive prediction. Depending on PMR, future product options could include:

```text
passive forecast
→ forecast + operator adjustment
→ soft intent/preference signal
→ reservation / pre-commit signal
```

However, reservation should not be forced into the current product without evidence that user friction and operations justify it.

---

## CP-06 — Menu-mix optimization may be a separate wedge

Sakarya's clause explicitly allows historical preference data to change production proportions among selected main courses.

Possible decision hierarchy:

```text
1. total meal quantity
2. campus/channel allocation
3. menu-choice mix
4. batch timing / replenishment
```

PMR should determine where the highest cost/uncertainty actually sits at Boğaziçi.

---

# 6. Stronger candidate buyer/user map

After these precedents, the likely role map becomes:

| Role | Possible responsibility | Evidence status |
| --- | --- | --- |
| University SKS / Food Services | contract owner, menu/control, service policy | repeated public pattern |
| University Control Organization | validates service, may co-decide production/menu mix | explicit in Uşak/Sakarya/Kırıkkale-type documents |
| Contractor operations / kitchen manager | daily demand estimate and production quantity | explicit in Uşak + Kırıkkale precedents |
| Data-system owner | smart card / turnstile / reservation / transaction export | explicit smart-card precedent at Uşak; Boğaziçi signals separately documented |
| Procurement/finance | hakediş / accepted quantity | explicit settlement relevance in Uşak/Kırıkkale |
| Student/staff diner | demand source / service recipient | obvious beneficiary, not automatically buyer |

### Commercial implication

The strongest initial commercial hypothesis may be **B2B2B-style operational value shared between university and contractor**, not purely university sustainability software.

Do not promote this to the application as validated buyer structure until interviews show who pays, who saves, and who can authorize software.

---

# 7. PMR script upgraded by contract precedents

## Contractor operations

1. Who forecasts tomorrow's breakfast/lunch/dinner quantity?
2. What exact data do they inspect?
3. Is last week / same weekday currently used?
4. How are academic breaks and events handled?
5. What happens if 200 extra portions remain?
6. Who pays for those 200 portions?
7. What happens if 200 portions are missing?
8. Are there penalty, emergency-production or service-level consequences?
9. Does payment use produced, delivered, card-swiped, served or approved quantity?
10. Do you forecast total quantity and menu-choice mix separately?
11. At what time is the final production decision irreversible?
12. Could a recommended range with uncertainty be more useful than a single number?

## University contract/control owner

1. Does the contractor choose daily quantity or do you send it?
2. What is the legal/contract source for the final quantity?
3. What constitutes accepted service for hakediş?
4. Does an existing card/turnstile/POS system produce the settlement count?
5. Can the contract quantity change during the year?
6. Who absorbs excess-food cost?
7. Who bears shortage risk?
8. Is there an operator override / approval workflow today?
9. Could forecast evidence be used contractually, or only operationally?
10. Would the university value waste reduction if it does not reduce its own invoice?

---

# 8. CS1 technical requirements created by the precedents

## 8.1 Predict a distribution, not only a point

When shortage and excess costs are asymmetric, point MAE is insufficient.

Output should support:

```text
p10
p50
p90
recommended_quantity
expected_excess
shortage_risk
```

Only call intervals calibrated when held-out calibration has been demonstrated.

## 8.2 Baseline must include current heuristic

Because contracts explicitly describe heuristics such as `previous week's corresponding day`, CS1 should implement that exact class of baseline.

Candidate baselines:

```text
B0 previous same weekday
B1 rolling same-weekday median
B2 regime-aware previous same weekday
B3 menu-aware historical neighbor
B4 operator-entered forecast
```

Any advanced model should beat the relevant heuristic on **decision loss and service guardrails**, not only MAE.

## 8.3 Settlement-aware evaluation

Where actual diners drive payment, evaluate:

```text
forecast error
excess portions
shortage probability
emergency top-up frequency
settled quantity
estimated variable cost exposure  # only if contract data support it
```

Do not convert predictions into TL savings until contract-specific unit economics are verified.

## 8.4 Separate total demand from mix demand

Sakarya-type rules mean the model can have multiple heads:

```text
total_demand_head
menu_mix_head
campus_allocation_head
```

Build only the heads justified by available data and operator decisions.

---

# 9. What this changes for KREATE narrative

## Before

> Universities have uncertain food demand, so AI could forecast it and reduce waste.

## Stronger evidence-safe narrative

> `PUBLIC SOURCE` Turkish university food-service contracts include real operational structures where daily meal quantities can be estimated from prior demand, actual diners can determine contractor settlement, excess production may remain at contractor risk, and underproduction can create service consequences. Other university specifications explicitly allow historical preference data to alter meal-production mix. `HYPOTHESIS` The team is testing whether Boğaziçi has a comparable decision point where existing aggregate signals can improve production or allocation decisions without increasing shortage risk.

This is much stronger than generic climate-tech language because it identifies a **real repeated decision mechanism** without pretending Boğaziçi's contract has already been verified to use it.

---

# 10. Evidence firewall

Do **not** claim from these precedents that:

- Boğaziçi pays only for card-swiped meals;
- TEMAŞ bears Boğaziçi's excess food cost;
- Boğaziçi's current contract makes TEMAŞ forecast quantity;
- Boğaziçi can change quantities daily;
- every university uses smart cards for settlement;
- historical-data forecasting is universally required;
- a forecast model will necessarily lower university expenditure;
- contractor savings automatically create university savings.

These remain PMR/contract-verification questions.

---

# 11. Sources

## Uşak University

KİK 2023/UH.II-1466:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=a2f80a616e9c557c0277ada12419f7fe4b56a43f838d580d271ac80b78fc28d7&KararMetni=463e03f9e3aad6ea48bee9aff80678331453bbe55b4fbbbde6250ac09a80c38d

## Kırıkkale University

KİK 2026/UH.I-2269:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

## Sakarya University

KİK 2026/UH.I-2163:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=992c5efa9fa05688b41bc2a9bf9e09c0927c462208d40fa9af7f78f7e2807899

## Marmara University

KİK 2026/UH.II-1601:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=e53bf685cc2908fe76abbf541eec9f9bd19b36dabe0cb1efb72281d2bc429276

---

# 12. Bottom line

This contract research is the strongest secondary evidence so far for the current product thesis.

The sector contains real documented workflows where:

```text
historical demand
→ production decision by operator
→ actual consumption measurement
→ asymmetric excess/shortage risk
→ contract settlement
```

and separately:

```text
historical preference data
→ production-mix adjustment
```

The next decisive Boğaziçi evidence is therefore extremely specific:

> **Who forecasts quantity under the current TEMAŞ contract, what historical/current signal is used, when is the quantity frozen, how is actual service counted for hakediş, and who absorbs excess versus shortage cost?**

If Boğaziçi resembles the Uşak/Kırıkkale archetype, the solution has a direct operational/economic user. If it does not, the team should pivot the intervention point rather than forcing the forecast thesis.