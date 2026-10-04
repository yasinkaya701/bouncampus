# TrayGate — EHB / CS1 Ownership and Interface Contract

## Purpose

TrayGate is the cafeteria dish-return measurement station used to quantify leftover food on returned trays/tabldots without adding a manual weighing step to the normal dishwashing workflow.

The product boundary is intentionally split:

- **EHB owns the physical capture system and device reliability.**
- **CS1 owns the computer-vision / decision-intelligence pipeline and waste analytics.**

The station should fit into the existing dirty-tray return / scraping / dishwashing flow and require no routine operator action beyond the existing tray handling process.

## Core operating flow

```text
Returned tray/tabldot
        ↓
EHB capture station
(RGB / optional depth + controlled lighting + trigger)
        ↓
Capture contract
        ↓
CS1 TrayGate Intelligence
(tray/compartment detection → food/empty segmentation →
 menu-conditioned interpretation → leftover estimate → confidence)
        ↓
Meal-level waste analytics / pilot evidence / dashboard
        ↓
Existing scraping / sorting / dishwashing flow
```

## EHB ownership — TrayGate Hardware

EHB is the final owner of the physical and embedded system required to produce repeatable, timestamped captures.

EHB owns:

- dish-return / dishwashing-line mechanical integration;
- camera selection and mounting geometry;
- RGB camera implementation;
- optional RGB-D / ToF / depth sensing implementation;
- controlled LED illumination and glare/shadow control;
- tray-presence detection and automatic capture trigger;
- tray positioning / guide geometry when needed for repeatability;
- enclosure and mounting suitable for a wet, frequently cleaned food-service environment;
- edge compute selection where capture-side compute is required;
- device-side power architecture;
- Ethernet / Wi-Fi / other approved network connectivity;
- device identity and provisioning;
- camera calibration storage/versioning;
- frame capture and device-side capture-quality checks;
- local buffering / store-and-forward behavior;
- retry, reconnect and idempotent upload behavior;
- firmware and device service software;
- BOM and sourcing;
- maintainability, cleaning access and replacement strategy;
- hardware verification plan and acceptance tests.

### EHB does NOT own

EHB must not implement or silently redefine:

- food classification semantics;
- food-vs-empty segmentation logic;
- leftover percentage calculation;
- menu-conditioned inference;
- model confidence thresholds;
- model WITHHOLD / READY decision semantics;
- meal-level waste analytics.

Those belong to CS1.

## CS1 ownership — TrayGate Intelligence

CS1 is the final owner of the software/model pipeline that converts valid TrayGate captures into waste measurements and decision-grade aggregates.

CS1 owns:

- tray/tabldot detection;
- tray pose normalization when required;
- compartment / region-of-interest detection;
- food-vs-empty segmentation;
- use of known daily menu / service context to reduce the classification search space;
- food-item attribution when attribution is justified by the available context;
- leftover fraction / percentage estimation;
- optional depth-assisted volume estimation when calibrated depth data are available;
- uncertainty / confidence estimation;
- abstention / `WITHHOLD` behavior for low-quality or ambiguous captures;
- per-tray result schema;
- meal/service-level aggregation;
- per-food leftover statistics;
- training / validation dataset construction;
- model evaluation and baseline comparison;
- calibration and drift detection;
- API/backend integration;
- dashboard/product integration;
- pilot measurement metrics and model-performance reporting.

### CS1 does NOT own

CS1 must not make final hardware decisions for:

- camera model;
- lens / mounting geometry;
- illumination hardware;
- enclosure;
- mechanical tray guide;
- power architecture;
- wet-environment protection;
- networking hardware;
- embedded buffering / firmware implementation.

Those belong to EHB.

## EHB → CS1 capture contract

Minimum capture payload:

```json
{
  "deviceId": "traygate-01",
  "captureId": "tg-2026-10-04-000123",
  "timestamp": "2026-10-04T12:34:56+03:00",
  "rgbFrame": "<object-store-or-local-reference>",
  "depthFrame": null,
  "trayDetected": true,
  "captureQuality": "VALID",
  "cameraCalibrationVersion": "cam-cal-v1",
  "deviceSoftwareVersion": "tg-device-v1"
}
```

