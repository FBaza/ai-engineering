from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion de la aplicacion, cargada desde variables de entorno / .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ANTHROPIC_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: Literal["anthropic", "openai"] = "anthropic"
    LLM_MODEL: str = "claude-haiku-4-5"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def validar_clave_del_proveedor(self) -> "Settings":
        """Exige la clave del proveedor seleccionado (fail fast al arrancar, no en la primera peticion)."""
        if self.LLM_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY es obligatoria cuando LLM_PROVIDER=anthropic")
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY es obligatoria cuando LLM_PROVIDER=openai")
        return self


@lru_cache
def get_settings() -> Settings:
    """Settings como singleton: se valida una sola vez, al arrancar (fail fast)."""
    return Settings()
