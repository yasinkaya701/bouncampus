# CS1 Cafeteria Recommendation Data Research

Status: `PUBLIC_DATA_FOUNDATION`

Owner: CS1 — Decision Intelligence

Branch scope: research/data design only. This document does not claim access to Boğaziçi private POS, BUCard, reservation, production, or waste telemetry.

## Decision target

The serious model target is not a decorative "what should I eat?" recommender. The primary decision is:

> For each campus × service × date, how many portions should be prepared / released in each batch, given information available before the decision freeze, while balancing surplus/waste risk against shortage/early-sellout risk?

A secondary layer can rank menu alternatives using observed preference evidence when that evidence exists (poll votes, tasting scores, item take-rates). It must not infer student preference from menu text alone and call it observed preference.

## Public data already located

### 1. Official Boğaziçi cafeteria menu archive

Provider: Boğaziçi University Yemekhane

- Monthly lunch/dinner menu: https://yemekhane.bogazici.edu.tr/aylik-menu
- Example full historical month: https://yemekhane.bogazici.edu.tr/aylik-menu/2026-01
- Example recent historical month: https://yemekhane.bogazici.edu.tr/aylik-menu/2026-08
- Breakfast archive pattern: https://yemekhane.bogazici.edu.tr/kahvalti-menu/YYYY-MM
- Packet menu pattern: https://yemekhane.bogazici.edu.tr/paket-menu/YYYY-MM
- Food/photo catalogue: https://yemekhane.bogazici.edu.tr/yemek-fotogralari

The January 2026 archive exposes date, service and linked dish names for lunch and dinner. The site navigation also exposes separate breakfast, packet-menu, food-catalogue, waste and survey surfaces.

**Use in model:** menu identity, menu composition, service type, dish recurrence, novelty, protein family, vegan/vegetarian alternatives, side/dessert/drink composition, menu-conditioned demand residuals.

**Important:** menu availability is a feature, not a demand target.

### 2. Dish-level food pages

The official site links individual dishes from historical menus. These pages can expose useful structured information such as portion mass, calories and ingredients where maintained.

**Use in model:** content representation and normalized menu features:

- calories per listed serving,
- portion grams,
- ingredient tokens,
- protein family,
- starch family,
- legumes,
- dairy,
- dessert/sugar proxy,
- vegan/vegetarian flag when supported by the official catalogue,
- recipe similarity / menu novelty.

Missing nutrition fields must remain missing; do not impute an official calorie value from a language model.

### 3. Official menu poll

The cafeteria announced a weekly menu poll in BUCAMPUS in which eligible users vote among three Wednesday lunch alternatives.

Source: https://yemekhane.bogazici.edu.tr/

Searchable announcement title: `Menü Anketi`.

**High-value private export request:** anonymous aggregate candidate vote counts by poll, candidate dish IDs/names, open/close timestamps, winning menu, eligible population if available.

If obtained, this is much better preference evidence than hand-assigned "popular" scores.

### 4. Official tasting activity / surveys

The cafeteria site exposes satisfaction and meal-tasting survey surfaces and announced a daily tasting activity with volunteer evaluation forms.

**High-value private export request:** de-identified aggregate tasting scores by date/service/menu item plus question schema and sample count.

These scores can be used as an auxiliary preference/quality target, but must not be conflated with served demand.

### 5. Waste surface

The official cafeteria navigation exposes `Atık Miktarları`. Public indexing/retrieval is not yet reliable enough to treat it as a parsed training table.

**Action:** request/export the underlying records from Food Services rather than fabricating or screen-reading numbers. Desired minimum fields are listed under `Private data required` below.

### 6. Academic calendar

Provider: Boğaziçi University

- Current calendar: https://akademiktakvim.bogazici.edu.tr/tr/

**Derived features:**

- `is_class_day`
- `semester_phase`
- `registration_period`
- `add_drop_period`
- `withdrawal_period`
- `midterm_proxy` only if supported by a real calendar/feed
- `final_exam_period`
- `holiday_no_classes`
- `days_from_semester_start`
- `days_to_final_period`

Do not infer attendance directly from these flags. They are contextual predictors.

### 7. Cafeteria operational announcements

Provider: Boğaziçi University Yemekhane announcements

