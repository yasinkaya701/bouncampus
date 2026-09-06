# BOUNCAMPUS — Pitch Script

## Opening (30 seconds)

> "A university campus knows tomorrow's timetable, weather, and events — yet many campus resources are still operated reactively."
>
> "Every day, buildings are heated for empty floors. Cafeterias prepare meals that end up as waste. Study spaces sit idle while others overflow."
>
> "What if the campus could know tomorrow's demand — before tomorrow happens?"

## Introduce BOUNCAMPUS (30 seconds)

> "Meet BOUNCAMPUS — a predictive campus sustainability platform."
>
> "BOUNCAMPUS uses one core intelligence: **occupancy forecasting**. We predict where and when people will be on campus tomorrow. Then we use that prediction to optimize two critical resources: **energy** and **food**."
>
> "Built for Boğaziçi University — 16,000 students, 21 buildings, 2 campuses."

## How It Works (60 seconds)

> "The system works in three layers:"
>
> 1. **Occupancy Intelligence** — Our XGBoost model predicts hourly building occupancy using timetable data, weather, events, and historical patterns.
>
> 2. **Optimization Engine** — OR-Tools solves a building consolidation problem: which floors need to be active? How many meals should be prepared?
>
> 3. **Campus Action Engine** — All recommendations are ranked by impact and delivered as actionable cards.

*[Show architecture diagram]*

## Demo (3-4 minutes)

### Demo Flow:
1. Show dashboard overview (KPIs, map)
2. Click on a building → show hourly occupancy forecast
3. Show action cards → explain a HIGH IMPACT recommendation
4. Run scenario simulator:
   - "What if tomorrow is exam week?"
   - Show before/after comparison
5. Show impact metrics

### Key Demo Moments:
- Map zooms into Kuzey Kampüs, Kare Blok glows red at 10:00, green at 18:00
- Action card: "Kare Blok floors 3-5 can enter eco mode after 18:00 → Save 184 kWh"
- Scenario: Exam week → campus occupancy +35%, energy +22%, food +21%
- System automatically updates the action plan

## Impact (30 seconds)

> "For Boğaziçi University, our model estimates daily potential:"
>
> | Metric | Impact |
> |--------|--------|
> | Energy saved | ~800 kWh/day |
> | CO₂ avoided | ~376 kg/day |
> | Food waste avoided | ~68 kg/day |
> | Cost saved | ~₺14,820/day |
>
> "That's **~₺5.4M** and **137 tonnes of CO₂** per year."

## Why This Is Different (30 seconds)

> "Boğaziçi already has motion sensors and automated lights. That's reactive automation."
>
> "BOUNCAMPUS is the **predictive layer** that sits on top. It doesn't replace existing systems — it makes them smarter by knowing demand before it happens."
>
> "And the same intelligence layer can extend to:"

```
Occupancy Intelligence
    ↓
Energy | Food | Mobility | Water | Waste | Cleaning | Space
```

## Close (15 seconds)

> "We built BOUNCAMPUS to work with existing campus data — timetables, weather, POS systems. No new hardware needed."
>
> "Predict campus demand. Optimize campus resources. Act before waste happens."
>
> "BOUNCAMPUS."

---

## Q&A Preparation

### Likely Questions

**Q: How accurate is your occupancy prediction?**
A: On synthetic data, XGBoost achieves ~85% R² for next-day prediction. With real campus data integration (BMS, card swipe), accuracy would improve significantly.

**Q: Why not use deep learning?**
A: For structured tabular data with clear features (schedule, weather, calendar), gradient boosting outperforms neural networks. It's also more interpretable — we can show which features drive predictions.

**Q: How would you handle privacy?**
A: We never track individuals. All data is aggregated at building/floor level. Food preferences use anonymized hash IDs. The system only needs "how many people" not "which people."

**Q: What's the data integration effort for a real deployment?**
A: We need 3 data sources: (1) timetable/course registration, (2) weather API (free), (3) cafeteria POS. BMS integration is optional but improves energy model accuracy. Timeline: 2-4 weeks.

**Q: Why OR-Tools instead of simple rules?**
A: Building consolidation is a combinatorial optimization problem. With 21 buildings × 4-6 floors, there are millions of possible configurations. OR-Tools finds the mathematically optimal solution in milliseconds.
