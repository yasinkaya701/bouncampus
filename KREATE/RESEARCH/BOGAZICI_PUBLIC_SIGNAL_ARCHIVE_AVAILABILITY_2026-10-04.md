# Boğaziçi Public Signal Archive Availability — 2026-10-04

**Purpose:** distinguish public signals that can actually be reconstructed historically from signals whose existence is public but historical values are not.  
**Status:** public-web data-readiness research. **No claim of internal API/data access.**

## Executive conclusion

Boğaziçi's public dining ecosystem provides a meaningful historical context layer, but not a production-demand training target.

Signals fall into three classes:

### A — reproducible historical public signals

- dated regular lunch/dinner menus;
- dated breakfast menus;
- package-menu/service channel context;
- service closures/hour changes/campus changes;
- package-service changes;
- meal-price changes;
- academic calendar;
- effective-date policy/service changes such as BUBizden introduction.

### B — public mechanism, historical values not publicly exposed

- weekly menu-vote counts/results;
- satisfaction-survey responses;
- pre-service tasting scores;
- BUCard/QR valid-entry counts.

### C — operational target data absent publicly

- planned production quantity;
- produced quantity;
- campus allocation quantity;
- served portions;
- stage-separated edible surplus/waste;
- sellout/unmet demand;
- operator overrides.

Therefore a public-data prototype can build the **context/event spine**, but it cannot honestly claim to train or validate the real production decision without private/pilot labels.

---

# 1. Regular menu history is reconstructable

Official menu archive pattern:

https://yemekhane.bogazici.edu.tr/aylik-menu/YYYY-MM

Current/historical pages expose dated lunch and dinner menus.

Example:
https://yemekhane.bogazici.edu.tr/aylik-menu/2026-08

Potential historical fields:

```text
service_date
meal_period
soup
main_dish
vegetarian_vegan_option
side_options
selectable_items
published_calories
published_portion_grams_if_present
```

### Data caution

Menu taxonomy must be normalized reproducibly; free-text dish names should not be manually recoded differently between train/test.

---

# 2. Breakfast is a separate archived service class

Official breakfast archive example:

https://yemekhane.bogazici.edu.tr/kahvalti-menu/2026-06

Breakfast should be treated separately from lunch/dinner unless real data justify pooling.

Candidate key:

```text
service_type = BREAKFAST
```

---

# 3. Package service is historically stateful

Current homepage and archived announcements show package service can operate as a separate channel and can be:

- enabled/disabled;
- restricted by meal period;
- changed during summer/holiday/Ramadan regimes.

Examples:

- current dining page: https://yemekhane.bogazici.edu.tr/
- summer 2026 package restriction: https://yemekhane.bogazici.edu.tr/yaz-donemi-paket-yemek-hizmeti-hakkinda
- announcement archive: https://yemekhane.bogazici.edu.tr/duyurular

### Feature requirement

```text
service_channel
package_service_available
package_service_meal_period
package_regime_id
```

Never interpret a suspended channel as naturally low demand.

---

# 4. Announcement archive is a valuable historical regime table

The official dining announcement archive currently contains dated operational changes spanning multiple years.

Source:
https://yemekhane.bogazici.edu.tr/duyurular

Examples include:

- summer service reductions;
- campus-specific closures/changes;
- package-service starts/stops;
- Ramadan operating hours;
- holiday service;
- breakfast-service changes;
- meal-price updates;
- renovation/transported-food regimes;
- BUBizden introduction.

### Recommended derived table

```text
regime_event_id
effective_start
effective_end
campus
meal_period
service_channel
event_type
old_state
new_state
source_url
published_at
confidence
```

### Critical rule

Announcement publication date and operational effective date can differ. Store both.

---

# 5. Price history is publicly reconstructable and may be a demand context feature

The current dining site publishes meal prices, and the announcement archive contains multiple dated price updates.

Official archive:
https://yemekhane.bogazici.edu.tr/duyurular

Current homepage:
https://yemekhane.bogazici.edu.tr/

