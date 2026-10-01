from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import actions, dashboard, energy, food, occupancy, operations, scenarios

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="BOUNCAMPUS campus intelligence and decision-support API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(occupancy.router)
app.include_router(energy.router)
app.include_router(food.router)
app.include_router(operations.router)
app.include_router(actions.router)
app.include_router(scenarios.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health",
        "decision_capabilities": "/api/v1/decision/capabilities",
        "truth_boundary": "decision-support models; no live university BMS/POS/turnstile telemetry claimed",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
