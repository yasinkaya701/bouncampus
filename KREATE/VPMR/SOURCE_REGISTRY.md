# VPMR Canonical Source Registry

**Curated:** 2026-10-06

Every row below has the same stable ID and core semantics as `source_registry.json`. Direct PDFs, graphics and alternate download URLs are also indexed in `VISUALS_AND_PDFS.md`.

Public, academic and standards sources are **not PMR/customer validation**. They can verify public facts, constrain hypotheses, identify targets and shape measurement/technical methods.

## A. Official/public context and procurement precedents

| ID | Source | Publisher | What it can support | Critical boundary |
| --- | --- | --- | --- | --- |
| VPMR-SRC-001 | [Campus food waste tracking](https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310) | Boğaziçi University | official campus food-waste baseline; monthly aggregate context | service-level overproduction labels; causal attribution of waste |
| VPMR-SRC-002 | [2025 SKS activity report](https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096) | Boğaziçi University SKS | dining operation scale; public aggregate meal/dining-hall context | campus-meal service truth |
| VPMR-SRC-003 | [Healthy and affordable food choices](https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314) | Boğaziçi University | central-kitchen context; portion/nutrition planning context | quantity decision owner; freeze time; service-level outcome |
| VPMR-SRC-004 | [Dining menu](https://yemekhane.bogazici.edu.tr/) | Boğaziçi University | public menu context | realized demand |
| VPMR-SRC-005 | [Menu survey](https://yemekhane.bogazici.edu.tr/menu-anketi) | Boğaziçi University | menu preference workflow | attendance reservation; served demand |
| VPMR-SRC-006 | [Kilyos meal reservation notice (20 May 2026)](https://yemekhane.bogazici.edu.tr/node/493) | Boğaziçi University | existence of a reservation workflow for the cited campus/period | universal reservation policy |
| VPMR-SRC-008 | [Dining FAQ](https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0) | Boğaziçi University | public clues about date/time/campus/turnstile context | data access; retention; served-meal equivalence |
| VPMR-SRC-009 | [BUCampus v1.1.2 announcement](https://bilgiislem.bogazici.edu.tr/tr/news/kampus/2/bucampusun-yeni-versiyonu-yayinda/3351) | Boğaziçi University IT | existence of menu voting/calendar product surfaces | backend export/API availability |
| VPMR-SRC-010 | [2025 Administration Activity Report](https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu(3).pdf) | Boğaziçi University | administrative/contracted service context | daily quantity semantics without exact clause/owner verification |
| VPMR-SRC-027 | [Insights Engine](https://insights-engine.refed.org/) | ReFED | external benchmark/solution context | local market validation |
| VPMR-SRC-028 | [Solutions Database](https://insights-engine.refed.org/solution-database) | ReFED | intervention landscape | local implementation feasibility |
| VPMR-SRC-030 | [KİK 2026/UH.I-2269 — Kırıkkale University Malzemeli Yemek Hizmeti](https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b) | Kamu İhale Kurumu / EKAP | official Turkish university procurement precedent where contractor determines daily quantity using prior meal counts; payment based on actually consumed meals; administration not responsible for excess production; shortage and demand-variation risk can be contractually asymmetric | Boğaziçi/TEMAŞ contract semantics; Boğaziçi buyer or decision owner |
| VPMR-SRC-031 | [KİK university dining precedent — production quantity and turnstile-based payment](https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=9611128e0826cb5014a4ac6f4dfc5a19d9efd22c609d58c78f14a636b0ac7250&KararMetni=bc6844c56eeb209fc60f05e3a7cc8b7abfe3b86dc04f193fe56fbb6d02a60da7) | Kamu İhale Kurumu / EKAP | official precedent where daily production quantity is set by contractor with administration approval and notified at least one day before; turnstile/mobile/ticket records can be settlement inputs | Boğaziçi event semantics; claim that one passage always equals one consumed meal in Boğaziçi |
| VPMR-SRC-032 | [İTÜ SAY Sistemi Rezervasyon İşlemi Detayları](https://sksv2.mozaik-test.itu.edu.tr/docs/librariesprovider73/default-document-library/it%C3%BC-say-sistemi-kullan%C4%B1m-detaylar%C4%B1.pdf?sfvrsn=0) | İstanbul Technical University | reservation-to-production planning precedent; published 48-hour preparation constraint; day/cafeteria/meal reservation semantics | current Boğaziçi reservation coverage; Boğaziçi freeze time |
| VPMR-SRC-033 | [İTÜ food-waste prevention and production-planning program](https://sustainability.itu.edu.tr/tr/itu-kafeteryalari-ve-yemek-hizmetleri-gida-israfini-onlemeye-yonelik-ozel-programlar-saglamaktadir) | İstanbul Technical University | Turkish university precedent using academic calendar, course/exam schedule, menu options, weather and historical meal counts in production estimation; documented replenishment/contingency behavior | Boğaziçi feature value; Boğaziçi current heuristic |
| VPMR-SRC-034 | [GTÜ dining services — production planning and unexpected demand](https://www.gtu.edu.tr/kategori/5904/0/display.aspx) | Gebze Technical University | current 2026 Turkish university precedent using historical consumption and daily user counts in production planning; early sell-out and rapid replenishment as an operational shortage pattern | Boğaziçi workflow; Boğaziçi willingness to pay |

## B. Measurement, policy and reporting methods

| ID | Source | Publisher | What it can support | Critical boundary |
| --- | --- | --- | --- | --- |
| VPMR-SRC-011 | [Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024) | UNEP | food-service measurement methodology; global reporting context | Boğaziçi measured result |
| VPMR-SRC-012 | [Food Loss and Waste Accounting and Reporting Standard](https://www.wri.org/research/food-loss-and-waste-accounting-and-reporting-standard) | WRI / FLW Protocol | inventory scope/boundary/reporting discipline | claim of implementation/compliance |
| VPMR-SRC-013 | [Guidance on FLW Quantification Methods](https://flwprotocol.org/wp-content/uploads/2017/06/FLW-Protocol_Guidance-on-FLW-Quantification-Methods.pdf) | FLW Protocol | measurement method selection | local measurement result |
| VPMR-SRC-014 | [Measuring and reporting food waste in hospitality and food service](https://www.wrap.ngo/resources/guide/measuring-and-reporting-food-waste-hospitality-and-food-service) | WRAP | practical measurement/reporting protocol design | Boğaziçi result |
| VPMR-SRC-015 | [Wasted Food Scale](https://www.epa.gov/sustainable-management-food/wasted-food-scale) | US EPA | prevention hierarchy | Turkish legal mandate; Boğaziçi outcome |
| VPMR-SRC-016 | [Resources for Assessing Wasted Food](https://www.epa.gov/sustainable-management-food/resources-assessing-wasted-food) | US EPA | practical assessment/log design | local measured outcome |
| VPMR-SRC-026 | [Foodservice methodology](https://insights-engine.refed.org/methodology/foodservice) | ReFED | US foodservice surplus/waste methodology reference | local customer validation |
| VPMR-SRC-029 | [Otel, Restoran ve Diğer Toplu Tüketim Yerlerinde Gıda İsrafı ile Mücadele Kılavuzu](https://www.tarimorman.gov.tr/abdgm/link/68/yayinlarimiz) | T.C. Tarım ve Orman Bakanlığı / FAO / Metro Türkiye | Türkiye-specific institutional food-service waste prevention context; separation/measurement/planning/service prevention practices | Boğaziçi measured outcome; proof that forecast error is the dominant local waste cause |

## C. Academic and external mechanism analogues

| ID | Source | Publisher | What it can support | Critical boundary |
| --- | --- | --- | --- | --- |
| VPMR-SRC-017 | [Reducing Food Waste in Campus Dining: A Data-Driven Approach](https://www.mdpi.com/2071-1050/17/2/379) | MDPI Sustainability | technical plausibility of contextual campus modeling | expected Boğaziçi model score; local causal effect |
| VPMR-SRC-018 | [Understanding the drivers of consumer level food waste in a university cafeteria](https://link.springer.com/article/10.1007/s44274-025-00509-y) | Springer | Turkish university consumer-level driver analogue | production-surplus causal claim |
| VPMR-SRC-019 | [Every plate counts: Evaluation of a food waste reduction campaign](https://doi.org/10.1016/j.resconrec.2019.104316) | Resources, Conservation & Recycling | campus intervention-evaluation analogue | Boğaziçi intervention effect |
| VPMR-SRC-020 | [Smaller servings vs information intervention](https://doi.org/10.1016/j.resconrec.2020.104786) | Resources, Conservation & Recycling | alternative causal lever: portion size | forecasting as dominant lever |
| VPMR-SRC-021 | [Food Choice and Waste in University Dining Commons](https://www.mdpi.com/2071-1050/13/4/2129) | MDPI Sustainability | multi-campus dining-waste observation analogue | local operational semantics |
| VPMR-SRC-022 | [Plate Food Waste in Food Services: systematic review/meta-analysis](https://doi.org/10.3390/foods13111739) | MDPI Foods | broad food-service plate-waste context | unserved surplus equivalence |
| VPMR-SRC-023 | [Automated food waste identification in university cafeterias using machine vision](https://www.mdpi.com/2076-3417/15/4/1814) | MDPI Applied Sciences | computer-vision measurement feasibility analogue | certified local mass measurement |
| VPMR-SRC-035 | [Machine learning models for short-term demand forecasting in food catering services](https://www.sciencedirect.com/science/article/pii/S0959652623044232) | Journal of Cleaner Production / Elsevier | multi-canteen catering demand-forecasting precedent; need to compare ML against operational/baseline forecasts; joint surplus and unmet-demand evaluation | transfer of reported waste-reduction percentages to Boğaziçi; local model utility before admitted service truth |
| VPMR-SRC-036 | [Demand Forecasting for Food Production Using Machine Learning Algorithms: A Case Study of University Refectory](https://hrcak.srce.hr/en/clanak/446387) | Technical Gazette / Hrčak | university-refectory demand forecasting precedent; calendar and meal-ingredient features as candidate inputs | Boğaziçi performance; novelty claim for calendar/menu-aware forecasting |
| VPMR-SRC-037 | [Machine Learning Techniques for Cafeteria Demand Forecasting: An Institutional Case](https://dergipark.org.tr/en/pub/opusjsr/article/1649256) | OPUS Journal of Society Research / Dergipark | institutional turnstile-demand forecasting precedent; multi-resolution demand modeling precedent | Boğaziçi turnstile access or field semantics; transfer of reported metrics/impact |

## D. Decision-time external inputs

| ID | Source | Publisher | What it can support | Critical boundary |
| --- | --- | --- | --- | --- |
| VPMR-SRC-007 | [Academic calendar](https://akademiktakvim.bogazici.edu.tr/) | Boğaziçi University | calendar/regime features known in advance | demand outcome |
| VPMR-SRC-024 | [Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api) | Open-Meteo | historical forecast input known at a decision horizon | hindsight actual weather masquerading as forecast |

## E. Reference datasets

| ID | Source | Publisher | What it can support | Critical boundary |
| --- | --- | --- | --- | --- |
| VPMR-SRC-025 | [Food Demand Forecasting dataset mirror](https://github.com/ashishpatel26/Food-Demand-Forecasting) | GitHub community mirror / Genpact challenge data | sandbox forecasting pipeline tests | Boğaziçi model performance; waste labels; PMR |

## Internal cross-reference artifacts

- Issue #82 — current CS1 service-truth acquisition contract.
- Issue #317 — VPMR cross-agent intake/coordination.
- `KREATE/PMR/` — parallel PMR source library, claim-source matrix, asset manifest and interview execution surfaces.
- Archive research branches listed in `AGENT_HANDOFF.md` — selective source salvage only; never wholesale-merge stale shared state.

## Registry rule

Do not assign a new ID to a PDF merely because it is an alternate representation of the same source. Put alternate PDF/data/visual URLs in the JSON source record and `VISUALS_AND_PDFS.md`. Create a new source ID only when the artifact has materially distinct provenance or claim semantics.
