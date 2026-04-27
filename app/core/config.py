from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_ENV: str = "development"
    DATABASE_URL: str
    CORS_ORIGINS: str = "*"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"

    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        if self.is_production:
            return f"{url}?ssl=true"
        return url


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
