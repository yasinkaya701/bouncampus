# VPMR Canonical Source Registry

**Access date for this initial pass:** 2026-10-06 unless stated otherwise.

Each source has a stable VPMR ID. IDs describe the source, not a conclusion. If a source materially changes, keep the old ID/history and add a dated successor rather than silently changing semantics.

## A. Boğaziçi official/public sources

| ID | Source | Class | What it can support | Critical boundary / note |
| --- | --- | --- | --- | --- |
| VPMR-SRC-001 | [Boğaziçi — Campus food waste tracking](https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310) | PUBLIC_CONTEXT | Official 2025 campus food-waste baseline, monthly values, reported service/capacity context | Total waste does not equal overproduction; stage/cause separation is not established |
| VPMR-SRC-002 | [Boğaziçi SKS — 2025 activity report](https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096) | PUBLIC_CONTEXT | Dining-hall count, daily meal scale, packaged-meal/public survey context | Published aggregates are not service-level labels |
| VPMR-SRC-003 | [Boğaziçi — Healthy and affordable food choices](https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314) | PUBLIC_CONTEXT | Central North Campus kitchen, menu/portion/nutrition preparation context | Does not establish daily quantity owner, freeze time or service-level truth |
| VPMR-SRC-004 | [Boğaziçi Dining — current menu](https://yemekhane.bogazici.edu.tr/) | PUBLIC_CONTEXT | Public pre-service menu composition, portions/calories when published | Menu is an input/context feature, not realized demand |
| VPMR-SRC-005 | [Boğaziçi Dining — Menu survey](https://yemekhane.bogazici.edu.tr/menu-anketi) | PUBLIC_CONTEXT | Authenticated preference-voting workflow and timing | Preference vote != attendance reservation != served meal |
| VPMR-SRC-006 | [Boğaziçi Dining — Kilyos reservation notice, 20 May 2026](https://yemekhane.bogazici.edu.tr/node/493) | PUBLIC_CONTEXT | Concrete evidence that one campus/time period used pre-service meal reservation and cancellation rules | Do not generalize the workflow/cutoff to other campuses or dates |
| VPMR-SRC-007 | [Boğaziçi academic calendar](https://akademiktakvim.bogazici.edu.tr/) | ARCHIVED_DECISION_INPUT | Pre-known academic regime/calendar features | Snapshot/version should be bound to the prediction date for historical evaluation |
| VPMR-SRC-008 | [Boğaziçi Dining FAQ](https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0) | PUBLIC_CONTEXT | Public clues about date/time/campus/turnstile context in payment/access troubleshooting | Does not prove retention, exportability, accessibility, cleanliness or equivalence to served meals |
| VPMR-SRC-009 | [BUCampus v1.1.2 announcement](https://bilgiislem.bogazici.edu.tr/tr/news/kampus/2/bucampusun-yeni-versiyonu-yayinda/3351) | PUBLIC_CONTEXT | Public clue that menu voting/results and calendar surfaces exist in BUCampus | Product surface != backend export/API access |
| VPMR-SRC-010 | [Boğaziçi 2025 Administration Activity Report PDF](https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf) | PUBLIC_CONTEXT | Contracted food-service governance/administrative context | PDF claims should be cited to exact page after human re-check before submission |

## B. Measurement and reporting standards

| ID | Source | Class | What it can support | Critical boundary / note |
| --- | --- | --- | --- | --- |
| VPMR-SRC-011 | [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024) | STANDARD_METHOD | International food-waste measurement/reporting methodology and food-service scope | Methodology does not provide a Boğaziçi outcome |
| VPMR-SRC-012 | [UNEP report repository/handle](https://wedocs.unep.org/handle/20.500.11822/45230) | STANDARD_METHOD | Stable report landing page and downloadable report | Prefer this or UNEP publication page over third-party copies |
| VPMR-SRC-013 | [Food Loss and Waste Accounting and Reporting Standard — WRI/FLW Protocol](https://www.wri.org/research/food-loss-and-waste-accounting-and-reporting-standard) | STANDARD_METHOD | Scope, inventory, reporting and comparability discipline | Standard compliance is not implied unless actually implemented |
| VPMR-SRC-014 | [FLW Standard — full PDF](https://flwprotocol.org/wp-content/uploads/2017/05/FLW_Standard_final_2016.pdf) | STANDARD_METHOD | Full methodology PDF; reusable reference under the publisher's stated license | Verify license/attribution before vendoring |
| VPMR-SRC-015 | [FLW Protocol — Guidance on Quantification Methods PDF](https://flwprotocol.org/wp-content/uploads/2017/06/FLW-Protocol_Guidance-on-FLW-Quantification-Methods.pdf) | STANDARD_METHOD | Weighing, counting, volume, waste-composition, records, diaries, surveys, mass-balance/model/proxy methods | Method selection must match pilot boundary and uncertainty |
| VPMR-SRC-016 | [WRAP — Measuring and reporting food waste in hospitality and food service](https://www.wrap.ngo/resources/guide/measuring-and-reporting-food-waste-hospitality-and-food-service) | STANDARD_METHOD | Practical hospitality/food-service measurement/reporting guidance and downloadable templates/PDFs | UK practice guidance; adapt to local operations |
| VPMR-SRC-017 | [US EPA — Wasted Food Scale](https://www.epa.gov/sustainable-management-food/wasted-food-scale) | STANDARD_METHOD | Prevention hierarchy; source reduction/prevention prioritized over downstream management | US policy graphic, not a local legal requirement or measured outcome |
| VPMR-SRC-018 | [US EPA — Resources for assessing wasted food](https://www.epa.gov/sustainable-management-food/resources-assessing-wasted-food) | STANDARD_METHOD | Practical assessment guides, logs and food-service measurement resources | Adapt field protocols to the local operational boundary |

## C. External evidence and analogues

| ID | Source | Class | What it can support | Critical boundary / note |
| --- | --- | --- | --- | --- |
| VPMR-SRC-019 | [Türker (2025), Sustainability — Reducing Food Waste in Campus Dining](https://www.mdpi.com/2071-1050/17/2/379) | ACADEMIC_ANALOGUE | Plausibility of campus demand/waste modeling using contextual signals | Reported model performance is not transferable to Boğaziçi |
| VPMR-SRC-020 | [Özokcu & Özdemir (2026) — Understanding drivers of consumer-level food waste in a university cafeteria](https://link.springer.com/article/10.1007/s44274-025-00509-y) | ACADEMIC_ANALOGUE | Turkish-university evidence on consumer-level food-waste drivers using survey + interviews | Consumer/plate-waste drivers are not automatically production-surplus drivers |
| VPMR-SRC-021 | [Özokcu & Özdemir — open PDF](https://link.springer.com/content/pdf/10.1007/s44274-025-00509-y.pdf) | ACADEMIC_ANALOGUE | Direct full-text PDF for review and exact citation | Preserve article license/attribution |
| VPMR-SRC-022 | [Every Plate Counts (2019), Resources Conservation & Recycling](https://doi.org/10.1016/j.resconrec.2019.104316) | ACADEMIC_ANALOGUE | Example of intervention evaluation with treatment/comparison dining halls and weighing | Intervention effect/context cannot be assumed at Boğaziçi |
| VPMR-SRC-023 | [Smaller servings vs information intervention (2020)](https://doi.org/10.1016/j.resconrec.2020.104786) | ACADEMIC_ANALOGUE | Portion-size intervention can be tested as a separate causal lever | Does not validate demand forecasting as the dominant lever |
| VPMR-SRC-024 | [Food Choice and Waste in University Dining Commons (2021)](https://www.mdpi.com/2071-1050/13/4/2129) | ACADEMIC_ANALOGUE | Multi-campus dining-waste observation and photo-based measurement analogue | External campus context only |
| VPMR-SRC-025 | [Plate Food Waste in Food Services — systematic review/meta-analysis (2024)](https://doi.org/10.3390/foods13111739) | ACADEMIC_ANALOGUE | Broad food-service plate-waste evidence and methodological context | Plate waste should not be conflated with unserved surplus |
| VPMR-SRC-026 | [Automated food-waste identification in university cafeterias (machine vision, 2025)](https://www.mdpi.com/2076-3417/15/4/1814) | ACADEMIC_ANALOGUE | Computer-vision feasibility analogue for TrayGate-like measurement | Requires local calibration/validation; pixels/classes are not certified mass |

## D. Decision-time data and external reference datasets

| ID | Source | Class | What it can support | Critical boundary / note |
| --- | --- | --- | --- | --- |
| VPMR-SRC-027 | [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) | ARCHIVED_DECISION_INPUT | Historical forecast snapshots that better represent what could have been known at the decision horizon | Do not use hindsight observations/reanalysis as if known at forecast cutoff |
| VPMR-SRC-028 | [Genpact Food Demand Forecasting dataset mirror](https://github.com/ashishpatel26/Food-Demand-Forecasting) | REFERENCE_DATASET | Sandbox demand-forecasting pipeline/schema practice | Not Boğaziçi, not university-specific ground truth, not waste labels, not PMR |

## E. Market-method reference tools

| ID | Source | Class | What it can support | Critical boundary / note |
| --- | --- | --- | --- | --- |
| VPMR-SRC-029 | [ReFED — Foodservice methodology](https://insights-engine.refed.org/methodology/foodservice) | STANDARD_METHOD | US foodservice surplus/waste methodology, equations, assumptions and data caveats | US-centric; use as method reference only |
| VPMR-SRC-030 | [ReFED Insights Engine](https://insights-engine.refed.org/) | PUBLIC_CONTEXT | Structured external benchmark/context and solutions research | Not local market validation |
| VPMR-SRC-031 | [ReFED Solutions Database](https://insights-engine.refed.org/solution-database) | PUBLIC_CONTEXT | Intervention catalogue and downloadable solution context | Evaluate local feasibility separately |

## Internal cross-reference artifacts

These are repo artifacts, not external evidence. They are valuable because other agents already did substantial research:

- Current master: `KREATE/RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md` — current evidence/product boundary.
- Issue #82 — CS1 service-truth acquisition contract and public source inventory.
- Archive branch `research/kreate-deep-pmr-market-20261004` — deep market/PMR synthesis, academic demand evidence, procurement, persona and beachhead research.
- Archive branch `research/kreate-evidence-20261005` — measurement standard, falsification matrix and information-value queue.
- Archive branch `research/kreate-contractor-gtm-clean-20261005` — contractor-led GTM and TEMAŞ PMR role map.
- Archive branch `agent/campus-data-geo/bogazici-pmr-target-map` — Boğaziçi operations/procurement/PMR target mapping.
- Archive branch `agent/decision-intelligence/cafeteria-data-research` — cafeteria data source manifests and modeling contracts.

Do not merge those stale branches wholesale. Recut only source-backed conclusions into current-master-compatible files and preserve their claim boundaries.
