# Boğaziçi 2025 Dining Tender Reissue Delta — Cancelled vs Successful Procedure

**Research date:** 2026-10-01  
**Purpose:** Compare Boğaziçi's cancelled 2026–2027 dining tender (`2025/1335958`) with the later successful reissue (`2025/1727143`) so agents do not copy clauses, line-item structure or economics across procedures that the University itself treated as materially different.  
**Status:** Secondary/public-procurement research. **NOT a reconstruction of the signed current technical specification. NOT legal advice.**

---

# 0. Executive conclusion

Boğaziçi ran two procurement procedures for essentially the same 2026–2027 dining-service period.

The first procedure was cancelled after objections to the tender documents led the administration to conclude that some specification provisions **had to be changed** and an EKAP amendment could not be issued at that stage.

The later reissue preserved the three headline meal quantities:

```text
380,000 breakfast/sahur
2,500,000 student meals
250,000 staff meals
```

but public bid-schedule mirrors show a major structural difference:

```text
CANCELLED 2025/1335958
public schedule surface: 3 meal line items

SUCCESSFUL 2025/1727143
public schedule surface: 15 items
= same 3 meal lines
+ 12 additional rows rendered as month-unit (Ay) items
```

The open-web parser does not reliably expose the descriptions of those 12 additional rows. Therefore this pack **does not name or classify them**.

What the delta safely establishes is:

> the current successful procurement cannot be treated as merely the cancelled procurement with a new IKN.

At minimum, the public bid-schedule structure changed materially while headline meal volumes stayed constant.

This strengthens two hard rules:

1. never copy a clause from the cancelled `2025/1335958` into the current TEMAŞ contract without direct current-document verification;
2. never divide the successful contract total by the 3.13M headline meals and call the quotient a verified meal cost, because the successful schedule publicly contains additional time/month-based line items whose economic role must be identified first.

---

# 1. Procedure timeline

## REISSUE-01 — Cancelled first procedure

**IKN:** `2025/1335958`  
**Announcement:** 08.09.2025  
**Tender date:** 07.10.2025  
**Planned service:** 01.01.2026–31.12.2027  
**Status:** cancelled.

Public EKAP-derived notice states that objections to the procurement documents were evaluated and that changes to provisions in the specifications were found necessary. Because an amendment (`zeyilname`) could not be issued through EKAP at that stage, the tender authority cancelled the procedure.

Sources:

- https://ekapveri.com/ihale/ekap-2025-1335958/
- https://www.ihaledetay.com/2025-1335958

### Evidence meaning

This is stronger than a generic administrative cancellation.

It directly tells us:

```text
old procurement documents
!=
acceptable final procurement documents
```

But the public cancellation notice does not reveal which exact clauses triggered the required changes.

---

## REISSUE-02 — Successful reissued procedure

**IKN:** `2025/1727143`  
**Announcement:** 17.10.2025  
**Tender date:** 17.11.2025  
**Contract date:** 25.12.2025  
**Service:** 01.01.2026–31.12.2027  
**Contractor:** TEMAŞ Gıda Sanayi ve Ticaret A.Ş.  
**Contract value:** 759,537,563.59 TRY.

Sources:

- https://ekapveri.com/ihale/ekap-2025-1727143/
- https://www.ihaledetay.com/2025-1727143

The reissue itself is also publicly marked as having a correction notice (`Düzeltme İlanı`).

### Consequence

Even within the successful procedure, procurement documents evolved.

Agents should therefore attach **IKN + document version/date** to every extracted contract fact.

---

# 2. Headline meal quantities stayed constant

Public notices for both procedures show the same three headline quantities:

| Meal class | Cancelled `2025/1335958` | Successful `2025/1727143` |
| --- | ---: | ---: |
| Breakfast / sahur | 380,000 | 380,000 |
| Student meal | 2,500,000 | 2,500,000 |
| Staff meal | 250,000 | 250,000 |
| **Headline total** | **3,130,000** | **3,130,000** |

