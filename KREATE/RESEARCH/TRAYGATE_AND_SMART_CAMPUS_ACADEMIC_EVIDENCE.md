# Academic Evidence — TrayGate Measurement + Decision-First Smart Campus

**Research date:** 2026-10-04  
**Status:** Peer-reviewed/academic secondary evidence. External study results are **not** Boğaziçi performance claims.

---

# 1. Decision-first smart campus thesis

## A-SC-01 — IoT data must be connected to organizational decisions

Valks, Arkesteijn, Koutamanis & den Heijer (2020), *Building Research & Information*, studied IoT applications and campus-management decision processes across four cases.

Paper:
https://consensus.app/papers/towards-a-smart-campus-supporting-campus-decisions-with-valks-arkesteijn/b023f515363f52ec9e289cf4f57d6659/

Key evidence:

- dynamic campus use and resource pressure motivate better management information;
- IoT can supply real-time use-pattern information;
- the literature reviewed by the authors suggests IoT information is often **not used in organizational decision-making**;
- the study therefore analyzes process-level requirements needed to connect information to actual campus decisions.

### Product implication

This supports BOUNCAMPUS's architecture principle:

```text
named decision first
-> identify owner + timing + action space
-> identify missing observations
-> integrate/sense only what changes the decision
```

It does **not** establish demand for BOUNCAMPUS, nor that every campus domain benefits from more sensing.

### Forbidden interpretation

> "Academic research proves smart-campus IoT improves all university decisions."

The more defensible interpretation is the opposite: data infrastructure alone is insufficient unless mapped to the organizational process.

---

# 2. Tray/leftover vision is technically plausible in constrained institutional settings

## A-TV-01 — FLIC real-world university-canteen dataset

Piccoli et al. (2026), *Applied Sciences*, introduced **FLIC**, a real-world dataset for visual leftover estimation.

Paper:
https://consensus.app/papers/flic-a-realworld-dataset-for-visual-estimation-of-food-piccoli-callegaro/86121a44fad75dfd9d67cae3a85c3777/

Dataset/study characteristics reported in the abstract:

- operational university canteen;
- **22 days** of collection;
- **401 paired** full-tray / leftover-tray image acquisitions;
- pixel-precise semantic segmentation masks;
- physically measured food mass as ground truth;
- standard **2D RGB imagery**;
- segmentation models including U-Net, DABNet, DINOv2+FeatUp and SAM;
- assisted food recognition using the **fixed daily menu** to map broad operator input to a specific food class.

### Why this matters for TrayGate

The study strongly supports the **constrained-task formulation**:

```text
fixed institutional setting
+ daily known menu
+ tray image
+ food/no-food segmentation
+ physically measured calibration/ground truth
```

This is materially different from open-world "recognize any food in any photo."

### Design implication

TrayGate V1 should prioritize:

- fixed capture geometry;
- controlled lighting;
- known tray/compartment geometry;
- known daily menu;
- food-vs-empty / leftover proportion;
- confidence / WITHHOLD;
- temporary measured ground truth during calibration/evaluation.

### Boundary

The study highlights that visual mass estimation remains intrinsically challenging. Therefore BOUNCAMPUS must not claim production-grade gram accuracy before its own measured calibration/validation exists.

---

# 3. RGB-D can support food-volume/weight estimation, but calibration is food-specific

## A-TV-02 — RGB + depth dining-hall estimation

González et al. (2024), *Sensors*, evaluated dish counting/content identification and portion-size/weight estimation in a dining-hall/self-service setting.

Paper:
https://consensus.app/papers/automated-food-weight-and-content-estimation-using-gonzález-garcia/a5dd10aded415b73aabaaed97c84b8e2/

Reported approach:

- RGB imagery for dish/content identification;
- RGB + depth for volume estimation;
- food-specific density models;
- experimentally calibrated volume-to-weight conversion tables;
- validation examples using rice and chicken.

### Product implication

