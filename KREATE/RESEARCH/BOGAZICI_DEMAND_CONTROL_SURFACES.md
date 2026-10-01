# Boğaziçi Dining Demand Control Surfaces — Reservation, Service Regime & Decision Timing

**Research date:** 2026-10-01  
**Status:** Secondary/public-source research. This file sharpens PMR and product architecture; it does **not** prove current term-time production rules, contractor economics or data access.

## Executive conclusion

Boğaziçi already has evidence of a richer demand-control system than a simple `forecast tomorrow's meal count` problem.

Public university sources show that the institution has used explicit meal reservations to:

- collect next-day meal intent;
- allow cancellation before service;
- impose an economic consequence on uncancelled no-shows in at least one special-service regime;
- switch service modality based on reservation count;
- support packaged delivery rather than dining-hall service in low-demand/special regimes;
- combine meal access with BUCard / BUCampus QR infrastructure.

The product question should therefore move from:

> How accurately can we predict demand?

into:

> **Which decision surface is still uncertain after using the cheapest existing signal, and what action can the operator change before its freeze point?**

A useful Boğaziçi dining decision engine may need to choose among quantity, service mode, campus allocation, menu mix, batch/replenishment policy and reservation/intent policy — not only output one demand scalar.

---

# BDC-01 — Boğaziçi has used next-day reservation as an operational input

`PUBLIC SOURCE`

For the 2026 Kurban Bayramı service plan at Kilyos, Boğaziçi required breakfast/lunch/dinner reservations through `kart.boun.edu.tr` by **18:00 on the previous day**.

The flow used existing university identity/card infrastructure:

```text
kart.boun.edu.tr
→ Yemekhane Form / Yemek Talep Formu
→ create meal request
→ list/delete requests
```

Primary source:
https://yemekhane.bogazici.edu.tr/node/493

### What this establishes

- An explicit pre-service demand/intent signal has been operationally deployed at Boğaziçi.
- Users can create and cancel a meal request.
- A one-day-ahead decision horizon is operationally possible in at least one special-service context.

### What remains unknown

- whether the reservation count changed the kitchen production quantity;
- who saw the count and at what exact time;
- whether TEMAŞ or the university used it;
- whether normal academic-term volume would make this workflow impractical;
- whether reservations were campus/meal/menu-specific in the production data layer.

---

# BDC-02 — Boğaziçi has used an explicit no-show commitment rule

`PUBLIC SOURCE`

The same 2026 announcement states that a reservation not cancelled through the web flow, but not collected by the student, would be treated as a consumed meal for **balance deduction**.

Primary source:
https://yemekhane.bogazici.edu.tr/node/493

This is important because the institution did not treat reservation as a costless survey response. It attached a user-facing consequence to uncancelled no-shows.

### Product implication

Reservation reliability is partly a **mechanism-design / incentive** problem.

A future data model should distinguish:

```text
reserved
cancelled_before_cutoff
uncancelled_no_show
walk_in_or_unreserved
served
```

Do not model `reserved == served`.

### Claim boundary

The public source does **not** establish:

- the size of the balance deduction;
- whether the contractor was paid for a no-show meal;
- whether production was reduced for cancellations;
- whether the rule materially reduced no-show behavior;
- whether this rule applies in normal term-time service.

---

# BDC-03 — Reservation count has directly changed Boğaziçi's service mode

`PUBLIC SOURCE — high strategic value`

During the January–February 2024 inter-semester period, Boğaziçi used reservation for selected meals across North, South, Anadolu Hisarı, Kandilli and Kilyos.

The university explicitly stated:

> when reservation counts were below **15**, meals would be offered as **packaged service**.

Primary source:
https://yemekhane.bogazici.edu.tr/ara-tatil-yemek-hizmeti-hakkinda

This is stronger than evidence that reservations merely existed. It shows a public, explicit mapping from **demand signal → operational action**.

```text
reservation count
        ↓
if low enough
        ↓
switch service regime
        ↓
packaged delivery / reception delivery in selected campuses
```

### Product implication

BOUNCAMPUS should support **policy decisions** in addition to point forecasts.

Possible decision objects include:

```text
production_quantity
dining_hall_open_vs_package
service_channel
campus_allocation
batch_size
menu_mix
reserve_capacity
```

A recommendation such as `use package mode for this campus/meal` may create more operational value than improving MAE by another small amount.

### Claim boundary

The value `15` is a historical/special-period rule, **not a current universal Boğaziçi threshold**. It must never be hard-coded as policy without owner validation.

---

# BDC-04 — Boğaziçi has multiple service channels and regimes

Public dining pages show materially different service modes over time:

- normal dining-hall breakfast/lunch/dinner;
- package lunch/dinner products;
- kiosk package service;
- summer package service restricted to weekday lunch for a defined period;
- holiday Kilyos reservation + packaged dorm delivery;
- low-reservation package conversion in the 2024 inter-semester regime.

Sources:

