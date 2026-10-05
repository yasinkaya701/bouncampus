# Economic Buyer & Incentive Archetypes — Turkish University Dining

**Research date:** 2026-10-05
**Status:** Public procurement / secondary research. This does not establish Boğaziçi's current payment mechanics unless explicitly sourced.

## Why this matters

The same physical problem — uncertain meal demand — can create different economic incentives depending on the contract.

If the wrong actor bears the cost or captures the benefit, BOUNCAMPUS may identify the right operational user but the wrong economic buyer.

## Archetype A — Contractor bears quantity risk

### Kırıkkale University, 2026
Official KIK decision:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

Technical terms described in the decision include:
- daily meal count determined by contractor using previous meal counts;
- penalties if insufficient food is produced;
- progress payment based only on meals actually consumed;
- university not responsible for excess food;
- daily demand variation risk/cost allocated to contractor.

### Economic interpretation

```text
contractor chooses quantity
+ contractor pays/absorbs excess
+ contractor faces shortage penalty
+ revenue tied to realized consumption
```

This creates a direct contractor incentive for better forecast/production decisions.

Potential roles:
- **end user:** contractor production manager / kitchen operations;
- **economic beneficiary:** contractor;
- **institutional gatekeeper:** university procurement/SKS;
- **buyer candidate:** contractor HQ/local project depending software authority.

## Archetype B — Institution determines quantity, contractor executes and protects service

### İzmir Katip Çelebi University, 2026 contract
Public KIK decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2025UH.II-2367-kamu-ihale-karari-kik

The published decision describes:
- production quantity determined by the administration from reservations plus forecasted student/personnel counts;
- contractor must produce the notified quantity;
- contractor must rapidly provide substitute/fast food if demand exceeds planned quantity;
- nobody should be turned away because food ran out;
- excess production / unsold meals are not the administration's responsibility;
- actual diners measured with electronic cards / turnstiles;
- contractor payment based on those realized counts.

### Economic interpretation

This is a split-control model:

```text
institution influences/sets plan
→ contractor executes
→ realized consumption determines settlement
→ contractor still bears at least part of execution/excess/shortage risk
```

Possible product consequence:
- recommendation user may be institution-side;
- economic value may be shared or primarily contractor-side;
- adoption can require both actors.

## Archetype C — Contractor must forecast but procurement data itself is inadequate

### Gebze Technical University, 2026
Public KIK decision mirror:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-962-kamu-ihale-karari-kik

The procurement documentation required the contractor to estimate daily meal counts while the administration was not obliged to pre-notify daily student meal numbers. The Board found that the documents lacked sufficient daily/reference information for a bidder to estimate meal volumes healthily.

### Implication

Demand information quality can be material not only operationally but **during procurement and cost formation**.

Potential value objects may therefore include:
- operational production planning;
- reference-demand evidence;
- transparent data contract between institution and contractor;
- future tender/service-level design.

These are different products/buyers and should not be collapsed without PMR.

## Archetype D — Institution-owned / internally operated dining

Some university dining operations are substantially institution-operated rather than contractor quantity-risk models.

In this archetype, possible economic logic becomes:

```text
institution buys ingredients/labor/capacity
→ institution owns production decision
→ institution absorbs surplus cost
→ institution absorbs shortage/reputation cost
```

This is likely a different sales process from contractor-led operations even if the software interface looks similar.

## 1. Decision-making unit map

For each target institution, PMR must separately identify:

### End user
Person who decides/approves production or batch quantity.

### Champion
Person with enough pain/influence to push a pilot.
Could be:
- Food Services Branch Manager;
- food engineer;
- central-kitchen manager;
- contractor project manager;
- sustainability lead only if operationally connected.

### Economic buyer
Person/unit with authority over budget/procurement.

### Primary beneficiary
Actor that captures:
- avoided ingredient/production cost;
- fewer penalties/emergency-prep costs;
- better service continuity;
- reporting/sustainability value.

### Veto holders
May include:
- SKS/administration;
- contractor HQ;
- procurement/legal;
- IT/data owner;
- food-safety/quality;
- privacy/security.

## 2. PMR questions that resolve buyer economics

Do not ask abstractly `Would this save money?`

Ask:
1. What is the unit used for contractor payment: ordered, produced, delivered, accepted, served, turnstile count, or another basis?
2. Who pays for food prepared but not consumed?
3. Who pays the labor/ingredient cost of emergency replenishment?
4. Are there shortage/late-service/quality penalties?
5. Does reducing prepared quantity reduce the university's bill, contractor's cost, both, or neither?
6. Who has authority to change the planned quantity?
7. Who has budget authority for software / measurement / pilot services?
8. Could the university require a contractor to use a decision tool, or must the contractor buy it independently?
9. When contracts renew, who writes the technical specification?
10. What measurable result would justify procurement or contract inclusion?

## 3. Beachhead consequence

A market is not homogeneous merely because every site is a university cafeteria.

Potential beachhead splits:

### Segment 1 — contractor-risk dining
- contractor controls or materially influences forecast;
- excess cost sits with contractor;
- realized consumption drives settlement.

### Segment 2 — institution-led planning + outsourced execution
- university sets quantity / allocation;
- contractor executes;
- risk allocation is shared.

### Segment 3 — institution-operated kitchens
- operational and economic control reside in same institution.

If sales language, buyer, procurement route or value capture differ substantially, DE methodology says these should be treated as separate segments.

## 4. Most attractive hypothesis

From a pure incentive standpoint, contractor-risk models may have the clearest financial reason to improve demand decisions because they can simultaneously face:
- lost margin from excess production;
- shortage penalties / service recovery;
- revenue based on realized meals.

However this is **not yet a beachhead decision** because:
- contractor software procurement access may be harder;
- incumbent systems may already exist;
- local project teams may lack purchase authority;
- BOUNCAMPUS's campus-context advantage may be weaker/stronger depending data access.

Test through PMR.

## 5. Boğaziçi unresolved boundary

Public sources establish the scale and current contractor identity, but the research has not yet established from authoritative contract text:
- who sets daily meal quantity;
- whether it is revisable and when;
- exact payment quantity semantics;
- who absorbs excess-production cost;
- shortage penalties / replenishment responsibility;
- who captures financial savings from a better forecast.

Until those are resolved, Boğaziçi economic buyer remains `UNKNOWN`.

## 6. Application implication

Safe:
> `Different Turkish university contracts allocate meal-demand risk differently, which is why our PMR is testing both the operational decision owner and who economically benefits from better quantity planning.`

Unsafe:
> `Universities save money whenever fewer meals are produced.`

The latter can be false in contractor-risk models.
