# CS1 Solar Exposure & Site Planning Design

## Goal
Extend the existing CS1 campus-operations decision layer so it can answer two operator questions without pretending to have a calibrated building simulation: (1) which rooms/classes receive direct sun at a given time, and (2) which candidate orientation for a new building is preferable under explicit registered daylight/heat weights.

## Architecture
Add one shared backend decision module, `backend/app/decision/solar_site_planning.py`, rather than duplicating solar logic inside class scheduling and energy review. The module provides deterministic solar position, room/facade exposure analysis, class-session linkage, and candidate building-orientation ranking. Existing class scheduling consumes precomputed per-room/per-slot exposure as an optional loss component; solar geometry remains advisory and never overrides hard capacity/feature/conflict feasibility.

## Inputs
- campus latitude/longitude
- timezone-aware ISO-8601 timestamps
- room geometry: room/building IDs, facade azimuth, window area, optional solar transmittance, optional caller-supplied obstruction elevation
- optional class sessions: class ID, room ID, timestamp
- new-building facade program: relative facade azimuth plus explicit daylight/heat sensitivity weights
- optional room `solar_load_by_slot` map for class scheduling

## Outputs
### Existing buildings
- sun azimuth/elevation for each sample
- mean direct exposure index per room
- window-area-weighted direct-gain index (dimensionless geometry proxy)
- affected class sessions above a caller-registered threshold
- explicit limitations and `REVIEW_REQUIRED` / `WITHHOLD` state

### New buildings
- ranked candidate orientations
- per-facade exposure and registered loss breakdown
- recommended orientation candidate for review
- `automatic_design_selection = false`

### Class scheduling
The existing min-cost assignment retains its hard feasibility rules. Optional `solar_exposure_weight >= 0` adds `solar_exposure_weight * room.solar_load_by_slot[slot]` to the registered assignment loss. Missing solar maps are neutral; malformed maps fail closed only when the solar weight is active.

## Solar geometry semantics
Use the compact NOAA solar-position approximation with conventional east-positive longitude and timezone-aware local timestamps. Facade exposure is a vertical-plane incidence proxy: direct exposure is zero when the sun is below the horizon, behind the facade, or below a caller-supplied obstruction elevation. This is not 3D ray tracing, a Radiance daylight model, CFD, a calibrated thermal model, SHGC simulation, or an achieved energy/comfort result.

## Truth boundary
Every solar/site result remains operator-reviewed. The product must state:
- no calibrated daylight or thermal prediction;
- no automatic HVAC/lighting/design actuation;
- obstruction geometry is caller supplied;
- no achieved energy, carbon, cost, comfort, or learning-performance claim;
- candidate orientation scores are registered relative-sensitivity units, not economic savings.

## API
Extend `/api/v1/ops/capabilities` with `solar_exposure` and `site_orientation`. Add:
- `POST /api/v1/ops/solar`
- `POST /api/v1/ops/site-orientation`
Pass optional `solar_exposure_weight` through `POST /api/v1/ops/classes`.

## Testing
- solar position sanity at Boğaziçi/Istanbul coordinates
- south vs north facade direct exposure
- obstruction horizon blocking
- class-session linkage
- deterministic new-building orientation ranking
- malformed geometry fails closed
- class scheduler prefers lower-exposure room only when solar weight is active
- invalid room solar map fails closed when active
- legacy class scheduling remains unchanged when solar weight is zero
- API capability/parameter wiring regression
