from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECONFORGE_", env_file=".env", extra="ignore")

    app_env: str = "development"
    api_keys: str = "local-dev-key:developer"
    rate_limit_requests: int = Field(default=120, ge=1, le=100_000)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)
    max_import_rows: int = Field(default=10_000, ge=1, le=1_000_000)
    webhook_timeout_seconds: float = Field(default=3.0, gt=0, le=30)
    webhook_max_attempts: int = Field(default=3, ge=1, le=10)
    default_currency: str = "USD"
    log_level: str = "INFO"

    @field_validator("default_currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        value = value.strip().upper()
        if len(value) != 3 or not value.isalpha():
            raise ValueError("default_currency must be a three-letter code")
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        level = value.strip().upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("unsupported log level")
        return level


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
  # internal: 509018
  # internal: 143010
