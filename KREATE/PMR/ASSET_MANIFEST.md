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
| A-014 | merged PMR/market red-team PR #213 | https://github.com/yasinkaya701/bouncampus/pull/213 | Git PR | INTERNAL_PROVENANCE | Merged repository provenance | Current-master research lineage |

| A-015 | Boğaziçi 2025 food-waste XLSX | https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx | XLSX | LINK_ONLY | Official university artifact; retain original URL, retrieval date and field/unit semantics | Raw public waste-data artifact |
| A-016 | Boğaziçi University Sustainability Report 2025 | https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/183-bogazici-university-sustainability-2025-yayin-20251104-115151.pdf | PDF | LINK_ONLY | Official university report; public availability does not imply unrestricted redistribution | Institutional sustainability context |
| A-017 | Boğaziçi official cafeteria visual | https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155309.png | PNG | LINK_ONLY | Official-hosted image; reuse rights not established here | Visual context only; do not infer sensor/workflow geometry |
| A-018 | İzmir Bakırçay University Akıllı Kampüs Ara Raporu | https://akilliuniversite.bakircay.edu.tr/Yuklenenler/Akilli_Universite/Sonuc%CC%A7_Raporu_20220428.pdf | PDF | LINK_ONLY | Official university-hosted report; verify reuse terms before copying | Smart-campus dining/utilization/planning precedent |

| A-019 | Boğaziçi food-waste report 2024 | https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2024_bu.pdf | PDF | LINK_ONLY | Official historical university report | Historical aggregate context |
| A-020 | Boğaziçi food-waste report 2023 | https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2023_bu.pdf | PDF | LINK_ONLY | Official historical university report | Historical aggregate context |
| A-021 | Türkiye food-service food-waste prevention guide | https://www.tarimorman.gov.tr/ABDGM/BelgelerArsiv/Belgeler/Uluslararas%C4%B1%20Kurulu%C5%9Flar/gastro-bakanlik-kilavuzu.pdf | PDF | LINK_ONLY | Ministry/FAO/Metro guide; verify exact reuse terms before copying | Türkiye-specific prevention/measurement context |
| A-022 | Türkiye national food loss/waste strategy | https://faolex.fao.org/docs/pdf/tur209489.pdf | PDF | LINK_ONLY | Official policy archive/reference | National policy context |
| A-023 | UI GreenMetric Guideline 2026 | https://uigreenmetric.com/wp-content/uploads/2026/06/2026_Guideline_UI-GreenMetric-SUR-eng-v2.pdf | PDF | LINK_ONLY | First-party guideline; keep as external reference | Sustainability-evidence / governance context |

| A-024 | University refectory food-waste / meal-improvement article | https://dergipark.org.tr/tr/download/article-file/4013917 | PDF | LINK_ONLY | Academic PDF; preserve article/journal provenance and verify reuse terms before copying | H2 falsification / intervention reference |

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
