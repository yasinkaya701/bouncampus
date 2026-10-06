# Claim → Source → PMR Gap Matrix

**Updated:** 2026-10-06  
**Purpose:** Prevent secondary/public research from silently turning into customer claims.

Source IDs resolve through [SOURCE_LIBRARY.md](SOURCE_LIBRARY.md) and [source_catalog.json](source_catalog.json).

| Claim / hypothesis | What secondary evidence currently says | Source IDs | What it does **not** establish | Primary evidence required |
| --- | --- | --- | --- | --- |
| **H1 — Reachable quantity control point exists** | Other Turkish universities publicly describe pre-service production planning; Boğaziçi has centrally coordinated dining operations. | S-BU-001, S-BU-003, S-TR-001, S-TR-002 | Who actually sets Boğaziçi/TEMAŞ quantities, at what time, and who can revise them. | Recent concrete workflow from university + contractor/production participants; decision timestamp and revision rights. |
| **H2 — Demand mismatch causes material addressable waste** | Boğaziçi publishes non-trivial aggregate food-waste data; other institutions describe demand uncertainty. | S-BU-002, S-TR-001, S-MEAS-001, S-ACAD-007, S-ACAD-008 | Waste stage/cause; whether forecast error is a dominant or avoidable cause. Academic evidence also shows plausible plate-waste/portion/taste mechanisms. | Recent mismatch incidents + stage-separated service-level measurement or credible records. |
| **H3 — Shortage risk is asymmetric and drives a buffer** | GTÜ describes unexpected demand and replenishment; İTÜ describes contingency preparation. Academic work models waste vs shortage costs. | S-TR-001, S-TR-002, S-ACAD-004 | Boğaziçi operator risk preference, actual buffer, penalty or service consequence. | Recent shortage + surplus examples; explicit current buffer/heuristic and consequence chain. |
| **H4 — Measurement/data are feasible** | Public menu/calendar/waste context exists; academic work shows turnstile data can be useful; standards define credible measurement methods. | S-BU-002, S-BU-004, S-BU-005, S-ACAD-002, S-MEAS-001, S-MEAS-002 | Access to Boğaziçi historical service-level planned/produced/served/surplus data; field semantics; retention. | Source owner, data dictionary, availability timestamps, sample real export or prospective measurement protocol. |
| **H5 — A usable persona owns/influences the decision** | University dining has identifiable governance/operations roles across institutions. | S-BU-001, S-TR-003 | Which real role/person owns the Boğaziçi quantity action, budget, pilot approval or veto. | Independent accounts converging on authority chain and a recent real decision. |
| **H6 — Workflow can adopt human-reviewed decision support** | Other institutions already combine signals and react to shortages, so operational adjustment is plausible. | S-TR-001, S-TR-002 | Trust threshold, integration burden, timing, food-safety/contract limits or willingness to act at Boğaziçi. | Observe existing revisions; ask what information changed the last real plan and what blocks action. |
| **Academic calendar/weather/menu are useful candidate signals** | They already appear in academic work and İTÜ practice. | S-TR-002, S-ACAD-003, S-ACAD-005, S-ACAD-006 | Incremental decision value at Boğaziçi. | Leakage-safe, decision-time ablation after real service labels exist. |
| **Turnstile/card counts may be useful signals** | Institutional research and İTÜ operations show this signal class is credible. | S-ACAD-002, S-TR-003 | Boğaziçi availability, privacy approval, duplicates/refunds/second-meal semantics. | Aggregate export feasibility + semantic reconciliation with actual served meals. |
| **Reservation intent may reduce uncertainty** | A Boğaziçi special-period reservation workflow existed; reservation-aware academic optimization exists. | S-BU-006, S-ACAD-004 | Campus-wide/current reservation coverage or reservation=served equivalence. | Ask exactly where reservations exist, cutoff, cancellations/no-shows and served reconciliation. |
| **Generic AI demand forecasting is differentiated** | **Contradicted.** Academic literature is established and Winnow Foresight now markets production forecasting. | S-ACAD-001, S-ACAD-003, S-COMP-002 | Any defensible moat. | PMR must identify a specific unresolved workflow/control-point gap worth switching for. |
| **Food-waste measurement + feedback is differentiated** | **Contradicted/commoditized in broad form.** Leanpath/Winnow already cover substantial tracking/feedback territory. | S-COMP-001, S-COMP-003 | Exact feature parity or segment fit. | Ask what incumbent stack is used and where the quantity decision still relies on manual judgment. |
| **Campus sustainability dashboard/evidence layer is differentiated** | **Contradicted as a broad novelty claim** by existing Türkiye campus platform offerings. | S-COMP-004 | Whether BOUNCAMPUS has a narrower operations wedge. | Buyer PMR on decision workflow, not dashboard desirability. |
| **Reducing unnecessary production is upstream prevention** | EPA/UNEP frameworks support prevention and rigorous measurement. | S-MEAS-001, S-MEAS-003 | That the proposed recommendation actually reduces measured Boğaziçi waste without increasing shortage. | Pre-registered control/intervention measurement with service guardrails. |
| **Buyer will pay because meal volume/waste is large** | **Unsupported.** Public scale and procurement context alone cannot prove WTP. | S-BU-001, S-BU-002 | Economic beneficiary, budget owner, procurement friction or price. | Contract/economic-buyer interview; current software/process cost and purchase criteria. |
| **Model performance should be the next priority** | **Not yet.** Literature shows many candidate methods; the main uncertainty remains the reachable decision and truth data. | S-ACAD-001…S-ACAD-006, S-INT-001 | Local usefulness. | Resolve H1–H5 and obtain real chronological service labels first. |

| **Real service-truth dataset exists in repo** | **False today.** CS1 classifies historical generated datasets as sandbox-only; IE issue #292 owns privacy-preserving aggregate acquisition. | S-INT-005 | Verified BUCard/SKS export and reconciled served semantics. | Source-owned export → semantic reconciliation → `scripts/cs1_service_truth_artifact_intake.py` → admission result. |

## Promotion rule

A row moves from **secondary-supported hypothesis** to **PMR-supported/contradicted** only when:
1. a real primary artifact/interview exists;
2. its provenance is stored;
3. reported fact vs team interpretation is separated;
4. the relevant `E-INT-*` / operational evidence record is created;
5. contradictory evidence is preserved.

No number of web sources substitutes for this promotion gate.
