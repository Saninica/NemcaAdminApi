import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Unified Vendor Data API"
    DEBUG: bool = True

    DATABASE_URI: str = "postgresql+asyncpg://user:1234*@localhost/testdb"

    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SERVER_IP: str = "0.0.0.0"
    ROOT_PATH: str = "/api"

    class Config:
        env_file = ".env"

settings = Settings()
