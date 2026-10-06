# KREATE Application Rubric Closure

**CS2 owns final synthesis. Domain owners must sign off factual claims in their area before submission.**

A section is not complete because prose exists. It is complete when the required evidence is traceable and the relevant owner/reviewer can defend it.

## Team — 20%

| Field | Current state |
| --- | --- |
| Evidence required | Human-verified team roster; complementary role/capability evidence; concrete ownership; evidence that the team can execute customer discovery and technical validation. |
| Owner | CS2 synthesis; each teammate signs off their own role/capability claims. |
| Current evidence IDs | — |
| Gap | Application-ready proof/examples of complementary execution are not yet registered in this KREATE evidence system. |
| Next action | Each teammate supplies concise verifiable capability evidence; CS2 removes generic team-superlative language. |
| Red-team question | If names/university titles were removed, what concrete evidence shows this team can discover the problem and execute the proposed next step? |

## Problem — 20%

| Field | Current state |
| --- | --- |
| Evidence required | Public/operational baseline plus multiple concrete last-incident stories showing severity, frequency, cause, current workflow, workaround, and failure consequence. |
| Owner | IE; EE/CS1 sign off technical/measurement claims. |
| Current evidence IDs | E-PUB-001, E-REP-001 |
| Gap | Public waste existence is not evidence that demand mismatch or the proposed intervention point is the root cause. |
| Next action | Interview operators/stakeholders using last-concrete-incident questions; create `E-INT-*` evidence that supports or contradicts `H-002`/`H-003`. |
| Red-team question | What evidence proves the problem is the production decision rather than menu quality, procurement, serving policy, leftovers, events, or another cause? |

## Beachhead Market — 10%

| Field | Current state |
| --- | --- |
| Evidence required | Evidence that a narrow institutional-dining segment shares the problem, is reachable for PMR/pilot, has a coherent decision workflow, and is meaningfully better as a first segment than broader alternatives. |
| Owner | IE; CS2 synthesis. |
| Current evidence IDs | E-REP-003 (current repo positioning only) |
| Gap | No interview evidence is registered yet to validate the beachhead. |
| Next action | Sample stakeholders across the proposed segment and record repeated/common versus institution-specific patterns. |
| Red-team question | Why is this a beachhead instead of simply the campus where the team happens to have context? |

## Persona — 10%

| Field | Current state |
| --- | --- |
| Evidence required | Verified decision owner/influencer; trigger; workflow; data used; authority; success metric; failure risk; objections; current workaround. |
| Owner | IE; domain owners sign off workflow/technical details. |
| Current evidence IDs | — |
| Gap | `H-005` is `UNKNOWN`; generic labels such as “sustainability office” or “cafeteria operator” are insufficient without decision evidence. |
| Next action | Ask every relevant interview who made the last production decision, who approved it, what data they used, and what happened when it was wrong. |
| Red-team question | Who can actually change the number of portions prepared, and what would make that person ignore our recommendation? |

## Primary Market Research — 40%

| Field | Current state |
| --- | --- |
| Evidence required | 16 distinct target interviews (hard minimum 12), documented with concrete incidents, current workflow, decision owner, data, risks, workarounds, exact quotes where useful, objections, referrals, and explicit changes to assumptions/product. |
| Owner | Shared: IE 4, EE 4, CS1 4, CS2 4; CS2 owns final synthesis. |
| Current evidence IDs | — |
| Gap | At bootstrap, no completed interview evidence is registered in the repository tracker; any conversations outside the repo remain `UNKNOWN` until documented. |
| Next action | Schedule, conduct, document, and evidence-link interviews. Prioritize depth and decision-relevant stories over raw count. |
| Red-team question | Which three beliefs changed because of PMR, and can every claimed change be traced to actual interview artifacts rather than team intuition? |

## Evidence admissibility

These are review rules, not claims about the market:

| Claim kind | Admissible primary evidence | Not sufficient by itself |
| --- | --- | --- |
| Public baseline / institutional fact | `PUBLIC_SOURCE` | Repo copy that repeats the number |
| Customer workflow / pain / persona / objection | `INTERVIEW` | `REPO_ARTIFACT`, model output, team intuition |
| Technical feasibility / measured behavior | `TECH_TEST` | Planned architecture or unexecuted protocol |
| Model/scenario output | `MODEL_RESULT` and label `MODEL ESTIMATE` | Describing the output as measured reality |
| Current repository/product state | `REPO_ARTIFACT` | Treating repository positioning as market validation |
| Achieved savings / impact | Measured operational result with traceable method; later climate conversion must document its factor | `MODEL_RESULT`, demo data, target, or policy heuristic |

A market claim may use public/repository evidence as context, but customer/problem/persona validation cannot be promoted solely from product documentation.

## Submission claim ledger

Every **material application claim** must appear here before final copy/paste. `DRAFT` means it is not submission-ready. `READY` requires a named domain owner and a second human reviewer. `CUT` preserves the decision to remove a claim rather than silently deleting the evidence trail.

Allowed labels: `FACT`, `PUBLIC SOURCE`, `INTERVIEW EVIDENCE`, `TECHNICAL TEST`, `MODEL ESTIMATE`, `POLICY HEURISTIC`, `HYPOTHESIS`, `UNKNOWN`.

