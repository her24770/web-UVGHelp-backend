from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    CORS_ORIGINS: str = "*"
    JWT_SECRET: str = "cambia-esto-en-produccion"
    JWT_EXPIRE_HOURS: int = 24

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
