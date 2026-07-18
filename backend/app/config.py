from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = BACKEND_ROOT.parent
ENV_FILES = (REPOSITORY_ROOT / ".env", BACKEND_ROOT / ".env")


class Settings(BaseSettings):
    """Runtime configuration that never contains a secret by default."""

    app_env: Literal["development", "test", "production"] = "development"
    app_version: str = "0.2.0"
    api_port: int = Field(default=8000, ge=1, le=65_535)
    cors_allowed_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:3001,http://127.0.0.1:3001"
    )
    max_intake_chars: int = Field(default=500, ge=1, le=2_000)
    max_body_bytes: int = Field(default=65_536, ge=1_024, le=1_048_576)
    procedure_data_mode: Literal["fixture", "disabled", "external"] = "fixture"
    rag_mode: Literal["disabled", "external"] = "external"
    llm_mode: Literal["disabled", "external"] = "external"
    rate_limit_enabled: bool = False
    rate_limit_requests: int = Field(default=60, ge=1, le=10_000)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3_600)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = ""
    openai_timeout_seconds: float = Field(default=20, ge=1, le=120)

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


_SETTINGS = get_settings()

# Backwards-compatible constants for existing modules.
APP_ENV = _SETTINGS.app_env
ALLOWED_ORIGINS = _SETTINGS.allowed_origins
OPENAI_API_KEY = _SETTINGS.openai_api_key
OPENAI_MODEL = _SETTINGS.openai_model
OPENAI_BASE_URL = _SETTINGS.openai_base_url
OPENAI_TIMEOUT_SECONDS = _SETTINGS.openai_timeout_seconds