### Important interpretation

The cancellation/reissue was **not simply a headline demand-volume reset**.

Material document changes happened while the published top-level meal quantities remained unchanged.

That makes it even less defensible to infer what changed from headline quantities alone.

---

# 3. Public bid-schedule surface changed from 3 to 15 items

## REISSUE-03 — Cancelled procedure public schedule

The public tender-schedule mirror for `2025/1335958` exposes only:

```text
Öğrenci Kahvaltı — 380,000 öğün
Öğrenci Yemek    — 2,500,000 öğün
Personel Yemek   — 250,000 öğün
```

Source:

https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4173515/cetvel/

## REISSUE-04 — Successful procedure public schedule

The corresponding public surface for `2025/1727143` identifies **15 schedule items**.

It contains the same three meal lines plus 12 additional rows rendered by the public parser as `Ay`-based entries with quantities such as 19 or 24 months.

Source:

https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4374218/

### Parser limitation

The public page does **not reliably expose the descriptions** of those 12 rows. The rendered table has apparent column/description loss.

Therefore do NOT infer that the rows are:

- labor;
- management;
- vehicle;
- equipment;
- staff roles;
- rent;
- another specific category.

Only the following are safe:

```text
successful public schedule item count = 15
meal rows visibly identifiable = 3
additional rendered month-based rows = 12
exact descriptions = UNRESOLVED
```

---

# 4. Why this matters for contract economics

The successful contract value is approximately 759.5M TRY.

A mechanical calculation:

```text
759,537,563.59 / 3,130,000 ≈ 242.66 TRY
```

is only a quotient.

The tender delta makes it even clearer that this is **not automatically**:

- student-meal unit price;
- staff-meal unit price;
- marginal meal cost;
- subsidy per meal;
- contractor ingredient cost;
- avoided cost of one less produced meal.

The successful bid schedule contains more than the three headline meal lines.

### Required economic decomposition

Before using TRY impact, obtain:

```text
winning line-item descriptions
winning line-item unit prices
which line items are quantity-linked
which line items are time/fixed-linked
price-adjustment rules
Q_HAKEDIS per line item
penalty/deduction structure
```

This should be joined to the `TURKIYE_PUBLIC_SERVICE_HAKEDIS_FRAMEWORK.md` pack.

---

# 5. Why this matters for clause provenance

The cancelled tender was abandoned specifically because tender-document objections required changes.

Therefore the current-procurement evidence hierarchy should be:

```text
C1 current signed contract / final technical specification
C2 current final administrative specification / final bid schedule
C3 current owner-confirmed control/hakediş records
C4 current successful public notice/result
C5 cancelled 2025 predecessor documents
C6 older Boğaziçi historical procurements
C7 other-university precedents
```

### Hard rule

A clause from `2025/1335958` may only be used as:

> `CANCELLED PREDECESSOR — question-generation evidence`

Never as:

> `CURRENT TEMAŞ CONTRACT FACT`.

---

# 6. The delta sharpens the current artifact request

The minimum comparison artifact is not the entire procurement bundle.

Ask for the **final successful unit-price schedule** with:

```text
LINE_ITEM_NO
LINE_ITEM_DESCRIPTION
UNIT
PLANNED_QUANTITY
WINNING_UNIT_PRICE
```

Then classify each line item:

```text
MEAL_VOLUME_LINKED
TIME_OR_PERIOD_LINKED
OTHER_FIXED_OR_SERVICE_COMPONENT
UNKNOWN
```

Do not classify until the description is verified.

### Next artifact

For one meal line item, inspect the quantity used in a real monthly hakediş:

```text
LINE_ITEM
PLANNED_CONTRACT_QTY
MONTHLY_HAKEDIS_QTY
UNIT_PRICE
DEDUCTION_IF_ANY
SOURCE_RECORD
```

This converts the procurement from headline economics into an operational decision model.

---

# 7. Reissue comparison questions for Food Services / procurement owner

Do not ask for confidential bidder information.

Ask:

