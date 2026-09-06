# BOUNCAMPUS — Assumptions & Methodology

All calculations in BOUNCAMPUS are based on transparent, documented assumptions.
This page is accessible from the dashboard via the "ℹ️ Assumptions" button.

## Energy Assumptions

| Parameter | Value | Source | Notes |
|-----------|-------|--------|-------|
| CO₂ emission factor | 0.47 kg CO₂e/kWh | IEA Turkey 2023 | Grid average, includes all sources |
| Electricity cost | ₺2.80/kWh | EPDK commercial tariff 2026 | Mesken dışı abone |
| HVAC share of building energy | 40-60% | ASHRAE literature | Varies by building age/type |
| Lighting share | 15-25% | DOE building benchmarks | LED vs fluorescent considered |
| Base load (always-on) | 10-20% | BMS typical values | Elevators, security, servers |
| HVAC comfort target | 22°C | ISO 7730 | ±1°C depending on building |
| Eco mode savings | 60-80% floor energy | Literature estimate | Reduced HVAC + lighting |

## Food Waste Assumptions

| Parameter | Value | Source | Notes |
|-----------|-------|--------|-------|
| Average portion weight | 0.40 kg | UNEP Food Waste Index | Includes all menu items |
| Baseline overproduction | 10-15% | Industry average | Turkish university cafeterias |
| Safety buffer | 3-5% | Operational requirement | Avoids shortage |
| Menu popularity impact | ±15% demand variation | Synthetic estimate | Based on Google Trends data |

## Occupancy Model Assumptions

| Parameter | Value | Source | Notes |
|-----------|-------|--------|-------|
| Course attendance rate | 70-90% | University average | Varies by department/course type |
| Library usage | Peak 14:00-20:00 | BU library patterns | Higher during exam weeks |
| Exam week multiplier | 1.2-1.5x | Estimate | More students on campus |
| Rain impact | +10-15% indoor occupancy | Weather behavior studies | Students stay indoors |
| Weekend occupancy | 15-30% of weekday | Typical university | Library and dorms mainly |

## Campus Data Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Total students | ~16,173 | BU official data |
| Daily campus population | 12,000-15,000 | Estimate (weekday) |
| Academic buildings | 21 | BU campus data |
| Dining halls | 2 (660 + 159 seats) | BU facilities |
| Class hours | 08:30-17:20 (main) | BU academic schedule |
| Semester weeks | 14-16 | BU academic calendar |

## What These Numbers Mean

### Energy Saving Example
```
If 3 floors (each 50 kW) are consolidated into 1:
  Saved = 2 floors × 50 kW × 4 hours = 400 kWh
  CO₂ = 400 × 0.47 = 188 kg CO₂e
  Cost = 400 × ₺2.80 = ₺1,120
```

### Food Waste Example
```
If production is reduced from 1,500 to 1,330 portions:
  Saved = 170 portions × 0.40 kg = 68 kg food
  Cost ≈ 170 × ₺15 (avg ingredient cost) = ₺2,550
```

## Limitations

1. **Synthetic data**: Current demo uses generated data. Real-world accuracy depends on actual campus data integration.
2. **Energy model simplification**: Real HVAC systems have more complex dynamics (thermal inertia, zone controls).
3. **Food preference data**: Collaborative filtering accuracy improves with more user interaction data.
4. **Weather sensitivity**: Model assumes linear temperature-energy relationship; real buildings may have nonlinear responses.

## Privacy Statement

BOUNCAMPUS does not track individual students. All occupancy data is aggregated at the building/floor level.

- ❌ "Yasin Kaya is in Building A"
- ✅ "Building A expected occupancy = 182 people"

Food preferences use anonymized hash IDs with no connection to real student identities.