- Current dining/menu surface: https://yemekhane.bogazici.edu.tr/
- Summer package service 2026: https://yemekhane.bogazici.edu.tr/yaz-donemi-paket-yemek-hizmeti-hakkinda
- Holiday reservation flow: https://yemekhane.bogazici.edu.tr/node/493
- 2024 inter-semester reservation regime: https://yemekhane.bogazici.edu.tr/ara-tatil-yemek-hizmeti-hakkinda

### Architecture implication

Do not train or evaluate one model across mixed service regimes without a regime field.

Minimum categorical context:

```text
academic_state
service_regime
dining_hall_or_package
campus
meal_period
weekday_or_weekend
special_period
reservation_required
```

A structural regime change can matter more than weather or a complex model feature.

---

# BDC-05 — Boğaziçi already has digitally observable service events

The current FAQ states that users can enter dining service using BUCard, and users without a physical card can use **BUCampus to scan the QR code at the turnstile**. The FAQ asks users reporting charging errors to identify the exact date, time, campus and turnstile.

Primary source:
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

The 2024 personnel payment change also states that detailed meal usage can be viewed through BUCard / BUCampus and that eligible personnel meal charges are aggregated into later payroll deduction.

Primary source:
https://yemekhane.bogazici.edu.tr/node/225

### What this supports

There are operational digital events with at least some combination of:

- time;
- campus/turnstile context;
- meal charge/access;
- identity-linked accounting in the source system.

### What this does not support

- team access to row-level or aggregate history;
- clean mapping from turnstile event to meal actually consumed;
- permission to use personally identifiable data;
- availability before production freeze.

### Data-design rule

The desired pilot interface should request **privacy-safe aggregate counts**, not user histories:

```text
date × campus × meal_period × service_channel → validated_served_count
```

---

# BDC-06 — Menu preference is already an explicit digital signal

Boğaziçi's 2024 menu survey used BUCampus institutional login, limited users to one vote, and used majority preference to choose the following week's Wednesday lunch menu.

Primary source:
https://yemekhane.bogazici.edu.tr/menu-anketi

### Product implication

The institution has already demonstrated a pattern of:

```text
collect explicit user intent/preferences
→ aggregate signal
→ alter a future food-service decision
```

Therefore the strongest product thesis is not `introduce digital feedback`. It is **join existing intent, historical service and operational constraints into a reusable decision/verification layer**.

PMR must determine whether menu-vote counts have any predictive relationship to actual uptake and whether those data are retained.

---

# BDC-07 — Formal control organization makes the workflow multi-role

Boğaziçi's current university commission/control page lists a formal **Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı**.

Primary source:
https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

Current listed principal members include:

- Ayhan Soylu — chair;
- Barış Pancar;
- Aygül Demir;
- Ahmed Musab Taş;
- Mustafa Tunç.

### Product implication

Do not model the workflow as only `SKS buyer ↔ contractor kitchen`.

There may be separate roles for:

```text
contract owner
production operator
control/acceptance organization
data owner
waste measurement owner
beneficiary
```

The decision record should preserve who **recommended**, who **approved**, who **executed**, and who **verified** an outcome.

### PMR routing implication

Add the Control Organization to the stakeholder map specifically for:

- production/distribution acceptance;
- service compliance;
- shortage handling;
- quantity/service-mode change authority;
- what operational records are trusted for contractor control.

---

# BDC-08 — Academic literature supports two different architectures depending on booking availability

Two peer-reviewed university dining studies illustrate why the product must not assume one technical architecture.

## Reservation + no-show architecture

Faezirad, Pooya & Naji-Azimi (2021), *Waste Management & Research*, explicitly model meal booking plus **presence/absence (show/no-show)** and optimize under both waste and shortage cost.

Paper:
https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/?utm_source=chatgpt

Use as a design reference for:

```text
reservation count
→ expected no-shows
→ expected unreserved/other uncertainty
→ cost-aware production decision
```

Do not import its reported impact percentage as a Boğaziçi estimate.

## No-prebooking architecture

Mehmet Acı (2023), *Technical Gazette*, studies a university refectory **without pre-booking**, using calendar effects and meal ingredients to forecast short-window demand.

Paper:
https://consensus.app/papers/demand-forecasting-for-food-production-using-machine-acı/53fc30fe33fe579f8949e9a42a0ecc14/?utm_source=chatgpt

Use as a design reference for passive-demand forecasting when explicit intent is unavailable.

### Decision rule

The first technical question is not `which ML model?`.

It is:

```text
Is there a reliable explicit intent signal before freeze?

YES → estimate residual uncertainty around intent.
NO  → forecast total demand from historical/context signals.
```

---

# 1. Updated Boğaziçi control-surface map

