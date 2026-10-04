# KREATE Current Status

**Last updated:** 2026-10-04

This file is current state only. Do not use it as a diary.

## Current objective

Close the highest-value evidence gaps for the October 8 application. Secondary research is now substantially stronger; **real PMR is still the gating item because it carries 40% of the stated rubric and cannot be replaced by web/repo research.**

- **HYPOTHESIS:** high-volume, centrally coordinated/institution-governed university dining is the current beachhead.
- **UNKNOWN:** whether Boğaziçi demand mismatch materially drives avoidable edible surplus and whether the production quantity is reachable before a useful freeze point.
- **PUBLIC SOURCE:** Boğaziçi has a material dining/waste baseline, central production context, formal contractor operation and existing digital/feedback infrastructure (`E-PUB-001`–`E-PUB-005`, `E-PUB-014`).
- **PUBLIC SOURCE:** several Turkish university procurements show that daily meal forecasting, actual-consumption settlement, shortage response and excess-risk allocation are real contract-level mechanisms, but the exact mechanism varies by institution (`E-PUB-006`–`E-PUB-008`, `E-PUB-012`, `E-PUB-013`).
- **FACT:** the repository has a falsifiable pilot protocol and human-reviewed decision policy (`E-REP-001`–`E-REP-004`).

## Rubric coverage status

| Rubric area | Current status | Current evidence | Highest-value remaining gap | Owner |
| --- | --- | --- | --- | --- |
| Team — 20% | IN PROGRESS | role structure exists | human-verified capability examples + final sign-off | CS2 |
| Problem — 20% | STRONG SECONDARY / PMR MISSING | E-PUB-001–008, E-PUB-012–014 | concrete target-workflow incidents proving cause, frequency, consequence and current workaround | IE |
| Beachhead — 10% | TESTING | Turkish procurement mechanisms + ICP research | repeated workflow/customer evidence at multiple institutions | IE |
| Persona — 10% | UNKNOWN | E-PUB-011 gives governance anchor only | verify actual quantity owner/user/buyer/beneficiary | IE |
| PMR — 40% | CRITICAL GAP | no `E-INT-*` evidence registered | conduct and document real interviews; show what changed | Shared; CS2 synthesis |
| Solution evidence | TECHNICALLY PREPARED / MARKET UNVALIDATED | E-REP-001–004 + academic research | prove workflow fit, data access and measurable operational value | CS1/EE/IE |

## Research completed / consolidated

- public Boğaziçi waste/service/central-production baseline;
- source-reconciliation matrix for conflicting capacity/service/waste semantics;
- 2026–2027 procurement scale + contractor mapping;
- Turkish university procurement taxonomy across different quantity/payment-risk structures;
- falsification-first PMR hypothesis matrix;
- role-owned Boğaziçi PMR target map;
- beachhead ICP/pilot-promotion gate;
- competitor capability matrix (Winnow / Leanpath / Emissary / status quo);
- decision-signal and data-readiness map;
- academic demand-modeling evidence and evaluation rules;
- TrayGate/visual-leftover academic feasibility boundaries;
- KVKK/data-minimization design boundaries;
- expanded public evidence registry without promoting secondary evidence into PMR.

See [`RESEARCH/README.md`](./RESEARCH/README.md) for the canonical research index.

## Current PMR hypotheses

### H-A — controllable decision

A named operator determines/approves production quantity before demand is known and has a non-zero adjustment window before a freeze point.

### H-B — material mismatch

Demand/planning mismatch repeatedly creates addressable edible surplus and/or shortages that can be affected by changing the production decision.

### H-C — asymmetric risk

Shortage is sufficiently costly/visible that operators use an explicit or implicit safety buffer based on historical experience/fragmented information.

These are **not supported yet** merely because analogous procurement structures exist elsewhere.

## Top evidence gaps — ordered by decision value

1. **Boğaziçi/TEMAŞ quantity owner** — university, contractor or joint?
2. **Freeze point / batch structure** — when does a change become costly/irreversible; can later batches react?
3. **Waste-stage split** — edible surplus vs prep vs plate/post-consumer waste.
4. **Settlement quantity** — ordered, produced, delivered, served/turnstile or another contract quantity?
5. **Excess/shortage incentive** — who bears financial/operational consequence?
6. **Service-level data availability** — planned/produced/served/surplus/sellout by campus x meal x date.
7. **Aggregate BUCard/turnstile semantics/access** — retention, duplicates, privacy-safe export.
8. **Current incumbent workflow** — spreadsheet/heuristic/software and what remains unresolved.
9. **Repeatability** — same mechanism at at least 2 additional target institutions.
10. **Adoption criteria** — what would cause the operator to trust, ignore or reject the recommendation?

## Immediate execution priority

```text
Food Services workflow owner
    ↓
TEMAŞ local production/project owner
    ↓
food engineer / daily operator
    ↓
BUCard/IT data owner
    ↓
waste measurement owner
    ↓
second/third university same-role interviews
```

Each real interview must use `PMR/INTERVIEW_TEMPLATE.md` and promote only narrow supported/contradicted claims into `EVIDENCE.md` as `E-INT-*`.

## Current kill/modify gates

Modify or kill the pre-service production wedge if repeated PMR shows:

- quantity is not a reachable decision;
- the useful freeze point does not exist;
- addressable edible surplus is not material;
- waste is mainly caused by a different controllable stage;
- shortage/safety constraints make quantity reduction unacceptable;
- outcomes cannot be measured at acceptable effort;
- an incumbent system already solves the decision adequately;
- no reachable sponsor captures enough operational/economic value.

## Claim firewall

Do not submit as fact before measured/PMR evidence:

- demand mismatch caused X% of Boğaziçi's 48,251 kg waste;
- BOUNCAMPUS has reduced waste/cost/CO2/water;
- current model accuracy on real cafeteria production data;
- live BUCard/POS/production access;
- TrayGate gram-level accuracy;
- competitor lacks a capability not directly verified;
- all Turkish universities are one market;
- 208 universities = 208 buyers/TAM.

## Latest KEEP / MODIFY / KILL decisions

| Decision ID | Outcome | Current decision |
| --- | --- | --- |
| D-001 | KEEP | October 8 is an evidence/application gate; PMR outranks extra demo polish. |
| D-002 | KEEP | Keep institutional dining as a **beachhead hypothesis**, not validated market. |
| D-003 | KEEP | Use existing institutional systems first; add sensing only for decision-critical missing measurements. |
| D-004 | MODIFY | Do not position differentiation as `AI forecasting` or `waste vision`; mature competitors already offer these categories. Test decision timing + university context + provenance + uncertainty + human action + verification instead. |
| D-005 | MODIFY | Define beachhead by quantity-decision/payment/measurement workflow, not merely `large Turkish universities`. |
| D-006 | KILL | Unsupported savings, first/only claims, fake live-data language, and external-study performance transfer are not allowed. |

See [DECISIONS.md](./DECISIONS.md) for durable decision records.