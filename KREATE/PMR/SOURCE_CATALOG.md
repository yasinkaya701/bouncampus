# PMR Source Catalog

**Updated:** 2026-10-06  
**Canonical machine-readable source:** [SOURCE_REGISTRY.json](./SOURCE_REGISTRY.json)

This is the human-readable view of the cumulative registry. Source presence means “useful, traceable input,” **not** “validated customer evidence.”

| ID | Source | Class | Best use | Explicit boundary |
| --- | --- | --- | --- | --- |
| \`SRC-BU-001\` | [SKS 2025 Activity Report / 2026–2027 Goals](https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096) | PUBLIC_OFFICIAL | Dining scale, package-meal and feedback-program context | Not service demand, quantity owner, root cause, access or adoption |
| \`SRC-BU-002\` | [Campus food waste tracking — 2025](https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310) | PUBLIC_OFFICIAL | Official aggregate waste baseline + public hall/service context | Not service labels, causal attribution or intervention effect |
| \`SRC-BU-003\` | [Healthy and affordable food choices](https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314) | PUBLIC_OFFICIAL | Centralized preparation / advance menu context | Not quantity ownership, adjustability or data export proof |
| \`SRC-BU-004\` | [Official Dining Hall site](https://yemekhane.bogazici.edu.tr/) | PUBLIC_OFFICIAL | Advance menu and operations navigation | Not actual served demand or internal production history |
| \`SRC-BU-005\` | [Kilyos reservation notice — 20 May 2026](https://yemekhane.bogazici.edu.tr/node/493) | PUBLIC_OFFICIAL | Proof a bounded reservation-intent workflow existed | Do not generalize cutoff/coverage; reservation ≠ served demand |
| \`SRC-BU-006\` | [Academic Calendar](https://akademiktakvim.bogazici.edu.tr/) | PUBLIC_OFFICIAL | Decision-time-known calendar context | No causal/forecast-lift claim |
| \`SRC-BU-007\` | [Sustainability Reports](https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063) | PUBLIC_OFFICIAL | Institutional sustainability/reporting context | Not dining workflow/persona/buyer evidence |
| \`SRC-POL-001\` | [Türkiye food loss/waste strategy — FAOLEX mirror](https://faolex.fao.org/docs/pdf/tur209489.pdf) | PUBLIC_OFFICIAL | National prevention/reduction/monitoring context | Not Boğaziçi causal proof or product impact |
| \`SRC-STD-001\` | [UI GreenMetric 2026 guideline](https://uigreenmetric.com/resources/university/guidelines/2026/english) | PUBLIC_OFFICIAL | Governance/digitalization/evidence why-now | Not willingness to buy or ranking-impact proof |
| \`SRC-ACA-001\` | [Rodrigues et al., JCP 2024](https://doi.org/10.1016/j.jclepro.2023.140265) | ACADEMIC | Forecasting mechanism + baseline-comparison design | Do not transfer model/waste-reduction performance |
| \`SRC-ACA-002\` | [Faezirad et al., 2021](https://pubmed.ncbi.nlm.nih.gov/33971773/) | ACADEMIC | Reservation/no-show uncertainty + waste/shortage trade-off | Not Boğaziçi reservation/economic semantics |
| \`SRC-ACA-003\` | [Musicus et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9180560/) | ACADEMIC | University-foodservice reduction/measurement practices | U.S. sample; no direct Boğaziçi transfer |
| \`SRC-ACA-004\` | [Kaur et al. review](https://doi.org/10.1108/IJCHM-07-2020-0672) | ACADEMIC | Multi-causal food-waste diagnosis | No Boğaziçi-specific causal share |
| \`SRC-METHOD-001\` | [Disciplined Entrepreneurship — PMR](https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf) | METHOD_REFERENCE | Interview/discovery method | No market fact |
| \`SRC-MEAS-001\` | [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024) | PUBLIC_OFFICIAL | Measurement-method selection | Does not mandate one Boğaziçi sensor/method |
| \`SRC-MEAS-002\` | [US EPA Wasted Food Scale](https://www.epa.gov/sustainable-management-food/wasted-food-scale) | PUBLIC_OFFICIAL | Prevention hierarchy + visual | Does not prove production forecasting is the local lever |

## Source-quality order

Prefer:

1. current official artifact directly describing the operating fact;
2. current legal/procurement/standards artifact;
3. source-owner export/schema with provenance;
4. peer-reviewed evidence for mechanisms/benchmarks;
5. vendor page only for the vendor's own stated capability;
6. general articles only as navigation clues.

## Current source gaps worth researching

Do not browse randomly. The next external artifacts with high information value are:

- current authoritative production/quantity responsibility or contract clause;
- current settlement/hakediş basis;
- current local contractor operational owner and planning artifact;
- source-owner BUCard aggregate data dictionary/report schema;
- source-owner waste measurement definition by stage/campus/service;
- second-site comparable production/report workflow;
- current incumbent planning software actually used by the operator.

## Conflict handling

If two official sources disagree:

- keep both source IDs;
- mark the claim \`RECONCILIATION_REQUIRED\`;
- preserve original values/labels;
- route the conflict into PMR with the source owner;
- do not silently choose the value that best fits the pitch.

Example already visible in \`SRC-BU-002\`: some published monthly “delivered to İSTAÇ” values exceed the same row's published “total food waste” value. The structured snapshot preserves this exactly and flags it for semantic reconciliation rather than correcting the source.
