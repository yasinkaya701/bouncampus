# Academic Demand-Modeling Evidence — 2026-10-04

**Status:** Secondary academic research. External performance numbers are **not** BOUNCAMPUS or Boğaziçi results.

---

# Executive conclusion

Academic literature supports the technical plausibility of university/institutional meal-demand forecasting, but it also makes one strategic point clear:

> **Forecasting itself is not novel.**

BOUNCAMPUS must win, if at all, on the operational decision workflow, feature timing, uncertainty/risk treatment, data semantics, human control and measured outcome verification.

---

# A-DM-01 — Catering demand forecasting should be benchmarked against operational baselines

Rodrigues, Miguéis, Freitas & Machado (2023), *Journal of Cleaner Production*:

https://consensus.app/papers/machine-learning-models-for-shortterm-demand-forecasting-rodrigues-miguéis/47d8e2ce5d015189bc052f02df2e3a47/

The study examines machine-learning approaches for short-term food-catering demand forecasting and explicitly compares against baseline models intended to mimic existing forecasting approaches.

### BOUNCAMPUS implication

Do not celebrate a model score in isolation.

The first real comparison must include operationally credible baselines such as:

```text
same weekday previous week
rolling median
trailing comparable-service mean
simple calendar-aware regression
```

A complex model is only promoted if it improves **out-of-time decision utility** on common support.

---

# A-DM-02 — University refectory demand can use calendar + meal composition

Mehmet Acı (2023), *Technical Gazette*, studied demand forecasting at a university refectory without pre-booking.

Paper:
https://consensus.app/papers/demand-forecasting-for-food-production-using-machine-acı/53fc30fe33fe579f8949e9a42a0ecc14/

The study evaluated multiple ML families and explicitly used:

- calendar effect;
- meal ingredients;
- demand during a limited service window such as lunch.

### Product implication

BOUNCAMPUS's candidate features such as calendar state and transparent menu composition are technically reasonable.

### Novelty boundary

Calendar-aware and meal-aware forecasting is not unique.

Therefore BOUNCAMPUS should not pitch:

> "We use the academic calendar and menu, unlike everyone else."

without a verified competitive comparison.

---

# A-DM-03 — Campus mobility/temperature/menu context can be predictive candidates

Gül Fatma Türker (2025), *Sustainability*:

https://consensus.app/papers/reducing-food-waste-in-campus-dining-a-datadriven-approach-turker/f9cb99983e0859509e84b8549e19c9f5/

The paper studies daily campus data and reports candidate predictive relationships involving:

- meal variety;
- meal counts;
- revenue;
- campus mobility;
- temperature.

### Product implication

These justify testing richer campus-context features **after** simple baselines.

### Critical caution

The abstract reports very high model-fit values for some algorithms and a food-waste result. Do not reuse those numbers as expected Boğaziçi performance.

The BOUNCAMPUS implementation should independently check:

- temporal split design;
- leakage risk;
- stability across academic regimes;
- decision utility versus a simple baseline.

---

# A-DM-04 — Turnstile data are a credible institutional demand signal

Aydın, Balcıoğlu & Sezen (2025), *OPUS Journal of Society Research*:

https://consensus.app/papers/machine-learning-techniques-for-cafeteria-demand-aydın-balcıoğlu/78329bb2e24e5c06a01d9f73bac74c0f/

The study uses **turnstile entry data from an academic institution** and compares XGBoost, LSTM and Prophet across daily/high-resolution forecasting.

The abstract reports recent historical patterns, weekly cycles and academic-calendar effects as important features.

### BOUNCAMPUS implication

This supports the idea that privacy-safe aggregate turnstile counts can be a useful realized-demand signal if operational semantics are validated.

### Boundary

It does not establish that Boğaziçi turnstile data are retained, accessible, clean, or one-to-one with served meals.

---

# A-DM-05 — Demand uncertainty should be translated into decision loss

Faezirad, Pooya & Naji-Azimi (2021), *Waste Management & Research*:

https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/

The study models university dining demand under uncertainty using reservation/show-no-show behavior and combines:

- waste cost;
- shortage penalty.

### Product implication

BOUNCAMPUS should not optimize only MAE/RMSE.

Candidate policy form:

```text
L(q, D) = c_surplus * max(q - D, 0)
        + c_shortage * max(D - q, 0)
```

where:

- `q` = proposed production quantity;
- `D` = realized demand;
- coefficients remain policy/PMR parameters until actual economics are verified.

