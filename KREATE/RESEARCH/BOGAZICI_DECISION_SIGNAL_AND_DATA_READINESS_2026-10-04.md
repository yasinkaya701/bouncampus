# Boğaziçi Decision-Signal & Data-Readiness Map — 2026-10-04

**Status:** Public-source + repository synthesis. **No claim of access to private operational datasets.**

## Decision target

The primary candidate decision remains:

> **For each campus x service x date, how many portions should be prepared/released, given information available before the production freeze, while balancing surplus against shortage risk?**

A recommendation is only useful if every feature used was available **before** the relevant decision cutoff.

---

# 1. Publicly available signals that can support a data pipeline today

## 1.1 Monthly regular menu archive

Official current/monthly menu pages expose dated lunch and dinner composition.

Sources:

- https://yemekhane.bogazici.edu.tr/aylik-menu
- example historical/current archive: https://yemekhane.bogazici.edu.tr/aylik-menu/2026-08

Observed fields include:

- date;
- lunch/dinner;
- soup;
- main meal;
- vegan/vegetarian alternative;
- side alternatives;
- selectable dessert/drink/salad items.

Individual/current food entries can expose:

- calories;
- cooked portion gram weights for some items.

### Candidate features

```text
meal_period
main_dish_family
vegetarian_option
starch_family
side_count
sweet/dessert indicator
published_calories
published_portion_grams
menu novelty / recurrence
```

### Boundary

Menu is context. It is **not** a demand label and not observed preference.

---

# 1.2 Breakfast menu archive

Official example:

https://yemekhane.bogazici.edu.tr/kahvalti-menu/2026-06

Breakfast is operationally distinct enough that it should not automatically share the same demand model with lunch/dinner.

Candidate separate service class:

```text
service_type = BREAKFAST
```

---

# 1.3 Packaged-meal channel

Official packaged-menu page:

https://yemekhane.bogazici.edu.tr/paket-menu

The current page exposes separate package lunch/dinner menus. This confirms that packaged service is not merely a theoretical channel.

### Model consequence

Do not collapse all meals into one demand target if regular dine-in and package channels are separately planned/distributed.

Candidate key:

```text
campus
meal_period
service_channel = DINE_IN | PACKAGE | OTHER
```

The ownership and allocation process remain PMR unknowns.

---

# 1.4 Operational regime announcements

The dining site publishes operational changes that create structural breaks.

Examples:

- 18 Aug–19 Sep 2025: breakfast/dinner suspended weekdays and all meal service suspended weekends across listed campuses;
- Kilyos summer period: weekday lunch continued while breakfast/dinner/weekend service paused;
- 2026 announcement index includes Ramadan-hour changes, Kilyos/Hisar changes, package-service changes, holiday service and meal-price changes.

Sources:

- https://yemekhane.bogazici.edu.tr/yaz-donemi-yemek-hizmeti-hakkinda
- https://yemekhane.bogazici.edu.tr/saritepe-kilyos-kampus-yemek-hizmeti-hakkinda
- https://yemekhane.bogazici.edu.tr/duyurular

### Required feature architecture

Do not treat a closed service as low demand.

```text
service_regime_id
campus_open_flag
meal_service_available
regular_term
exam_period
summer_reduced_service
holiday
ramadan_hours
campus_specific_exception
package_only_or_special_channel
price_regime_id
```

Each derived regime must retain source + effective dates.

---

# 1.5 Academic calendar

Official calendar:

https://akademiktakvim.bogazici.edu.tr/

Candidate pre-service features:

```text
is_class_day
term_phase
registration_or_orientation
add_drop
exam_period
holiday
summer_term
days_from_term_start
```

### Boundary

Schedule/calendar information is a context feature, not live occupancy.

---

# 1.6 Menu voting / preference signal

The BUCampus menu survey publicly confirms authenticated weekly voting for Wednesday lunch alternatives.

Source:
https://yemekhane.bogazici.edu.tr/menu-anketi

### High-value export if available

```text
poll_id
candidate_menu_items
vote_count
open_at
close_at
winner
```

### Boundary

Vote != reservation. Vote != campus attendance. Vote != portion demand.

Use only as an optional preference feature if historical aggregates can be accessed and show out-of-sample incremental value.

---

# 1.7 BUCard / QR turnstile clue

Official FAQ indicates support workflows involving:

- date;
- time;
- campus;
- turnstile;
- BUCard / BUCampus QR entry.

Source:
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

### Safe interpretation

Some operational access events carry time/campus/turnstile context.

### Unknowns requiring IT PMR/data-owner confirmation

- historical retention;
- aggregate export ability;
- duplicate/failed/refund semantics;
- whether QR and card events share a clean schema;
- whether one event corresponds one-to-one with a served meal;
- whether data exist before or only after a service.

### Ideal privacy-safe export

```text
date
campus
meal_window
validated_entry_count
source_definition
```

No student identity is required for the first pilot.

---

# 1.8 Weather

