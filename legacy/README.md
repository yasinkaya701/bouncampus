# Legacy archive

This directory contains source kept for historical reference only. Files under `legacy/` are intentionally outside the active application/runtime tree and must not be imported by production code.

## Archived surfaces

- `frontend/src/app/flow/page.tsx` — former `/flow` campus-flow prototype. It used hard-coded occupancy, queue, shuttle and library figures while presenting them as live operational values. The route was not part of the documented product surface, primary navigation, sitemap, or feature registry, so it was removed from the active Next.js route tree.

## Archived backend utilities

- `backend/synthetic-training/generator.py` — former data generator that deterministically synthesized weather, occupancy, cafeteria demand and waste-like fields from assumptions. It is retained only for provenance; it must not be treated as measured campus data or a production data-ingestion path.
- `backend/synthetic-training/generate_and_train.py` — former convenience entrypoint that regenerated those synthetic datasets and trained legacy models from them. Docker/runtime startup did not invoke this script, so it was removed from the active backend tree.

The existing backend datasets are not moved by this cleanup because legacy backend model code still reads them at runtime. Their presence must not be interpreted as measured university telemetry.

## Archived documentation

- `docs/platform-walkthrough-pre-food-waste.md` — previous platform-wide walkthrough built around a four-stage Mission Control demo, a 30-day pilot and energy/CO₂ expansion metrics. The active KREATE release now uses the narrower five-beat food-waste jury flow and 14-day matched pilot documented in `docs/jury-demo-script.md`, `docs/hackathon-product-release.md` and the root README.

## Rule

Do not revive legacy code or documentation by linking or importing it directly. If an idea becomes product-relevant again, rebuild it against current source/provenance rules and the product truth boundary instead of reactivating mock telemetry, synthetic training data, or superseded pitch flows.
