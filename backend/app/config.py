from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "BOUNCAMPUS"
    APP_VERSION: str = "1.0.0-beta"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./data/db/campus.db"

    # Data paths
    DATA_DIR: str = "./app/data"
    GENERATED_DATA_DIR: str = "./data"
    MODELS_DIR: str = "./data/models"

    # Model constants. These are assumptions, not live tariffs/emission factors.
    CO2_PER_KWH: float = 0.47
    COST_PER_KWH: float = 2.8
    FOOD_WASTE_KG_PER_PORTION: float = 0.4

    # CORS: override with a JSON list in production, e.g.
    # CORS_ORIGINS='["https://your-project.vercel.app"]'
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
