# PDF / Visual / Data Reference Manifest

**Updated:** 2026-10-06  
**Policy:** link-first. Do not vendor third-party binaries unless redistribution rights are clear, the artifact is materially useful offline, and origin/license/checksum are recorded.

This file is an asset-navigation layer for PMR preparation. An asset appearing here is **not** PMR evidence and is not automatically admissible as an application claim.

| Source ID | Asset | Direct / canonical reference | Useful view | Repo treatment | Claim boundary |
| --- | --- | --- | --- | --- | --- |
| \`SRC-BU-002\` | Official 2025 campus food-waste table | https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310 | Monthly waste table + dining-hall/service context | Derived rows copied to \`data/bogazici_food_waste_2025_official.csv\` with provenance | Aggregate public baseline only; not service truth |
| \`SRC-BU-007\` | Boğaziçi Sustainability Reports hub | https://kurumsalveri.bogazici.edu.tr/tr/pages/surdurulebilirlik-raporlari/1063 | Sustainability 2025/2024 and GHG Inventory 2025 download links | Link only; reports are large and rights/size make blind vendoring low value | Institutional sustainability context only |
| \`SRC-STD-001\` | UI GreenMetric 2026 guideline | https://uigreenmetric.com/resources/university/guidelines/2026/english | Official page with PDF download | Link only | Why-now/evidence-governance context, not buyer validation |
| \`SRC-STD-001\` | UI GreenMetric 2026 direct PDF | https://uigreenmetric.com/wp-content/uploads/2026/06/2026_Guideline_UI-GreenMetric-SUR-eng-v2.pdf | PDF page 10: category weights; page 51: Governance & Digitalization section | Link only | Do not claim BOUNCAMPUS changes ranking |
| \`SRC-POL-001\` | Türkiye food-loss/waste national strategy | https://faolex.fao.org/docs/pdf/tur209489.pdf | National prevention/reduction/monitoring strategy | Link only; use FAOLEX stable mirror when ministry deep link breaks | National policy context, not Boğaziçi causal proof |
| \`SRC-METHOD-001\` | Disciplined Entrepreneurship PMR method PDF | https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf | Interview/research method | Link only | Method reference only |
| \`SRC-MEAS-001\` | UNEP Food Waste Index Report 2024 | https://www.unep.org/resources/publication/food-waste-index-report-2024 | Official landing page | Link only | Measurement-method context |
| \`SRC-MEAS-001\` | UNEP report PDF | https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf | Full methodology | Link only | Does not select a required Boğaziçi sensor/method |
| \`SRC-MEAS-002\` | EPA Wasted Food Scale | https://www.epa.gov/sustainable-management-food/wasted-food-scale | Official prevention hierarchy visual | Link only; visual is externally owned | Supports prevention hierarchy only |
| \`SRC-ACA-003\` | Open-access university foodservice paper | https://pmc.ncbi.nlm.nih.gov/articles/PMC9180560/ | Article tables on measurement, reduction strategies and barriers | Link only; CC BY article can be quoted/reused only with proper attribution and need | U.S. sample; no Boğaziçi transfer |
| \`SRC-ACA-002\` | University dining uncertainty paper | https://pubmed.ncbi.nlm.nih.gov/33971773/ | Abstract/bibliographic record | Link only | External mechanism evidence |
| \`SRC-ACA-001\` | Catering-demand forecasting paper | https://doi.org/10.1016/j.jclepro.2023.140265 | DOI landing page | Link only | External benchmark/mechanism; no transferred performance |

## Useful official web visuals

These are useful during interviews/pitch preparation but should normally remain external links:

1. **Boğaziçi 2025 food-waste table** — the official monthly table is the best source visual for the public baseline. Do not redraw it into a causal chart implying forecasting explains month-to-month variation.
2. **UI GreenMetric 2026 category table** — useful to show that Waste and Governance/Digitalization are explicit institutional sustainability categories. This is contextual, not product validation.
3. **EPA Wasted Food Scale** — useful to explain why preventing avoidable production can be preferable to downstream recovery **if** PMR proves the production decision is a real reachable cause.
4. **Boğaziçi Sustainability Reports** — source of official institutional report graphics; use as citation/navigation, not as evidence of dining workflow.

## Binary-copy rules

Before committing any external PDF/image/XLSX:

1. verify redistribution/license terms;
2. record canonical source URL and retrieval date;
3. compute and record SHA-256;
4. state whether it is an immutable snapshot or merely a working copy;
5. do not store personal or transaction-level data;
6. prefer a stable canonical link when offline storage adds little value.

For copyrighted papers and reports, link to the publisher/official landing page by default.

## Raw / structured data rules

Public aggregate tables may be transcribed into a small structured file when:

- every row traces to one source ID;
- the transcription preserves original units/labels;
- no missing field is fabricated;
- the file is labeled as public aggregate context;
- downstream code cannot silently treat it as \`SERVICE_TRUTH_V1\`.

The current example is \`data/bogazici_food_waste_2025_official.csv\`.

## Future asset backlog

Only add/download when it resolves an active question:

- privacy-preserving BUCard aggregate export + data dictionary — **real institutional artifact; #292**;
- accepted SKS reconciliation note/schema — **real institutional artifact; #292**;
- produced/served/surplus/waste report template — if source owner can provide it;
- current procurement/contract clauses that define quantity, settlement or penalties — if authoritative and current;
- second-site operational report/schema — for repeatability testing;
- measurement protocol photos/diagrams — only after site permission and privacy review.

Do not fill this directory with decorative images. Every visual should answer a PMR, measurement, buyer or evidence question.
