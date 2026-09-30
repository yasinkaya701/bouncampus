# Türkiye University Dining Reservation Signals — Forecasting Alternative & Hybrid Input

**Research date:** 2026-10-01  
**Status:** Public-source secondary research. Presence of reservation systems at other universities does not prove Boğaziçi's normal-term workflow or data access.

## Executive conclusion

A critical product assumption has changed:

> **Demand forecasting is not the only credible way to reduce university dining uncertainty in Türkiye. Reservation/intent systems are already used by multiple universities specifically to plan meal quantities and reduce waste/shortage risk.**

Therefore BOUNCAMPUS must not frame the problem as "universities do not know tomorrow's diners, so they need ML." Some institutions obtain an explicit intent signal.

The stronger design space is:

```text
historical demand
+ academic/service regime
+ menu context
+ reservation / intent signal when available
+ expected no-show / late-demand uncertainty
        ↓
operator decision
        ↓
production quantity / mix / allocation
```

The key PMR question becomes:

> **What is the cheapest, lowest-friction signal available before the production freeze point, and what uncertainty remains after using it?**

---

# R-01 — Kayseri University expanded reservation campus-wide in April 2026

`PUBLIC SOURCE`

Kayseri University announced that its reservation-based dining system, previously used at the 15 Temmuz Campus, would expand to all university campuses from **6 April 2026**. Students and staff are instructed to reserve via **Halkbank Kampüste**.

The announcement also differentiates service for reserved vs non-reserved users and charges a higher fee for non-reserved dining.

Source:
https://sksd.kayseri.edu.tr/tr/duyuru-detay/10301/yemekhane-rezervasyon-sistemi-duyurusu

**Implication:** institutions can use pricing/service design to increase reservation coverage; demand management is partly a behavior/incentive problem, not only prediction.

---

# R-02 — Recep Tayyip Erdoğan University explicitly links reservation to production and waste prevention

`PUBLIC SOURCE`

Recep Tayyip Erdoğan University's dining announcement explains that its reservation system was introduced to reduce waste, improve quality and avoid students being left without meals. Reservations close before the service day; after the reservation period ends, **the quantities are communicated to the contractor and production preparation begins**.

Source:
https://sks.erdogan.edu.tr/tr/news-detail/yemekhane-rezervasyon-sistemi/4787

The university explicitly states that knowing the number of meals to prepare is intended to prevent both insufficient delivery and excess food when diners do not arrive.

## Product implication

This is strong sector evidence that a **pre-production demand signal can directly enter the contractor workflow**.

But reservation still may not equal realized demand. Questions remain:

- no-show rate;
- late/unreserved demand;
- cancellation behavior;
- reservation deadline vs ingredient/cooking freeze;
- menu-choice specificity;
- campus/location changes after reservation.

A hybrid model may add value by estimating the residual uncertainty around reservations.

---

# R-03 — İzmir Katip Çelebi University states the operational reason directly

`PUBLIC SOURCE`

A September 2026 İKÇÜ notice says reservations must be completed before a cutoff so that dining can be **planned according to the daily number of people**, sufficient food can be prepared without service interruption, and unnecessary production/food waste can be reduced.

Source:
https://sks.ikcu.edu.tr/Duyuru/

**Implication:** the product problem is recognized operationally in the sector, but institutions may choose reservation rather than passive forecast as the control mechanism.

---

# R-04 — Fırat University moved to a reservation system in 2026

`PUBLIC SOURCE`

Fırat University announced transition to a meal reservation system in June 2026 through a bank-protocol-supported flow.

Sources:

- https://fenf.firat.edu.tr/tr/announcements-detail/52017
- https://ogrencidekanligi.firat.edu.tr/announcements-detail/52108

**Implication:** reservation capability can be bundled with campus-card/payment infrastructure rather than purchased as standalone sustainability software.

---

# R-05 — Erzincan Binali Yıldırım University uses next-day reservation cutoffs

`PUBLIC SOURCE`

EBYÜ states that reservation is used across multiple dining locations and reservations can be made through Halkbank Kampüste / Rapor.al, with a cutoff on the day before the meal.

Source:
https://sks.ebyu.edu.tr/yemekhane-rezervasyon-sistemi-hakkinda/

**Implication:** banking/payment partners and generic institutional reservation systems are part of the substitute landscape.

---

# R-06 — Additional sector signals

Public university sources show meal reservation flows at several other institutions, including:

- Karadeniz Technical University — campus-card reservation:  
  https://bilgiislem.ktu.edu.tr/sks/duyuru/yemek-hizmetleri-hakkinda-duyuru
- Burdur Mehmet Akif Ersoy University — MAKÜ Net / campus-card reservation:  
  https://htmyo.maku.edu.tr/tr/yemekhane
- Amasya University — reservation explicitly framed around preventing waste:  
  https://sksdb.amasya.edu.tr/2025-2026-egitim-ogretim-yili-beslenme-hizmetleri-hakkinda-bilgilendirme