`depthFrame` is optional. RGB-only operation must remain possible for early pilots.

Recommended `captureQuality` values:

- `VALID`
- `BLURRED`
- `UNDEREXPOSED`
- `OVEREXPOSED`
- `PARTIAL_TRAY`
- `DEPTH_INVALID`
- `DEVICE_ERROR`

CS1 must treat non-`VALID` captures conservatively and may return `WITHHOLD`.

## CS1 output contract

Minimum inference result:

```json
{
  "captureId": "tg-2026-10-04-000123",
  "mealId": "2026-10-04-lunch-north",
  "trayId": "anonymous-tray-000123",
  "items": [
    {
      "food": "pilav",
      "leftoverPercent": 31,
      "confidence": 0.91
    },
    {
      "food": "tavuk",
      "leftoverPercent": 8,
      "confidence": 0.94
    }
  ],
  "readiness": "READY",
  "modelVersion": "traygate-intelligence-v1"
}
```

Recommended readiness values:

- `READY`
- `REVIEW_REQUIRED`
- `WITHHOLD`

## MVP measurement strategy

The first product target is **menu-conditioned leftover quantification**, not open-world food recognition.

The MVP should exploit constraints that make the problem tractable:

1. fixed or bounded camera geometry;
2. controlled illumination;
3. known tray/tabldot family;
4. known meal/service time;
5. known daily menu where available;
6. known or detectable tray compartments;
7. confidence-aware abstention.

Preferred progression:

1. food-vs-empty segmentation;
2. per-compartment leftover percentage bands;
3. continuous leftover percentage;
4. optional RGB-D volume estimation;
5. mass-equivalent estimates only after measured calibration evidence exists.

The system must not claim gram-level accuracy from RGB imagery unless validated against measured ground truth.

## Ground truth and calibration

A scale may be used temporarily during dataset creation or validation to provide ground truth, but **a scale is not part of the required production TrayGate workflow**.

Ground-truth collection may use:

- manual pre/post weighing;
- food-specific weighed samples;
- known container/compartment geometry;
- RGB-D volume references;
- human annotation.

Any conversion from image/depth output to grams must record the calibration method and evidence class.

## Privacy boundary

TrayGate should image only the tray inspection region required for measurement.

Default design goals:

- no face capture;
- no person identification;
- no student identity linkage;
- no biometric processing;
- no unnecessary cafeteria-wide video retention.

The preferred product artifact is a per-tray measurement event, not surveillance video.

## Acceptance criteria

### EHB acceptance

EHB is complete for an MVP station when it can demonstrate, with the correct evidence label:

- repeatable tray capture at the defined inspection point;
- controlled illumination sufficient for the CS1 evaluation dataset;
- timestamped captures with stable device identity;
- valid calibration metadata;
- automatic triggering without routine operator interaction;
- safe and cleanable physical integration concept;
- defined behavior for network loss and device restart;
- a documented BOM and verification plan.

### CS1 acceptance

CS1 is complete for an MVP intelligence path when it can demonstrate:

- tray/ROI detection on the agreed capture geometry;
- food-vs-empty segmentation baseline;
- menu-conditioned leftover estimation;
- explicit model metrics on held-out data;
- confidence / abstention behavior;
- per-tray structured output through the agreed contract;
- service-level waste aggregation;
- no unsupported production-accuracy or waste-reduction claims.

## Cross-role change control

Changes to any of the following require EHB + CS1 review because they can change model behavior or physical capture quality:

- image resolution / compression;
- camera intrinsics or mounting pose;
- depth representation;
- illumination geometry;
- capture timing;
- tray positioning assumptions;
- calibration schema;
- capture-quality semantics;
- payload/schema fields used by inference.

EHB owns the physical source of the data. CS1 owns the interpretation of that data. Neither role may change the cross-boundary contract unilaterally.
