# Boğaziçi Feedback & Alternative Root-Cause Signals — 2026-10-04

**Purpose:** prevent BOUNCAMPUS from over-attributing the published food-waste total to production-demand mismatch.  
**Status:** public-source context only. **Not causal evidence for food waste.**

## Executive conclusion

Boğaziçi already collects several kinds of food-service feedback, and official sources contain non-trivial signals around meal quality, taste, portion sufficiency, physical capacity and user preference.

This matters because the production-forecasting thesis can be wrong even if food waste is high. A material share of waste could instead be driven by:

- taste / perceived quality;
- menu composition and preference;
- portion-size mismatch;
- service experience;
- preparation/cooking quality;
- downstream plate waste.

Therefore PMR and any pilot must separate **unserved edible surplus** from **plate/post-consumer waste** and explicitly test these alternative causes.

---

## 1. Daily pre-service tasting exists

Boğaziçi Food Services publicly states that volunteer students can join tastings before lunch and dinner, and that participants complete a short evaluation form.

Official sources:
- https://yemekhane.bogazici.edu.tr/yemek-tadim-etkinligi
- https://sks.bogazici.edu.tr/en/announcements/food-tasting-event/4165

### Implication

The institution already has a pre-service quality feedback mechanism.

Do **not** infer that tasting scores are stored in a structured dataset or are available to BOUNCAMPUS.

PMR question:
> What decisions, if any, change after a poor tasting result, and are those results retained at meal-item/service level?

---

## 2. Menu preference voting exists

Boğaziçi publicly operates a weekly menu-voting mechanism through BUCampus for Wednesday lunch, where authenticated users select among alternatives.

Official sources:
- https://yemekhane.bogazici.edu.tr/menu-anketi
- https://bilgiislem.bogazici.edu.tr/tr/news/kampus/2/bucampusun-yeni-versiyonu-yayinda/3351

### Boundary

A preference vote is **not** a reservation, attendance commitment or served-meal count.

### Research implication

Preference may be a useful menu-level feature, but only if historical vote snapshots can be linked to actual service demand without leakage.

It may also help diagnose downstream food acceptance rather than only forecast attendance.

---

## 3. 2025 Food Services reports a 2,386-person satisfaction survey

The official 2025 SKS activity report states:

- 2,386 participants in a satisfaction survey;
- feedback was shared;
- a live request/complaint area was added to the dining website;
- daily meal rating through BUCampus is a 2026–2027 target.

Official source:
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

### What this proves

Food-service quality/user feedback is an active management concern.

### What it does not prove

The public report does not expose the detailed 2025 response distribution or show that any specific complaint causes food waste.

PMR should ask whether the underlying survey has meal-level or issue-level data and whether recurring quality/menu complaints align with waste observations.

---

## 4. Official 2024 employee survey shows food quality/taste is a plausible alternative factor

Boğaziçi's official 2024 employee satisfaction survey reports the following dining-service scores:

- `quality and taste`: **55.50**;
- `portion adequacy`: **64.50**;
- `dining hall physical capacity`: **59.29**;
- `would prefer university dining among alternatives`: **61.02**.

Official source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/79-2024-yili-calisan-memnuniyeti-anketi-yayin-20251016-014308.pdf

### Important boundary

This is an **employee satisfaction** survey, not a food-waste study and not a student-only sample.

The scores do not establish that poor taste or portion size caused any measured waste.

### Why it matters

They are enough to reject the assumption that the only plausible cause worth testing is quantity forecasting.

A correct PMR sequence must ask:

```text
when food remained,
was it:
  cooked but unserved surplus?
  food served but returned?
  prep/cooking loss?

and if returned:
  was taste/quality/menu/portion a factor?
```

---

## 5. Official reporting shows user-experience interventions are ongoing

The 2025 SKS report lists measures including:

- tasting events;
- menu voting;
- request/complaint channel;
- package meal expansion;
- meal-access changes;
- future daily meal scoring.

This suggests the institution is already actively modifying service design and feedback systems.

### Product consequence

BOUNCAMPUS should not position itself as introducing "feedback" or "digital dining management" from scratch.

The more defensible gap to test is:

> Are these existing signals connected to the production/allocation decision before its freeze point, and are outcomes later reconciled with the decision?

---

## 6. Root-cause decision tree for PMR

For each concrete waste incident, classify the dominant mechanism before deciding what product to build:

```text
food remaining / wasted
|
+-- pre-consumer edible surplus
|   +-- demand lower than expected
|   +-- batch/allocation error
|   +-- contract/service buffer
|   +-- unexpected closure/regime change
|
+-- plate/post-consumer waste
|   +-- taste/quality
|   +-- portion too large
|   +-- menu mismatch/preference
|   +-- temperature/service quality
|   +-- diner behavior/satiety
|
+-- preparation/process waste
    +-- trimming
    +-- cooking error
    +-- storage/handling
    +-- quality rejection
```

The first branch supports production-decision intelligence most directly.
The second may require menu/portion/quality interventions.
The third may require process or kitchen-operations interventions.

---

## 7. High-value PMR prompts added by this evidence

- "When a meal has high waste, how do you distinguish unserved food from tray-return waste?"
- "Tell me about the last meal that students disliked. Did that affect returned food or next-service planning?"
- "Are tasting scores or satisfaction complaints connected to specific menu items/services?"
- "Do menu-vote results influence how much of an item is produced, or only which item is selected?"
- "When portions are judged too large/small, who can change grammage and on what timeline?"
- "What percentage of food-waste attention internally is about production surplus versus plate waste?"

---

## 8. Application claim firewall

Safe:
> Boğaziçi operates multiple feedback mechanisms around dining quality and menu preference, and official employee survey data show quality/taste and capacity are meaningful service dimensions.

Unsafe:
> Poor taste causes X% of Boğaziçi food waste.

Unsafe:
> Production forecasting is the dominant cause of Boğaziçi food waste.

Both causal claims require direct service-level evidence.

---

## Current strategic conclusion

The food-production wedge remains plausible, but the research now strengthens the need for a **root-cause stage split before intervention selection**.

The PMR should be capable of returning one of three outcomes:

- **KEEP** production-quantity decision intelligence;
- **MODIFY** toward portion/menu/quality or batch/allocation decision support;
- **KILL** the current food-production wedge if measured waste is mostly outside its causal reach.
