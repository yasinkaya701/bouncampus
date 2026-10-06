# PMR Artifact Index

**Updated:** 2026-10-06  
**Purpose:** direct links to reusable PDFs, spreadsheets, images, reports and research artifacts that support PMR preparation.

## Repository policy

Default to **link + provenance + summary**, not copying third-party binaries into git.

Why:

- licenses/redistribution rights are often unclear;
- large PDFs/images bloat git history;
- the official URL preserves provenance and version context;
- some sources update over time.

Copy a binary into the repository only when redistribution rights are clear, the artifact is stable and essential for reproducibility, and the file size is reasonable. Otherwise keep the canonical link here.

For every copied artifact, record:

```text
source_id
original_url
publisher
retrieved_at
license_or_reuse_basis
sha256
local_path
notes
```

---

# 1. Boğaziçi official artifacts

## ART-BU-001 — 2025 food-waste spreadsheet

- **Source ID:** SRC-BU-002
- **Type:** XLSX
- **Canonical URL:** https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx
- **Landing page:** https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
- **Use:** official machine-readable/inspectable annual waste artifact.
- **Boundary:** not meal-level production, served demand, waste-stage or causal data.

## ART-BU-002 — Sustainability Report 2025

- **Source ID:** SRC-BU-003
- **Type:** PDF
- **Canonical URL:** https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/183-bogazici-university-sustainability-2025-yayin-20251104-115151.pdf
- **Index:** https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063
- **Use:** official institutional sustainability context and source trail.
- **Boundary:** secondary/public evidence, not PMR.

## ART-BU-003 — Official cafeteria visual

- **Source ID:** SRC-BU-005
- **Type:** PNG
- **Canonical URL:** https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155309.png
- **Landing page:** https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
- **Use:** visual context for internal research/pitch preparation.
- **Boundary:** do not infer camera placement, operational geometry or waste process from one image.

---

# 2. PMR methodology PDFs / guides

## ART-PMR-001 — Disciplined Entrepreneurship: Primary Market Research

- **Source ID:** SRC-PMR-001
- **Type:** PDF
- **URL:** https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf
- **Use:** interview design, qualitative discovery and falsification discipline.

## ART-PMR-002 — Current Disciplined Entrepreneurship PMR page

- **Source ID:** SRC-PMR-002
- **Type:** web guide
- **URL:** https://www.d-eship.com/step1a/
- **Use:** live methodology entry point.

---

# 3. Food-waste measurement standards / public guides

## ART-MEAS-001 — UNEP Food Waste Index Report 2024

- **Source ID:** SRC-MEAS-002
- **Type:** PDF
- **Direct PDF:** https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf
- **Landing page:** https://www.unep.org/resources/publication/food-waste-index-report-2024
- **Use:** measurement boundaries/methods for food service.
- **Local interpretation:** [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md)

## ART-MEAS-002 — US EPA Wasted Food Scale

- **Source ID:** SRC-MEAS-003
- **Type:** web + downloadable visual resources
- **URL:** https://www.epa.gov/sustainable-management-food/wasted-food-scale
- **Use:** prevention/source-reduction hierarchy and visual reference.
- **Rule:** link to official EPA visual assets rather than mirroring them unless reuse terms are checked.

## ART-MEAS-003 — US EPA assessment resources

- **Source ID:** SRC-MEAS-005
- **Type:** resource page + downloadable guides
- **URL:** https://www.epa.gov/sustainable-management-food/resources-assessing-wasted-food
- **Use:** practical audit/measurement documents.

---

# 4. Smart-campus / workflow PDFs

## ART-CAMPUS-001 — İzmir Bakırçay University Akıllı Kampüs Ara Raporu

- **Source ID:** SRC-TGT-007
- **Type:** PDF
- **URL:** https://akilliuniversite.bakircay.edu.tr/Yuklenenler/Akilli_Universite/Sonuc%CC%A7_Raporu_20220428.pdf
- **Use:** public example of cafeteria utilization, food-purchasing planning, course/reservation/occupancy signals within a university smart-campus program.
- **Boundary:** architecture/currentness/transferability must not be assumed.

---

# 5. Academic papers — direct reference set

These are primarily **method/mechanism references**, not customer evidence.

| Artifact | Source ID | Link | PMR use |
| --- | --- | --- | --- |
| Campus dining demand prediction | SRC-ACAD-001 | https://doi.org/10.3390/su17020379 | feature/data precedent; question whether those signals exist/usefully arrive before freeze |
| Catering short-term forecasting | SRC-ACAD-002 | https://www.sciencedirect.com/science/article/pii/S0959652623044232 | baseline/forecast utility and surplus-shortage trade-off |
| Subsidy-based university dining under uncertainty | SRC-ACAD-003 | https://pubmed.ncbi.nlm.nih.gov/33971773/ | reservation/no-show and asymmetric-cost interview prompts |
| Turkish daily meal-demand forecasting | SRC-ACAD-004 | https://dergipark.org.tr/tr/pub/ejosat/article/397549 | local institutional precedent |
| Institutional cafeteria demand forecasting | SRC-ACAD-005 | https://dergipark.org.tr/en/pub/opusjsr/article/1649256 | turnstile-based current-method precedent |
| Consumer-level university cafeteria waste drivers | SRC-ACAD-006 | https://link.springer.com/article/10.1007/s44274-025-00509-y | alternative-cause falsification |
| Higher-ed food-waste intervention review | SRC-ACAD-007 | https://www.sciencedirect.com/science/article/pii/S2772912524000538 | avoid forecasting monoculture |
| University canteen portion/waste study | SRC-ACAD-008 | https://www.mdpi.com/2071-1050/16/10/4317 | waste-stage/portion measurement prompts |
| Machine-vision cafeteria intervention | SRC-ACAD-009 | https://www.mdpi.com/2076-3417/15/9/5036 | CV comparison and privacy red-team |
| School catering forecasting / plate tracking | SRC-ACAD-010 | https://www.sciencedirect.com/science/article/pii/S0921344921006066 | adjacent mechanism precedent |

