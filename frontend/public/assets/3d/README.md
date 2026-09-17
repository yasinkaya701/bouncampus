# BOUNCAMPUS 3D assets

This directory is the public boundary for repository-owned 3D assets.

## Current rendering source

BOUNCAMPUS currently derives campus building geometry from OpenStreetMap building footprints and metadata through:

- `/api/v1/campus-geometry`
- `/api/v1/building-locations`

OpenStreetMap data is licensed under ODbL 1.0. The application must retain `© OpenStreetMap contributors` attribution and make the ODbL data license clear.

## High-detail photogrammetry

High-detail Boğaziçi photogrammetry models discovered on Sketchfab are registered in `frontend/src/lib/campus-3d-assets.ts` and displayed from their provider-hosted embed URLs.

Their binary GLB/GLTF/OBJ files are intentionally **not** copied into this repository because BOUNCAMPUS has not independently verified model-specific redistribution rights. A public model page or embeddable viewer is not treated as permission to redistribute the model binary.

If a model-specific license is later verified, add the binary only with:

1. the exact source URL and model UID;
2. author attribution;
3. license name and permanent license URL or evidence;
4. SHA-256 checksum;
5. conversion/optimization steps;
6. a note explaining whether derivatives may be redistributed.

Do not import geometry from Google Maps / Google Earth or other sources whose terms do not grant redistribution rights.
