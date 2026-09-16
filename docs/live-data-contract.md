# BOUNCAMPUS Live Data Contract

This document defines what BOUNCAMPUS is allowed to call **live**, what is an **official snapshot**, and what is a **model estimate**. The distinction is part of the product contract and must remain visible in API responses and the UI.

## Provenance classes

| Class | Meaning | Current examples |
|---|---|---|
| `OFFICIAL_LIVE` | Fetched at request/revalidation time from a public Boğaziçi University service | SKS cafeteria page, Mekik shuttle system, Academic Calendar |
| `OFFICIAL_SNAPSHOT` | Data originated from an official public Boğaziçi source but is bundled as a dated local snapshot | BUIS/ÖBİKAS public course schedule snapshot |
| `EXTERNAL_LIVE` | Live third-party source measured/modelled for campus coordinates | Open-Meteo weather for Bebek |
| `MODEL_ESTIMATE` | BOUNCAMPUS calculation derived from inputs/assumptions; not a sensor reading | occupancy, energy, food demand, savings, CO2 avoided |
| `FALLBACK` | Upstream source failed or timed out | source outage / parser failure |

## Current official/public feeds

### Cafeteria
- Source: `https://yemekhane.bogazici.edu.tr`
- Owner: Boğaziçi University SKS
- Cache/revalidation: 15 minutes
- Product rule: if structured fields cannot be parsed, show the source as reachable but **do not invent a dish**.

### Shuttle
- Source: `https://mekik.bogazici.edu.tr/`
- Current product route: Güney Meydan -> Kuzey Kampüs
- Cache/revalidation: 5 minutes
- Product rule: timetable values are official live page values. They are not GPS vehicle positions.

### Academic Calendar
- Source: `https://akademiktakvim.bogazici.edu.tr/`
- Cache/revalidation: 15 minutes
- Product rule: calendar events may affect scenario features; they do not imply actual attendance unless another source supplies attendance.

### Course Schedule
- Source: `https://registration.bogazici.edu.tr/BUIS/General/schedule.aspx`
- Current implementation: repository snapshot captured 2026-09-06
- Product rule: course schedule is official-source data but **not live enrollment or turnstile occupancy**.
- Before hackathon: refresh the snapshot after registration/add-drop changes and record the new capture timestamp.

### Weather
- Source: Open-Meteo, Bebek campus coordinates
- Provenance: `EXTERNAL_LIVE`
- Product rule: never describe this as a Boğaziçi weather station.

## Decision-model contract

### Occupancy
Input: public course schedule snapshot, room-to-building mapping, room-capacity assumptions.
Output: estimated scheduled classroom load.

Not currently available: card/turnstile counts, Wi-Fi association counts, camera counts, room sensors.

### Energy
Input: estimated scheduled load, building energy profile, external weather.
Output: physics-lite baseline and low-use optimization estimate.

Not currently available: BMS, smart-meter or utility telemetry. Therefore `predicted_energy_mwh`, savings and CO2 values are model outputs.

### Cafeteria demand
Input: scheduled lunch-period class flow and weather modifier.
Output: meal-demand estimate.

Not currently available: SKS POS transaction stream or kitchen production telemetry.

## Runtime health

`GET /api/v1/health`

Returns:
- aggregate status: `ok` or `degraded`
- source-level `ok` state
- provenance and fetch timestamp
- request latency

A single upstream source failure must not make the whole dashboard crash. It must degrade visibly and must not be silently replaced by a fabricated live value.

## Release gates

A pull request is hackathon-demo ready only when:
1. `npm ci` passes.
2. `npm run typecheck` passes.
3. `npm run lint` passes.
4. `npm run build` passes.
5. critical JSON datasets parse successfully.
6. `/api/v1/health` returns at least one official Boğaziçi source as healthy in the deployed environment.
7. UI labels all model KPIs as `MODEL TAHMİNİ`.
8. no screen claims BMS, sensor, POS, GPS, ISO certification or real-time occupancy unless such an integration is actually connected and verified.

## Next integrations for a real campus pilot

Highest-value Boğaziçi-owned integrations, subject to university authorization:
1. anonymized Wi-Fi/AP occupancy counts or turnstile aggregates;
2. BMS/smart-meter energy telemetry by building/floor;
3. SKS anonymized POS totals by meal and 15-minute interval;
4. shuttle GPS/AVL feed if available;
5. room-capacity master data and current course enrollment counts.

These integrations should enter through the same provenance layer so the existing model estimates can be calibrated rather than silently replaced.