| Claim ID | Claim | Label | Evidence IDs | Domain owner | Human reviewer | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | Boğaziçi University publishes an official campus food-waste tracking source. | PUBLIC SOURCE | E-PUB-001 | IE | TODO — independent reviewer | DRAFT | Source existence is registered. Re-open the official page and verify date/current values before any numeric claim becomes READY. |
| C-002 | The current repository implements human-reviewed decision readiness, abstention, transparent baselines and pilot evidence-quality gates. | FACT | E-REP-004 | CS1 | TODO — independent reviewer | DRAFT | Repo-state claim only; it does not prove operator adoption, measured accuracy or operational impact. |
| C-003 | The repository contains a proposed falsifiable CONTROL/INTERVENTION food-waste pilot protocol with guardrails. | FACT | E-REP-002 | EE | TODO — independent reviewer | DRAFT | Protocol existence is real; pilot execution and effect are not. |
| C-004 | The current repository/application positions institutional dining as the working product wedge. | FACT | E-REP-001, E-REP-003 | CS2 | TODO — independent reviewer | DRAFT | Positioning is not customer or beachhead validation. |
| C-005 | A material, still-reversible pre-service quantity/batch/allocation decision exists at Boğaziçi. | HYPOTHESIS | — | IE | TODO — independent reviewer | DRAFT | Blocked on a recent-service reconstruction: owner, decision object, revision rights and freeze point. Route through #358 / CS2 claim gate. |
| C-006 | Demand mismatch is a material cause of avoidable Boğaziçi food waste. | HYPOTHESIS | — | IE + EE | TODO — independent reviewer | DRAFT | Public waste totals establish waste existence, not causal stage or mechanism. Requires incident + stage-separated primary evidence. |
| C-007 | Privacy-minimized service-level operational truth is exportable and semantically usable for CS1. | UNKNOWN | — | IE + CS1 | TODO — independent reviewer | DRAFT | Blocked on #292/#82: aggregate export, data dictionary, timestamps, corrections and reconciliation. |
| C-008 | The intended operational user can safely act on a BOUNCAMPUS recommendation before freeze. | HYPOTHESIS | — | IE | TODO — independent reviewer | DRAFT | Persona, authority, trust threshold, approval path and override behavior remain primary-evidence questions. |
| C-009 | The same product boundary repeats at a second institutional dining site. | HYPOTHESIS | — | IE + CS2 | TODO — independent reviewer | DRAFT | Requires a second-site reconstruction with comparable owner/freeze/signal/action/buyer topology. |
| C-010 | “BUCard/turnstile count equals meals physically served.” | UNKNOWN | — | IE + CS1 | — | CUT | Forbidden equivalence until source-owner semantics and reconciliation prove a narrower relationship. |
| C-011 | “BOUNCAMPUS has reduced food waste by 10%.” | UNKNOWN | — | EE + CS2 | — | CUT | The 10% value is only a proposed/illustrative pilot threshold; no achieved local result is registered. |
| C-012 | “BOUNCAMPUS has already produced local cost, CO2 or water savings.” | UNKNOWN | — | CS2 + EE | — | CUT | No admitted local measured effect exists; impact conversion is downstream of measured waste reduction. |
| C-013 | “Generic AI demand forecasting is BOUNCAMPUS's unique moat.” | UNKNOWN | — | CS2 | — | CUT | Do not use broad novelty language; canonical CS2 product strategy treats generic forecasting as non-differentiating. |
| C-014 | “Public tender scale proves buyer willingness-to-pay or favorable contract economics.” | UNKNOWN | — | IE + CS2 | — | CUT | Blocked on #358 authoritative acceptance/hakediş, beneficiary and purchase-path evidence. |
| C-015 | “BOUNCAMPUS is already validated to scale across universities.” | UNKNOWN | — | CS2 | — | CUT | Current portability is a repeatability hypothesis, not a validated market claim. |

### Claim promotion rules

1. Raw notes/model output/test logs are not application evidence by themselves.
2. A claim is promoted only after the relevant artifact is represented in `EVIDENCE.md` or explicitly remains `HYPOTHESIS`/`UNKNOWN`.
3. `INTERVIEW EVIDENCE`, `PUBLIC SOURCE`, `TECHNICAL TEST`, and `MODEL ESTIMATE` labels must have evidence of the matching type.
4. A `READY` claim must have a named domain owner and a different human reviewer where practical.
5. Unsupported superlatives, impact numbers, percentages, live-data language, or calibrated-confidence wording are rewritten or cut.
6. Contradictory evidence must stay visible; PMR is not a vote-counting exercise.

## Final claim sign-off

Before submission, CS2 must verify:

1. every material factual/market claim is represented in the submission claim ledger;
2. every material factual/market claim has an evidence ID or is visibly labeled `HYPOTHESIS`/`UNKNOWN`;
3. each domain owner has reviewed claims in their area;
4. AI-generated application prose has a named second-human reviewer;
5. unsupported percentages, savings, model confidence, live-data claims, and pilot outcomes are removed;
6. the final application describes what PMR changed, not merely how many interviews occurred;
7. `python scripts/kreate_check.py --submission` passes on the exact submission commit;
8. the final text is manually compared against the evidence registry after the validator passes.
