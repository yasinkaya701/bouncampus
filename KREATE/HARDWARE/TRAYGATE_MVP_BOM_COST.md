# TrayGate MVP BOM and Cost Envelope

Issue: #297  
Parent: #119  
Owner: EHB — Embedded Hardware, Communications & Integration  
Price observation date: 2026-10-06

## Scope

This BOM covers the **MVP RGB capture station** needed to generate repeatable TrayGate captures and deliver them through the merged EHB↔CS1 contract.

It does not price a full production rollout, custom PCB, installation labor, CS1 model development, or a physically validated wet-environment enclosure.

## Architecture priced

```text
Tray presence trigger
        |
Camera Module 3
        |
Raspberry Pi 5 capture/runtime
        |
local queue -> Ethernet/Wi-Fi -> CS1
        |
controlled diffuse lighting
        |
mount + splash/cleaning enclosure concept
```

Default optics are defined in `TRAYGATE_OPTICAL_CAPTURE_GATE.md`.

## Base RGB capture-station BOM

| Item | Qty | Selected / constrained part | Unit USD | Evidence | Notes |
|---|---:|---|---:|---|---|
| Capture compute | 1 | Raspberry Pi 5, **1GB** | 45 | `DATASHEET` / official current price | Capture/runtime suitability is still an `ASSUMPTION`; no local-CS1-inference claim |
| RGB camera | 1 | Raspberry Pi Camera Module 3, standard visible-light | 25 | `DATASHEET` / official current starting price | 11.9MP IMX708; autofocus/manual focus control |
| USB-C PSU | 1 | Raspberry Pi 27W 5.1V/5A supply or approved equivalent | 12-20 | electrical spec `DATASHEET`; price range `ASSUMPTION` | Re-check approved reseller at procurement |
| Storage | 1 | 64GB high-endurance microSD | 8-15 | `ASSUMPTION` | OS + durable queue; endurance class to be finalized |
| Camera interconnect | 1 | correct Pi 5 CSI cable + strain relief | 5-10 | `ASSUMPTION` | Final length follows mechanical layout |
| Controlled lighting | 1 | high-CRI visible LEDs + diffuser + driver | 20-35 | `ASSUMPTION` | Freeze after illumination bench test |
| Tray trigger | 1 | short-range ToF / break-beam / photoelectric class | 10-25 | `ASSUMPTION` | Final technology depends on geometry/steam validation |
| Enclosure + optical window + mount | 1 | splash/cleaning-resistant serviceable concept | 30-60 | `ASSUMPTION` | Not an IP-rating claim |
| Cabling/glands/connectors/fasteners | 1 lot | low-voltage installation hardware | 10-20 | `ASSUMPTION` | Include strain relief |
| Cooling | 1 | Pi 5 active cooler/equivalent if thermal test requires it | 0-10 | `ASSUMPTION`; optional | Final enclosure may require it |

## Cost envelope

Excluding optional cooling:
- low estimate: **USD 165**;
- high estimate: **USD 255**.

With up to USD 10 cooling allowance:
- planning envelope: **USD 165-265 per prototype station**.

Evidence class: `CALCULATION` from the table above. This is deliberately a range, not a procurement quote.

## Official price/spec facts used

### Raspberry Pi 5 1GB

Raspberry Pi introduced the 1GB Pi 5 at **USD 45**; its 1GB price remained unchanged through the 1 October 2026 memory-price update.

Sources:
- https://www.raspberrypi.com/news/1gb-raspberry-pi-5-now-available-at-45-and-memory-driven-price-rises/
- https://www.raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/

### Camera Module 3

The official product page states Camera Module 3 is available from **USD 25** and specifies the 11.9MP IMX708 sensor.

Source:
- https://www.raspberrypi.com/products/camera-module-3/

### Raspberry Pi 27W power supply

Manufacturer electrical specification: 5.1V, 5.0A, 25.5W output; 100-240VAC input. The Pi 5 launch article documented a USD 12 launch price, but this BOM uses **USD 12-20 as a procurement assumption** and requires a current approved-reseller re-check.

Sources:
- https://www.raspberrypi.com/products/27w-power-supply/
- https://www.raspberrypi.com/news/introducing-raspberry-pi-5/

## Why 1GB Pi 5 is the base

