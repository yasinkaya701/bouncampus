# PMR-A Primary-Evidence Unlock Matrix

**Updated:** 2026-10-06  
**Scope:** #292, #358 and their CS1/CS2/EE/EHB consumers.  
**Boundary:** this is a decision gate, not evidence. A row becomes unlocked only from a source-owned response or authoritative artifact with provenance.

| Gate | Minimum evidence | Unlocks | Still does not prove | Consumer |
| --- | --- | --- | --- | --- |
| A1 BUCard report existence | source owner confirms named dining report + report identifier/schema | request can target an existing report rather than generic export discovery | export permission; served-meal semantics | IE |
| A2 Aggregate exportability | source owner provides/approves privacy-safe campus × meal-period × service-date aggregate with timestamp/source ID | candidate measured input can enter CS1 intake quarantine | `actual_served`; finality | IE → CS1 |
| A3 Reconciliation semantics | SKS/BİDB explain retry/refund/reversal/second-meal/package handling and authoritative final report/version | source-native count may be mapped to an accepted semantic field | produced quantity; surplus; shortage | IE → CS1 |
| A4 Served-truth admission | authoritative owner explicitly identifies which reconciled field means physically served/accepted meals, with finalization semantics | `actual_served` admission for SERVICE_TRUTH_V1 | production or waste outcomes | CS1 |
| A5 Outcome linkage | source-owned produced + surplus/waste + shortage/early-sellout records can be joined by service ID/date/campus/period | decision-loss benchmark and shortage/surplus asymmetry | causal model lift | CS1/EE |
| B1 Current contract bundle | authoritative 2025/1727143 admin + technical specs + correction/addendum history | current-clause interpretation | operational practice if contract differs from execution | IE/CS2 |
| B2 Unit-price schedule | authoritative awarded/current work-item schedule | work-item/unit-price basis | actual payable daily quantity; margin; savings | IE/CS2 |
| B3 Acceptance/hakediş semantics | source-owned muayene-kabul/hakediş form + owner explanation of accepted/payable count and record precedence | accepted/payable quantity wording; settlement actor map | software buyer/WTP | IE → CS2 |
| B4 Freeze/change rights | source owner identifies last reversible production/allocation point and governing record | product intervention/control point | willingness to adopt | IE/CS1/CS2 |
| B5 Risk ownership | authoritative clause or owner response identifies who bears overproduction, shortage and penalties | bounded economic-beneficiary hypothesis | WTP; savings magnitude | CS2 |
| C1 Measurement gap | existing manual/scale/report inventory shows a decision-critical outcome field is absent/unreliable | bounded EE/EHB sensing requirement | sensor ROI or deployment approval | EE/EHB |
| C2 Buyer authority | primary evidence identifies pilot approver, economic buyer, procurement approver and veto separately | buyer/persona claims | budget/WTP unless separately stated | CS2 |

## Fail-closed promotion rules

1. A public webpage or activity report can establish owner/routing/report existence, but cannot satisfy A2–A5 or B3–B5 by itself unless it contains the authoritative field/semantic evidence.
2. User-facing passage history is not a service-truth export.
3. Reservation is intent unless reconciled to served truth.
4. A unit-price contract or unit-price schedule does not by itself reveal the accepted operational count.
5. Operational authority, hakediş signature authority, pilot approval and software purchasing authority are separate facts.
6. Generated repository rows remain `GENERATED_SANDBOX` and cannot unlock any primary-evidence gate.
7. A denied or unavailable export is a valid PMR result: record the denial and redesign the measurement/data plan rather than fabricating a substitute.

## Handoff behavior

- **IE:** return gate ID + provenance + exact source-native wording/field names.
- **CS1:** admit only A4/A5-qualified outcome fields; keep A2/A3 data quarantined with source-native names.
- **CS2:** keep savings/WTP/buyer/economic-benefit wording blocked until the corresponding B/C gates are satisfied.
- **EE/EHB:** open sensing work only after C1, and target the demonstrated missing field rather than a generic camera/sensor concept.
- **PMR-A:** maintain contradictions, gate state and cross-role deltas; do not create duplicate acquisition lanes.
