# TrayGate MVP Optical Geometry and Capture-Quality Gate

Issue: #296  
Parent: #119  
Owner: EHB — Embedded Hardware, Communications & Integration  
Evidence state: design-only (`ASSUMPTION`, `DATASHEET`, `CALCULATION`); no `BENCH_TEST` or `FIELD_TEST` claim.

## Decision

Use **Raspberry Pi Camera Module 3, standard visible-light variant** as the default RGB MVP camera for TrayGate. Use Camera Module 3 Wide only when the installation cannot provide the working distance required by the standard lens.

Reasons:
- at the same 4608 x 2592 sensor resolution, the standard lens keeps more pixels on the tray plane;
- controlled TrayGate geometry does not require an ultra-wide scene when sufficient vertical clearance exists;
- repeatable tray-plane sampling is more valuable than capturing unnecessary surroundings;
- powered autofocus can be used during calibration, then a per-device focus position can be locked for repeatable capture.

This is an EHB camera/geometry decision only. It does not define CS1 segmentation, food classification, leftover estimation, or model-confidence logic.

## Manufacturer facts

Raspberry Pi Camera Module 3 standard:
- Sony IMX708, 11.9 MP;
- full non-HDR output: 4608 x 2592;
- pixel size: 1.4 um;
- horizontal FoV: 66 degrees;
- vertical FoV: 41 degrees;
- powered autofocus;
- nominal focus range approximately 10 cm to infinity;
- official product price starts at USD 25.

Camera Module 3 Wide:
- same 4608 x 2592 sensor;
- horizontal FoV: 102 degrees;
- vertical FoV: 67 degrees.

Sources observed 2026-10-06:
- https://www.raspberrypi.com/products/camera-module-3/
- https://www.raspberrypi.com/documentation/hardware/camera/computers/camera_software.html
- https://www.raspberrypi.com/news/raspberry-pi-camera-module-still-image-capture/
- https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

Evidence class: `DATASHEET`.

## Provisional tray-plane envelope

Until the actual Boğaziçi tray/tabldot family is measured, use a conservative **600 mm x 400 mm required inspection envelope**.

Evidence class: `ASSUMPTION`. The fixture must replace this with measured dimensions before any field-ready claim.

## Working-distance calculation

For a camera at distance `d` from the tray plane:

```text
scene_width  = 2 * d * tan(horizontal_FoV / 2)
scene_height = 2 * d * tan(vertical_FoV / 2)
```

For Camera Module 3 standard at 550 mm:

```text
width  ~= 2 * 550 * tan(33 deg)   ~= 714 mm
height ~= 2 * 550 * tan(20.5 deg) ~= 411 mm
horizontal sampling ~= 4608 / 714 ~= 6.45 px/mm
vertical sampling   ~= 2592 / 411 ~= 6.30 px/mm
```

At 600 mm:

```text
width  ~= 779 mm
height ~= 449 mm
sampling ~= 5.9 px/mm horizontally and 5.8 px/mm vertically
```

First mechanical target:
- nominal optical height: **550-600 mm above tray plane**;
- camera axis approximately normal to the reference tray plane;
- tray guide keeps the full 600 x 400 mm inspection envelope inside the image with margin.

Evidence class: `CALCULATION` derived from `DATASHEET` FoV and the `ASSUMPTION` envelope.

## Standard vs wide fallback rule

For the provisional 600 x 400 mm envelope, the standard lens needs approximately 535 mm minimum working distance; the wide lens needs approximately 302 mm.

Decision rule:
1. if installation clearance provides >= 550 mm optical height, use the standard lens;
2. if measured clearance cannot provide it, evaluate the wide lens;
3. standard -> wide is a cross-role capture-geometry change and requires CS1 review;
4. no accuracy claim is allowed until the final lens/height combination is physically tested.

## Focus policy

**Do not use continuous autofocus during normal TrayGate capture.**

