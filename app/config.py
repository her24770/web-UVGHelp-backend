from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    CORS_ORIGINS: str = "*"

    model_config = {"env_file": ".env"}


settings = Settings()