Depth can improve physical-volume reasoning, but **volume != mass without calibration/density assumptions**.

Therefore:

- RGB-only leftover percentage is a defensible first measurement target;
- optional RGB-D can estimate volume;
- gram-level mass estimates require food-specific calibration and measured validation;
- density/calibration versions must be part of provenance.

### Forbidden interpretation

Do not copy external error rates into TrayGate performance claims. Different food, tray geometry, camera placement, lighting and service workflow invalidate direct transfer.

---

# 4. Measurement architecture recommendation

## Tier 0 — use existing records

If the institution already records trustworthy service-level:

- produced portions;
- served portions;
- edible surplus;
- plate waste;

then BOUNCAMPUS should integrate these first.

## Tier 1 — simple physical counters

If denominator/flow data are missing:

- production/batch count;
- serving-line count;
- tray-return count.

Prefer deterministic counting over CV when it satisfies the decision requirement.

## Tier 2 — TrayGate RGB

Use when post-consumer leftover composition/proportion is decision-critical and existing measurement is insufficient.

Target output:

```text
tray_detected
capture_quality
menu_id
compartment_id
food_class_or_menu_mapping
leftover_percent
confidence
readiness
```

## Tier 3 — TrayGate RGB-D

Use only when volume materially improves the downstream decision and the operational/calibration burden is justified.

Target additional fields:

```text
estimated_volume
volume_uncertainty
camera_calibration_version
depth_quality
```

## Tier 4 — estimated mass

Only after measured calibration:

```text
estimated_mass
food_density_model_version
mass_calibration_dataset
mass_error_distribution
```

No production claim should skip directly from image segmentation to grams without this evidence chain.

---

# 5. Measurement validation protocol derived from literature

For a bounded TrayGate technical test:

1. fix camera/tray geometry;
2. use controlled lighting;
3. record menu identity;
4. capture full/reference and leftover trays where feasible;
5. obtain temporary scale-based ground truth for validation samples;
6. split evaluation by food type / texture class;
7. report segmentation and leftover-proportion metrics separately from mass error;
8. characterize failures for liquid/viscous/mixed foods;
9. include `WITHHOLD` for poor capture/depth/unknown-menu conditions;
10. do not silently exclude difficult trays.

### Useful evaluation hierarchy

```text
capture success
-> tray/compartment localization
-> food-vs-empty segmentation
-> leftover percentage calibration
-> optional volume error
-> optional mass error
-> operational throughput / failure rate
```

This prevents one headline metric from hiding the actual failure mode.

---

# 6. Product positioning consequence

TrayGate is **not** the primary differentiated company thesis because specialist food-waste vendors already use camera/scale or vision systems.

The stronger BOUNCAMPUS architecture is:

```text
existing institutional data where sufficient
+ optional measurement modules where missing
        ↓
source semantics / provenance
        ↓
uncertainty-aware decision
        ↓
human action
        ↓
measured outcome
```

TrayGate contributes only where post-consumer food measurement changes a real decision or validates an intervention.

---

# 7. Evidence boundaries for application/pitch

## Safe

- Academic research shows that constrained visual leftover estimation in university/canteen settings is technically plausible.
- Fixed menus and controlled institutional settings can simplify recognition compared with open-world food recognition.
- RGB-D can support volume estimation, while mass estimation requires calibration.
- Smart-campus research emphasizes connecting sensor information to actual organizational decision processes.

## Unsafe before BOUNCAMPUS technical tests

- "TrayGate measures grams accurately."
- "TrayGate is validated."
- "TrayGate works for every Turkish dish."
- "Our vision model achieves external-paper accuracy."
- "More sensors automatically improve campus operations."

---

# 8. Immediate research/test implication

Before investing further in TrayGate hardware, PMR should first answer:

> **Which waste-stage measurement is actually missing today, and what production/menu/portion decision would change if that measurement existed?**

If there is no decision consequence, do not add the sensor.