1. The first 2026–2027 tender was cancelled because specification changes were necessary. Which **categories of requirement** materially changed before the reissue?
2. The public schedule for the successful tender contains more rows than the initial three meal lines. What do the additional line items represent?
3. Which line items vary with the number of meals actually accepted?
4. Which line items are paid by month/time regardless of meal volume?
5. Does reducing physical overproduction change the University's payment, the contractor's internal variable cost, both, or neither for each component?
6. Was any daily quantity / acceptance / staffing / service-channel provision changed between the cancelled and successful procedures?
7. Which final document/version should the team cite for current quantity and payment semantics?

### Why this interview matters

A single answer can prevent a false savings model built on the wrong cost denominator.

---

# 8. Product implications by possible line-item structure

These are scenarios, not current facts.

## Scenario A — meal-volume line dominates variable payment

Potential:

```text
better Q decision
→ lower accepted meal quantity where excess avoided
→ possible university + contractor value
```

Still requires `Q_HAKEDIS` verification.

## Scenario B — significant time/fixed service components

Potential:

```text
physical food reduction
→ contractor ingredient/waste benefit
but
→ smaller immediate university invoice change
```

The buyer/user economic story may differ.

## Scenario C — contractor receives meal unit price on validated consumption

Potential:

```text
excess production mainly contractor P&L risk
```

Contractor may be the strongest direct user.

## Scenario D — university call-off/accepted delivery drives meal payment

Potential:

```text
quantity planning may affect university spend more directly
```

Do not select a scenario without final schedule + hakediş evidence.

---

# 9. Research value for P0-05 current operator baseline

The reissue delta does **not** expose the current forecasting heuristic.

No reliable public source found in this research cycle states that current TEMAŞ/Food Services uses:

- previous same weekday;
- moving average;
- BUCard forecast;
- reservation count;
- fixed quantities;
- another explicit formula.

Therefore:

```text
CURRENT_OPERATOR_BASELINE = UNKNOWN
```

This is an important result, not a gap to fill by guessing.

P0-05 still requires a current operator incident walkthrough:

> For tomorrow's lunch, what number did you start from, which data did you look at, what adjustment did you make, and when was it locked?

---

# 10. Safe narrative

### Safe

> Boğaziçi cancelled its first 2026–2027 dining procurement because tender-document objections required specification changes. The later successful procurement retained the same headline meal quantities but public bid-schedule mirrors expose a larger line-item structure. The team is therefore treating the final contract and current control records — not the cancelled tender or a blended contract-value-per-meal calculation — as the source of truth for economics.

### Unsafe

> `The first tender was cancelled because its forecasting model was wrong.`

> `The 12 new lines are staffing costs.`

> `The successful tender added 12 employees.`

> `Boğaziçi pays 242.66 TL per meal.`

> `The current contract uses the same technical clauses as the cancelled tender.`

None is established.

---

# 11. Sources

1. Cancelled predecessor `2025/1335958`, notice + cancellation reason:  
   https://ekapveri.com/ihale/ekap-2025-1335958/  
   https://www.ihaledetay.com/2025-1335958
2. Cancelled predecessor public schedule surface:  
   https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4173515/cetvel/
3. Successful current procurement `2025/1727143`:  
   https://ekapveri.com/ihale/ekap-2025-1727143/  
   https://www.ihaledetay.com/2025-1727143
4. Successful public 15-item schedule surface:  
   https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4374218/

---

# 12. Bottom line

The cancelled and successful procurements share the same visible meal-volume headline but are **not interchangeable document sets**.

The correct current economic research chain is:

```text
FINAL SUCCESSFUL BID SCHEDULE
→ identify line-item classes
→ CURRENT Q_HAKEDIS per line
→ WINNING UNIT PRICE
→ penalties / fixed components
→ physical vs contract economic consequence
```

And P0-05 remains deliberately unresolved:

```text
CURRENT QUANTITY-PLANNING HEURISTIC
= must come from current operator evidence, not desk-research invention.
```