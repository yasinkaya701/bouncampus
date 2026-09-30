# Boğaziçi Food-Service Source Reconciliation Matrix

**Research date:** 2026-10-01  
**Purpose:** Prevent agents from merging similarly named metrics, events or governance descriptions across official Boğaziçi sources without reconciling year, unit, scope, version and counting semantics.  
**Status:** Secondary/public-source research. This is a data-quality control artifact, not PMR or pilot evidence.

---

# 1. Why this exists

Official Boğaziçi sources are individually useful, but some fields that look comparable are **not safely interchangeable**. The correct response is not to pick a preferred number. Agents must preserve the disagreement and ask for a data dictionary or source-owner clarification when the difference matters.

Use this matrix before building datasets, calculating rates, writing application claims, choosing model targets or mapping decision authority.

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
| Reservation vs realized demand | 2024/2026 special-period announcements show explicit next-day meal requests through `kart.boun.edu.tr`. | 2026 holiday notice explicitly allows cancellation and says uncancelled meals not collected are still treated as taken for balance deduction; normal FAQ separately describes BUCard/QR turnstile access. | An active reservation is an intent/commitment event, not proof of physical service or consumption. A charged no-show can exist without a turnstile/service event. | Keep `reserved`, `cancelled`, `uncancelled_no_show`, `validated_entry/served` and `user_charge` as separate fields. Never train `served` labels from reservation counts without reconciliation. |
| Historical reservation threshold vs current policy | January 2024 inter-semester notice states **reservation counts below 15 → packaged service** for that regime. | Current normal-term public pages do not publish the same threshold as a universal operating rule. | The 15-person threshold is context-specific historical policy, not a timeless production constraint. | Store threshold with effective period/regime. Do not encode it into product logic until current operator confirms a rule. |
| User meal charge vs contractor settlement | BUCard/BUCampus sources describe student/personnel charging, balance deduction and payroll-linked meal charges. | Current 2026–2027 procurement is a unit-price contractor agreement, but public sources inspected so far do not establish which quantity becomes hakediş/payment. | A user's meal charge/subsidy accounting is a different money flow from contractor payment/acceptance. A no-show balance deduction does not prove contractor settlement. | Model `user_charge`, `university_subsidy/accounting` and `contract_settled_qty/value` separately. Do not derive contractor economics from BUCard prices. |
| Dining entry vs consumed meal | FAQ indicates date/time/campus/turnstile context exists for BUCard support and QR entry is supported. | No public source specifies retention, export schema, refunds, duplicate attempts or meal-consumption semantics. | `turnstile event` may not equal `meal served` one-to-one. | Request privacy-safe aggregates and reconciliation against serving counts before defining ground truth. |
| Default service hours vs actual service availability | General pages publish regular campus/meal windows. | Summer, holiday and inter-semester announcements suspend meals, change channels and introduce reservation/package regimes. | Calendar exceptions create structural zeros and regime shifts. | Build a service-availability/regime calendar from actual announcements; distinguish closed service from low demand. |
| Central production vs local capacity | Official sources state meals are produced in the North Campus central kitchen and distributed. | Dining-hall capacities are local seating/service constraints. | Production quantity and local seat capacity are different constraints; multiple seat turnovers occur in a meal window. | Do not cap predicted portions at seating capacity. Model campus allocation, meal window and turnover separately if needed. |
| Safe/sustainable food governance composition | Current impact/SDG pages describe a Safe and Sustainable Food Commission including appointed academics plus SKS, Food Services, Administrative & Financial Affairs and Deputy Secretary-General roles. | A publicly hosted 2024 draft/directive PDF version lists a broader composition including General Secretary, Support Services, **Corporate Data Management**, Asset Management, Food Services and **Control Organisation Coordinator**. | These may be different directive versions or draft/final structures. Treating the broader list as current without version confirmation can misroute interviews and overstate data-governance authority. | Cite the specific version/date. For current stakeholder routing, verify membership from a current university source/owner; use older/draft composition only as evidence that cross-unit data/governance was contemplated. |
| Control organisation existence vs decision authority | Current university commission page lists a **Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı** and current sustainability pages describe inspection of contractor food service. | Public pages emphasize quality, hygiene, standards and contract compliance; they do not say the control organisation sets daily production quantity. | Oversight/acceptance authority is not necessarily production-planning authority. | Interview Control Organisation for accepted records, service compliance, shortage handling and approval boundaries; do not label it quantity owner before PMR. |

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
9. 2024 inter-semester reservation/service-mode rule:  
   https://yemekhane.bogazici.edu.tr/ara-tatil-yemek-hizmeti-hakkinda
10. 2026 holiday reservation/no-show rule:  
   https://yemekhane.bogazici.edu.tr/node/493
11. Personnel meal accounting / BUCard detail:  
   https://yemekhane.bogazici.edu.tr/node/225
12. Current Control Organisation membership:  
   https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246
13. Current Safe and Sustainable Food Management policy surface:  
   https://impact.bogazici.edu.tr/1522-sustainably-farmed-food-campus
14. Publicly hosted 2024 safe/sustainable-food directive draft/version:  
   https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/bogazici_universitesi_guvenli_ve_surdurulebilir_gida_yonetimi_yonergesi_19_07_2024_-taslak.pdf
15. 2026–2027 Boğaziçi meal procurement:  
   https://ekapveri.com/ihale/ekap-2025-1727143/

---

# 4. Canonical ingestion rule for agents

Every imported field must carry at least:

```text
source_id
source_url
source_publication_or_measurement_year
source_version_or_effective_date
retrieved_at
metric_name_as_published
value
unit
period
population_or_scope
campus
meal_type
service_channel
service_regime
measurement_or_event_stage
counting_semantics
confidence
known_conflicts
```

If `unit`, `period`, `scope`, `version`, event stage or `counting_semantics` is unknown, preserve `UNKNOWN`. Do not infer it from neighboring fields.

---

# 5. Pilot ground-truth recommendation

The minimum clean operational table should be built around the **decision boundary**, not the sustainability-reporting boundary:

```text
DATE
CAMPUS
MEAL_TYPE
SERVICE_CHANNEL
SERVICE_REGIME
RESERVATIONS_CREATED
RESERVATIONS_CANCELLED
ACTIVE_RESERVATIONS_AT_CUTOFF
UNRESERVED_DEMAND
PLANNED_PORTIONS
PRODUCED_PORTIONS
SERVED_PORTIONS_OR_VALIDATED_ENTRY_COUNT
UNSERVED_EDIBLE_SURPLUS
PREPARATION_WASTE_KG
PLATE_WASTE_KG
OTHER_WASTE_KG
WASTE_DESTINATION
MENU_ID
USER_CHARGE_SEMANTICS
CONTRACT_SETTLED_QTY
DATA_SOURCE
```

Not every field must exist on day one. Missing fields should remain null with documented collection responsibility; they should not be reconstructed from incompatible annual/monthly public statistics.

---

# 6. Bottom line

The official sources are strong enough to establish **scale, governance, central production, digital service infrastructure, reservation capability, service-regime switching and a measured waste stream**. They are not yet internally consistent enough to serve as a single modeling or governance dataset.

For KREATE, that is not a weakness to hide. It is a concrete discovery: the first technical deliverable should include a **data-contract/reconciliation layer** so that Food Services, contractor, control organisation, BUCard/IT and model outputs refer to the same operational units, timestamps and versions.