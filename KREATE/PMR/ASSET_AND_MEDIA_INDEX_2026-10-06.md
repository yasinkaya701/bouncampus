# PMR Asset and Media Index

**Updated:** 2026-10-06  
**Purpose:** direct source artifacts for agents preparing PMR, evidence review, application writing, diagrams, and pilot measurement.

This is a **link-first index**. Do not mirror third-party binary assets into the repository unless redistribution permission is clear. When a binary is intentionally archived later, record source URL, retrieval date, license/permission, and checksum.

## 1. Raw data / machine-readable artifacts

### Boğaziçi 2025 waste spreadsheet

- **Type:** XLSX
- **Source ID:** `SRC-BOUN-FOODWASTE-2025-XLSX`
- **Direct file:**  
  https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/2025%20Y%C4%B1l%C4%B1%20At%C4%B1k%20Bilgisi%281%29.xlsx
- **Official parent page:**  
  https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
- **Use:** raw-source reconciliation, column/period inspection, future checksum capture.
- **Warning:** do not treat a column as service-level ground truth until its semantics are confirmed with the data owner. The rendered official table itself contains August/October boundary inconsistencies.

## 2. PDFs / reports / standards

### Disciplined Entrepreneurship PMR practical guide

- **Type:** PDF
- **Source ID:** `SRC-METHOD-DE-PMR-2019`
- https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf
- **Use:** interview method, qualitative-first discovery, hypothesis testing, observation/dialogue/test design.

### Boğaziçi SDG 2 institutional publication

- **Type:** PDF
- **Source ID:** `SRC-BOUN-SDG2-2024-PDF`
- https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/18--yayin-20250910-094806.pdf
- **Use:** official food-system/sustainability background and archival evidence.
- **Boundary:** institutional reporting is not PMR.

### Boğaziçi historical 2023 food-waste PDF

- **Type:** PDF
- https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/food_waste_2023_bu.pdf
- **Use:** historical source trail only.
- **Boundary:** verify metric definitions before year-to-year comparison.

### UNEP Food Waste Index Report 2024

- **Type:** report page + PDF
- **Source ID:** `SRC-UNEP-FWI-2024`
- Landing page: https://wedocs.unep.org/items/dbe2cd4c-8384-4636-8359-5847f42b9711
- PDF: https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf
- **Use:** food-service waste measurement boundary and reporting design.

### Food Loss and Waste Standard

- **Type:** standard page + overview PDF
- **Source IDs:** `SRC-FLW-STANDARD`, `SRC-FLW-OVERVIEW-PDF`
- Standard: https://flwprotocol.org/flw-standard/
- Overview PDF: https://flwprotocol.org/wp-content/uploads/2016/12/FLW-Standard_Overview_December-2016.pdf
- Tools: https://flwprotocol.org/flw-tools/
- **Use:** accounting/reporting scope, quantification method selection, pilot reporting structure.

## 3. Official Boğaziçi photographs / visuals

All four images below are linked by the official 2025 Campus Food Waste Tracking page. Keep them as external links unless reuse permission is confirmed.

### Dining hall interior

- https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155309.png

### Serving / food-service area

- https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155358.png

### Dining hall interior — second view

- https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155428.png

### Outdoor seating / facility context

- https://mediastore.cc.bogazici.edu.tr/web/userfiles/images/ekran_goruntusu_2024-10-16_155707.png

**Parent/provenance page:**  
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

### Visual-use rule

For internal analysis:
- use the images as layout/facility context;
- do not infer occupancy, throughput, camera feasibility, lighting performance, tray geometry, or current equipment state from a single public image.

For external/pitch use:
- check the source site's reuse/permission terms first;
- preserve attribution;
- prefer linking/citing over copying when rights are unclear.

## 4. Current operational web surfaces

### 2025 campus food-waste tracking

https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

Useful for:
- public 2025 monthly food-waste values;
- annual total;
- dining-hall capacities;
- service context;
- raw spreadsheet and official media links.

### Sustainable food choices on campus

https://kurumsalveri.bogazici.edu.tr/tr/pages/233-sustainable-food-choices-on-campus/1313

Useful for:
- institutional food-service background;
- preparation/menu/portion context;
- sustainability practices.

### Dining monthly menu

https://yemekhane.bogazici.edu.tr/aylik-menu

Useful for:
- meal calendar;
- menu taxonomy;
- candidate context variables.

Do not equate menu publication with quantity or demand.

### BUCampus menu survey

https://yemekhane.bogazici.edu.tr/menu-anketi

Useful for:
- existence of an authenticated preference interaction;
- candidate pre-service context signal;
- interview questions about whether/how it affects production.

Do not equate a vote with reservation, actual served demand, payment, or production quantity.

### Dining / cooking / distribution control body

https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

Useful for:
- governance-role discovery;
- interview/referral map;
- separating control/verification from production, procurement and system ownership.

## 5. Academic / benchmark material

### Campus dining demand prediction / food waste

Gül Fatma Türker (2025), *Reducing Food Waste in Campus Dining: A Data-Driven Approach to Demand Prediction and Sustainability*, Sustainability 17(2), 379.

- DOI: https://doi.org/10.3390/su17020379
- **Source ID:** `SRC-ACADEMIC-TURKER-2025`
- **Use:** external benchmark, candidate variables, evaluation ideas.
- **Boundary:** not local customer evidence and not transferable impact.

## 6. Method web references

### Disciplined Entrepreneurship Step 1A — PMR

https://www.d-eship.com/step1a/

### MIT Orbit — What is primary market research?

https://orbit-kb.mit.edu/hc/en-us/articles/204891786-What-is-primary-market-research/

## 7. Suggested local archival structure — only when needed

If later agents need immutable copies and rights permit:

```text
KREATE/PMR/assets/
  README.md
  public/
    <source-id>/
      source.url
      retrieved_at.txt
      sha256.txt
      license_or_permission.txt
      <original-file>
```

Do **not** add large PDFs/images/XLSX files merely because they exist. Archive only when one of these is true:
- source is unstable and needed for reproducibility;
- a pilot/claim depends on an immutable snapshot;
- license/permission is clear;
- a checksum is required for evidence admission.

Otherwise keep the canonical URL in the source registry.

## 8. Missing artifacts to request through PMR

The highest-value future artifacts are not more public PDFs. Ask source owners for privacy-minimized operational artifacts such as:

- one example daily production/quantity planning sheet;
- field/data dictionary for any aggregate service counts;
- one anonymized date × site × meal export;
- waste weighing/reporting form and stage definitions;
- decision/freeze timeline or SOP;
- accepted/served count reconciliation rule;
- contract/hakediş field definitions relevant to quantity;
- current operator heuristic or planning worksheet.

These artifacts can close semantic gaps that public research cannot.
