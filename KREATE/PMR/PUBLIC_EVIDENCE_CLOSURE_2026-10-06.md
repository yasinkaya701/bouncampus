# PMR-A Public Evidence Closure Matrix — IKN 2025/1727143

**As of:** 2026-10-06  
**Purpose:** freeze what public-web evidence can and cannot support for the Boğaziçi 2026–2027 dining contract and its service-truth/payment chain.

## Promotion states

- **VERIFIED_PUBLIC** — directly supported by current public/first-party evidence.
- **CLASSIFIED_PUBLIC** — structural class is recoverable, but labels/values are incomplete.
- **PUBLICLY_UNRESOLVED** — targeted public search did not recover the authoritative value/artifact.
- **SOURCE_OWNER_REQUIRED** — requires a real institutional/contract-owner artifact or walkthrough.

## Decision matrix

| Question | State | Publicly supportable answer | Must not infer | Next evidence |
|---|---|---|---|---|
| Contract form | VERIFIED_PUBLIC | Current IKN 2025/1727143 is a unit-price bid/contract structure. | Headline value is a meal unit price. | Authoritative unit-price schedule. |
| Meal rows | VERIFIED_PUBLIC | 380k breakfast, 2.5m student meals, 250k staff meals. | These are actual served/payable quantities. | Monthly hakediş + control record. |
| Added rows | CLASSIFIED_PUBLIC | Final schedule has 12 monthly labor/personnel-priced rows absent from cancelled 2025/1335958 public schedule. | Exact current role title for any row. | Final schedule/spec labels. |
| Labor row pattern | CLASSIFIED_PUBLIC | Exposed worker-count pattern: 1,2,2,3,5,1,11,17,10,10,5,8 with 19/24-month duration classes. | Mapping old job titles onto current rows. | Current staffing table + intact schedule. |
| Monthly service execution | VERIFIED_PUBLIC | Boğaziçi reports food-service work executed monthly and acceptance proposals prepared for realized service. | Monthly acceptance count equals BUCard passage. | Representative monthly package. |
| Acceptance governance | VERIFIED_PUBLIC | Dining Control Organization / acceptance workflow and Spending Authority route are institutionally evidenced. | Exact payable count, signer chain or freeze right. | Current contract-specific package. |
| BUCard report surfaces | VERIFIED_PUBLIC | Institutional IT evidence names cafeteria live report, daily passage reports with package-meal information, and personnel meal report. | passage = served = accepted = payable. | #292 aggregate export + SKS semantic reconciliation. |
| Payable quantity | SOURCE_OWNER_REQUIRED | Public web does not establish which operational count becomes payable. | Derivation from annual quantities or activity totals. | One redacted monthly hakediş + upstream puantaj/icmal/control record. |
| Awarded per-row prices | PUBLICLY_UNRESOLVED | No authoritative public per-row awarded-price schedule recovered in targeted sweep. | contract value / total meals. | Final unit-price schedule / contract owner. |
| Daily quantity freeze/change rights | SOURCE_OWNER_REQUIRED | Not established publicly for current contract. | Historical clause carry-over. | Current technical/admin spec or owner confirmation. |
| Savings/margin/WTP | BLOCKED | Cannot be computed from current public evidence. | Any headline-value shortcut. | Payable-unit economics + operational counterfactual + buyer evidence. |

## Current recoverable contract structure

```text
IKN 2025/1727143
├── 12 labor/personnel-priced monthly rows
│   ├── duration class: 24 months
│   └── duration class: 19 months
└── 3 meal rows
    ├── student breakfast: 380,000 meals
    ├── student meal: 2,500,000 meals
    └── staff meal: 250,000 meals
```

Exact labor titles and awarded row prices remain unresolved.

## One-service join gate

No downstream claim may collapse these quantities without source-owner evidence:

```text
ordered != produced != passage != served != control_accepted != payable
```

Minimum closing packet for one representative service slice:

1. quantity request/order and revisions;
2. BUCard/SKS aggregate service report with correction semantics;
3. Control Organization puantaj/icmal/inspection quantity;
4. hakediş work-item quantity/unit;
5. acceptance/muayene reference;
6. reconciliation rule for disagreement.

Preferred join grain: `service_date × campus × meal_period × meal_category/work_item`, or the closest authoritative grain with aggregation documented.

## Public sources

- Current final schedule mirror: https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4374218/
- Cancelled predecessor schedule: https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4173515/cetvel/
- Historical KİK baseline 2023/UH.I-1542: https://arsiv.kikkararlari.com/index.php?Itemid=9&id=74668&option=com_content&task=view
- Historical KİK baseline 2023/UH.I-1543: https://arsiv.kikkararlari.com/index.php?Itemid=9&id=74669&option=com_content&task=view
- Current dining governance directive: https://sks.bogazici.edu.tr/sites/sks.boun.edu.tr_2023/files/yemekhizmetleri_yonerge.pdf
- Jan-2026 Dining Control Organization assignment: https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/564-genel-sekreterlik-20260112-095525.pdf
- Boğaziçi 2025 Administration Activity Report: https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu%283%29.pdf

## Historical-source firewall

Historical KİK/Boğaziçi contracts are **DIFF_BASELINE_ONLY**. They may generate current-document search targets and interview questions. They may not prove current role titles, penalties, payable quantities, change rights, unit prices, margins or savings.
