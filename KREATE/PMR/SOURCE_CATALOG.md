# PMR Source Catalog

**Updated:** 2026-10-06  
**Canonical machine-readable register:** [source_catalog.json](./source_catalog.json)

Legend:

- `OFFICIAL_PUBLIC` — authoritative institution/government source.
- `METHOD_STANDARD` — measurement/research standard or methodology.
- `PEER_REVIEWED` — academic source; case-study results do not become our pilot evidence.
- `VENDOR_CLAIM` — vendor-published capability/outcome; never treat as independent proof.
- `PUBLIC_OPERATIONAL` — public operational information useful for mechanism/target discovery.

## Boğaziçi / decision-context sources

| ID | Source | Kind | PMR use | Direct asset | Critical limitation |
| --- | --- | --- | --- | --- | --- |
| PMR-SRC-001 | [Boğaziçi Campus Food Waste Tracking](https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310) | OFFICIAL_PUBLIC | H2/H4; official aggregate context and source-quality audit | [2025 source spreadsheet](https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx) | Monthly aggregate, not service truth; current 2025 table has unreconciled internal semantics. |
| PMR-SRC-002 | [Boğaziçi Impact — Campus Food Waste Tracking](https://impact.bogazici.edu.tr/221-campus-food-waste-tracking) | OFFICIAL_PUBLIC | historical 2023/2024 context | [2024 food-waste PDF](https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2024_bu.pdf) · [2023 food-waste PDF](https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2023_bu.pdf) | Historical aggregate reporting; not intervention/causal evidence. |
| PMR-SRC-003 | [SKS 2025 activity-report page](https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096) | OFFICIAL_PUBLIC | scale, operating context, outreach/source-owner discovery | — | Re-open before using any date-sensitive numeric claim. |
| PMR-SRC-004 | [Official dining menu](https://yemekhane.bogazici.edu.tr/) | PUBLIC_OPERATIONAL | decision-time menu context | — | Menu availability does not prove historical immutable snapshots. |
| PMR-SRC-005 | [Kilyos reservation notice — 20 May 2026](https://yemekhane.bogazici.edu.tr/node/493) | OFFICIAL_PUBLIC | proves a bounded reservation-intent workflow can exist | — | Do not generalize cutoff/coverage to other campuses or dates. |
| PMR-SRC-006 | [Boğaziçi Academic Calendar](https://akademiktakvim.bogazici.edu.tr/) | OFFICIAL_PUBLIC | pre-known temporal context | — | Must preserve the version actually available before a historical decision cutoff. |

## PMR and measurement methodology

| ID | Source | Kind | PMR use | Direct asset | Critical limitation |
| --- | --- | --- | --- | --- | --- |
| PMR-SRC-007 | [Disciplined Entrepreneurship — Primary Market Research](https://www.d-eship.com/step1a/) | METHOD_STANDARD | PMR interview discipline, direct-customer research | [PMR PDF](https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf) | Method guidance, not market evidence. |
| PMR-SRC-008 | [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024) | METHOD_STANDARD | food-service measurement methods and reporting context | [Full PDF](https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf) · [Key messages PDF](https://wedocs.unep.org/bitstream/handle/20.500.11822/45275/Food-Waste-Index-2024-key-messages.pdf) | Global methodology/context; not site validation. |
| PMR-SRC-009 | [Food Loss & Waste Accounting and Reporting Standard](https://flwprotocol.org/flw-standard/) | METHOD_STANDARD | scope, boundary, quantification/reporting discipline | [WRI overview](https://www.wri.org/research/food-loss-and-waste-accounting-and-reporting-standard) | Standard does not select our operational decision or causal intervention. |
| PMR-SRC-010 | [WRAP Hospitality & Food Service guide](https://www.wrap.ngo/resources/guide/hospitality-and-food-service) | METHOD_STANDARD | measurement/action guidance and practical artifacts | downloadable files on source page | UK-oriented operational guidance; adapt, do not copy assumptions blindly. |
| PMR-SRC-011 | [T.C. Tarım ve Orman Bakanlığı / FAO — Toplu Tüketimde Gıda İsrafı Kılavuzu](https://www.tarimorman.gov.tr/ABDGM/BelgelerArsiv/Belgeler/Uluslararas%C4%B1%20Kurulu%C5%9Flar/gastro-bakanlik-kilavuzu.pdf) | OFFICIAL_PUBLIC | Türkiye-specific separation, measurement, prevention, planning context | PDF (97 pages) | Guidance; not proof of Boğaziçi practice. |
| PMR-SRC-012 | [T.C. ÇŞİDB — Sıfır Atık Yönetmeliği announcement](https://cygm.csb.gov.tr/sifir-atik-yonetmeligi-resmi-gazetede-yayimlanarak-yururluge-girmistir.-duyuru-383053) | OFFICIAL_PUBLIC | regulatory context / stakeholder questions | — | Legal applicability/detail must be checked against current official text before compliance claims. |

## Academic / operational mechanism sources

| ID | Source | Kind | PMR use | DOI / PDF | Critical limitation |
| --- | --- | --- | --- | --- | --- |
| PMR-SRC-013 | Aydın, Balcıoğlu & Sezen — *Machine Learning Techniques for Cafeteria Demand Forecasting: An Institutional Case* | PEER_REVIEWED | H1/H3/H4; turnstile-based institutional demand forecasting | [DOI](https://doi.org/10.26466/opusjsr.1649256) · [PDF](https://dergipark.org.tr/en/download/article-file/4651557) | Model/case estimate; not BOUNCAMPUS field impact. |
| PMR-SRC-014 | Türker — *Reducing Food Waste in Campus Dining: A Data-Driven Approach to Demand Prediction and Sustainability* | PEER_REVIEWED | H1/H2/H4; campus context + demand prediction | [DOI](https://doi.org/10.3390/su17020379) | Treat reported reduction as the paper's case/model result, not our causal evidence. |
| PMR-SRC-015 | Faezirad et al. — *Preventing food waste in subsidy-based university dining systems...* | PEER_REVIEWED | H3; reservation/show-no-show uncertainty + waste/shortage cost | [DOI](https://doi.org/10.1177/0734242X211017974) | Case/model framework; external context only. |
| PMR-SRC-016 | Rodrigues et al. — *Machine learning models for short-term demand forecasting in food catering services* | PEER_REVIEWED | H2/H3; baselines, wasted meals and unmet demand | [DOI](https://doi.org/10.1016/j.jclepro.2023.140265) | External catering services; confidential data; modeled operational consequences. |
| PMR-SRC-017 | Fatemi et al. — *Food waste reduction and its environmental consequences: a quasi-experimental study in a campus canteen* | PEER_REVIEWED | H2 falsification pressure: taste, portion, quality, menu causes | [Publisher](https://link.springer.com/article/10.1186/s40066-024-00488-y) | Different site/intervention; does not identify Boğaziçi causal mix. |
| PMR-SRC-018 | Özbiltekin-Pala et al. — *Food waste management: an example from university refectory* | PEER_REVIEWED | H2; Türkiye university plate-waste mechanism | [DOI](https://doi.org/10.1108/BFJ-09-2020-0802) | Plate-waste study; not production-surplus evidence. |
| PMR-SRC-019 | Aydın Gastronomy — *Determination of the Amount of Food Waste and Improving Meals to Reduce Food Waste in the University Refectory* | PEER_REVIEWED | H2; intervention/menu-quality alternative | [Landing](https://dergipark.org.tr/tr/pub/aydingas/article/1503134) · [PDF](https://dergipark.org.tr/tr/download/article-file/4013917) | Site-specific; use as contrary/alternative-cause evidence. |

## Türkiye cross-university repeatability

| ID | Source | Kind | PMR use | Critical limitation |
| --- | --- | --- | --- | --- |
| PMR-SRC-020 | [GTÜ dining page](https://www.gtu.edu.tr/kategori/5904/0/display.aspx) | OFFICIAL_PUBLIC | H1/H3; historical demand + expected-user planning and replenishment mechanism | Does not prove willingness to buy or workflow equivalence. |
| PMR-SRC-021 | [İTÜ food-waste prevention / planning page](https://sustainability.itu.edu.tr/tr/itu-kafeteryalari-ve-yemek-hizmetleri-gida-israfini-onlemeye-yonelik-ozel-programlar-saglamaktadir) | OFFICIAL_PUBLIC | H1/H3; academic calendar/weather/history already used operationally | Kills novelty of these input classes; not Boğaziçi validation. |
| PMR-SRC-022 | [İTÜ electronic dining-entry source](https://kim.itu.edu.tr/itukart/yemekhane-uygulamasi) | OFFICIAL_PUBLIC | H4; example of electronic dining-entry infrastructure | Infrastructure existence ≠ accessible/exportable service truth. |

## Competitor / incumbent reality

| ID | Source | Kind | PMR use | Critical limitation |
| --- | --- | --- | --- | --- |
| PMR-SRC-023 | [Winnow — Universities](https://www.winnowsolutions.com/industries/universities) | VENDOR_CLAIM | current alternative / capability map | Vendor marketing. |
| PMR-SRC-024 | [Winnow Foresight announcement — Sep 2026](https://www.winnowsolutions.com/resources/news/winnow-and-hilton-announce-winnow-foresight-a-mobile-first-ai-powered-forecasting-tool-designed-to-predict-kitchen-demand-and-prevent-food-waste) | VENDOR_CLAIM | kills “nobody forecasts production” novelty | Vendor claim; hotel workflow may differ from target universities. |
| PMR-SRC-025 | [Leanpath — University of Nebraska case](https://www.leanpath.com/case-study-u-of-nebraska/) | VENDOR_CLAIM | university incumbent / measurement-feedback alternative | Outcome figures are vendor case-study claims. |
| PMR-SRC-026 | [Emissary Campus](https://emissary.com.tr/tr/cozumler/emissary-campus) | VENDOR_CLAIM | Türkiye campus sustainability/reporting incumbent | Broad platform; exact food-production control-point depth must be verified. |

## How to cite in internal work

Prefer source ID + claim, e.g.:

> `PMR-SRC-015`: external university-dining literature explicitly models shortage penalty and waste cost under demand uncertainty.

Never write:

> “H3 is validated.”

Only real PMR from target/relevant customers can change the customer-evidence state.
