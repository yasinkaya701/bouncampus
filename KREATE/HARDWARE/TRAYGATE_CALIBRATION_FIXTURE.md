# TrayGate Calibration and Geometry Fixture

Issue: #300  
Parent: #119  
Owner: EHB — Embedded Hardware, Communications & Integration  
Evidence state: design-only; no physical fixture or measured result is claimed.

## Purpose

Define a repeatable non-energized reference fixture that lets EHB detect camera/lighting/geometry drift before invalid captures reach CS1.

The fixture is not a production scale and does not convert images to grams. A temporary scale may still be used separately for CS1 dataset ground truth.

## Reference stack

```text
camera mount datum
      |
controlled illumination datum
      |
calibration target plane
      |
tray-guide reference plane
      |
station base / mechanical datum
```

All optical checks are referenced to the same tray plane used in normal capture.

## Physical reference features

The fixture shall provide:
- a rigid reference tray plane;
- known X/Y dimensions covering the required inspection envelope;
- repeatable mechanical stops or locating pins for the calibration plate;
- four corner fiducials plus one center fiducial;
- checkerboard or equivalent camera-calibration pattern;
- high-frequency sharpness targets at center and four corners;
- a matte neutral patch and bright/dark reference patches for exposure checks;
- a visible fixture identifier/revision that is not person-identifying;
- a documented camera-to-plane height datum;
- a documented optical-axis/pose datum.

Exact dimensions are `ASSUMPTION` until the real tray family and station mechanics are measured.

## Calibration outputs

A successful calibration run produces a versioned station record containing at minimum:
- `cameraCalibrationVersion`;
- device identifier;
- camera module identity/serial if available without personal data;
- fixture revision;
- image resolution/crop/HDR mode;
- lens/focus position;
- exposure/gain/white-balance profile when locked;
- camera-to-reference-plane distance;
- estimated camera intrinsics and distortion terms when used;
- pose/registration result relative to fixture fiducials;
- center/corner sharpness metric distributions and thresholds;
- lighting/reference-patch measurements used by the capture-quality gate;
- timestamp and device software version;
- evidence label.

CS1 receives the version identifier through the existing capture contract; the detailed station calibration artifact remains an EHB verification record unless a cross-role change requires review.

## Commissioning procedure

1. install camera, optical window, lighting and tray guide;
2. clean the optical window using the intended service procedure;
3. place fixture on the tray-plane stops;
4. verify camera height and gross pose against mechanical datums;
5. acquire calibration frames under controlled lighting;
6. run autofocus once and capture the per-device lens position;
7. switch to the locked manual-focus policy;
8. estimate/check intrinsics and pose if the CS1 geometry profile depends on them;
9. collect at least 20 stationary frames for center/corner sharpness repeatability;
10. evaluate exposure/reference patches and clipping;
11. store the resulting calibration record under a new immutable version;
12. run the capture-quality gate using that version;
13. only `VALID` captures are eligible for CS1 ingestion.

## Pass/fail categories

Calibration must fail closed when any of these are outside the station's bench-derived limits:
- tray envelope not fully visible;
- camera pose or height outside tolerance;
- fiducials cannot be located reliably;
- center/corner sharpness below threshold;
- exposure reference patches outside limits;
- unacceptable clipping;
- required calibration metadata missing;
- optical window contamination prevents a valid check;
- fixture revision is unknown.

Failure must not silently create a new calibration version.

## Recalibration triggers

Create a new calibration version after:
- camera replacement;
- camera mount movement;
- tray-guide/reference-plane movement;
- optical-window replacement;
- lighting source/diffuser/driver replacement;
- resolution/crop/HDR/focus/exposure policy change;
- repeated `BLURRED`, `UNDEREXPOSED`, `OVEREXPOSED` or `PARTIAL_TRAY` events;
- enclosure service that can alter optical geometry;
- CS1 requests revalidation because the capture distribution changed.

## Routine verification

Before a pilot day or after maintenance, a short verification may reuse the current calibration version only if:
- fixture revision matches;
- fiducial/pose check remains inside the previously bench-derived tolerance;
- center/corner sharpness remains above stored thresholds;
- exposure/reference patches remain inside stored limits;
- no controlled setting changed.

Otherwise perform full recalibration and increment the calibration version.

## Ground-truth scale boundary

A scale is **not** part of the production TrayGate path.

If a temporary scale is used for model ground truth:
- record scale identity, calibration status, tare method and timestamp separately;
- link the measured sample to the anonymous capture/sample ID;
- never treat the scale as a required production sensor;
- never infer gram accuracy from the optical fixture alone.

## Evidence progression

| Claim | Allowed evidence now | Promotion requirement |
|---|---|---|
| fixture geometry concept | `ASSUMPTION` | measured mechanical artifact |
| FoV/working-distance math | `CALCULATION` | confirm after build |
| camera capabilities | `DATASHEET` | manufacturer source |
| pose/sharpness/exposure repeatability | none yet | `BENCH_TEST` with setup and raw results |
| dish-return operational robustness | none yet | `FIELD_TEST` |
| production calibration stability | none yet | `PRODUCTION_EVIDENCE` |

## Acceptance for the design slice

- reference plane and datums are explicit;
- calibration outputs are versioned;
- focus/sharpness and exposure verification are tied to the existing capture-quality contract;
- recalibration triggers are explicit;
- temporary ground-truth weighing is separated from the production workflow;
- no bench/field performance is fabricated.

This document closes the design artifact for #300. Physical tolerances and thresholds remain intentionally unresolved until the fixture is built and measured.