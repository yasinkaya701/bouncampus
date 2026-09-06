# 🏫 BOUNCAMPUS

**Predict campus demand. Optimize campus resources. Act before waste happens.**

> A university campus knows tomorrow's timetable, weather and events — yet many campus resources are still operated reactively. What if the campus could know tomorrow's demand before tomorrow happens?

BOUNCAMPUS is a predictive campus sustainability platform built for **Boğaziçi University**. It uses occupancy forecasting to optimize energy consumption and food production across the campus.

## 🎯 Core Modules

| Module | Description |
|--------|-------------|
| **Occupancy Intelligence** | Predicts hourly building & floor occupancy using XGBoost |
| **Building Energy Optimizer** | Floor-level energy optimization using OR-Tools |
| **Cafeteria Demand Optimizer** | Food demand prediction with collaborative filtering |
| **Campus Action Engine** | Prioritized daily action recommendations |
| **Scenario Simulator** | What-if analysis (heatwave, exam week, events, etc.) |

## 🏗️ Architecture

```
CAMPUS DATA (Timetable, Weather, Events)
         ↓
   OCCUPANCY FORECASTER (XGBoost)
         ↓
   Campus Digital State
         ↓
  ┌──────┴──────┐
  ↓             ↓
ENERGY       FOOD
OPTIMIZER    OPTIMIZER
  ↓             ↓
  └──────┬──────┘
         ↓
  CAMPUS ACTION ENGINE
         ↓
  TODAY'S ACTION PLAN
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.11+ / FastAPI |
| ML Models | XGBoost, scikit-learn |
| Collaborative Filtering | implicit (ALS) |
| Optimization | Google OR-Tools |
| Database | SQLite |
| Frontend | Next.js 14 / React |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Map | Leaflet.js + OpenStreetMap |
| Deploy | Vercel (frontend) + Railway (backend) |

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Generate synthetic data and train models
python -m app.data.generator

# Start the API server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the dashboard.

## 📊 Impact Metrics

| Metric | Unit |
|--------|------|
| 🔌 Energy Saved | kWh |
| 🌍 CO₂ Avoided | kg CO₂e |
| 🍽️ Food Waste Avoided | kg |
| 💰 Cost Saved | ₺ (TL) |

## 🏛️ Campus Data

Built with **Boğaziçi University** real building data:
- **Güney Kampüs** (South Campus, Bebek) — 10 buildings
- **Kuzey Kampüs** (North Campus, Hisarüstü) — 11 buildings
- ~16,000 students, ~2,200 staff
- 2 main dining halls (660 + 159 seats)

> For the hackathon demonstration, we created a privacy-preserving synthetic campus dataset. The system is designed to work with existing campus timetable, BMS, and POS data.

## 👥 Team

| Role | Focus |
|------|-------|
| CS / Data & ML | Occupancy prediction, food demand model, data pipeline |
| CS / Platform | Dashboard, campus map, scenario simulator |
| Industrial Eng. | OR-Tools optimization, cost model, action engine |
| Electrical Eng. | Floor-level energy model, HVAC simulation |

## 📄 License

MIT

---

*Built for the Sustainability Hackathon — October 15, 2026*
