# python/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sorad School Accounts API"
    DATABASE_URL: str
    JWT_SECRET_KEY: str = "supersecretkeychangeinprod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Default admin login seeded automatically
    DEFAULT_ADMIN_EMAIL: str = "admin@soradschool.com"
    DEFAULT_ADMIN_PASSWORD: str = "Admin123!"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()