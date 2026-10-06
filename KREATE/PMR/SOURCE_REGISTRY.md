# PMR Source Registry

**Updated:** 2026-10-06  
**Rule:** this is a cumulative secondary-source registry. It is not a count of completed PMR interviews.

## Field semantics

- **ID** — stable source identifier; never recycle an ID for a different source.
- **Class** — `PUBLIC SOURCE`, `ACADEMIC SOURCE`, `VENDOR SOURCE`, or `PUBLIC PROCUREMENT`.
- **Status** — `VERIFIED`, `CANDIDATE`, `STALE`, or `SUPERSEDED`.
- **Use** — the narrow question/claim the source can legitimately inform.
- **Does not prove** — the inference that must not be made.
- **Maps to** — PMR hypotheses: H1 control point, H2 mismatch, H3 shortage asymmetry, H4 data/measurement, H5 persona/authority, H6 workflow adoption; plus commercial/privacy/competition where relevant.

---

## A. Boğaziçi baseline and institutional context

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-BU-001 | PUBLIC SOURCE | VERIFIED | [Boğaziçi — Campus Food Waste Tracking](https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310) | Official university food-waste context, monthly 2025 waste table, dining-hall/service context, current waste-management actions. | That demand-forecast error caused the reported annual waste; service-level surplus; willingness to adopt BOUNCAMPUS. | H2, H4 |
| SRC-BU-002 | PUBLIC SOURCE | VERIFIED | [Boğaziçi 2025 food-waste XLSX](https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx) | Machine-readable/inspectable official waste artifact linked by the university page. | Meal-level causality, waste-stage split, produced/served counts or current quantity owner. | H2, H4 |
| SRC-BU-003 | PUBLIC SOURCE | VERIFIED | [Boğaziçi Sustainability Report 2025 PDF](https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/183-bogazici-university-sustainability-2025-yayin-20251104-115151.pdf) | Institutional sustainability context and source trail. | PMR, product demand, buyer authority, pilot permission. | H4, H5 |
| SRC-BU-004 | PUBLIC SOURCE | VERIFIED | [Boğaziçi Sustainability Reports index](https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063) | Canonical landing page for current/previous reports. | Any specific operational workflow not explicitly documented in a report. | H4 |
| SRC-BU-005 | PUBLIC SOURCE | VERIFIED | [Official cafeteria visual](https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155309.png) | Visual context only; useful in internal research/pitch source index. | Camera geometry, queue flow, waste stage or sensor feasibility without field validation. | H4 |

### Current Boğaziçi truth boundary

Public sources establish that food waste is measured/reported at institutional level and that dining operations exist at meaningful scale. They do **not** currently establish the decision owner, exact freeze point, batch flexibility, settlement basis, service-level waste stages, historical data accessibility, or product adoption. Those remain interview targets.

---

