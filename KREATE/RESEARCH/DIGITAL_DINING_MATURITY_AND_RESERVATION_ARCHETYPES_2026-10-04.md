# Digital Dining Maturity & Reservation Archetypes — 2026-10-04

**Purpose:** determine whether the initial market can be treated as one common demand-planning workflow, or whether existing digital/reservation systems materially change the problem and product.  
**Status:** secondary/public-source market segmentation evidence. **Not customer validation.**

## Executive conclusion

Turkish universities already span materially different dining-data architectures.

At least three archetypes are visible from official sources:

1. **reservation-first dining** — diners commit to campus/meal in advance;
2. **integrated card/identity dining** — cafeteria card systems are connected to institutional student/personnel systems;
3. **non-reservation / historical-demand planning** — quantity is inferred from past demand and other context.

This means BOUNCAMPUS should not define its beachhead only by institution size. A university with a strong reservation system has a different forecasting problem from one with no pre-commitment signal.

The product must discover the existing demand signal first, then decide whether the value is:

```text
forecasting
reservation no-show correction
walk-in estimation
campus allocation
batch release
surplus/shortage verification
```

---

# 1. Amasya University — explicit reservation-first demand signal

Amasya University's official SKS page states that a meal reservation system is already used:

> to prevent waste and determine the total number of meals for internal stakeholders.

Official source:
https://sksdb.amasya.edu.tr/yemek-rezervasyon-sistemi-hakkinda

The university asks users to specify:

- meal period;
- campus;
- reservation choice.

A separate official guidance page states that the reservation is tied to the selected campus and that a user cannot consume the reservation at another campus; turnstile passage is enforced accordingly.

Official sources:
- https://suluovamyo.amasya.edu.tr/yemekhane-hizmetleri-ve-rezervasyon-sistemi-hakkinda-duyuru
- https://sksdb.amasya.edu.tr/2025-2026-egitim-ogretim-yili-beslenme-hizmetleri-hakkinda-bilgilendirme

The public instructions also show reservation windows can be set a week in advance for the following week's service.

### Strategic implication

At a site like Amasya, the first decision problem may not be generic attendance forecasting.

More plausible residual problems include:

```text
reservation -> actual attendance / no-show
+
unreserved walk-ins
+
campus-specific allocation
+
late changes
+
shortage/surplus safety margin
```

A simple forecast product that ignores reservations would be inferior to the existing operating signal.

---

# 2. Amasya also combines reservation with post-meal feedback

Amasya publicly describes enhancements to the reservation system that allow users to rate:

- the day's menu as a whole;
- individual menu components;
- suggestions/complaints after service.

Official source:
https://sksdb.amasya.edu.tr/yemek-rezervasyon-sistemi-yenilikler

### Implication

Some institutions already combine:

```text
pre-service commitment signal
+
post-service preference/quality feedback
```

BOUNCAMPUS cannot claim that combining feedback and digital dining is itself novel.

The unresolved opportunity is whether these signals are translated into better production/allocation decisions and objectively linked to outcomes.

---

# 3. Akdeniz University — integrated cafeteria-card infrastructure

Akdeniz University's official 2024 institutional self-evaluation report states that it operates a **Yemekhane Kart Yönetim Sistemi (YKYS)** and that this system is integrated with:

- PBS — personnel information;
- OBS — student information.

The report also describes wider integrated institutional information-management infrastructure and notes a 2024 benchmarking effort with İstanbul Technical University around information management.

Official source:
https://webis.akdeniz.edu.tr/uploads/1083/content/A%C3%9C_K%C4%B0DR_2024_M%C4%B0S%20%C3%A7%C4%B1kt%C4%B1s%C4%B1.pdf

### What this supports

Some target universities have mature identity/card/data infrastructure.

### What it does not support

- that cafeteria transaction history is available to a forecasting vendor;
- that card events equal meals consumed;
- that production planners see this data before their decision;
- that the existing system includes production forecasting.

### Strategic implication

`digital maturity` can be both:

**opportunity**
- easier integration;
- cleaner realized-demand signals;
- stronger institutional data governance.

**risk**
- existing software may already cover more workflow;
- security/IT review may be stricter;
- a new standalone dashboard may be redundant.

---

# 4. Reservation maturity changes the product object

## Archetype R0 — no pre-commitment signal

Likely product question:
> How many meals should we expect?

Potential inputs:
- history;
- academic calendar;
- menu;
- weather;
- campus activity;
- events.

## Archetype R1 — partial reservation

Product question:
> How should reservations be corrected for no-shows and walk-ins?

Potential inputs:
- reservation count;
- historical reservation-to-show conversion;
- campus/meal;
- late cancellations;
- context.

## Archetype R2 — strong reservation / campus-locked allocation

Product question:
> How much safety stock/batch flexibility is still needed around a strong committed signal?

Potential value may move toward:
- no-show prediction;
- late allocation;
- second-batch release;
- exception detection;
- service-risk planning.

## Archetype R3 — reservation + operational feedback + integrated systems

Product question:
> Can the system close the loop from commitment → production → served → surplus/shortage → learning better than the incumbent stack?

This is the most difficult incumbent environment but potentially the richest data environment.

---

# 5. Beachhead implication

A more homogeneous beachhead may need to include an existing-signal clause.

Candidate definition:

> High-volume institutional university dining operations where the production/allocation decision is reachable and **current pre-service demand signals are either absent, incomplete, or not sufficiently reconciled with realized service outcomes**.

This is better than assuming all high-volume universities need another forecast.

---

# 6. PMR questions added by this research

For every institution ask:

- Is there a reservation system?
- Is reservation optional or mandatory?
- At what deadline does reservation close?
- Is it campus-specific and meal-specific?
- How often do reserved diners not arrive?
- How many non-reserved diners are admitted?
- Does the kitchen receive the reservation count before production freezes?
- How is the safety buffer set on top of reservations?
- Are card/turnstile actuals reconciled against reservations?
- Does the production planner see those reconciliation reports?
- What decision remains difficult even with the current system?

Do not pitch forecasting until the answer to these is known.

---

# 7. Product architecture consequence

The demand module should support an adapter hierarchy:

```text
no reservation
    -> history/context baseline

partial reservation
    -> reservation + conversion/walk-in model

strong reservation
    -> exception / safety-buffer model
```

This is strategically more robust than forcing every institution into one feature pipeline.

---

# 8. Market-screening field additions

Add to ICP screening:

```text
reservation_system: none | partial | strong
reservation_deadline
campus_specific: yes/no
meal_specific: yes/no
walk_in_policy
no_show_rate_known: yes/no
turnstile_actuals_available: yes/no
reservation_actual_reconciliation: none/manual/automated
planner_access_before_freeze: yes/no
```

These fields can materially change both product fit and sales difficulty.

---

## Current conclusion

Digital dining maturity is not a simple positive score.

The best early customer is likely not the institution with the most technology or the least technology, but the one where:

```text
real decision pain
+
reachable operator
+
usable existing signal
+
clear residual gap
+
measurable outcome
```

coexist.
