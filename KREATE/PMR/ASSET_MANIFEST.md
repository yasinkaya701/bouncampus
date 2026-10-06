# PMR Asset / PDF / Visual Manifest

**Updated:** 2026-10-06  
**Purpose:** Keep reusable research assets discoverable without copying copyrighted material into the repository blindly.

## Policy

Default to **link + metadata**, not binary duplication.

A file may be copied into the repository only when:
1. the reuse/license terms are clear enough for this public repository;
2. attribution requirements are recorded;
3. the original URL and access date are preserved;
4. a SHA-256 checksum is recorded after download;
5. the binary adds real offline/reproducibility value.

Statuses:
- `LINK_ONLY` — preserve external link; do not copy without further rights review.
- `COPY_ALLOWED_WITH_ATTRIBUTION` — license/reuse appears compatible; attribution still required.
- `COPY_CANDIDATE` — likely reusable but verify exact asset/page terms before committing binary.
- `INTERNAL_PROVENANCE` — GitHub branch/PR reference, not an external asset.

| ID | Asset | Direct link | Format | Status | Attribution / reuse note | Repo role |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | Disciplined Entrepreneurship PMR guide | https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf | PDF | LINK_ONLY | Publicly accessible; reuse terms not established here | Interview-method reference |
| A-002 | UNEP Food Waste Index Report 2024 | https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf | PDF | LINK_ONLY | UNEP report includes reproduction conditions; keep linked unless repository-use terms are reviewed for the exact use | Measurement methodology |
| A-003 | FLW Accounting & Reporting Standard | https://flwprotocol.org/wp-content/uploads/2017/05/FLW_Standard_final_2016.pdf | PDF | COPY_ALLOWED_WITH_ATTRIBUTION | WRI/FLW Protocol identifies Creative Commons reuse; preserve exact attribution/license | Measurement/accounting standard |
| A-004 | EPA Wasted Food Scale graphics | https://www.epa.gov/sustainable-management-food/wasted-food-scale-graphics | PNG/SVG download page | COPY_CANDIDATE | EPA page provides graphics for reuse; credit U.S. EPA and verify the chosen asset variant | Presentation / prevention hierarchy visual |
| A-005 | İTÜ reservation-system guide | https://sksv2.mozaik-test.itu.edu.tr/docs/librariesprovider73/default-document-library/it%C3%BC-say-sistemi-kullan%C4%B1m-detaylar%C4%B1.pdf?sfvrsn=0 | PDF | LINK_ONLY | Official-hosted document; reuse license not established | Reservation workflow precedent |
| A-006 | Faezirad et al. university-dining optimization paper | https://ris.utwente.nl/ws/files/266946365/Faezirad_2021_Preventing_food_waste_in_subsidy_ba.pdf | PDF | LINK_ONLY | Open repository copy; verify publication/repository license before redistributing | Asymmetric waste/shortage research |
| A-007 | Türker 2025 campus dining paper | https://www.mdpi.com/2071-1050/17/2/379/pdf | PDF | COPY_ALLOWED_WITH_ATTRIBUTION | MDPI article is open access under CC BY; retain author/title/DOI/license attribution | Context-feature benchmark |
| A-008 | Acı & Yergök 2023 article page / PDF entry | https://hrcak.srce.hr/en/clanak/446387 | HTML/PDF link | LINK_ONLY | Repository/journal reuse terms should be checked before binary redistribution | Calendar/menu forecasting precedent |
| A-009 | Boğaziçi 2025 food-waste data page | https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310 | HTML/data table | LINK_ONLY | Official source; preserve retrieval date and table semantics | Public problem-scale context |
| A-010 | Boğaziçi SKS 2025 activity report page | https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096 | HTML/report page | LINK_ONLY | Official source | Dining scale / operating context |
| A-011 | Winnow Foresight announcement | https://www.winnowsolutions.com/resources/news/introducing-winnow-foresight-a-new-way-to-prevent-food-waste-and-improve-guest-satisfaction-with-ai-powered-forecasting | HTML/images | LINK_ONLY | Vendor content; do not copy screenshots/logos without permission | Competitive red-team |
| A-012 | stale agent PMR target-map branch | https://github.com/yasinkaya701/bouncampus/tree/agent/campus-data-geo/bogazici-pmr-target-map | Git branch | INTERNAL_PROVENANCE | Internal repository history | Selective source/target salvage |
| A-013 | stale deep PMR/market branch | https://github.com/yasinkaya701/bouncampus/tree/research/kreate-deep-pmr-market-20261004 | Git branch | INTERNAL_PROVENANCE | Internal repository history | Research backlog / selective salvage |
| A-014 | merged PMR/market red-team PR #213 | https://github.com/yasinkaya701/bouncampus/pull/213 | Git PR | INTERNAL_PROVENANCE | Merged repository provenance | Current-master research lineage |\n| A-015 | Boğaziçi 2026–2027 academic calendar | https://intl.bogazici.edu.tr/sites/intl.bogazici.edu.tr/files/academic_calendar_2026-2027.pdf | PDF | LINK_ONLY | Official university PDF; redistribution terms not established here | Versionable calendar/context feature reference |
| A-016 | Boğaziçi SDG-2 sustainability report | https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/18--yayin-20250910-094806.pdf | PDF | LINK_ONLY | Official university media-store report; prefer project-redrawn charts from cited values | Local sustainability / dining visual reference |
| A-017 | Fatemi et al. 2024 campus-canteen intervention | https://link.springer.com/article/10.1186/s40066-024-00488-y | HTML/PDF | COPY_CANDIDATE | Open-access article; verify figure-specific credits before reuse | Root-cause / direct-weighing visual and pilot-method precedent |
| A-018 | Türkiye Ministry mass-catering hygiene guidance | https://www.tarimorman.gov.tr/GKGM/Menu/132/ | HTML/PDF index | LINK_ONLY | Government official index; use current linked guide and retain source/version | Safety/operating guardrail reference |
| A-019 | Boğaziçi student events calendar | https://takvim.bogazici.edu.tr/tr/events/students | HTML | LINK_ONLY | Official source; event presence ≠ attendance magnitude | Public event/context signal reference |