This directly motivates:

- planning bands rather than one scalar;
- shortage guardrails;
- explicit risk sensitivity;
- human override.

---

# 1. Recommended model ladder

## Stage 0 — current operational heuristic

First document what the operator actually does.

Possible examples to test:

- yesterday / previous same weekday;
- recent average;
- fixed percentage buffer;
- reservation count + walk-in estimate;
- contractor experience;
- campus/event adjustment.

This is the true incumbent baseline.

## Stage 1 — naive reproducible baselines

1. previous same weekday/service;
2. rolling median;
3. trailing comparable-service mean;
4. seasonal median by campus x meal x channel.

## Stage 2 — transparent context model

Features:

- weekday;
- academic state;
- service regime;
- menu categories;
- time since dish/menu recurrence;
- decision-time weather forecast;
- prior demand.

Models:

- linear/GAM;
- interpretable tree model.

## Stage 3 — serious tabular ML

Candidate:

- CatBoost;
- LightGBM/XGBoost;
- quantile boosting.

## Stage 4 — sequence/deep models

Only if longitudinal data volume and regime stability justify them.

Do not assume LSTM/TFT is automatically better on a small institutional dataset.

---

# 2. Recommended output is a distribution/range, not magic number

A practical output should separate:

```text
predicted_demand
lower_planning_bound
recommended_quantity
upper_planning_bound
source_coverage
risk_state
```

The range must not be called a statistically calibrated confidence interval unless calibration has actually been evaluated.

Use honest labels such as:

- planning band;
- prediction quantiles if trained/evaluated as such;
- policy range if constructed from heuristics.

---

# 3. Evaluation protocol

## Time splits

Use rolling-origin / forward-chaining evaluation.

Avoid random train/test splits that leak adjacent-day patterns.

Keep structural regimes visible:

- normal term;
- exams;
- summer service;
- Ramadan/special hours;
- campus closure;
- package-only periods.

## Prediction metrics

- MAE;
- WAPE;
- RMSE secondary;
- pinball loss for quantiles;
- empirical band coverage + width.

## Decision metrics

- excess portions;
- unserved edible surplus;
- shortage/unmet demand;
- early-sellout frequency;
- emergency substitution;
- asymmetric decision loss;
- regret versus actual operator plan;
- override rate;
- waste kg / 100 served, when measured consistently.

---

# 4. Leakage controls

A feature is invalid if it was not known before the decision cutoff.

Common traps:

- realized same-day weather instead of forecast available at cutoff;
- final reservation count after production freeze;
- actual turnstile/served count from the target service;
- target-service waste;
- menu edit after the stored decision snapshot;
- future rolling aggregates;
- event attendance observed only after service.

Store:

```text
observed_at
available_at_decision_time
```

separately wherever timing matters.

---

# 5. Feature ablation rule

Every additional context source should have to earn its place.

Test increments such as:

```text
historical baseline
+ academic calendar
+ service regime
+ menu features
+ weather forecast
+ reservation/intention
+ mobility/occupancy aggregate
```

Remove features that do not improve out-of-time prediction/decision utility or whose operational collection burden exceeds their benefit.

This avoids "more data = better AI" architecture.

---

# 6. Menu representation

Start interpretable:

- animal protein family;
- legume/vegetable main;
- vegan option;
- starch type;
- dessert/sweet indicator;
- published portion grams where available;
- published calories where available;
- exact dish recurrence;
- menu novelty.

Only later test learned text/ingredient embeddings.

Never create an LLM-generated `popularity_score` and treat it as observed customer preference.

Use actual preference evidence only when available:

- menu vote;
- item take-rate;
- tasting/satisfaction aggregate;
- repeat demand residuals.

---

# 7. Model promotion gate

A richer model should not replace the baseline unless:

1. chronological holdout performance improves;
2. decision loss improves on common services;
3. shortage guardrails do not worsen materially;
4. missingness behavior is safe;
5. recommendation arrives before freeze time;
6. feature availability is operationally sustainable;
7. behavior is interpretable enough for the operator/risk level;
8. failure/abstention conditions are explicit.

---

# 8. Why BOUNCAMPUS still needs PMR even with strong academic evidence

No paper answers:

- Boğaziçi's exact quantity owner;
- freeze time;
- payment semantics;
- data-access path;
- local shortage penalty;
- waste-stage share;
- operator trust/adoption;
- integration/procurement friction.

Academic evidence validates the **problem class and candidate methods**, not the local product-market fit.
