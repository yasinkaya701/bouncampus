# Boğaziçi Public Waste-Stage Gap — 2026-10-04

**Purpose:** document exactly what public Boğaziçi waste sources can and cannot establish about the causal stage of the reported food-waste total.  
**Status:** public-source reconciliation. **Absence of a public stage split is not proof that internal stage-level records do not exist.**

## Executive conclusion

After targeted review of current official Boğaziçi food-waste, Zero Waste and dining sources, the public 2025 food-waste total **cannot be decomposed** into the operational stages required to validate BOUNCAMPUS's production-planning hypothesis.

The public evidence supports:

- a 2025 total food-waste quantity;
- monthly total food-waste reporting;
- recovery / İSTAÇ-related quantities;
- institutional waste-separation categories such as cooked-food leftovers, bread and organic waste.

It does **not** publicly expose a service-level split of:

```text
preparation/process waste
unserved edible production surplus
plate/post-consumer waste
```

Therefore the published **48,251 kg** must not be used as a model target or treated as `overproduction waste`.

---

# 1. Current official 2025 food-waste page

Official Boğaziçi source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

The page reports:

- total 2025 food waste: **48,251 kg**;
- monthly `Total Food Waste` values;
- amounts delivered to İSTAÇ for recycling;
- waste-oil quantities.

### What is missing publicly

The table does not identify whether one kilogram came from:

- trimming/preparation;
- cooked food never served;
- service-line surplus;
- food returned on plates/trays;
- food discarded for quality/safety reasons;
- another food-waste pathway.

### Claim rule

Safe:
> Boğaziçi publicly reports 48,251 kg total food waste in 2025.

Unsafe:
> Boğaziçi overproduced 48,251 kg of food in 2025.

Unsafe:
> demand forecasting caused/could prevent the published total.

---

# 2. Zero Waste dining categories are collection categories, not causal stages

Boğaziçi's Zero Waste report describes cafeteria waste separation categories including:

- organic waste such as egg shells and fruit/vegetable peels;
- bread scraps;
- `yemek artıkları (pişmiş yemekler)` / cooked-food leftovers;
- recyclable/non-recyclable streams.

Official report:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Assets/R8_Ministry_Bogazici_University_Zero_Waste_Report.pdf

### Important semantic boundary

`cooked-food leftovers` is not equivalent to:

```text
unserved edible surplus
```

because the same collection stream may contain food from different operational stages depending on local collection practice.

Similarly:

```text
organic waste
```

can include unavoidable preparation material and should not automatically be classified as avoidable food waste.

---

# 3. Sustainability reporting shows downstream routes, not production causality

Boğaziçi's environmental sustainability reporting shows downstream pathways for streams such as:

- food leftovers;
- bread leftovers;
- compostable organic material;
- waste oil.

Official sustainability-report source:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Assets/Documents/Dosyalar/2024_bogazici_universitesi_cevresel_surdurulebilirlik_raporu_2.pdf

This supports the existence of organized recovery/diversion pathways.

It does not identify:

- the original meal/service;
- the production quantity;
- whether the food was ever served;
- whether the waste was avoidable;
- why it became waste.

---

# 4. Existing public dining-quality mechanisms make stage attribution more important

Boğaziçi also publicly operates:

- pre-service tasting;
- menu preference voting;
- satisfaction/feedback channels;
- portion/quality control processes.

These create plausible non-forecast explanations for some waste, including:

- menu acceptance;
- taste/quality;
- portion size;
- preparation/service issues.

See:
`BOGAZICI_FEEDBACK_AND_ALTERNATIVE_ROOT_CAUSE_SIGNALS_2026-10-04.md`.

### Research implication

The annual total alone cannot tell us whether the highest-value intervention is:

```text
production quantity
campus allocation
batch release
portion size
menu design
quality/process control
```

---

# 5. Required minimum stage schema for PMR/pilot

The target data owner should be asked whether the following are recorded separately:

```text
service_id
service_date
campus
meal_period
planned_quantity
produced_quantity
served_quantity

prep_waste_kg
unserved_edible_surplus_kg
plate_waste_kg
other_food_waste_kg

measurement_method
measurement_time
collection_point
reuse_or_donation_quantity
compost_quantity
other_disposition
```

If internal records do not provide this split, the first pilot must instrument it manually before claiming a causal reduction.

---

# 6. Interview questions for the authoritative waste owner

- What exactly enters `Total Food Waste` in the 2025 public table?
- At which physical collection points is it weighed?
- Is the date a generation date, pickup date or accounting date?
- Are kitchen/preparation and dining-room/tray streams weighed separately?
- Is cooked but unserved food separately counted before disposal/donation?
- Are donated/reused portions excluded from the waste total or recorded elsewhere?
- Is plate waste distinguishable from service-line surplus?
- Is there campus-level or meal-level granularity internally?
- Which scale/device/process produces the authoritative figure?
- Can a pilot create a temporary stage-separated measurement process?

---

# 7. Modeling consequence

Before stage-level operational labels exist:

- public annual/monthly waste may be used as **problem context**;
- public waste must not be used as a supervised target for next-service production forecasting;
- model training needs actual `served demand` or equivalent decision-level target;
- impact evaluation needs physical stage-specific measurement.

The minimum safe chain is:

```text
planned/produced
-> served
-> unserved edible surplus
-> plate/prep waste separately
```

not:

```text
public monthly waste total
-> infer daily demand error
```

---

# 8. Evidence-state consequence

This research **does not reject** H-B (material decision-linked mismatch).

It establishes that public evidence is insufficient to support H-B at Boğaziçi.

Current state remains:

```text
H-B = UNKNOWN / TESTING
```

Required promotion evidence:

- real operator incident(s);
- stage-separated waste/surplus records or pilot measurement;
- reachable prior decision that could have changed the outcome.

---

## Current conclusion

The 48,251 kg figure is valuable because it proves a material institutional food-waste stream exists.

Its greatest current methodological value is **problem scale**, not a machine-learning label and not proof of overproduction.

The next decisive evidence must come from the waste-data owner and daily production workflow, not another interpretation of the annual public total.