Commissioning procedure:
1. place the calibration target on the reference tray plane;
2. run autofocus once under controlled illumination;
3. record the resulting lens position for that physical camera;
4. switch to manual focus and apply the recorded position;
5. save it under `cameraCalibrationVersion`;
6. repeat after camera replacement, mount movement, optical-window change, or failed sharpness verification.

Raspberry Pi documents manual lens-position control and module-to-module calibration variation. Therefore one universal LensPosition value must not be copied across all stations.

## Exposure, white balance and HDR

Preferred operating mode:
- stable diffuse visible illumination;
- avoid direct specular LED reflection into the lens;
- establish exposure/gain/white-balance during calibration;
- keep them fixed for the validated lighting/geometry profile where practical;
- mark captures invalid when lighting leaves the calibrated envelope rather than silently creating an unvalidated image distribution.

Exact exposure/gain/white-balance values require physical calibration and are not invented here.

Default MVP capture is **non-HDR full resolution (4608 x 2592)**. Raspberry Pi documents Camera Module 3 HDR output at 2304 x 1296. TrayGate should first solve contrast with controlled lighting rather than halve each image dimension. HDR can be evaluated only if clipping remains and CS1 accepts the changed capture distribution.

## Lighting concept

```text
opaque / matte hood
        |
diffuse LED source(s)
       \|/
     [camera]
        |
reference tray plane
```

Requirements:
- visible-light, high-CRI diffuse source preferred;
- symmetric source placement around the optical path or behind a diffuser;
- no bare point LEDs producing strong wet-tray specular reflections;
- matte internal hood surfaces;
- image only the required tray inspection region, not faces or cafeteria-wide video;
- no illuminance number is claimed until exposure/noise bench measurements exist.

## Device-side capture-quality gate

Required checks:
1. tray is present and inside the inspection envelope;
2. frame is available and decodable;
3. no gross underexposure/overexposure;
4. no partial-tray clipping;
5. focus/sharpness passes the calibrated station threshold;
6. optional depth validity only when depth exists;
7. calibration version is present.

Use the already merged values: `VALID`, `BLURRED`, `UNDEREXPOSED`, `OVEREXPOSED`, `PARTIAL_TRAY`, `DEPTH_INVALID`, `DEVICE_ERROR`.

The gate is about capture validity only; it must not infer food semantics or identity.

## Sharpness acceptance procedure

Calibration target: planar checkerboard plus high-frequency/Siemens-star regions at image center and four tray-envelope corners.

Procedure:
1. warm camera/compute to normal operating state;
2. lock calibrated focus/exposure;
3. acquire at least 20 triggered frames without target movement;
4. verify the full inspection envelope is visible;
5. compute a sharpness metric independently on center + four corner regions (for example variance-of-Laplacian or Tenengrad);
6. record the per-region distribution as the station calibration reference;
7. derive the station threshold from measured repeatability with margin;
8. store metric, threshold and method under the calibration version;
9. a normal capture below threshold becomes `BLURRED` and is withheld;
10. never silently relax a failing threshold.

No magic numeric threshold is specified before hardware exists. A threshold copied from another camera is prohibited.

Evidence after execution:
- procedure/design: `ASSUMPTION`;
- optical geometry math: `CALCULATION`;
- manufacturer optical facts: `DATASHEET`;
- measured station distributions: `BENCH_TEST`;
- dish-return-line performance: `FIELD_TEST`.

## Recalibration triggers

Re-run optical calibration after camera replacement, mount/reference-plane movement, optical-window replacement, illumination replacement, repeated blur/exposure failures, or software changes to resolution/crop/compression/focus/exposure/HDR.

## Capture-contract preservation

This design does not change the merged minimum payload or privacy boundary. Changes to resolution/crop, intrinsics, mounting pose, illumination geometry, timing, calibration schema or capture-quality semantics require CS1 consumer review.

## Remaining physical evidence

This closes the **design decision** for #296. Before promotion beyond design, measure real tray dimensions, build the fixture, collect sharpness/exposure repeatability, set station thresholds, test cleaning/splash/steam effects, and verify trigger timing under representative tray motion.