import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Sistema de Gestión de Alquileres")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres123@localhost:5432/alquileres_db"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "desarrollo_secreto_cambiar_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ]
    
    # Timezone
    TIMEZONE: str = os.getenv("TIMEZONE", "America/La_Paz")
    
    # Configuración de mora (Bolivia)
    TASA_MORA_DIARIA_DEFAULT: float = 0.5  # 0.5% por día
    
    class Config:
        case_sensitive = True


settings = Settings()
