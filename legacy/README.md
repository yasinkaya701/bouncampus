# Legacy archive

This directory contains source kept for historical reference only. Files under `legacy/` are intentionally outside the active application/runtime tree and must not be imported by production code.

## Archived surfaces

- `frontend/src/app/flow/page.tsx` — former `/flow` campus-flow prototype. It used hard-coded occupancy, queue, shuttle and library figures while presenting them as live operational values. The route was not part of the documented product surface, primary navigation, sitemap, or feature registry, so it was removed from the active Next.js route tree.

## Rule

Do not revive legacy code by linking or importing it directly. If an idea becomes product-relevant again, rebuild it against current source/provenance rules and the product truth boundary instead of reactivating mock telemetry.