Weather is a candidate exogenous feature, not a guaranteed useful signal.

### Leakage rule

If the quantity freezes at T-1, training/evaluation must use the forecast that could have been available at T-1, not realized future weather.

Realized historical weather can be used only for:

- exploratory analysis;
- explicitly labeled oracle/upper-bound experiments.

---

# 2. Critical private/operational data still missing

Public context is insufficient to validate the core model.

## P0

| Dataset | Minimum fields | Reason |
| --- | --- | --- |
| planned/requested quantity | service_id, quantity, created_at, owner | reconstruct current decision |
| production | service_id, produced portions/kg, batch timestamps | quantify overproduction/action |
| served demand | service_id, campus, meal/channel, served count | target / realized demand |
| edible surplus | service_id, quantity/kg, method | addressable production-surplus outcome |
| shortage/sellout | service_id, event time, substitution/unmet demand | service guardrail |

## P1

| Dataset | Minimum fields | Reason |
| --- | --- | --- |
| waste-stage breakdown | prep / edible surplus / plate / other | determine causal mechanism |
| reservation snapshots if any | count + snapshot_at | pre-service intent |
| campus allocation | planned/delivered/returned | separate total production from allocation |
| operator overrides | recommended/planned/action/reason | learn hidden constraints |
| menu-poll aggregates | candidate/votes/time | preference feature test |

## P2

- ingredient/component cost;
- contractor settlement quantity;
- monthly progress-payment reconciliation;
- recipe/ingredient detail;
- staffing/batch constraints.

Economic modeling must wait until payment/cost semantics are verified.

---

# 3. Canonical service-level table

One row should represent one **decision episode**, not one sustainability-reporting month.

```text
service_id
service_date
campus_id
meal_period
service_channel
information_cutoff_at
decision_freeze_at
current_plan_quantity
menu_id
service_regime_id
calendar_features
weather_forecast_snapshot
reservation_or_intent_features
historical_demand_features
source_coverage
recommended_lower
recommended_target
recommended_upper
operator_action
operator_override_reason
produced_portions
served_portions
edible_surplus_kg
prep_waste_kg
plate_waste_kg
early_sellout
measurement_method
truth_status
```

Every post-service field must be excluded from pre-service model features.

---

# 4. Model ladder — complexity must be earned

Before sophisticated ML, benchmark:

1. same weekday + same service previous week;
2. rolling median by campus x meal x channel;
3. trailing comparable-service mean;
4. calendar/regime-aware linear/GAM baseline;
5. tree/boosting model;
6. quantile model for planning range;
7. only then deep sequence models if data volume supports them.

## Evaluation

Use chronological / forward-chaining splits.

Do not random-shuffle adjacent service dates across train/test.

Report:

### Prediction

- MAE;
- WAPE;
- quantile pinball loss;
- empirical planning-band coverage/width.

### Decision

- surplus portions/kg;
- shortage/sellout;
- asymmetric decision loss;
- regret vs current operational baseline;
- waste kg / 100 served where measured;
- operator override rate.

A slightly less accurate model can be operationally better if it handles asymmetric shortage/surplus risk better.

---

# 5. Feature leakage checklist

Reject or version carefully:

- realized weather after cutoff;
- final reservation count after freeze;
- service entry count observed during/after service;
- target-service waste;
- menu/vote changes after cutoff;
- operator edits made after recommendation;
- future rolling statistics.

Store both:

```text
observed_at
available_at_decision_time
```

where relevant.

---

# 6. Data-provenance requirement

Every source should retain at minimum:

```text
source_id
source_system_or_url
source_owner
retrieved_at
observed_at_or_effective_at
available_at_decision_time
scope
measurement_stage
unit
counting_semantics
parser_or_transform_version
quality_state
known_conflicts
```

This requirement is not academic decoration: official public sources already demonstrate that similarly named dining metrics can carry different years, scopes and denominators.

---

# 7. Stop conditions

Until real P0 targets exist:

- public context may be parsed and used to validate engineering;
- no Boğaziçi production-demand model accuracy can be claimed;
- no waste-reduction percentage can be claimed;
- no monetary savings can be claimed;
- synthetic labels must remain synthetic fixtures;
- schedule data must not be represented as observed occupancy.

---

# 8. Highest-value data-access PMR questions

## Food Services / contractor

- Where is planned quantity recorded?
- Where are produced and delivered quantities recorded?
- Is there a campus x meal x date history?
- Are batches timestamped?
- Is surplus separately recorded from general waste?
- Is sellout/substitution recorded?

## IT / BUCard

- Can privacy-safe aggregate entry counts be exported by date x campus x meal window?
- What exactly does one valid event mean?
- What retention horizon exists?
- Are duplicates/refunds/failed attempts distinguishable?

## waste owner

- What is the authoritative waste boundary?
- generation date or collection date?
- pre-consumer vs plate waste?
- campus/meal resolution?
- measurement method?

A `NO` answer is useful evidence: it defines the measurement product required for a pilot.
