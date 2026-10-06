# Dining Primary-Evidence Closing Packet

**Date:** 2026-10-06  
**Canonical gates:** #292 (BUCard/SKS), #358 (contract/hakediş), #82 (CS1 service-truth admission)

This packet is the smallest source-owner evidence set that closes the remaining dining decision chain without person/card-level data.

## Packet P1 — BUCard/BİDB report sample

**Owner route:** BUCard Office / BİDB  
**Ask for:** one privacy-preserving aggregate sample/export from an existing named dining report surface.

Preserve source-native fields plus, where available:
- service_date
- campus / dining hall
- meal_period
- meal_category
- reported count field name and value
- package-meal field
- report_generated_at / version
- source_report_id
- correction/finality marker

**No person/card/student/staff identifiers.**

**Closes:** #292 A2 only (exportability/access).  
**Does not close:** passage=served, actual_served, payable quantity.

## Packet P2 — SKS/Food Services semantic reconciliation

**Owner route:** Yemek Hizmetleri Şube Müdürlüğü / Yemek Hizmeti Yürütme Kurulu  
**Ask:** field-level explanation for the P1 report:
- what creates one reported event;
- duplicate/retry/refund/reversal treatment;
- second-meal treatment;
- package-meal treatment;
- late correction/finalization rule;
- which report/version is operationally final;
- whether any field means physically served meals.

**Closes:** #292 A3; closes A4 only if an authoritative served field/finality rule is explicitly identified.  
**Unlocks #82:** only A4-qualified served truth may be mapped to `actual_served`.

## Packet P3 — Current contract work-item schedule

**Owner route:** İhale ve Satınalma / İMİD  
**Ask for:** authoritative final 2025/1727143 unit-price schedule and relevant final technical/admin clauses; awarded prices may be redacted if disclosure is restricted.

Must recover:
- all 15 work-item labels;
- unit and quantity;
- 12 labor-row titles and 19/24-month structure;
- 3 meal rows;
- payment/hakediş quantity clause;
- final correction/zeyilname history.

**Closes:** #358 B1/B2 structure.  
**Does not close:** actual monthly payable quantity or daily freeze rights unless clauses explicitly do so.

## Packet P4 — One redacted monthly control→hakediş slice

**Owner route:** Dining Control Organization + relevant Tahakkuk/Harcama Yetkilisi  
**Ask for:** one representative month, sensitive monetary values redacted if needed:
- upstream Control Organization puantaj/icmal/quantity record;
- hakediş work-item quantity/unit fields;
- acceptance/muayene reference;
- correction/deduction/reconciliation record.

Required provenance:
`artifact_id, owner_role, period, campus_scope, meal_period_scope, generated_at/version, authoritative_status, joins_to`.

**Closes:** #358 B3 when the source owner can trace a realized-service quantity into the hakediş work item.

## Packet P5 — Quantity decision/freeze semantics

**Owner route:** SKS/Food Services + Dining Control Organization; contractor operations only for contractor-side mechanics.

Ask:
- who issues initial daily quantity;
- latest reversible timestamp;
- revision/reallocation/batch rule;
- shortage/overproduction handling;
- which record is authoritative after disagreement;
- whether human-reviewed recommendation may alter quantity and under what approval.

**Closes:** #358 B4/B5 only to the extent explicitly evidenced.

## One-service join

Preferred grain:
`service_date × campus × meal_period × meal_category/work_item`.

If an authoritative source is coarser, retain its native grain and document the aggregation. Never fabricate a finer join.

The following remain distinct until source-owner evidence proves equality:

`ordered != produced != passage != served != control_accepted != payable`

## Consumer promotion rules

### CS1 (#82)
- P1 alone: raw source-native feature candidate only.
- P1+P2 A4: reconciled served label may be admitted with provenance.
- P4/P5: enables decision-cutoff and controllable-quantity evaluation.
- No generated/demo/public aggregate data becomes measured local truth.

### CS2
- P3: contract structure only.
- P4: payable-quantity semantics, not automatically savings.
- P5 + measured operational counterfactual: required before defensible impact/economic claims.
- WTP/buyer/adoption remain separate PMR evidence.

### IE/PMR
Every received artifact must record:
- source owner and route;
- acquisition date;
- whether original/redacted;
- native grain;
- semantic status;
- stable reference/checksum where possible;
- exact gates promoted.

## Definition of done

The dining evidence chain is operationally closed only when one real service slice can be traced:

`quantity decision → service report → semantic reconciliation → Control Organization quantity → hakediş payable quantity`

with correction/finality semantics and without relying on inferred equality between those quantities.
