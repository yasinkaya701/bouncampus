# CS2 Application Claim → Missing Fact → Falsifier Map

**Date:** 2026-10-06  
**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Status:** application/pitch guardrail. Not PMR evidence, measured impact, or customer validation.

This file translates the current product narrative into falsifiable primary-evidence requirements. It complements `KREATE/PMR/CLAIM_SOURCE_MATRIX.md` and does not replace the canonical source catalog.

| ID | Candidate application claim | Current status | Missing primary fact | Best stakeholder / artifact | Falsifying answer or result | Safe current wording |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | “We use AI to predict cafeteria demand.” | Technically plausible but **not differentiated**. | Is there a reachable pre-freeze decision where a recommendation improves current practice? | Food Services quantity owner + contractor production planner; one reconstructed recent service. | Quantity is already fixed before useful signals arrive, or current process is adequate. | “We are testing whether decision-time signals can improve a reachable production/allocation decision.” |
| C-02 | “Our forecasting is unique.” | **Contradicted** by established academic work and Winnow Foresight. | What unresolved workflow/control-point gap is not solved by generic forecasting? | Operator + buyer interviews; incumbent workflow map. | Existing tool/process solves the same decision with acceptable effort and quality. | “Differentiation must come from local decision integration, semantics and verification—not forecasting alone.” |
| C-03 | “We reduce food waste.” | **Unproven locally.** | What fraction of current waste is unserved surplus/addressable by quantity decisions? | Stage-separated measurement + recent incident reconstruction. | Dominant waste is preparation/plate waste or otherwise outside the decision. | “The pilot will test whether reducing avoidable overproduction lowers measured surplus without raising shortage.” |
| C-04 | “We will reduce waste by X%.” | **Forbidden before intervention evidence.** | Prospective control/intervention outcome with predefined measurement boundary. | Measured pilot dataset + protocol + independent review. | Effect is null/unstable, measurement quality is inadequate, or shortage worsens. | Use a target only: “We will measure change prospectively; no reduction percentage is claimed yet.” |
| C-05 | “We save ₺X / cut food cost.” | **Unsupported.** | Who economically captures avoided excess, and how settlement/payment changes when quantity changes. | Procurement/contract owner + TEMAŞ finance/operations + authoritative contract/specification. | Buyer does not capture savings, price/acceptance mechanics decouple from avoided production, or shortage costs dominate. | “Economic value depends on verified contract and settlement mechanics; no savings amount is claimed.” |
| C-06 | “BUCard/turnstile/reservation data tells us demand.” | **Unverified semantics.** | Event definitions, timing, corrections, duplicates/no-shows and relation to served meals. | Data owner + data dictionary + aggregate export + reconciliation sample. | Signal arrives after freeze, cannot be exported, or does not reconcile to service truth. | “These are candidate intent/access signals pending source-owner semantic verification.” |
| C-07 | “No new hardware is needed.” | Conditional. | Are existing records sufficient to measure the outcome and distinguish waste stages? | Data owner + waste measurement owner + sample export/observation. | Existing records cannot produce trustworthy service-level outcome truth. | “We prefer existing aggregate records; new sensing is justified only for a decision-critical measurement gap.” |
| C-08 | “Our computer-vision waste tracking is unique.” | **Contradicted/commoditized broadly.** | Is vision required for a local missing field that incumbents/current records do not cover? | Waste owner + EE/EHB measurement review + incumbent-stack inventory. | Existing records/scales or mature tools cover the field adequately, or camera/privacy burden exceeds decision value. | “Vision is optional measurement infrastructure, not the product thesis.” |
| C-09 | “We provide a campus sustainability dashboard.” | Broad novelty claim **unsafe**. | Does a buyer need a specific operational evidence workflow not already handled by reporting systems? | Sustainability/reporting owner + buyer. | Dashboard/reporting need is already satisfied and does not alter a decision. | “Reporting is a by-product of verified operational records, not the primary wedge.” |
| C-10 | “Boğaziçi’s procurement proves the market.” | **Unsupported.** | Can a decision-support/data product be purchased/approved, by whom, through what path, and with what incentive? | Procurement owner + SKS approver + contractor-side decision maker. | No viable approval/budget path or buyer/beneficiary split blocks adoption. | “The public tender establishes a large contracted food-service operation, not software demand or WTP.” |
| C-11 | “TEMAŞ is paid per actual served meal.” | **Unknown.** | Exact hakediş/acceptance basis and authoritative unit-price schedule. | Current contract/specification + acceptance/payment owner. | Payment is based on another accepted quantity or fixed/committed mechanism. | “The public notice establishes unit-price contracting, but the accepted payment quantity is still unknown.” |
| C-12 | “5,000 meals/day is Boğaziçi’s demand.” | **False framing.** | None needed to reject the wording; public notice labels this as a bidder capacity criterion tied to half the administration’s stated daily need. | Current tender notice. | Already falsified as a measured-demand claim. | “5,000 meals/day is a qualification threshold, not measured served demand.” |
| C-13 | “The same product scales to other universities.” | **Unproven.** | Second-site owner/freeze/signal/action/payment chain with the same product boundary. | Mature-operation site + reservation-first counter-archetype site. | Decision topology differs enough to require another product/workflow. | “Repeatability is a PMR hypothesis; one second-site match and one counter-archetype must be tested.” |
| C-14 | “Forecast accuracy is the main KPI.” | **Rejected as product KPI.** | Does a better forecast produce a better approved action and physical outcome? | Shadow/advisory pilot records. | More accurate prediction does not change decisions/outcomes or increases shortage risk. | “Decision utility, coverage, override behavior, surplus and shortage guardrails matter more than forecast score alone.” |
| C-15 | “Academic/vendor results show what BOUNCAMPUS will achieve.” | **Forbidden transfer.** | Local measured evidence under the actual workflow. | Local pilot + admitted artifacts. | Local effect is smaller, absent or opposite. | “External studies justify testing mechanisms; they do not predict local impact.” |

## Pitch/application promotion gate

Before any quantitative or strong comparative claim enters a deck/application:

1. identify its evidence class;
2. name the exact source/artifact;
3. state the scope the source actually supports;
4. state the missing primary fact;
5. state the falsifying answer/result;
6. keep unsupported numbers out;
7. preserve competitor overlap;
8. preserve shortage/service-risk guardrails;
9. require prospective local measurement for impact;
10. use KEEP / MODIFY / KILL after evidence review.

## Current CS2 narrative

The strongest current narrative is:

```text
BOUNCAMPUS is not “another cafeteria forecasting model.”

It is a decision-support and verification loop that tests whether
already-available pre-service signals can improve one reachable quantity decision
before freeze, while preserving operator control, reconciling signal semantics,
and measuring both surplus and shortage prospectively.
```

That narrative itself remains conditional on real PMR and operational artifacts.
