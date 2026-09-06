# BOUNCAMPUS — Architecture

## System Overview

```
CAMPUS DATA
│
┌──────────────┼──────────────┐
│              │              │
Timetable    Weather      Events
│              │              │
└──────────────┼──────────────┘
               ↓
     OCCUPANCY FORECASTER
        (XGBoost Model)
               ↓
      Campus Digital State
    (Building × Hour × Floor)
               ↓
   ┌───────────┴────────────┐
   ↓                        ↓
ENERGY OPTIMIZER      FOOD OPTIMIZER
(OR-Tools +           (XGBoost +
 Floor Energy Model)   Collaborative
   ↓                   Filtering)
   ↓                        ↓
Building Actions      Meal Production
   └───────────┬────────────┘
               ↓
      CAMPUS ACTION ENGINE
     (Priority: HIGH/MED/LOW)
               ↓
   ┌─────────────────────┐
   │  TODAY'S ACTION PLAN │
   │  Cards + Timeline    │
   └─────────────────────┘
```

## Data Flow

### Input Sources
1. **Timetable/Courses** → Scheduled students per building per hour
2. **Weather** → Temperature, rain, humidity (affects HVAC + outdoor behavior)
3. **Events** → Extra people, special schedules
4. **Historical Data** → Past occupancy patterns, sales, energy consumption
5. **Menu Data** → Dish popularity scores, user food preferences

### Processing Pipeline
1. Feature engineering combines all inputs into prediction features
2. XGBoost model predicts `occupancy_ratio` per building × floor × hour
3. Energy model calculates `P_floor = P_base + P_HVAC(T, occ) + P_lighting(occ)`
4. OR-Tools solver minimizes energy while meeting capacity constraints
5. Food optimizer predicts demand with collaborative filtering adjustment
6. Action Engine ranks all recommendations by impact

### Output
- Dashboard KPIs (occupancy, energy, food, savings)
- Interactive campus map with building status
- Prioritized action cards (HIGH/MEDIUM/LOW)
- Scenario comparison (original vs modified)

## API Architecture

```
Frontend (Next.js)
    ↓ REST API
Backend (FastAPI)
    ├── /api/v1/dashboard    → Complete dashboard data
    ├── /api/v1/occupancy    → Occupancy forecasts
    ├── /api/v1/energy       → Energy optimization
    ├── /api/v1/food         → Food demand prediction
    ├── /api/v1/actions      → Action recommendations
    ├── /api/v1/scenarios    → What-if simulation
    ├── /api/v1/buildings    → Building metadata
    └── /api/v1/metrics      → Impact metrics
```

## Energy Model Detail

### Floor-Level Calculation
```
P_floor = P_base + P_HVAC + P_lighting

P_HVAC = α × |T_outside - T_target| × (0.3 + 0.7 × occupancy_ratio)
P_lighting = P_light_max × (0.1 + 0.9 × occupancy_ratio)
```

### Building Profiles
| Profile | Base Load | HVAC α | Lighting Max | T_target |
|---------|-----------|--------|-------------|----------|
| Historic (Perkins, Anderson) | Higher | Higher | Medium | 22°C |
| Modern (Kare Blok, New Hall) | Lower | Lower | Higher | 22°C |
| Library | Medium | Medium | High | 21°C |
| Dining | Medium | High | Medium | 23°C |
| Dormitory | Low | Medium | Low | 22°C |

## Optimization Formulation

### Energy Consolidation (OR-Tools MIP)
```
Minimize: Σ E(b,f) × x(b,f) + λ × C(b,f) × x(b,f)
Subject to: Σ Cap(b,f) × x(b,f) ≥ Expected_Occupancy × (1 + buffer)
            x(b,f) ∈ {0, 1}
```

### Food Production
```
Recommended = Predicted_Demand × (1 + safety_buffer)
Waste_Avoided = Baseline_Production - Recommended
```

## Assumptions

All assumptions are transparent and displayed on the dashboard:

| Assumption | Value | Source |
|-----------|-------|--------|
| CO₂ per kWh | 0.47 kg | Turkey grid average (IEA) |
| Energy cost | ₺2.8/kWh | EPDK commercial tariff |
| Food waste per portion | 0.4 kg | UNEP food waste estimate |
| HVAC proportion | ~40-60% of building energy | Literature average |
| Safety buffer (food) | 3-5% | Industry standard |
