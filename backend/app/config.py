from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "BOUNCAMPUS"
    DATABASE_URL: str = "sqlite:///./data/db/campus.db"
    
    # Data paths
    DATA_DIR: str = "./app/data"
    GENERATED_DATA_DIR: str = "./data"
    MODELS_DIR: str = "./data/models"
    
    # Energy constants
    CO2_PER_KWH: float = 0.47
    COST_PER_KWH: float = 2.8 # TL
    FOOD_WASTE_KG_PER_PORTION: float = 0.4
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
