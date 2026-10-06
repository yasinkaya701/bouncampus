# CS2 Competitor + Procurement Refresh — 2026-10-06

**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Scope:** bounded current-source verification for product positioning, procurement interpretation, and PMR question generation.  
**Evidence class:** secondary/public/vendor research only. This file is **not** PMR, pilot evidence, local model evidence, customer validation, or legal/procurement advice.

## Why this refresh exists

Issue #322 asks CS2 to keep competitor capability references current, reverify useful procurement cases, map application claims to missing primary facts/falsifiers, and prevent external effect sizes from becoming BOUNCAMPUS impact claims.

This refresh rechecks existing canonical source families without creating a parallel PMR registry. Existing source IDs continue to resolve through `KREATE/PMR/source_catalog.json` and `KREATE/PMR/SOURCE_LIBRARY.md`.

## 1. Current procurement surface — reverified

### S-PROC-001 — Boğaziçi 2026–2027 food-service procurement

- **IKN:** 2025/1727143
- **Public mirror:** https://ekapveri.com/ihale/ekap-2025-1727143/
- **Result mirror:** https://www.ihaledetay.com/2025-1727143
- **Official lookup surface:** https://ekap.kik.gov.tr/EKAP/
- **Reverified:** 2026-10-06

Current public result/notice context supports the following narrow facts:

- the service covers Boğaziçi University North, South, Kilyos, Kandilli, Hisar and Anadolu Hisarı campuses;
- the advertised two-year quantities are 2,500,000 student meals, 380,000 breakfasts/sahur meals and 250,000 staff meals;
- the result identifies TEMAŞ Gıda Sanayi ve Ticaret A.Ş. as the awarded contractor;
- the public result reports a contract date of 2025-12-25 and a contract amount of 759,537,563.59 TRY;
- the notice states the economically most advantageous offer is determined on price;
- bids are structured as item quantity × unit price and the awarded agreement is a unit-price contract;
- the bidder capacity criterion is 5,000 meals/day, described as one half of the administration's stated daily meal need.

### What S-PROC-001 does **not** prove

Do not convert the procurement notice/result into any of the following claims:

- actual daily production or actual served demand;
- the quantity used for hakediş/payment acceptance;
- the operational freeze point or who can revise quantity;
- current unit-price schedule by meal type;
- penalties, shortage consequence or surplus ownership;
- software/data-access rights;
- buyer willingness to purchase BOUNCAMPUS;
- savings addressable by the product.

The 5,000 meals/day figure is a **bidder capacity threshold**, not measured daily demand.

### S-PROC-002 — cancelled predecessor procurement

- **IKN:** 2025/1335958
- **Public mirror:** https://ekapveri.com/ihale/ekap-2025-1335958/
- **Reverified:** 2026-10-06

The public record states the procurement was cancelled after objections to the tender documents were evaluated and changes to specifications were found necessary; the timing did not allow an EKAP addendum before the tender date.

This is useful only as a procurement-change precedent and document-discovery lead.

**Forbidden inference:** the cancellation does not prove a technology problem, food-waste problem, data-access problem, or product demand.

## 2. Competitor capability refresh

### Winnow — generic forecasting novelty is closed

Canonical sources:
- **S-COMP-001:** https://www.winnowsolutions.com/
- **S-COMP-002:** https://www.winnowsolutions.com/resources/news/introducing-winnow-foresight-a-new-way-to-prevent-food-waste-and-improve-guest-satisfaction-with-ai-powered-forecasting
- **S-COMP-005:** https://www.winnowsolutions.com/resources/news/winnow-and-hilton-announce-winnow-foresight-a-mobile-first-ai-powered-forecasting-tool-designed-to-predict-kitchen-demand-and-prevent-food-waste

Reverified 2026-10-06:

- Winnow publicly markets food-waste measurement plus production forecasting.
- Winnow Foresight is positioned as a mobile-first AI production-forecasting tool.
- Vendor material says Foresight uses guest occupancy and waste data to create daily production plans and can forecast at individual-food-item level.
- The launch positioning is focused on hotel kitchens and was developed with Hilton chefs.

