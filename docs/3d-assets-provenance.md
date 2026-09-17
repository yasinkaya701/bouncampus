# Boğaziçi 3D asset provenance

Last reviewed: 2026-09-17

BOUNCAMPUS separates **renderable source-backed geometry** from **high-detail visual references**. This prevents a public viewer from being mistaken for a redistribution license.

## Repository-rendered geometry

| Source | Coverage | Use | License / boundary |
| --- | --- | --- | --- |
| OpenStreetMap / Overpass | South, North, Hisar, Uçaksavar, Kandilli, Anadolu Hisarı, Kilyos campus bounds | Building footprints, tagged height/levels, roof shape/material/colour where available | ODbL 1.0; retain `© OpenStreetMap contributors` attribution and ODbL notice |

Source and license: https://www.openstreetmap.org/copyright

Implementation:

- `frontend/src/app/api/v1/campus-geometry/route.ts` — campus-wide footprint geometry.
- `frontend/src/app/api/v1/building-locations/route.ts` — named building matching and exact OSM record URLs.
- `frontend/src/lib/campus-geometry.ts` — explicit visualization fallback rules when OSM height/roof detail is missing.

Missing heights are visualization estimates, not survey measurements.

## High-detail external photogrammetry references

The following models are hosted by Sketchfab and attributed in the public viewer to **Havadan Harita / Buğrahan Yeni**. Their model binaries are not checked into BOUNCAMPUS until model-specific redistribution rights are independently verified.

| Coverage | Sketchfab UID | Repository treatment |
| --- | --- | --- |
| North Campus buildings 1–5 | `7ee0a7f38d434c519be728a3ab493722` | Provider-hosted embed only |
| North Campus dormitories 6–7 | `d153dab298bd472787c6896063f9a9b7` | Provider-hosted embed only |
| Uçaksavar Campus — Superdorm / KSS | `58f91e285e0c4a4dafff412ccc553ecf` | Provider-hosted embed only |
| Kandilli — New Geophysics Building | `364f2ef47974416baa046626efae4fa0` | Provider-hosted embed only |
| Kilyos Campus — Dormitory Building | `39aa2add49de4877bedf68e7d618e097` | Provider-hosted embed only |
| Anadolu Hisarı Campus — Indoor Pool | `bc509269e0c747deb58b4a7b369fba0b` | Provider-hosted embed only |

Collection reference for North / Hisar models:
https://sketchfab.com/havadanharita/collections/bogazici-universitesi-kuzey-hisar-kampus-5181ff7662c8440db5d2b292b34a1f19

Canonical model pages can be addressed as `https://sketchfab.com/models/<UID>`; embeds use `https://sketchfab.com/models/<UID>/embed`.

The Kilyos model is also referenced as a project 3D scan in Turkish Ministry seismic-resilience / energy-efficiency documentation, which supports provenance of the scan but does **not** by itself grant BOUNCAMPUS redistribution rights.

## Acceptance rule for future binary assets

A GLB/GLTF/OBJ/texture package may enter `frontend/public/assets/3d/` only when all of the following are recorded:

1. exact original source URL and model/revision identifier;
2. author/owner attribution;
3. explicit redistribution and derivative-work license evidence;
4. SHA-256 checksum of the imported source and optimized output;
5. transformation pipeline (decimation, texture conversion, Draco/KTX2, coordinate transform, etc.);
6. campus/building mapping and placement metadata.

Unknown or ambiguous licenses remain link/embed-only.