- Ankara Music and Fine Arts University — reservation system introduced for efficient public-resource use and waste prevention:  
  https://www.mgu.edu.tr/yemek-rezervasyon-sistemi/
- Afyonkarahisar Health Sciences University — reservation used for planning and sustainable service:  
  https://skultur.afsu.edu.tr/ogrenciye-beslenme-hizmetleri-ve-rezervasyon-sistemi-hakkinda-bilgilendirme-yapildi/

This is a purposive set of public examples, not a prevalence estimate across Türkiye.

---

# R-07 — There is also a university-developed reservation product

`PUBLIC SOURCE — product description`

Altınbaş University publicly describes **MyMeal**, a university-developed meal reservation system offering personnel reservation, meal tracking/management, calorie information and QR-based reservation scanning, with integration capability for institutional applications.

Source:
https://software.altinbas.edu.tr/mymeal/index_tr.html

**Competitive implication:** universities may build/share their own reservation tooling; BOUNCAMPUS should not treat reservation UX as a novel moat.

---

# R-08 — Boğaziçi has demonstrated reservation capability in special-service conditions

`PUBLIC SOURCE`

For the 2026 Kurban Bayramı service plan, Boğaziçi announced that Kilyos meal service would use a reservation flow through `kart.boun.edu.tr`. Reservations for meals had to be submitted by the previous day at 18:00; un-cancelled/no-show meals were treated as taken for balance deduction.

Source:
https://yemekhane.bogazici.edu.tr/node/493

Boğaziçi's normal dining FAQ separately confirms BUCard and BUCAMPUS QR-based turnstile use for meal access:

https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

## What this supports

- Boğaziçi has had the technical/operational ability to collect explicit meal intent for at least a special-service case.
- The university has digital meal-access infrastructure.

## What this does **not** support

- normal-term daily reservation is currently used;
- the special-event reservation data are available to the team;
- reservation should replace forecasting;
- the same cutoff would work in normal high-volume service;
- no-show behavior under the special service generalizes to term-time dining.

---

# Forecast vs reservation vs hybrid

| Strategy | Strength | Weakness | Best when |
| --- | --- | --- | --- |
| Passive forecast | zero user friction; can cover all diners | irreducible uncertainty; depends on history/context | reservations unavailable/unpopular |
| Mandatory reservation | strong explicit intent signal | user friction; late demand; no-shows; exclusion risk | institution can enforce and users comply |
| Incentivized reservation | better coverage without hard exclusion | pricing/equity complexity | institution can design incentives |
| Hybrid reservation + forecast | uses explicit intent plus residual uncertainty model | more integration complexity | reservations cover meaningful but imperfect demand |
| Batch/replenishment control | reacts to early actual service | operational/cooking constraints | production can be staged |

---

# Product architecture implication

Do not hard-code BOUNCAMPUS as a pure forecasting product.

The decision engine should eventually be able to treat signals as adapters:

```text
historical_service_counts
reservation_counts
cancellation_counts
menu_preferences
academic_calendar
campus/service_regime
allowed aggregate occupancy/context signals
weather/events if they add value
```

and explicitly report which signals were available before the decision deadline.

A future recommendation could be:

```text
reserved: 4,820
expected reservation no-show: 6%
expected unreserved demand: 510
recommended production: 5,070–5,180
operator guardrail: preserve 3% reserve batch
```

This is only a design example; no Boğaziçi values are established.

---

# PMR questions added by reservation research

## Boğaziçi Food Services / contractor

1. Is reservation used during normal academic-term service anywhere, or only special periods?
2. Why was reservation chosen for the 2026 holiday/Kilyos service?
3. What worked and what failed?
4. What was the no-show/cancellation rate?
5. Was the reservation count used to change production quantity?
6. When was the count visible relative to kitchen freeze time?
7. Could the same workflow scale to normal service volume?
8. Would mandatory reservation create unacceptable student friction/equity/service issues?
9. Is a softer intent signal preferable to hard reservation?
10. If a reservation count existed, what uncertainty would still remain for the kitchen?

## Students

Only after operator need is established:

- What reservation cutoff would be tolerable?
- How often would plans change after reserving?
- Would an incentive/price difference change compliance?
- What happens when a student forgets to reserve?

Student preference alone must not determine the production-control architecture.

---

# Strategic decision rule

### Forecasting wedge strengthens if

- reservation is absent or low coverage;
- mandatory reservation is operationally undesirable;
- enough historical/context data exist;
- production can react before service.

### Hybrid wedge strengthens if

- reservation exists but no-show/unreserved demand remains material;
- the reservation signal is accessible before the production decision;
- operator needs a safety-stock/batch recommendation rather than a raw count.

### Reservation-first wedge strengthens if

- explicit intent dramatically reduces uncertainty;
- users accept it;
- integration is easy;
- forecasting adds little incremental decision value.

The team should let PMR/pilot evidence choose among these rather than defending ML for its own sake.