**CS2 consequence:** do not pitch “AI predicts how much food to prepare” as the moat.

**Boundary:** all performance/outcome statements on Winnow pages remain vendor claims unless independently verified; hotel fit does not establish Turkish public-university fit.

### Leanpath — generic measurement / AI vision novelty is also closed

Canonical sources:
- **S-COMP-003:** https://www.leanpath.com/industries/college-university/
- **S-COMP-006:** https://www.leanpath.com/products/food-waste-tracking/
- additional current capability surface: https://www.leanpath.com/products/plate-waste-tracking/
- **Reverified:** 2026-10-06

Current first-party material shows:

- explicit college/university positioning;
- AI-enabled tracking for high-volume foodservice;
- floor-scale and photography/root-cause workflows;
- plate-waste tracking with computer vision through a partner integration;
- reporting/analytics positioned for operational and sustainability use.

**CS2 consequence:** do not claim generic food-waste tracking, dashboarding, computer vision, or campus sustainability reporting as unique.

**Boundary:** Leanpath outcomes/testimonials are vendor/customer marketing evidence, not transferable BOUNCAMPUS effect sizes.

## 3. Product-positioning decision

The defensible current wedge is narrower than “AI cafeteria forecasting”:

```text
pre-service signals that are actually available before freeze
→ semantic reconciliation against operational truth
→ reachable quantity/service decision
→ transparent baseline
→ bounded recommendation + uncertainty
→ accountable human approval / override
→ execution record
→ prospective surplus + shortage measurement
→ evidence-grade claim promotion
```

This wedge remains a hypothesis until PMR closes the owner/freeze/data/incentive chain.

## 4. Claims that are now unsafe

Do **not** use these in an application, deck, demo caption or judge answer unless the required local evidence exists:

- “first AI system for cafeteria demand forecasting”;
- “unique food-waste tracking / computer-vision platform”;
- “will reduce Boğaziçi food waste by X%”;
- “will save Boğaziçi ₺X”;
- “BUCard/turnstile data gives actual meal demand”;
- “the current contractor is paid directly by actual served meals”;
- “the 5,000 meals/day procurement figure is current demand”;
- “Boğaziçi can deploy this without new data agreements”;
- “the same workflow scales to other universities”;
- “published academic/vendor effect sizes are expected BOUNCAMPUS outcomes”.

## 5. Highest-value primary facts CS2 still needs

1. **Quantity owner:** who sets/approves the service-level quantity?
2. **Freeze point:** when is that quantity practically fixed, and what can still change afterward?
3. **Settlement truth:** which count/record drives contractor acceptance or payment?
4. **Economic consequence:** who benefits from less excess and who bears shortage risk?
5. **Signal semantics:** what do reservation, BUCard, QR, turnstile, served and settlement events each mean?
6. **Current baseline:** what rule/heuristic/tool is used today?
7. **Waste-stage split:** preparation vs unserved surplus vs plate/post-consumer waste.
8. **Second-site repeatability:** does another institution expose the same owner/freeze/signal/action chain?
9. **Pilot authority:** who can approve data access, a shadow test and a bounded intervention?
10. **Incumbent stack:** what software/reporting/measurement tools already exist in the workflow?

## 6. Merge / source-registry note

No new canonical source ID is allocated in this bounded refresh because the key procurement and competitor pages already exist in the cumulative PMR catalog. The Leanpath plate-waste page is recorded here as a current capability surface; if it becomes decision-critical, add it to the canonical catalog through the shared PMR fan-in rather than creating a parallel registry.

## 7. Definition of done for this refresh

- procurement claims are constrained to what the current public record actually supports;
- cancellation is not misrepresented as product evidence;
- competitor references are current as of 2026-10-06;
- generic forecasting/tracking/vision novelty claims are explicitly closed;
- local savings/waste-impact claims remain blocked until measured;
- the application narrative has a narrower falsifiable wedge;
- the companion claim-falsifier map converts every promoted statement into a missing primary fact and a kill/modify answer.