| A-020 | Boğaziçi 2024 food-waste report | https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2024_bu.pdf | PDF | LINK_ONLY | Official one-page university report; preserve source URL/date | Historical public data context |
| A-021 | Boğaziçi 2025 food-waste source workbook | https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx | XLSX | LINK_ONLY | Official linked workbook; preserve raw semantics and do not silently normalize | Current public raw-source context |
| A-022 | Türkiye toplu tüketim gıda-israfı kılavuzu | https://www.tarimorman.gov.tr/ABDGM/BelgelerArsiv/Belgeler/Uluslararas%C4%B1%20Kurulu%C5%9Flar/gastro-bakanlik-kilavuzu.pdf | PDF | LINK_ONLY | T.C. Tarım ve Orman Bakanlığı / FAO / Metro Türkiye; verify reuse terms before copying | Türkiye measurement/prevention guidance |
| A-023 | University refectory food-waste / meal-improvement article | https://dergipark.org.tr/tr/download/article-file/4013917 | PDF | LINK_ONLY | Academic PDF; preserve article provenance and journal terms | H2 falsification / alternative-cause evidence |

## Image-use rule

For figures/graphics in a presentation or application:
- prefer first-party reusable graphics (for example EPA) or openly licensed academic figures;
- preserve visible source/attribution;
- do not screenshot vendor product pages as if they were project assets;
- do not copy a report cover/figure merely because the report PDF is publicly downloadable;
- if a figure is redrawn from data, cite the source dataset and label it as a project-created visualization.

## Binary ingest record

If a future agent stores a binary under `KREATE/PMR/assets/`, add a row here with:

```text
asset_id
source_id
original_url
retrieved_at
original_filename
repo_path
sha256
mime_type
license
attribution
transformation = none | crop | redraw | derived-chart
```

No binary currently becomes evidence merely by being committed to the repository.


## Recommended team-owned visuals

Prefer these over copied vendor/report graphics:

1. **PMR evidence ladder** — secondary context → testable hypothesis → real incident interview → source-owned operational data → measured pilot → impact claim.
2. **Dining decision loop** — signals → quantity/allocation decision → freeze point → production/service → served/surplus/waste → next cycle.
3. **Data-truth boundary** — `GENERATED_SANDBOX -X-> measured benchmark`; `SOURCE-OWNED EXPORT -> semantic reconciliation -> CS1 intake -> eligible measured evidence`.
4. **Root-cause tree** — production surplus / preparation loss / service-allocation mismatch / plate waste / menu acceptance / safety constraints / measurement artifact.
5. **Stakeholder decision map** — Food Services ↔ contractor ops ↔ BİD/BUCard ↔ measurement owner ↔ procurement/finance, with unresolved questions on each edge.

Every project-created chart should put source ID(s), data year and boundary note directly in the caption.
