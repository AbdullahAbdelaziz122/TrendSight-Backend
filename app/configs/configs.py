from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # App
    APP_NAME: str = "My FastAPI App"
    DEBUG: bool = False
    
    # CORS
    # ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Cache the settings object creation
@lru_cache
def get_settings() -> Settings:
    """
    Returns cached Settings instance.
    This ensures .env file is read only once.
    """
    return Settings()