Operational changes such as holiday closures, Ramadan service-hour changes, package-service periods, campus-specific closures/repairs and price changes are structural-break features.

**Derived features:**

- `service_regime_id`
- `is_package_service`
- `service_hours_variant`
- `campus_open_flag`
- `holiday_regime`
- `ramadan_regime`
- `price_regime_id`

These features need effective start/end dates and provenance. A text announcement should be converted into a dated regime table, not embedded as an untraceable prompt.

### 8. Weather

Provider: Open-Meteo

- Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api

Candidate variables:

- temperature,
- apparent temperature,
- precipitation,
- rain,
- relative humidity,
- wind speed,
- weather code.

**Leakage rule:** if the kitchen decision is made at T-1 day, production experiments should use the weather forecast that would have been available at T-1, not realized same-day reanalysis. Historical realized weather can be used for exploratory analysis and an explicit oracle/upper-bound experiment only.

### 9. Environmental intensity proxies

Provider: Our World in Data / Poore & Nemecek food-system data

- GHG intensity: https://ourworldindata.org/grapher/ghg-per-kg-poore

The OWID chart provides an open CSV/API and CC BY reuse terms. It can support ingredient-category environmental intensity proxies.

Provider: ADEME AGRIBALYSE

- Documentation/data portal: https://agribalyse.ademe.fr/

**Use:** external proxy features for scenario analysis, not measured Boğaziçi environmental impact.

Dish-level carbon/water estimates are uncertain because campus recipe weights, sourcing and preparation can differ materially. Preserve `impact_provenance=EXTERNAL_LCA_PROXY` and uncertainty/coverage.

## Private data required for a real production recommender

Public menu/context data is not enough to train the actual production recommendation target. Request the following exports, ideally at `campus × service × date` granularity with stable service IDs.

| Priority | Dataset | Minimum fields | Why it matters |
| --- | --- | --- | --- |
| P0 | Served meal count | service_id, date, campus, service_type, served_count, source timestamp | Primary demand target |
| P0 | Production quantity | service_id, prepared_portions or prepared_kg, batch timestamps | Converts demand forecast into production decision evaluation |
| P0 | Waste / leftovers | service_id, avoidable production waste kg/portions, measurement method, timestamp | Direct waste objective |
| P0 | Reservation snapshot | service_id, snapshot_at, active_reservations | Strong intent signal; must be reconciled with show/no-show |
| P1 | Reserved-served reconciliation | reserved_served_count, unreserved_served_count | Learns show rate and walk-in component without treating reservation as demand |
| P1 | Stockout / sellout | item/service, stockout time, affected portions if known | Shortage penalty / service quality |
| P1 | Menu poll | poll_id, candidates, vote_count, open/close time, winner | Observed preference signal |
| P1 | Tasting/satisfaction | menu/service, aggregate score, n, questionnaire version | Auxiliary quality/preference target |
| P1 | Item take-rate | item, portions offered, portions selected | Learns menu mix rather than only total attendance |
| P2 | Operator plan and override | recommendation, operator plan, override, reason, timestamps | Decision-quality and human-in-loop evaluation |
| P2 | Cost | food/component cost or service-level production cost | Economic objective; do not substitute menu retail/subsidy price |

### Privacy boundary

The forecasting model does not need student identities. Prefer service-level aggregates. If raw reservation/user events are ever supplied, transform to privacy-preserving aggregates upstream and document retention/access policy.

## Canonical service-level training table

One row per service decision:

```text
service_id
service_date
campus_id
service_type
information_cutoff_at
decision_freeze_at
menu_id
menu_features...
calendar_features...
operational_regime_features...
weather_forecast_features...
reservation_features...
history_features...
served_count                 # target; observed
prepared_count               # decision/outcome context
waste_count_or_kg            # outcome
stockout_flag/time           # outcome
source_coverage
source_freshness
truth_status
```

Do not place post-service observations into pre-service features.

## Menu representation

Keep two representations in parallel.

### Transparent engineered representation

- soup category
- animal protein: beef / poultry / fish / none
- legume main
- vegan alternative
- rice / bulgur / pasta / pastry side
- fried indicator where derivable from recipe/name
- dessert type
- dairy side/drink
- listed calories and portion grams coverage
- menu novelty: days since exact dish/menu last appeared
- recurrence counts over trailing windows