| Control surface | Public evidence | Current certainty | P0 validation question |
| --- | --- | --- | --- |
| Reservation / intent | 2024 + 2026 special-period workflows | Proven capability, normal-term use unknown | Is reservation used or technically available in normal service? |
| Cancellation | Users can delete requests; 2026 uncancelled no-show rule | Proven in special regime | What is cancellation cutoff and observed rate? |
| Quantity | Large formal meal procurement; sector precedents | Decision owner unknown | Who sets each campus/meal production quantity and when? |
| Service mode | Historical `<15 reservations → package` rule | Proven historical special-period rule | Who may switch dining-hall/package mode today? |
| Campus allocation | Six-campus procurement + centralized production research | Plausible control point | When is campus allocation frozen and can it move? |
| Package vs hall channel | Multiple public package/hall regimes | Proven channel heterogeneity | Are channel quantities planned separately? |
| Menu selection | BUCampus weekly menu survey | Proven user preference input | Are vote totals retained and used beyond selection? |
| Menu mix quantity | Vegan/vegetarian alternatives and sector precedents | Unknown at Boğaziçi | Are alternatives produced to fixed or adaptive ratios? |
| Batch/replenishment | No public Boğaziçi rule found | UNKNOWN | Is cooking staged and can later batches respond to demand? |
| User commitment rule | 2026 no-show balance deduction | Proven special regime | Did this materially improve show rate / planning reliability? |

---

# 2. Product-selection logic for agents

Before implementing a model, identify the strongest available signal and reachable action.

```text
A. Explicit reservation high coverage + reliable
   → reservation-first planning
   → simple safety factor / uncertainty band may be enough

B. Reservation exists but has material no-show / walk-in demand
   → hybrid intent + residual uncertainty model

C. Reservation creates too much friction or is not used
   → passive forecasting from historical/menu/calendar context

D. Quantity is hard to change but service mode/channel is flexible
   → optimize service regime instead of quantity

E. Total quantity is fixed but menu mix is flexible
   → optimize mix, not attendance
```

No agent should select A–E without evidence.

---

# 3. P0 PMR questions generated by this pack

## Food Services / Control Organization

1. In the 2024 inter-semester process, what operational reason produced the `<15 → package` rule?
2. Who was authorized to make that service-mode decision?
3. Is any equivalent threshold/rule used today?
4. In the 2026 Kilyos holiday process, who received the reservation count at 18:00?
5. Did that count directly become a production request, or was a buffer added?
6. How many reservations were cancelled before cutoff?
7. How many uncancelled reservations were not collected?
8. How many meals were requested without a prior reservation?
9. Did the balance-deduction rule change no-show behavior?
10. Which parts of the reservation flow already exist in the current BUCard platform and could be activated without new software?

## TEMAŞ / kitchen operator

1. If you received a reservation count of `R`, how would you turn it into produced quantity `Q`?
2. What uncertainty/buffer is normally added?
3. Which uncertainty is larger: no-shows, walk-ins, menu mix, campus allocation, or timing?
4. Can you change service mode, batch size or campus allocation after the initial quantity decision?
5. What is the latest useful timestamp for an updated signal?

## BİD / BUCard

Request only aggregate schema and metadata first:

```text
reservation_created_count
reservation_cancelled_count
reservation_active_at_cutoff
validated_turnstile_or_qr_count
campus
meal_period
service_date
recorded_at
```

Ask whether historical special-period data survive and whether an anonymized aggregate export can be produced.

---

# 4. Pilot ladder

A low-risk pilot can be staged before any complex ML.

## Pilot 0 — retrospective reconciliation

For one historical reservation period:

```text
active reservations at cutoff
vs
actual validated service count
```

Measure:

- show rate;
- cancellation rate;
- residual demand error;
- whether errors vary by campus/meal/day.

## Pilot 1 — simple reservation correction

Compare:

```text
Q1 = reservation count
Q2 = reservation count × historical show factor + simple walk-in buffer
```

Evaluate against actual served quantity and shortage guardrails.

## Pilot 2 — contextual residual model

Only if Pilot 1 leaves material predictable error, test calendar/menu/campus features.

## Pilot 3 — decision policy

Test whether the prediction changes a real operator action:

- quantity;
- batch;
- campus allocation;
- package/hall service mode.

A better prediction with no changed decision is not a successful product pilot.

---

# 5. New falsification conditions

The reservation/decision-intelligence wedge weakens materially if:

- historical reservation data no longer exist;
- normal-term reservation is rejected because friction/exclusion costs dominate;
- reservation already predicts realized service closely enough that no meaningful residual decision remains;
- kitchen quantities are fixed before any usable reservation/forecast signal;
- service mode, quantity, mix and allocation are all contractually non-discretionary;
- actual served counts cannot be reconciled with reservation/production records;
- no stakeholder owns the decision or benefits from improving it.

If those conditions hold, stop adding model complexity and select another operational control point.

---

# 6. Claim firewall

Do **not** claim that:

- Boğaziçi currently uses reservation in normal academic-term dining;
- the historical `15` threshold remains valid today;
- reservation no-shows are a major current source of Boğaziçi waste;
- BUCard event data are accessible to the team;
- balance deduction equals contractor settlement/payment;
- better reservation prediction will reduce the published 48,251 kg food-waste figure by any specific amount;
- Control Organization membership reveals who makes daily production quantities.

What can safely be said:

> `PUBLIC SOURCE` Boğaziçi has deployed explicit meal reservation in special/low-demand operating regimes, has used reservation count to change service modality in a historical inter-semester case, and has attached a cancellation/no-show commitment rule in a 2026 holiday case. `HYPOTHESIS` The team is testing whether existing intent/access signals can reduce uncertainty in a reachable dining production or service-mode decision during normal operations.
