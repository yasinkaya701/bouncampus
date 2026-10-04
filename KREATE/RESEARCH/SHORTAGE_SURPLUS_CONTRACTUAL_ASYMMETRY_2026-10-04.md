# Shortage–Surplus Contractual Asymmetry — 2026-10-04

**Purpose:** determine whether the shortage-versus-surplus tradeoff in institutional university dining is merely theoretical or can be encoded directly in contract economics/penalties.  
**Status:** cross-university public procurement evidence. **Not Boğaziçi contract semantics and not PMR evidence.**

## Executive conclusion

Current official Turkish public-procurement evidence shows at least one very strong asymmetric planning structure:

```text
contractor chooses daily quantity from historical demand
+
insufficient production can trigger a penalty
+
payment is based on food actually eaten
+
administration does not bear excess-food risk
+
leftover food cannot be reused in another meal
```

This is a concrete example of a decision where forecast error has **different consequences on the two sides**.

It strongly supports H-C as a plausible market mechanism:

> operators may rationally maintain a safety buffer because shortage and surplus are not symmetric.

It does **not** establish that Boğaziçi/TEMAŞ has the same penalties, payment basis or buffer behavior.

---

# 1. Kırıkkale University — official 2026 Public Procurement Board decision

Official KİK decision:

- University: Kırıkkale University
- Decision: `2026/UH.I-2269`
- Decision date: **26 August 2026**
- Procurement: `2026/1174924`, Malzemeli Yemek Hizmeti

Official source:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

The reproduced Technical Specification states that:

1. daily meal quantities are determined by the **contractor**, considering previous meal counts;
2. if insufficient food is produced, a **penalty** is applied;
3. progress/payment (`hakediş`) is calculated using the number of meals **actually eaten**;
4. the administration is not responsible for food left over from excess production;
5. excess food cannot be reused in another meal;
6. the contractor is expected to account for demand variation associated with academic calendar and menu.

### Why this matters

This creates an explicit operating objective closer to:

```text
minimize expected surplus cost
while avoiding a penalized shortage
```

than to:

```text
minimize forecast MAE
```

---

# 2. Economic structure implied by the example

Under this documented structure, a simplified project-level risk picture is:

## If contractor underestimates demand

Potential consequences:

- inadequate food availability;
- contractual penalty;
- service failure;
- operational recovery burden.

## If contractor overestimates demand

Potential consequences:

- additional food is produced;
- administration does not bear responsibility for excess;
- payment is tied to meals actually eaten;
- remaining food cannot simply be shifted into another meal.

### Research inference

The contractor is exposed to both sides but in different ways.

This can rationally produce an implicit safety margin even if the operator cares about waste.

### Critical boundary

The exact marginal cost and penalty magnitude are not the same thing as a BOUNCAMPUS willingness-to-pay value.

---

# 3. This shows why `accuracy` is an incomplete model objective

Suppose two forecasts have the same MAE:

```text
Forecast A: repeatedly underproduces by 50
Forecast B: repeatedly overproduces by 50
```

Under an asymmetric contract, they are not economically/operationally equivalent.

Candidate decision-loss form:

```text
L(q, D)
  = c_excess * max(q-D, 0)
  + c_shortage * max(D-q, 0)
  + c_service_failure * I(stockout)
```

where all coefficients remain PMR/contract parameters.

### Product consequence

The planning band should reflect:

- shortage tolerance;
- service-level guardrail;
- surplus consequence;
- decision authority.

Not simply model confidence.

---

# 4. Historical demand is contractually expected to inform planning

The same Kırıkkale clause directly references previous meal counts as a planning input.

This makes the true baseline very important.

A new product should compare against:

```text
operator's historical-count heuristic
```

not against an intentionally weak baseline.

If the existing historical-count process performs sufficiently well, the value of additional contextual AI can be low.

---

# 5. Academic calendar and menu variation appear in contract-risk reasoning

The decision states that demand can vary with:

- academic calendar;
- menu.

### Implication

These are not only academic-modeling feature ideas; at least one real university procurement explicitly treats them as sources of quantity uncertainty.

### Boundary

No fixed weight is implied.

The contract does not say:

```text
calendar = 50%
menu = 20%
```

These remain site-specific model questions.

---

# 6. Cross-case comparison

## Kırıkkale

```text
contractor determines quantity
-> paid on actual meals eaten
-> penalty for insufficient production
-> excess risk not administration's
```

## İzmir Katip Çelebi

Current research indicates:

```text
university/admin determines quantity
using reservation + expected walk-ins
-> contractor produces
-> actual electronic/turnstile count supports payment
-> administration not responsible for excess
```

## Sakarya

Current official procurement evidence shows:

```text
university control organization + contractor
can jointly change selected-dish production mix
using historical preference data
```

### Market implication

The same technical forecasting problem can sit in three different governance/economic structures:

```text
contractor-owned
university-owned
joint
```

This reinforces workflow-based segmentation.

---

# 7. H-C evidence boundary

## Secondary evidence supports

> asymmetric shortage/surplus risk **can exist** in Turkish university dining contracts.

## Secondary evidence does not support

> Boğaziçi operators intentionally add a X% safety buffer.

> Boğaziçi shortage is more expensive than surplus.

> TEMAŞ bears all surplus cost at Boğaziçi.

These require target-site PMR/contract evidence.

---

# 8. Target-site PMR questions sharpened by this case

To Boğaziçi Food Services:

- If the contractor produces too little, what happens contractually and operationally?
- If it produces too much, who bears the cost?
- What quantity determines hakediş/payment?
- Can surplus be carried to another service?
- Is there any formal or informal minimum safety margin?
- What happened during the last early sellout or near-stockout?

To TEMAŞ local operations:

- Is the project paid on produced, delivered, served or another quantity?
- Does excess ingredient/production cost stay in project P&L?
- Are there shortage penalties or service-level penalties?
- How much implicit buffer is normally added and why?
- Which dishes/batches carry the highest shortage risk?
- Can the buffer differ by dish/menu/meal period?

---

# 9. QVP consequence

If a similar structure exists at the target site, the best value proposition may not be:

> reduce food waste.

It could become:

> reduce avoidable excess **without increasing penalized/visible shortage risk**.

or, contractor-side:

> improve contribution margin on served-meal contracts while protecting service level.

Both remain hypotheses until target economics are known.

---

# 10. Product-design consequence

A useful recommendation should be able to expose:

```text
expected demand
recommended quantity
lower-risk quantity
surplus-risk estimate
shortage-risk state
active contract/policy constraint
operator override
```

But numerical `cost` or `risk probability` labels must not be shown as calibrated until measured evidence exists.

---

## Current conclusion

The shortage/surplus asymmetry is not merely an optimization-theory convenience; it appears in real Turkish university contract design.

This makes H-C a high-value PMR question and strengthens the case for decision-focused rather than accuracy-only modeling.

The target-site contract remains the decisive evidence.