The base EHB station must capture frames, run capture-quality checks, timestamp/version events, persist a local queue, retry idempotently, expose diagnostics and upload to CS1. Those duties do not inherently require a large-RAM board.

However, suitability of 1GB under the final workload remains an `ASSUMPTION` until profiled. If CS1 requires local inference on the same node, memory/compute must be re-profiled instead of silently increasing the base BOM.

## Optional local-inference upgrade

Official Raspberry Pi price announcements show materially higher 2026 prices for larger-memory Pi 5 variants. For planning, moving from the USD 45 1GB base to a roughly USD 110 4GB Pi 5 adds about **USD 65** before any accelerator, storage or thermal changes.

Therefore:
- capture-only baseline stays 1GB unless profiling disproves it;
- local inference is a separate SKU/configuration decision;
- do not buy inference headroom until CS1 supplies measured runtime requirements.

Evidence: official vendor announcements; cost delta is `CALCULATION`.

## Excluded costs

The USD 165-265 prototype envelope excludes:
- VAT / Turkish taxes;
- shipping / customs;
- reseller markup beyond observed official pricing;
- custom metalwork or CNC;
- custom PCB fabrication/assembly;
- installation labor / facilities work;
- production-certified IP enclosure testing;
- network drops / switches;
- tools and test equipment;
- spare inventory;
- calibration labor;
- CS1 model training/inference infrastructure;
- cloud/object-storage cost;
- temporary ground-truth scale;
- field pilot support.

These exclusions must accompany any quoted prototype cost.

## Sourcing and technical risks

| Risk | Current state | Mitigation |
|---|---|---|
| Raspberry Pi memory prices are volatile in 2026 | official vendor increases observed | keep 1GB base; re-check approved reseller on purchase date |
| Türkiye camera/board availability | not verified here | record seller/date/currency/MPN before purchase |
| Trigger under steam/wet reflections | unverified | compare break-beam, ToF and industrial photoelectric in #298 |
| LED CRI/flicker claims | unverified | select traceable source and measure exposure/flicker before freeze |
| Enclosure cost after cleanability/IP requirements | unverified | retain range until mechanical concept is selected |
| microSD wear from queue writes | unverified | use high-endurance media and test queue pattern in #299 |

## Sourcing alternates and change gates

| Function | Baseline | Allowed alternate | Change gate |
|---|---|---|---|
| Capture compute | Raspberry Pi 5 1GB | Pi 5 2GB/4GB when measured workload requires more memory | profile final capture/runtime workload; update cost envelope |
| RGB camera | Camera Module 3 standard | Camera Module 3 Wide when measured installation clearance cannot support standard-lens geometry | rerun tray-plane coverage math and obtain CS1 capture-distribution review |
| Storage | 64GB high-endurance microSD | equivalent traceable high-endurance media with equal-or-greater capacity | validate queue-write endurance and power-loss recovery |
| Tray trigger | short-range ToF / break-beam / photoelectric class | another listed trigger class | bench-test wet/steam/reflection behavior before freeze |
| PSU | official Raspberry Pi 27W PSU | electrically compliant, traceable equivalent | verify voltage/current, connector, thermal behavior, and local safety requirements before deployment |

Alternates are not automatic substitutions: camera, compute, trigger, storage, and power changes must preserve the validated interface and rerun the affected acceptance checks.

## Procurement rule

Before purchase:
1. prefer Raspberry Pi Approved Reseller pricing for Pi/camera/PSU;
2. record seller, date, currency, VAT/shipping treatment and manufacturer part number;
3. do not replace camera/lens with a similar part without rerunning optical geometry and CS1 change control;
4. record observed cost as a dated observation, never a guaranteed future price.

## Acceptance implications

The BOM is not complete merely because parts are orderable. Promotion beyond design still requires actual tray dimensions, optical fixture validation, lighting repeatability, trigger reliability, enclosure thermal testing, power-loss/restart/queue testing, cleaning/splash serviceability review and CS1 end-to-end contract validation.

## Decision summary

For hackathon/MVP planning:
- use **USD 165-265** for one RGB capture prototype station;
- budget at least **~USD +65** if moving from 1GB to 4GB Pi 5 for local inference, before inference-specific extras;
- keep depth hardware out of the base BOM until RGB evaluation demonstrates a justified need.

This closes the cost-envelope design work for #297 without claiming purchase, assembly, bench performance or field performance.