Do not copy publisher PDFs into git unless open-license/redistribution terms are explicitly verified.

---

# 6. Competitor/vendor visual and product references

Vendor material is useful for **novelty red-team and interview prompts**, not independent performance evidence.

## Winnow

- **Source IDs:** SRC-COMP-001, SRC-COMP-002
- Launch: https://www.winnowsolutions.com/resources/news/winnow-and-hilton-announce-winnow-foresight-a-mobile-first-ai-powered-forecasting-tool-designed-to-predict-kitchen-demand-and-prevent-food-waste
- Product explainer: https://www.winnowsolutions.com/resources/news/introducing-winnow-foresight-a-new-way-to-prevent-food-waste-and-improve-guest-satisfaction-with-ai-powered-forecasting?hs_amp=true
- **Use:** current visual/product reference for AI production forecasting; ask interviewees how their present workflow compares.

## Leanpath

- **Source IDs:** SRC-COMP-003, SRC-COMP-004
- College/university: https://www.leanpath.com/industries/college-university/
- Tracking products: https://www.leanpath.com/products/food-waste-tracking/
- **Use:** current food-waste measurement/analytics/incumbent comparison.

## Emissary Campus

- **Source ID:** SRC-COMP-005
- URL: https://emissary.com.tr/tr/cozumler/emissary-campus
- **Use:** Turkish university sustainability-data/evidence/audit comparison.

Detailed capability red-team:
[../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md)

---

# 7. External university workflow pages

These pages are valuable because they expose **different operational archetypes to sample through PMR**.

| Institution | Source ID | Public page | Why sample |
| --- | --- | --- | --- |
| İTÜ | SRC-TGT-001 | https://www.sks.itu.edu.tr/hizmetlerimiz/beslenme-hizmetleri | mature in-house/automated large-scale operation |
| RTEÜ | SRC-TGT-002 | https://sks.erdogan.edu.tr/tr/news-detail/yemekhane-rezervasyon-sistemi/4787 | reservation-before-production / explicit cutoff archetype |
| Kayseri University | SRC-TGT-003 | https://sksd.kayseri.edu.tr/tr/duyuru-detay/10301/yemekhane-rezervasyon-sistemi-duyurusu | current multi-campus reservation archetype |
| AFSÜ | SRC-TGT-004 | https://skultur.afsu.edu.tr/ogrenciye-beslenme-hizmetleri-ve-rezervasyon-sistemi-hakkinda-bilgilendirme-yapildi/ | weekly planning/reservation archetype |
| Anadolu University | SRC-TGT-005 | https://abp.anadolu.edu.tr/tr/ogrenci/beslenmeolanaklari | large-scale dining + reservation comparison |
| Altınbaş | SRC-TGT-006 | https://software.altinbas.edu.tr/mymeal/index_tr.html | university-developed incumbent alternative |

When a target becomes outreach/scheduled/completed, update [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md). A public page alone never changes a tracker row to `COMPLETED`.

---

# 8. Privacy/legal design references

These are product-design boundaries, **not legal advice**.

- [SRC-PRIV-001 — KVKK general principles](https://www.kvkk.gov.tr/Icerik/6606/General-Principles-in-Processing-of-Personal-Data)
- [SRC-PRIV-002 — obligation to inform](https://www.kvkk.gov.tr/Icerik/6641/Obligation-to-inform)
- [SRC-PRIV-003 — camera/audio proportionality decision](https://www.kvkk.gov.tr/Icerik/6892/2020-212)
- [SRC-PRIV-004 — biometric-data guideline](https://www.kvkk.gov.tr/Icerik/7462/Guideline-on-Considerations-in-The-Processing-of-Biometric-Data)

Use these to bias V1 toward aggregate service-level signals, bounded camera FOV, no biometrics, minimal raw-data retention and institution-reviewed deployment.

---

# 9. Artifact acquisition queue

Only acquire/copy into repo if it materially improves reproducibility.

| Priority | Artifact | Action | Owner lane |
| --- | --- | --- | --- |
| P0 | Boğaziçi 2025 waste XLSX | inspect schema/units and record checksum if used analytically | CS2/CS1 |
| P0 | real interview notes/artifacts | store using PMR template; redact only as agreed with interviewee | IE + interviewer |
| P0 | service-level export sample | obtain from authorized owner; document field semantics | IE/CS1 |
| P1 | official detailed procurement/tender mechanics | link authoritative clause/page; extract only narrow mechanics | IE/CS2 |
| P1 | UNEP/EPA measurement guide used by pilot | pin exact version/date | EE/CS2 |
| P1 | competitor screenshots/visuals | prefer links; use only for internal comparison unless reuse is allowed | CS2 |
| P2 | papers/reference PDFs | keep DOI/landing links unless open license clearly permits repository copy | all |

---

# 10. Visual-use rule for pitch/application

A visual may be used only when its provenance and meaning are clear.

For each visual used outside this index, annotate internally:

```text
visual_id
source_id
source_url
publisher
what_the_visual_shows
what_we_are_not_inferring
reuse_status
```

Do not use a source image as decoration if it implies a measurement/result BOUNCAMPUS has not produced.
