# Türkiye Institutional Dining — Procurement, Policy & Operational Precedents

**Research date:** 2026-10-06  
**Evidence class:** secondary/public-source research only. **Not PMR, not Boğaziçi contract evidence, not customer validation.**

## Executive implication

Turkish institutional dining has multiple documented operating archetypes where the production-quantity decision, shortage responsibility and settlement quantity are economically meaningful. This strengthens the plausibility of the BOUNCAMPUS control-point hypothesis, but it also makes one thing clear: **the product cannot assume a universal workflow. Contract and decision semantics are segment-defining variables.**

## 1. Türkiye-specific food-waste prevention method

`VPMR-SRC-029` is an official guide prepared through T.C. Tarım ve Orman Bakanlığı, FAO and Metro Türkiye for hotels, restaurants and other mass-consumption food-service settings.

It explicitly covers separation/measurement, planning, processing, service, prevention and food-waste tracking. It is useful because it gives the project a Türkiye-specific methodological reference rather than relying only on UNEP/EPA/WRAP.

**Boundary:** it does not establish the cause or magnitude of Boğaziçi waste and does not prove that demand forecasting is the dominant intervention.

## 2. Kırıkkale University — contractor bears quantity uncertainty

Official KİK decision `2026/UH.I-2269` (`VPMR-SRC-030`) reproduces technical-specification language stating that:

- daily meal counts are determined by the contractor using previous meal counts;
- insufficient food can trigger penalties;
- payment/hakediş is based on food actually consumed;
- the administration is not responsible for excess food;
- demand may vary with academic calendar and menu.

### Product consequence

This is a strong public precedent for an **asymmetric decision-loss problem**:

```text
too little → service/penalty risk
too much → contractor carries excess-production risk
payment → realized consumption
```

If Boğaziçi/TEMAŞ has similar economics, the contractor may be a direct beneficiary/user of better quantity decisions. If the contract differs, the buyer and beneficiary may be elsewhere.

### PMR question

> For the last service where quantity was wrong, who paid for the excess and who bore the shortage consequence? Which count drove payment?

## 3. University precedent — one-day-ahead quantity + turnstile settlement

`VPMR-SRC-031` is an official KİK precedent where the reproduced specification states that production quantity is set daily by the contractor with administration approval, communicated at least one day in advance, while turnstile/mobile/ticket records contribute to the consumed-meal count used for payment.

### Product consequence

This proves that the following objects can be distinct in real Turkish institutional contracts:

```text
planned/declared production quantity
administrative approval
actual access/consumption records
payment/settlement quantity
```

Therefore BOUNCAMPUS must not collapse `planned`, `produced`, `turnstile`, `served`, `accepted` and `settled` into one field.

## 4. İTÜ — reservation tied explicitly to production planning

The official İTÜ SAY guide (`VPMR-SRC-032`) states that the reservation system aims to know how many meals to produce and thereby reduce waste. The guide describes at least a 48-hour preparation need and reservations by day, dining hall and meal.

The separate İTÜ sustainability page (`VPMR-SRC-033`) describes production estimates using academic calendar, course/exam intensity, menu options, weather and historical consumed-meal counts; it also describes rapid alternative-menu preparation when demand exceeds production.

### Product consequence

Reservation, calendar, weather and historical demand are **not novel features**. Differentiation must come from a specific unresolved decision/workflow/evidence problem.

### Segmentation question

Institutions with mature reservations may have a different uncertainty structure from walk-in-heavy services. Treat `reservation-heavy` vs `walk-in-heavy` as a possible market segmentation dimension.

## 5. GTÜ — planning exists, but mismatch still occurs

GTÜ's dining page, updated 10 September 2026 (`VPMR-SRC-034`), says production quantity uses historical consumption, daily user counts and waste-prevention planning, while unexpected demand can still cause some dishes to sell out early and require rapid replenishment.

### Product consequence

The alternative is not necessarily `no planning`. A realistic competitor is often:

```text
experienced operator
+ historical consumption
+ user-count estimate
+ menu judgment
+ safety buffer / replenishment
```

BOUNCAMPUS must benchmark against that operational baseline, not only against naive ML baselines.

## 6. Academic evidence narrows the novelty claim

### Rodrigues et al. — catering services

`VPMR-SRC-035` compares machine-learning demand forecasts against baseline models intended to mimic existing catering forecasts across three catering services. The paper reports both surplus/waste and unmet-demand implications.

Use: supports baseline-vs-model evaluation and asymmetric decision metrics.

Boundary: reported effect sizes are external case-study results and must never become expected BOUNCAMPUS impact.

### Acı & Yergök — university refectory

`VPMR-SRC-036` uses calendar effects and meal ingredients for university-refectory demand forecasting without pre-booking.

Use: calendar/menu-aware forecasting is established prior art.

### Aydın et al. — institutional turnstile data

`VPMR-SRC-037` uses institutional turnstile entry data for cafeteria demand forecasting.

Use: turnstile data are a credible signal class.

Boundary: it does not establish Boğaziçi access, privacy approval, retention or `turnstile == served meal` semantics.

## 7. Market archetypes suggested by public evidence

| Archetype | Quantity owner | Signal pattern | Economic risk | BOUNCAMPUS implication |
| --- | --- | --- | --- | --- |
| Contractor-risk / pay-per-consumed | Contractor | history + local judgment | excess and shortage can sit heavily with contractor | contractor may be user + beneficiary |
| Admin-approved contractor plan | Contractor + administration | planned quantity submitted before service | shared approval, settlement via consumption records | workflow/approval integration matters |
| Reservation-heavy | institutional system / dining ops | reservations well before production | uncertainty partly reduced upstream | value may shift to no-show/allocation/exception decisions |
| Walk-in / heuristic-heavy | kitchen/operations | history, calendar, menu, weather, user counts | buffer vs sell-out tradeoff | decision-support opportunity if incremental lift is real |

These are **research archetypes**, not claims that any specific institution exactly fits one bucket.

## 8. P0 PMR questions created by this research

1. Who sets tomorrow's production quantity at Boğaziçi/TEMAŞ?
2. What exact timestamp is the freeze/commit point?
3. Is there an administration approval step?
4. Which current heuristic/system produces the number?
5. What count drives hakediş/payment?
6. Who pays for excess production?
7. What penalty/service consequence follows underproduction?
8. Are reservations available for normal services or only exceptional periods?
9. Can privacy-safe aggregate turnstile/payment counts be exported, and what event does each row represent?
10. Can the operator replenish during service, and at what cost/latency?
11. Does a second contractor/university project use the same planning/settlement semantics?

## 9. Decision consequence

Desk research now has diminishing returns for the core market thesis. The next high-value evidence is **primary**: decision-owner incidents, contract/hakediş semantics, source-owner data dictionaries and a second-site repeatability test.
