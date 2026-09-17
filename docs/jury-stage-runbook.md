# BOUNCAMPUS — KREATE Jury Stage Runbook

## Objective

The live demo must prove four things in under 90 seconds:

1. the problem is real,
2. the product can make an operational decision,
3. the AI is bounded by uncertainty and a human,
4. success is measured by a falsifiable pilot rather than a synthetic impact claim.

Use `/demo` as the entrypoint. It redirects to the guided `/demo/jury` experience.

## 90-second choreography

### 00–16s — Problem

Say:

> Boğaziçi Üniversitesi 2025 için 48.251 kilogram yemek atığı yayımlıyor. Biz problemi tahmin etmiyoruz; resmi veriden başlıyoruz.

On screen:

- show `48,251 kg`,
- point to `OFFICIAL_PUBLIC`,
- do not open another product module.

### 16–36s — Decision

Say:

> Bir sonraki serviste tek bir kesin sayı vermiyoruz. Ders programı, hava, menü ve akademik takvim bağlamını bir araya getirip bir üretim bandı ve karar güveni üretiyoruz.

If live context is healthy:

- point to the band,
- point to signal coverage,
- point to missing-signal reason codes if any.

If live context is degraded:

- do **not** apologize,
- point to `WITHHOLD`,
- say: “Bağlam yoksa sayı uydurmuyoruz.”

This degraded path is a product proof, not a demo failure.

### 36–54s — Human gate

Say:

> Model tek başına mutfağa komut vermez. Yalnızca yeterli bağlam varsa kontrollü pilot onayı açılır; otomatik dispatch her durumda kapalıdır.

Actions:

1. show `HOLD` as the safe default,
2. if and only if `PILOT_READY`, click `Approve controlled pilot`,
3. point to `AUTO_DISPATCH=false`.

Never imply that the click sent a command to a real kitchen.

### 54–76s — Evidence

Say:

> Başarıyı da model ilan etmiyor. On dört günlük CONTROL ve INTERVENTION pilotunda ana KPI’mız 100 servis edilen öğün başına atık kilogramı. Hedefimiz en az yüzde 10 azalma; bu henüz sonuç değil.

Show:

- `kg / 100 served meals`,
- `≥10% TARGET_NOT_RESULT`,
- `5+5` minimum measured services,
- early-sellout guardrail.

Open Pilot Evidence Lab only if the jury asks how real data enters the system or if there is enough time.

### 76–90s — Close

Say exactly:

> 48 tonluk problemi raporlamıyoruz; bir sonraki öğünde oluşmasını önlemeye çalışıyoruz. Ama başarıyı AI söylemiyor — kontrollü pilot söylüyor.

Then stop talking and take questions.

## Fail-safe demo policy

The demo must remain credible under partial infrastructure failure.

### Official baseline available, live context unavailable

Expected product behavior:

- official problem metrics remain visible,
- live-context health shows `FALLBACK` or `PARTIAL`,
- operational recommendation becomes `WITHHOLD`,
- pilot approval remains disabled,
- no stale number is presented as current.

Presenter line:

> Bu gördüğünüz hata yönetimi değil sadece; ürün davranışı. Kritik bağlam yoksa operasyonel karar üretmiyoruz.

### Pilot scoring endpoint unavailable

Do not invent a scorecard. Show the blank CSV measurement contract and explain the pre-registered gates.

### Official source website cannot be opened on venue Wi-Fi

Do not retry repeatedly. The product contains the sourced baseline and provenance label. Mention that the official source URL is embedded and move on.

## What not to show first

Do not open the presentation with:

- energy optimization,
- shuttle routing,
- 3D campus assets,
- generic smart-campus language,
- scenario savings,
- CO2 or water numbers that have not been measured.

These are expansion capabilities, not the KREATE wedge.

## Presenter split for a 4-person team

Recommended split:

- **Speaker 1 — Problem / opening:** 00–16s
- **Speaker 2 — Decision engine:** 16–36s
- **Speaker 3 — Human gate + pilot:** 36–76s
- **Speaker 4 — close / scale / Q&A handoff:** 76–90s

If transitions feel slower than one sentence, use one primary presenter for the full 90 seconds and let the others own Q&A domains instead.

## Q&A ownership

- Product/problem/impact: Speaker 1
- Data/model/uncertainty: Speaker 2
- Pilot methodology/food operations: Speaker 3
- Scale/business/accelerator plan: Speaker 4

## Pre-stage checklist

Before presenting:

- open `/demo`,
- confirm the page reaches `/demo/jury`,
- confirm the official 48,251 kg baseline is visible,
- note whether live context is `LIVE`, `PARTIAL`, or `FALLBACK`,
- never refresh simply to chase a prettier live state,
- keep Pilot Evidence Lab in a second tab,
- keep the official source in a third tab only if network is reliable,
- rehearse both the live path and the `WITHHOLD` fail-safe path,
- keep the final line verbatim.

## Release acceptance criteria

The jury build is acceptable only if:

- `/demo` resolves to the guided jury mode,
- official evidence renders without the live food API,
- live API failure does not create a fake production number,
- `PILOT_APPROVED` is disabled unless the recommendation is genuinely `PILOT_READY`,
- Pilot Evidence Lab accepts strict CSV measurement imports,
- malformed CSV rows surface validation errors,
- export produces the same measurement schema,
- no achieved waste, CO2, or water savings are claimed without measured evidence,
- frontend typecheck, lint and production build pass.