## B. PMR method and customer-discovery discipline

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-PMR-001 | PUBLIC SOURCE | VERIFIED | [Disciplined Entrepreneurship — Primary Market Research PDF](https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf) | Method basis for direct customer interaction, qualitative discovery and hypothesis testing. | Any BOUNCAMPUS market/customer conclusion. | H1–H6 |
| SRC-PMR-002 | PUBLIC SOURCE | VERIFIED | [Disciplined Entrepreneurship PMR step](https://www.d-eship.com/step1a/) | Current PMR guidance/entry point. | Product-market fit or evidence from a specific customer. | H1–H6 |
| SRC-PMR-003 | PUBLIC SOURCE | VERIFIED | [MIT Martin Trust Center — conducting primary market research](https://entrepreneurship.mit.edu/news/entrepreneurs-can-conduct-primary-market-research/) | Interview/research discipline and customer-learning framing. | A substitute for actual interviews. | H1–H6 |
| SRC-PMR-004 | PUBLIC SOURCE | VERIFIED | [MIT Sloan — Disciplined Entrepreneurship questions](https://mitsloan.mit.edu/ideas-made-to-matter/disciplined-entrepreneurship-6-questions-startup-success) | Customer-first venture framing and segmentation discipline. | Evidence for this market’s willingness to buy. | H5, H6 |

---

## C. Food-waste measurement and prevention standards

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-MEAS-001 | PUBLIC SOURCE | VERIFIED | [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024) | International measurement framework; food-service measurement methods and boundary discipline. | Which measurement method is feasible at Boğaziçi; local waste cause. | H2, H4 |
| SRC-MEAS-002 | PUBLIC SOURCE | VERIFIED | [UNEP Food Waste Index 2024 full PDF](https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf) | Direct PDF artifact for methodology review. | Validated TrayGate accuracy or a local pilot result. | H4 |
| SRC-MEAS-003 | PUBLIC SOURCE | VERIFIED | [US EPA Wasted Food Scale](https://www.epa.gov/sustainable-management-food/wasted-food-scale) | Prevention/source reduction hierarchy; upstream prevention framing. | That BOUNCAMPUS will reduce waste or emissions. | H2 |
| SRC-MEAS-004 | PUBLIC SOURCE | VERIFIED | [US EPA — prevent wasted food through source reduction](https://www.epa.gov/sustainable-management-food/prevent-wasted-food-through-source-reduction) | Operational prevention concepts. | Local causal effect or business case. | H2, H6 |
| SRC-MEAS-005 | PUBLIC SOURCE | VERIFIED | [US EPA — resources for assessing wasted food](https://www.epa.gov/sustainable-management-food/resources-assessing-wasted-food) | Practical measurement/audit guides and downloadable resources. | Site-specific measurement validity. | H4 |

Detailed interpretation already exists in [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md).

---

## D. Academic demand forecasting and food-waste evidence

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-ACAD-001 | ACADEMIC SOURCE | VERIFIED | [Turker (2025), Sustainability — campus dining demand prediction](https://doi.org/10.3390/su17020379) | Demonstrates use of campus entries, dining entries, weather, food/menu features and ML in university dining. | Transferable accuracy, savings or feature usefulness at Boğaziçi. | H2, H4 |
| SRC-ACAD-002 | ACADEMIC SOURCE | VERIFIED | [Rodrigues et al. (2024), Journal of Cleaner Production — catering demand forecasting](https://www.sciencedirect.com/science/article/pii/S0959652623044232) | Multi-site catering forecasting study; illustrates baseline comparison and modeled waste/unmet-demand trade-off. | Expected BOUNCAMPUS impact; local economics. | H2, H3, H6 |
| SRC-ACAD-003 | ACADEMIC SOURCE | VERIFIED | [Preventing food waste in subsidy-based university dining systems (2021), PubMed](https://pubmed.ncbi.nlm.nih.gov/33971773/) | Reservation/show/no-show and shortage/waste cost under uncertainty. | Boğaziçi’s actual reservation process, costs or achievable reduction. | H2, H3 |
| SRC-ACAD-004 | ACADEMIC SOURCE | VERIFIED | [Yemekhane için Yapay Zeka Teknikleri Kullanımı ile Günlük Talep Tahmini (2018)](https://dergipark.org.tr/tr/pub/ejosat/article/397549) | Turkish institutional precedent for daily meal-demand forecasting. | Novelty or current product demand. | H2 |
| SRC-ACAD-005 | ACADEMIC SOURCE | VERIFIED | [Machine Learning Techniques for Cafeteria Demand Forecasting: An Institutional Case (2025)](https://dergipark.org.tr/en/pub/opusjsr/article/1649256) | Recent institutional turnstile-based forecasting comparison. | Boğaziçi data availability or model promotion. | H2, H4 |
| SRC-ACAD-006 | ACADEMIC SOURCE | VERIFIED | [Understanding drivers of consumer-level food waste in a university cafeteria (2026)](https://link.springer.com/article/10.1007/s44274-025-00509-y) | Helps prevent over-attributing all food waste to forecasting; highlights consumer/meal-level drivers. | That the same drivers dominate Boğaziçi. | H2 |
| SRC-ACAD-007 | ACADEMIC SOURCE | VERIFIED | [Higher-education food-waste intervention systematic review (2024)](https://www.sciencedirect.com/science/article/pii/S2772912524000538) | Intervention landscape: awareness, trayless dining, portions and other strategies; emphasizes context/evaluation heterogeneity. | That forecasting is the best intervention at Boğaziçi. | H2, H6 |
| SRC-ACAD-008 | ACADEMIC SOURCE | VERIFIED | [University canteen portion/waste study (2024), Sustainability](https://www.mdpi.com/2071-1050/16/10/4317) | Direct weighing/portion context; reinforces waste-stage and portion-size alternative causes. | Local prevalence or causal ranking. | H2, H4 |
| SRC-ACAD-009 | ACADEMIC SOURCE | VERIFIED | [Machine-vision food-waste intervention in university cafeterias (2025)](https://www.mdpi.com/2076-3417/15/9/5036) | Comparison point for automated vision-based waste systems and privacy/design trade-offs. | That face-linked or identity-heavy sensing is appropriate for BOUNCAMPUS. | H4, privacy |
| SRC-ACAD-010 | ACADEMIC SOURCE | VERIFIED | [School catering forecasting / plate-tracking study](https://www.sciencedirect.com/science/article/pii/S0921344921006066) | Adjacent institutional evidence that forecasting/measurement can affect serving waste under the studied setting. | University-specific transferability or expected effect size. | H2, H4 |

---

## E. External university workflow archetypes and interview targets

These sources identify **sampling targets**, not PMR conclusions.

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-TGT-001 | PUBLIC SOURCE | VERIFIED | [İTÜ — Beslenme Hizmetleri](https://www.sks.itu.edu.tr/hizmetlerimiz/beslenme-hizmetleri) | Mature university dining operation, electronic identity-card dining automation, food-service governance; high-information second-site interview target. | That İTÜ has an unmet forecasting problem or would buy a tool. | H1, H4, H5, H6 |
| SRC-TGT-002 | PUBLIC SOURCE | VERIFIED | [Recep Tayyip Erdoğan University — meal reservation system](https://sks.erdogan.edu.tr/tr/news-detail/yemekhane-rezervasyon-sistemi/4787) | Concrete reservation-before-production archetype; useful for freeze-point and reservation-first PMR questions. | That Boğaziçi uses the same process. | H1, H2, H3 |
| SRC-TGT-003 | PUBLIC SOURCE | VERIFIED | [Kayseri University — meal reservation announcement (2026)](https://sksd.kayseri.edu.tr/tr/duyuru-detay/10301/yemekhane-rezervasyon-sistemi-duyurusu) | Current reservation-led planning archetype across campuses. | Local buyer economics or product demand. | H1, H2, H3 |
| SRC-TGT-004 | PUBLIC SOURCE | VERIFIED | [AFSÜ — reservation system information (2026)](https://skultur.afsu.edu.tr/ogrenciye-beslenme-hizmetleri-ve-rezervasyon-sistemi-hakkinda-bilgilendirme-yapildi/) | Weekly reservation/planning archetype and explicit resource-efficiency rationale. | That weekly reservation is suitable at Boğaziçi. | H1, H2, H6 |
| SRC-TGT-005 | PUBLIC SOURCE | VERIFIED | [Anadolu University — feeding opportunities](https://abp.anadolu.edu.tr/tr/ogrenci/beslenmeolanaklari) | Large-scale university dining + reservation-system context; potential comparative PMR site. | Exact decision rights, forecast error or willingness to adopt. | H1, H4, H5 |
| SRC-TGT-006 | PUBLIC SOURCE | VERIFIED | [Altınbaş University MyMeal](https://software.altinbas.edu.tr/mymeal/index_tr.html) | Existing university-developed meal reservation/tracking alternative; useful incumbent/status-quo comparison. | That MyMeal is deployed elsewhere or solves forecasting/waste causality. | competition, H6 |
| SRC-TGT-007 | PUBLIC SOURCE | VERIFIED | [İzmir Bakırçay University — Akıllı Kampüs Ara Raporu PDF](https://akilliuniversite.bakircay.edu.tr/Yuklenenler/Akilli_Universite/Sonuc%CC%A7_Raporu_20220428.pdf) | Public smart-campus artifact linking cafeteria utilization/reporting, food purchasing planning, occupancy/course/reservation signals. | That its architecture is current, transferable or a customer requirement. | H2, H4, competition |

When an institution is contacted, create a real tracker row/update and a dedicated interview record. Do not convert these rows into `COMPLETED` or `E-INT-*` evidence without a conversation.

---

## F. Competitors / alternatives

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-COMP-001 | VENDOR SOURCE | VERIFIED | [Winnow + Hilton — Winnow Foresight launch, 29 Sep 2026](https://www.winnowsolutions.com/resources/news/winnow-and-hilton-announce-winnow-foresight-a-mobile-first-ai-powered-forecasting-tool-designed-to-predict-kitchen-demand-and-prevent-food-waste) | Confirms current vendor positioning includes AI production forecasting; kills generic “nobody forecasts” novelty claim. | Independent performance, university fit or Turkish procurement fit. | competition, H6 |
| SRC-COMP-002 | VENDOR SOURCE | VERIFIED | [Winnow Foresight explainer](https://www.winnowsolutions.com/resources/news/introducing-winnow-foresight-a-new-way-to-prevent-food-waste-and-improve-guest-satisfaction-with-ai-powered-forecasting?hs_amp=true) | Item-level production-plan workflow and no-extra-hardware positioning in the described product. | Equivalent functionality in every segment/workflow. | competition |
| SRC-COMP-003 | VENDOR SOURCE | VERIFIED | [Leanpath — College & University](https://www.leanpath.com/industries/college-university/) | Current university food-waste offering; prevents unsafe novelty claims. | Independent outcome evidence or a precise feature-gap conclusion. | competition, H6 |
| SRC-COMP-004 | VENDOR SOURCE | VERIFIED | [Leanpath — Food Waste Tracking](https://www.leanpath.com/products/food-waste-tracking/) | Current measurement/analytics capability reference. | That Leanpath solves the exact pre-freeze decision at target sites. | competition |
| SRC-COMP-005 | VENDOR SOURCE | VERIFIED | [Emissary Campus](https://emissary.com.tr/tr/cozumler/emissary-campus) | Turkish university sustainability/data/audit platform; kills “first campus sustainability platform” framing. | Daily food-production decision depth or customer preference for BOUNCAMPUS. | competition, H6 |

Detailed red-team: [../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md).

---

## G. Privacy and data-minimization constraints

| ID | Class | Status | Source | Use | Does not prove | Maps to |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-PRIV-001 | PUBLIC SOURCE | VERIFIED | [KVKK — General Principles in Processing of Personal Data](https://www.kvkk.gov.tr/Icerik/6606/General-Principles-in-Processing-of-Personal-Data) | Data-minimization/proportionality design boundary. | Legal approval of any specific deployment; this repo is not legal advice. | H4, H6, privacy |
| SRC-PRIV-002 | PUBLIC SOURCE | VERIFIED | [KVKK — Obligation to Inform](https://www.kvkk.gov.tr/Icerik/6641/Obligation-to-inform) | Deployment/privacy checklist input. | That a specific notice/process is sufficient. | H4, H6, privacy |
| SRC-PRIV-003 | PUBLIC SOURCE | VERIFIED | [KVKK decision 2020/212 — camera/audio proportionality](https://www.kvkk.gov.tr/Icerik/6892/2020-212) | Supports camera-minimization and no-unnecessary-audio design posture. | Approval of TrayGate or a campus camera setup. | H4, privacy |
| SRC-PRIV-004 | PUBLIC SOURCE | VERIFIED | [KVKK — biometric-data processing guideline](https://www.kvkk.gov.tr/Icerik/7462/Guideline-on-Considerations-in-The-Processing-of-Biometric-Data) | Reinforces avoiding biometric shortcuts when aggregate/non-identifying signals suffice. | A legal opinion for a particular institution. | H4, privacy |

---

# Cross-source conclusions that are safe today

1. **Forecasting itself is not novel.** Academic papers, university systems and vendors already use reservations, history, calendar/context and ML.
2. **Food waste is multi-causal.** Demand mismatch is one candidate mechanism among portioning, menu preference, preparation/process loss and post-consumer behavior.
3. **Decision timing matters.** Reservation-first and replenishment archetypes imply the product must discover the real control point rather than assume one static prior-day forecast.
4. **Measurement boundary matters more than gadget sophistication.** A service-level matched pilot needs stable waste-stage/denominator semantics.
5. **Existing alternatives are strong.** Human judgment, spreadsheets, reservation systems, turnstile records, Leanpath/Winnow-like products and campus platforms are all part of the competitive set.
6. **Privacy burden can be reduced by design.** The first decision usually needs aggregate counts and service-level outcomes, not identity/biometrics.
7. **The remaining moat is a hypothesis.** University-specific context, source quality, explicit abstention, operator review, and decision→outcome verification matter only if PMR shows users/buyers care.

# Update rule

When adding a source:

1. search this file and `source_registry.json` for URL/title duplicates;
2. prefer official/primary publication over a secondary mirror;
3. add exact date/version when available;
4. state one narrow use and one explicit non-inference;
5. map it to a live question/hypothesis;
6. add PDF/XLSX/image to [ARTIFACT_INDEX.md](./ARTIFACT_INDEX.md) if present;
7. never mark public research as `INTERVIEW EVIDENCE`.
