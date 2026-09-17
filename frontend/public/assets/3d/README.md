# Boğaziçi 3D asset provenance

BOUNCAMPUS has two complementary 3D layers.

## 1. Native campus geometry

The in-app `Geometry 3D` scene is generated from source-backed OpenStreetMap building footprints and metadata. It is rendered by the application instead of shipping scraped third-party model binaries. The existing `/api/v1/campus-geometry` route provides the footprint/height/roof metadata used by the Three.js scene.

OpenStreetMap data is subject to the Open Database License (ODbL). The application preserves source links for matched geometry.

## 2. Provider-hosted photogrammetry

The `Photogrammetry` view exposes public, provider-hosted Boğaziçi University photogrammetry scenes created by **Havadan Harita / Buğrahan Yeni** on Sketchfab.

| Asset | Campus | Sketchfab model ID | Repository policy |
| --- | --- | --- | --- |
| North Campus — 1-2-3-4-5 campus | North | `7ee0a7f38d434c519be728a3ab493722` | External embed only |
| North Campus — dormitories 6-7 | North | `d153dab298bd472787c6896063f9a9b7` | External embed only |
| Superdorm & indoor sports hall | Uçaksavar | `58f91e285e0c4a4dafff412ccc553ecf` | External embed only |
| New Geophysics Building | Kandilli | `364f2ef47974416baa046626efae4fa0` | External embed only |
| Indoor swimming pool | Anadolu Hisarı | `bc509269e0c747deb58b4a7b369fba0b` | External embed only |
| Dormitory building | Kilyos / Sarıtepe | `39aa2add49de4877bedf68e7d618e097` | External embed only |

Primary collection: <https://sketchfab.com/havadanharita/collections/bogazici-universitesi-kuzey-hisar-kampus-5181ff7662c8440db5d2b292b34a1f19>

Official campus reference: <https://harita.bogazici.edu.tr/>

Additional official/public construction documents were used only as corroborating evidence for campus/building identity and dimensional context, not as a source of redistributed model files:

- Uçaksavar: <https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/isgpl_faz_02_rev_20240503101742.pdf>
- Kandilli New Geophysics Building: <https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/jeofizik_isg_18_20240429121846.pdf>
- Kilyos/Sarıtepe: <https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/isgpl_faz_02_rev_20231005104413.pdf>

## Redistribution boundary

The public Sketchfab pages confirm that these scenes can be viewed/embedded. The repository does **not** assume that this also grants permission to redistribute downloaded GLB/GLTF/OBJ binaries. Until a model-specific downloadable license is independently verified, no third-party photogrammetry binary is copied into `public/` or committed to git.

If a future model has a verified redistribution license, add the exact license, author, original URL, retrieval date, checksum, and conversion pipeline to `photogrammetry-manifest.json` before vendoring it.
