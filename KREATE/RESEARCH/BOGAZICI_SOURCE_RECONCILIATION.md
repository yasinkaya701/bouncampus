# Boğaziçi Food-Service Source Reconciliation Matrix

**Research date:** 2026-10-01  
**Purpose:** Prevent agents from merging similarly named metrics across official Boğaziçi sources without reconciling year, unit, scope and counting semantics.  
**Status:** Secondary/public-source research. This is a data-quality control artifact, not PMR or pilot evidence.

---

# 1. Why this exists

Official Boğaziçi sources are individually useful, but some fields that look comparable are **not safely interchangeable**. The correct response is not to pick a preferred number. Agents must preserve the disagreement and ask for a data dictionary or source-owner clarification when the difference matters.

Use this matrix before building datasets, calculating rates, writing application claims or choosing model targets.

---

# 2. Reconciliation matrix

| Topic | Official source A | Official source B | Why they cannot be silently merged | Required action |
| --- | --- | --- | --- | --- |
| Dining-hall capacity | Sustainability food-waste page lists six halls totaling **1,734** seats/capacity units: North 660, South 159, Kilyos 118, Kandilli 200, Hisar 124, Anadolu Hisarı 473. | 2025 University Administration Activity Report Table 106 lists six halls totaling **1,652**: North 692, South 114, Hisar 118, Kandilli 120, Anadolu Hisarı 486, Sarıtepe 122. | Same concept name but materially different per-campus values and total. This may reflect source dates, renovations, room definitions, seating layouts or reporting basis. Public sources do not resolve the difference. | Store both with source/year fields. Do not use either as a hard model capacity constraint until owner confirms which layout applies to the pilot period. |
| Population served vs beneficiaries | Sustainability source says catering is provided for approximately **13,000 students + 2,000 staff**. | 2025 Administration Activity Report lists **17,466 students + 2,478 staff = 19,944 people benefiting from meal services**. | Campus population/service audience and annual beneficiary counts are not necessarily the same statistic. A person may be counted under eligibility/benefit semantics not represented by the approximate campus population statement. | Never compute participation rate by dividing these fields. Ask for unique diner definitions and observation period. |
| Daily meal scale vs annual servings | 2025 SKS activity report states **6,000 daily meals**. | 2024 SKS report lists 157,697 student breakfasts + 1,157,911 student meals + 96,838 staff meals = **1,412,446 reported servings** in the year. | Different years and denominators; `daily meals` may be planning capacity, average, working-day figure or another operational label. Annual servings include multiple categories and service days. | Keep as separate scale indicators. For forecasting, request timestamped actual served counts rather than derive daily demand from either figure. |
| Packaged meals | 2025 SKS Food Services section lists **2,000 packaged meals**. | Public packaged-menu pages and BUCampus announcement confirm packaged service exists but do not establish the denominator for the 2,000 figure. | `2,000` could be annual, period, capacity, distribution count or another measure; the public label alone is insufficient. | Mark unit/period `UNKNOWN`; ask Food Services before using the number in a claim or model. |
| Food waste vs İSTAÇ delivery | 2025 food-waste table reports monthly total food waste and says İSTAÇ-delivered waste is included in total. | August shows **1,502 kg total vs 3,550 kg delivered**; October **1,334 kg total vs 4,850 kg delivered**. | A same-month subset interpretation is mathematically impossible for these rows. Timing/backlog or semantic differences are possible but unconfirmed. | Do not calculate monthly recycling rates or train against these columns until generation-date vs collection-date semantics are documented. |
| Waste outcome boundary | Public sustainability pages publish university-level monthly food-waste totals. | Operational production decisions occur by campus, meal, batch and service channel. | Monthly university total may combine preparation waste, unserved food, plate waste and collection timing. It is too coarse to attribute to a production decision. | Forecast served demand first; measure pilot waste prospectively at the same campus × meal × decision boundary. |
| Menu preference vs demand | BUCampus/menu survey records votes for Wednesday lunch options. | BUCard/QR dining access is a separate service-entry mechanism. | A vote expresses preference; it does not establish attendance, campus, quantity or collection. | Treat vote totals as optional exogenous features only after out-of-sample ablation. Never use them as demand labels. |
| Dining entry vs consumed meal | FAQ indicates date/time/campus/turnstile context exists for BUCard support and QR entry is supported. | No public source specifies retention, export schema, refunds, duplicate attempts or meal-consumption semantics. | `turnstile event` may not equal `meal served` one-to-one. | Request privacy-safe aggregates and reconciliation against serving counts before defining ground truth. |
| Default service hours vs actual service availability | General pages publish regular campus/meal windows. | 2025 summer announcements suspended breakfast/dinner and weekend service for periods/campuses. | Calendar exceptions create structural zeros and regime shifts. | Build a service-availability calendar from actual announcements; distinguish closed service from low demand. |
| Central production vs local capacity | Official sources state meals are produced in the North Campus central kitchen and distributed. | Dining-hall capacities are local seating/service constraints. | Production quantity and local seat capacity are different constraints; multiple seat turnovers occur in a meal window. | Do not cap predicted portions at seating capacity. Model campus allocation, meal window and turnover separately if needed. |

---

# 3. Source references

1. Campus food waste tracking / sustainability dining capacities:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
2. 2025 University Administration Activity Report, including Table 106 and food-service beneficiary reporting:  
   https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf
3. 2025 SKS Activity Report:  
   https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
4. 2024 SKS Activity Report:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/303-2024-yili-faaliyet-raporu-yayin-20251205-150840.pdf
5. BUCampus/menu survey:  
   https://yemekhane.bogazici.edu.tr/menu-anketi
6. Dining FAQ / BUCard / QR:  
   https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
7. Summer service-regime announcement:  
   https://yemekhane.bogazici.edu.tr/yaz-donemi-yemek-hizmeti-hakkinda
8. Centralized food production / sustainable-food source:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313

---

# 4. Canonical ingestion rule for agents

Every imported field must carry at least:

```text
source_id
source_url
source_publication_or_measurement_year
retrieved_at
metric_name_as_published
value
unit
period
population_or_scope
campus
meal_type
service_channel
counting_semantics
confidence
known_conflicts
```

If `unit`, `period`, `scope` or `counting_semantics` is unknown, preserve `UNKNOWN`. Do not infer it from neighboring fields.

---

# 5. Pilot ground-truth recommendation

The minimum clean operational table should be built around the **decision boundary**, not the sustainability-reporting boundary:

```text
DATE
CAMPUS
MEAL_TYPE
SERVICE_CHANNEL
PLANNED_PORTIONS
PRODUCED_PORTIONS
SERVED_PORTIONS_OR_VALIDATED_ENTRY_COUNT
UNSERVED_EDIBLE_SURPLUS
PREPARATION_WASTE_KG
PLATE_WASTE_KG
OTHER_WASTE_KG
WASTE_DESTINATION
MENU_ID
SERVICE_REGIME
DATA_SOURCE
```

Not every field must exist on day one. Missing fields should remain null with documented collection responsibility; they should not be reconstructed from incompatible annual/monthly public statistics.

---

# 6. Bottom line

The official sources are strong enough to establish **scale, governance, central production, digital service infrastructure and a measured waste stream**. They are not yet internally consistent enough to serve as a single modeling dataset.

For KREATE, that is not a weakness to hide. It is a concrete discovery: the first technical deliverable should include a **data-contract/reconciliation layer** so that Food Services, contractor and model outputs refer to the same operational units.