This representation is preferred for early models because it is auditable.

### Learned representation

After enough history exists, create embeddings from normalized dish/ingredient tokens. Embeddings may improve generalization across rare dishes, but they should be evaluated by ablation against transparent features.

Do not use an LLM-generated scalar `popularity_score` as if it were ground truth.

## Recommended model ladder

Complexity is earned by out-of-time evidence.

### Baselines

1. historical median by campus × service × weekday;
2. same weekday previous week;
3. rolling median/mean;
4. raw reservation at decision cutoff, if available;
5. corrected reservation = reservation × historical show rate + historical unreserved component;
6. menu-conditioned linear/GAM baseline.

### Main tabular models

First serious candidates:

- CatBoost / LightGBM / XGBoost for point demand;
- quantile gradient boosting for P10/P50/P90 or similar decision intervals;
- generalized additive model / hierarchical model as an interpretable comparator.

Do not jump to LSTM/TFT until there is enough sequential history to justify it. Deep sequence models are not automatically stronger on small institutional datasets.

### Decision layer

Forecasting and recommendation are separate stages.

Given predictive demand distribution `D` and a proposed production quantity `q`, evaluate a pre-registered asymmetric loss such as:

```text
L(q, D) = c_surplus * max(q - D, 0) + c_shortage * max(D - q, 0)
```

`c_surplus` and `c_shortage` are policy/sensitivity parameters until real economics/PMR establishes them. Do not label them TRY costs without evidence.

The system may output `WITHHOLD` when critical sources are missing or the decision is no longer operationally reachable.

## Evaluation protocol

### Split

Use rolling-origin / forward-chaining evaluation. Never random-split adjacent cafeteria days.

Example:

- train: earliest block
- validation: next chronological block
- test: final untouched block
- repeat rolling folds if history is sufficient

Keep regime shifts visible; do not silently shuffle Ramadan, summer and exam periods across train/test.

### Metrics

Forecast metrics:

- MAE
- WAPE
- RMSE as secondary
- pinball loss for quantiles
- empirical interval coverage and width

Decision metrics:

- surplus portions/kg
- shortage portions / early-sellout events
- asymmetric decision loss
- regret versus operational baseline
- waste kg per 100 served when measured
- operator override rate when piloted

Model promotion must be compared on common support. A model that only predicts easy rows cannot beat a baseline by dropping hard rows.

## Feature leakage checklist

Reject a feature from a decision-time dataset if it was not known before `information_cutoff_at`.

Common leakage traps:

- realized same-day weather instead of forecast available at cutoff;
- final reservation count captured after production freeze;
- served count embedded in a reconciliation feature;
- waste measurement from the target service;
- poll/tasting result published after the production decision;
- menu edits made after the saved menu snapshot;
- future rolling statistics.

## Data quality fields required on every source

Each ingested dataset should carry:

- `source_id`
- `source_url_or_system`
- `retrieved_at`
- `effective_at`
- `available_at_decision_time`
- `license_or_access_basis`
- `raw_hash` when stored
- `parser_version`
- `quality_status`
- `missingness_reason`

A source-health failure should be machine-readable and should be able to downgrade a recommendation.

## Immediate collection order

1. Parse all available official monthly lunch/dinner menus into service rows.
2. Parse breakfast and packet-menu archives separately.
3. Crawl linked dish pages and build a normalized dish dictionary.
4. Join official academic-calendar flags by date.
5. Build a dated operational-regime table from cafeteria announcements.
6. Join decision-time-valid weather data/forecasts.
7. Map dish ingredients to external LCA categories with explicit proxy provenance.
8. Obtain P0 private exports: served, prepared, waste and reservation snapshots.
9. Only after P0 targets exist, benchmark baselines and serious ML using chronological evaluation.

## Stop conditions / truth boundary

Until P0 observed targets exist:

- public data can validate ingestion, feature engineering and menu representation;
- public data cannot prove production-demand accuracy;
- do not publish an `R²`, MAE, waste-reduction percentage or monetary savings as Boğaziçi performance;
- do not call synthetic labels measured data;
- synthetic events, if used for software tests, must live in explicitly synthetic fixtures and never in evidence outputs.

The immediate goal of this research branch is to make the model data-ready without crossing that boundary.