### Candidate context

```text
student_breakfast_price
student_lunch_price
student_dinner_price
personnel_price_tier
price_regime_id
```

### Boundary

Price change is a plausible demand feature, not a proven causal driver.

Only use if historical demand labels later show incremental out-of-sample value.

---

# 6. BUBizden is a dated access/policy regime change

Boğaziçi launched BUBizden meal support effective **26 February 2026**.

Official announcement:
https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi

Public description states eligible students can receive one meal entitlement per day and rights are managed through the university mobile application.

### Candidate regime feature

```text
bubizden_active
```

Potential future private aggregate signal:

```text
bubizden_entitlements_issued
bubizden_entitlements_used
```

### Boundary

The public page does not expose historical daily usage counts.

Do not infer that BUBizden materially changed demand without actual data.

---

# 7. Menu-vote mechanism is public; vote history is not publicly reproducible

Official menu-vote page:
https://yemekhane.bogazici.edu.tr/menu-anketi

The page establishes:

- authenticated BUCampus voting;
- one vote per user;
- a recurring Friday–Monday voting window;
- vote winner influences Wednesday lunch menu.

### Publicly missing

Targeted public search did not expose an official historical series of:

```text
candidate options
vote counts
winner count/share
poll snapshots
```

### Consequence

Do not include historical vote count as a production feature in a reproducible public model unless an internal export is obtained.

The mechanism can still be represented as a known policy/process.

---

# 8. Satisfaction/tasting mechanisms are public; response history is not

Official current satisfaction survey surface:
https://yemekhane.bogazici.edu.tr/anketler/memnuniyet-anketi

Official tasting activity:
https://yemekhane.bogazici.edu.tr/yemek-tadim-etkinligi

The existence and timing of these mechanisms are public.

The detailed historical response-level/service-level scores are not publicly exposed in a reproducible archive found in this research.

### Consequence

Do not convert the presence of a survey into a time-series model feature.

Ask the source owner whether aggregate historical exports exist internally.

---

# 9. BUCard/QR event history is operationally plausible but not public

Public support pages establish event context such as:

- time;
- campus;
- turnstile;
- card/QR use.

But no public historical count endpoint was identified.

### Required internal export

Prefer:

```text
service_date
campus
meal_window
validated_entry_count
count_semantics
```

No identity-level fields are necessary for the first decision test.

---

# 10. Public context spine vs private target spine

## Public context spine can be built now

```text
date
academic_calendar
menu
service_regime
campus_service_availability
channel_regime
price_regime
policy_events
weather_forecast_snapshot if archived appropriately
```

## Private/pilot target spine is still required

```text
current_plan
produced
served
unserved_surplus
stage_separated_waste
sellout/substitution
override
```

Without the second spine, public context can support:

- demo engineering;
- source-semantic validation;
- exploratory regime analysis;

but not real production-forecast performance claims.

---

# 11. Recommended CS1 public-data work

Useful now:

1. build deterministic menu archive parser;
2. build announcement/regime-event parser;
3. build price-regime history;
4. build academic-calendar table;
5. version all source effective dates;
6. create schema ready for private target joins.

Do not spend time training a sophisticated model against synthetic/proxy labels and present it as cafeteria intelligence.

---

# 12. PMR/data-owner asks created by this research

## Food Services

- Is menu-vote history exportable by poll/date?
- Are tasting scores retained by menu item/service?
- Are satisfaction comments/results retained with timestamps?
- Which of these signals are actually consulted before production quantity is fixed?

## BİD / BUCampus / BUCard

- Can aggregate meal-window entry counts be exported historically?
- Can BUBizden daily entitlement/use counts be exported in aggregate?
- Can menu-vote counts be exported without user identity?
- What are retention and counting semantics?

---

## Current conclusion

Boğaziçi already has enough **public historical context** to build a serious temporal/regime data spine.

The missing problem is not lack of web data.

It is lack of **decision-level target and outcome data**.

That distinction should remain explicit in both the architecture and the KREATE narrative.
