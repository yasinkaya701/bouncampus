from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import occupancy, energy, food, actions, scenarios, dashboard

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(occupancy.router)
app.include_router(energy.router)
app.include_router(food.router)
app.include_router(actions.router)
app.include_router(scenarios.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Welcome to BOUNCAMPUS API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
